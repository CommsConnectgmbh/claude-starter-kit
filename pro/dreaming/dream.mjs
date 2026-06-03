#!/usr/bin/env node
// claude-dreaming — nightly Memory-Curator for Claude Code's auto-memory.
//
// Runs `claude -p` (Max Plan session) over every memory/*.md file, asks for
// a structured review, writes a diff report. The --apply step is separate
// and only touches suggestions with confidence >= 0.85.
//
// Configuration (env vars):
//   MEMORY_DIR        absolute path to your memory folder (required)
//   CLAUDE_BIN        path to the `claude` CLI (default: looks up PATH)
//   APPLY_THRESHOLD   minimum confidence for auto-apply (default: 0.85)
//   LANGUAGE          'en' or 'de' (default: en — controls prompt language)
//
// Find your MEMORY_DIR by checking the auto-memory section of any Claude Code
// system reminder — it lists the absolute path. Typical shapes:
//   ~/.claude/projects/<encoded-cwd>/memory
//
// Usage:
//   MEMORY_DIR=/path/to/memory node dream.mjs                # generate report
//   MEMORY_DIR=/path/to/memory node dream.mjs --apply 2026-01-15  # apply plan
//
// Backups land in $MEMORY_DIR/.dreaming-log/applied/ — nothing is destroyed.

import {
  readdirSync, readFileSync, writeFileSync, mkdirSync,
  statSync, existsSync, unlinkSync,
} from "node:fs";
import { spawnSync } from "node:child_process";
import { join } from "node:path";

const MEMORY_DIR = process.env.MEMORY_DIR;
const CLAUDE_BIN = process.env.CLAUDE_BIN || "claude";
const APPLY_THRESHOLD = Number(process.env.APPLY_THRESHOLD || 0.85);
const LANG = (process.env.LANGUAGE || "en").toLowerCase();

if (!MEMORY_DIR) {
  console.error("MEMORY_DIR env var required. See header for details.");
  process.exit(2);
}
if (!existsSync(MEMORY_DIR)) {
  console.error(`MEMORY_DIR does not exist: ${MEMORY_DIR}`);
  process.exit(2);
}

const LOG_DIR = join(MEMORY_DIR, ".dreaming-log");
const APPLY_DIR = join(LOG_DIR, "applied");
const TODAY = new Date().toISOString().slice(0, 10);
const REPORT_PATH = join(LOG_DIR, `${TODAY}.md`);
const RAW_PATH = join(LOG_DIR, `${TODAY}.raw.json`);

const args = process.argv.slice(2);
const APPLY = args[0] === "--apply" ? (args[1] || TODAY) : null;

mkdirSync(LOG_DIR, { recursive: true });
mkdirSync(APPLY_DIR, { recursive: true });

function loadMemoryFiles() {
  const files = readdirSync(MEMORY_DIR)
    .filter(f => f.endsWith(".md") && !f.startsWith("."))
    .sort();
  return files.map(f => {
    const path = join(MEMORY_DIR, f);
    const st = statSync(path);
    return {
      file: f,
      mtime: st.mtime.toISOString().slice(0, 10),
      size: st.size,
      content: readFileSync(path, "utf8"),
    };
  });
}

