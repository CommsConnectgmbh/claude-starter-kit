---
name: second-opinion
description: >-
  Holt eine ZWEITE MEINUNG zu Code von einem anderen Modell — echtes OpenAI-Codex
  wenn eingeloggt, sonst kostenlos & lokal via Ollama (qwen2.5-coder). Gegen-Review
  zu Claude-generiertem Code, damit Bugs/Security/Edge-Cases gefunden werden, die dem
  ersten Modell entgangen sind. Nutze dies, wenn der User eine zweite Meinung, einen
  Gegen-Check, ein adversariales Review will, oder bevor Code committed/gemerged wird.
  Trigger: "zweite Meinung", "second opinion", "gegen-check", "lass codex/ollama
  drueberschauen", "review den diff lokal", "ist der code gut", "vor dem merge pruefen".
---

# Second Opinion (Code-Reviewer, zweites Modell)

Holt eine **zweite Meinung** von einem **anderen** Modell — ein fremdes Modell
fängt andere Fehler als das, das den Code geschrieben hat.

**Zwei Backends, automatisch gewählt:**
- **Codex** (OpenAI, kostenpflichtiges Abo) — wenn `codex` installiert *und*
  eingeloggt ist (`codex login`). Wird bevorzugt.
- **Ollama** `qwen2.5-coder` (lokal, gratis) — Fallback wenn kein Codex-Login.

Erzwingen: `SECOND_OPINION_BACKEND=codex` oder `=ollama`.
Codex-Modell überschreiben: `SECOND_OPINION_CODEX_MODEL=<name>`.

## Wann benutzen
- Vor `git commit` / vor dem Merge eines PRs.
- Wenn der User "zweite Meinung", "gegen-check", "lokal reviewen" sagt.
- Nach größeren selbst geschriebenen Änderungen, als Sanity-Check.

## Voraussetzung
Eines von beiden reicht:
- **Codex:** `npm i -g @openai/codex` und einmalig `codex login` (ChatGPT-Abo/API-Key).
- **Ollama:** läuft auf `http://localhost:11434` mit einem coder-Modell.
  Falls das Modell fehlt: `ollama pull qwen2.5-coder:14b-instruct`.

## Verwendung

```bash
# uneingecheckte Änderungen (Standard)
python3 ~/.claude/skills/second-opinion/review.py

# nur gestagte Änderungen
python3 ~/.claude/skills/second-opinion/review.py --staged

# Commit-Range (z.B. PR-Branch gegen main)
python3 ~/.claude/skills/second-opinion/review.py --range main..HEAD

# konkrete Dateien (ganzer Inhalt, auch ohne git)
python3 ~/.claude/skills/second-opinion/review.py src/auth.ts src/db.ts

# Diff von stdin
git diff | python3 ~/.claude/skills/second-opinion/review.py --raw
```

## Workflow (so nutzt Claude es)
1. Script auf den relevanten Diff loslassen (`--staged` vor Commit, `--range` vor Merge).
2. Findings **triagieren** — das lokale 14B-Modell ist schwächer als Opus, also
   nicht blind übernehmen: jedes Finding gegen den echten Code prüfen.
3. Echte Bugs/Security/Edge-Cases fixen, Quatsch/Halluzinationen verwerfen.
4. Dem User kurz berichten: was bestätigt, was verworfen, was gefixt.

## Hinweise
- Modell-Override: `SECOND_OPINION_MODEL=... ` oder `--model <name>`.
- Anderer Host: `OLLAMA_HOST=http://...:11434`.
- Große Diffs werden bei ~60k Zeichen abgeschnitten — dann lieber pro Verzeichnis/Datei reviewen.
- Das ist ein **Hilfs**-Reviewer, kein Gatekeeper: die finale Bewertung macht Claude.
