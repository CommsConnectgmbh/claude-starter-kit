# Launch playbook

Pre-written copy + a launch sequence so you don't have to invent it at 9 AM on launch day. Pick what fits your voice; edit before posting.

## Pre-launch checklist (do this first)

- [ ] Repo description on GitHub set (see `.github/repo-meta.md`)
- [ ] Repo topics set: `claude-code`, `claude`, `anthropic`, `dotfiles`, `starter-kit`, `agents`, `ai-coding`
- [x] `OWNER` placeholders replaced with `CommsConnectgmbh` (done during initial publish)
- [ ] Replace the LICENSE copyright line if needed
- [ ] Create the v0.1.0 release tag on GitHub (`gh release create v0.1.0 --generate-notes`)
- [ ] Pin the repo on your GitHub profile
- [ ] Verify the install.sh raw URL resolves and the script runs in a clean container

```bash
# Container smoke test
docker run --rm -it -v "$PWD:/repo" ubuntu:24.04 bash -c '
  apt-get update -qq && apt-get install -y -qq curl git ca-certificates
  curl -fsSL https://raw.githubusercontent.com/CommsConnectgmbh/claude-starter-kit/main/install.sh | bash
'
```

## Launch day — the sequence

**T = 0 (morning, local time):**
1. Post on Twitter/X (thread, 4 tweets — copy below)
2. Cross-post the single best tweet to LinkedIn (different copy, see below)
3. Submit to Hacker News (title + URL only, see below)

**T + 2 hours:**
4. Reply to your own HN post with a substantive comment (your story, not a sales pitch)
5. Post in /r/ClaudeAI (Reddit)

**T + 24 hours:**
6. If HN dropped off, do NOT resubmit — repost on Hacker News is bannable. Wait 30+ days.
7. If Twitter post landed, quote-tweet with the most interesting reply.

**T + 1 week:**
8. Write a follow-up post with adoption numbers, surprises, contributions received.

---

## Copy: Twitter / X thread

Tweet 1 (hook):
```
I almost published my whole ~/.claude/ folder.

Then I actually read it.

I shipped this instead — a small, sanitized starter kit + a script that scans your ~/.claude/ for the things you'd accidentally leak.

github.com/CommsConnectgmbh/claude-starter-kit
```

