# Model setup (template for ~/.claude/CLAUDE.md)

- Claude is the brain: planning, architecture, difficult debugging, and reviewing Codex's work.
  Subscription: Claude Pro; switch to Claude Max 5x if the allowance is insufficient.
- Codex (ChatGPT Business) is the base: emails, customer data, writing, routine code, and independent review
  (`codex exec "Review the diff …"`). The author and reviewer are never the same model.
- Do not give Claude customer or personal data: Pro/Max is a consumer subscription without
  a data processing agreement. The `privacy-guard.py --brain` hook blocks email, CRM, and
  calendar tools as well as customer folders. Delegate customer-related tasks to Codex.
- Research without personal data: `gemini-research "Task"` (Google AI Pro, with sources).
- Long documents: `docling <file> --to md`, then `lokal-zusammenfassen` (Ollama, no cost, data stays local).
- Count and calculate with scripts, never with a language model.
- One topic per session; subagents return concise summaries only.
