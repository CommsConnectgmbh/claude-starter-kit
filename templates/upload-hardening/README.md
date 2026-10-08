# Upload hardening

One component for one problem: **remove metadata from uploaded images before they reach
storage.**

`strip-image-metadata.ts` has no dependencies and runs in browsers, Node, and Deno.
The same file covers Server Actions, API routes, Edge Functions, and client uploads.
Copy it, import it, and call it at each upload point.

## Why this matters

Phone photos carry GPS coordinates, camera model, capture time, and often an embedded
thumbnail. For user-generated content, the location is often a home or workplace.
Three situations where this causes problems:

- **Public buckets.** If a file is served through a public URL, anyone with the link can read
  its coordinates.
- **Sharing.** Receipts sent to accounting or evidence shared with third parties carry the
  capture location with them.
- **Cropped images.** Many tools do not update the embedded EXIF thumbnail when cropping,
  so it still shows the uncropped original.

EXIF and XMP fields also contain free text that multimodal models read.
If an upload passes through an OCR or vision pipeline, these fields are a known carrier
for indirect prompt injection (OWASP LLM01, MITRE ATLAS AML.T0051.001).

## Integration

```ts
import { stripImageMetadataForUpload } from '@/lib/strip-image-metadata';

const bytes = stripImageMetadataForUpload(
  new Uint8Array(await file.arrayBuffer()),
  'profilfoto',            // appears in the log when metadata is removed
);

await storage.from('avatars').upload(pfad, bytes, { contentType: file.type });
```

That is all. `stripImageMetadata()` also returns *what* was removed if you want to log it.

## Three properties that matter

**Lossless.** Only metadata segments are removed. Pixel data stays identical, byte for byte.
No re-encoding or loss of quality.

**Never throws.** If the byte layout is unexpected, the original is returned unchanged.
An upload must not fail because a file has an unexpected structure, especially when it
is the only copy of a piece of evidence.

**Preserves orientation.** This is an easy trap: phone cameras often store an image
sideways and record its rotation only in EXIF tag `0x0112`. Removing EXIF entirely turns
portrait photos sideways. This file writes back a minimal EXIF segment containing only
that tag: 36 bytes rather than the usual several hundred. GPS, Make, Model, DateTime,
and MakerNote are still removed.

## Limits

Only JPEG and PNG are processed. PDF, HEIC, and WebP pass through unchanged because
these upload paths also handle documents that must not be altered. If you need to
sanitize HEIC, convert it first.

The ICC color profile is preserved to avoid color shifts. An option lets you remove it too.

## Existing files

The component takes effect once integrated. Files already in storage remain untouched;
those need a one-time pass over the existing collection. A useful sequence: analyze and
count first, then write changes with a backup, then repeat the analysis. If the second
pass finds nothing, you have verified idempotence and a clean collection.

## Related

The kit's `hygiene` skill does the same for text (invisible Unicode characters) and includes
a command-line version for images, useful for one-time passes and files outside the app.
