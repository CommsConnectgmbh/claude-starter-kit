# Advanced Setup: Codex als Basis, Claude als Gehirn, Datenschutz sauber

<!-- ENTWURF (Gerüst mit Fakten). Fließtext folgt, siehe PR. Preise: Stand 03.10.2026, netto, offizielle Preisseiten. -->

Für alle, die nach dem Starter-Kit weniger zahlen, Token sparen und Kundendaten DSGVO-sauber verarbeiten wollen.

**Die Idee in einem Satz:** Jedes Modell macht nur, wofür es am besten und am günstigsten ist, und Kundendaten gehen nur dorthin, wo ein Auftragsverarbeitungsvertrag (AVV) besteht.

## 1. Die Rollen

| Rolle | Dienst | Kosten (netto/Monat) | Bekommt Kundendaten? |
|---|---|---|---|
| **Basis:** Mails, Kunden, Texte, Routine-Code, Gegencheck | Codex über **ChatGPT Business** | ab 42 € (jährlich) bzw. 52 € (monatlich) für die Mindestzahl von 2 Standard-Plätzen; mit einem 100-US-$-Platz in der Praxis rund 130 € (siehe Abschnitt 2) | **Ja** (AVV, kein Training) |
| **Gehirn:** Planung, Architektur, schwierige Fehler, Prüfen | **Claude Pro**, bei Bedarf **Max 5x** | 18 € (15 € jährlich) bzw. 90 € | **Nein** (Verbraucher-Abo ohne AVV) |
| **Recherche und Visuelles:** Web, Doku, Video, Screenshots | **Google AI Pro** (Gemini, CLI `agy`) | 18,48 € (21,99 € brutto) | **Nein** (Verbraucher-Abo ohne AVV) |
| **Lokal:** PDFs umwandeln, lange Inhalte verdichten | **Ollama** + **docling** auf dem eigenen Rechner | 0 € | **Ja** (Daten verlassen den Rechner nicht) |

Autor ≠ Prüfer: Was Codex schreibt, prüft Claude; was Claude plant oder baut, prüft Codex.

## 2. Was kostet das, verglichen mit „alles bei Claude“?

**Erst die Codex-Plätze verstehen.** ChatGPT Business braucht mindestens 2 Plätze. Es gibt zwei Arten:

| Platz | Preis | Codex-Kontingent pro 5 Stunden (laut OpenAI) |
|---|---|---|
| Standard | 21 € jährlich / 26 € monatlich | wie Plus: GPT-6 Astra 5–45, GPT-6 Sol 15–150, GPT-6 Luna 350–3.000 Nachrichten |
| Business 100 US-$ | 100 US-$ (Euro-Preis auf der Seite nicht angegeben) | GPT-6 Astra voll im Kontingent enthalten, Kontingent wie Pro 5x: Astra 25–225, Sol 70–700, Luna 1.750–14.000 |

