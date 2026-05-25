# GitHub repo metadata

Copy these into the GitHub repo settings when you publish. Not visible in the rendered repo.

## Description (250 char max)

```
A small, honest, working Claude Code setup. 2 production agents (German legal + tax), 1 decision skill, a sanitizer that flags personal data in your own ~/.claude/ before you publish. The kit you'd actually want to install.
```

## Topics (use the GitHub topic picker — these are the ones to enter)

- `claude-code`
- `claude`
- `anthropic`
- `dotfiles`
- `starter-kit`
- `ai-agents`
- `ai-coding`
- `developer-tools`
- `productivity`
- `german-law`

## Website URL

Leave blank unless you have a project page. The repo speaks for itself.

## Social preview image

Optional. If you make one:
- 1280×640 PNG
- High-contrast text "claude-starter-kit" + the one-liner from the README
- Keep it text-only — image-heavy social cards date faster than text ones

## Repository settings

- Issues: enabled
- Projects: disabled (premature)
- Wiki: disabled (use docs/ in-repo instead)
- Discussions: enabled (good for "how do I sanitize X?" Q&A)
- Sponsorships: leave off until you have a clear policy

## Branch protection (`main`)

- Require pull request before merging: yes
- Require status checks to pass: yes (`shellcheck`, `sanitizer-self-test`, `markdown-link-check`)
- Require linear history: optional (cleaner log if yes)
- Include administrators: no (don't lock yourself out)

## Labels to create

Standard set plus repo-specific:
- `security` (red) — for leak reports
- `sanitizer` (yellow) — for sanitizer pattern issues/PRs
- `good first issue` (green) — for new contributors
- `documentation` (blue) — for doc-only PRs
- `wontfix` (gray) — for the inevitable scope-creep requests

## Release process

```bash
# Tag the version
git tag -s v0.1.0 -m "v0.1.0 — initial public release"
git push origin v0.1.0

# Create the release
gh release create v0.1.0 \
  --title "v0.1.0 — initial public release" \
  --notes-from-tag

# (Optional) Pin the release on the repo
```
