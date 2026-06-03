# claude-dreaming

A nightly memory curator for Claude Code's auto-memory.

Claude Code automatically writes memory files about you, your projects, your feedback. Over time those files drift — duplicates pile up, project status gets stale, the index falls out of sync with the files. That bloats every conversation's context (more tokens, slower starts) and the noise can dilute the signal Claude actually uses.

`claude-dreaming` runs once a night, reads every memory file, asks Claude to review the whole set, and writes a report. High-confidence suggestions (default >= 0.85) apply automatically with full backups. Lower-confidence ones wait for your review.

## What it catches

- **Duplicates** — two files saying the same thing (e.g. `feedback_no_demo.md` + `feedback_demo_off.md`) → merge proposal
- **Stale entries** — projects marked active that obviously aren't anymore
- **Index drift** — `MEMORY.md` description that no longer matches the file's body
- **Missing index entries** — orphan memory files Claude can no longer surface
- **Recurring patterns** — themes spread across 3+ files with no dedicated memory yet → suggest a new one
- **Naming inconsistencies** — same semantic type filed under different prefixes

## Why it pays off

Claude Code's auto-memory grows monotonically. Every new project, every correction, every reference adds a file. Without curation you eventually hit:
- `MEMORY.md` getting truncated at line 200 (newer entries silently disappear)
- Token bloat (~150 memory files at 1 KB each = ~150 KB pulled into every relevant turn)
- Stale data competing with fresh data for Claude's attention

Curation keeps the index lean and the files accurate. See [`docs/05-memory-hygiene.md`](../../docs/05-memory-hygiene.md) for the full pattern.

## Requirements

- `node` >= 18
- `claude` CLI installed and logged in (Max plan recommended — the script unsets `ANTHROPIC_API_KEY` to avoid API billing)
- Read/write access to your memory folder

## Manual run

```bash
MEMORY_DIR=/absolute/path/to/your/memory node dream.mjs
# review the report in $MEMORY_DIR/.dreaming-log/<date>.md
MEMORY_DIR=/absolute/path/to/your/memory node dream.mjs --apply 2026-01-15
```

Backups land in `$MEMORY_DIR/.dreaming-log/applied/`. Nothing is destroyed without a backup.

## Finding your MEMORY_DIR

Look at any system reminder Claude Code shows you — the auto-memory section names the absolute path. Typical shape:
```
~/.claude/projects/<encoded-cwd>/memory
```

## Scheduling

### macOS (launchd)

Use `../launchd/de.user.claude-dreaming.plist.template` — replace the four `__PLACEHOLDER__` tokens and `launchctl load` it. See the template header for details.

### Linux (cron / systemd)

Cron one-liner (3 AM nightly):
```cron
0 3 * * * MEMORY_DIR=/path/to/memory PATH=/usr/local/bin:/usr/bin:/bin /path/to/pro/dreaming/run-nightly.sh
```

### Windows (Task Scheduler)

Create a daily task running `node dream.mjs` with `MEMORY_DIR` set in the action's environment, and a second task five minutes later for `node dream.mjs --apply <today>`. Or wrap both in a single `.cmd` script analogous to `run-nightly.sh`.

## Configuration

| Env var | Default | Meaning |
|---|---|---|
| `MEMORY_DIR` | (required) | Absolute path to memory folder |
| `CLAUDE_BIN` | `claude` | Path to the `claude` CLI |
| `APPLY_THRESHOLD` | `0.85` | Minimum confidence for auto-apply |
| `LANGUAGE` | `en` | Prompt language: `en` or `de` |

## Safety model

- **Backups before every change.** Every applied edit copies the original to `.dreaming-log/applied/<date>__<filename>` first.
- **Confidence gate.** Only suggestions with confidence ≥ `APPLY_THRESHOLD` are touched. Anything below stays in the report for manual review.
- **Patterns + renames never auto-apply.** New-memory proposals and file renames always require your review — too easy to lose context.
- **No network egress beyond `claude` itself.** The script only reads/writes the memory folder and shells out to the local `claude` CLI.
