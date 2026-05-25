# Security policy

## Reporting a leak in the published files

If you find any of the following in this repository, report it as a security issue (not a regular issue):

- A real person's name (other than contributors who explicitly opted in)
- A company or product name belonging to a third party
- API keys, tokens, or credentials of any kind
- An email address other than ones already public in `LICENSE` / `CONTRIBUTING.md`
- A personal file path (`/Users/<name>/`, `C:\Users\<name>\`, etc.)
- An internal codename, project ID, or hostname that could identify a non-public system

**How to report:**

- Open a GitHub issue using the "Security: leak found" template (if available)
- Or email the maintainer directly via the address in the repo metadata
- Or, for high-sensitivity findings, use [GitHub's private vulnerability reporting](https://docs.github.com/en/code-security/security-advisories/guidance-on-reporting-and-writing-information-about-vulnerabilities/privately-reporting-a-security-vulnerability)

The repo will be force-rebased to remove the leak once confirmed. Watch the commits if you want to follow the fix.

## Reporting an unsafe pattern in the sanitizer

The sanitizer at `scripts/sanitize-dotclaude.sh` is a pattern-matcher, not a guarantee. If you find a category of personal/proprietary data it misses, please open a regular issue with:

- The pattern (e.g. "Slack workspace IDs look like `T0XXXXX` and aren't caught")
- An example regex that would catch it
- Whether you've tested the regex against a real `~/.claude/` to confirm it doesn't produce excessive false positives

PRs that add new patterns to `PERSONAL_PATTERNS` are welcome.

## Threat model

This repo is a **read-only configuration starter**. It does not:

- Execute network calls during normal use
- Collect telemetry
- Phone home

The two scripts (`install.sh`, `scripts/sanitize-dotclaude.sh`) do execute locally. Read them before running, especially the install script if you use the `curl ... | bash` form. Both are kept short on purpose so audit takes under five minutes.

## What is explicitly NOT a security issue

- Bugs in the example agents' legal/tax reasoning — these are research aids, never legal/tax advice (see disclaimers in the files)
- Memory entries you accidentally published yourself by skipping the sanitizer — sorry, that's on you
- Third-party skills installed via `docs/04-recommended-third-party.md` — their security is the upstream maintainer's responsibility
