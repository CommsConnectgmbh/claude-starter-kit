#!/usr/bin/env node
// self-heal · fix-agent — turns synthetic findings into fix PRs (or issues).
//
// It reads the latest report from ../synthetic/reports, picks actionable findings,
// and spawns Claude Code headless in the target repo to reproduce + fix + open a PR.
// Free on a Claude subscription via `claude -p` — no API key.
//
// SAFETY (not negotiable — these are the guardrails that make autonomy safe):
//   1. DRY-RUN by default. It only prints the plan + prompt. Real work needs --live.
//   2. Capped per run (SELF_HEAL_MAX, default 1) — no runaway PR storms.
//   3. The agent opens a PR, NEVER merges. Merge stays gated on green tests / a human.
//   4. Sensitive repos (real customers, billing) are ISSUE-ONLY — diagnosis, no code PR.
//   5. Login/test-setup noise and generic resource errors are skipped, not "fixed".
//
//   node fix.mjs            # dry-run: show what it would do
//   node fix.mjs --live     # actually spawn the fixer
//
// Configure your repos in repos.json next to this file (see repos.example.json):
//   { "example-home": { "repo": "/abs/path/to/repo" },
//     "billing":      { "repo": "/abs/path/to/repo", "issueOnly": true } }

import { readdirSync, readFileSync, existsSync } from "node:fs";
import { spawnSync } from "node:child_process";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const __dir = dirname(fileURLToPath(import.meta.url));
const REPORTS = join(__dir, "..", "synthetic", "reports");
const LIVE = process.argv.includes("--live");
const MAX = Number(process.env.SELF_HEAL_MAX || 1);

const reposPath = join(__dir, "repos.json");
if (!existsSync(reposPath)) { console.error("Missing repos.json (copy repos.example.json and fill in paths)."); process.exit(1); }
const REPOS = JSON.parse(readFileSync(reposPath, "utf8"));

// Findings that are environment/test noise rather than app bugs — never auto-fix these.
const SKIP = [/login/i, /credential/i, /timeout exceeded/i, /net::ERR_/i, /favicon/i, /third-party|analytics|tracking/i];

function latestReport() {
  const files = existsSync(REPORTS) ? readdirSync(REPORTS).filter((f) => f.endsWith(".json")).sort() : [];
  if (!files.length) return null;
  return JSON.parse(readFileSync(join(REPORTS, files.at(-1)), "utf8"));
}

function branchExists(repo, branch) {
  return spawnSync("git", ["-C", repo, "rev-parse", "--verify", branch], { encoding: "utf8" }).status === 0;
}

const report = latestReport();
if (!report || !report.findings?.length) { console.log("No findings to act on."); process.exit(0); }

const actionable = report.findings
  .filter((f) => REPOS[f.flow])                              // we know the repo
  .filter((f) => !SKIP.some((re) => re.test(f.detail)))      // not noise
  .slice(0, MAX);

if (!actionable.length) { console.log("Nothing actionable after filtering."); process.exit(0); }

for (const f of actionable) {
  const cfg = REPOS[f.flow];
  const branch = `fix/self-heal-${f.fp.replace(/[^a-z0-9]+/gi, "-").slice(0, 40)}`;
  const issueOnly = !!cfg.issueOnly;

  console.log(`\n— ${f.flow} [${f.kind}] ${issueOnly ? "(issue-only)" : ""}`);
  console.log(`  ${f.detail}`);

  if (!issueOnly && branchExists(cfg.repo, branch)) { console.log("  → branch already exists, skipping (dedupe)."); continue; }

  const task = issueOnly
    ? `A synthetic test found this in "${f.flow}":\n[${f.kind}] ${f.detail}\n\nReproduce and diagnose. Open a GitHub ISSUE with root cause + suggested fix. Do NOT change code — this repo is issue-only.`
    : `A synthetic test found this in "${f.flow}":\n[${f.kind}] ${f.detail}\n\nReproduce it, write the minimal correct fix (no band-aids), run the tests, then open a PR from branch ${branch}. Do NOT merge.`;

  if (!LIVE) { console.log("  DRY-RUN — would spawn:\n    claude -p (in " + cfg.repo + ")\n    " + task.replace(/\n/g, "\n    ")); continue; }

  const res = spawnSync("claude", ["-p", task], { cwd: cfg.repo, stdio: "inherit" });
  console.log(`  claude exited ${res.status}`);
}

console.log(`\nDone (${LIVE ? "live" : "dry-run"}, cap ${MAX}).`);
