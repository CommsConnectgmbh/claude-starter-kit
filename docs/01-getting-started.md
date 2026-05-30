# Das mentale Modell

Bevor du tiefer einsteigst, lerne diese 4 Begriffe. Anfänger verwechseln sie ständig.

| Begriff | Wo es lebt | Was es macht | Wann es greift |
|---|---|---|---|
| **CLAUDE.md** | Im Wurzelverzeichnis deines Projekts | Projekt-spezifische Regeln (Stack, Konventionen, "mach nicht X") | Jeder Turn — Claude liest die Datei automatisch |
| **Auto-Memory** | `~/.claude/projects/.../memory/` | Sachen die zwischen Conversations bestehen sollen (wer du bist, deine Präferenzen) | Claude schreibt + liest automatisch |
| **Skills** | `~/.claude/skills/<name>/SKILL.md` | Wiederverwendbare Workflows (`/council`, `/verify`, etc.) | Wenn du den Slash-Command tippst oder wenn die Description matched |
| **Agents** | `~/.claude/agents/<name>.md` | Spezialisierte Sub-Claudes mit eigenem System-Prompt und eigener Tool-Auswahl | Wenn die Description zur Frage passt — Claude delegiert |

Plus eine fünfte Sache:

| Begriff | Wo es lebt | Was es macht |
|---|---|---|
| **settings.json** | `~/.claude/settings.json` | Konfiguriert die Runtime (Theme, Permission-Mode, Plugins) — nicht das Verhalten |

## Was wann benutzen

**Du arbeitest neu an einem Projekt** → schreib eine `CLAUDE.md`. Schon nach 5 Minuten Pflege spart sie dir später Stunden.

**Du erklärst Claude was über dich** → das landet automatisch in Memory. Du musst nichts manuell tun. Wenn du was korrigieren willst: einfach sagen "vergiss X", "X war falsch, richtig ist Y".

**Du machst regelmäßig dieselbe Art Aufgabe** → das ist ein Skill-Kandidat. Beispiel: jedes Mal wenn du eine PR review willst, machst du dieselben 4 Schritte. Schreib ein `code-review` Skill.

**Du brauchst einen Experten für ein Fachgebiet** → das ist ein Agent. Beispiel: Steuerrecht-Recherche braucht andere Tools (WebFetch ja, Bash nein) und einen ganz anderen System-Prompt (Quellenpflicht, Disclaimer). Das gehört nicht in den Haupt-Claude rein.

## Was NICHT memory ist

Memory ist nicht für:
- Code-Konventionen — die gehören in `CLAUDE.md`
- Bug-Fix-Rezepte — der Fix ist im Code, der Commit-Message hat den Kontext
- Aktuelle Aufgaben — die sind ephemer
- Sachen die aus `git log` ablesbar sind

Wenn dein Memory-Ordner mit Müll volläuft, hast du wahrscheinlich Sachen drin die in `CLAUDE.md` gehören.

## Permission-Modi (settings.json)

| Mode | Was es macht | Wann benutzen |
|---|---|---|
| `default` | Fragt bei jedem Shell-Befehl | Anfang — bis du Claude vertraust |
| `acceptEdits` | Auto-allow für Datei-Edits, fragt bei Shell | Wenn du in einem Repo arbeitest und schnell iterieren willst |
| `plan` | Read-only, keine Änderungen | Wenn du nur planen oder lesen willst |
| `bypassPermissions` | Alles auto-allow | Nur in einem Wegwerf-Env oder wenn du wirklich weißt was du tust |

Standard im `settings.example.json` dieses Repos ist `default`. Sicher für den Start.

## Was als nächstes lesen

- [`02-memory-system.md`](02-memory-system.md) — Wie Memory wirklich funktioniert, was reinkommen soll und was nicht
- [`03-skills-vs-agents.md`](03-skills-vs-agents.md) — Die 2-Minuten-Faustregel wann was
- [`04-the-daily-loop.md`](04-the-daily-loop.md) — Der tägliche Arbeits-Loop: explore → plan → code → commit, Kontext-Disziplin, Verifizierung
