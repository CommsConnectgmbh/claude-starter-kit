# MCPs: connect Claude to your real tools

[MCPs (Model Context Protocol servers)](https://modelcontextprotocol.io) are how Claude Code
talks to outside systems — your issue tracker, error monitor, database, CRM. Without them,
Claude is stuck with files and the shell. With them, *"what errors did we see last night?"*
or *"file this as a bug in Linear"* just work.

This is a curated list of the MCPs that pair well with the rest of the kit. Each one is a
single `claude mcp add` away and authenticates on first use.

## The shortlist

| MCP | One-line setup | Why it pairs with this kit |
|---|---|---|
| [Linear](https://linear.app) | `claude mcp add --transport sse linear https://mcp.linear.app/sse` | Safe landing spot for "found, don't fix yet" — see [docs/06](06-linear-issues.md). |
| [Sentry](https://sentry.io) | `claude mcp add --transport http sentry https://mcp.sentry.dev/mcp` | Real error monitor the [self-heal](05-self-healing-apps.md) loop reads from. See below. |
| [Supabase](https://supabase.com) | `claude mcp add --transport http supabase https://mcp.supabase.com/mcp` | Inspect schema, run SQL, read logs — invaluable if your stack is Supabase. |

All three are hosted by the vendor — no proxy, no API key in a file, OAuth on first call.
Add the ones that match your stack, skip the rest.

## Sentry: pair it with self-heal

The [self-heal](05-self-healing-apps.md) doc says *"for real traffic, install a real error
monitor."* Sentry's MCP is the bridge that lets the fix-agent read what real users hit:

```bash
claude mcp add --transport http sentry https://mcp.sentry.dev/mcp
```

After auth you can ask things like:

> *"List unresolved issues in project `web-app` from the last 24h, grouped by file. Open a
> Linear issue for any with more than 10 events."*

This turns Sentry from a dashboard you forget to check into a queue the loop pulls from.
Combine with the Linear MCP (above) and the **gating pattern** from [docs/06](06-linear-issues.md)
to keep autonomous fixes out of customer-facing repos.

## Linear: where unsupervised work goes to land

Covered in detail in [docs/06](06-linear-issues.md). Two lines worth repeating:

- "Found, don't touch" bugs from self-heal → Linear issue with repro steps, not a silent PR.
- "Noticed, not now" observations mid-task → filed and forgotten, instead of derailing the work.

## Adding your own

Two flavours of MCP:

1. **Hosted (HTTP/SSE)** — the vendor runs it. `claude mcp add --transport http <name> <url>`.
   OAuth on first call. This is the path of least resistance — prefer it.
2. **Local (stdio)** — runs on your machine as a subprocess. Use this for self-hosted things,
   custom tools, or proxies. `claude mcp add <name> -- <command> <args...>`.

To inspect what's wired up:

```bash
claude mcp list
```

If a hosted MCP isn't responding after auth, the most common cause is an expired token —
remove and re-add to re-trigger OAuth.

## What to skip

- **Don't add an MCP for something you don't use yet.** Each one is more tools in the
  context window. Add when you have a recurring "I wish Claude could just…" moment.
- **Don't put API keys for hosted MCPs in `.env` files.** OAuth handles it; if you ever have
  to paste a token, you're probably on the wrong path.
- **Don't bundle MCP configs into a shared repo's `.mcp.json`.** That file is fine for *project-
  scoped* MCPs (e.g. a project-specific database), but personal tools belong in
  `~/.claude.json`, never checked in.

## Reading further

- [Anthropic MCP docs](https://modelcontextprotocol.io)
- [Claude Code MCP guide](https://docs.claude.com/en/docs/claude-code/mcp)
- [Linear issues — docs/06](06-linear-issues.md)
- [Self-healing apps — docs/05](05-self-healing-apps.md)
