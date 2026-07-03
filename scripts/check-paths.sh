#!/usr/bin/env bash
# Prüft, dass jeder in Markdown-Dateien verlinkte LOKALE Pfad wirklich existiert
# und dass alle Shell-Skripte syntaktisch fehlerfrei sind.
# Läuft lokal (./scripts/check-paths.sh) und in CI. Exit 1 bei Fehlern.
set -uo pipefail
cd "$(dirname "$0")/.." || exit 2

fail=0

echo "== 1. Shell-Skripte: bash -n =="
while IFS= read -r sh; do
  if bash -n "$sh" 2>/dev/null; then
    echo "  ok  $sh"
  else
    echo "  FEHLER (Syntax): $sh"; bash -n "$sh"; fail=1
  fi
done < <(find . -name '*.sh' -not -path './.git/*' -not -path '*/node_modules/*')

echo "== 2. Markdown: lokale Link-/Pfad-Ziele existieren =="
rm -f /tmp/check_paths_fail
# Alle Markdown-Dateien durchgehen; Links relativ zum Ordner der Datei auflösen.
while IFS= read -r md; do
  dir=$(dirname "$md")
  # Extrahiere ](target) — nimm nur den target-Teil.
  grep -oE '\]\([^)]+\)' "$md" 2>/dev/null | sed -E 's/^\]\(//; s/\)$//' | while IFS= read -r target; do
    # Überspringe externe/Anker-/Mail-Links und GitHub-UI-Routen
    # (../../issues/new/choose, ../../pulls … sind auf GitHub gültig, keine Dateien).
    case "$target" in
      http://*|https://*|mailto:*|\#*|"") continue ;;
      */issues/*|*/issues|*/pull/*|*/pulls|*/pulls/*|*/wiki|*/wiki/*|*/discussions*|*/releases*|*/actions*|*/compare/*) continue ;;
    esac
    # Anchor und Query abschneiden.
    clean=${target%%#*}
    clean=${clean%%\?*}
    [ -z "$clean" ] && continue
    # Absolute Repo-Pfade (mit führendem /) relativ zum Repo-Root prüfen.
    case "$clean" in
      /*) path=".${clean}" ;;
      *)  path="${dir}/${clean}" ;;
    esac
    if [ ! -e "$path" ]; then
      echo "  FEHLENDES ZIEL: $md → $target"
      echo "MISSING" >> /tmp/check_paths_fail
    fi
  done
done < <(find . -name '*.md' -not -path './.git/*' -not -path '*/node_modules/*')

if [ -f /tmp/check_paths_fail ]; then rm -f /tmp/check_paths_fail; fail=1; else echo "  ok  alle lokalen Markdown-Ziele existieren"; fi

if [ "$fail" -ne 0 ]; then
  echo "== FEHLGESCHLAGEN =="; exit 1
fi
echo "== ALLES GRÜN =="
