# The daily loop: explore → plan → code → commit

The first three docs covered *structure* — what CLAUDE.md, memory, skills, and agents are. This one covers *motion*: how to actually drive Claude Code through a real task without it going sideways.

There is one principle underneath everything here, so learn it first.

## Context is the resource you manage

Every file Claude reads, every command it runs, every message you send lands in one finite context window. A fresh session in a mid-size repo can burn 20k+ tokens before you type anything. Past roughly 70–80% full, quality drops in a specific, recognizable way: Claude starts "forgetting" things you said earlier, re-reading files it already saw, and making more mistakes.

You can't stop the window from filling. You *can* decide what goes in and when to reset:

- **`/clear` between unrelated tasks.** Finished the auth bug, now doing a CSS tweak? Clear first. Carrying the auth context into the CSS task only adds noise.
- **Delegate big reads to an agent.** "Search the codebase for every place we validate input" can return 40 file excerpts. Let a subagent do that digging and report back a summary — its context fills up and gets thrown away, yours stays clean. (See [`03-skills-vs-agents.md`](03-skills-vs-agents.md).)
- **Keep CLAUDE.md short.** It's reloaded every turn. Every stale line is permanent rent.

Rule of thumb: **if you had to correct Claude twice on the same point, the context is probably polluted. `/clear` and restart with a sharper prompt beats fighting it.**

## The four phases

For anything bigger than a one-line change, run these in order. The whole point is to separate *thinking* from *doing* so a wrong assumption gets caught before it becomes 200 lines of wrong code.

### 1. Explore (read-only)

Press **Shift+Tab** until you reach **Plan Mode**. In this mode Claude reads and reasons but makes **no edits**. Use it to build a shared understanding before any code exists.

```
Read src/auth and explain how sessions and login work.
Also show me how we manage secrets via environment variables.
```

### 2. Plan

Still in Plan Mode, ask for an actual plan — which files change, in what order, what the tricky parts are.

```
I want to add Google OAuth. Which files need to change?
What does the session flow look like? Write a plan before touching anything.
```

Read the plan. This is the cheapest possible moment to catch a bad approach — it's just text. If the plan is wrong, say so and re-plan. Don't approve a plan you only half-read.

### 3. Code

Leave Plan Mode (Shift+Tab back to normal) and let it execute — **with a way to check its own work baked into the prompt** (next section).

```
Implement the OAuth flow per the plan. Write tests for the callback handler,
run the test suite, and fix anything that fails.
```

### 4. Commit

```
Create a commit with a clear message and open a PR.
```

**When to skip the loop:** trivial changes. If you can describe the whole diff in one sentence ("rename `foo` to `bar` everywhere"), just say that. Plan Mode for a typo fix is ceremony.

## The single biggest quality lever: give Claude a way to verify

This is the one habit that separates "looks plausible" from "actually works." **Without a way to check itself, Claude produces code that reads correctly and fails at runtime.** With one, it catches its own mistakes before you ever see them.

A verification handle is anything Claude can run or compare against: a test, an expected output, a screenshot to diff, a lint command, a type-check.

| Weak prompt | Strong prompt |
|---|---|
| "Add email validation" | "Write `validateEmail`. Test cases: `user@example.com` → true, `invalid` → false. Run the tests after implementing." |
| "Make the dashboard nicer" | "[screenshot] Implement this design. Then take a screenshot and compare it to the original." |
| "The build is broken" | "The build fails with this error: [error]. Fix the root cause — don't suppress the error." |

If you can't give it a verification handle, at minimum ask it to *write a failing test first*, then make it pass.

## Write prompts as symptom + location + success criteria

Vague: *"Fix the login bug."*

Sharp:

> Users report login fails after a session timeout. Check the auth flow in `src/auth/`, especially token refresh. Write a failing test that reproduces it, then fix the cause.

Three things made it sharp: the **symptom** (fails after timeout), the **location** (`src/auth/`, token refresh), and the **success criterion** (a test that now passes). Reference files with `@src/auth/login.ts`, not "the login file." Paste errors and screenshots directly. Point at a pattern to follow: "do it like `HotDogWidget.tsx`."

### The briefing prompt (for bigger features)

For anything substantial, don't brief Claude — make it brief *you*:

```
I want to build [one-line description].
Interview me with the AskUserQuestion tool. Ask about technical approach,
UI/UX, edge cases, and trade-offs. Don't ask the obvious questions —
dig into the parts I'm likely to have missed. Then write a complete
briefing to BRIEFING.md.
```

Then start a **fresh session** and point it at `BRIEFING.md`. Clean context, a reference doc you both agree on.

## Carrying work across sessions

Context doesn't survive a `/clear` or a closed terminal — but you don't want it to. You want a *clean* handoff, not a dragged-along mess.

- **`claude --continue`** resumes your last session as-is. **`claude --resume`** lets you pick from a list.
- **Esc** stops Claude mid-action (context preserved). **Esc Esc** opens rewind — jump back to an earlier state of chat, code, or both.
- **`/compact <focus>`** summarizes the conversation so far, optionally biased toward a topic, freeing space without a full reset.

For a real end-of-day handoff that outlives the session entirely, have Claude write it down:

```
Summarize today's session into HANDOFF.md so I can resume cleanly tomorrow:
- What got done (concrete changes, files, commits)
- Where we are (what works, what's tested, what's half-finished)
- What's next (the immediate next step, with reasoning)
- Decisions & dead ends (so we don't re-litigate them)
- Open questions
Be concrete: file paths, function names, line numbers. No filler.
```

Next morning: `Read HANDOFF.md and summarize in 5 sentences where we are and what's next.` Pair the handoff with `/clear` and you get a clean context *plus* a full briefing — the best of both.

## Common failure modes

| Symptom | Cause | Fix |
|---|---|---|
| Claude "forgets" things you said earlier | Context full of unrelated work | `/clear` between independent tasks |
| You correct the same thing 3+ times | Polluted context — the bad version keeps anchoring | `/clear`, restart with a sharper prompt |
| Code looks right but fails at runtime | No verification handle in the prompt | Always give it a test / expected output / screenshot |
| "Investigate X" reads hundreds of files | Scope too broad | Narrow the scope or hand it to a subagent |
| CLAUDE.md rules get ignored | File too long; signal lost in noise | Cut it under ~200 lines; for must-happen things use a hook |

---

The whole loop in one line: **manage the context, explore before you plan, plan before you code, and never ship Claude code it couldn't check itself.**
