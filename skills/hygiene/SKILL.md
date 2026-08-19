---
name: hygiene
description: "Find and remove invisible Unicode characters from text (zero-width, bidi/Trojan-Source, Unicode tags, exotic spaces) and metadata from images (EXIF/GPS, XMP, PNG text chunks). Use before sending mail, letters or marketing copy, before CSV imports, when a search mysteriously finds nothing, before uploading user photos, and as a deterministic pre-filter for anything from an untrusted source that reaches an LLM. Trigger phrases: 'invisible characters', 'zero width', 'unsichtbare Zeichen', 'komische Zeichen im Text', 'strip EXIF', 'EXIF entfernen', 'GPS aus Foto', 'remove metadata', 'Metadaten strippen', 'clean this text', 'hygiene'. NOT a watermark remover — see the last section."
user-invocable: true
---

# /hygiene — clean what you cannot see

One tool, two directions: what goes out is clean, what comes in is defused.

```
python3 ~/.claude/skills/hygiene/scripts/hygiene.py <mode> [target...] [options]
```

| Mode | Purpose |
|---|---|
| `scan` | Inspect text, reports line:column + codepoint. **Exit 1 on a finding** (CI/hook friendly) |
| `clean` | Clean text to stdout, or in place with `-i` |
| `img-scan` | Show image metadata. Exit 1 on a finding |
| `img-clean` | Remove image metadata, losslessly (pixels stay byte-identical) |

Options: `--clip` (read from and write back to the clipboard, macOS `pbpaste`/`pbcopy`),
`-i` (in place), `--spaces` (normalize exotic spaces), `--aggressive` (also drop the ICC
color profile), `-q` (summary only).

No dependencies. Python standard library only, so it runs wherever Python does.

## The common case

Mail or letter finished, before sending:

```bash
python3 ~/.claude/skills/hygiene/scripts/hygiene.py clean --clip
```

Reads the clipboard, cleans it, puts it back. Then paste as usual.

## What gets removed

**Always** — never legitimate in running text:

- Zero-width characters, word joiner, soft hyphen, BOM (U+200B–200D, U+2060, U+00AD, U+FEFF)
- Bidi control characters (U+202A–202E, U+2066–2069) — the basis of *Trojan Source*,
  where what you see differs from what is actually there
- The Unicode tag block (U+E0000–E007F) — fully invisible, can hide entire sentences

**Only with `--spaces`** — non-breaking space and friends survive by default, because they
are legitimate typography in many languages (`5 %`, `z. B.`, number + unit).

**Images:** EXIF (including GPS, camera make, model, timestamp), XMP, JPEG comments,
PNG `tEXt`/`zTXt`/`iTXt`/`eXIf`. JFIF stays (harmless, some decoders expect it). The ICC
color profile stays unless you pass `--aggressive` — removing it shifts colors.

**One thing that must survive: EXIF orientation.** Phone cameras often store the image
sideways and record the rotation only in tag `0x0112`. Strip the whole EXIF block and a
portrait photo shows up rotated. `img-clean` therefore writes back a minimal EXIF segment
carrying that single tag — 36 bytes instead of often several hundred. `img-scan` does not
report such a segment as a finding, so scanning stays quiet after cleaning.

## Why this matters

- **Before sending.** Invisible characters survive copy-paste out of any chat window and
  show up as boxes or `?` on the recipient's screen.
- **Before CSV import.** A BOM or non-breaking space in the header row breaks column
  matching, and the error message never mentions it.
- **When search finds nothing.** A zero-width space inside a word, and no `LIKE`, no
  `includes()` and no user will ever find that record again.
- **Before uploading photos.** Phone pictures carry GPS coordinates. Anything user-uploaded
  that lands in a public bucket publishes the location it was taken at.
- **As an LLM pre-filter.** Hidden instructions in foreign mail, PDFs or images are the
  standard carrier for indirect prompt injection (OWASP LLM01, MITRE ATLAS AML.T0051.001).
  This is the cheap deterministic first pass, not a replacement for a detector model.

## As a hook or in CI

`scan` exits 1 on a critical finding, which makes it usable as a pre-commit hook or a
pipeline step:

```bash
python3 ~/.claude/skills/hygiene/scripts/hygiene.py scan -q src/**/*.tsx
```

## Tests

```bash
python3 ~/.claude/skills/hygiene/scripts/test_hygiene.py
```

26 checks covering both directions, including the ones that would hurt silently:
orientation survives, scanning is quiet after cleaning, PDFs pass through untouched,
malformed input returns the original instead of raising, exit codes are correct.

## What this deliberately does not do

It does **not** attack statistical watermarks (SynthID-Text and similar), does **not**
strip C2PA provenance, and does **not** rewrite text.

Those techniques exist to obscure that content was machine-generated. Since 2 August 2026,
Article 50 of the EU AI Act requires the opposite — machine-readable marking of AI-generated
content — and major model providers now embed such marks. A tool that removes them is a
liability for anyone who sells to regulated customers, and by its own authors' admission it
degrades the prose while never being verifiable.

The deterministic part above is unaffected by that line: zero-width characters and EXIF
data are not a provenance signal. They are junk and a data leak.
