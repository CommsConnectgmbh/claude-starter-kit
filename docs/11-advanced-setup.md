[Deutsch](11-advanced-setup.de.md) · **English**

# Advanced setup: Codex as your base, Claude as the brain, handling data privacy

You use the starter kit and want to keep track of running costs and token usage as a founder or solo business owner. This guide shows you how to divide work between Codex, Claude, Gemini and local tools, and how to handle customer data in that setup.

**The idea:** Use each model where it fits the task and the cost. Customer data only goes to services covered by a data processing agreement (DPA), or stays on your computer.

Prices are current as of **03.10.2026** and exclude VAT unless explicitly marked as including VAT. Sources are listed with the cost comparison. The footnote shows which figures come from our own bill and how amounts were derived.

## 1. The roles

Codex is your base for day-to-day work. Claude handles planning and review, Gemini handles research and visual tasks. You can prepare long documents locally. The table also shows which services receive customer data in this setup.

| Role | Service | Cost (excluding VAT/month) | Receives customer data? |
|---|---|---|---|
| **Base:** email, customers, writing, routine code, cross-checking | Codex through **ChatGPT Business** | from 42 € (annual billing) or 52 € (monthly billing) for the minimum of 2 Standard seats; with a 100-US-$ seat, around 130 € in practice (see section 2) | **Yes** (DPA, no training) |
| **Brain:** planning, architecture, difficult bugs, review | **Claude Pro**, or **Max 5x** if needed | 18 € (15 € with annual billing) or 90 € | **No** (consumer subscription without a DPA) |
| **Research and visuals:** web, documentation, video, screenshots | **Google AI Pro** (Gemini, CLI `agy`) | 18,48 € (21,99 € including VAT) | **No** (consumer subscription without a DPA) |
| **Local:** converting PDFs, condensing long documents | **Ollama** + **docling** on your own computer | 0 € | **Yes** (data stays on your computer) |

For cross-checking, the rule is: author ≠ reviewer. Have Claude review what Codex writes; Codex reviews what Claude plans or builds. The customer data boundaries in the table still apply.

## 2. What does it cost compared with doing everything in Claude?

Costs mainly depend on which Codex seats you choose and how much you work with Claude. **Start with the Codex seats:** ChatGPT Business requires at least 2 seats. There are two types:

| Seat | Price | Codex allowance per 5 hours (according to OpenAI) |
|---|---|---|
| Standard | 21 € with annual billing / 26 € with monthly billing | same as Plus: GPT-6 Astra 5–45, GPT-6 Sol 15–150, GPT-6 Luna 350–3.000 messages |
| Business 100 US-$ | 100 US-$ (euro price not listed on the page) | GPT-6 Astra fully included in the allowance, same allowance as Pro 5x: Astra 25–225, Sol 70–700, Luna 1.750–14.000 |

