---
name: scrape
description: "Pull structured data from a web page, read-only, and emit it as clean JSON. Given a one-line intent ('top stories on Hacker News', 'product names + prices on example.com/products'), fetch the page, find the data, parse it, return one JSON document on stdout. Use for one-shot data extraction the user wants as machine-readable output. Trigger phrases: 'scrape', 'zieh die daten von', 'extrahier von der seite', 'hol mir als JSON', 'pull data from', 'parse this page'. Read-only: refuses mutating intents (login, submit, post, order). For repeated scrapes, follow with /skillify to save it as a reusable scraper. NOT for multi-page crawls or auth flows."
argument-hint: "<one-line intent or URL>"
user-invocable: true
source: "Reimplemented from garrytan/gstack /scrape (MIT). The intent → prototype → JSON methodology and read-only discipline are ported; the gstack $B browse daemon and the $B skill registry/match path are replaced by WebFetch (static) + Playwright via npx (JS-rendered). The skill-match path becomes the companion /skillify scraper lookup."
---

# /scrape — Read-only web data extraction

One-line intent in, one JSON document out.

## Step 1 — Determine intent
The text after `/scrape` is the intent. If absent, ask once: *"What do you want to
scrape? One line, e.g. 'top stories on Hacker News' or 'product names + prices on
example.com/products'."* Don't front-load clarifying questions — cheaper to refine
while prototyping.

## Step 2 — Refuse mutating intents
If the intent implies writes — *submit, post, send, log in, click X, fill the form,
delete, create, order, book* — refuse:
> "/scrape is read-only. For mutating flows, drive the page directly with Playwright
> or ask for a dedicated automation script."
Stop. Do not enter the prototype path.

## Step 3 — Check for an existing saved scraper
Look in `scrapers/` (repo root) for a saved scraper whose `intent`/triggers match
(written by /skillify). If `scrapers/<name>.mjs` exists and clearly covers this intent:
```bash
node scrapers/<name>.mjs   # prints the JSON directly
```
Emit its JSON and stop. If no confident match, fall through to the prototype path.

## Step 4 — Prototype path
Pick the lightest tool that works:

**A. Static HTML (default — try first):** use the **WebFetch** tool on the URL with a
prompt that asks for the specific data as JSON. Good for server-rendered pages.

**B. JS-rendered / WebFetch came back empty or partial:** use Playwright via npx.
Write a throwaway probe, iterate selectors against the real HTML:
```bash
cat > /tmp/scrape-$$.mjs <<'EOF'
import { chromium } from 'playwright';
const url = process.argv[2];
const b = await chromium.launch();
const p = await b.newPage();
await p.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
const html = await p.content();
await b.close();
process.stdout.write(html);
EOF
npx -y playwright@latest /tmp/scrape-$$.mjs "<url>" > /tmp/scrape-$$.html
```
Then read `/tmp/scrape-$$.html`, find the repeating structure (list rows, table cells,
cards), and extract. For lists of links, pull `a[href]`. Iterate: try a selector, check
the output, refine. (Run `npx -y playwright@latest install chromium` once if the browser is missing.)

## Step 5 — Emit
One JSON document on stdout. Use a stable shape — typically `{ "items": [...], "count": N }`.
Do not wrap it in prose in the chat reply (callers pipe to `jq`) unless the user asked
for an explanation. Logs and notes go in chat, not in the JSON.

## Step 6 — Skillify nudge
After a successful prototype, append exactly one line and nothing more:
> "Say /skillify to save this as a reusable scraper (instant on next call)."

## When the prototype fails
If after 3–4 selector attempts no sensible JSON shape emerges:
- Report what you tried, what came back, what's blocking (lazy-loaded, JS-gated, paywalled, bot-blocked).
- Do NOT write a partial result and call it done. Do NOT suggest /skillify on a broken prototype.
- Ask: (a) try a different selector, (b) different page, or (c) stop.

## What this skill does NOT do
- Mutating actions, auth/login flows, cookie import, multi-page crawls. One-shot, read-only, per call.

## Respect & limits
- Honor `robots.txt` intent and rate limits; this is for data the user is entitled to read.
- Never scrape anything behind a login the user hasn't authorized you to use.
