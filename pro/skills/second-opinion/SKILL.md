---
name: second-opinion
description: >-
  Get a free SECOND OPINION on code from a local coding model (Ollama, default
  qwen2.5-coder) as an adversarial counter-review to Claude-written code, to
  catch bugs/security/edge-cases the first model missed. Use this when the user
  wants a second opinion, a counter-check, an adversarial review, or before
  code is committed/merged. Trigger phrases: "second opinion", "counter check",
  "review the diff locally", "have ollama look at it", "before I merge",
  "is this code OK?", "adversarial review". Uses OpenAI Codex when logged in,
  otherwise a free local model (Ollama) — a foreign model catches different bugs.
---

# Second Opinion (code reviewer, different model)

Get a **second opinion** from a **different** model — a foreign model catches
different mistakes than the one that wrote the code.

**Two backends, chosen automatically:**
- **Codex** (OpenAI, paid subscription) — when `codex` is installed *and* logged
  in (`codex login`). Preferred.
- **Ollama** `qwen2.5-coder` (local, free) — fallback when there is no Codex login.

Force with `SECOND_OPINION_BACKEND=codex|ollama`.
Override the Codex model with `SECOND_OPINION_CODEX_MODEL=<name>`.

## When to use

- Before `git commit` / before merging a PR.
- When the user says "second opinion", "counter-check", "review locally", "have ollama check this".
- After any non-trivial self-written change as a sanity check.

## Prerequisite

Either one is enough:
- **Codex:** `npm i -g @openai/codex` and a one-time `codex login`
  (ChatGPT subscription or API key).
- **Ollama:** running locally (`http://localhost:11434`) with a coder model.
  Install once: `ollama pull qwen2.5-coder:14b-instruct`.

A smaller Ollama model (7b) works too and is much faster on modest hardware —
just expect more noise to triage. Codex is stronger but sends the diff to
OpenAI; Ollama stays fully local and free.

## Usage

```bash
# uncommitted changes (default)
python3 ~/.claude/skills/second-opinion/review.py

# staged changes only
python3 ~/.claude/skills/second-opinion/review.py --staged

# commit range (e.g. PR branch vs main)
python3 ~/.claude/skills/second-opinion/review.py --range main..HEAD

# specific files (whole content, even without git)
python3 ~/.claude/skills/second-opinion/review.py src/auth.ts src/db.ts

# diff from stdin
git diff | python3 ~/.claude/skills/second-opinion/review.py --raw
```

## Workflow (how Claude should use it)

1. Run the script on the relevant diff (`--staged` before commit, `--range` before merge).
2. **Triage the findings** — the local model is weaker than Claude/Opus, so
   don't accept findings blindly: check each one against the actual code.
3. Fix real bugs / security / edge cases, discard hallucinations.
4. Report back briefly: what was confirmed, what was discarded, what was fixed.

## Notes

- Model override: `SECOND_OPINION_MODEL=...` or `--model <name>`.
- Remote Ollama: `OLLAMA_HOST=http://...:11434`.
- Large diffs are truncated around 60k chars — for monster diffs, review per
  directory/file instead.
- This is a **helper** reviewer, not a gatekeeper: the final call is Claude's.
