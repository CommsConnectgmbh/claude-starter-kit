---
name: feedback-no-emojis
description: Never add emojis to code, commits, PR descriptions, or UI unless explicitly asked
metadata:
  type: feedback
---

Never add emojis to code, commits, PR descriptions, or UI copy unless I explicitly ask.

**Why:** Personal preference. Emojis in technical artifacts age badly and clutter diffs.

**How to apply:** This rule covers everything you generate — file contents, commit messages, PR bodies, log lines, UI strings, comments. Markdown chat responses are fine without emojis too. If a downstream tool (e.g. a release-notes generator) inserts them later, that's not your concern.