When you use up the allowance, you buy additional credits. For using Codex as your base throughout the working day, this setup uses a 100-US-$ seat plus a Standard seat. That came to around **130 € per month** for us. Source: [chatgpt.com/codex/pricing](https://chatgpt.com/de-DE/codex/pricing/?type=team).

This gives you the following combinations. The footnote shows how the costs were calculated.[^rechenweg]

| | Entry level: small Codex base | Recommended: full Codex base | With a bigger brain | Everything in Claude |
|---|---|---|---|---|
| Components | 2 Standard seats + Claude Pro + Google AI Pro + Ollama | 100-$ seat + Standard seat + Claude Pro + Google AI Pro + Ollama | same as “full”, but with Claude Max 5x | Claude Max 20x |
| Monthly cost excluding VAT | **88,48 €** (75,48 € with annual billing) + credits as needed | **around 166 €** (130 € + 18 € + 18,48 €) | **around 238 €** | **180 €** |
| Codex allowance | same as Plus | same as Pro 5x, Astra included | same as Pro 5x | none |
| Claude allowance | Pro | Pro | Max 5x | Max 20x |
| DPA for customer data | Codex | Codex | Codex | **none** |

If Claude also needs to receive customer data, add Claude Team to the comparison. Claude Team has a DPA. With 1 Premium + 1 Standard seat, it costs 126,27 € with monthly billing or 108 € with annual billing. Together with 2 Standard Codex seats and Google AI Pro, that comes to 196,75 € with monthly billing or 168,48 € with annual billing.

[^rechenweg]: Calculation: A Standard seat costs 26 € with monthly billing / 21 € with annual billing. The 130 € comes from the actual bill for 1 Business-100-$ seat + 1 Standard seat. Claude Pro: 18/15 €; Max 5x: 90 €; Max 20x: 180 € (200 US-$, euro price derived from the ratio of 100/200 $ to 90 €). Google AI Pro: 21,99 € including VAT = 18,48 € excluding VAT. Claude Team Premium: 105,23/90 €, Standard: 21,04/18 €. The calculation for the larger combination is: 238 € = 130 + 90 + 18,48.

Sources (as of 03.10.2026): [claude.com/pricing](https://claude.com/pricing), [chatgpt.com/pricing](https://chatgpt.com/pricing), [one.google.com](https://one.google.com). Prices change. Check them yourself before subscribing.

## 3. Data privacy: which plan can receive customer data?

Besides price, consider which data you want to process with a service. The table compares the training settings and DPAs of the individual plans.

| Plan | Training on your data | DPA (Art. 28 GDPR) | For customer data |
|---|---|---|---|
| ChatGPT Business | no (default) | yes, complete online: [Data Processing Addendum](https://openai.com/policies/data-processing-addendum/) | **yes** |
| ChatGPT Plus / Pro | yes, can be disabled | no | no |
| Claude Pro / Max | yes, can be disabled | no | no |
| Claude Team | no (default) | yes (commercial terms) | yes |
| Google AI Pro | yes (“Gemini-Apps-Aktivität”), can be disabled | no | no |
| Ollama locally | not applicable | not applicable | yes |

For the setup with Claude Pro/Max and Google AI Pro, this means you only process customer and personal data with Codex Business or locally. Give Claude Pro/Max and Gemini tasks that can be fully described without customer data. Disable training everywhere regardless. The settings are covered in section 4.

## 4. Setting up accounts (step by step)

Once you have chosen your plans, set up the services one by one. For each service, you will find the sign-in steps, the tools you need and the matching templates from the kit.

### 4.1 ChatGPT Business and Codex (the base)

Start with your Business account and the DPA. Then install Codex, copy the profiles and use the test commands to check which model starts.

1. [chatgpt.com/pricing](https://chatgpt.com/pricing) → “Business und Enterprise” → “Loslegen”. At least 2 seats; payment by credit or debit card; monthly or annual billing.
2. Invite a second person (or use a second account of your own for automations).
3. Complete the DPA: [openai.com/policies/data-processing-addendum](https://openai.com/policies/data-processing-addendum/) (requires the Organization ID from the Workspace-Einstellungen).
4. Install Codex:
   - macOS/Linux: `curl -fsSL https://chatgpt.com/codex/install.sh | sh`
   - Windows (PowerShell): `powershell -ExecutionPolicy ByPass -c "irm https://chatgpt.com/codex/install.ps1 | iex"`
5. Sign in: `codex login` → “Sign in with ChatGPT” using the Business account.
6. Models and profiles: copy [`advanced/codex/config.toml.example`](../advanced/codex/config.toml.example), [`astra.config.toml`](../advanced/codex/astra.config.toml), [`luna.config.toml`](../advanced/codex/luna.config.toml) to `~/.codex/`.
7. Working instructions: use [`advanced/codex/AGENTS.example.md`](../advanced/codex/AGENTS.example.md) as `~/.codex/AGENTS.md`.
8. Test: `codex exec "Antworte nur mit ok"` and `codex exec -p astra "Antworte nur mit ok"`; the model is shown at the top of the output.

### 4.2 Claude Pro and Claude Code (the brain)

Next, set up Claude for planning and review. Disable training and copy the rules for working without customer data. The hook settings follow after the account setup.

1. [claude.ai](https://claude.ai) → create an account → upgrade to **Pro** (later to **Max 5x** if needed).
2. Disable training: Profil unten links → Settings → Privacy → turn off “Help improve our AI models”.
3. Install Claude Code:
   - macOS/Linux: `curl -fsSL https://claude.ai/install.sh | bash`
   - Windows (PowerShell): `irm https://claude.ai/install.ps1 | iex`
4. Sign in: start `claude` (or `/login`) and confirm with the Pro account.
5. Rules: add [`advanced/claude/CLAUDE.snippet.md`](../advanced/claude/CLAUDE.snippet.md) to `~/.claude/CLAUDE.md`.
6. Set up the privacy hook in “brain” mode (section 5).

### 4.3 Google AI Pro and Antigravity-CLI (research)

For research and visual tasks, set up Google AI Pro and the Antigravity-CLI. The final test runs the research tool.

1. [one.google.com](https://one.google.com) → subscribe to Google AI Pro.
2. Disable training: [myactivity.google.com/product/gemini](https://myactivity.google.com/product/gemini) → “Aktiviert” → “Deaktivieren”.
3. Install the CLI:
   - macOS/Linux: `curl -fsSL https://antigravity.google/cli/install.sh | bash`
   - Windows (PowerShell): `irm https://antigravity.google/cli/install.ps1 | iex`
4. Sign in: start `agy` once, sign in through the browser with your Google account.
5. Research tool: copy [`advanced/tools/gemini-research`](../advanced/tools/gemini-research) to `~/.local/bin/` and make it executable. Test: `gemini-research "Aktuelle stabile Python-Version mit Quelle" -w 40`.

### 4.4 Ollama and docling (local, free)

Finally, add the local tools. Use docling to convert documents to Markdown; Ollama and the summarizer prepare long documents on your computer.

1. Install Ollama: macOS `curl -fsSL https://ollama.com/install.sh | sh`, Windows `irm https://ollama.com/install.ps1 | iex` (or use the installer from [ollama.com](https://ollama.com)).
2. Download the model: `ollama pull gemma4:12b` (needs around 8 GB of free memory).
3. docling for PDFs/DOCX/PPTX → Markdown: `uv tool install docling` (or `pip install docling`), run `docling datei.pdf --to md`.
4. Summarizer: copy [`advanced/tools/lokal-zusammenfassen`](../advanced/tools/lokal-zusammenfassen) to `~/.local/bin/`; requires `pip install openpyxl` for Excel. Test with a CSV: `lokal-zusammenfassen --nur-text test.csv`.

## 5. Enforcing data privacy with technical checks

Add a technical check to the rules in your instruction files: [`advanced/hooks/privacy-guard.py`](../advanced/hooks/privacy-guard.py) checks every tool call before it runs. Configure the hook with different settings for Claude and Codex.

- In **Claude Code** with `--brain`: blocks email, CRM and calendar tools and customer folders, and blocks email addresses and IBANs in requests sent to Gemini. Entry in `~/.claude/settings.json`:

```json
{ "hooks": { "PreToolUse": [ { "matcher": "*", "hooks": [
  { "type": "command", "timeout": 15, "command": "python3 ~/.claude/hooks/privacy-guard.py --brain" } ] } ] } }
```

- In **Codex** without `--brain` (Codex may receive customer data): only blocks requests containing personal data sent to Gemini. Entry in `~/.codex/hooks.json`:

```json
{ "hooks": { "PreToolUse": [ { "matcher": "*", "hooks": [
  { "type": "command", "timeout": 15, "command": "python3 ~/.codex/hooks/privacy-guard.py" } ] } ] } }
```

The hook has a limit: it does not detect names or commercial terms in running text. Those are covered by the rules in `CLAUDE.md` and `AGENTS.md`.

## 6. Saving tokens: what we measured

Once the setup is running, you can influence usage in two places: the model you choose and the content you send it. The following points come from our measurements and tests.

- **An inexpensive default model, the expensive one only when needed:** In Codex, Astra costs several times as many credits as Sol. Use Sol as the default and Astra only for final drafts.
- **Reasoning effort “medium”** instead of “high” as the default.
- **Short instruction files:** Every model call includes them. In our setup, every Codex step started with around 32.000 tokens before any work was done.
- **Every step sends the entire history again:** List first, then open selectively; one topic per session.
- **Never read PDFs as images:** First `docling … --to md`, then read or summarize locally.
- **Summarize locally:** In our test, Gemma 4 12B (without thinking mode) summarized a contract and an email thread without errors, in under a minute per task on a Mac mini M4 Pro with 24 GB.
- **Never count with a language model:** Three local models miscounted 84 table rows as 64 to 89. `lokal-zusammenfassen` counts tables with a script and gives the model only the exact numbers.

## 7. How to direct the setup

You can enter your tasks in Claude or Codex. Use the same phrases to direct which tool takes over. You will also find the assignments in [`AGENTS.example.md`](../advanced/codex/AGENTS.example.md):

| You say | Who takes over |
|---|---|
| “Research …” | Gemini through `gemini-research` |
| “Summarize this PDF” | locally: docling + `lokal-zusammenfassen` |
| “Write to the customer …” | Codex (final draft `-p astra`) |
| “Plan this”, “Review my code” | Claude |
| “Count …” | Script |

## 8. Which option is worth it for you?

Your choice mainly depends on three questions: Do you work with customer data, do you use Codex all day, and is your Claude allowance sufficient? These lead to the following options.

- **Solo, working with customer data, tight budget:** Small Codex base (2 Standard seats) with Claude Pro; use Astra sparingly.
- **Codex as your workhorse throughout the day:** A 100-US-$ seat plus a Standard seat, alongside Claude Pro: less expensive than Claude Max 20x, with a DPA for customer data.
- **Claude Pro is not enough as the brain:** Claude Max 5x instead of Pro.
- **Small team, Claude also needs to receive customer data:** Claude Team instead of Pro/Max.
- **No customer data, only your own projects:** Claude Max 20x on its own is convenient, but more expensive than the Codex base.
