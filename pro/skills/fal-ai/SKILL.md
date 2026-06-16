---
name: fal-ai
description: >-
  Generate images and short videos via the fal.ai API — talking-head UGC ads,
  product shots, hero stills, B-roll, lip-synced spokesperson clips. Direct
  model access (Veo 3.1 / 3.1 Fast, Seedance 2.0, Kling, Nano Banana 2, Flux),
  no SaaS wrapper. Use when the user asks for "a UGC video", "talking head ad",
  "fal video / image", "Veo video", "Seedance / Kling video", "Nano Banana
  image", "Flux image", or wants cheap, scriptable creative generation. Skill
  assumes a `FAL_KEY` is available in the env.
---

# fal-ai — direct fal.ai image / video generation

A no-frills pattern for generating marketing creative (stills + short clips)
straight from the [fal.ai](https://fal.ai) REST API. Cheaper than SaaS
wrappers (Arcads etc.) because there's no markup on per-second pricing — and
you choose the model per shot instead of being locked to one.

## Setup

1. Create a fal.ai account, generate an API key.
2. Put it in your env: `export FAL_KEY=...` (or in `~/.env` / project `.env.local`).
3. That's it — calls are plain HTTPS, no SDK required (an SDK exists if you prefer).

## Model cheat sheet (prices as of writing — verify on fal.ai/models)

| Key | Endpoint | Type | Length | Price |
|---|---|---|---|---|
| `veo3.1` | `fal-ai/veo3.1` | text → video | 4 / 6 / 8s | ~$0.40/s, audio included |
| `veo3.1-i2v` | `fal-ai/veo3.1/image-to-video` | image → video | 4 / 6 / 8s | ~$0.40/s |
| `veo3.1-fast` | `fal-ai/veo3.1/fast` | text → video | 4 / 6 / 8s | ~$0.20/s |
| `seedance-2.0` | `fal-ai/bytedance/seedance-2.0/text-to-video` | text → video | 4–15s | ~$0.06/s |
| `seedance-2.0-i2v` | `fal-ai/bytedance/seedance-2.0/image-to-video` | image → video | 4–15s | ~$0.06/s |
| `kling-2.0` | `fal-ai/kling-video/v2/master/text-to-video` | text → video | 5 / 10s | ~$0.28/s |
| `nano-banana-2` | `fal-ai/nano-banana-2` | text → image | — | ~$0.03 / image |
| `flux-pro` | `fal-ai/flux-pro/v1.1-ultra` | text → image | — | ~$0.06 / image |

**Cheapest first drafts:** `seedance-2.0` (~$0.50 for 8s, lower fidelity, fine
for thumbnails / spec ideation).
**Best speech & lip-sync:** `veo3.1-fast` (~$1.60 for 8s, decent non-English
voice if you ask for it).

## Workflow (Claude's playbook)

1. **Confirm intent.** Single image / image set / short clip / talking-head
   ad? Aspect ratio? Duration? Language of dialogue (Veo otherwise defaults
   to English-accented)? If the user said "make an ad" without details, ask
   one quick clarifying question before burning credits.
2. **Pick the cheapest viable model** for a first draft. Don't reach for
   `veo3.1` (full) before you've seen a `veo3.1-fast` cut.
3. **Build the spec** (a JSON like the one below) and show the user the
   dialogue / prompt block + estimated cost. **Wait for approval** before
   firing — generation is non-refundable.
4. **Call the API** (synchronous or via `queue.fal.run` for long jobs).
5. **Save the output** locally with a sortable filename like
   `outputs/2026-06-16_03_label.mp4`. Log spend to `logs/fal-ai.jsonl` so
   future sessions know what's already been generated.

## Spec template

```json
{
  "label": "<short-id>",
  "model": "veo3.1-fast",
  "duration": "8s",
  "resolution": "720p",
  "aspect_ratio": "9:16",
  "generate_audio": true,
  "prompt": "<one paragraph: scene + subject + camera + dialogue>",
  "negative_prompt": "<things to avoid, e.g. 'English speech, distorted face'>"
}
```

## Dialogue handling for talking-head clips

Veo / Seedance generate the **voice themselves** from text in the prompt.
Embed the dialogue inline and tell the model the language explicitly:

> `... He says, in casual German: "Servus. Erster Deal gewonnen, Lukas..."`

For German output, **explicitly write "in casual German"** — Veo defaults to
English-accented voice otherwise. Add `English speech` to `negative_prompt`.

## Minimal client (synchronous; fine for stills + short clips)

```python
# pip install requests
import os, requests, time

FAL = "https://fal.run"
KEY = os.environ["FAL_KEY"]
HEAD = {"Authorization": f"Key {KEY}", "Content-Type": "application/json"}

def generate(endpoint: str, payload: dict, poll_url: str | None = None):
    r = requests.post(f"{FAL}/{endpoint}", json=payload, headers=HEAD)
    r.raise_for_status()
    data = r.json()
    # Some models return a queue id — poll until done.
    if "status_url" in data:
        while True:
            s = requests.get(data["status_url"], headers=HEAD).json()
            if s.get("status") in ("COMPLETED", "FAILED"):
                return s
            time.sleep(2)
    return data
```

Use this as a starting point — fal's official SDK does the polling for you
if you prefer.

## Cost discipline

- Log every call (model, duration, label, USD estimate) to a JSONL so you
  can reconcile against the fal billing page.
- Cap per session — a runaway loop on `veo3.1` at $3.20/clip burns money fast.
- Diff prompts before re-running — small tweaks rarely need a full
  regeneration if you already have a near-miss.

## What this skill is NOT

- Not an autonomous ad-buyer — generation only; placement is your job.
- Not a brand-compliance gate — if you have banned vocab (e.g. financial
  products that can't say "bet"), check the dialogue against the project's
  own rules **before** firing.
- Not stitching / editing — for cut + audio mixing, hand the clips to
  CapCut / Resolve / ffmpeg afterwards.
