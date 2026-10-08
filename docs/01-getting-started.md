[Deutsch](01-getting-started.de.md) · **English**

# The mental model

Before you go further, learn these 4 terms. Beginners often mix them up.

| Term | Where it lives | What it does | When it applies |
|---|---|---|---|
| **CLAUDE.md** | Your project's root directory | Project-specific rules (stack, conventions, "don't do X") | Every turn: Claude reads the file automatically |
| **Auto-Memory** | `~/.claude/projects/.../memory/` | Information that should persist between conversations (who you are, your preferences) | Claude writes and reads it automatically |
| **Skills** | `~/.claude/skills/<name>/SKILL.md` | Reusable workflows (`/council`, `/verify`, etc.) | When you type the slash command or the description matches |
| **Agents** | `~/.claude/agents/<name>.md` | Specialized Claude subagents with their own system prompt and tool selection | When the description matches the question, Claude delegates |

There is also a fifth piece:

| Term | Where it lives | What it does |
|---|---|---|
| **settings.json** | `~/.claude/settings.json` | Configures the runtime (theme, permission mode, plugins), rather than behavior |

## Which one to use

**Starting work on a new project?** Write a `CLAUDE.md`. Even 5 minutes spent maintaining it can save you hours later.

**Telling Claude something about yourself?** It goes into memory automatically. You do not need to do anything manually. To correct something, just say "forget X" or "X was wrong; the correct answer is Y."

**Doing the same kind of task regularly?** That is a candidate for a skill. For example, if every PR review follows the same 4 steps, write a `code-review` skill.

**Need an expert in a particular field?** Use an agent. Tax law research, for example, needs different tools (WebFetch yes, Bash no) and a different system prompt (source requirements, disclaimer). Keep that separate from your main Claude session.

## What does not belong in memory

Memory is not for:

- Code conventions: put those in `CLAUDE.md`.
- Bug fix recipes: the fix is in the code, and the commit message provides context.
- Current tasks: they are temporary.
- Information you can get from `git log`.

If your memory folder fills up with clutter, it probably contains things that belong in `CLAUDE.md`.

## Permission modes (settings.json)

| Mode | What it does | When to use it |
|---|---|---|
| `default` | Asks before every shell command | At the start, until you trust Claude |
| `acceptEdits` | Allows file edits automatically; asks before shell commands | When working in a repo and iterating quickly |
| `plan` | Read-only, no changes | When you only want to plan or read |
| `bypassPermissions` | Allows everything automatically | Only in a disposable environment or when you know what you are doing |

This repo's `settings.example.json` uses `default`. A safe starting point.

## Read next

- [`02-memory-system.md`](02-memory-system.md): how memory works and what belongs in it.
- [`03-skills-vs-agents.md`](03-skills-vs-agents.md): the 2-minute rule of thumb for choosing between them.
- [`04-the-daily-loop.md`](04-the-daily-loop.md): the daily workflow, explore → plan → code → commit, context discipline, and verification.
