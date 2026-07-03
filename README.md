# claude-starter-kit

Claude Code Starter-Kit auf Deutsch — Skills, Agents, CLAUDE.md-Vorlagen und ein 10-Minuten-Setup für alle, die gerade mit Claude Code anfangen.
Für deutsche Entwickler und Gründer, die [Claude Code](https://docs.claude.com/en/docs/claude-code) frisch installiert haben und ein gutes Setup wollen, ohne sich durch die Doku zu wühlen.

*A German-language starter kit for Claude Code: skills, agents, CLAUDE.md templates, and a 10-minute setup.*

[![CI](https://github.com/CommsConnectgmbh/claude-starter-kit/actions/workflows/ci.yml/badge.svg)](https://github.com/CommsConnectgmbh/claude-starter-kit/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/CommsConnectgmbh/claude-starter-kit?style=social)](https://github.com/CommsConnectgmbh/claude-starter-kit/stargazers)

---

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
| [`docs/05-self-healing-apps.md`](docs/05-self-healing-apps.md) | **Apps, die sich aus ihrer Nutzung selbst reparieren** — synthetischer Nutzer + Fix-Agent, nächtlich, mit harten Sicherheits-Leitplanken |
| [`docs/06-linear-issues.md`](docs/06-linear-issues.md) | **Claude an einen Issue-Tracker (Linear) hängen** — Funde sicher ablegen statt unbeaufsichtigt fixen; das Gating-Pattern |
| [`docs/07-mcps.md`](docs/07-mcps.md) | **MCP-Übersicht** — die kuratierte Shortlist (Linear, Sentry, Supabase), Setup mit einer Zeile, Pairing mit Self-Heal |
| [`docs/08-third-party-accounts.md`](docs/08-third-party-accounts.md) | **Welche Drittanbieter-Accounts du wofür brauchst** — Sign-up-Links, Free-Tier-Status, was das Kit minimal vs erweitert braucht |
| [`agents/legal-de.md`](agents/legal-de.md) + [`agents/tax-de.md`](agents/tax-de.md) | **Echte deutsche Recht- und Steuer-Recherche-Agenten** als Praxis-Beispiel wie ein Domain-Agent aufgebaut wird (Quellenpflicht, Disclaimer, Workflow) |
| [`templates/memory/`](templates/memory/) | Beispiel wie Memory-Einträge aussehen sollten |
| [`templates/desktop-launchers/`](templates/desktop-launchers/) | **Doppelklick-Starter** für Mac (`.command`) + Windows (`.bat`) — Claude direkt im Skip-Permissions-Modus |
| [`install.sh`](install.sh) | One-Command-Installer für alles oben (`--yes`, `--with-pro`, `--no-agents`, `--with-launcher`) |
| [`pro/skills/`](pro/skills/) | **Optionaler Pro-Layer**: 6 Skills gebundelt (`autoplan`, `spec`, `second-opinion`, `compliance`, `fal-ai`, `openai-image`) + 5 obra-Skills geklont |
| [`pro/self-heal/`](pro/self-heal/) | **Lauffähiges Self-Healing**: synthetischer Playwright-Nutzer + Fix-PR-Agent + launchd/cron-Template |

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

- **Gebundelt** (in diesem Repo, MIT):
  - `autoplan`, `spec` (gstack-derived) — Plan durch Multi-Lens-Review; vage Idee → ausführbare Spec
  - `second-opinion` — kostenloser lokaler Code-Reviewer via Ollama (Codex-Plugin-Ersatz)
  - `compliance` — Quartals-Audit-Pattern (Aikido + Supabase Advisors + Prowler)
  - `fal-ai`, `openai-image` — direkter API-Zugriff für Marketing-Creative (BYO Key)
- **Geklont** (obra/superpowers, MIT): `when-stuck`, `root-cause-tracing`, `inversion-exercise`, `dispatching-parallel-agents`, `subagent-driven-development`.

`autoplan`/`spec` rufen optionale Companion-Skills (Frontend-Design, ein unabhängiger Reviewer = `second-opinion`) — fehlen die, wird die Phase sauber übersprungen. Details: [`pro/skills/README.md`](pro/skills/README.md).

Außerdem im Pro-Layer: [`pro/dreaming/`](pro/dreaming/) — ein nächtlicher Memory-Curator, der deine Auto-Memory dedupliziert, veraltete Einträge findet und den Index synchron hält (launchd/cron-Template inklusive).

---

## Self-Healing: Apps, die sich aus ihrer Nutzung reparieren (optional)

Ein nächtlicher Loop, der echte Bugs in deinen Apps findet und Fix-PRs aufmacht — **ohne dass ein einziger echter Nutzer nötig ist**, und mit Leitplanken, die verhindern, dass etwas unbeaufsichtigt live geht.

```
  synthetischer Nutzer   →   Fehler-Erfassung      →   Fix-Agent
  (klickt Happy-Paths)       (Monitor + run.mjs)       (Claude Code → PR)
```

- **Bau keinen schlechteren Sentry.** Für echten Traffic: einen echten Error-Monitor einbinden.
- **Der eigentliche Hebel ist der synthetische Nutzer** — Playwright klickt jede Nacht die Hauptflows durch, fängt Console-/Page-Errors, fehlgeschlagene Requests, HTTP-5xx.
- **Der Fix-Agent gehört dir:** Dry-Run per Default, gedeckelt pro Lauf, **öffnet PRs, mergt nie**, sensible Repos (echte Kunden/Billing) sind **issue-only**.

Setup in [`pro/self-heal/README.md`](pro/self-heal/README.md), das Warum in [`docs/05-self-healing-apps.md`](docs/05-self-healing-apps.md).

```bash
cd pro/self-heal && npm install && npx playwright install chromium
node synthetic/run.mjs            # Funde nach synthetic/reports/
node agent/fix.mjs                # DRY-RUN — zeigt nur, was es fixen würde
```

---

## MCPs: Claude an deine echten Tools anbinden (optional)

[MCPs (Model Context Protocol servers)](https://modelcontextprotocol.io) sind, wie Claude Code mit Außenwelt spricht — Issue-Tracker, Error-Monitor, DB, CRM. Die kuratierte Shortlist, die zum Rest des Kits passt:

```bash
claude mcp add --transport sse  linear   https://mcp.linear.app/sse      # safe landing für „found, don't fix yet"
claude mcp add --transport http sentry   https://mcp.sentry.dev/mcp      # echter Error-Monitor für Self-Heal
claude mcp add --transport http supabase https://mcp.supabase.com/mcp    # Schema/SQL/Logs, falls dein Stack Supabase ist
```

OAuth beim ersten Call, kein API-Key in `.env`. Nur die hinzufügen, die zum Stack passen. Details + Gating-Pattern: [`docs/07-mcps.md`](docs/07-mcps.md) + [`docs/06-linear-issues.md`](docs/06-linear-issues.md).

---

## Desktop-Launcher: Doppelklick statt Terminal (optional)

Keine Lust, jedes Mal ein Terminal aufzumachen? Im Kit liegt für beide Welten ein Doppelklick-Starter, der Claude direkt im Skip-Permissions-Modus startet (kein Nachfragen vor jedem Tool-Call — nur auf eigener, vertrauter Maschine sinnvoll).

**Mac:**
```bash
./install.sh --with-launcher
# legt ~/Desktop/start-claude.command an, ausführbar, fertig.
```

**Windows:**
```cmd
copy templates\desktop-launchers\start-claude.bat "%USERPROFILE%\Desktop\"
```

Details + Troubleshooting: [`templates/desktop-launchers/README.md`](templates/desktop-launchers/README.md).

---

## Lizenz

MIT. Mach damit was du willst. Bug oder Verbesserung? Issue oder PR.

---

Gebaut von [Rainer Roloff](https://rainerroloff.de) — mehr Projekte rund um Claude Code und ein „Schreib mir" auf [rainerroloff.de](https://rainerroloff.de).
