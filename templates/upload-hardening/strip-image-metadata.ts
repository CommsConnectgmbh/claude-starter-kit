// Entfernt Metadaten aus hochgeladenen Bildern, bevor sie im Storage landen.
//
// Warum: Fotos aus Handykameras tragen EXIF mit GPS-Koordinaten, Kameramodell,
// Aufnahmezeit und oft einem eingebetteten Vorschaubild. Wird so ein Bild
// weitergereicht oder in einem oeffentlichen Bucket abgelegt, wandert der
// Aufnahmeort mit — bei nutzergenerierten Inhalten also regelmaessig eine
// Wohn- oder Arbeitsadresse. Fuer die Verarbeitung wird davon nichts gebraucht
// (Datenminimierung, Art. 5 Abs. 1 lit. c DSGVO).
//
// Zweiter Grund: EXIF- und XMP-Felder sind Freitext und werden von multimodalen
// Modellen mitgelesen. Sie sind ein bekannter Traeger fuer indirekte
// Prompt-Injection (OWASP LLM01, MITRE ATLAS AML.T0051.001) — relevant, sobald
// hochgeladene Bilder durch eine OCR- oder Vision-Kette laufen.
//
// Ausnahme, die bleiben MUSS: die EXIF-Orientation. Handykameras speichern das
// Bild oft liegend und legen die Drehung nur als Tag 0x0112 ab. Wird das EXIF
// komplett entfernt, erscheint ein hochkant fotografiertes Bild quer. Deshalb
// wird bei vorhandener Orientation ein minimales EXIF-Segment neu geschrieben,
// das ausschliesslich dieses eine Tag traegt — GPS, Make, Model, DateTime,
// UserComment und MakerNote fallen weg.
//
// Grundsaetze:
//   - Verlustfrei. Pixeldaten werden nicht angefasst, kein Re-Encoding.
//   - Wirft nie. Bei unerwartetem Byte-Layout kommt das Original unveraendert
//     zurueck: ein Upload darf nie an dieser Stelle scheitern.
//   - Nur JPEG und PNG. PDF, HEIC und WebP gehen unveraendert durch — ueber
//     dieselben Upload-Pfade laufen in der Praxis auch Dokumente.
//
// Laeuft in Browser, Node und Deno: reines Uint8Array, keine Runtime-APIs.
// Damit dieselbe Funktion in Server Actions, API-Routen, Edge Functions und
// Client-Uploads.
//
// Erprobt in Produktion, mit 22 Tests in zwei Projekten abgesichert.

/** JFIF-Segment. Bleibt: harmlos, manche Decoder erwarten es. */
const JPEG_APP0 = 0xe0;
/** EXIF/XMP. Wird entfernt — bis auf die Orientation, siehe Kopfkommentar. */
const JPEG_APP1 = 0xe1;
/** ICC-Farbprofil. Bleibt per Default: Entfernen würde Farben verschieben. */
const JPEG_APP2 = 0xe2;
/** Start of Scan — ab hier beginnen die Pixeldaten. */
const JPEG_SOS = 0xda;
/** Kommentarsegment. */
const JPEG_COM = 0xfe;

/** PNG-Chunks mit Text-, Zeit- oder EXIF-Inhalt. */
const PNG_METADATA_CHUNKS = ["tEXt", "zTXt", "iTXt", "eXIf", "tIME", "dSIG"];
const PNG_ICC_CHUNK = "iCCP";

const JPEG_MAGIC = [0xff, 0xd8, 0xff];
const PNG_MAGIC = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a];

export interface StripOptions {
  /** Auch das ICC-Farbprofil entfernen. Default false — verschiebt sonst Farben. */
  removeIccProfile?: boolean;
}

export interface StripResult {
  bytes: Uint8Array;
  /** Wie viele Bytes entfernt wurden. 0 = nichts gefunden oder Format unbekannt. */
  removedBytes: number;
  /** Welche Blöcke entfernt wurden, für Logging. Z. B. ["APP1", "COM"]. */
  removed: string[];
  /**
   * Gesetzt, wenn eine EXIF-Orientation gerettet und als minimales APP1 neu
   * geschrieben wurde. null, wenn keine vorhanden oder ohnehin 1 (normal).
   */
  orientationKept?: number | null;
}

function startsWith(bytes: Uint8Array, magic: number[]): boolean {
  if (bytes.length < magic.length) return false;
  return magic.every((b, i) => byteAt(bytes, i) === b);
}

/**
 * Byte an einer Position, ausserhalb der Grenzen 0. Explizit, weil der Web-Build
 * mit `noUncheckedIndexedAccess` laeuft und ein blanker Indexzugriff dort
 * `number | undefined` ist. Alle Aufrufer pruefen die Grenzen vorher selbst.
 */
function byteAt(bytes: Uint8Array, index: number): number {
  return bytes[index] ?? 0;
}

