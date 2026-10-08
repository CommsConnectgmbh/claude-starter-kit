# Desktop launchers

Double-click launchers for Claude Code on Mac and Windows.

The idea: no terminal to open, no command to type. Put the icon on your desktop, double-click it, and Claude starts in **skip-permissions mode** (without asking before every tool call). Use this only on a machine you own and trust, never on someone else's hardware.

## Mac (`start-claude.command`)

```bash
cp templates/desktop-launchers/start-claude.command ~/Desktop/
chmod +x ~/Desktop/start-claude.command
```

The first time, right-click → **Open** and confirm the Gatekeeper warning. After that, double-clicking is enough.

To use a fixed project folder:

```bash
CLAUDE_LAUNCHER_WORKDIR=~/projekte/mein-projekt ~/Desktop/start-claude.command
```

Or edit the `WORKDIR` line directly in the `.command` script.

## Windows (`start-claude.bat`)

```cmd
copy templates\desktop-launchers\start-claude.bat "%USERPROFILE%\Desktop\"
```

Double-clicking opens a new Command Prompt window and starts Claude directly.

To use a fixed project folder, set `CLAUDE_LAUNCHER_WORKDIR` beforehand or edit the `WORKDIR` assignment in the `.bat` file.

## Why `--dangerously-skip-permissions`?

By default, Claude Code asks before every Bash or MCP call that is not on the allowlist. That slows down active work on your own projects. Skip-permissions mode lets Claude do anything you could do yourself. Leave it off on someone else's hardware, shared machines, and in CI/CD.

If you want fewer prompts without skipping permissions entirely, the kit includes `/fewer-permission-prompts`. It analyzes your transcripts and writes a targeted allowlist to `~/.claude/settings.json`.

## Troubleshooting

**Mac: cannot open the app because the developer is unidentified.** Right-click → Open → confirm. You only need to do this once.

**Mac: the window opens, but you cannot type.** An outdated Claude version may hang during initialization. Run `claude update` in a terminal.

**Windows: the window flashes and closes immediately.** `claude` is not on PATH. Run `where claude` in Command Prompt. If it returns nothing, reinstall Claude Code or add it to PATH.

**Both: `command not found: claude`.** This is also a PATH issue. On Mac, `claude` is usually under `~/.local/bin/` or `/opt/homebrew/bin/`; make sure that directory is on PATH.
