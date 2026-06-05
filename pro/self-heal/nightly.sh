#!/usr/bin/env bash
# self-heal nightly — synthetic run, then dry-run the fixer so you get a report
# without anything touching code unsupervised. Flip to --live once you trust it.
set -euo pipefail
cd "$(dirname "$0")"

echo "▸ synthetic run"
node synthetic/run.mjs

echo "▸ fix-agent (dry-run)"
node agent/fix.mjs            # add --live to let it open PRs / issues

# Optional: mail yourself the latest report. Wire up your own sender here.
# latest=$(ls -t synthetic/reports/*.md | head -1)
# node notify.mjs "$latest"