function buildPrompt(memories) {
  const bundle = memories.map(m =>
    `===== FILE: ${m.file} (mtime: ${m.mtime}, ${m.size}B) =====\n${m.content.trim()}`
  ).join("\n\n");

  const intro = LANG === "de"
    ? `Du bist "Dreaming" — ein nächtlicher Memory-Curator für Claude Code.\nHeute ist ${TODAY}. Du bekommst ALLE Memory-Files dieses Users.`
    : `You are "Dreaming" — a nightly memory curator for Claude Code's auto-memory.\nToday is ${TODAY}. You receive ALL memory files for this user.`;

  const goals = LANG === "de" ? `
Ziele:
1. **Duplikate finden**: Mehrere Files mit derselben Information → Vorschlag zum Mergen.
2. **Stale Einträge**: Inhalte die offensichtlich überholt sind (alte "AKTIV seit X"-Marker, abgeschlossene Projekte mit "in progress"-Wording).
3. **Index-Drift**: MEMORY.md-Einträge deren Beschreibung nicht mehr zum Datei-Inhalt passt.
4. **Fehlende Index-Einträge**: Memory-Files ohne Eintrag in MEMORY.md.
5. **Wiederkehrende Patterns**: Themen die in 3+ Files auftauchen aber kein dediziertes Memory haben.
6. **Naming-Inkonsistenzen**: gleicher semantischer Typ, unterschiedliche Präfixe (z.B. feedback_x / reference_x).

WICHTIG:
- Sei KONSERVATIV. Bei Zweifel: nichts vorschlagen. Memory ist sensibel, falsche Löschung = Schaden.
- Confidence-Score pro Vorschlag (0.0-1.0). Nur Vorschläge mit confidence >= ${APPLY_THRESHOLD} werden automatisch applied.
- Keine Vorschläge zu sensitiven Feedback-Memories ohne sehr hohe Sicherheit.
` : `
Goals:
1. **Find duplicates**: Multiple files containing the same information → suggest a merge.
2. **Stale entries**: Content clearly outdated (old "ACTIVE since X" markers, completed projects still marked in-progress).
3. **Index drift**: MEMORY.md entries whose description no longer matches the file's content.
4. **Missing index entries**: Memory files without an entry in MEMORY.md.
5. **Recurring patterns**: Themes appearing in 3+ files without a dedicated memory.
6. **Naming inconsistencies**: same semantic type, different prefixes (e.g. feedback_x vs. reference_x).

IMPORTANT:
- Be CONSERVATIVE. When in doubt, suggest nothing. Memory is sensitive — wrong deletion = damage.
- Confidence score per suggestion (0.0-1.0). Only suggestions with confidence >= ${APPLY_THRESHOLD} are auto-applied.
- No suggestions on sensitive feedback memories without very high certainty.
`;

  const schema = `
Output: ONLY a JSON object wrapped in <DREAM_JSON>...</DREAM_JSON> tags.
Schema:
{
  "summary": "1-2 sentence overview",
  "stats": {"files_total": N, "duplicates": N, "stale": N, "index_drift": N, "missing_index": N, "new_patterns": N, "renames": N},
  "duplicates": [{"primary": "file.md", "duplicates": ["a.md","b.md"], "merged_slug": "...", "merged_description": "new 1-liner for MEMORY.md", "merged_content": "complete new body incl. frontmatter", "confidence": 0.9, "reasoning": "..."}],
  "stale": [{"file": "x.md", "action": "delete|update", "new_content": "...", "confidence": 0.9, "reasoning": "..."}],
  "index_drift": [{"file": "x.md", "current_line": "- [x](x.md) — old", "suggested_line": "- [x](x.md) — new", "confidence": 0.9}],
  "missing_index": [{"file": "x.md", "suggested_section": "Reference", "suggested_line": "- [x](x.md) — ...", "confidence": 0.95}],
  "new_patterns": [{"slug": "feedback_xyz", "type": "feedback", "evidence_files": ["a.md","b.md"], "content": "complete body incl. frontmatter", "index_line": "- [feedback_xyz](feedback_xyz.md) — ...", "confidence": 0.8, "reasoning": "..."}],
  "renames": [{"old": "x.md", "new": "y.md", "reason": "...", "confidence": 0.9}]
}

If nothing to do: empty arrays. NO explanation outside the tags.
`;

  return `${intro}\n${goals}${schema}\n===== MEMORY FILES (${memories.length}) =====\n\n${bundle}\n\n===== END =====\n\nEmit the DREAM_JSON now.`;
}

function runClaude(prompt) {
  const env = Object.fromEntries(
    Object.entries(process.env).filter(([k]) => k !== "ANTHROPIC_API_KEY" && k !== "ANTHROPIC_AUTH_TOKEN")
  );
  const result = spawnSync(CLAUDE_BIN, ["-p", "--output-format", "text"], {
    input: prompt,
    env,
    encoding: "utf8",
    maxBuffer: 50 * 1024 * 1024,
    timeout: 30 * 60 * 1000,
  });
  if (result.status !== 0) {
    throw new Error(`claude exited ${result.status}: ${result.stderr || result.stdout}`);
  }
  return result.stdout;
}

function extractJson(raw) {
  const m = raw.match(/<DREAM_JSON>([\s\S]*?)<\/DREAM_JSON>/);
  if (!m) throw new Error("No DREAM_JSON block found in output");
  return JSON.parse(m[1].trim());
}

