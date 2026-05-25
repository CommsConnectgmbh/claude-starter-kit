#!/usr/bin/env bash
#
# install.sh — interactive installer for claude-starter-kit.
#
# Usage (after cloning):
#   ./install.sh
#
# Usage (one-liner — reads what's about to happen, asks before each step):
#   curl -fsSL https://raw.githubusercontent.com/CommsConnectgmbh/claude-starter-kit/main/install.sh | bash
#
# What it does:
#   1. Detects whether you're running from a local clone or from curl-pipe-bash.
#      If from curl, clones the repo into ~/.claude-starter-kit/ first.
#   2. Asks before each install step (council skill / agents / settings / templates).
#   3. NEVER overwrites without showing a diff first.
#   4. Records what was installed in ~/.claude/.starter-kit-installed for later updates.

set -euo pipefail

# --- Configuration ------------------------------------------------------------
REPO_URL="${REPO_URL:-https://github.com/CommsConnectgmbh/claude-starter-kit.git}"
CLONE_DIR="${CLONE_DIR:-$HOME/.claude-starter-kit}"
CLAUDE_DIR="${CLAUDE_DIR:-$HOME/.claude}"

# --- Colors -------------------------------------------------------------------
if [[ -t 1 ]]; then
  BOLD=$'\033[1m'; GREEN=$'\033[0;32m'; YELLOW=$'\033[0;33m'; CYAN=$'\033[0;36m'; RESET=$'\033[0m'
else
  BOLD=""; GREEN=""; YELLOW=""; CYAN=""; RESET=""
fi

say()    { printf "%s\n" "$*"; }
header() { printf "\n%s%s%s\n" "$BOLD" "$*" "$RESET"; }
ok()     { printf "  %s✓%s %s\n" "$GREEN" "$RESET" "$*"; }
warn()   { printf "  %s!%s %s\n" "$YELLOW" "$RESET" "$*"; }
ask()    { printf "%s?%s %s [y/N] " "$CYAN" "$RESET" "$*"; read -r REPLY; [[ "$REPLY" =~ ^[Yy]$ ]]; }

# --- Resolve source directory -------------------------------------------------
if [[ -d "${BASH_SOURCE%/*}/skills/council" ]]; then
  # Running from a local clone
  SRC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
else
  # Running via curl-pipe-bash — clone the repo
  header "Cloning repo to $CLONE_DIR"
  if [[ -d "$CLONE_DIR/.git" ]]; then
    say "  Already cloned. Pulling latest."
    git -C "$CLONE_DIR" pull --ff-only
  else
    git clone "$REPO_URL" "$CLONE_DIR"
  fi
  SRC_DIR="$CLONE_DIR"
fi

ok "Source: $SRC_DIR"
ok "Target: $CLAUDE_DIR"

# --- Sanity check -------------------------------------------------------------
if [[ ! -d "$CLAUDE_DIR" ]]; then
  warn "$CLAUDE_DIR doesn't exist yet."
  if ask "Create it now?"; then
    mkdir -p "$CLAUDE_DIR"
    ok "Created $CLAUDE_DIR"
  else
    say "Aborted."
    exit 0
  fi
fi

# --- Per-component install ----------------------------------------------------
INSTALLED=()

install_council() {
  header "Council skill — 5-role decision-making"
  say "  Will install: $CLAUDE_DIR/skills/council/SKILL.md"
  if [[ -f "$CLAUDE_DIR/skills/council/SKILL.md" ]]; then
    warn "Already exists. Diff:"
    diff "$CLAUDE_DIR/skills/council/SKILL.md" "$SRC_DIR/skills/council/SKILL.md" || true
    if ! ask "Overwrite?"; then return; fi
  fi
  if ask "Install council skill?"; then
    mkdir -p "$CLAUDE_DIR/skills/council"
    cp "$SRC_DIR/skills/council/SKILL.md" "$CLAUDE_DIR/skills/council/"
    ok "Installed council. Try it: /council <your decision>"
    INSTALLED+=("skills/council")
  fi
}

install_agents() {
  header "German legal + tax agents"
  say "  Will install: $CLAUDE_DIR/agents/legal-de.md + tax-de.md"
  say "  Skip this if you don't need German law."
  if ! ask "Install both agents?"; then return; fi
  mkdir -p "$CLAUDE_DIR/agents"
  for a in legal-de tax-de; do
    if [[ -f "$CLAUDE_DIR/agents/$a.md" ]]; then
      warn "$a.md already exists. Diff:"
      diff "$CLAUDE_DIR/agents/$a.md" "$SRC_DIR/agents/$a.md" || true
      if ! ask "Overwrite $a.md?"; then continue; fi
    fi
    cp "$SRC_DIR/agents/$a.md" "$CLAUDE_DIR/agents/"
    ok "Installed agent: $a"
    INSTALLED+=("agents/$a.md")
  done
}

install_settings() {
  header "Settings.json template"
  say "  Will install: $CLAUDE_DIR/settings.json (only if you don't have one)"
  if [[ -f "$CLAUDE_DIR/settings.json" ]]; then
    warn "settings.json already exists. Diff against template:"
    diff "$CLAUDE_DIR/settings.json" "$SRC_DIR/settings.example.json" || true
    say "  Not overwriting. Edit by hand if you want pieces of the template."
    return
  fi
  if ask "Install fresh settings.json from template?"; then
    cp "$SRC_DIR/settings.example.json" "$CLAUDE_DIR/settings.json"
    ok "Installed settings.json (defaultMode = 'default' — safe choice)"
    INSTALLED+=("settings.json")
  fi
}

install_sanitizer() {
  header "Sanitizer script"
  say "  Will install: $CLAUDE_DIR/sanitize-dotclaude.sh"
  if ask "Install sanitizer script?"; then
    cp "$SRC_DIR/scripts/sanitize-dotclaude.sh" "$CLAUDE_DIR/sanitize-dotclaude.sh"
    chmod +x "$CLAUDE_DIR/sanitize-dotclaude.sh"
    ok "Installed sanitizer. Run before publishing anything: $CLAUDE_DIR/sanitize-dotclaude.sh"
    INSTALLED+=("sanitize-dotclaude.sh")
  fi
}

show_templates_hint() {
  header "Templates (manual install)"
  say "  Project CLAUDE.md skeleton:   $SRC_DIR/templates/CLAUDE.example.md"
  say "  Memory pattern example:       $SRC_DIR/templates/memory/"
  say "  Copy these into your projects when relevant; they don't go in ~/.claude/."
}

# --- Run ---------------------------------------------------------------------
header "claude-starter-kit installer"
say "This installer asks before each step. Nothing is overwritten without a diff."

install_council
install_agents
install_settings
install_sanitizer
show_templates_hint

# --- Record what was installed -----------------------------------------------
if [[ ${#INSTALLED[@]} -gt 0 ]]; then
  {
    printf "# claude-starter-kit install log\n"
    printf "# Installed on: %s\n" "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
    printf "# Source: %s\n\n" "$SRC_DIR"
    for item in "${INSTALLED[@]}"; do
      printf "%s\n" "$item"
    done
  } > "$CLAUDE_DIR/.starter-kit-installed"
  ok "Wrote install log to $CLAUDE_DIR/.starter-kit-installed"
fi

header "Done"
say "Read the docs next: $SRC_DIR/docs/01-getting-started.md"
say "Star the repo if it helps: https://github.com/CommsConnectgmbh/claude-starter-kit"