Tweet 2 (what's in it):
```
What's in the kit:
• 2 production agents (German legal + tax research, both with mandatory source citation)
• 1 decision-making skill (5-role council, picks a side, no hedging)
• A sanitizer that scans your ~/.claude/ for personal data
• Docs explaining skills vs agents vs memory

~1300 lines. Read in 20 min.
```

Tweet 3 (the sanitizer):
```
The most useful file is probably scripts/sanitize-dotclaude.sh.

Run it on your own ~/.claude/. It flags API keys, paths, emails, and any company codenames you add.

When I ran it on mine, it caught 7 files I'd have shipped without thinking.

Including the two agents in this repo, before I sanitized them.
```

Tweet 4 (call to action):
```
If you've been sitting on a "should I open-source my Claude Code setup?" question — read the STORY.md. The answer is usually "yes, but not the whole thing."

Star the repo if useful. Open an issue if you find a leak. Both are wins.

github.com/CommsConnectgmbh/claude-starter-kit
```

## Copy: LinkedIn single post (longer form)

```
A small thing I shipped today: claude-starter-kit.

Most public Claude Code dotfiles repositories do one of two things — dump everything (which leaks the maintainer's client names, API references, and forgotten codenames) or strip everything (so they're useless to install).

I tried to ship the working middle: 2 sanitized production agents (German legal + tax research), 1 decision-making skill, a CLAUDE.md skeleton, and a sanitizer script that scans your own ~/.claude/ folder and flags personal data before you publish.

Two things I learned writing it:

1. The sanitizer is the most reusable artifact. It caught 7 files in my own setup that I'd have published without thinking, including the two agents in this repo before I sanitized them.

2. "Two repos" beats "one repo" — your live setup stays private with your clients and API keys; a curated subset is what you publish. The kit makes the second one easier to maintain.

Link in the first comment. MIT licensed.
```

## Copy: Hacker News

Title (under 80 chars, no clickbait):
```
A sanitized Claude Code starter kit, with the script I used to sanitize it
```

URL:
```
https://github.com/CommsConnectgmbh/claude-starter-kit
```

First comment (post 1-2 minutes after submitting):
```
Author here. The TL;DR is in the README, but the longer story is in STORY.md:
I almost published my whole ~/.claude/ folder, then read it, then closed my
laptop. This repo is the curated public subset of a real working setup, plus
the sanitizer script that made it safe to publish.

The two agents (German legal + tax) are not toy examples — they're the actual
research agents I use, with mandatory source citation, statutory disclaimers,
and a discipline to refuse anything that needs a licensed professional. The
methodology applies to any jurisdiction; the kmein/gesetze + gesetze-im-internet.de
URLs are the German-specific bits.

The sanitizer alone is maybe the most reusable part. It's a 130-line bash script,
shellcheck-clean, with patterns for API keys, paths, and customizable company
codenames. Run it on your own ~/.claude/ before you publish anything.

Happy to discuss the design decisions, what I deliberately left out, or why
I think Anthropic's auto-memory feature is the highest-leverage Claude Code
feature most users don't turn on.
```

## Copy: Reddit /r/ClaudeAI

Title:
```
[Tool] A sanitized starter kit for Claude Code — and the script I used to sanitize my own ~/.claude/
```

Body:
```
Hey folks. I shipped a small repo today aimed at people who want to publish
their Claude Code setup but get nervous when they actually look at what's in
the folder.

What's in it:
- 2 real production agents (German legal + tax research, both MIT, both with
  mandatory source citation discipline)
- 1 skill called "council" — 5-role decision-making framework (Visionär,
  Kritiker, Kreativer, Skeptiker, Logiker) that picks a side and refuses to
  hedge
- A sanitizer script that scans your own ~/.claude/ and flags API keys,
  personal paths, email addresses, and any company codenames you add
- A CLAUDE.md skeleton + a worked example of the auto-memory pattern
- Docs explaining skills vs agents vs memory vs settings

Link: https://github.com/CommsConnectgmbh/claude-starter-kit

The thing I'm most curious about is whether the sanitizer catches enough by
default. If you run it and it misses something obvious in your setup, please
open an issue or PR with the pattern — I'd love to harden it.
```

## Copy: short blurb for your own blog (if you have one)

```
Today I open-sourced claude-starter-kit, a small Claude Code setup
distilled from my own daily workflow with the client names and API references
surgically removed. The most interesting artifact is probably the sanitizer
script that made it possible to publish at all — it scans a ~/.claude/ folder
and flags everything you'd accidentally leak.

Most public Claude Code dotfiles repositories are dangerous because their
maintainers never look at them again after the first commit. The kit is built
around the idea that publishing should be a deliberate act, not a default,
and that the working middle (real agents + a sanitizer) beats both extremes
(dump everything / strip everything).

[Link]
```

## What NOT to do on launch day

- Don't @ Anthropic employees on Twitter unless you know them personally. The repo is not an Anthropic product.
- Don't claim the agents are "legally vetted" or "tax-compliant". They're research aids with mandatory disclaimers.
- Don't promise updates you can't sustain. The CHANGELOG.md commits you to nothing — keep it that way.
- Don't cross-post the same copy to all five channels. Each platform has its own voice; the snippets above are different on purpose.
- Don't argue with low-effort criticism in comments. Reply to substantive feedback only.

## If it doesn't go viral

That's fine. The repo is useful even with 12 stars. The sanitizer is useful even with 0 stars. Pin it to your GitHub profile and move on. A small, durable tool beats a viral moment that nobody installs.