function readUint32BE(bytes: Uint8Array, offset: number): number {
  return (
    ((byteAt(bytes, offset) << 24) >>> 0) +
    (byteAt(bytes, offset + 1) << 16) +
    (byteAt(bytes, offset + 2) << 8) +
    byteAt(bytes, offset + 3)
  );
}

/**
 * Liest die EXIF-Orientation (TIFF-Tag 0x0112) aus einem APP1-Segment.
 * `segment` beginnt hinter Marker und Längenfeld, also bei "Exif\0\0".
 * Gibt null zurück, wenn kein oder ein unlesbares EXIF vorliegt.
 */
function readOrientation(segment: Uint8Array): number | null {
  // "Exif\0\0" (6 Byte), danach der TIFF-Header.
  if (segment.length < 14) return null;
  for (let i = 0; i < 4; i++) {
    if (byteAt(segment, i) !== "Exif".charCodeAt(i)) return null;
  }
  const tiff = 6;
  const little = byteAt(segment, tiff) === 0x49 && byteAt(segment, tiff + 1) === 0x49;
  const big = byteAt(segment, tiff) === 0x4d && byteAt(segment, tiff + 1) === 0x4d;
  if (!little && !big) return null;

  const u16 = (o: number) =>
    little
      ? byteAt(segment, o) | (byteAt(segment, o + 1) << 8)
      : (byteAt(segment, o) << 8) | byteAt(segment, o + 1);
  const u32 = (o: number) =>
    little
      ? (byteAt(segment, o) | (byteAt(segment, o + 1) << 8) |
        (byteAt(segment, o + 2) << 16) | (byteAt(segment, o + 3) << 24)) >>> 0
      : ((byteAt(segment, o) << 24) | (byteAt(segment, o + 1) << 16) |
        (byteAt(segment, o + 2) << 8) | byteAt(segment, o + 3)) >>> 0;

  const ifd0 = tiff + u32(tiff + 4);
  if (ifd0 + 2 > segment.length) return null;
  const count = u16(ifd0);
  // Ein IFD mit absurd vielen Einträgen ist kaputt, nicht interessant.
  if (count > 512) return null;

  for (let i = 0; i < count; i++) {
    const entry = ifd0 + 2 + i * 12;
    if (entry + 12 > segment.length) return null;
    if (u16(entry) === 0x0112) {
      // SHORT: der Wert steht in den ersten zwei Byte des Wertfelds.
      const value = u16(entry + 8);
      return value >= 1 && value <= 8 ? value : null;
    }
  }
  return null;
}

/**
 * Baut ein minimales APP1-Segment, das nur die Orientation trägt.
 * Aufbau: Marker, Länge, "Exif\0\0", TIFF-Header (big endian), IFD0 mit einem
 * Eintrag, leerer Next-IFD-Zeiger. Insgesamt 36 Byte.
 */
function buildOrientationExif(orientation: number): Uint8Array {
  const payload = [
    0x45, 0x78, 0x69, 0x66, 0x00, 0x00, // "Exif\0\0"
    0x4d, 0x4d, 0x00, 0x2a, // "MM", 42 — big endian
    0x00, 0x00, 0x00, 0x08, // IFD0 beginnt 8 Byte nach dem TIFF-Header
    0x00, 0x01, // ein Eintrag
    0x01, 0x12, // Tag 0x0112 Orientation
    0x00, 0x03, // Typ SHORT
    0x00, 0x00, 0x00, 0x01, // Anzahl 1
    (orientation >> 8) & 0xff, orientation & 0xff, 0x00, 0x00, // Wert, linksbündig
    0x00, 0x00, 0x00, 0x00, // kein weiteres IFD
  ];
  const length = payload.length + 2; // Längenfeld zählt sich selbst mit
  return new Uint8Array([0xff, 0xe1, (length >> 8) & 0xff, length & 0xff, ...payload]);
}

function concat(parts: Uint8Array[], totalLength: number): Uint8Array {
  const out = new Uint8Array(totalLength);
  let offset = 0;
  for (const part of parts) {
    out.set(part, offset);
    offset += part.length;
  }
  return out;
}

