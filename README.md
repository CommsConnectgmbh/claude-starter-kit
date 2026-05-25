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

## 2. Den Council-Skill installieren

Wenn du eine Entscheidung treffen musst (sollte ich Feature X bauen? Plan A oder B?), bekommst du normal vage "es kommt darauf an"-Antworten.

Mit dem Council-Skill spielt Claude 5 Perspektiven durch (Visionär, Kritiker, Kreativer, Skeptiker, Logiker), benennt wo sie sich widersprechen, und gibt dir am Ende eine klare Empfehlung. Kein Rumdrucksen.

```bash
mkdir -p ~/.claude/skills/council
cp claude-starter-kit/skills/council/SKILL.md ~/.claude/skills/council/
```

Probier's: tippe in Claude Code `/council Soll ich heute Sport machen?`

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
| [`docs/03-skills-vs-agents.md`](docs/03-skills-vs-agents.md) | Wann Skills, wann Agents — die häufigste Verwechslung |
| [`agents/legal-de.md`](agents/legal-de.md) + [`agents/tax-de.md`](agents/tax-de.md) | **Echte deutsche Recht- und Steuer-Recherche-Agenten** als Praxis-Beispiel wie ein Domain-Agent aufgebaut wird (Quellenpflicht, Disclaimer, Workflow) |
| [`templates/memory/`](templates/memory/) | Beispiel wie Memory-Einträge aussehen sollten |
| [`install.sh`](install.sh) | Interaktiver Installer der alles oben auf einmal macht |

Wenn du die deutschen Agents installieren willst:
```bash
mkdir -p ~/.claude/agents
cp agents/legal-de.md agents/tax-de.md ~/.claude/agents/
```

---

## Lizenz

MIT. Mach damit was du willst. Bug oder Verbesserung? Issue oder PR.
