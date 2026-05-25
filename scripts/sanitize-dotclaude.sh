#!/usr/bin/env bash
#
# sanitize-dotclaude.sh — scan your ~/.claude/ folder and flag entries that
# contain likely-personal strings (names, emails, domains, project IDs, paths).
#
# Output:
#   - A list of files that look safe to share as-is.
#   - A list of files that need redaction, with the matching lines.
#   - A list of files that should NOT be shared (likely client/internal info).
#
# This script is read-only. It modifies nothing. Run it before publishing any
# part of your ~/.claude/ folder.
#
# Usage:
#   ./scripts/sanitize-dotclaude.sh [path-to-claude-dir]
#
# Default path is ~/.claude.

set -euo pipefail

CLAUDE_DIR="${1:-$HOME/.claude}"

if [[ ! -d "$CLAUDE_DIR" ]]; then
  echo "Error: $CLAUDE_DIR does not exist." >&2
  exit 1
fi

# --- Configure these for your own situation ------------------------------------
# Add your own name, company names, domains, internal project codenames here.
# The script greps case-insensitively for any of these patterns.

PERSONAL_PATTERNS=(
  # Generic indicators
  "@gmail\\.com"
  "@yahoo\\.com"
  "@outlook\\.com"
  "@hotmail\\.com"
  # API/secret indicators
  "sk-[a-zA-Z0-9]{20,}"
  "sk_live_[a-zA-Z0-9]{20,}"
  "AKIA[A-Z0-9]{16}"
  "supabase.*[a-z0-9]{20,}"
  "ghp_[a-zA-Z0-9]{36,}"
  "github_pat_[a-zA-Z0-9_]{20,}"
  # Path indicators (likely personal). Each requires a real character class
  # after the prefix, so documentation placeholders like `/Users/<you>/` or
  # `C:\Users\…` are NOT flagged as false positives.
  "/Users/[a-z][a-z0-9_-]+/"
  "C:\\\\Users\\\\[A-Z][A-Za-z0-9_-]+"
  "C:\\\\Claude Code\\\\[A-Z]"
)

# Add company-specific terms here. Anything matching these is automatically
# flagged DO-NOT-SHARE.
COMPANY_PATTERNS=(
  # Examples — replace with your own:
  # "AcmeCorp"
  # "client-codename"
)

# Directories to always skip (binary / not interesting for sharing review)
SKIP_DIRS=(
  "backups"
  "cache"
  "file-history"
  "ide"
  "paste-cache"
  "plugins"
  "projects"
  "session-env"
  "sessions"
  "shell-snapshots"
  "tasks"
  "telemetry"
  "downloads"
)

# Files to always skip
SKIP_FILES=(
  "history.jsonl"
  "policy-limits.json"
  ".last-cleanup"
  "mcp-needs-auth-cache.json"
  "settings.local.json"
)

# -----------------------------------------------------------------------------

# Build find arguments in an array to preserve quoting and globs.
SKIP_ARGS=()
for d in "${SKIP_DIRS[@]}"; do
  SKIP_ARGS+=(-not -path "$CLAUDE_DIR/$d/*")
done
for f in "${SKIP_FILES[@]}"; do
  SKIP_ARGS+=(-not -name "$f")
done

# Color helpers (no color if not a TTY)
if [[ -t 1 ]]; then
  GREEN=$'\033[0;32m'
  YELLOW=$'\033[0;33m'
  RED=$'\033[0;31m'
  BOLD=$'\033[1m'
  RESET=$'\033[0m'
else
  GREEN=""; YELLOW=""; RED=""; BOLD=""; RESET=""
fi

echo "${BOLD}Scanning $CLAUDE_DIR${RESET}"
echo ""

SAFE=()
REDACT=()
DONOTSHARE=()

while IFS= read -r -d '' file; do
  matches=""

  # Check for company patterns first — these are auto DO-NOT-SHARE
  has_company=false
  if [[ ${#COMPANY_PATTERNS[@]} -gt 0 ]]; then
    for pat in "${COMPANY_PATTERNS[@]}"; do
      if grep -qiE "$pat" "$file" 2>/dev/null; then
        has_company=true
        matches+="  [company] $(grep -niE "$pat" "$file" | head -3)"$'\n'
      fi
    done
  fi

  # Check personal patterns
  has_personal=false
  for pat in "${PERSONAL_PATTERNS[@]}"; do
    if grep -qiE "$pat" "$file" 2>/dev/null; then
      has_personal=true
      matches+="  [personal] $(grep -niE "$pat" "$file" | head -3)"$'\n'
    fi
  done

  if $has_company; then
    DONOTSHARE+=("$file")
    echo "${RED}DO NOT SHARE${RESET}  $file"
    echo "$matches"
  elif $has_personal; then
    REDACT+=("$file")
    echo "${YELLOW}REDACT${RESET}        $file"
    echo "$matches"
  else
    SAFE+=("$file")
  fi
done < <(find "$CLAUDE_DIR" -type f \( -name "*.md" -o -name "*.json" -o -name "*.sh" -o -name "*.py" -o -name "*.js" -o -name "*.ts" \) "${SKIP_ARGS[@]}" -print0)

echo ""
echo "${BOLD}Summary${RESET}"
echo "  ${GREEN}Safe:${RESET}         ${#SAFE[@]} files"
echo "  ${YELLOW}Need redaction:${RESET} ${#REDACT[@]} files"
echo "  ${RED}Do not share:${RESET}  ${#DONOTSHARE[@]} files"
echo ""

if [[ ${#SAFE[@]} -gt 0 ]]; then
  echo "${BOLD}Safe files (no personal/company strings detected):${RESET}"
  for f in "${SAFE[@]}"; do
    echo "  $f"
  done
  echo ""
fi

cat <<EOF
${BOLD}Important caveats${RESET}

This script catches common patterns, NOT everything. It does not understand:
  - Codenames you forgot to add to COMPANY_PATTERNS
  - Customer names mentioned in passing
  - Internal terminology that means nothing publicly but identifies a client
  - References to private repos by their structure

Before publishing any "safe" file, READ IT. A human review is mandatory.

Also: this script does not scan ~/.claude/projects/, ~/.claude/sessions/, or
~/.claude/history.jsonl. Those folders contain conversation transcripts and
should NEVER be published — they are full of everything you've ever told Claude.
EOF
