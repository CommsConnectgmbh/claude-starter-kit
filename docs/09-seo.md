# SEO: audit and improve your site with a measuring engine

Most "SEO help" from an AI is prose — advice it made up without ever looking at
your page. Useful once, unverifiable, and blind to what your site actually ships.
The better setup pairs two layers: an **engine** that *measures* (fetch, render,
Core Web Vitals, schema validation, sitemaps, backlinks, AI-search visibility)
and the model's **strategy** on top to interpret and fix. Measure first, then act.

The engine is a community plugin, [`claude-seo`](https://github.com/AgriciDaniel/claude-seo)
(MIT) — 25 skills, 18 sub-agents, and real Python scripts behind a single `/seo`
command. This doc wires it up cleanly.

## Install (one marketplace, one plugin)

```bash
claude plugin marketplace add AgriciDaniel/claude-seo
claude plugin install claude-seo@agricidaniel-claude-seo
```

This installs everything **namespaced** as `claude-seo:*`, so it never collides
with skills you already have. Do **not** use the repo's `install.sh` — it copies
skills flat into `~/.claude/skills/` and can overwrite a same-named skill.

### The one gotcha: Python dependencies

The scripts call `python3` directly, so `python3` must see the deps. On macOS with
Homebrew, `python3` is [PEP 668](https://peps.python.org/pep-0668/) "externally
managed" and refuses a plain `pip install`. Install into your **user** site — it
lands in `~/.local`, leaves Homebrew's own packages untouched, and is reversible:

```bash
PLUGIN=~/.claude/plugins/cache/agricidaniel-claude-seo/claude-seo/*/
python3 -m pip install --user --break-system-packages -r $PLUGIN/requirements.txt
```

Verify: `python3 -c "import bs4, trafilatura; print('ok')"`.

## Use it

```
/seo audit <url>          Full audit, parallel sub-agents, health score 0–100
/seo page <url>           Deep single-page analysis
/seo technical <url>      Crawlability, indexability, Core Web Vitals (INP)
/seo schema <url>         Detect / validate / generate Schema.org (JSON-LD)
/seo content <url>        E-E-A-T / content-quality gates
/seo geo <url>            AI Overviews / ChatGPT / Perplexity visibility
/seo backlinks <url>      Backlink profile (free: Moz, Bing, Common Crawl)
/seo local <url>          Local SEO: GBP, citations, reviews, map pack
/seo drift baseline|compare <url>   Track SEO changes over time
```

Run `/seo` with no argument for the full command list.

## What actually moves rankings (the fixes worth doing first)

The engine will surface these; here's what to prioritise when it does:

- **Internal links from your strongest page.** Your homepage has the most
  authority. If it doesn't link to your money pages with descriptive anchor text,
  they rank weaker than they should. Check the footer and nav first.
- **Thin content on commercial terms.** A 600-word page won't beat established
  competitors on a head term. Win the **specific long-tail** where you're
  genuinely differentiated instead — narrower query, thinner competition.
- **Schema that stays in sync.** If you hand-write a JSON-LD `FAQPage`, keep it
  identical to the visible FAQ. The engine's `/seo schema` validates this;
  the post-edit hook flags broken JSON-LD as you write it.
- **A sitemap that lists every indexable page**, referenced from `robots.txt`.

## Optional: connect real data

Out of the box you get on-page and technical analysis. For live ranking and
traffic data, `claude-seo` can read **Google Search Console, PageSpeed, CrUX and
GA4** (needs Google credentials) and premium backlink APIs (DataForSEO). Add these
only when you'll actually use them — see the plugin's README for the auth setup.

## What to skip

- **Don't install the Google/DataForSEO extras "just in case."** On-page + technical
  covers most of the work; wire live data when you have a page you're actively ranking.
- **Don't trust a single script's number blindly.** `parse_html` reports "0 internal
  links" if you forget the `--url` base — verify surprising findings against the raw HTML.
- **Don't audit a JS-rendered (SPA) page with a raw fetch.** Use `--render auto`, or
  the fetcher only sees the empty shell.

## Reading further

- [`claude-seo` on GitHub](https://github.com/AgriciDaniel/claude-seo)
- [Skills vs agents — docs/03](03-skills-vs-agents.md)
- [MCPs — docs/07](07-mcps.md)
