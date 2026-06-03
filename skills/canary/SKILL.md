---
name: canary
description: "Post-deploy canary monitoring for a web app — capture a baseline before deploy, then watch the live URL for a window after deploy and alert on regressions (page load failures, NEW console errors, performance regressions, new 404s) relative to the baseline, not absolutes. Use right after pushing to production, especially for setups that ship straight to production without a staging environment. Trigger phrases: 'canary', 'überwach den deploy', 'check production nach dem deploy', 'monitor the live site', 'post-deploy check', 'ist der deploy gesund', 'smoke-test prod'. NOT for pre-merge code review (use /code-review) or functional QA (use /verify)."
argument-hint: "<production-url> [--baseline] [--duration 10m] [--pages /,/dashboard] [--quick]"
user-invocable: true
source: "Reimplemented from garrytan/gstack /canary (MIT). Methodology (baseline → monitor-loop → relative-alert → health report) ported; the gstack browse daemon ($B) is replaced by a self-contained Playwright runner via npx."
---

# /canary — Post-deploy monitoring

Watch a freshly deployed URL and alert on what **changed** vs a baseline. Start fast:
begin monitoring within ~30s of invocation; don't over-analyze first.

## Arguments
- `/canary <url>` — monitor for 10 minutes after deploy.
- `--baseline` — capture baseline BEFORE deploying (run this first, ideally).
- `--duration 5m` — custom window (1m–30m).
- `--pages /,/dashboard,/settings` — explicit page list (else auto-discover).
- `--quick` — single-pass health check, no continuous loop.

## Engine — Playwright via npx (no global install needed)
All page checks use one throwaway script. Write it once to a temp file, then call it
per page. It captures screenshot + console errors + load time as JSON.

```bash
mkdir -p .canary-reports/baselines .canary-reports/screenshots
cat > .canary-reports/_probe.mjs <<'EOF'
import { chromium } from 'playwright';
const [url, shot] = [process.argv[2], process.argv[3]];
const errors = [];
const b = await chromium.launch();
const p = await b.newPage();
p.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
p.on('pageerror', e => errors.push(String(e)));
const t0 = Date.now();
let status = 0, ok = true;
try { const r = await p.goto(url, { waitUntil: 'load', timeout: 30000 }); status = r ? r.status() : 0; }
catch (e) { ok = false; errors.push('GOTO_FAILED: ' + e.message); }
const load_ms = Date.now() - t0;
if (shot) await p.screenshot({ path: shot, fullPage: true }).catch(() => {});
await b.close();
process.stdout.write(JSON.stringify({ url, ok, status, load_ms, console_errors: errors.length, errors }));
EOF
# Run a probe like:  npx -y playwright@latest .canary-reports/_probe.mjs "<url>" ".canary-reports/screenshots/home-1.png"
```
If `npx playwright` reports a missing browser, run `npx -y playwright@latest install chromium` once.

## Phase 1 — Setup
Parse args. Default duration 10m. Default pages: auto-discover from nav.

## Phase 2 — Baseline (`--baseline` mode, run BEFORE deploy)
For each page (or homepage), run the probe and record screenshot path, console-error
count, load time. Write `.canary-reports/baseline.json`:
```json
{ "url": "<url>", "timestamp": "<ISO>", "branch": "<branch>",
  "pages": { "/": { "screenshot": "baselines/home.png", "console_errors": 0, "load_time_ms": 450 } } }
```
Then STOP: "Baseline captured. Deploy, then run `/canary <url>` to monitor."

## Phase 3 — Page discovery
If no `--pages`, navigate the homepage, extract the top ~5 internal nav links via the
probe (add `a[href]` extraction), always include `/`, and confirm the list with the
user via AskUserQuestion (A: these pages / B: add more / C: homepage only).

## Phase 4 — Pre-deploy snapshot (if no baseline exists)
No `baseline.json`? Probe each monitored page once now as the reference point. Record
console-error count + load time per page.

## Phase 5 — Continuous monitoring loop
Monitor for the window. Every 60s, probe each page and compare against baseline/reference:
1. **Page load failure** (`ok:false` / timeout) → **CRITICAL**
2. **New console errors** (count above baseline) → **HIGH**
3. **Perf regression** (load_ms > 2× baseline) → **MEDIUM**
4. **New 404s** (status 404 not in baseline) → **LOW**

Rules:
- **Alert on changes, not absolutes.** 3 baseline errors staying at 3 is fine; one NEW error alerts.
- **Don't cry wolf.** Only alert on patterns persisting across 2+ consecutive checks; a single blip is not an alert.
- On CRITICAL/HIGH, notify immediately via AskUserQuestion with an alert block (time, page, type, finding, screenshot path, baseline vs current) and options: A) investigate now / B) keep watching (transient) / C) rollback the deploy / D) dismiss as false positive.

Use a `sleep 60` between checks; keep looping for the full window — do not stop early
or hand off to a notification.

## Phase 6 — Health report
On completion (or early stop) write `.canary-reports/<date>-canary.md` (+ `.json`):
```
CANARY REPORT — <url>
Duration: X min | Pages: N | Checks: N | Status: HEALTHY / DEGRADED / BROKEN
Per-page: page | status | new errors | avg load (vs baseline)
Alerts fired: N (x critical, y high, z medium)
VERDICT: DEPLOY IS HEALTHY / HAS ISSUES — details above
```

## Phase 7 — Baseline update
If healthy, offer (AskUserQuestion) to copy the latest screenshots over the baseline
and refresh `baseline.json`. Otherwise keep the old baseline.

## Honest limits
- Without a baseline, canary degrades to a plain health check — encourage `--baseline` before deploying.
- Perf thresholds are relative (2× = regression); 1.5× may be normal variance.
- Screenshots are evidence — every alert cites a screenshot path.
