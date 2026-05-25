# The memory system

Claude Code ships with a built-in auto-memory mechanism. The model writes facts about you to a folder on disk; on every new conversation, the index of those facts is loaded into context automatically.

This is the highest-leverage Claude Code feature most people never turn on.

## Where memory lives

When you start a conversation in a project, Claude creates (or uses) a memory folder. The exact path depends on the project path, but it looks like:

```
~/.claude/projects/<encoded-project-path>/memory/
```

Inside that folder:

```
memory/
├── MEMORY.md                  # Index — one line per memory file
├── user_you.md                # Who you are
├── feedback_no_emojis.md      # A preference
├── project_acme.md            # Context about the current project
├── reference_team_handles.md  # Pointers to external systems
└── ...
```

`MEMORY.md` is always loaded into context. The individual memory files are loaded on-demand when their description matches the current conversation.

## The four memory types

| Type | Purpose | Examples |
|---|---|---|
| `user` | Who you are, your role, your expertise | "Solo founder, 10 years Go, learning React" |
| `feedback` | Corrections + confirmations of how to work with you | "Don't summarize what you just did", "Prefer bundled PRs over splits" |
| `project` | Why the current work exists, what stage it's in | "v2 launch on YYYY-MM-DD, freeze non-critical changes after" |
| `reference` | Pointers to external systems | "Bugs tracked in Linear project ACME" |

## What NOT to put in memory

This is the part everyone gets wrong. Memory is for **non-obvious, persistent facts**. It is NOT for:

- Things derivable by reading the codebase (architecture, conventions, file paths)
- Things in git history (who-changed-what, recent fixes)
- Things already in `CLAUDE.md`
- Ephemeral state (current task, in-progress work)
- Bug-fix recipes (the fix is in the code; the commit message has the context)

If you find your memory folder filling with junk, it usually means Claude saved things that belonged in `CLAUDE.md` or in a code comment.

## Memory file structure

Each file starts with frontmatter:

```markdown
---
name: short-kebab-case-slug
description: One-line summary used to decide relevance in future conversations
metadata:
  type: user | feedback | project | reference
---

Body content. For feedback/project types, structure as:

The rule or fact.

**Why:** The reason behind it — often an incident or stakeholder ask.
**How to apply:** When and where this should kick in.

Link related memories with [[other-slug]].
```

The `Why` line matters more than people realize. A rule without its reason becomes an unanswerable question six months later: "Was this still relevant? Was it about that specific incident? Can I override it?"

## How to use it well

1. **Tell Claude things on purpose.** "Remember that we never mock the database in integration tests." It will save that as a feedback entry.
2. **Correct it when it's wrong.** "No, that was for the old auth flow — we don't do that anymore." It will update the relevant memory.
3. **Audit periodically.** Read `MEMORY.md` once a month. Delete what's stale.
4. **Don't fight the auto-write.** If Claude saves something you didn't expect, look at the entry — usually it's catching something real you said in passing.

## Memory vs CLAUDE.md

| | Memory | CLAUDE.md |
|---|---|---|
| Scope | Cross-conversation, per-project | Per-conversation, per-project |
| Who writes it | Claude (auto) | You (manual) |
| What goes in | Preferences, project state, references | Coding conventions, project structure |
| Loaded when | Description matches conversation | Every turn |
| Best for | "Who I am and how to work with me" | "What this codebase is and how it works" |

Rule of thumb: if a new contributor (human or AI) would need to know it to be productive, it goes in `CLAUDE.md`. If it's specific to you and your way of working, it goes in memory.
