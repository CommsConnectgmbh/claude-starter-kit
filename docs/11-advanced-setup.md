# Advanced Setup: Codex als Basis, Claude als Gehirn, Datenschutz sauber

Du nutzt das Starter-Kit und willst als Gründer oder Solo-Selbstständiger deine laufenden Kosten und den Token-Verbrauch im Blick behalten. Dieser Leitfaden zeigt dir, wie du die Arbeit auf Codex, Claude, Gemini und lokale Werkzeuge verteilst und dabei mit Kundendaten umgehst.

**Die Idee:** Du setzt jedes Modell dort ein, wo es für die Aufgabe und die Kosten passt. Kundendaten gehen nur an Dienste, mit denen ein Auftragsverarbeitungsvertrag (AVV) besteht, oder bleiben auf deinem Rechner.

Die Preisangaben haben den Stand **03.10.2026** und sind netto, sofern sie nicht ausdrücklich als brutto gekennzeichnet sind. Die Quellen stehen beim Kostenvergleich. Die Fußnote zeigt, welche Werte aus der eigenen Rechnung stammen und wie Beträge abgeleitet wurden.

## 1. Die Rollen

Codex ist deine Basis für die tägliche Arbeit. Claude übernimmt Planung und Prüfung, Gemini die Recherche und visuelle Aufgaben. Lange Inhalte kannst du lokal aufbereiten. Die Tabelle zeigt dir auch, welche Dienste in diesem Setup Kundendaten bekommen.

| Rolle | Dienst | Kosten (netto/Monat) | Bekommt Kundendaten? |
|---|---|---|---|
| **Basis:** Mails, Kunden, Texte, Routine-Code, Gegencheck | Codex über **ChatGPT Business** | ab 42 € (jährlich) bzw. 52 € (monatlich) für die Mindestzahl von 2 Standard-Plätzen; mit einem 100-US-$-Platz in der Praxis rund 130 € (siehe Abschnitt 2) | **Ja** (AVV, kein Training) |
| **Gehirn:** Planung, Architektur, schwierige Fehler, Prüfen | **Claude Pro**, bei Bedarf **Max 5x** | 18 € (15 € jährlich) bzw. 90 € | **Nein** (Verbraucher-Abo ohne AVV) |
| **Recherche und Visuelles:** Web, Doku, Video, Screenshots | **Google AI Pro** (Gemini, CLI `agy`) | 18,48 € (21,99 € brutto) | **Nein** (Verbraucher-Abo ohne AVV) |
| **Lokal:** PDFs umwandeln, lange Inhalte verdichten | **Ollama** + **docling** auf dem eigenen Rechner | 0 € | **Ja** (Daten verlassen den Rechner nicht) |

Für den Gegencheck gilt: Autor ≠ Prüfer. Was Codex schreibt, lässt du Claude prüfen; was Claude plant oder baut, prüft Codex. Dabei gelten weiterhin die Grenzen für Kundendaten aus der Tabelle.

## 2. Was kostet das, verglichen mit „alles bei Claude“?

Die Kosten hängen vor allem davon ab, welche Codex-Plätze du wählst und wie viel du mit Claude arbeitest. **Zuerst zu den Codex-Plätzen:** ChatGPT Business braucht mindestens 2 Plätze. Es gibt zwei Arten:

| Platz | Preis | Codex-Kontingent pro 5 Stunden (laut OpenAI) |
|---|---|---|
| Standard | 21 € jährlich / 26 € monatlich | wie Plus: GPT-6 Astra 5–45, GPT-6 Sol 15–150, GPT-6 Luna 350–3.000 Nachrichten |
| Business 100 US-$ | 100 US-$ (Euro-Preis auf der Seite nicht angegeben) | GPT-6 Astra voll im Kontingent enthalten, Kontingent wie Pro 5x: Astra 25–225, Sol 70–700, Luna 1.750–14.000 |

