---
name: Security — leak found
about: You found a real name, client, API key, path, or other personal data in a published file
title: "Leak: <short description>"
labels: security
---

**Which file:**
`path/to/file.md`

**What was leaked:**
- [ ] Real person's name
- [ ] Company / product name (third party)
- [ ] API key / token / credential
- [ ] Email address
- [ ] Personal file path
- [ ] Internal codename / project ID
- [ ] Hostname or internal URL
- [ ] Other (describe below)

**Specific lines / quotes** (redact the leak itself if you're being careful — describe instead):

```
e.g. "Line 42 contains a path under /Users/<name>/..."
```

**Severity** (your call):
- [ ] Low — embarrassing but not harmful
- [ ] Medium — could identify a real party
- [ ] High — credential, contractual exposure, or active risk

**Suggested fix** (optional):
