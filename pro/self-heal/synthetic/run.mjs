#!/usr/bin/env node
// self-heal · synthetic user — drives your app's main flows with a headless browser,
// captures what breaks, and writes a report the fix-agent can act on.
//
// The point: error monitoring (Sentry et al.) only catches what *real* users trigger.
// Pre-revenue, with little or no traffic, that surface is empty. A synthetic user clicks
// the happy paths every night so bugs surface with zero real users.
//
// Setup (one time, from pro/self-heal):
//   npm install                       # pulls in playwright (see package.json)
//   npx playwright install chromium   # browser binary
//
// Run:
//   node synthetic/run.mjs            # run every flow in ./flows
//   node synthetic/run.mjs smoke      # run only flows/smoke.mjs
//
// A flow file exports: export default { name, url, run: async (page) => { ... } }
// `run` does the clicking; this harness handles browser setup, error capture, reporting.

import { readdirSync, mkdirSync, writeFileSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { chromium } from "playwright";

const __dir = dirname(fileURLToPath(import.meta.url));
const FLOW_DIR = join(__dir, "flows");
const REPORT_DIR = join(__dir, "reports");
const only = process.argv[2]; // optional flow name filter

// Stable fingerprint so the same bug across runs dedupes to one finding.
function fingerprint(flow, kind, detail) {
  const norm = String(detail)
    .replace(/https?:\/\/[^\s"')]+/g, "<url>")    // strip volatile URLs
    .replace(/0x[0-9a-f]+|\b\d{3,}\b/gi, "<n>")   // strip ids/numbers
    .slice(0, 160);
  return `${flow}::${kind}::${norm}`;
}

function attach(page, flow, findings) {
  const push = (kind, detail) =>
    findings.push({ flow, kind, detail: String(detail).slice(0, 500), fp: fingerprint(flow, kind, detail) });

  page.on("console", (m) => { if (m.type() === "error") push("console-error", m.text()); });
  page.on("pageerror", (e) => push("page-error", e.message || e));
  page.on("requestfailed", (r) => push("request-failed", `${r.method()} ${r.url()} — ${r.failure()?.errorText}`));
  page.on("response", (r) => { if (r.status() >= 500) push("http-5xx", `${r.status()} ${r.url()}`); });
}

async function main() {
  mkdirSync(REPORT_DIR, { recursive: true });
  const flowFiles = readdirSync(FLOW_DIR)
    .filter((f) => f.endsWith(".mjs") && !f.startsWith("_"))
    .filter((f) => !only || f === `${only}.mjs`);

  if (!flowFiles.length) { console.error("No flow files in ./flows"); process.exit(1); }

  const browser = await chromium.launch();
  const findings = [];
  const ran = [];

  for (const file of flowFiles) {
    const flow = (await import(join(FLOW_DIR, file))).default;
    const name = flow.name || file.replace(/\.mjs$/, "");
    const ctx = await browser.newContext();
    const page = await ctx.newPage();
    attach(page, name, findings);
    process.stdout.write(`▸ ${name} … `);
    try {
      if (flow.url) await page.goto(flow.url, { waitUntil: "domcontentloaded", timeout: 30000 });
      if (flow.run) await flow.run(page);
      console.log("done");
      ran.push(name);
    } catch (e) {
      findings.push({ flow: name, kind: "step-failed", detail: String(e.message || e).slice(0, 500), fp: fingerprint(name, "step-failed", e.message || e) });
      console.log("step-failed");
    }
    await ctx.close();
  }
  await browser.close();

  // dedupe by fingerprint, count occurrences
  const byFp = new Map();
  for (const f of findings) {
    const prev = byFp.get(f.fp);
    if (prev) prev.count++;
    else byFp.set(f.fp, { ...f, count: 1 });
  }
  const unique = [...byFp.values()];

  const stamp = new Date().toISOString().replace(/[:.]/g, "-");
  const json = { stamp, ranFlows: ran, findingCount: unique.length, findings: unique };
  writeFileSync(join(REPORT_DIR, `${stamp}.json`), JSON.stringify(json, null, 2));

  const md = [
    `# self-heal report — ${stamp}`,
    ``,
    `Flows run: ${ran.join(", ") || "none"}`,
    `Unique findings: ${unique.length}`,
    ``,
    ...unique.map((f) => `- **[${f.kind}]** \`${f.flow}\` ×${f.count}\n  ${f.detail}`),
    unique.length ? "" : "_Clean — nothing broke._",
  ].join("\n");
  writeFileSync(join(REPORT_DIR, `${stamp}.md`), md);

  console.log(`\n${unique.length} unique finding(s) → reports/${stamp}.md`);
  process.exit(0);
}

main().catch((e) => { console.error(e); process.exit(1); });