function buildReport(plan, memories) {
  const s = plan.stats || {};
  const lines = [];
  lines.push(`# Dreaming Report ${TODAY}`);
  lines.push("");
  lines.push(`**Summary:** ${plan.summary || "(none)"}`);
  lines.push("");
  lines.push(`**Stats:** ${memories.length} files scanned · ${s.duplicates || 0} dup · ${s.stale || 0} stale · ${s.index_drift || 0} drift · ${s.missing_index || 0} missing-idx · ${s.new_patterns || 0} new-pattern · ${s.renames || 0} rename`);
  lines.push("");

  const section = (title, items, render) => {
    if (!items || !items.length) return;
    lines.push(`## ${title}`);
    lines.push("");
    items.forEach((it, i) => {
      lines.push(`### ${i + 1}. (confidence ${it.confidence ?? "?"})`);
      lines.push(render(it));
      lines.push("");
    });
  };

  section("Duplicates", plan.duplicates, d =>
    `- Primary: \`${d.primary}\`\n- With: ${(d.duplicates || []).map(x => `\`${x}\``).join(", ")}\n- New slug: \`${d.merged_slug}\`\n- Reasoning: ${d.reasoning || "-"}\n\n<details><summary>Merged content</summary>\n\n\`\`\`\n${d.merged_content || ""}\n\`\`\`\n</details>`
  );
  section("Stale", plan.stale, st =>
    `- File: \`${st.file}\`\n- Action: **${st.action}**\n- Reasoning: ${st.reasoning || "-"}` + (st.new_content ? `\n\n<details><summary>New content</summary>\n\n\`\`\`\n${st.new_content}\n\`\`\`\n</details>` : "")
  );
  section("Index Drift", plan.index_drift, d =>
    `- File: \`${d.file}\`\n- Current: \`${d.current_line}\`\n- Suggested: \`${d.suggested_line}\``
  );
  section("Missing Index", plan.missing_index, m =>
    `- File: \`${m.file}\` → Section **${m.suggested_section}**\n- Line: \`${m.suggested_line}\``
  );
  section("New Pattern Suggestions", plan.new_patterns, n =>
    `- Slug: \`${n.slug}\` (type: ${n.type})\n- Evidence: ${(n.evidence_files || []).map(x => `\`${x}\``).join(", ")}\n- Reasoning: ${n.reasoning || "-"}\n\n<details><summary>Body</summary>\n\n\`\`\`\n${n.content || ""}\n\`\`\`\n</details>`
  );
  section("Renames", plan.renames, r =>
    `- \`${r.old}\` → \`${r.new}\`\n- Reason: ${r.reason || "-"}`
  );

  lines.push("---");
  lines.push("");
  lines.push("## Apply");
  lines.push("");
  lines.push(`Suggestions with confidence >= ${APPLY_THRESHOLD} can be auto-applied:`);
  lines.push("");
  lines.push("```");
  lines.push(`MEMORY_DIR=${MEMORY_DIR} node dream.mjs --apply ${TODAY}`);
  lines.push("```");
  lines.push("");
  lines.push(`Lower-confidence suggestions (< ${APPLY_THRESHOLD}) stay untouched and need manual review.`);
  return lines.join("\n");
}

function backupFile(filename) {
  const src = join(MEMORY_DIR, filename);
  if (!existsSync(src)) return;
  const dst = join(APPLY_DIR, `${TODAY}__${filename}`);
  writeFileSync(dst, readFileSync(src));
}

function updateIndex(updates) {
  const indexPath = join(MEMORY_DIR, "MEMORY.md");
  if (!existsSync(indexPath)) return;
  let idx = readFileSync(indexPath, "utf8");
  for (const u of updates) {
    if (u.kind === "replace") {
      idx = idx.replace(u.from, u.to);
    } else if (u.kind === "append-section") {
      const re = new RegExp(`(## ${u.section}\\n[\\s\\S]*?)(\\n\\n## |\\n*$)`);
      idx = idx.replace(re, (_, body, tail) => `${body}\n${u.line}${tail}`);
    } else if (u.kind === "remove") {
      idx = idx.split("\n").filter(l => !l.includes(u.contains)).join("\n");
    }
  }
  writeFileSync(indexPath, idx);
}

