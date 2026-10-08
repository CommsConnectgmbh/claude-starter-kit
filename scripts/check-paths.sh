#!/usr/bin/env bash
# Check that every LOCAL path linked in Markdown files exists
# and that all shell scripts have valid syntax.
# Run locally (./scripts/check-paths.sh) and in CI. Exit 1 on errors.
set -uo pipefail
cd "$(dirname "$0")/.." || exit 2

fail=0

echo "== 1. Shell scripts: bash -n =="
while IFS= read -r sh; do
  if bash -n "$sh" 2>/dev/null; then
    echo "  ok  $sh"
  else
    echo "  ERROR (syntax): $sh"; bash -n "$sh"; fail=1
  fi
done < <(find . -name '*.sh' -not -path './.git/*' -not -path '*/node_modules/*')

echo "== 2. Markdown: local link/path targets exist =="
rm -f /tmp/check_paths_fail
# Walk all Markdown files; resolve links relative to each file's directory.
while IFS= read -r md; do
  dir=$(dirname "$md")
  # Extract ](target), keeping only the target.
  grep -oE '\]\([^)]+\)' "$md" 2>/dev/null | sed -E 's/^\]\(//; s/\)$//' | while IFS= read -r target; do
    # Skip external links, anchors, mail links, and GitHub UI routes
    # (../../issues/new/choose, ../../pulls … are valid on GitHub, not files).
    case "$target" in
      http://*|https://*|mailto:*|\#*|"") continue ;;
      */issues/*|*/issues|*/pull/*|*/pulls|*/pulls/*|*/wiki|*/wiki/*|*/discussions*|*/releases*|*/actions*|*/compare/*) continue ;;
    esac
    # Strip the anchor and query.
    clean=${target%%#*}
    clean=${clean%%\?*}
    [ -z "$clean" ] && continue
    # Check absolute repo paths (starting with /) relative to the repo root.
    case "$clean" in
      /*) path=".${clean}" ;;
      *)  path="${dir}/${clean}" ;;
    esac
    if [ ! -e "$path" ]; then
      echo "  MISSING TARGET: $md → $target"
      echo "MISSING" >> /tmp/check_paths_fail
    fi
  done
done < <(find . -name '*.md' -not -path './.git/*' -not -path '*/node_modules/*')

if [ -f /tmp/check_paths_fail ]; then rm -f /tmp/check_paths_fail; fail=1; else echo "  ok  all local Markdown targets exist"; fi

if [ "$fail" -ne 0 ]; then
  echo "== FAILED =="; exit 1
fi
echo "== ALL CHECKS PASSED =="
