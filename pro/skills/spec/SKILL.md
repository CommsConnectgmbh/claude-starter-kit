---
name: spec
description: "Turn vague intent into a precise, executable spec before any code is written. Five strict phases: understand the why → lock scope → interrogate the code → draft review → file the spec (optionally spawn an implementing agent). Use when the user has a fuzzy feature/bug/refactor idea and wants it pinned down so an unfamiliar implementer (or a fresh subagent) could execute it without guessing. Trigger phrases: 'spec', 'schreib eine spec', 'mach ein ticket draus', 'spezifizier das', 'turn this into a spec', 'pin this down', 'executable spec', 'sauberes ticket'. NOT for work that's already well-defined (just do it), and NOT for pure brainstorming (use council first). Pairs with subagent-driven-development for execution."
argument-hint: "<rough intent> [--execute] [--no-gate]"
user-invocable: true
source: "Reimplemented from garrytan/gstack /spec (MIT). Methodology ported; gstack daemon/telemetry/redaction-engine stripped; the quality gate routes to an optional independent-reviewer skill (e.g. a local-model reviewer) and degrades gracefully when none is installed."
---

# /spec — Vague intent → executable spec

One command. Fuzzy idea in, a spec an unfamiliar implementer could execute out.

The value moment: the user sees you grounded in their **actual code**, not a generic
checklist. Read first, ask second.

> **Companion skills (optional).** The Phase 4.5 quality gate calls an
> independent-reviewer skill if installed and skips gracefully if not. `--execute`
> can hand off to `subagent-driven-development`.

## Flags (parse from the invocation)

| Flag | Default | Effect |
|------|---------|--------|
| `--execute` | OFF | After filing the spec, spawn a fresh subagent (Agent tool) to implement it. |
| `--no-gate` | gate ON | Skip the independent-reviewer quality gate between Phase 4 and Phase 5. |
| `--audit` | OFF | Route Phase 5 to the audit/cleanup template instead of the standard one. |
| `--file <path>` | inferred | Write the spec to this path instead of the default `specs/` location. |

Echo the parsed flags back at the start of Phase 1.

## Process (STRICT — never skip or combine phases)

### Phase 1 — Understand the "Why"
Ask until you can crisply answer all five (skip the ones obvious for a solo dev):
1. **Who** is affected? (end user role, internal team, automated system)
2. **What** is the current behavior — verified, not assumed?
3. **What** should it be instead?
4. **Why now?** (blocks other work / costs money / correctness / compliance)
5. **How will we know it's done?** — observable, measurable, not vibes.

Do not proceed until all five are answered without hand-waving.

### Phase 2 — Scope and Boundaries
Ask until you can answer:
1. **What is explicitly out of scope?** Lock this early — kills creep later.
2. **What existing systems does this touch?** Files, tables, endpoints, services.
3. **Ordering constraints?** Must A happen before B?
4. **Smallest version that delivers the value?** Always find the MVP cut.
5. **Failure modes + rollback?** What breaks if shipped wrong?

Do not proceed until scope is locked.

### Phase 3 — Technical Interrogation (HARD requirement: read code first)
**Mandatory:** before asking ANY Phase 3 question, read at least one piece of
real evidence via Grep/Glob/Read. Do not ask "what file should I look at?" — find
it yourself and cite `path:line` in your first question.

- **Concrete file/symbol named:** Grep the symbol, Read the file, cite the line.
- **Project-level prompt** ("rethink auth"): Read `package.json`/`go.mod`, the
  relevant top-level dir, existing `docs/<topic>.md`. Cite what you found, then ask.
- **Truly greenfield:** say so explicitly ("searched X/Y/Z, found nothing — treating
  as greenfield") and proceed.

Then ask only about categories that apply (skip the rest): data model, API,
background processing, UI, infrastructure/secrets/cost, testing/regression risk.
Don't ask what the code already answers.

### Phase 4 — Draft Review
Present the full draft spec and ask: **"Does this accurately capture what you want?
What did I get wrong?"** Iterate until confirmed.

### Phase 4.5 — Quality Gate (`--no-gate` to skip)
After the user confirms, run an independent-reviewer skill on the draft (if installed).
Ask it to score the spec 0–10 for "executability by an unfamiliar implementer" and
list specific ambiguities (missing acceptance criteria, fuzzy metrics, unnamed files).
- **Score ≥ 7:** pass, print `Quality gate: N/10 ✓`, continue.
- **Score < 7:** surface the ambiguities, offer to address and re-score (max 3 rounds).
  After 3 rounds still < 7, ask: ship anyway / save draft and stop / one more round.
- **Reviewer unavailable:** print one line ("gate skipped — no reviewer installed")
  and continue. Never block on gate failure.

Before any spec leaves this session, apply your project's standing rules from
`CLAUDE.md` (e.g. no customer names in the spec body — anonymize to a role or
"Customer A"; no internal jargon in anything user-facing).

### Phase 5 — File the Spec (`--execute` to also implement)
Write the final spec using the structure below.

```markdown
# <Title — imperative, specific>

## Why
<the answer to Phase 1, 2–4 sentences>

## Scope
**In:** …
**Out:** …

## Current behavior
<verified, with path:line references>

## Target behavior
<what should happen>

## Implementation notes
<files to touch, data model, API, ordering constraints — grounded in Phase 3>

## Acceptance criteria
- [ ] <observable, testable outcome>
- [ ] …

## Risks & rollback
<failure modes, how to revert>
```

Default location: `specs/<YYYY-MM-DD>-<slug>.md` in the repo (create `specs/` if
absent). If a GitHub remote exists and the user wants a tracked ticket, offer
`gh issue create` with this body.

**With `--execute`:** spawn a fresh subagent via the Agent tool with the spec as its
brief, then hand off to **subagent-driven-development** if the spec has multiple
independent tasks. Without `--execute`: stop after filing and tell the user the path.

## Honest limits
- The gate is reviewer judgment, not a guarantee — it catches ambiguity, not every bug.
- This skill produces a spec; it does not implement unless `--execute` is passed.
