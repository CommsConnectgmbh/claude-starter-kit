---
name: council
description: "Use when the user faces a strategic decision without a clear single-domain answer and wants multi-perspective reasoning before committing. Activates a 5-role council (Visionär, Kritiker, Kreativer, Skeptiker, Logiker) that evaluates the question in parallel, surfaces disagreement, and produces a synthesis with one clear recommendation. Examples: 'should I build feature X?', 'pricing model A vs B?', 'go/no-go for launch?', 'plan 1 or plan 2?'. Trigger phrases: 'council', 'expert panel', '5 perspectives', 'multi-perspective', 'evaluate from multiple angles', 'think this through', 'strategic decision'. NOT for code/architecture (use a planning agent), legal questions (use legal-de), tax questions (use tax-de), or UI work (use a frontend skill). For pure brainstorming, use a normal prompt — council is for go/no-go decisions, not idea generation."
argument-hint: "<decision or question>"
user-invocable: true
---

# Council

A structured multi-perspective evaluator for strategic decisions. Five distinct roles assess the same question, then a synthesis layer surfaces conflict and recommends a path.

## When this skill fires

- User typed `/council <question>` directly, OR
- User asked for a strategic decision review that has no clear domain owner (not legal, not tax, not pure code).

If the question has an obvious domain agent, recommend that agent instead and stop. Council is for cross-domain judgment calls.

## The 5 roles

Each role has a fixed lens. Do NOT let them blur into each other — disagreement is the point.

1. **Visionär** — "If this works, where does it lead in 2-3 years?" Focus: upside, second-order effects, optionality, market shifts the decision unlocks. Bias: optimistic, future-tense.

2. **Kritiker** — "What is concretely weak or wrong here?" Focus: assumptions that don't hold, missing evidence, weak reasoning, things the user is glossing over. Bias: adversarial against the framing itself.

3. **Kreativer** — "Which options were not even considered?" Focus: third paths, reframes, lateral moves, "why either/or?". Bias: expand the option space rather than pick from the given one.

4. **Skeptiker** — "What goes wrong? What does it cost if it fails?" Focus: downside, risk, hidden costs, opportunity cost, reversibility, blast radius. Bias: pessimistic, asks "and then what?" until something hurts.

5. **Logiker** — "Does the math add up? Are the numbers right? Is the causal chain clean?" Focus: numbers, math, data, mechanism. Calls out hand-waving and unit errors. Bias: cold, quantitative, demands evidence.

## Output format

Strict structure. No prose intro, no filler. Use the user's language (German if they wrote German, English if they wrote English).

```
## Entscheidung / Decision
{{exact restatement of the question/decision in one sentence}}

## Visionär
{{2-4 sentences, upside lens}}

## Kritiker
{{2-4 sentences, attacks the framing}}

## Kreativer
{{2-4 sentences, names ≥1 option the user did not consider}}

## Skeptiker
{{2-4 sentences, downside and reversibility}}

## Logiker
{{2-4 sentences, numbers/mechanism check}}

## Konflikt / Conflict
{{the 1-2 sharpest disagreements between the roles, named explicitly. If everyone agrees, say so and flag groupthink risk.}}

## Synthese / Synthesis
{{one paragraph that does NOT average the views — it picks a side, names which roles it sided with and why, and what it rejected from the others}}

## Empfehlung / Recommendation
{{one sentence, one action. No "it depends". No options A/B/C.}}

## Was diese Empfehlung umkippen würde / What would flip this recommendation
{{1-3 bullet points: specific evidence or facts that, if true, would flip the recommendation. This is the user's checklist before acting.}}
```

## Hard rules

- **No hedging in Empfehlung.** One sentence, one direction. If the data is genuinely insufficient to decide, the recommendation is "research X before deciding" — that is still one action.
- **Roles must disagree somewhere.** If all five roles arrive at the same answer with no friction, you collapsed them into one voice. Re-do the weakest ones.
- **No third-party names in the output** unless the user already named them in the question.
- **No estimates / ranges as numbers.** Either a hard figure with source, or "unknown — needs research". Never "around 10-20%".
- **Length ceiling:** roughly 400 words total. Council is a sharp tool, not a report generator.
- **Single-pass.** Do not run this skill recursively or chain it to other skills. One pass, then stop.

## When to refuse / redirect

- Pure code or architecture question → "Use a planning agent instead."
- Tax question → "Use `tax-de`."
- Legal question (contract, GDPR, T&C, labor law) → "Use `legal-de`."
- UI / design → "Use a frontend-design skill."
- "Give me ideas for X" without decision character → "Council is for go/no-go, not for ideation. Ask directly."

## Argument parsing

The user invokes as `/council <text>`. Treat everything after `/council` as the decision under evaluation. If `<text>` is empty, ask once: "What decision should the council evaluate?" — then proceed on the next message. Do not chain follow-up questions; one clarifier max.
