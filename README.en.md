[Deutsch](README.md) · **English**

# claude-starter-kit

**Skills, agents, CLAUDE.md templates and a 10-minute setup for Claude Code — German-first, fully bilingual.**

This is the foundation one founder used to ship 12 real apps alongside a day job — packaged as a public starter kit. Built for anyone who freshly installed [Claude Code](https://docs.claude.com/en/docs/claude-code) and wants a good setup without digging through the docs. Everything below works in English, and the bundled `council` skill answers in whatever language you ask.

[![CI](https://github.com/CommsConnectgmbh/claude-starter-kit/actions/workflows/ci.yml/badge.svg)](https://github.com/CommsConnectgmbh/claude-starter-kit/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/CommsConnectgmbh/claude-starter-kit?style=social)](https://github.com/CommsConnectgmbh/claude-starter-kit/stargazers)

![/council in action — Claude runs five perspectives on a decision and gives one clear recommendation](assets/council-demo-en.gif)

*One of the bundled skills: `/council` runs five perspectives on a decision and gives one clear recommendation — real recording.*

---

**You just installed [Claude Code](https://docs.claude.com/en/docs/claude-code). Now what?**

Do these three things and you have a solid setup. Ten minutes.

---

## 1. Put a CLAUDE.md into your project

`CLAUDE.md` is a small file in your project's root. Claude reads it automatically on every request. It holds: what the project is, which commands exist (`npm run dev`, `pytest`, etc.), and what Claude must NOT do.

```bash
git clone https://github.com/CommsConnectgmbh/claude-starter-kit.git
cd your-project
cp ../claude-starter-kit/templates/CLAUDE.example.md CLAUDE.md
```

Then open `CLAUDE.md` and fill in the blanks (5 minutes). Saves you from repeating it in every conversation.

---

## 2. Install the core skills (one command)

```bash
cd claude-starter-kit
./install.sh            # interactive — shows diffs before anything is overwritten
# or fully non-interactive:
./install.sh --yes
```

This installs four skills + (optionally) the German legal/tax agents + a safe `settings.json` template. Fresh machine? Runs straight through, nothing to overwrite.

| Skill | For what |
|---|---|
| `council` | A decision on the table (build feature X? plan A or B?)? Claude runs 5 perspectives (Visionary, Critic, Creative, Skeptic, Logician), names the contradictions, and gives one clear recommendation. No hedging. |
| `scrape` | Pull read-only data from a website as clean JSON. |
| `skillify` | Turn a successful `/scrape` into a reusable script — instant next time. |
| `canary` | After a deploy, watch the live URL and alert only on real regressions (relative to a baseline, not absolute). |

Try it: type `/council Should I ship my half-built feature to ten users now, or finish it first?` in Claude Code — this is what it looks like ([GIF above](#claude-starter-kit), [how it's made](assets/council-demo/)).

<details>
<summary><b>Another example as text</b> — different question, click to expand 👇</summary>

<br>

> **Question:** `/council Should I spend this month building the next feature, or on marketing to get my first users?`

**Decision** — Spend this month building the next feature, or spend it on marketing to acquire the first users?

**Visionary** — Marketing now means your first ten users start feeding you real signal — every future feature gets built against reality instead of guesswork, compounding for years. First users also become case studies, referrals, and the story you tell the next hundred. The feature can wait; a live feedback loop can't.

**Critic** — The framing assumes the product is already good enough to market — that's the unexamined claim. It also treats "a feature" and "marketing" as month-sized blocks, when both are really weeks of work plus indefinite iteration. And "first users" hides the real question: paying users, or just signups?

**Creative** — Why one whole month on either? A third path: spend one week shipping the feature *as* the marketing — build the smallest thing that gives you something worth talking about, then spend the rest reaching out to 30 hand-picked prospects. Or skip both and do 15 customer interviews first to learn whether the missing feature is even the blocker to adoption.

**Skeptic** — Building a feature nobody has asked for is the most reversible-looking but most expensive mistake: a month gone, zero validation, and you still don't know if anyone wants it. Marketing's downside is smaller — worst case you get rejection, which is itself data. The asymmetry favors marketing.

**Logician** — With zero users, feature-value is unmeasurable — you have no denominator. Marketing produces a countable output (conversations, signups, conversion rate) within the month; building does not. One number you can compute beats one you can't.

**Conflict** — Visionary/Skeptic/Logician say ship-to-market now; Critic says the product may not be ready to market at all. That's the real fault line: is lack of a feature the reason nobody's signed up, or have you just never asked anyone?

**Synthesis** — I side with the Skeptic and Logician over the Visionary's romance and the Critic's caution: with zero users, the binding constraint is *information*, and marketing is the only one of the two that produces measurable information this month. I reject building — it spends your scarcest asset (time before validation) on an unfalsifiable bet. I fold in the Creative's discipline: aim outreach at a specific, narrow prospect list, not broad noise.

**Recommendation** — Spend this month on direct outreach to get your first users, and let their reactions decide the next feature.

**What would flip this recommendation**
- You already have engaged users who are churning or blocked specifically by the missing feature.
- The product genuinely cannot be demoed or onboarded without that feature (it's table-stakes, not enhancement).
- You have prior evidence that marketing converts poorly *because* of that specific gap.

</details>

> Only need individual ones? `cp skills/<name>/SKILL.md ~/.claude/skills/<name>/` is enough.

---

## 3. Understand auto-memory (5 min read, no install)

Claude Code automatically remembers things about you across conversations — who you are, how you work, what your projects are. It's the underrated killer feature.

Skim [`docs/02-memory-system.md`](docs/02-memory-system.md). Then in your next conversation just tell Claude: "I'm a <role>, mostly work on <project>, prefer <style>." It stores that automatically and uses it from then on.

---

**That's it. You're set up.**

Did this save you an afternoon of digging through docs? A ⭐ helps others find the kit.

---

## What else is in the repo (optional)

> Note: the in-depth guides under `docs/` and the two domain agents are currently **German-only** (they're German legal/tax research agents). The skills, patterns and templates themselves are language-agnostic.

| What | For what |
|---|---|
| [`docs/01-getting-started.md`](docs/01-getting-started.md) | The mental model behind Claude Code (Settings vs CLAUDE.md vs Memory vs Skills vs Agents) |
| [`docs/04-the-daily-loop.md`](docs/04-the-daily-loop.md) | **How to drive Claude through real tasks** — explore → plan → code → commit, context discipline, verification, session handover |
| [`docs/03-skills-vs-agents.md`](docs/03-skills-vs-agents.md) | When skills, when agents — the most common mix-up |
| [`docs/05-self-healing-apps.md`](docs/05-self-healing-apps.md) | **Apps that repair themselves from their own usage** — synthetic user + fix agent, nightly, with hard safety guardrails |
| [`docs/06-linear-issues.md`](docs/06-linear-issues.md) | **Wire Claude to an issue tracker (Linear)** — file findings safely instead of fixing unattended; the gating pattern |
| [`docs/07-mcps.md`](docs/07-mcps.md) | **MCP overview** — the curated shortlist (Linear, Sentry, Supabase), one-line setup, pairing with self-heal |
| [`docs/08-third-party-accounts.md`](docs/08-third-party-accounts.md) | **Which third-party accounts you need for what** — sign-up links, free-tier status, minimal vs extended |
| [`docs/09-seo.md`](docs/09-seo.md) | **SEO with a measuring engine** — install the `claude-seo` plugin cleanly (`/seo audit <url>`), dodge the macOS Python-deps trap, and which fixes actually move rankings |
| [`docs/10-token-efficiency.md`](docs/10-token-efficiency.md) | **Token efficiency — what actually helps, what's hype** — why `CLAUDE.md` is the real lever, and how to measure any "70× fewer tokens" tool against your own repo in ten minutes instead of believing the benchmark |
| [`agents/legal-de.md`](agents/legal-de.md) + [`agents/tax-de.md`](agents/tax-de.md) | **Real German legal & tax research agents** as a worked example of how a domain agent is built (source discipline, disclaimer, workflow) |
| [`templates/memory/`](templates/memory/) | Example of what memory entries should look like |
| [`templates/desktop-launchers/`](templates/desktop-launchers/) | **Double-click launchers** for Mac (`.command`) + Windows (`.bat`) — Claude straight in skip-permissions mode |
| [`install.sh`](install.sh) | One-command installer for everything above (`--yes`, `--with-pro`, `--no-agents`, `--with-launcher`) |
| [`pro/skills/`](pro/skills/) | **Optional pro layer**: 6 bundled skills (`autoplan`, `spec`, `second-opinion`, `compliance`, `fal-ai`, `openai-image`) + 5 cloned obra skills |
| [`pro/self-heal/`](pro/self-heal/) | **Runnable self-healing**: synthetic Playwright user + fix-PR agent + launchd/cron template |

To install the German agents individually:
```bash
mkdir -p ~/.claude/agents
cp agents/legal-de.md agents/tax-de.md ~/.claude/agents/
```

---

## Pro layer (optional)

Heavier workflow skills, opt-in:

```bash
./install.sh --with-pro      # core + pro in one
# or pro only:
cd pro/skills && ./install-pro-skills.sh
```

- **Bundled** (in this repo, MIT):
  - `autoplan`, `spec` (gstack-derived) — planning through multi-lens review; vague idea → executable spec
  - `second-opinion` — free local code reviewer via Ollama (Codex-plugin replacement)
  - `compliance` — quarterly audit pattern (Aikido + Supabase Advisors + Prowler)
  - `fal-ai`, `openai-image` — direct API access for marketing creative (BYO key)
- **Cloned** (obra/superpowers, MIT): `when-stuck`, `root-cause-tracing`, `inversion-exercise`, `dispatching-parallel-agents`, `subagent-driven-development`.

`autoplan`/`spec` call optional companion skills (frontend design, an independent reviewer = `second-opinion`) — if they're missing, that phase is cleanly skipped. Details: [`pro/skills/README.md`](pro/skills/README.md).

Also in the pro layer: [`pro/dreaming/`](pro/dreaming/) — a nightly memory curator that dedupes your auto-memory, finds stale entries and keeps the index in sync (launchd/cron template included).

---

## Self-Healing: apps that repair themselves from their usage (optional)

A nightly loop that finds real bugs in your apps and opens fix PRs — **without a single real user needed**, and with guardrails that stop anything from going live unattended.

```
  synthetic user       →   error capture         →   fix agent
  (clicks happy paths)     (monitor + run.mjs)       (Claude Code → PR)
```

- **Don't build a worse Sentry.** For real traffic: wire in a real error monitor.
- **The real lever is the synthetic user** — Playwright clicks the main flows every night, catches console/page errors, failed requests, HTTP 5xx.
- **The fix agent is yours:** dry-run by default, capped per run, **opens PRs, never merges**, sensitive repos (real customers/billing) are **issue-only**.

Setup in [`pro/self-heal/README.md`](pro/self-heal/README.md), the why in [`docs/05-self-healing-apps.md`](docs/05-self-healing-apps.md).

```bash
cd pro/self-heal && npm install && npx playwright install chromium
node synthetic/run.mjs            # findings to synthetic/reports/
node agent/fix.mjs                # DRY-RUN — only shows what it would fix
```

---

## MCPs: connect Claude to your real tools (optional)

[MCPs (Model Context Protocol servers)](https://modelcontextprotocol.io) are how Claude Code talks to the outside world — issue tracker, error monitor, DB, CRM. The curated shortlist that fits the rest of the kit:

```bash
claude mcp add --transport sse  linear   https://mcp.linear.app/sse      # safe landing for "found, don't fix yet"
claude mcp add --transport http sentry   https://mcp.sentry.dev/mcp      # real error monitor for self-heal
claude mcp add --transport http supabase https://mcp.supabase.com/mcp    # schema/SQL/logs, if your stack is Supabase
```

OAuth on first call, no API key in `.env`. Only add the ones that fit your stack. Details + gating pattern: [`docs/07-mcps.md`](docs/07-mcps.md) + [`docs/06-linear-issues.md`](docs/06-linear-issues.md).

---

## Desktop launcher: double-click instead of terminal (optional)

Don't feel like opening a terminal every time? The kit ships a double-click launcher for both worlds that starts Claude straight in skip-permissions mode (no prompt before each tool call — only sensible on your own, trusted machine).

**Mac:**
```bash
./install.sh --with-launcher
# creates ~/Desktop/start-claude.command, executable, done.
```

**Windows:**
```cmd
copy templates\desktop-launchers\start-claude.bat "%USERPROFILE%\Desktop\"
```

Details + troubleshooting: [`templates/desktop-launchers/README.md`](templates/desktop-launchers/README.md).

---

## License

MIT. Do whatever you want with it. Bug or improvement? Issue or PR.

---

Built by [Rainer Roloff](https://rainerroloff.de) — more projects around Claude Code and a "get in touch" at [rainerroloff.de](https://rainerroloff.de).
