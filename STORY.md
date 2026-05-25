# Why this repo exists

I almost published my whole `~/.claude/` folder.

I was going to do what a lot of Claude Code users do: throw the directory on GitHub as `dotclaude`, write a one-paragraph README, and call it a contribution to the community. It worked for me. It would probably work for someone else. Open source, right?

Then I actually read the folder.

## What was in there

- An agent description that mentioned three of my clients by name as "Beispiele für Vertragsprüfung"
- A `memory/` folder with 240 files including the active state of every project I'm running, who owes me money, which deals are closing this quarter, and what my customers are paying
- A compliance skill orchestrator wired to my Aikido API keys, Supabase project refs, and a Mac mini's local IP
- A settings file in `bypassPermissions` mode (fine for me, criminal as a default for a stranger)
- Hardcoded paths under `C:\Claude Code\…` from when I'd worked on a Windows machine
- Forty marketing skills I'd bought from a commercial pack and forgotten weren't mine to redistribute
- A skill called `huashu-design` from a Chinese designer named 花叔 that I'd installed and absolutely could not legally re-upload
- My personal email in three frontmatter blocks

If I'd published that, the best case was that nobody noticed. The worst case was a DMCA from one of the original authors, an angry call from a client whose codename leaked, and a security incident if anyone parsed the settings and saw `bypassPermissions: true`.

I closed the laptop.

## The publishing dilemma

There are two existing answers in the Claude Code dotfiles space, and both are bad:

**Option A: Publish everything.** Most public `~/.claude/` repos do this. The maintainer's setup, warts and all. Easy to fork. Ships with the maintainer's client list, API project IDs, internal codenames they forgot about. Useful for the maintainer. Dangerous for anyone who installs it without auditing every file.

**Option B: Publish nothing real.** A starter template with placeholders, empty agent files saying "Customize me!", a `CLAUDE.md` that's basically the official docs reformatted. Safe to ship. Useless to install. Cargo-cult.

The actual answer is **two repos**:

1. **Your private one** — the live `~/.claude/`, with your clients, your codenames, your API references. Pin to your dotfiles or a private GitHub repo.
2. **A public, curated subset** — the workflows that have nothing to do with your business, sanitized properly, with the third-party material linked instead of copied.

This is the second repo.

## What I kept

The agents and skill I shipped are the ones that:

1. Solve a problem I actually have (German legal research, German tax research, multi-perspective strategic decisions)
2. Are entirely **mine** to license (MIT)
3. Survive sanitization without losing their value — the methodology and the discipline are the product, not the names of my clients

Two production research agents and one decision skill. ~1300 lines total. Not a starter template — actual working tools that happen to also be safe to publish.

## What I cut

Everything that was:
- About a specific client, deal, project, or codename
- From a third-party skill pack I'd installed
- Tied to my specific API keys, machine paths, or org accounts
- A snapshot of operational state that would rot in days
- Memory entries (the whole `memory/` folder is yours forever — never publish it)

## The sanitizer

The single most useful artifact in this repo is probably the smallest. `scripts/sanitize-dotclaude.sh` reads your `~/.claude/`, ignores the cache and transcript folders, and flags every file containing patterns that look personal or proprietary: API keys, user-path strings, email addresses, and whatever client codenames you add to the `COMPANY_PATTERNS` array.

It is not magic. It will not catch a client name you forgot to add to the list. But it catches API keys 100% of the time, paths 100% of the time, and forces you to **look at the flagged files** before publishing.

When I ran it on my own setup it flagged seven files I'd have shipped without thinking, including the two agents in this repo (in their original, unsanitized form). The sanitizer is the reason this repo exists at all.

## What I want this to be

A small kit a stranger can install in 60 seconds, with the working pieces extracted from a real production setup, plus the tool that lets you do the same to your own.

If you build on it, sanitize it the same way before you re-share. If you find a leak in the published files, open an issue — sanitization is never a one-pass job.

If you read this and decided to keep your `~/.claude/` private, that's a win too. Most setups should be private. Publishing a working subset is a deliberate act, not a default.

---

*Written 2026-05-25 as part of the kit's launch. If you found this through someone's tweet and the repo is much bigger now — read the changelog.*
