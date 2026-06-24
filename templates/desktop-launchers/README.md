# Desktop launchers

Doppelklick-Starter für Claude Code — auf Mac und Windows.

Idee: kein Terminal aufmachen, kein Befehl tippen. Icon auf dem Desktop, einmal klicken, Claude läuft im **Skip-Permissions-Modus** (fragt nicht vor jedem Tool-Call). Nur auf eigener, vertrauter Maschine sinnvoll — auf fremder Hardware niemals.

## Mac (`start-claude.command`)

```bash
cp templates/desktop-launchers/start-claude.command ~/Desktop/
chmod +x ~/Desktop/start-claude.command
```

Erstes Mal: Rechtsklick → **Öffnen** (Gatekeeper-Warnung bestätigen). Danach reicht Doppelklick.

Variante mit fixem Projekt-Ordner:

```bash
CLAUDE_LAUNCHER_WORKDIR=/Volumes/Code/MeinProjekt ~/Desktop/start-claude.command
```

…oder die `WORKDIR`-Zeile direkt im `.command`-Skript anpassen.

## Windows (`start-claude.bat`)

```cmd
copy templates\desktop-launchers\start-claude.bat "%USERPROFILE%\Desktop\"
```

Doppelklick öffnet ein neues Command-Prompt-Fenster und startet Claude direkt.

Variante mit fixem Projekt-Ordner: setze `CLAUDE_LAUNCHER_WORKDIR` vorher oder editiere die `WORKDIR`-Zuweisung im `.bat`.

## Warum `--dangerously-skip-permissions`?

Standardmäßig fragt Claude Code vor jedem nicht-allowlisteten Bash- oder MCP-Call nach. Beim aktiven Arbeiten an eigenen Projekten frisst das Tempo. Skip-Permissions = Claude darf alles, was du selbst dürftest. Auf fremder oder geteilter Hardware: weglassen. Im CI/CD: weglassen.

Wenn du gar nicht skippen, sondern nur weniger Prompts willst, gibt es im Kit `/fewer-permission-prompts` — analysiert deine Transcripts und schreibt eine gezielte Allowlist in `~/.claude/settings.json`.

## Troubleshooting

**Mac: „Öffnen nicht möglich, weil unbekannter Entwickler".** Rechtsklick → Öffnen → Bestätigen. Einmalig.

**Mac: Fenster öffnet, aber kein Input möglich.** Veraltete Claude-Version, die beim Init hängt. Update: `claude update` im Terminal.

**Windows: Fenster blitzt auf und schließt sofort.** `claude` ist nicht auf PATH. Prüfen mit `where claude` im Command-Prompt. Falls leer: Claude Code neu installieren / PATH-Eintrag setzen.

**Beide: `command not found: claude`.** Wie oben — PATH-Problem. Auf Mac liegt `claude` meist unter `~/.local/bin/` oder `/opt/homebrew/bin/`; sicherstellen, dass das in PATH ist.
