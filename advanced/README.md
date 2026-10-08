# advanced/

Tools and templates for [`docs/11-advanced-setup.md`](../docs/11-advanced-setup.md):
Codex as your base, Claude as the brain, Gemini for research, local models for preparation, and privacy enforced through tooling.

| File | Purpose |
|---|---|
| [`tools/gemini-research`](tools/gemini-research) | Research without personal data through Gemini (Google AI Pro, `agy` CLI); returns a concise summary with sources and blocks email addresses and IBANs |
| [`tools/lokal-zusammenfassen`](tools/lokal-zusammenfassen) | Summarize long emails, PDFs, and spreadsheets locally with Ollama; scripts provide exact counts for tables |
| [`hooks/privacy-guard.py`](hooks/privacy-guard.py) | Privacy hook for Claude Code (`--brain`) and Codex |
| [`codex/`](codex/) | Codex configuration, `astra`/`luna` profiles, and an `AGENTS.md` template |
| [`claude/CLAUDE.snippet.md`](claude/CLAUDE.snippet.md) | Rules for `~/.claude/CLAUDE.md` |
