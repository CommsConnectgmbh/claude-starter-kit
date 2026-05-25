---
name: Sanitizer — missing pattern
about: The sanitizer should catch a category of personal data it currently misses
title: "Sanitizer: missing pattern for <category>"
labels: enhancement, sanitizer
---

**Category of data:**
e.g. "Slack workspace IDs", "Notion page IDs", "AWS account IDs"

**Example pattern that catches it:**
```
e.g. T0[A-Z0-9]{8,10}
```

**False positive risk:**
How likely is this regex to fire on innocent text? Tested against your own `~/.claude/`?

**Source/spec for the pattern** (optional):
e.g. "Slack workspace IDs always start with T, length 9-11" — link to docs if possible.