Über das Kontingent hinaus kauft man Credits. Wer Codex als echte Basis für den ganzen Arbeitstag nutzt, nimmt einen 100-US-$-Platz plus einen Standard-Platz. Das ergab bei uns rund **130 € im Monat**. Quelle: [chatgpt.com/codex/pricing](https://chatgpt.com/de-DE/codex/pricing/?type=team).


| | Einstieg: Codex-Basis klein | Empfohlen: Codex-Basis voll | Mit größerem Gehirn | Alles bei Claude |
|---|---|---|---|---|
| Zusammensetzung | 2 Standard-Plätze + Claude Pro + Google AI Pro + Ollama | 100-$-Platz + Standard-Platz + Claude Pro + Google AI Pro + Ollama | wie „voll“, aber Claude Max 5x | Claude Max 20x |
| Netto pro Monat | **88,48 €** (jährlich 75,48 €) + Credits bei Bedarf | **rund 166 €** (130 € + 18 € + 18,48 €) | **rund 238 €** | **180 €** |
| Codex-Kontingent | wie Plus | wie Pro 5x, Astra inklusive | wie Pro 5x | keines |
| Claude-Kontingent | Pro | Pro | Max 5x | Max 20x |
| AVV für Kundendaten | Codex | Codex | Codex | **keiner** |

Zum Vergleich, wenn auch Claude Kundendaten sehen soll: Claude Team (1 Premium- + 1 Standard-Platz, 126,27 € monatlich bzw. 108 € jährlich) hat einen AVV; zusammen mit 2 Standard-Codex-Plätzen und Google AI Pro sind das 196,75 € monatlich bzw. 168,48 € jährlich.

<!-- Rechenweg: Standard-Platz 26 € monatlich / 21 € jährlich; 130 € = reale Rechnung für 1 Business-100-$-Platz + 1 Standard-Platz; Claude Pro 18/15 €; Max 5x 90 €; Max 20x 180 € (200 US-$, Euro-Preis aus dem Verhältnis 100/200 $ zu 90 €); Google AI Pro 21,99 € brutto = 18,48 € netto; Claude Team Premium 105,23/90 €, Standard 21,04/18 €. 238 € = 130 + 90 + 18,48. -->

Quellen (Stand 03.10.2026): [claude.com/pricing](https://claude.com/pricing), [chatgpt.com/pricing](https://chatgpt.com/pricing), [one.google.com](https://one.google.com). Preise ändern sich: vor dem Abschluss selbst prüfen.

## 3. Datenschutz: welcher Tarif darf Kundendaten sehen?

| Tarif | Training mit deinen Daten | AVV (Art. 28 DSGVO) | Für Kundendaten |
|---|---|---|---|
| ChatGPT Business | nein (Standard) | ja, online abschließen: [Data Processing Addendum](https://openai.com/policies/data-processing-addendum/) | **ja** |
| ChatGPT Plus / Pro | ja, abschaltbar | nein | nein |
| Claude Pro / Max | ja, abschaltbar | nein | nein |
| Claude Team | nein (Standard) | ja (kommerzielle Bedingungen) | ja |
| Google AI Pro | ja („Gemini-Apps-Aktivität“), abschaltbar | nein | nein |
| Ollama lokal | entfällt | entfällt | ja |

Folgerung: Kunden- und Personendaten nur an Codex Business oder lokal. Claude Pro/Max und Gemini bekommen Aufgaben, die ohne Kundendaten vollständig beschrieben sind. Training trotzdem überall abschalten (Abschnitt 4).

## 4. Konten einrichten (Schritt für Schritt)

### 4.1 ChatGPT Business und Codex (die Basis)

1. [chatgpt.com/pricing](https://chatgpt.com/pricing) → „Business und Enterprise“ → „Loslegen“. Mindestens 2 Plätze; Zahlung per Kredit- oder Debitkarte; monatlich oder jährlich.
2. Zweite Person einladen (oder zweiten eigenen Zugang für Automationen).
3. AVV abschließen: [openai.com/policies/data-processing-addendum](https://openai.com/policies/data-processing-addendum/) (braucht die Organization ID aus den Workspace-Einstellungen).
4. Codex installieren:
   - macOS/Linux: `curl -fsSL https://chatgpt.com/codex/install.sh | sh`
   - Windows (PowerShell): `powershell -ExecutionPolicy ByPass -c "irm https://chatgpt.com/codex/install.ps1 | iex"`
5. Anmelden: `codex login` → „Sign in with ChatGPT“ mit dem Business-Konto.
6. Modelle und Profile: [`advanced/codex/config.toml.example`](../advanced/codex/config.toml.example), [`astra.config.toml`](../advanced/codex/astra.config.toml), [`luna.config.toml`](../advanced/codex/luna.config.toml) nach `~/.codex/` kopieren.
7. Arbeitsanweisung: [`advanced/codex/AGENTS.example.md`](../advanced/codex/AGENTS.example.md) als `~/.codex/AGENTS.md`.
8. Test: `codex exec "Antworte nur mit ok"` und `codex exec -p astra "Antworte nur mit ok"`; im Kopf der Ausgabe steht das Modell.

### 4.2 Claude Pro und Claude Code (das Gehirn)

1. [claude.ai](https://claude.ai) → Konto anlegen → Upgrade auf **Pro** (später bei Bedarf **Max 5x**).
2. Training abschalten: Profil unten links → Settings → Privacy → „Help improve our AI models“ aus.
3. Claude Code installieren:
   - macOS/Linux: `curl -fsSL https://claude.ai/install.sh | bash`
   - Windows (PowerShell): `irm https://claude.ai/install.ps1 | iex`
4. Anmelden: `claude` starten (oder `/login`) und mit dem Pro-Konto bestätigen.
5. Regeln: [`advanced/claude/CLAUDE.snippet.md`](../advanced/claude/CLAUDE.snippet.md) in `~/.claude/CLAUDE.md` übernehmen.
6. Datenschutz-Hook im Modus „Gehirn“ einrichten (Abschnitt 5).

### 4.3 Google AI Pro und Antigravity-CLI (Recherche)

1. [one.google.com](https://one.google.com) → Google AI Pro abschließen.
2. Training abschalten: [myactivity.google.com/product/gemini](https://myactivity.google.com/product/gemini) → „Aktiviert“ → „Deaktivieren“.
3. CLI installieren:
   - macOS/Linux: `curl -fsSL https://antigravity.google/cli/install.sh | bash`
   - Windows (PowerShell): `irm https://antigravity.google/cli/install.ps1 | iex`
4. Anmelden: `agy` einmal starten, Browser-Anmeldung mit dem Google-Konto.
5. Recherche-Werkzeug: [`advanced/tools/gemini-research`](../advanced/tools/gemini-research) nach `~/.local/bin/` kopieren, ausführbar machen. Test: `gemini-research "Aktuelle stabile Python-Version mit Quelle" -w 40`.

### 4.4 Ollama und docling (lokal, kostenlos)

1. Ollama installieren: macOS `curl -fsSL https://ollama.com/install.sh | sh`, Windows `irm https://ollama.com/install.ps1 | iex` (oder Installer von [ollama.com](https://ollama.com)).
2. Modell laden: `ollama pull gemma4:12b` (braucht rund 8 GB Arbeitsspeicher frei).
3. docling für PDFs/DOCX/PPTX → Markdown: `uv tool install docling` (oder `pip install docling`), Aufruf `docling datei.pdf --to md`.
4. Verdichter: [`advanced/tools/lokal-zusammenfassen`](../advanced/tools/lokal-zusammenfassen) nach `~/.local/bin/`, braucht `pip install openpyxl` für Excel. Test mit einer CSV: `lokal-zusammenfassen --nur-text test.csv`.

## 5. Datenschutz technisch erzwingen

[`advanced/hooks/privacy-guard.py`](../advanced/hooks/privacy-guard.py) prüft jeden Werkzeug-Aufruf, bevor er passiert.

- In **Claude Code** mit `--brain`: sperrt Mail-, CRM- und Kalender-Werkzeuge und Kunden-Ordner, blockiert Mailadressen und IBANs in Übergaben an Gemini. Eintrag in `~/.claude/settings.json`:

```json
{ "hooks": { "PreToolUse": [ { "matcher": "*", "hooks": [
  { "type": "command", "timeout": 15, "command": "python3 ~/.claude/hooks/privacy-guard.py --brain" } ] } ] } }
```

- In **Codex** ohne `--brain` (Codex darf Kundendaten): blockiert nur Übergaben mit Personendaten an Gemini. Eintrag in `~/.codex/hooks.json`:

```json
{ "hooks": { "PreToolUse": [ { "matcher": "*", "hooks": [
  { "type": "command", "timeout": 15, "command": "python3 ~/.codex/hooks/privacy-guard.py" } ] } ] } }
```

Grenze: Namen und Konditionen im Fließtext erkennt kein Hook. Dafür stehen die Regeln in `CLAUDE.md` und `AGENTS.md`.

## 6. Token sparen: was wir gemessen haben

- **Günstiges Standardmodell, teures nur gezielt:** In Codex kostet Astra ein Mehrfaches an Credits von Sol. Sol als Standard, Astra nur für Endfassungen.
- **Denkaufwand „medium“** statt „high“ als Standard.
- **Kurze Anweisungsdateien:** Jeder Modellaufruf schickt sie mit. Bei uns startete jeder Codex-Schritt mit rund 32.000 Token, bevor gearbeitet wurde.
- **Jeder Schritt schickt den ganzen Verlauf erneut:** Erst Liste, dann gezielt öffnen; ein Thema pro Sitzung.
- **PDFs nie als Bild einlesen:** erst `docling … --to md`, dann lesen oder lokal verdichten.
- **Lokal verdichten:** Gemma 4 12B (ohne Denkmodus) fasste in unserem Test einen Vertrag und einen Mailverlauf fehlerfrei zusammen, in unter einer Minute pro Aufgabe auf einem Mac mini M4 Pro mit 24 GB.
- **Zählen nie per Sprachmodell:** Drei lokale Modelle haben 84 Tabellenzeilen auf 64 bis 89 verzählt. `lokal-zusammenfassen` zählt Tabellen per Skript und gibt dem Modell nur die exakten Zahlen.

## 7. So steuerst du das Setup

Die gleichen Sätze funktionieren in Claude und in Codex (Tabelle in [`AGENTS.example.md`](../advanced/codex/AGENTS.example.md)):

| Du sagst | Wer übernimmt |
|---|---|
| „Recherchier …“ | Gemini über `gemini-research` |
| „Fass das PDF zusammen“ | lokal: docling + `lokal-zusammenfassen` |
| „Schreib dem Kunden …“ | Codex (Endfassung `-p astra`) |
| „Plan das“, „Prüf meinen Code“ | Claude |
| „Zähl …“ | Skript |

## 8. Wann lohnt sich was?

- **Solo, Kundendaten im Spiel, knappes Budget:** Codex-Basis klein (2 Standard-Plätze) mit Claude Pro; Astra nur sparsam.
- **Codex als Arbeitstier für den ganzen Tag:** ein 100-US-$-Platz plus ein Standard-Platz, dazu Claude Pro: günstiger als Claude Max 20x, mit AVV für Kundendaten.
- **Claude Pro reicht als Gehirn nicht:** Claude Max 5x statt Pro.
- **Kleines Team, Claude soll auch Kundendaten sehen:** Claude Team statt Pro/Max.
- **Keine Kundendaten, nur eigene Projekte:** Claude Max 20x allein ist bequem, aber teurer als die Codex-Basis.
