# Upload-Hardening

Ein Baustein, ein Problem: **Metadaten aus hochgeladenen Bildern entfernen, bevor sie im
Storage landen.**

`strip-image-metadata.ts` ist abhängigkeitsfrei und läuft in Browser, Node und Deno.
Damit deckt dieselbe Datei Server Actions, API-Routen, Edge Functions und Client-Uploads
ab — kopieren, importieren, an jeder Upload-Stelle einhängen.

## Warum das nicht optional ist

Fotos aus Handykameras tragen GPS-Koordinaten, Kameramodell, Aufnahmezeit und oft ein
eingebettetes Vorschaubild. Bei nutzergenerierten Inhalten ist das regelmäßig eine Wohn-
oder Arbeitsadresse. Drei Konstellationen, in denen es konkret weh tut:

- **Öffentliche Buckets.** Wird die Datei über eine öffentliche URL ausgeliefert, sind die
  Koordinaten für jeden lesbar, der den Link hat.
- **Weitergabe.** Belege an die Buchhaltung, Nachweise an Dritte — der Aufnahmeort reist mit.
- **Zugeschnittene Bilder.** Das eingebettete EXIF-Thumbnail wird beim Zuschneiden von vielen
  Werkzeugen nicht aktualisiert und zeigt weiterhin das ungeschnittene Original.

Dazu kommt: EXIF- und XMP-Felder sind Freitext und werden von multimodalen Modellen
mitgelesen. Läuft der Upload durch eine OCR- oder Vision-Kette, sind sie ein bekannter
Träger für indirekte Prompt-Injection (OWASP LLM01, MITRE ATLAS AML.T0051.001).

## Einbau

```ts
import { stripImageMetadataForUpload } from '@/lib/strip-image-metadata';

const bytes = stripImageMetadataForUpload(
  new Uint8Array(await file.arrayBuffer()),
  'profilfoto',            // erscheint im Log, wenn etwas entfernt wurde
);

await storage.from('avatars').upload(pfad, bytes, { contentType: file.type });
```

Das war es. `stripImageMetadata()` gibt zusätzlich zurück, *was* entfernt wurde, falls
das protokolliert werden soll.

## Drei Eigenschaften, auf die es ankommt

**Verlustfrei.** Es werden ausschließlich Metadaten-Segmente ausgeschnitten, die Pixeldaten
bleiben Byte für Byte identisch. Kein Re-Encoding, kein Qualitätsverlust.

**Wirft nie.** Bei unerwartetem Byte-Layout kommt das Original unverändert zurück. Ein
Upload darf nicht daran scheitern, dass eine Datei anders aufgebaut ist als erwartet —
gerade wenn die Datei das einzige Exemplar eines Nachweises ist.

**Die Orientation überlebt.** Das ist die Falle, in die man bei diesem Thema als Erstes
tappt: Phone-Kameras speichern das Bild häufig liegend und legen die Drehung nur in
EXIF-Tag `0x0112` ab. Wer das EXIF komplett entfernt, dreht jedes Hochformat-Foto quer.
Diese Datei schreibt stattdessen ein minimales EXIF-Segment zurück, das nur dieses eine
Tag trägt — 36 Byte statt oft mehrerer hundert. GPS, Make, Model, DateTime und MakerNote
fallen trotzdem weg.

## Grenzen

Nur JPEG und PNG werden bearbeitet. PDF, HEIC und WebP gehen unverändert durch, weil über
dieselben Upload-Pfade in der Praxis auch Dokumente laufen und die auf keinen Fall
angefasst werden dürfen. Wer HEIC absichern muss, konvertiert ohnehin vorher.

Das ICC-Farbprofil bleibt erhalten, sonst verschieben sich die Farben. Es lässt sich per
Option mitentfernen.

## Bestandsdaten

Der Baustein wirkt ab Einbau. Was schon im Storage liegt, bleibt unberührt — dafür braucht
es einen einmaligen Durchlauf über die vorhandenen Dateien. Sinnvoll ist dabei die
Reihenfolge: erst nur analysieren und zählen, dann mit Sicherung schreiben, danach den
Analyselauf wiederholen. Wenn der zweite Lauf nichts mehr findet, ist die Funktion
nachweislich idempotent und der Bestand sauber.

## Verwandt

Der Skill `hygiene` aus diesem Kit macht dasselbe für Text (unsichtbare Unicode-Zeichen)
und bringt für Bilder eine Kommandozeilen-Fassung mit — praktisch für einmalige Läufe und
für Dateien außerhalb der Anwendung.
