#!/usr/bin/env python3
"""
hygiene.py — findet und entfernt unsichtbare Zeichen in Text und Metadaten in Bildern.

Nur stdlib, keine Installation noetig.

BEWUSST NICHT ENTHALTEN
-----------------------
Kein Angriff auf statistische Wasserzeichen (SynthID-Text o. ae.), kein C2PA-Stripping,
kein Umschreiben von Text. Solche Verfahren zielen darauf, die Herkunft KI-generierter
Inhalte zu verschleiern -- seit dem 02.08.2026 verlangt Art. 50 EU AI Act genau das
Gegenteil. Dieses Werkzeug hilft dabei nicht und soll es auch nicht.

Was hier passiert, ist die andere Richtung: Hygiene, und die Angriffsflaeche verkleinern.
Unsichtbare Zeichen brechen CSV-Importe, SQL-Suchen und Mail-Rendering, und sie sind ein
bekannter Traeger fuer Prompt-Injection (OWASP LLM01, MITRE ATLAS AML.T0051.001).
Bild-Metadaten transportieren GPS-Koordinaten aus Handyfotos.

VERWENDUNG
----------
  hygiene.py scan  [DATEI...|-]     Text pruefen         (Exit 1 = Fund, fuer CI/Hooks)
  hygiene.py clean [DATEI...|-]     Text saeubern        (stdout, oder -i fuer in-place)
  hygiene.py img-scan  BILD...      Bild-Metadaten zeigen
  hygiene.py img-clean BILD...      Bild-Metadaten entfernen

  --clip        liest aus der Zwischenablage (pbpaste); bei clean zurueck (pbcopy)
  -i            Datei direkt ueberschreiben statt nach stdout
  --spaces      exotische Leerzeichen auf normales Space normalisieren
                (NBSP bleibt sonst erhalten: in deutscher Typografie legitim, z. B. "5 %")
  --aggressive  img-clean entfernt zusaetzlich das ICC-Farbprofil
  -q            nur Zusammenfassung
"""

from __future__ import annotations

import argparse
import subprocess
import sys

# ---------------------------------------------------------------- Zeichenklassen

# Unsichtbar und in Fliesstext nie legitim. Traeger fuer versteckte Instruktionen.
INVISIBLE = {
    0x200B: "ZERO WIDTH SPACE",
    0x200C: "ZERO WIDTH NON-JOINER",
    0x200D: "ZERO WIDTH JOINER",
    0x2060: "WORD JOINER",
    0x2061: "FUNCTION APPLICATION",
    0x2062: "INVISIBLE TIMES",
    0x2063: "INVISIBLE SEPARATOR",
    0x2064: "INVISIBLE PLUS",
    0xFEFF: "ZERO WIDTH NO-BREAK SPACE (BOM)",
    0x00AD: "SOFT HYPHEN",
    0x180E: "MONGOLIAN VOWEL SEPARATOR",
}

# Richtungssteuerung. Basis von "Trojan Source": Anzeige weicht vom echten Inhalt ab.
BIDI = {
    0x200E: "LEFT-TO-RIGHT MARK",
    0x200F: "RIGHT-TO-LEFT MARK",
    0x061C: "ARABIC LETTER MARK",
    0x202A: "LEFT-TO-RIGHT EMBEDDING",
    0x202B: "RIGHT-TO-LEFT EMBEDDING",
    0x202C: "POP DIRECTIONAL FORMATTING",
    0x202D: "LEFT-TO-RIGHT OVERRIDE",
    0x202E: "RIGHT-TO-LEFT OVERRIDE",
    0x2066: "LEFT-TO-RIGHT ISOLATE",
    0x2067: "RIGHT-TO-LEFT ISOLATE",
    0x2068: "FIRST STRONG ISOLATE",
    0x2069: "POP DIRECTIONAL ISOLATE",
}

# Unicode-Tag-Block: vollstaendig unsichtbar, kann ganze Saetze verstecken.
TAGS = range(0xE0000, 0xE0080)

