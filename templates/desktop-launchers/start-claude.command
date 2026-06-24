#!/usr/bin/env bash
#
# start-claude.command — double-clickable Mac Desktop launcher for Claude Code.
#
# What it does:
#   - Opens in your home directory (so Claude can navigate from a sane root).
#   - Starts the claude CLI with --dangerously-skip-permissions, so you don't
#     get asked before every tool call. Only do this on a machine you trust.
#
# Install:
#   1) cp templates/desktop-launchers/start-claude.command ~/Desktop/
#   2) chmod +x ~/Desktop/start-claude.command
#   3) Double-click it. (First time: right-click → Open to bypass Gatekeeper.)
#
# Tip: change WORKDIR below if you want it to land in a specific project dir.

set -u

WORKDIR="${CLAUDE_LAUNCHER_WORKDIR:-$HOME}"

if ! command -v claude >/dev/null 2>&1; then
  echo "Error: 'claude' is not on PATH."
  echo "Install Claude Code first: https://docs.claude.com/en/docs/claude-code"
  echo
  read -r -p "Press Enter to close..." _
  exit 1
fi

cd "$WORKDIR" || { echo "Cannot cd into $WORKDIR"; exit 1; }
exec claude --dangerously-skip-permissions
