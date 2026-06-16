---
name: openai-image
description: >-
  Generate marketing images via OpenAI's Images API (`gpt-image-1`, the GPT-4o
  image model) — hero shots, social posts, ad creatives, illustrations,
  product mockups, photo-real comps. Use when the user asks for "an image",
  "a hero image", "a social graphic", "an OG image", "ad creative", "gpt-image",
  "DALL-E", "OpenAI image", or wants generated visuals via OpenAI. Skill
  assumes an `OPENAI_API_KEY` is available in the env.
---

# openai-image — gpt-image-1 (OpenAI Images API)

A direct, no-frills pattern for generating marketing visuals with OpenAI's
current image model. `gpt-image-1` understands long instructions, renders
legible text in images (rare for image models), and produces consistent
brand-looking output.

## Setup

1. Create an OpenAI Platform account → [platform.openai.com/signup](https://platform.openai.com/signup) (separate from a ChatGPT subscription — this is the API side).
2. Load credit and create an API key → [platform.openai.com/api-keys](https://platform.openai.com/api-keys).
3. Put it in your env: `export OPENAI_API_KEY=sk-...`.
4. Check your org has access to `gpt-image-1` — most do by default; high-volume use may require ID verification under [platform.openai.com/settings/organization/general](https://platform.openai.com/settings/organization/general).

> **Account-only skill** — you bring the OpenAI account, the skill brings the rail. Nothing here is hosted by us.

## Pricing (verify on platform.openai.com/docs/pricing)

Roughly tiered by resolution + quality:

| Size | Quality | Approx. price |
|---|---|---|
| 1024×1024 | low | ~$0.011 |
| 1024×1024 | medium | ~$0.042 |
| 1024×1024 | high | ~$0.167 |
| 1024×1536 / 1536×1024 | high | ~$0.25 |

Default to **`medium`** for drafts, **`high`** for finals. Don't burn `high`
on prompt iteration.

## Workflow (Claude's playbook)

1. **Clarify intent** in one sentence: use case (hero / social / ad / OG),
   target aspect ratio, must-include-text, style direction. If the user said
   "make me an image" with no hint, ask one question first.
2. **Write the prompt** like a creative brief, not a hashtag list:
   - Subject + setting + camera/angle (for photo-real) or medium (for illustration)
   - Lighting + mood
   - Text overlays in quotes (gpt-image-1 renders text reliably; specify exact wording)
   - Style anchors ("editorial photograph, shot on 35mm, natural light")
   - Negative space if you'll add text on top
3. **Generate at `medium` quality first.** Show the user, iterate on prompt.
4. **Re-render at `high` only when the composition is right.**
5. **Save** with a sortable filename: `outputs/2026-06-16_03_hero.png`.

## Minimal client

```python
# pip install openai
from openai import OpenAI
import base64, pathlib

client = OpenAI()  # uses OPENAI_API_KEY

def gen(prompt: str, *, size="1024x1024", quality="medium", out: str):
    r = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size=size,
        quality=quality,
        n=1,
    )
    img_b64 = r.data[0].b64_json
    pathlib.Path(out).write_bytes(base64.b64decode(img_b64))
    return out
```

For multi-variant runs (e.g. "give me 4 hero options"), set `n=4` — it's
billed per image either way, but a single call is more convenient.

## Editing existing images (inpaint / variation)

`gpt-image-1` also supports `images.edit` with an input image + mask:

```python
client.images.edit(
    model="gpt-image-1",
    image=open("hero.png", "rb"),
    mask=open("mask.png", "rb"),    # transparent = "edit here"
    prompt="replace the laptop with an open notebook",
    size="1024x1024",
)
```

Use this when you have a near-miss and don't want to re-roll the whole
composition. **Don't** use it for tiny tweaks that ffmpeg / Pillow can do
deterministically.

## Cost discipline

- Default to `medium`; promote to `high` only on the chosen variant.
- Log every call (prompt hash, size, quality, USD) so you can reconcile.
- For social / ad variants, **stick with one composition + tweak prompts**
  instead of re-rolling — keeps the look consistent across the campaign.

## When to use fal-ai vs openai-image

- **Photo-real with legible on-image text → openai-image.** Other models
  still struggle with text; gpt-image-1 nails it.
- **Stylised illustrations / posters / variants → either.** fal's Flux Pro
  is also strong and cheaper for pure illustration.
- **Video / talking-head → fal-ai** (this skill is image-only).

## What this skill is NOT

- Not a brand-asset manager — saving outputs and tagging them is on you.
- Not a copyright clearance layer — if the prompt mentions named brands /
  people, you own the output's legal status.
- Not a stitcher — for grids, banners, OG-image overlays, hand the result to
  Pillow / ffmpeg / Figma afterwards.