# Exotische Leerzeichen. Sehen aus wie Space, sind keiner.
SPACES = {
    0x00A0: "NO-BREAK SPACE",
    0x1680: "OGHAM SPACE MARK",
    0x2000: "EN QUAD", 0x2001: "EM QUAD",
    0x2002: "EN SPACE", 0x2003: "EM SPACE",
    0x2004: "THREE-PER-EM SPACE", 0x2005: "FOUR-PER-EM SPACE",
    0x2006: "SIX-PER-EM SPACE", 0x2007: "FIGURE SPACE",
    0x2008: "PUNCTUATION SPACE", 0x2009: "THIN SPACE",
    0x200A: "HAIR SPACE",
    0x202F: "NARROW NO-BREAK SPACE",
    0x205F: "MEDIUM MATHEMATICAL SPACE",
    0x3000: "IDEOGRAPHIC SPACE",
}


def classify(cp: int) -> tuple[str, str] | None:
    """Gibt (Klasse, Name) zurueck, oder None wenn das Zeichen unauffaellig ist."""
    if cp in INVISIBLE:
        return "unsichtbar", INVISIBLE[cp]
    if cp in BIDI:
        return "bidi", BIDI[cp]
    if cp in TAGS:
        return "tag", "UNICODE TAG"
    if cp in SPACES:
        return "space", SPACES[cp]
    return None


# ---------------------------------------------------------------- Text

def scan_text(text: str, include_spaces: bool = True) -> list[dict]:
    """Findet alle auffaelligen Zeichen mit Zeile/Spalte."""
    hits = []
    line = col = 1
    for ch in text:
        if ch == "\n":
            line, col = line + 1, 1
            continue
        found = classify(ord(ch))
        if found and (include_spaces or found[0] != "space"):
            hits.append({
                "line": line, "col": col, "cp": ord(ch),
                "kind": found[0], "name": found[1],
            })
        col += 1
    return hits


def clean_text(text: str, normalize_spaces: bool = False) -> tuple[str, int]:
    """Entfernt unsichtbare/bidi/tag-Zeichen. Leerzeichen nur auf Wunsch."""
    out = []
    removed = 0
    for ch in text:
        found = classify(ord(ch))
        if found is None:
            out.append(ch)
            continue
        kind = found[0]
        if kind in ("unsichtbar", "bidi", "tag"):
            removed += 1
        elif kind == "space":
            if normalize_spaces:
                out.append(" ")
                removed += 1
            else:
                out.append(ch)
        continue
    return "".join(out), removed


# ---------------------------------------------------------------- Bilder

JPEG_KEEP_APP0 = 0xE0   # JFIF, harmlos, manche Decoder erwarten es
JPEG_EXIF_APP1 = 0xE1   # EXIF/XMP
JPEG_ICC_APP2 = 0xE2    # Farbprofil

PNG_STRIP = {b"tEXt", b"zTXt", b"iTXt", b"eXIf", b"tIME", b"dSIG"}
PNG_ICC = b"iCCP"


def jpeg_segments(data: bytes):
    """Iteriert JPEG-Segmente als (marker, start, end). Stoppt am Bilddatenstrom."""
    if data[:2] != b"\xff\xd8":
        return
    i = 2
    n = len(data)
    while i + 3 < n:
        if data[i] != 0xFF:
            return
        marker = data[i + 1]
        if marker == 0xDA:  # Start of Scan, ab hier Pixeldaten
            return
        seg_len = int.from_bytes(data[i + 2:i + 4], "big")
        yield marker, i, i + 2 + seg_len
        i += 2 + seg_len


def read_orientation(segment: bytes) -> int | None:
    """EXIF-Orientation (Tag 0x0112) aus einem APP1-Segment lesen.

    Handykameras speichern das Bild oft liegend und legen die Drehung nur hier
    ab. Wird das EXIF komplett entfernt, erscheint ein Hochformat-Foto quer.
    """
    if len(segment) < 14 or not segment.startswith(b"Exif"):
        return None
    tiff = 6
    order = segment[tiff:tiff + 2]
    if order == b"II":
        end = "little"
    elif order == b"MM":
        end = "big"
    else:
        return None
    u16 = lambda o: int.from_bytes(segment[o:o + 2], end)
    u32 = lambda o: int.from_bytes(segment[o:o + 4], end)
    ifd0 = tiff + u32(tiff + 4)
    if ifd0 + 2 > len(segment):
        return None
    count = u16(ifd0)
    if count > 512:
        return None
    for i in range(count):
        entry = ifd0 + 2 + i * 12
        if entry + 12 > len(segment):
            return None
        if u16(entry) == 0x0112:
            value = u16(entry + 8)
            return value if 1 <= value <= 8 else None
    return None


