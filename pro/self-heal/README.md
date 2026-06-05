# self-heal — apps that improve themselves from their own usage

A nightly loop that finds real bugs in your apps and opens fix PRs for them — with zero
real users required, and with hard guardrails so nothing ships unsupervised.

Three moving parts, each doing only what it's uniquely good at:

```
  synthetic user        →   error capture        →   fix-agent
  (clicks happy paths)      (console/page/5xx)       (Claude Code → PR)
```

## Why this shape

**Capture = use your error monitor.** Don't build a worse Sentry. A real error-monitoring SDK
(Sentry, etc.) already groups, dedupes, scrubs PII and tracks releases across web / RN /
Capacitor — for free at small scale. Wire that into your apps for *real* traffic.

**But monitoring only catches what real users trigger.** Pre-revenue, that surface is empty.
So you build the one thing off-the-shelf tools don't give you:

1. **A synthetic user** (`synthetic/`) — Playwright clicks each app's main journeys every
   night and reports what breaks. Bugs surface without a single real user.
2. **A fix-agent under your control** (`agent/`) — instead of a black-box autofixer, a
   `claude -p` job reads the findings, reproduces, writes the fix, runs tests, opens a PR.

## Setup

```bash
cd pro/self-heal
npm install                              # pulls in playwright (see package.json)
npx playwright install chromium          # browser binary, one time

# 1. Add a flow per critical path (copy synthetic/flows/example.mjs)
# 2. Map flow → repo:
cp agent/repos.example.json agent/repos.json   # then edit paths

node synthetic/run.mjs                    # see findings in synthetic/reports/
node agent/fix.mjs                        # DRY-RUN — prints what it would fix
node agent/fix.mjs --live                 # actually open PRs/issues (start small)
```

Schedule `nightly.sh` with the launchd template in `../launchd/` (macOS) or cron (Linux).

## The guardrails (this is the important part)

Autonomy is only safe because of what the agent **cannot** do:

- **Dry-run by default.** `fix.mjs` shows the plan; real changes need `--live`.
- **Capped per run** (`SELF_HEAL_MAX`, default 1). No PR storms.
- **Opens PRs, never merges.** Merge stays gated on green tests or a human.
- **Issue-only repos.** Mark anything with real customers or billing `"issueOnly": true` —
  it gets a diagnosis issue, never an unsupervised code change.
- **Noise filter.** Login/test-setup failures and third-party request errors are skipped,
  not "fixed".

## Files

| Path | What |
|---|---|
| `synthetic/run.mjs` | Browser harness: runs flows, captures errors, writes deduped reports |
| `synthetic/flows/example.mjs` | Template for one user journey — copy per critical path |
| `agent/fix.mjs` | Reads latest report → spawns Claude Code to fix → PR (or issue) |
| `agent/repos.example.json` | Flow → repo map; copy to `repos.json` |
| `nightly.sh` | synthetic run + dry-run fixer, for scheduling |

Reports and `repos.json` are gitignored — they're machine- and bug-specific, not source.
