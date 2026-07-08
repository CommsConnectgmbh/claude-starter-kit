# Token efficiency — what actually helps (and what's hype)

Every few weeks a tool shows up promising to cut your Claude token usage by "70×" or "500×" — usually by pre-indexing your codebase into a knowledge graph so Claude navigates the graph instead of re-reading files.

Before you install any of it, two things worth knowing.

## First: on a flat-rate plan, "fewer tokens" isn't the goal

If you're on a Max or Pro subscription, your tokens are effectively flat-rate. A tool that cuts token *cost* by 70× saves you nothing — you already paid. What you actually want is:

- **Speed** — less to read means faster turns.
- **Context headroom** — fitting the relevant code in the window so Claude isn't working blind.

Both are real. But they're a smaller prize than the "70× cheaper" headline implies, and most of the headline benchmarks are run against half-a-million-token monorepos, not your project.

## The real levers (in order)

1. **A `CLAUDE.md` in every repo.** This is the single biggest win and it's free. Claude reads it on every request. Put in it: what the project is, the commands (`npm run dev`, `pytest`), the architecture in three sentences, and what *not* to touch. This does the same job a code-index would — pointing Claude at the right place — but it never goes stale, because you maintain it alongside the code. See section 1 of the README.
2. **The memory system.** Persistent facts about you, the project, and how you work, loaded every session. See [`02-memory-system.md`](02-memory-system.md).
3. **Targeted search.** Modern Claude Code already greps, globs, and spins up read-only sub-agents that summarize a subsystem and return only the conclusion. It doesn't re-read your whole tree per question. The problem the graph tools solve is, to a large extent, already solved.

## Second: measure any "Nx" tool on YOUR repo before adopting it

Don't trust a blog benchmark. Run the tool once against your own code and look at the numbers. Here's the method — it takes ten minutes and it's the same discipline that keeps you honest everywhere: **verify before you assess.**

1. **Build the index once and time it.** Cheap and local? Or does it need an API key and ship descriptions of your code to a third party? (That last part matters if you have any confidentiality obligations.)
2. **Compare the index size to the codebase size.** Convert both to tokens (`chars ÷ ~3.7`). If the generated index is *bigger* than the source it indexes, you can't hold it in context anyway — you're relying entirely on per-query lookups, so those had better be good.
3. **Check query relevance on your real vocabulary.** Query the terms you actually use — including non-English domain terms. Do they resolve to the right code, or to a heading in some `REPORT.md`?
4. **Try a relationship query.** These tools sell "understands how your code connects." Ask for the path between two real concepts. If the answer is "they both import React," it's noise, not signal.
5. **Factor in staleness.** The index is a snapshot. If you deploy several times a day, it's wrong several times a day unless a watcher keeps rebuilding it. A stale index is worse than none, because it points you confidently at the wrong place.

## A real case study

We ran exactly this on two of our own repos. Local build, no API key needed (the AST extraction is genuinely free and fast) — so far so good. Then:

- **Small app (~40 files, ~120k tokens of source):** the generated graph was **2× larger than the entire codebase**. On a repo that small, a single `grep` answers any question for near-zero tokens. Net value: negative.
- **Large app (~380 files, ~1.26M tokens of source):** here the premise finally applies — the code no longer fits in one context. Symbol lookups *were* cheap and precise (~100 tokens to jump to an exact `file:line`). But: the graph was still 1.4× bigger than the code; relationship queries returned React-import noise; our non-English domain terms missed entirely; and two near-duplicate folders made almost every hit resolve to the wrong twin.

**Verdict:** graph-index tools earn their keep only on a *single, very large, cleanly-structured* repo you work in daily and can't hold in context — and even then, measure first. For everything else, a maintained `CLAUDE.md` plus memory plus targeted search wins, with none of the staleness tax.

## The meta-lesson

The reason this doc exists isn't the graph tools. It's the habit: **when something promises a 70× win, don't wave it in or wave it off from memory — spend ten minutes and measure it on your own repo.** The same rule applies to a benchmark, a "best practice," or your own first impression. Look before you conclude.
