# Skills vs Agents

These two get confused constantly. The difference matters because it changes how Claude finds and uses them.

## Skills

A **skill** is a self-contained instruction bundle for Claude to follow. It lives at `~/.claude/skills/<name>/SKILL.md`.

When a skill matches the current request, Claude loads its contents and follows them as part of the current conversation — same context, same model, same tools.

Skills are good for:
- **Repeatable workflows.** "When I ask for a council review, always produce these 5 perspectives in this exact format."
- **Quality gates.** "Before declaring a UI change done, run through this checklist."
- **Methodology.** "When I'm stuck, walk through this dispatch table to pick the right technique."

Example: `skills/council/SKILL.md` in this repo. It's a decision-making framework — same Claude, same tools, but with a specific output structure.

## Agents

An **agent** is a separate sub-Claude with its own system prompt, its own tool allowlist, and its own context window. It lives at `~/.claude/agents/<name>.md`.

When a request matches an agent's description, the main Claude can delegate to it. The agent runs in isolation — fresh context, no memory of the main conversation except what's in the dispatch prompt — and returns a single summary.

Agents are good for:
- **Domain expertise.** "When the user asks about German tax law, hand off to a tax-specialist with strict source-citation rules."
- **Heavy research.** Don't pollute the main context with 30 search results — let an agent do the digging and report back.
- **Different tool needs.** An agent might need `WebFetch` for legal databases but no shell access.

Example: `agents/legal-de.md` in this repo. Mandatory disclaimer, mandatory source citation, no code-writing — totally different posture from main Claude.

## How to choose

| Question | Answer |
|---|---|
| Does the work need a totally different system prompt? | **Agent** |
| Do you want a fresh context window (no pollution)? | **Agent** |
| Is it a workflow Claude should fold into the current turn? | **Skill** |
| Is it triggered by a slash command the user types? | **Skill** (with `user-invocable: true`) |
| Does it produce one final report, then exit? | **Agent** |
| Does it run inline and you see each step? | **Skill** |

## Frontmatter cheat sheet

**Skill:**
```yaml
---
name: my-skill
description: When to fire this skill (specific trigger phrases help Claude pick it)
user-invocable: true              # optional, lets user type /my-skill
argument-hint: "<input>"          # optional, shown in / autocomplete
---
```

**Agent:**
```yaml
---
name: my-agent
description: When to delegate to this agent (be specific — Claude uses this to choose)
model: sonnet                     # or opus, haiku
tools: Read, Write, Edit, Bash, WebFetch, Grep, Glob, TodoWrite
---
```

The `description` field is the most important thing in both. Claude reads only the description (not the body) when deciding whether to invoke. A vague description means the skill/agent will be skipped even when it would have been perfect.

Write descriptions like trigger documentation: include example phrases, list non-obvious negative cases ("NOT for X"), and front-load the strongest signals.

## When you don't need either

Sometimes the right answer is just a CLAUDE.md rule, or a one-time instruction you give per-conversation. Don't create a skill for something you do twice a year — the maintenance cost (broken when you change tools, drifts out of date) exceeds the savings.

## Installing skills from someone else's collection

Large public skill collections exist — some with several hundred entries in a single
repository, often installable with one command. Resist that command.

Claude picks a skill by reading **every** description before deciding. Descriptions are the
one part of a skill that is always in context. Install 800 of them and you have not gained
800 capabilities; you have buried the twelve you actually use under a pile of noise, and
made every selection worse.

Curate instead. The question for each candidate is narrow: **does this skill point at
something that actually exists in my stack?** A skill about hardening a service you don't
run, or about a threat model that doesn't apply to you, costs context on every single turn
and returns nothing.

A workable routine:

1. Clone the collection to a scratch directory, don't install it.
2. Grep the skill names for the technologies you really use.
3. Read two or three candidates in full — that tells you whether the collection is genuine
   expertise or generated filler.
4. Copy over the handful that survive, and write down **why** each one earned its place.
   Future you will not remember, and that note is what makes the set prunable later.
5. Keep the source, licence and a removal snippet next to them. Third-party skills that
   cannot be cleanly removed become permanent whether they still help or not.

Attribution is not optional: most of these collections are permissively licensed but still
require the notice to travel with the code. And check who actually publishes a collection —
a repository name containing a well-known vendor's name does not mean that vendor wrote it
or stands behind it.
