# Contributing

Thanks for considering a contribution. A few ground rules first — most PRs that get rejected here are rejected for the same reasons.

## The bar for new content

Anything added to this repo must pass three checks:

1. **It's yours to license under MIT.** If you didn't write it, link to the source instead of copying it. The whole point of this kit is "credit stays with the author."
2. **It's sanitizable.** No personal names, no company names, no client codenames, no internal paths, no API keys. Run `./scripts/sanitize-dotclaude.sh <your-fork>` before opening the PR. CI does this too, but local feedback is faster.
3. **It's not redundant.** If your skill duplicates something in `obra/superpowers-skills`, in Anthropic's official packs, or in a major marketing pack, link it from `docs/04-recommended-third-party.md` instead of adding it.

## Submitting an agent or skill

1. Fork the repo.
2. Add your agent/skill in the right folder with a sanitized version.
3. Update `README.md` and the relevant doc if it changes the install story.
4. Run `./scripts/sanitize-dotclaude.sh .` against your fork. Resolve every REDACT and DO NOT SHARE flag before opening the PR.
5. Open the PR with a description that includes:
   - What problem the agent/skill solves
   - Why it's not already covered by something linked in `docs/04-recommended-third-party.md`
   - Any external dependencies (URLs, CLIs, API keys the user would need)
   - Confirmation that you ran the sanitizer

## Submitting a sanitizer pattern

If you've found a category of personal data the sanitizer misses, open an issue first to discuss the pattern. PRs are then welcome with:

- The new regex added to `PERSONAL_PATTERNS` or `COMPANY_PATTERNS`
- A test that demonstrates the regex catches the case
- A note in `SECURITY.md` if the pattern is non-obvious

## Submitting documentation

Doc PRs are the easiest to merge. Keep them:

- Specific (concrete file paths, concrete commands)
- Short (the reader will not read more than 1500 words per doc)
- Honest (if something is hard or annoying, say so — don't sell)

## What we won't merge

- **Logo or branding additions.** Not yet.
- **Issue templates with required emoji.** No emoji policy is repo-wide.
- **Skills that wrap a commercial API and require a paid key to be useful.** Link them from docs instead.
- **A `package.json` or build step.** The repo is intentionally script-and-markdown only.
- **A redistribution of a third-party skill pack.** Even if the license technically permits it. Link to the source.

## Style

- Markdown: GitHub-flavored, ATX headers, fenced code blocks with language tags.
- Shell: bash, `set -euo pipefail`, `shellcheck`-clean.
- No emoji in any file (the agents and docs explicitly need to stay neutral).
- No marketing language ("blazing fast", "best-in-class", etc.). The repo doesn't sell, it ships.

## Maintainer commitment

PRs will get a first-look response within 7 days. Larger changes (new agents, new docs) take longer. Sanitizer pattern PRs that come with a test usually merge same week.

If a PR has been open for 30 days with no maintainer response, ping the issue with a comment — it almost certainly got lost.
