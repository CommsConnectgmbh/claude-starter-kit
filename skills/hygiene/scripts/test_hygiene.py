#!/usr/bin/env python3
"""Tests fuer hygiene.py. Aufruf: python3 test_hygiene.py"""

import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from hygiene import (  # noqa: E402
    build_orientation_exif,
    clean_text,
    img_clean,
    img_inspect,
    is_orientation_only,
    read_orientation,
    scan_text,
)

fehler = []


def pruefe(bedingung, name):
    if bedingung:
        print(f"  ok    {name}")
    else:
        print(f"  FAIL  {name}")
        fehler.append(name)


# ---------------------------------------------------------------- Text

print("\nText")

t = "Test​mit‮versteckt, 5 % Rabatt\U000e0041"
treffer = scan_text(t)
pruefe(len([h for h in treffer if h["kind"] != "space"]) == 3, "drei kritische Zeichen gefunden")
pruefe(any(h["kind"] == "space" for h in treffer), "NBSP wird als Leerzeichen-Variante gemeldet")

sauber, entfernt = clean_text(t)
pruefe(entfernt == 3, "drei Zeichen entfernt")
pruefe("​" not in sauber and "‮" not in sauber, "Zero-Width und Bidi weg")
pruefe("\U000e0041" not in sauber, "Unicode-Tag weg")
pruefe(" " in sauber, "NBSP bleibt ohne --spaces (deutsche Typografie)")

mit_spaces, _ = clean_text(t, normalize_spaces=True)
pruefe(" " not in mit_spaces and "5 %" in mit_spaces, "--spaces normalisiert NBSP")

pruefe(clean_text("normaler Text")[1] == 0, "sauberer Text bleibt unveraendert")
pruefe(scan_text("") == [], "leerer Text ist unkritisch")


# ---------------------------------------------------------------- EXIF-Helfer

print("\nEXIF-Bausteine")

exif = build_orientation_exif(6)
pruefe(len(exif) == 36, "minimales EXIF ist 36 Byte")
pruefe(read_orientation(exif[4:]) == 6, "Orientation liest sich zurueck")
pruefe(is_orientation_only(exif[4:]), "als reines Orientation-EXIF erkannt")
pruefe(all(read_orientation(build_orientation_exif(o)[4:]) == o for o in range(1, 9)),
       "alle acht Werte ueberleben den Roundtrip")
pruefe(read_orientation(b"nichts") is None, "Muell liefert None statt Absturz")
pruefe(read_orientation(b"Exif\x00\x00MM") is None, "abgeschnittenes EXIF liefert None")


# ---------------------------------------------------------------- Bilder

print("\nBilder")


def jpeg_segment(marker, payload):
    laenge = len(payload) + 2
    return bytes([0xFF, marker]) + laenge.to_bytes(2, "big") + payload


def baue_jpeg(orientation=6):
    eintraege = (
        b"\x01\x12\x00\x03\x00\x00\x00\x01" + orientation.to_bytes(2, "big") + b"\x00\x00"
        b"\x01\x0f\x00\x02\x00\x00\x00\x06\x00\x00\x00\x2e"
        b"\x88\x25\x00\x04\x00\x00\x00\x01\x00\x00\x00\x34"
    )
    exif_payload = (
        b"Exif\x00\x00MM\x00\x2a\x00\x00\x00\x08\x00\x03" + eintraege
        + b"\x00\x00\x00\x00Apple\x00"
    )
    return (
        b"\xff\xd8"
        + jpeg_segment(0xE0, b"JFIF\x00")
        + jpeg_segment(0xE1, exif_payload)
        + jpeg_segment(0xFE, b"interne notiz")
        + b"\xff\xda\x00\x08\x01\x02\x03\x04\xff\xd9"
    )


with tempfile.TemporaryDirectory() as d:
    p = Path(d) / "foto.jpg"
    original = baue_jpeg(6)
    p.write_bytes(original)

    funde = img_inspect(str(p))
    pruefe(len(funde) == 2, "EXIF und Kommentar werden gefunden")
    pruefe(any("Orientation 6 bleibt" in f for f in funde), "Orientation wird als bleibend angezeigt")

    img_clean(str(p))
    nachher = p.read_bytes()

    pruefe(b"Apple" not in nachher, "Herstellername entfernt")
    pruefe(b"interne notiz" not in nachher, "Kommentar entfernt")
    pruefe(b"\x88\x25" not in nachher, "GPS-Zeiger entfernt")
    pruefe(b"JFIF" in nachher, "JFIF bleibt")
    pruefe(nachher.endswith(b"\x01\x02\x03\x04\xff\xd9"), "Pixeldaten unangetastet")

    # Orientation muss ueberleben, sonst liegt ein Hochformat-Foto quer.
    i, gefunden = 2, None
    while i + 4 <= len(nachher) and nachher[i] == 0xFF:
        m = nachher[i + 1]
        if m == 0xDA:
            break
        ln = int.from_bytes(nachher[i + 2:i + 4], "big")
        if m == 0xE1:
            gefunden = read_orientation(nachher[i + 4:i + 2 + ln])
        i += 2 + ln
    pruefe(gefunden == 6, "Orientation ueberlebt den Strip")

    pruefe(img_inspect(str(p)) == [], "Scan ist nach dem Clean ruhig (idempotent)")

    vorher_laenge = len(p.read_bytes())
    img_clean(str(p))
    pruefe(len(p.read_bytes()) == vorher_laenge, "zweiter Clean aendert nichts")

    # Orientation 1 heisst normal — dann faellt das EXIF ganz weg.
    p2 = Path(d) / "normal.jpg"
    p2.write_bytes(baue_jpeg(1))
    img_clean(str(p2))
    pruefe(b"Exif" not in p2.read_bytes(), "bei Orientation 1 faellt das EXIF komplett")

    # PDFs und Unbekanntes duerfen nicht angefasst werden.
    p3 = Path(d) / "beleg.pdf"
    pdf = b"%PDF-1.7\n1 0 obj\nendobj\n"
    p3.write_bytes(pdf)
    img_clean(str(p3))
    pruefe(p3.read_bytes() == pdf, "PDF bleibt unveraendert")

    # CLI-Durchlauf, inklusive Exit-Code.
    p4 = Path(d) / "text.txt"
    p4.write_text("a​b", encoding="utf-8")
    r = subprocess.run([sys.executable, str(Path(__file__).parent / "hygiene.py"),
                        "scan", str(p4)], capture_output=True, text=True)
    pruefe(r.returncode == 1, "scan gibt Exit 1 bei kritischem Fund (CI-tauglich)")
    p4.write_text("sauber", encoding="utf-8")
    r = subprocess.run([sys.executable, str(Path(__file__).parent / "hygiene.py"),
                        "scan", str(p4)], capture_output=True, text=True)
    pruefe(r.returncode == 0, "scan gibt Exit 0 bei sauberem Text")

print()
if fehler:
    print(f"{len(fehler)} FEHLGESCHLAGEN: {', '.join(fehler)}")
    sys.exit(1)
print("alle Tests bestanden")
