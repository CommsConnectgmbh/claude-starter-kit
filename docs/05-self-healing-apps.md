# Self-healing apps: turn usage into fixes

The first four docs were about driving Claude through *one* task. This one is about a system
that runs without you: your apps find their own bugs and propose fixes overnight.

The runnable version lives in [`pro/self-heal/`](../pro/self-heal/). This doc is the *why* —
read it before you wire it up, because the design decisions are the whole point.

## The trap: don't build a worse Sentry

The obvious first instinct is to build a little error collector — an SDK, an ingest endpoint,
a database table. Resist it. Error monitoring is a solved, commoditised problem: tools like
Sentry already do grouping, fingerprinting, dedup, PII scrubbing, rate limiting and release
tracking, across web / React Native / Capacitor, free at small scale.

So for **real** traffic: install a real error monitor and move on. Sentry has an MCP server,
so the fix-agent can read what real users hit without you scraping a dashboard — see
[docs/07](07-mcps.md). The interesting work is everywhere a monitor *can't* help you.

## The real gap: no users, no signal

An error monitor only ever sees what real people trigger. Before you have traffic, the
dashboard stays empty — which feels like "no bugs" but means "no observers." That's the gap
worth building into:

**A synthetic user.** A headless browser that clicks your main journeys every night —
sign in, send the message, upload the receipt, place the bet — while a harness watches for
console errors, page errors, failed requests and HTTP 5xx. Bugs surface with zero real users.
This is exactly how a "feature X is broken" bug gets caught the night you ship it instead of
the week a customer finally hits it.

**A fix-agent you control.** Rather than a vendor's black-box autofixer, a `claude -p` job
reads the night's findings, reproduces them, writes the minimal fix, runs the tests, and opens
a PR. On a Claude subscription this is free and lives inside your normal review flow.

```
  synthetic user        →   error capture        →   fix-agent
  (clicks happy paths)      (real monitor + run.mjs)  (Claude Code → PR)
```

## Why it's safe to let it run

Autonomy is only acceptable because of what the agent **cannot** do. These aren't optional:

- **Dry-run by default** — it shows the plan; code changes need an explicit `--live`.
- **Capped per run** — one fix at a time by default, never a storm of PRs.
- **Opens PRs, never merges** — merge stays gated on green tests or a human.
- **Issue-only for sensitive repos** — anything with real customers or billing gets a
  diagnosis issue, never an unsupervised code change. (This is where [Linear](06-linear-issues.md)
  comes in — the safe landing spot for "found, not yet fixed.")
- **Noise filter** — login/setup failures and third-party request errors are skipped, not
  "fixed" into fake patches.

## When to reach for this

- You ship small and often (especially "straight to production") and want a net under it.
- You have several apps and can't manually click every flow after every deploy.
- You're pre-revenue and your monitoring is silent — *because* nobody's using it yet.

Start with one flow on one app in dry-run. Watch a few reports. Only then turn on `--live`,
and only on a repo where an unwanted PR is harmless. Trust is earned one green run at a time.
