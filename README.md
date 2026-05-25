# claude-starter-kit

**Drei Sachen installieren. Fertig. Du hast ein gutes Claude-Code-Setup.**

Du brauchst: [Claude Code](https://docs.claude.com/en/docs/claude-code) installiert, ein Terminal.

```bash
git clone https://github.com/CommsConnectgmbh/claude-starter-kit.git
cd claude-starter-kit
```

---

## 1. Das Entscheidungs-Skill installieren

Lass Claude bei strategischen Entscheidungen **5 Perspektiven** durchspielen (Visionär, Kritiker, Kreativer, Skeptiker, Logiker) — und am Ende eine klare Empfehlung geben statt "es kommt drauf an".

```bash
mkdir -p ~/.claude/skills/council
cp skills/council/SKILL.md ~/.claude/skills/council/
```

Benutzung: tippe in Claude Code `/council Soll ich Feature X bauen?`

---

## 2. Die deutschen Recht- und Steuer-Agenten installieren

Zwei Recherche-Agenten mit Pflicht-Quellenzitaten (BGB / DSGVO / UWG / EStG / UStG / KStG …) und vorgeschriebenem Disclaimer (§ 2 RDG / § 2 StBerG). Sie schreiben keine Verträge und füllen keine Steuererklärungen aus — sie recherchieren, du gehst zum RA/StB.

```bash
mkdir -p ~/.claude/agents
cp agents/legal-de.md agents/tax-de.md ~/.claude/agents/
```

**Skip diesen Schritt** wenn du kein deutsches Recht / Steuern brauchst.

Benutzung: frag einfach was zu DSGVO oder Lohnsteuer — Claude erkennt das Thema und holt sich automatisch den passenden Agenten.

---

## 3. Die CLAUDE.md-Vorlage in dein Projekt legen

Jedes Projekt sollte eine `CLAUDE.md` im Root haben — kurze Regeln die Claude bei jedem Turn ließt (Tech-Stack, Konventionen, "mach NICHT X"). Sonst erklärst du das in jeder Conversation neu.

```bash
cp templates/CLAUDE.example.md /pfad/zu/deinem/projekt/CLAUDE.md
# dann öffnen und mit deinen Sachen ausfüllen (5 Minuten)
```

---

**Das war's. Du bist startklar.**

Tipp: Erste Conversation in einem neuen Projekt — sag Claude wer du bist, was du machst, wie du arbeiten willst. Es speichert das in `~/.claude/projects/.../memory/` und weiß es ab dann immer. Das ist die unterschätzteste Feature von Claude Code.

---

## Optional, wenn du tiefer willst

| Was | Wo |
|---|---|
| Erklärung was Skills / Agents / Memory / CLAUDE.md unterscheidet | [`docs/03-skills-vs-agents.md`](docs/03-skills-vs-agents.md) |
| Wie Auto-Memory funktioniert und was du NICHT speichern sollst | [`docs/02-memory-system.md`](docs/02-memory-system.md) |
| Naming-Konventionen für eigene Skills/Agents/Memory | [`docs/05-naming-conventions.md`](docs/05-naming-conventions.md) |
| Welche fremden Skills es lohnt zu installieren (obra, Anthropic) | [`docs/04-recommended-third-party.md`](docs/04-recommended-third-party.md) |
| Beispiel: `/council` in echtem Einsatz | [`examples/council-publish-decision.md`](examples/council-publish-decision.md) |
| Du willst dein eigenes `~/.claude/` veröffentlichen? Erst diesen Sanitizer drüberlaufen lassen | [`scripts/sanitize-dotclaude.sh`](scripts/sanitize-dotclaude.sh) |
| Warum dieses Repo überhaupt existiert | [`STORY.md`](STORY.md) |

---

## Lizenz

MIT. Mach damit was du willst. Pull-Requests willkommen.

Wenn dir das Setup eine Stunde gespart hat, gib dem Repo einen Stern.