def is_orientation_only(segment: bytes) -> bool:
    """Traegt dieses APP1 ausschliesslich die Orientation? Dann ist es unser eigenes."""
    return (
        read_orientation(segment) is not None
        and len(segment) == len(build_orientation_exif(1)) - 4
    )


def build_orientation_exif(orientation: int) -> bytes:
    """Minimales APP1-Segment, das nur die Orientation traegt (36 Byte)."""
    payload = (
        b"Exif\x00\x00"
        b"MM\x00\x2a"          # big endian, 42
        b"\x00\x00\x00\x08"   # IFD0-Offset
        b"\x00\x01"            # ein Eintrag
        b"\x01\x12"            # Tag Orientation
        b"\x00\x03"            # Typ SHORT
        b"\x00\x00\x00\x01"   # Anzahl 1
        + orientation.to_bytes(2, "big") + b"\x00\x00"
        + b"\x00\x00\x00\x00"  # kein weiteres IFD
    )
    return b"\xff\xe1" + (len(payload) + 2).to_bytes(2, "big") + payload


def img_inspect(path: str, aggressive: bool = False) -> list[str]:
    """Listet Metadaten-Bloecke auf, die img-clean auch wirklich entfernen wuerde.

    JFIF (APP0) wird nie entfernt und daher nicht gemeldet, sonst schlaegt der
    Exit-Code bei jedem normalen JPEG an und ist als CI-Signal wertlos.
    """
    data = open(path, "rb").read()
    found = []
    if data[:2] == b"\xff\xd8":
        for marker, start, end in jpeg_segments(data):
            size = end - start
            if marker == 0xFE:
                found.append(f"JPEG COM (Kommentar), {size} B")
            elif 0xE0 <= marker <= 0xEF:
                if marker == JPEG_KEEP_APP0:
                    continue
                if marker == JPEG_ICC_APP2 and not aggressive:
                    continue
                seg = data[start + 4:end]
                # Ein EXIF, das nur noch die Orientation traegt, ist das
                # Ergebnis von img-clean und wird nicht erneut gemeldet --
                # sonst schlaegt der Scan nach dem Clean weiter an.
                if marker == JPEG_EXIF_APP1 and is_orientation_only(seg):
                    continue
                tag = seg[:6]
                label = {0xE1: "EXIF/XMP", 0xE2: "ICC-Profil"}.get(
                    marker, f"APP{marker - 0xE0}")
                extra = ""
                if marker == 0xE1 and b"Exif" in tag:
                    orient = read_orientation(seg)
                    extra = " [EXIF, ggf. GPS]" if orient is None else f" [EXIF, Orientation {orient} bleibt]"
                elif marker == 0xE1:
                    extra = " [XMP]"
                found.append(f"JPEG APP{marker - 0xE0} ({label}), {size} B{extra}")
    elif data[:8] == b"\x89PNG\r\n\x1a\n":
        i = 8
        while i + 8 <= len(data):
            ln = int.from_bytes(data[i:i + 4], "big")
            typ = data[i + 4:i + 8]
            if typ in PNG_STRIP or (typ == PNG_ICC and aggressive):
                found.append(f"PNG {typ.decode('ascii', 'replace')}-Chunk, {ln} B")
            if typ == b"IEND":
                break
            i += 12 + ln
    else:
        found.append("unbekanntes Format (nur JPEG und PNG werden unterstuetzt)")
    return found