function applyPlan(date) {
  const planPath = join(LOG_DIR, `${date}.raw.json`);
  if (!existsSync(planPath)) {
    console.error(`No plan found at ${planPath}`);
    process.exit(2);
  }
  const plan = JSON.parse(readFileSync(planPath, "utf8"));
  const indexUpdates = [];
  const applied = { dedup: [], stale: [], drift: [], missing: [], skipped: [] };

  for (const d of plan.duplicates || []) {
    if ((d.confidence || 0) < APPLY_THRESHOLD) { applied.skipped.push(`dup ${d.primary}`); continue; }
    const newFile = `${d.merged_slug}.md`;
    backupFile(d.primary);
    (d.duplicates || []).forEach(backupFile);
    writeFileSync(join(MEMORY_DIR, newFile), d.merged_content);
    if (newFile !== d.primary && existsSync(join(MEMORY_DIR, d.primary))) {
      unlinkSync(join(MEMORY_DIR, d.primary));
    }
    (d.duplicates || []).forEach(f => {
      const p = join(MEMORY_DIR, f);
      if (existsSync(p) && f !== newFile) unlinkSync(p);
      indexUpdates.push({ kind: "remove", contains: `(${f})` });
    });
    indexUpdates.push({ kind: "remove", contains: `(${d.primary})` });
    applied.dedup.push(`${d.primary} ← ${(d.duplicates || []).join(",")} → ${newFile}`);
  }

  for (const s of plan.stale || []) {
    if ((s.confidence || 0) < APPLY_THRESHOLD) { applied.skipped.push(`stale ${s.file}`); continue; }
    backupFile(s.file);
    if (s.action === "delete") {
      const p = join(MEMORY_DIR, s.file);
      if (existsSync(p)) unlinkSync(p);
      indexUpdates.push({ kind: "remove", contains: `(${s.file})` });
    } else if (s.action === "update" && s.new_content) {
      writeFileSync(join(MEMORY_DIR, s.file), s.new_content);
    }
    applied.stale.push(`${s.file} (${s.action})`);
  }

  for (const d of plan.index_drift || []) {
    if ((d.confidence || 0) < APPLY_THRESHOLD) { applied.skipped.push(`drift ${d.file}`); continue; }
    indexUpdates.push({ kind: "replace", from: d.current_line, to: d.suggested_line });
    applied.drift.push(d.file);
  }

  for (const m of plan.missing_index || []) {
    if ((m.confidence || 0) < APPLY_THRESHOLD) { applied.skipped.push(`missing ${m.file}`); continue; }
    indexUpdates.push({ kind: "append-section", section: m.suggested_section, line: m.suggested_line });
    applied.missing.push(m.file);
  }

  // new_patterns and renames stay manual — too risky to auto-apply.
  (plan.new_patterns || []).forEach(n => applied.skipped.push(`new ${n.slug} (manual review)`));
  (plan.renames || []).forEach(r => applied.skipped.push(`rename ${r.old}→${r.new} (manual review)`));

  if (indexUpdates.length) {
    backupFile("MEMORY.md");
    updateIndex(indexUpdates);
  }

  const summaryPath = join(LOG_DIR, `${date}.applied.md`);
  const out = [
    `# Dreaming Applied ${date} (run at ${new Date().toISOString()})`,
    "",
    `Dedup: ${applied.dedup.length} · Stale: ${applied.stale.length} · Drift: ${applied.drift.length} · Missing-idx: ${applied.missing.length} · Skipped: ${applied.skipped.length}`,
    "",
    "## Applied",
    ...["dedup", "stale", "drift", "missing"].flatMap(k => applied[k].map(x => `- ${k}: ${x}`)),
    "",
    "## Skipped (manual review required)",
    ...applied.skipped.map(x => `- ${x}`),
    "",
    `Backups: \`${APPLY_DIR}\``,
  ].join("\n");
  writeFileSync(summaryPath, out);
  console.log(out);
}

// --- main ---
if (APPLY) {
  applyPlan(APPLY);
  process.exit(0);
}

console.log(`[dreaming] Loading memory files from ${MEMORY_DIR}...`);
const memories = loadMemoryFiles();
if (!memories.length) {
  console.log("[dreaming] No memory files found. Nothing to curate.");
  process.exit(0);
}
console.log(`[dreaming] Loaded ${memories.length} files. Building prompt...`);
const prompt = buildPrompt(memories);
console.log(`[dreaming] Prompt size: ${(prompt.length / 1024).toFixed(1)} KB. Calling claude -p...`);
const t0 = Date.now();
const raw = runClaude(prompt);
console.log(`[dreaming] Claude returned in ${((Date.now() - t0) / 1000).toFixed(1)}s. Parsing...`);
writeFileSync(RAW_PATH.replace(".raw.json", ".raw.txt"), raw);
let plan;
try {
  plan = extractJson(raw);
} catch (e) {
  console.error(`[dreaming] Parse failed: ${e.message}`);
  console.error(`[dreaming] Raw output saved at ${RAW_PATH.replace(".raw.json", ".raw.txt")}`);
  process.exit(3);
}
writeFileSync(RAW_PATH, JSON.stringify(plan, null, 2));
const report = buildReport(plan, memories);
writeFileSync(REPORT_PATH, report);
console.log(`[dreaming] Report written: ${REPORT_PATH}`);
console.log(`[dreaming] Apply via: MEMORY_DIR=${MEMORY_DIR} node ${import.meta.url.replace("file://", "")} --apply ${TODAY}`);
