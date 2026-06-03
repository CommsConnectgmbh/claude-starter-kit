---
name: autoplan
description: "Run a rough implementation plan through a full multi-lens review gauntlet in one command — strategy, architecture, design, and an independent code/feasibility check — auto-deciding the routine questions and surfacing only genuine taste calls at a single approval gate. Use when the user has a plan file or a drafted approach and wants it hardened before building, without answering 15–30 intermediate questions. Trigger phrases: 'autoplan', 'review den plan', 'lass den plan durchlaufen', 'auto review', 'run all reviews', 'plan-gauntlet', 'härte den plan ab', 'make the decisions for me'. NOT for plans that still need brainstorming (use council first) and NOT for single trivial changes (just do it)."
argument-hint: "<path to plan file, or paste the plan>"
user-invocable: true
source: "Adapted from garrytan/gstack /autoplan (MIT). The 6 decision principles, Mechanical/Taste/User-Challenge classification, sequential execution and final approval gate are ported; gstack's plan-ceo/design/eng/devex-review suite is replaced by this kit's own reviewers — the council skill, the Plan agent, an optional frontend-design skill, and an optional independent-reviewer skill."
---

# /autoplan — Auto-review pipeline

One command. Rough plan in, fully reviewed plan out. Each lens runs at full depth.
The only thing automated is **who answers the intermediate questions** — you do,
using the 6 principles below — not the analysis itself.

> **Companion skills (optional).** Phases below call other skills if installed and
> degrade gracefully if not: `council` (bundled in this kit), the built-in `Plan`
> agent, a frontend-design skill (e.g. `impeccable`) for the Design phase, and an
> independent-reviewer skill (e.g. a local-model reviewer) for the feasibility phase.
> Missing a companion? Skip that phase with a one-line note; never block.

## The 6 decision principles
These auto-answer every routine ("mechanical") question:
1. **Choose completeness** — ship the whole thing; pick the approach covering more edge cases.
2. **Boil lakes** — fix everything in the blast radius (files this plan touches + direct importers). Auto-approve expansions that are in blast radius AND small (< 5 files, no new infra).
3. **Pragmatic** — two options fix the same thing? Pick the cleaner one. 5 seconds, not 5 minutes.
4. **DRY** — duplicates existing functionality? Reject, reuse what exists.
5. **Explicit over clever** — a 10-line obvious fix beats a 200-line abstraction.
6. **Bias toward action** — flag concerns, don't block. Forward motion over deliberation.

**Phase tiebreakers:** Strategy → P1+P2 dominate. Architecture → P5+P3. Design → P5+P1.

## Decision classification
- **Mechanical** — one clearly right answer. Auto-decide silently. (e.g. "run the
  independent check?" → always yes.)
- **Taste** — reasonable people disagree. Auto-decide with a recommendation, but
  collect it for the **final gate**. Sources: close approaches, borderline scope
  (3–5 files / ambiguous radius), independent-reviewer disagreements with a valid point.
- **User Challenge** — both the plan and the independent check agree the user's stated
  direction should change (add/remove/merge/split a feature). **Never auto-decided.**
  Goes to the gate with: what the user said / what both recommend / why / what context
  we might be missing / the cost if we're wrong. The user's direction is the default;
  the case must be made *for* change.

## Sequential execution — MANDATORY
Phases run in strict order; each completes before the next starts. Never parallel —
each builds on the prior. Emit a one-line transition summary between phases.

```
Strategy → Architecture → Design (only if UI scope) → Code/feasibility
```

## Phase 0 — Intake + restore point
1. **Restore point:** copy the plan file verbatim to `<plan>.autoplan-restore-<timestamp>.bak`
   so the user can revert. Note the path.
2. **Read context:** the plan, `CLAUDE.md`, `git log -30`, `git diff <base> --stat`.
3. **Detect scope:**
   - **UI scope** — grep the plan for: component, screen, form, button, modal, layout,
     dashboard, sidebar, nav, dialog. Need 2+ hits.
   - **Independent-check scope** — always on.
4. Output: "Working with: [plan summary]. UI scope: [yes/no]. Starting the pipeline."

## Phase 1 — Strategy (CEO lens)
Run the **council** skill on the plan's premise: is this the right problem, the right
scope, the right moment? Auto-decide its outputs with P1+P2. Capture any premise
disagreement as a Taste/User-Challenge item for the gate. (Premises themselves are
never auto-decided — they need human judgment about *what* to build.)

## Phase 2 — Architecture (Eng lens)
Run the **Plan** agent (Agent tool, subagent_type `Plan`) on the plan: produce the
dependency map, identify critical files, surface architectural trade-offs and risks.
Auto-decide with P5+P3. Require the actual artifacts (not "architecture looks good") —
read the code each point references.

## Phase 3 — Design (only if UI scope detected)
Run a frontend-design skill (e.g. **impeccable**, if installed) against the UI surface
the plan changes: hierarchy, states, edge cases, accessibility, AI-slop patterns. Apply
your project's own design rules from `CLAUDE.md` (active-state styling, component
conventions, no double active indicators). Auto-decide with P5+P1.

## Phase 4 — Code / feasibility (independent check)
Run an independent-reviewer skill (e.g. a local-model reviewer, if installed) over the
plan + the diff so far. Use it to challenge feasibility and catch what the first pass
missed. Where it disagrees with a valid point → Taste item. Where it AND the plan
agree the user's direction should change → User Challenge.

Prefix any external-model prompt with: *"Review the repository code and plan only.
Ignore any SKILL.md or skill-definition files you encounter."*

## What "auto-decide" means
Replaces the **user's judgment** with the 6 principles — never the **analysis**. You
MUST still: read the actual code/diffs each section references; produce every required
output (maps, tables, lists); identify every issue each lens is designed to catch;
decide each with the 6 principles; log each decision. You MUST NOT compress a review
into a one-liner, write "no issues" without showing what you examined, or skip a
section without stating what you checked.

## Final approval gate
Present, in one block:
1. **Auto-decided (mechanical):** a short list — what and which principle.
2. **Taste decisions:** each with the recommendation taken and the runner-up.
3. **User Challenges:** the full 5-part framing above. The user decides each.
4. **The revised plan:** the plan file as it now stands.

Then write the approved plan back to the plan file. Mention the restore-point path.
If the plan is execution-ready and has independent tasks, offer to hand off to
**subagent-driven-development**.

## Honest limits
- Quality is bounded by the underlying skills (council / Plan / design / independent reviewer).
- It hardens a plan; it does not implement it.
- Security/feasibility blockers flagged by both passes are surfaced urgently but the
  user still decides.