def img_clean(path: str, aggressive: bool = False) -> tuple[int, int]:
    """Entfernt Metadaten in-place. Gibt (Bytes vorher, Bytes nachher) zurueck."""
    data = open(path, "rb").read()
    before = len(data)

    if data[:2] == b"\xff\xd8":
        out = bytearray(b"\xff\xd8")
        cuts = []
        orientation = None
        for marker, start, end in jpeg_segments(data):
            drop = False
            if marker == 0xFE:                      # Kommentar
                drop = True
            elif 0xE0 <= marker <= 0xEF:
                if marker == JPEG_KEEP_APP0:
                    drop = False                    # JFIF behalten
                elif marker == JPEG_ICC_APP2:
                    drop = aggressive               # Farbprofil nur auf Wunsch
                else:
                    drop = True                     # EXIF, XMP, alles andere
            if drop:
                if marker == JPEG_EXIF_APP1 and orientation is None:
                    orientation = read_orientation(data[start + 4:end])
                cuts.append((start, end))
        last = 2
        for start, end in cuts:
            out += data[last:start]
            last = end
        out += data[last:]
        # Orientation als minimales EXIF wieder einsetzen, hinter JFIF.
        if orientation is not None and orientation != 1:
            exif = build_orientation_exif(orientation)
            insert = 2
            for marker, start, end in jpeg_segments(bytes(out)):
                if marker == JPEG_KEEP_APP0:
                    insert = end
                break
            out = bytearray(bytes(out)[:insert] + exif + bytes(out)[insert:])
        data = bytes(out)

    elif data[:8] == b"\x89PNG\r\n\x1a\n":
        out = bytearray(data[:8])
        i = 8
        while i + 8 <= len(data):
            ln = int.from_bytes(data[i:i + 4], "big")
            typ = data[i + 4:i + 8]
            chunk = data[i:i + 12 + ln]
            drop = typ in PNG_STRIP or (typ == PNG_ICC and aggressive)
            if not drop:
                out += chunk
            if typ == b"IEND":
                break
            i += 12 + ln
        data = bytes(out)
    else:
        return before, before

    open(path, "wb").write(data)
    return before, len(data)


# ---------------------------------------------------------------- IO

def read_source(target: str, use_clip: bool) -> str:
    if use_clip:
        return subprocess.run(["pbpaste"], capture_output=True, text=True).stdout
    if target == "-":
        return sys.stdin.read()
    return open(target, encoding="utf-8").read()


def main() -> int:
    p = argparse.ArgumentParser(add_help=False)
    p.add_argument("mode", choices=["scan", "clean", "img-scan", "img-clean"])
    p.add_argument("targets", nargs="*")
    p.add_argument("--clip", action="store_true")
    p.add_argument("-i", "--in-place", action="store_true")
    p.add_argument("--spaces", action="store_true")
    p.add_argument("--aggressive", action="store_true")
    p.add_argument("-q", "--quiet", action="store_true")
    p.add_argument("-h", "--help", action="store_true")
    a = p.parse_args()

    if a.help:
        print(__doc__)
        return 0

    targets = a.targets or (["-"] if not a.clip else [])

    # ---- Bilder
    if a.mode in ("img-scan", "img-clean"):
        if not targets:
            print("Kein Bild angegeben.", file=sys.stderr)
            return 2
        total = 0
        for t in targets:
            if a.mode == "img-scan":
                found = img_inspect(t, a.aggressive)
                print(f"\n{t}")
                if found:
                    for f in found:
                        print(f"  · {f}")
                    total += len(found)
                else:
                    print("  sauber")
            else:
                before, after = img_clean(t, a.aggressive)
                saved = before - after
                total += saved
                print(f"{t}: {before:,} → {after:,} B  ({saved:,} B entfernt)")
        if a.mode == "img-scan":
            print(f"\n{total} Metadaten-Block(s) gefunden.")
            return 1 if total else 0
        return 0

    # ---- Text
    exit_code = 0
    for t in (targets or ["<clip>"]):
        text = read_source(t, a.clip)
        label = "Zwischenablage" if a.clip else t

        if a.mode == "scan":
            hits = scan_text(text, include_spaces=True)
            hard = [h for h in hits if h["kind"] != "space"]
            if not a.quiet:
                print(f"\n{label}")
                if not hits:
                    print("  sauber")
                for h in hits:
                    flag = "  " if h["kind"] == "space" else "! "
                    print(f"  {flag}Z{h['line']}:{h['col']}  U+{h['cp']:04X}  "
                          f"{h['kind']:<11} {h['name']}")
            if hits:
                print(f"\n  {len(hard)} kritisch, {len(hits) - len(hard)} Leerzeichen-Variante(n)")
            if hard:
                exit_code = 1
        else:
            cleaned, removed = clean_text(text, normalize_spaces=a.spaces)
            if a.clip:
                subprocess.run(["pbcopy"], input=cleaned, text=True)
                print(f"Zwischenablage bereinigt: {removed} Zeichen entfernt.",
                      file=sys.stderr)
            elif a.in_place and t != "-":
                open(t, "w", encoding="utf-8").write(cleaned)
                print(f"{t}: {removed} Zeichen entfernt.", file=sys.stderr)
            else:
                sys.stdout.write(cleaned)
                print(f"{removed} Zeichen entfernt.", file=sys.stderr)

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
