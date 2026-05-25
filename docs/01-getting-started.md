# Getting started

If you've never used Claude Code before, do the official setup first: <https://docs.claude.com/en/docs/claude-code>.

This doc assumes Claude Code is installed and you've successfully run `claude` in a terminal at least once.

## The mental model

Claude Code has four ways to extend or steer its behavior. Newcomers conflate them constantly. Get this straight first:

| Layer | What it does | Where it lives | When to use |
|---|---|---|---|
| **CLAUDE.md** | Project-specific instructions Claude reads every turn | Project root | Coding conventions, gotchas, "don't do X" rules |
| **Memory** | Cross-session facts about you, your projects, your preferences | `~/.claude/projects/.../memory/` | Things that should persist across conversations |
| **Skills** | Self-contained capability bundles you (or Claude) can invoke | `~/.claude/skills/<name>/SKILL.md` | Reusable workflows: decision-making, design audits, deploy scripts |
| **Agents** | Specialized sub-Claudes with their own tool access + system prompt | `~/.claude/agents/<name>.md` | Domain experts: legal, tax, code review, security |

Settings (`~/.claude/settings.json`) configure the runtime itself — permissions, theme, plugins, voice — not behavior.

## Day-1 install

```bash
# Clone this repo somewhere
git clone https://github.com/<your-handle>/claude-starter-kit.git ~/code/claude-starter-kit
cd ~/code/claude-starter-kit

# 1. Settings (diff first, this overwrites)
diff ~/.claude/settings.json settings.example.json
# If you're happy with the diff:
cp settings.example.json ~/.claude/settings.json

# 2. Install the council skill (decision-making)
mkdir -p ~/.claude/skills/council
cp skills/council/SKILL.md ~/.claude/skills/council/

# 3. Install the German legal + tax agents (skip if you don't need German law)
mkdir -p ~/.claude/agents
cp agents/legal-de.md agents/tax-de.md ~/.claude/agents/

# 4. Drop a CLAUDE.md skeleton into your first project
cp templates/CLAUDE.example.md /path/to/your/project/CLAUDE.md
# Then edit it to fit the project
```

## Day-2: turn on auto-memory

Auto-memory is the single biggest lever for making Claude Code feel like it knows you.

1. Read `docs/02-memory-system.md`.
2. Copy `templates/memory/` into your project's memory folder (Claude tells you the path the first time it writes a memory).
3. Start a conversation. Tell Claude a few things about yourself — your role, what you're working on, two or three preferences. Watch the memory files appear.

## Day-3: install third-party skills

Don't reinvent. The community has high-quality skills already.

Read `docs/04-recommended-third-party.md` for a curated list. Most install with one git clone + symlink.

## What to read next

- `docs/02-memory-system.md` — how to use auto-memory without polluting it
- `docs/03-skills-vs-agents.md` — when to write a skill vs an agent
- `docs/04-recommended-third-party.md` — what to install from elsewhere
- `docs/05-naming-conventions.md` — naming patterns for memory entries

## When to ask vs do

If you're using `defaultMode: "default"` in settings, Claude asks before every shell command. That's annoying but safe. Once you trust the setup, switch to `acceptEdits` (auto-allow file edits, still asks for shell). `bypassPermissions` is convenient but means Claude can do anything — only use it in a throwaway environment or if you really trust your CLAUDE.md.
