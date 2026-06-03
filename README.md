# claude-starter-kit

**Du hast gerade [Claude Code](https://docs.claude.com/en/docs/claude-code) installiert. Was jetzt?**

Mach diese drei Sachen und du hast ein gutes Setup. Zehn Minuten.

---

## 1. Eine CLAUDE.md in dein Projekt legen

`CLAUDE.md` ist eine kleine Datei im Wurzelverzeichnis deines Projekts. Claude liest sie bei jeder Anfrage automatisch. Da rein gehört: was das Projekt ist, welche Befehle es gibt (`npm run dev`, `pytest`, etc.), und was Claude NICHT tun soll.

```bash
git clone https://github.com/CommsConnectgmbh/claude-starter-kit.git
cd dein-projekt
cp ../claude-starter-kit/templates/CLAUDE.example.md CLAUDE.md
```

Dann öffne `CLAUDE.md` und fülle die Lücken (5 Minuten). Spar dir das in Zukunft, in jeder Conversation zu wiederholen.

---

## 2. Die Core-Skills installieren (ein Befehl)

```bash
cd claude-starter-kit
./install.sh            # interaktiv — zeigt Diffs bevor was überschrieben wird
# oder komplett ohne Rückfragen:
./install.sh --yes
```

Das installiert vier Skills + (auf Wunsch) die deutschen Recht/Steuer-Agents + ein sicheres `settings.json`-Template. Frische Maschine? Läuft sofort durch, nichts zu überschreiben.

| Skill | Wofür |
|---|---|
| `council` | Entscheidung anstehend (Feature X bauen? Plan A oder B?)? Claude spielt 5 Perspektiven durch (Visionär, Kritiker, Kreativer, Skeptiker, Logiker), benennt die Widersprüche, gibt eine klare Empfehlung. Kein Rumdrucksen. |
| `scrape` | Read-only Daten von einer Webseite als sauberes JSON ziehen. |
| `skillify` | Einen erfolgreichen `/scrape` als wiederverwendbares Skript ablegen — beim nächsten Mal instant. |
| `canary` | Nach dem Deploy die Live-URL überwachen und nur bei echten Regressionen alarmieren (relativ zur Baseline, nicht absolut). |

Probier's: tippe in Claude Code `/council Soll ich heute Sport machen?`

> Brauchst du nur einzelne? `cp skills/<name>/SKILL.md ~/.claude/skills/<name>/` reicht.

---

## 3. Auto-Memory verstehen (5 Min lesen, kein Install)

Claude Code merkt sich automatisch Sachen über dich zwischen Conversations — wer du bist, wie du arbeitest, was deine Projekte sind. Das ist die unterschätzte Killer-Funktion.

Lies kurz [`docs/02-memory-system.md`](docs/02-memory-system.md). Dann in deiner nächsten Conversation einfach Claude sagen: "Ich bin <Rolle>, arbeite hauptsächlich an <Projekt>, bevorzuge <Stil>." Es legt das automatisch ab und benutzt es ab dann immer.

---

**Das war's. Du bist startklar.**

---

## Was noch im Repo liegt (optional)

| Was | Wofür |
|---|---|
| [`docs/01-getting-started.md`](docs/01-getting-started.md) | Das mentale Modell hinter Claude Code (Settings vs CLAUDE.md vs Memory vs Skills vs Agents) |
| [`docs/04-the-daily-loop.md`](docs/04-the-daily-loop.md) | **Wie du Claude durch echte Aufgaben fährst** — explore → plan → code → commit, Kontext-Disziplin, Verifizierung, Session-Übergabe |
| [`docs/03-skills-vs-agents.md`](docs/03-skills-vs-agents.md) | Wann Skills, wann Agents — die häufigste Verwechslung |
| [`agents/legal-de.md`](agents/legal-de.md) + [`agents/tax-de.md`](agents/tax-de.md) | **Echte deutsche Recht- und Steuer-Recherche-Agenten** als Praxis-Beispiel wie ein Domain-Agent aufgebaut wird (Quellenpflicht, Disclaimer, Workflow) |
| [`templates/memory/`](templates/memory/) | Beispiel wie Memory-Einträge aussehen sollten |
| [`install.sh`](install.sh) | One-Command-Installer für alles oben (`--yes`, `--with-pro`, `--no-agents`) |
| [`pro/skills/`](pro/skills/) | **Optionaler Pro-Layer**: `autoplan`, `spec` (gebundelt) + 5 obra-Skills (geklont) |

Wenn du die deutschen Agents einzeln installieren willst:
```bash
mkdir -p ~/.claude/agents
cp agents/legal-de.md agents/tax-de.md ~/.claude/agents/
```

---

## Pro-Layer (optional)

Schwerere Workflow-Skills, opt-in:

```bash
./install.sh --with-pro      # Core + Pro in einem
# oder nur Pro:
cd pro/skills && ./install-pro-skills.sh
```

- **Gebundelt** (gstack, MIT): `autoplan` (Plan durch Multi-Lens-Review jagen), `spec` (vage Idee → ausführbare Spec).
- **Geklont** (obra/superpowers, MIT): `when-stuck`, `root-cause-tracing`, `inversion-exercise`, `dispatching-parallel-agents`, `subagent-driven-development`.

`autoplan`/`spec` rufen optionale Companion-Skills (Frontend-Design, ein unabhängiger Reviewer) — fehlen die, wird die Phase sauber übersprungen. Details: [`pro/skills/README.md`](pro/skills/README.md).

Außerdem im Pro-Layer: [`pro/dreaming/`](pro/dreaming/) — ein nächtlicher Memory-Curator, der deine Auto-Memory dedupliziert, veraltete Einträge findet und den Index synchron hält (launchd/cron-Template inklusive).

---

## Lizenz

MIT. Mach damit was du willst. Bug oder Verbesserung? Issue oder PR.
