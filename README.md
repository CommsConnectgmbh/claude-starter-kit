# claude-starter-kit

A working day-one setup for [Claude Code](https://docs.claude.com/en/docs/claude-code) — two real production agents, one decision-making skill, a sanitizer that scans your `~/.claude/` for the things you'd accidentally leak, and the docs to put it together.

**If you've ever thought about publishing your `~/.claude/` folder, then opened it again and shut your laptop — this is what you should ship instead.**

```
              you ask Claude something
                       │
                       ▼
            ┌──────────────────────┐
            │     CLAUDE.md        │  project rules · conventions · don'ts
            └──────────┬───────────┘
                       │
            ┌──────────▼───────────┐
            │    auto-memory       │  who you are · preferences · context
            │     (MEMORY.md)      │  → persists across conversations
            └──────────┬───────────┘
                       │
            ┌──────────▼───────────┐
            │       skills         │  reusable workflows · /council · /verify
            │   (~/.claude/skills) │  → run inline in this turn
            └──────────┬───────────┘
                       │
            ┌──────────▼───────────┐
            │       agents         │  domain experts · legal-de · tax-de
            │   (~/.claude/agents) │  → isolated context, return one report
            └──────────────────────┘

      this kit ships one of each + the docs to wire them up
```

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Release](https://img.shields.io/github/v/release/CommsConnectgmbh/claude-starter-kit)](https://github.com/CommsConnectgmbh/claude-starter-kit/releases)
[![No emojis](https://img.shields.io/badge/emojis-zero-black.svg)](#)

## What you get

- **Two production agents** — German legal (`legal-de`) and German tax (`tax-de`), with mandatory source citation, statutory disclaimers (§ 2 RDG / § 2 StBerG), and a hard rule to refuse anything that needs a licensed professional. Survive sanitization without losing value.
- **One decision skill** — `/council`, five roles (Visionär, Kritiker, Kreativer, Skeptiker, Logiker) that must disagree somewhere, then pick a side. No "it depends".
- **A sanitizer script** — scans your own `~/.claude/` and flags API keys, personal paths, emails, and any company codenames you add. Caught seven files in the maintainer's own setup that would have shipped without it.
- **A CLAUDE.md skeleton** — drop into any project, fill the blanks, stop re-explaining your stack every conversation.
- **A worked memory example** — what `MEMORY.md` actually looks like when you use the auto-memory feature properly, plus what NOT to save.
- **Five docs** — setup, memory system, skills-vs-agents, recommended third-party skills, naming conventions. 20-minute read.

## What you provide

- A [Claude Code](https://docs.claude.com/en/docs/claude-code) install.
- A `~/.claude/` folder (created on first run if it doesn't exist).
- Two minutes to diff the settings before overwriting yours.

That's it. No subscriptions, no signups, no telemetry. MIT, no strings.

## 60-second install

```bash
# One-liner (reads what's about to happen, no surprises)
curl -fsSL https://raw.githubusercontent.com/CommsConnectgmbh/claude-starter-kit/main/install.sh | bash

# Or clone and pick what you want
git clone https://github.com/CommsConnectgmbh/claude-starter-kit.git
cd claude-starter-kit && ./install.sh
```

The installer asks before touching anything in `~/.claude/`. It never overwrites without showing you a diff first.

## What makes this different

Most public Claude Code dotfiles repos do one of two things:

1. **Dump everything.** Skills, agents, settings, sometimes the memory folder. Easy to clone, ships with the maintainer's client names, API project IDs, internal paths, and codenames they forgot about. Useful for them, dangerous for you.
2. **Strip everything.** Generic templates, no real content, basically a typed-up version of the Claude Code docs.

This kit is the working middle: **real agents that solve real problems, with the personal context surgically removed and the third-party material linked to its source instead of copied.**

| | Dump-it-all repos | Empty-template repos | **This kit** |
|---|---|---|---|
| Real working agents | Yes (but theirs) | No | **Yes (sanitized)** |
| Safe to publish from yours | No | n/a | **Yes — sanitizer included** |
| Third-party credit | Usually missing | n/a | **Linked, never re-uploaded** |
| Memory system explained | No | Sometimes | **Worked example + docs** |
| Personal data in commits | Yes (accidentally) | No | **No (CI-checked)** |

## The two real agents

`agents/legal-de.md` and `agents/tax-de.md` are not toy examples. They are the actual German legal and tax research agents from a working solo founder's daily setup. Both:

- Enforce mandatory source citation (paragraph + URL for every claim)
- End every answer with the statutory disclaimer (§ 2 RDG / § 2 StBerG)
- Refuse to write contracts, file taxes, or do anything that requires a licensed professional
- Use the [kmein/gesetze](https://github.com/kmein/gesetze) GitHub mirror as primary source, with `gesetze-im-internet.de` as the citation-grade fallback
- Cover the BMF Lohnsteuer-PAP via [`canida-software/lohnsteuer`](https://github.com/canida-software/lohnsteuer) (MIT)

If you don't need German law, delete the `agents/` folder and the rest of the kit still works.

## The council skill — try it now

```
/council Should I open-source my Claude Code setup?
```

Five roles answer in parallel — Visionär, Kritiker, Kreativer, Skeptiker, Logiker — then a synthesis layer picks a side. No hedging. No "it depends". One sentence recommendation, plus a checklist of facts that would flip it.

See [`examples/council-publish-decision.md`](examples/council-publish-decision.md) for a real run.

## The sanitizer — run it on your own `~/.claude/`

```bash
./scripts/sanitize-dotclaude.sh ~/.claude
```

Scans every `.md`, `.json`, `.sh`, `.py`, `.js`, `.ts` under `~/.claude/` (except cache and transcript folders) and flags:

- Files with API key patterns (`sk-…`, `AKIA…`, `ghp_…`, `github_pat_…`)
- Files with personal paths (`/Users/<you>/`, `C:\Users\…`)
- Files with email addresses
- Files matching any company/client codename you add to `COMPANY_PATTERNS`

Tested in this repo. Validated against a real live `~/.claude/` containing 337 files (zero false negatives on the maintainer's own agents).

## Why this is public

Long version: [`STORY.md`](STORY.md).

Short version: most Claude Code setups die in private because the maintainer can't separate "what's mine" from "what's my client's". The sanitizer + the two-repo pattern (yours stays private; this one is what you publish) solves that.

## Install components individually

```bash
# Skills only
cp -r skills/council ~/.claude/skills/

# Agents only (skip if you don't need German law)
cp agents/*.md ~/.claude/agents/

# Settings (DIFF FIRST, this overwrites)
diff ~/.claude/settings.json settings.example.json
cp settings.example.json ~/.claude/settings.json

# CLAUDE.md skeleton for a new project
cp templates/CLAUDE.example.md /path/to/your/project/CLAUDE.md
```

## What's NOT in here

| Skill | Source | Why not included |
|---|---|---|
| `when-stuck`, `root-cause-tracing`, `inversion-exercise`, `dispatching-parallel-agents`, `subagent-driven-development` | [obra/superpowers-skills](https://github.com/obra/superpowers-skills) (Jesse Vincent, MIT) | Install from source — they get credit, you get updates |
| `impeccable` / frontend-design | Anthropic (Apache 2.0) | Install from Anthropic's official channels |
| Marketing skill packs (40+) | Commercial / various authors | Buy from the author |
| `huashu-design`, `arcads-external-api` | Third-party | Not mine to redistribute |

See [`docs/04-recommended-third-party.md`](docs/04-recommended-third-party.md) for install instructions.

## Documentation

| Doc | What it covers |
|---|---|
| [`docs/01-getting-started.md`](docs/01-getting-started.md) | Day-1 install + the mental model (CLAUDE.md vs memory vs skills vs agents) |
| [`docs/02-memory-system.md`](docs/02-memory-system.md) | How Claude Code's auto-memory works and what NOT to save |
| [`docs/03-skills-vs-agents.md`](docs/03-skills-vs-agents.md) | When to write a skill vs an agent |
| [`docs/04-recommended-third-party.md`](docs/04-recommended-third-party.md) | Curated list of skills worth installing from elsewhere |
| [`docs/05-naming-conventions.md`](docs/05-naming-conventions.md) | Naming patterns for memory files, skills, agents, slash commands |

## Contributing

PRs welcome — see [`CONTRIBUTING.md`](CONTRIBUTING.md). The main rule: if you contribute an agent or skill, sanitize it the same way these were. The sanitizer in CI will catch most leaks, but a second pair of eyes is required.

Found a leak in the published files? Open a security issue — see [`SECURITY.md`](SECURITY.md).

## License

MIT. See [`LICENSE`](LICENSE). Third-party material linked from `docs/04-recommended-third-party.md` retains its own license — check before redistribution.

---

If this saved you an hour, star it. If it saved you from leaking a client name, send a thank-you to your past self for running the sanitizer.
