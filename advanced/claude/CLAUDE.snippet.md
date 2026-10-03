# Modell-Setup (Vorlage für ~/.claude/CLAUDE.md)

- Claude ist das Gehirn: Planung, Architektur, schwierige Fehlersuche, Prüfen von Codex-Arbeit.
  Abo: Claude Pro; reicht das Kontingent nicht, Claude Max 5x.
- Codex (ChatGPT Business) ist die Basis: Mails, Kundendaten, Texte, Routine-Code, Gegencheck
  (`codex exec "Prüfe den Diff …"`). Autor und Prüfer sind nie dasselbe Modell.
- Kunden- und Personendaten bekommt Claude nicht: Pro/Max ist ein Verbraucher-Abo ohne
  Auftragsverarbeitungsvertrag. Der Hook `privacy-guard.py --brain` sperrt Mail-, CRM- und
  Kalender-Werkzeuge sowie Kunden-Ordner. Aufgaben mit Kundenbezug gibst du an Codex.
- Recherche ohne Personenbezug: `gemini-research "Auftrag"` (Google AI Pro, mit Quellen).
- Lange Dokumente: `docling <datei> --to md`, dann `lokal-zusammenfassen` (Ollama, 0 Kosten, Daten bleiben lokal).
- Zählen und Rechnen per Skript, nie per Sprachmodell.
- Ein Thema, eine Sitzung; Subagents liefern nur Kondensate.
