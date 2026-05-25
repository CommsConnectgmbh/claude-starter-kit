# Recommended third-party skills

This kit deliberately stays small. The skills below are not mine — they belong to other authors with their own licenses. Install them from the source.

## Thinking-method skills — `obra/superpowers-skills`

[Jesse Vincent](https://github.com/obra) maintains a set of skills that formalize problem-solving techniques. They're MIT-licensed and battle-tested. If you only install one third-party pack, install this one.

```bash
git clone https://github.com/obra/superpowers-skills.git ~/code/superpowers-skills
# Then symlink the skills you want into ~/.claude/skills/
ln -s ~/code/superpowers-skills/skills/when-stuck ~/.claude/skills/when-stuck
ln -s ~/code/superpowers-skills/skills/root-cause-tracing ~/.claude/skills/root-cause-tracing
ln -s ~/code/superpowers-skills/skills/inversion-exercise ~/.claude/skills/inversion-exercise
ln -s ~/code/superpowers-skills/skills/dispatching-parallel-agents ~/.claude/skills/dispatching-parallel-agents
ln -s ~/code/superpowers-skills/skills/subagent-driven-development ~/.claude/skills/subagent-driven-development
```

What each one does:

- **when-stuck** — Diagnoses *which kind* of stuck you are and dispatches to the right technique (simplification, inversion, etc.).
- **root-cause-tracing** — Traces a bug backward through the call chain to find the original trigger, then suggests fixing at the source plus defense-in-depth.
- **inversion-exercise** — "What if the opposite assumption is true?" Reveals hidden assumptions and third paths.
- **dispatching-parallel-agents** — When 3+ independent failures could be investigated concurrently, dispatches one subagent per problem.
- **subagent-driven-development** — Executes a multi-task plan with a fresh subagent per task plus a code-review gate between them.

## Frontend design — Anthropic's `impeccable` / frontend-design

Anthropic publishes a frontend-design skill bundle. Check Anthropic's official channels for the current install location (it moves around as they iterate). License: Apache 2.0.

Use this for: designing components, auditing UI craft, polishing layouts, picking type and color systems.

## Marketing / SEO / growth packs

There are several commercial and free marketing skill packs available. If you do marketing work, these can save weeks. Buy or download from the original author — don't pirate them.

Categories worth looking for:
- Copywriting (landing pages, emails, ad copy)
- SEO (on-page audit, programmatic SEO, schema markup)
- CRO (page CRO, signup flow, popup optimization)
- Paid ads (ad creative iteration, channel strategy)
- Content strategy (content planning, social posts)

## Design / visual

- Diagram and mockup generators
- Logo and brand identity
- Slide / presentation builders
- Video and image generation pipelines

These usually wrap a specific tool API (FAL, Replicate, Anthropic Files API, etc.) and produce assets. Pick based on the tools you already pay for.

## How to evaluate a third-party skill before installing

1. **Read the SKILL.md fully.** Skills run with your tool permissions. A malicious skill could do anything you can.
2. **Check the description for triggers.** If the description is too broad, the skill will fire constantly and pollute your sessions.
3. **Check the tools allowlist.** A skill that wants `Bash(*)` deserves more scrutiny than one that only reads files.
4. **Look at the source/license.** Reputable repos with permissive licenses are easier to update and trust.

## What this kit does NOT include and why

To be explicit: the live setup this kit is based on uses many of the third-party skills above. They're not in this repo because they aren't mine to redistribute. Linking is the right answer — credit stays with the author, and you get updates.
