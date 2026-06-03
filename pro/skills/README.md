# Pro Skills

An optional layer on top of the core kit — workflow and reasoning skills for heavier
day-to-day work. Two sources, one installer:

1. **Bundled here** (`autoplan`, `spec`) — gstack-derived, MIT, shipped in this repo.
2. **Cloned from upstream** (`when-stuck`, `root-cause-tracing`, …) — copied straight
   from `obra/superpowers-skills` so attribution stays intact and updates flow back.

## Install

```bash
./install-pro-skills.sh        # interactive: shows a diff before overwriting
./install-pro-skills.sh --yes  # non-interactive
```

## What gets installed

### Bundled (gstack-derived, MIT — [garrytan/gstack](https://github.com/garrytan/gstack))

| Skill | What it does |
|---|---|
| `autoplan` | Run a rough plan through a multi-lens review gauntlet (strategy → architecture → design → feasibility), auto-deciding routine questions and surfacing only real taste calls at one approval gate. |
| `spec` | Turn vague intent into a precise, executable spec — five strict phases, grounded in your actual code, with an optional quality gate. |

> **Companion skills are optional.** `autoplan` and `spec` call out to other skills if
> they're installed and **degrade gracefully** if not:
> - `council` — bundled in the core kit (`../../skills/council`). Install it for the strategy phase.
> - A **frontend-design** skill (e.g. `impeccable`) — for `autoplan`'s Design phase. Not bundled; bring your own.
> - An **independent-reviewer** skill (e.g. a local-model reviewer) — for the feasibility/quality gate. Not bundled; bring your own.
>
> Missing a companion just skips that phase with a one-line note. Nothing blocks.

### Cloned ([obra/superpowers-skills](https://github.com/obra/superpowers-skills), MIT — Jesse Vincent)

| Skill | What it does |
|---|---|
| `when-stuck` | Matches your kind of stuck-ness to the right technique (simplification, inversion, root-cause-tracing). |
| `root-cause-tracing` | Trace bugs backward through the call chain instead of patching symptoms. |
| `inversion-exercise` | Flip an unquestioned assumption to find a third path. |
| `dispatching-parallel-agents` | When 3+ independent failures could be investigated concurrently. |
| `subagent-driven-development` | Multi-task plan execution with a fresh subagent per task + review gates. |

The installer clones `obra/superpowers-skills` into a temp dir, copies only the five
skills above into `~/.claude/skills/`, and shows a diff before overwriting. There are
many more upstream (debugging, testing, planning, code review) — browse the repo and
copy any you want in manually.

## UI/UX skills (not bundled)

Skills like `ui-ux-pro-max`, `impeccable`, `huashu-design`, and `design-motion-principles`
are great for frontend work but each comes from a different source with its own license.
Not redistributed here. If you want them:

- `impeccable` — adapted from Anthropic's frontend-design skill (Apache 2.0); search the Anthropic Skills docs.
- `ui-ux-pro-max`, `huashu-design`, `design-motion-principles` — search the community Claude skill registries.

Drop any you find into `~/.claude/skills/<name>/SKILL.md`.

## Why a separate tier?

- **Lean core.** The base kit stays small and runs immediately for everyone. Pro is opt-in.
- **Clean attribution.** Upstream stays the source of truth for the cloned skills; bundled ones carry their `source:` line.
