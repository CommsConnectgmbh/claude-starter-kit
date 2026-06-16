#!/usr/bin/env bash
#
# install-pro-skills.sh — installs the optional "Pro" skill layer:
#   1. Bundled gstack-derived skills (autoplan, spec) shipped in this repo.
#   2. A curated subset of obra/superpowers-skills, cloned fresh from upstream.
#
# Nothing is overwritten without showing you a diff first.
# Pass --yes (or -y) for a non-interactive install.

set -euo pipefail

CLAUDE_DIR="${CLAUDE_DIR:-$HOME/.claude}"
SRC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
UPSTREAM="https://github.com/obra/superpowers-skills.git"

# Bundled in this repo (pro/skills/<name>/SKILL.md). gstack-derived where noted, MIT.
#  autoplan / spec       — gstack-derived
#  second-opinion        — local Ollama as adversarial reviewer
#  compliance            — quarterly Aikido+Supabase+Prowler audit pattern
#  fal-ai / openai-image — direct image/video API skills (BYO key)
BUNDLED=(autoplan spec second-opinion compliance fal-ai openai-image)

# Cloned from obra/superpowers-skills — universal techniques, not project-specific.
OBRA=(
  when-stuck
  root-cause-tracing
  inversion-exercise
  dispatching-parallel-agents
  subagent-driven-development
)

if [[ -t 1 ]]; then
  GREEN=$'\033[0;32m'; CYAN=$'\033[0;36m'; YELLOW=$'\033[0;33m'; BOLD=$'\033[1m'; RESET=$'\033[0m'
else
  GREEN=""; CYAN=""; YELLOW=""; BOLD=""; RESET=""
fi

ASSUME_YES=""
[[ "${1:-}" == "--yes" || "${1:-}" == "-y" ]] && ASSUME_YES=1

say()  { printf "%s\n" "$*"; }
sec()  { printf "\n%s%s%s\n" "$BOLD" "$*" "$RESET"; }
ok()   { printf "  %s✓%s %s\n" "$GREEN" "$RESET" "$*"; }
warn() { printf "  %s!%s %s\n" "$YELLOW" "$RESET" "$*"; }
ask()  { [[ "$ASSUME_YES" == "1" ]] && return 0; printf "%s?%s %s [y/N] " "$CYAN" "$RESET" "$*"; read -r r; [[ "$r" =~ ^[Yy]$ ]]; }

command -v git >/dev/null || { echo "git is required"; exit 2; }
mkdir -p "$CLAUDE_DIR/skills"

# install_skill <name> <src_skill_md>
install_skill() {
  local name="$1" src="$2"
  local dst_dir="$CLAUDE_DIR/skills/$name"
  local dst="$dst_dir/SKILL.md"
  if [[ -f "$dst" ]]; then
    if diff -q "$dst" "$src" >/dev/null 2>&1; then
      ok "$name already up-to-date."
      return
    fi
    say "  Diff for $name:"
    diff -u "$dst" "$src" || true
    ask "  Overwrite $name?" || { warn "Skipped $name."; return; }
  fi
  mkdir -p "$dst_dir"
  cp "$src" "$dst"
  # Copy any sibling assets (scripts referenced by SKILL.md).
  local src_dir; src_dir=$(dirname "$src")
  for asset in "$src_dir"/*; do
    [[ -f "$asset" ]] || continue
    [[ "$(basename "$asset")" == "SKILL.md" ]] && continue
    cp "$asset" "$dst_dir/"
  done
  ok "Installed $name"
}

sec "1. Bundled gstack-derived skills (autoplan, spec)"
say "  Note: these call optional companion skills (a frontend-design skill, an"
say "  independent-reviewer skill). Missing companions are skipped gracefully."
for skill in "${BUNDLED[@]}"; do
  src="$SRC_DIR/$skill/SKILL.md"
  [[ -f "$src" ]] || { warn "Bundled skill '$skill' missing from repo — skipping."; continue; }
  install_skill "$skill" "$src"
done

sec "2. obra/superpowers-skills (cloned fresh from upstream)"
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
git clone --depth=1 --quiet "$UPSTREAM" "$TMP/superpowers"
ok "Clone complete."
for skill in "${OBRA[@]}"; do
  src=$(find "$TMP/superpowers" -type f -name "SKILL.md" -path "*/$skill/*" | head -n 1 || true)
  [[ -z "$src" ]] && { warn "Source not found for '$skill' upstream — skipping."; continue; }
  install_skill "$skill" "$src"
done

sec "Done"
say "  Skills live in $CLAUDE_DIR/skills/"
say "  gstack skills bundled here (MIT, garrytan/gstack). obra skills: $UPSTREAM (MIT, Jesse Vincent)."
say "  Re-run this script to pull obra updates."
