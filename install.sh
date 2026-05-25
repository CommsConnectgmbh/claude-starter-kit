#!/usr/bin/env bash
#
# install.sh — installs the council skill and (optionally) the German legal+tax agents.
#
# Run from inside a clone of this repo:
#   ./install.sh
#
# Nothing is overwritten without showing you a diff first. Nothing in your
# ~/.claude/ is touched without an explicit y/n prompt.

set -euo pipefail

CLAUDE_DIR="${CLAUDE_DIR:-$HOME/.claude}"
SRC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [[ -t 1 ]]; then
  GREEN=$'\033[0;32m'; CYAN=$'\033[0;36m'; BOLD=$'\033[1m'; RESET=$'\033[0m'
else
  GREEN=""; CYAN=""; BOLD=""; RESET=""
fi

say()  { printf "%s\n" "$*"; }
head() { printf "\n%s%s%s\n" "$BOLD" "$*" "$RESET"; }
ok()   { printf "  %s✓%s %s\n" "$GREEN" "$RESET" "$*"; }
ask()  { printf "%s?%s %s [y/N] " "$CYAN" "$RESET" "$*"; read -r r; [[ "$r" =~ ^[Yy]$ ]]; }

[[ -d "$CLAUDE_DIR" ]] || mkdir -p "$CLAUDE_DIR"

head "1. Council skill (universal — recommended)"
say "  Adds /council — 5-perspective decision helper."
if ask "  Install?"; then
  mkdir -p "$CLAUDE_DIR/skills/council"
  if [[ -f "$CLAUDE_DIR/skills/council/SKILL.md" ]]; then
    diff "$CLAUDE_DIR/skills/council/SKILL.md" "$SRC_DIR/skills/council/SKILL.md" || true
    ask "  Overwrite existing?" || { say "  Skipped."; SKIP_COUNCIL=1; }
  fi
  if [[ -z "${SKIP_COUNCIL:-}" ]]; then
    cp "$SRC_DIR/skills/council/SKILL.md" "$CLAUDE_DIR/skills/council/"
    ok "Installed. Try: /council Should I ship feature X?"
  fi
fi

head "2. German legal + tax research agents (only if you need them)"
say "  Adds legal-de + tax-de agents. Mandatory source citation, statutory disclaimers."
say "  Skip this if you don't work with German law."
if ask "  Install?"; then
  mkdir -p "$CLAUDE_DIR/agents"
  for a in legal-de tax-de; do
    if [[ -f "$CLAUDE_DIR/agents/$a.md" ]]; then
      diff "$CLAUDE_DIR/agents/$a.md" "$SRC_DIR/agents/$a.md" || true
      ask "  Overwrite $a.md?" || continue
    fi
    cp "$SRC_DIR/agents/$a.md" "$CLAUDE_DIR/agents/"
    ok "Installed agent: $a"
  done
fi

head "3. settings.json template (only if you don't have one yet)"
if [[ -f "$CLAUDE_DIR/settings.json" ]]; then
  say "  You already have a settings.json. Not touching it. Diff against template:"
  diff "$CLAUDE_DIR/settings.json" "$SRC_DIR/settings.example.json" || true
elif ask "  Install fresh settings.json from template?"; then
  cp "$SRC_DIR/settings.example.json" "$CLAUDE_DIR/settings.json"
  ok "Installed settings.json with defaultMode = 'default' (safe choice)."
fi

head "Manual steps"
say "  → Drop templates/CLAUDE.example.md into your project root as CLAUDE.md."
say "  → Read docs/02-memory-system.md to understand auto-memory."
say "  → Star the repo if it helped: https://github.com/CommsConnectgmbh/claude-starter-kit"
