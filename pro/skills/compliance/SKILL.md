---
name: compliance
description: >-
  Runs a quarterly security/compliance audit by orchestrating three scanners
  into one consolidated report: Aikido (code/cloud/dependencies/secrets),
  Supabase Advisors (DB/auth hygiene — only if your stack uses Supabase), and
  Prowler (GitHub/Vercel/Cloudflare account-level config). Output is a single
  Markdown report ready as compliance evidence for bank/insurance/government
  customers (GDPR / NIS2 / BSI C5 / ISO 27001 preparation). Use when the user
  wants to run a compliance scan, generate a quarterly compliance report,
  audit security across all projects, or asks about "compliance posture",
  "quarterly compliance report", "security audit", or names any of Aikido /
  Supabase Advisors / Prowler.
---

# Compliance — quarterly audit orchestrator

A pattern, not a runner: this skill describes the orchestration. You wire it
to your environment (your accounts, your tokens, your output dir). The skill
keeps Claude on a predictable rail so you don't redesign the audit each quarter.

| Tool | Scope | Output |
|---|---|---|
| **Aikido** | Code / dependencies / secrets / cloud-misconfig (all repos + cloud) | JSON via REST API |
| **Supabase Advisors** *(if applicable)* | RLS gaps, performance lints, security lints (per project) | JSON via Management API |
| **Prowler** | GitHub org, Vercel team, Cloudflare account-level config | JSON / SARIF via CLI |

The consolidated report is a **compliance evidence asset** — keep one per
quarter, alongside a baseline for trend comparison.

## Third-party accounts you'll need

This skill is the orchestrator — the scanners are run by **your** accounts at:

| Service | Sign up | Free tier |
|---|---|---|
| [Aikido](https://www.aikido.dev/) | [aikido.dev/signup](https://app.aikido.dev/login/signup) | Free tier covers small repos + cloud |
| [Supabase](https://supabase.com/) *(skip if not on it)* | [supabase.com/dashboard](https://supabase.com/dashboard) | Free tier; Advisors API is included |
| [Prowler](https://prowler.com/) | OSS — `pip install prowler` ([docs](https://docs.prowler.com)) | Free OSS CLI; cloud version optional |

## What you need to provide (per environment)

Put these in your local env (a `~/.env.compliance` file, or your usual secret
store — **never** check them in). The skill assumes they are reachable:

```bash
# Aikido
AIKIDO_CLIENT_ID=...
AIKIDO_CLIENT_SECRET=...

# Supabase (skip block if not on Supabase)
SUPABASE_ACCESS_TOKEN=...
# plus any project-scoped PATs you need

# Prowler (one per provider you actually use)
GITHUB_PAT=...                # repo + read:org scope
VERCEL_API_TOKEN=...
CLOUDFLARE_API_TOKEN=...

# Delivery (optional — pick one)
RESEND_API_KEY=...            # or SMTP / Slack webhook / etc.
COMPLIANCE_REPORT_RECIPIENT=you@example.com
```

Suggested project layout:

```
compliance/
  scan.py            # orchestrator (you own this — see "Flow" below)
  scans/             # raw scanner output, timestamped per run
  reports/           # consolidated MD/PDF per quarter
  baseline/          # baseline snapshots for trend comparison
```

## Flow of a quarterly run

1. **Aikido** — OAuth client-credentials → `/issues/export` → classify by severity + repo.
2. **Supabase Advisors** *(skip if not used)* — enumerate `/v1/projects`, then per project hit `/advisors/security` + `/advisors/performance`.
3. **Prowler** (sequential, one per provider you use):
   - `prowler github --personal-access-token $GITHUB_PAT`
   - `prowler vercel --vercel-api-key $VERCEL_API_TOKEN`
   - `prowler cloudflare --cloudflare-api-token $CLOUDFLARE_API_TOKEN`
4. **Trend comparison** with the last baseline (delta findings per severity).
5. **Report generation** — Markdown (PDF optional).
6. **Delivery** — to whatever channel you set in env.

## Unified severity mapping

| Level | Aikido | Supabase | Prowler |
|---|---|---|---|
| critical | critical | (n/a) | critical |
| high | high | error | high |
| medium | medium | warn | medium |
| low / info | low / info | info | low / info |

## Compliance framework mapping (indicative, not legal advice)

- **GDPR**: Art. 32 (TOMs), Art. 25 (Privacy by Design), Art. 30 (records), Art. 33 (breach notification)
- **NIS2** (EU, since Oct 2024): risk management, incident reporting, supply chain
- **BSI C5** (Germany): operational + organisational controls
- **ISO 27001 Annex A**: A.5 (policies), A.8 (asset mgmt), A.9 (access control), A.12 (operations), A.14 (acquisition/dev)

## Report structure

```
# Compliance quarterly report Q{N}/{YYYY}
## Executive summary
## Trend (vs. previous quarter)
## Aikido — code & cloud
## Supabase Advisors — DB / auth hygiene
## Prowler — platform config (GitHub / Vercel / Cloudflare)
## Compliance framework mapping
## Action plan (Q+1)
```

## Scheduling

Run on the **first business day of each quarter** (Jan 1 / Apr 1 / Jul 1 / Oct 1) at 06:00.

- **macOS**: `launchd` `.plist` calling `python3 compliance/scan.py --mode quarterly`.
- **Linux**: `cron` entry: `0 6 1 1,4,7,10 * python3 /path/to/compliance/scan.py --mode quarterly`.
- **Windows**: Task Scheduler with `quarterly` trigger.

On failure, alert via the channel you configured (mail/Slack with the stack trace).

## On-demand run

```bash
python3 compliance/scan.py --mode adhoc
```

## What this skill is NOT

- Not a fix engine — reporting only.
- Not a pen test — no active exploitation.
- Not certification documentation — frameworks mapping is indicative; real
  ISO/SOC2 evidence needs an auditor.
- Not legal advice — for DPO/lawyer matters, ask a human.

## When the user invokes it

1. Check `compliance/last_run.json` for the last run timestamp.
2. > 85 days ago → full quarterly run.
3. < 85 days ago → ad-hoc run only (no baseline rotation).
4. Write report to `compliance/reports/YYYY-Q{N}_compliance.md`.
5. Deliver via configured channel.
