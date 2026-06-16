#!/usr/bin/env bash
#
# install.sh — one command to install the core starter kit:
#   skills: council, scrape, skillify, canary
#   agents: legal-de, tax-de   (German legal/tax research — opt-out)
#   settings.json template     (only if you don't have one yet)
#
# Run from inside a clone of this repo:
#   ./install.sh                 # interactive — diffs before overwriting
#   ./install.sh --yes           # non-interactive — installs everything, auto-overwrites
#   ./install.sh --with-pro      # also run pro/skills/install-pro-skills.sh
#   ./install.sh --no-agents     # skip the German legal/tax agents
#
# Nothing in your ~/.claude/ is overwritten without a diff (unless --yes).

set -euo pipefail

CLAUDE_DIR="${CLAUDE_DIR:-$HOME/.claude}"
SRC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

ASSUME_YES=""; WITH_PRO=""; NO_AGENTS=""
for arg in "$@"; do
  case "$arg" in
    --yes|-y)    ASSUME_YES=1 ;;
    --with-pro)  WITH_PRO=1 ;;
    --no-agents) NO_AGENTS=1 ;;
  esac
done

if [[ -t 1 ]]; then
  GREEN=$'\033[0;32m'; CYAN=$'\033[0;36m'; YELLOW=$'\033[0;33m'; BOLD=$'\033[1m'; RESET=$'\033[0m'
else
  GREEN=""; CYAN=""; YELLOW=""; BOLD=""; RESET=""
fi

say()  { printf "%s\n" "$*"; }
sec()  { printf "\n%s%s%s\n" "$BOLD" "$*" "$RESET"; }
ok()   { printf "  %s✓%s %s\n" "$GREEN" "$RESET" "$*"; }
warn() { printf "  %s!%s %s\n" "$YELLOW" "$RESET" "$*"; }
ask()  { [[ "$ASSUME_YES" == "1" ]] && return 0; printf "%s?%s %s [y/N] " "$CYAN" "$RESET" "$*"; read -r r; [[ "$r" =~ ^[Yy]$ ]]; }

mkdir -p "$CLAUDE_DIR/skills" "$CLAUDE_DIR/agents"

# install_skill <name> — copies skills/<name>/SKILL.md (+ sibling assets) into ~/.claude
install_skill() {
  local name="$1"
  local src="$SRC_DIR/skills/$name/SKILL.md"
  local dst_dir="$CLAUDE_DIR/skills/$name"
  local dst="$dst_dir/SKILL.md"
  [[ -f "$src" ]] || { warn "Skill '$name' missing from repo — skipping."; return; }
  if [[ -f "$dst" ]]; then
    if diff -q "$dst" "$src" >/dev/null 2>&1; then ok "$name already up-to-date."; return; fi
    say "  Diff for $name:"; diff -u "$dst" "$src" || true
    ask "  Overwrite $name?" || { warn "Skipped $name."; return; }
  fi
  mkdir -p "$dst_dir"
  cp "$src" "$dst"
  for asset in "$SRC_DIR/skills/$name"/*; do
    [[ -f "$asset" ]] || continue
    [[ "$(basename "$asset")" == "SKILL.md" ]] && continue
    cp "$asset" "$dst_dir/"
  done
  ok "Installed skill: $name"
}

install_agent() {
  local name="$1"
  local src="$SRC_DIR/agents/$name.md" dst="$CLAUDE_DIR/agents/$name.md"
  [[ -f "$src" ]] || { warn "Agent '$name' missing from repo — skipping."; return; }
  if [[ -f "$dst" ]]; then
    if diff -q "$dst" "$src" >/dev/null 2>&1; then ok "$name already up-to-date."; return; fi
    say "  Diff for $name:"; diff -u "$dst" "$src" || true
    ask "  Overwrite $name?" || { warn "Skipped $name."; return; }
  fi
  cp "$src" "$dst"
  ok "Installed agent: $name"
}

sec "Core skills"
say "  council  — 5-perspective decision helper"
say "  scrape   — read-only web data → clean JSON"
say "  skillify — codify a successful scrape into a reusable script"
say "  canary   — post-deploy monitoring (alerts on what changed vs a baseline)"
for s in council scrape skillify canary; do install_skill "$s"; done

if [[ -z "$NO_AGENTS" ]]; then
  sec "German legal + tax research agents (--no-agents to skip)"
  say "  legal-de + tax-de — mandatory source citation, statutory disclaimers."
  if [[ "$ASSUME_YES" == "1" ]] || ask "  Install these?"; then
    for a in legal-de tax-de; do install_agent "$a"; done
  fi
fi

sec "settings.json template (only if you don't have one yet)"
if [[ -f "$CLAUDE_DIR/settings.json" ]]; then
  say "  You already have a settings.json. Not touching it. Diff against template:"
  diff "$CLAUDE_DIR/settings.json" "$SRC_DIR/settings.example.json" || true
elif [[ "$ASSUME_YES" == "1" ]] || ask "  Install fresh settings.json from template?"; then
  cp "$SRC_DIR/settings.example.json" "$CLAUDE_DIR/settings.json"
  ok "Installed settings.json with defaultMode = 'default' (safe choice)."
fi

if [[ -n "$WITH_PRO" ]]; then
  sec "Pro skill layer"
  if [[ "$ASSUME_YES" == "1" ]]; then
    bash "$SRC_DIR/pro/skills/install-pro-skills.sh" --yes
  else
    bash "$SRC_DIR/pro/skills/install-pro-skills.sh"
  fi
fi

sec "Manual steps"
say "  → Drop templates/CLAUDE.example.md into your project root as CLAUDE.md."
say "  → Read docs/04-the-daily-loop.md — how to actually drive Claude through a task."
say "  → Read docs/02-memory-system.md to understand auto-memory."
say "  → Optional Pro layer (autoplan, spec + obra skills): ./install.sh --with-pro"
say "  → Self-healing apps (synthetic user + fix-agent): see pro/self-heal/README.md + docs/05."
say "  → Let Claude file work in Linear (issue tracker): see docs/06-linear-issues.md."
say "  → Wire up MCPs (Linear / Sentry / Supabase, one line each): see docs/07-mcps.md."
say "  → Star the repo if it helped: https://github.com/CommsConnectgmbh/claude-starter-kit"