Wenn du das Kontingent aufbrauchst, kaufst du zusätzliche Credits. Für Codex als Basis über den ganzen Arbeitstag ist hier ein 100-US-$-Platz plus ein Standard-Platz vorgesehen. Das ergab bei uns rund **130 € im Monat**. Quelle: [chatgpt.com/codex/pricing](https://chatgpt.com/de-DE/codex/pricing/?type=team).

Damit ergeben sich die folgenden Kombinationen. Den Rechenweg zu den Kosten findest du in der Fußnote.[^rechenweg]

| | Einstieg: Codex-Basis klein | Empfohlen: Codex-Basis voll | Mit größerem Gehirn | Alles bei Claude |
|---|---|---|---|---|
| Zusammensetzung | 2 Standard-Plätze + Claude Pro + Google AI Pro + Ollama | 100-$-Platz + Standard-Platz + Claude Pro + Google AI Pro + Ollama | wie „voll“, aber Claude Max 5x | Claude Max 20x |
| Netto pro Monat | **88,48 €** (jährlich 75,48 €) + Credits bei Bedarf | **rund 166 €** (130 € + 18 € + 18,48 €) | **rund 238 €** | **180 €** |
| Codex-Kontingent | wie Plus | wie Pro 5x, Astra inklusive | wie Pro 5x | keines |
| Claude-Kontingent | Pro | Pro | Max 5x | Max 20x |
| AVV für Kundendaten | Codex | Codex | Codex | **keiner** |

Soll auch Claude Kundendaten sehen, kommt zum Vergleich Claude Team hinzu. Für Claude Team besteht ein AVV. Mit 1 Premium- + 1 Standard-Platz kostet es 126,27 € monatlich bzw. 108 € jährlich. Zusammen mit 2 Standard-Codex-Plätzen und Google AI Pro sind das 196,75 € monatlich bzw. 168,48 € jährlich.

[^rechenweg]: Rechenweg: Ein Standard-Platz kostet 26 € monatlich / 21 € jährlich. Die 130 € stammen aus der realen Rechnung für 1 Business-100-$-Platz + 1 Standard-Platz. Claude Pro: 18/15 €; Max 5x: 90 €; Max 20x: 180 € (200 US-$, Euro-Preis aus dem Verhältnis 100/200 $ zu 90 €). Google AI Pro: 21,99 € brutto = 18,48 € netto. Claude Team Premium: 105,23/90 €, Standard: 21,04/18 €. Die Rechnung für die größere Kombination lautet: 238 € = 130 + 90 + 18,48.

Quellen (Stand 03.10.2026): [claude.com/pricing](https://claude.com/pricing), [chatgpt.com/pricing](https://chatgpt.com/pricing), [one.google.com](https://one.google.com). Preise ändern sich. Prüfe sie vor dem Abschluss selbst.

## 3. Datenschutz: welcher Tarif darf Kundendaten sehen?

Neben dem Preis zählt, welche Daten du mit einem Dienst verarbeiten willst. Die Tabelle stellt dafür die Trainingseinstellungen und den AVV der einzelnen Tarife gegenüber.

| Tarif | Training mit deinen Daten | AVV (Art. 28 DSGVO) | Für Kundendaten |
|---|---|---|---|
| ChatGPT Business | nein (Standard) | ja, online abschließen: [Data Processing Addendum](https://openai.com/policies/data-processing-addendum/) | **ja** |
| ChatGPT Plus / Pro | ja, abschaltbar | nein | nein |
| Claude Pro / Max | ja, abschaltbar | nein | nein |
| Claude Team | nein (Standard) | ja (kommerzielle Bedingungen) | ja |
| Google AI Pro | ja („Gemini-Apps-Aktivität“), abschaltbar | nein | nein |
| Ollama lokal | entfällt | entfällt | ja |

Für das Setup mit Claude Pro/Max und Google AI Pro heißt das: Du verarbeitest Kunden- und Personendaten nur mit Codex Business oder lokal. Claude Pro/Max und Gemini gibst du Aufgaben, die sich ohne Kundendaten vollständig beschreiben lassen. Schalte das Training trotzdem überall ab. Die Einstellungen dafür folgen in Abschnitt 4.

## 4. Konten einrichten (Schritt für Schritt)

Wenn du deine Tarife gewählt hast, richtest du die Dienste nacheinander ein. Zu jedem Dienst findest du die Anmeldung, die benötigten Werkzeuge und die passenden Vorlagen aus dem Kit.

### 4.1 ChatGPT Business und Codex (die Basis)

Beginne mit deinem Business-Konto und dem AVV. Danach installierst du Codex, übernimmst die Profile und prüfst mit den Testbefehlen, welches Modell startet.

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

Als Nächstes richtest du Claude für Planung und Prüfung ein. Schalte das Training ab und übernimm die Regeln für die Arbeit ohne Kundendaten. Die Hook-Einstellungen folgen nach der Kontoeinrichtung.

1. [claude.ai](https://claude.ai) → Konto anlegen → Upgrade auf **Pro** (später bei Bedarf **Max 5x**).
2. Training abschalten: Profil unten links → Settings → Privacy → „Help improve our AI models“ aus.
3. Claude Code installieren:
   - macOS/Linux: `curl -fsSL https://claude.ai/install.sh | bash`
   - Windows (PowerShell): `irm https://claude.ai/install.ps1 | iex`
4. Anmelden: `claude` starten (oder `/login`) und mit dem Pro-Konto bestätigen.
5. Regeln: [`advanced/claude/CLAUDE.snippet.md`](../advanced/claude/CLAUDE.snippet.md) in `~/.claude/CLAUDE.md` übernehmen.
6. Datenschutz-Hook im Modus „Gehirn“ einrichten (Abschnitt 5).

### 4.3 Google AI Pro und Antigravity-CLI (Recherche)

Für Recherche und visuelle Aufgaben richtest du Google AI Pro und die Antigravity-CLI ein. Mit dem abschließenden Test rufst du das Recherche-Werkzeug auf.

1. [one.google.com](https://one.google.com) → Google AI Pro abschließen.
2. Training abschalten: [myactivity.google.com/product/gemini](https://myactivity.google.com/product/gemini) → „Aktiviert“ → „Deaktivieren“.
3. CLI installieren:
   - macOS/Linux: `curl -fsSL https://antigravity.google/cli/install.sh | bash`
   - Windows (PowerShell): `irm https://antigravity.google/cli/install.ps1 | iex`
4. Anmelden: `agy` einmal starten, Browser-Anmeldung mit dem Google-Konto.
5. Recherche-Werkzeug: [`advanced/tools/gemini-research`](../advanced/tools/gemini-research) nach `~/.local/bin/` kopieren, ausführbar machen. Test: `gemini-research "Aktuelle stabile Python-Version mit Quelle" -w 40`.

### 4.4 Ollama und docling (lokal, kostenlos)

Zum Schluss kommen die lokalen Werkzeuge dazu. Mit docling wandelst du Dokumente in Markdown um; Ollama und der Verdichter bereiten lange Inhalte auf deinem Rechner auf.

1. Ollama installieren: macOS `curl -fsSL https://ollama.com/install.sh | sh`, Windows `irm https://ollama.com/install.ps1 | iex` (oder Installer von [ollama.com](https://ollama.com)).
2. Modell laden: `ollama pull gemma4:12b` (braucht rund 8 GB Arbeitsspeicher frei).
3. docling für PDFs/DOCX/PPTX → Markdown: `uv tool install docling` (oder `pip install docling`), Aufruf `docling datei.pdf --to md`.
4. Verdichter: [`advanced/tools/lokal-zusammenfassen`](../advanced/tools/lokal-zusammenfassen) nach `~/.local/bin/`, braucht `pip install openpyxl` für Excel. Test mit einer CSV: `lokal-zusammenfassen --nur-text test.csv`.

## 5. Datenschutz technisch erzwingen

Die Regeln aus den Anweisungsdateien ergänzt du durch einen technischen Check: [`advanced/hooks/privacy-guard.py`](../advanced/hooks/privacy-guard.py) prüft jeden Werkzeug-Aufruf, bevor er ausgeführt wird. Für Claude und Codex trägst du den Hook mit unterschiedlichen Einstellungen ein.

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

Der Hook hat eine Grenze: Namen und Konditionen im Fließtext erkennt er nicht. Dafür gelten die Regeln in `CLAUDE.md` und `AGENTS.md`.

## 6. Token sparen: was wir gemessen haben

Wenn das Setup läuft, kannst du den Verbrauch an zwei Stellen beeinflussen: bei der Modellwahl und bei den Inhalten, die du dem Modell mitgibst. Die folgenden Punkte beruhen auf unseren Messungen und Tests.

- **Günstiges Standardmodell, teures nur gezielt:** In Codex kostet Astra ein Mehrfaches an Credits von Sol. Sol als Standard, Astra nur für Endfassungen.
- **Denkaufwand „medium“** statt „high“ als Standard.
- **Kurze Anweisungsdateien:** Jeder Modellaufruf schickt sie mit. Bei uns startete jeder Codex-Schritt mit rund 32.000 Token, bevor gearbeitet wurde.
- **Jeder Schritt schickt den ganzen Verlauf erneut:** Erst Liste, dann gezielt öffnen; ein Thema pro Sitzung.
- **PDFs nie als Bild einlesen:** erst `docling … --to md`, dann lesen oder lokal verdichten.
- **Lokal verdichten:** Gemma 4 12B (ohne Denkmodus) fasste in unserem Test einen Vertrag und einen Mailverlauf fehlerfrei zusammen, in unter einer Minute pro Aufgabe auf einem Mac mini M4 Pro mit 24 GB.
- **Zählen nie per Sprachmodell:** Drei lokale Modelle haben 84 Tabellenzeilen auf 64 bis 89 verzählt. `lokal-zusammenfassen` zählt Tabellen per Skript und gibt dem Modell nur die exakten Zahlen.

## 7. So steuerst du das Setup

Du kannst deine Aufgaben in Claude oder in Codex eingeben. Mit den gleichen Sätzen steuerst du, welches Werkzeug übernimmt. Die Zuordnung findest du auch in [`AGENTS.example.md`](../advanced/codex/AGENTS.example.md):

| Du sagst | Wer übernimmt |
|---|---|
| „Recherchier …“ | Gemini über `gemini-research` |
| „Fass das PDF zusammen“ | lokal: docling + `lokal-zusammenfassen` |
| „Schreib dem Kunden …“ | Codex (Endfassung `-p astra`) |
| „Plan das“, „Prüf meinen Code“ | Claude |
| „Zähl …“ | Skript |

## 8. Wann lohnt sich was?

Für deine Auswahl sind vor allem drei Fragen entscheidend: Arbeitest du mit Kundendaten, nutzt du Codex den ganzen Tag und reicht dir das Claude-Kontingent? Daraus ergeben sich die folgenden Varianten.

- **Solo, Kundendaten im Spiel, knappes Budget:** Codex-Basis klein (2 Standard-Plätze) mit Claude Pro; Astra nur sparsam.
- **Codex als Arbeitstier für den ganzen Tag:** ein 100-US-$-Platz plus ein Standard-Platz, dazu Claude Pro: günstiger als Claude Max 20x, mit AVV für Kundendaten.
- **Claude Pro reicht als Gehirn nicht:** Claude Max 5x statt Pro.
- **Kleines Team, Claude soll auch Kundendaten sehen:** Claude Team statt Pro/Max.
- **Keine Kundendaten, nur eigene Projekte:** Claude Max 20x allein ist bequem, aber teurer als die Codex-Basis.
