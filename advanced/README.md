# advanced/

Werkzeuge und Vorlagen zum Leitfaden [`docs/11-advanced-setup.md`](../docs/11-advanced-setup.md):
Codex als Basis, Claude als Gehirn, Gemini für Recherche, lokale Modelle für Vorarbeit, Datenschutz technisch erzwungen.

| Datei | Wofür |
|---|---|
| [`tools/gemini-research`](tools/gemini-research) | Recherche ohne Personenbezug über Gemini (Google AI Pro, CLI `agy`), nur Kondensat mit Quellen zurück; blockiert Mailadressen und IBANs |
| [`tools/lokal-zusammenfassen`](tools/lokal-zusammenfassen) | Lange Mails, PDFs, Tabellen lokal mit Ollama verdichten; Tabellen werden per Skript exakt gezählt |
| [`hooks/privacy-guard.py`](hooks/privacy-guard.py) | Datenschutz-Hook für Claude Code (`--brain`) und Codex |
| [`codex/`](codex/) | Codex-Konfiguration, Profile `astra`/`luna`, Vorlage `AGENTS.md` |
| [`claude/CLAUDE.snippet.md`](claude/CLAUDE.snippet.md) | Regeln für `~/.claude/CLAUDE.md` |
