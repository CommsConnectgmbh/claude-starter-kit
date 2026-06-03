---
name: skillify
description: "Codify the most recent successful /scrape into a permanent, reusable scraper script on disk (scrapers/<name>.mjs) plus a small manifest, so the next time the same data is needed it runs instantly instead of re-prototyping. Use right after a /scrape that produced JSON the user accepted. Trigger phrases: 'skillify', 'mach das wiederverwendbar', 'speicher den scraper', 'save this scrape', 'make it permanent', 'als skript ablegen'. Refuses if there is no recent successful /scrape in the conversation, and never writes a half-broken script to disk."
user-invocable: true
source: "Adapted from garrytan/gstack /skillify (MIT). The provenance guard, iron 'never ship a half-broken skill' contract, and synthesize-from-final-attempt discipline are ported; gstack's $B browse-skill registry + per-tier install is replaced by a plain self-contained scrapers/<name>.mjs + scrapers/manifest.json that /scrape looks up."
---

# /skillify — Turn a successful scrape into a reusable scraper

Codify the last good `/scrape` into a standalone script. The contract: **never write a
half-broken scraper to disk.** Write to a temp file, run it, and only move it into
`scrapers/` on (a) a passing run + (b) explicit user approval. On either failure, the
temp file is removed. There is no "almost shipped" state.

## Step 1 — Provenance guard
Walk back through the conversation, **at most 10 turns**, for the most recent `/scrape`
that was bounded (you can identify the intent line and the trailing JSON it produced)
and that the user did NOT invalidate ("that's wrong", "retry"). If none, refuse with
exactly:
> "No recent /scrape result found in this conversation. Run /scrape <intent> first, then say /skillify."
Stop. Do not synthesize from chat fragments. Do not skillify a scrape that came from an
already-saved scraper (Step 3 of /scrape) — there's nothing new to codify.

If the candidate is a few turns back and the user has since moved on, confirm once:
*"The last successful /scrape was '<intent>' a few turns back. Skillify that one?"*
A "yes" continues; anything else refuses with the message above.

## Step 2 — Propose name
From the intent, derive a short name: lowercase letters/digits/dashes, ≤32 chars,
starts with a letter, no consecutive dashes (e.g. `hn-frontpage`, `pypi-stats`). Check
`scrapers/manifest.json` for a name collision; if it exists, propose a distinct name.
Confirm the name with the user (AskUserQuestion), with the proposed name as the
recommended option.

## Step 3 — Synthesize the script
Use **only the final, working** fetch/selector logic that produced the accepted JSON.
Drop failed selector attempts, unrelated commands, and all conversation prose. Keep the
parsing in a **pure function** so it's testable without the network.

```js
// scrapers/<name>.mjs  — reusable, self-contained
const TARGET_URL = '<the URL the prototype used>';

// Pure: HTML in, parsed rows out. No fetch here.
export function parse(html) {
  const items = [];
  // ...the working extraction logic...
  return items;
}

async function getHtml(url) {
  // Path A (static): plain fetch — use when /scrape succeeded via WebFetch.
  const r = await fetch(url, { headers: { 'user-agent': 'Mozilla/5.0 scrape-bot' } });
  return await r.text();
  // Path B (JS-rendered): if the prototype needed Playwright, replace the body with:
  //   const { chromium } = await import('playwright');
  //   const b = await chromium.launch(); const p = await b.newPage();
  //   await p.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
  //   const html = await p.content(); await b.close(); return html;
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const html = await getHtml(TARGET_URL);
  const items = parse(html);
  process.stdout.write(JSON.stringify({ items, count: items.length }) + '\n');
}
```
Pick Path A or B to match what the original /scrape actually used. Keep the same JSON
shape the user accepted.

## Step 4 — Stage + test (in temp, never in place)
Write the script to `/tmp/skillify-<name>-$$.mjs` and run it:
```bash
node /tmp/skillify-<name>-$$.mjs
```
(For Path B, `npx -y playwright@latest /tmp/skillify-<name>-$$.mjs` so the browser resolves.)
The run passes only if it exits 0 AND prints JSON with `count > 0` and the same shape as
the accepted scrape. If it fails: report what broke, delete the temp file, and stop —
do NOT write anything to `scrapers/`.

## Step 5 — Approval gate
Show the user the staged script and a sample of its output. Ask (AskUserQuestion):
save to `scrapers/<name>.mjs` / rename / discard. Only on an explicit save:

## Step 6 — Commit to disk (atomic)
```bash
mkdir -p scrapers
mv /tmp/skillify-<name>-$$.mjs scrapers/<name>.mjs
```
Append to `scrapers/manifest.json` (create `{"scrapers":[]}` if absent) an entry:
`{ "name": "<name>", "intent": "<intent line>", "url": "<TARGET_URL>", "triggers": ["<paraphrases>"] }`
so a future `/scrape` with a matching intent finds and runs it (Step 3 of /scrape).

## Step 7 — Confirm
Tell the user: `scrapers/<name>.mjs` saved; next time say `/scrape <intent>` or run
`node scrapers/<name>.mjs` directly.

## Honest limits
- A saved scraper breaks when the target page's markup changes — re-run /scrape + /skillify to refresh it.
- It captures the final working logic only; it is not a general crawler.
- Pages with anti-bot defenses or auth are out of scope (so is anything /scrape refused).