function stripJpeg(bytes: Uint8Array, opts: StripOptions): StripResult {
  const keep: Uint8Array[] = [bytes.subarray(0, 2)]; // SOI
  const removed: string[] = [];
  let total = 2;
  let i = 2;
  // Aus dem ersten EXIF-Segment gerettet, danach als minimales APP1 neu gesetzt.
  let orientation: number | null = null;
  let orientationKept: number | null = null;

  while (i + 4 <= bytes.length) {
    // Kein gültiger Marker, oder ab Start of Scan folgen Pixeldaten ohne
    // Längenangabe: ab hier nichts mehr interpretieren.
    if (byteAt(bytes, i) !== 0xff) break;

    const marker = byteAt(bytes, i + 1);
    if (marker === JPEG_SOS) break;

    // Längenfeld zählt sich selbst mit, daher +2 für den Marker.
    const segmentLength = (byteAt(bytes, i + 2) << 8) + byteAt(bytes, i + 3);
    const end = i + 2 + segmentLength;
    // Längenangabe unplausibel — nicht weiter interpretieren.
    if (segmentLength < 2 || end > bytes.length) break;

    let drop = false;
    let label = "";
    if (marker === JPEG_COM) {
      drop = true;
      label = "COM";
    } else if (marker >= 0xe0 && marker <= 0xef) {
      label = `APP${marker - 0xe0}`;
      if (marker === JPEG_APP0) drop = false;
      else if (marker === JPEG_APP2) drop = Boolean(opts.removeIccProfile);
      else drop = true; // APP1 = EXIF/XMP, und alles andere an Anwendungsdaten
    }

    if (drop) {
      // Vor dem Verwerfen die Orientation retten: ohne sie wuerde ein
      // Hochformat-Foto quer dargestellt.
      if (marker === JPEG_APP1 && orientation === null) {
        orientation = readOrientation(bytes.subarray(i + 4, end));
      }
      removed.push(label);
    } else {
      keep.push(bytes.subarray(i, end));
      total += end - i;
    }
    i = end;
  }

  // Alles ab hier (Pixeldaten, Reste, nicht interpretierbare Bytes) unverändert.
  if (i < bytes.length) {
    keep.push(bytes.subarray(i));
    total += bytes.length - i;
  }

  // Orientation als minimales EXIF wieder einsetzen — hinter JFIF, vor den
  // Bilddaten. Bei Orientation 1 (normal) ist nichts zu retten.
  if (orientation !== null && orientation !== 1) {
    const exif = buildOrientationExif(orientation);
    // Position: direkt nach SOI und einem eventuellen JFIF-Segment.
    const insertAt = keep.length > 1 && byteAt(keep[1] ?? new Uint8Array(), 1) === JPEG_APP0
      ? 2
      : 1;
    keep.splice(insertAt, 0, exif);
    total += exif.length;
    orientationKept = orientation;
  }

  return {
    bytes: concat(keep, total),
    removedBytes: bytes.length - total,
    removed,
    orientationKept,
  };
}

function stripPng(bytes: Uint8Array, opts: StripOptions): StripResult {
  const keep: Uint8Array[] = [bytes.subarray(0, 8)]; // Signatur
  const removed: string[] = [];
  let total = 8;
  let i = 8;

  while (i + 8 <= bytes.length) {
    const length = readUint32BE(bytes, i);
    // 4 Byte Länge + 4 Byte Typ + Daten + 4 Byte CRC
    const end = i + 12 + length;
    if (length < 0 || end > bytes.length) break;

    const type = String.fromCharCode(
      byteAt(bytes, i + 4), byteAt(bytes, i + 5),
      byteAt(bytes, i + 6), byteAt(bytes, i + 7),
    );
    const drop =
      PNG_METADATA_CHUNKS.includes(type) ||
      (type === PNG_ICC_CHUNK && Boolean(opts.removeIccProfile));

    if (drop) {
      removed.push(type);
    } else {
      keep.push(bytes.subarray(i, end));
      total += end - i;
    }

    i = end;
    if (type === "IEND") break;
  }

  // Reste nach IEND oder nicht interpretierbare Bytes unverändert übernehmen.
  if (i < bytes.length) {
    keep.push(bytes.subarray(i));
    total += bytes.length - i;
  }

  return { bytes: concat(keep, total), removedBytes: bytes.length - total, removed };
}

/**
 * Entfernt Metadaten aus JPEG und PNG. Andere Formate kommen unverändert zurück.
 * Wirft nie — im Zweifel gewinnt das Original.
 */
export function stripImageMetadata(
  bytes: Uint8Array,
  opts: StripOptions = {},
): StripResult {
  const unchanged: StripResult = { bytes, removedBytes: 0, removed: [] };
  try {
    if (startsWith(bytes, JPEG_MAGIC)) return stripJpeg(bytes, opts);
    if (startsWith(bytes, PNG_MAGIC)) return stripPng(bytes, opts);
    return unchanged;
  } catch {
    return unchanged;
  }
}

/**
 * Bequemer Aufruf für die Ingest-Pfade: gibt nur die Bytes zurück und schreibt
 * eine Logzeile, wenn etwas entfernt wurde.
 */
export function stripImageMetadataForUpload(
  bytes: Uint8Array,
  context: string,
): Uint8Array {
  const result = stripImageMetadata(bytes);
  if (result.removedBytes > 0) {
    console.log(
      `[${context}] Bild-Metadaten entfernt: ${result.removed.join(", ")} ` +
        `(${result.removedBytes} B)`,
    );
  }
  return result.bytes;
}
