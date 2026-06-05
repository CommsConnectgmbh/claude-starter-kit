# Linear: give Claude a place to file work

Skills and agents make Claude *do* things. An issue tracker gives it somewhere to **record**
things — bugs it found but shouldn't fix unsupervised, follow-ups it noticed mid-task, work
that's real but not for right now. Wiring Claude to [Linear](https://linear.app) closes that
loop. (Any tracker works — Linear is the concrete example here.)

## Why an agent needs a tracker

Two situations come up constantly once Claude does more than one-off edits:

1. **"Found, but don't touch."** The [self-heal](05-self-healing-apps.md) agent reproduces a
   bug in a repo with real customers. The right move isn't a silent PR — it's a clear issue
   with root cause and a suggested fix, for a human to schedule. A tracker is that safe
   landing spot.
2. **"Noticed, not now."** Mid-task Claude spots a second bug, a missing test, a sketchy
   pattern. You don't want it to wander off-task — but you don't want the observation lost
   either. "File it in Linear and keep going" is the clean answer.

## Wiring it up (MCP)

Linear ships an MCP server, so Claude Code can read and create issues directly. Add it:

```bash
claude mcp add --transport sse linear https://mcp.linear.app/sse
```

Then authenticate once when prompted. After that you can just say:

> "File a Linear issue: checkout throws on empty cart. Team Web, label bug, include the repro
> steps from the report above."

and Claude creates it with title, description, team, and labels filled in. To confirm what's
available, ask Claude to list your Linear teams first — it'll use the MCP tools to fetch them.

No MCP? The same thing works through Linear's GraphQL API with a personal API key (store it in
the environment, never in a repo) — but MCP is the lower-friction path and worth preferring.

## The gating pattern (the actually useful part)

A tracker turns "autonomous" from scary into safe by splitting **diagnosis** from **change**:

| Repo kind | Synthetic finding becomes… |
|---|---|
| Side project, no users | a fix **PR** (gated on green tests) |
| Real customers / billing | a Linear **issue** only — never an unsupervised code change |

In [`pro/self-heal/agent/repos.json`](../pro/self-heal/) that's the `"issueOnly": true` flag.
Same loop, two safety levels: trusted repos get fixes, sensitive repos get a paper trail you
review. That single distinction is what makes letting an agent run overnight a calm decision
instead of a risky one.

## A good habit

End a long session with: *"Anything you noticed but didn't do — file as Linear issues so we
don't lose it."* You get a clean backlog of real follow-ups, and the current task stayed
focused instead of sprawling.
