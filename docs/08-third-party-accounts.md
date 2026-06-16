# Third-party accounts: what you'll want, and why

This kit is **opinionated about the rails, agnostic about the rails' provider**.
Skills bring the workflow; you bring the account at whichever service does the
underlying work. Nothing is hosted by us — every API key stays on your machine.

This page is the map: which account unlocks which skill, where to sign up,
and what each one costs at small scale.

## At a glance

| Account | Free tier? | Unlocks | Sign up |
|---|---|---|---|
| **[Anthropic](https://www.anthropic.com/api)** (Claude API) | Pay-as-you-go | Everything in this kit — Claude Code itself, all skills, all agents | [console.anthropic.com](https://console.anthropic.com/) |
| **[Ollama](https://ollama.com)** (local LLM) | Free (runs on your machine) | `second-opinion` — free adversarial code review | [ollama.com/download](https://ollama.com/download) |
| **[Linear](https://linear.app)** | Free for small teams | Linear MCP — safe landing spot for "found, don't fix yet" findings | [linear.app](https://linear.app/signup) |
| **[Sentry](https://sentry.io)** | Generous free tier | Sentry MCP — real error monitoring for `pro/self-heal/` | [sentry.io/signup](https://sentry.io/signup) |
| **[Supabase](https://supabase.com)** | Free tier (2 projects) | Supabase MCP + `compliance` (Advisors API) | [supabase.com/dashboard](https://supabase.com/dashboard) |
| **[fal.ai](https://fal.ai)** | $1 starter credit, then pay-as-you-go | `fal-ai` — Veo / Seedance / Kling / Flux / Nano Banana | [fal.ai/dashboard/keys](https://fal.ai/dashboard/keys) |
| **[OpenAI Platform](https://platform.openai.com)** | Pay-as-you-go (separate from ChatGPT subscription) | `openai-image` — gpt-image-1 for marketing visuals | [platform.openai.com/signup](https://platform.openai.com/signup) |
| **[Aikido](https://www.aikido.dev/)** | Free tier covers small repos | `compliance` — code / dependency / cloud scanner | [aikido.dev/signup](https://app.aikido.dev/login/signup) |
| **[Prowler](https://prowler.com)** | OSS CLI (free) | `compliance` — GitHub / Vercel / Cloudflare config scan | `pip install prowler` |

## What you really need vs nice-to-have

**Minimum to use this kit at all:**
- Anthropic API access (you're already there if you have Claude Code installed).
- That's it. The core skills (`council`, `scrape`, `skillify`, `canary`) and the German agents need nothing else.

**Strongly recommended (one of):**
- **Ollama** — turns on `second-opinion` for free, gives you the independent-reviewer companion for `autoplan` / `spec` without paying for a second model.
- **Linear** — gives Claude a place to file work it found but shouldn't fix unsupervised. The Linear MCP makes this one line. See [docs/06](06-linear-issues.md).

**Add when the use case shows up:**
- **Sentry** — when you ship to real users and want the [self-heal loop](05-self-healing-apps.md) to fix what Sentry sees.
- **fal.ai / OpenAI Images** — when you're producing marketing creative and want it scripted instead of clicked.
- **Supabase** — if Supabase is already your DB stack; the MCP makes inspecting schema / running SQL trivial.
- **Aikido + Prowler** — when a customer asks for a compliance/security report (or you want one for yourself, quarterly). See `pro/skills/compliance/`.

## What's NOT in this kit

- **No hosted backend.** This repo is files you install into `~/.claude/`. Nothing phones home.
- **No proxies for paid APIs.** If a skill calls a paid service, the key is in **your** env. We don't sit between you and the vendor.
- **No vendor lock-in.** Every skill that uses a third-party service is one model-key swap away from an alternative — fal-ai → Replicate; OpenAI Images → fal Flux; Linear → any tracker; Ollama → LM Studio. The skill is the pattern, not the brand.

## Security hygiene (boring but important)

- API keys in `~/.env` / project `.env.local` — **never** committed to git.
- For hosted MCPs, prefer OAuth (Linear, Sentry, Supabase all support it) over personal tokens — see [docs/07](07-mcps.md).
- One key per project where possible. A leaked broad key is much worse than a leaked scoped one.
- Rotate keys when you stop using a project, when an ex-collaborator had access, or at least once a year.

## Reading further

- [docs/01-getting-started.md](01-getting-started.md) — the mental model
- [docs/06-linear-issues.md](06-linear-issues.md) — Linear deep-dive
- [docs/07-mcps.md](07-mcps.md) — MCP shortlist and setup commands
