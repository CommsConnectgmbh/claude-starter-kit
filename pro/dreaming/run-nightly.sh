#!/bin/bash
# Nightly dreaming pass — invoke from cron / launchd / Task Scheduler.
#
# Set MEMORY_DIR before sourcing or pass it inline:
#   MEMORY_DIR=/path/to/memory ./run-nightly.sh

set -euo pipefail

cd "$(dirname "$0")"

LOG_DIR="./scheduler_logs"
mkdir -p "$LOG_DIR"
TS=$(date +%Y-%m-%d_%H%M%S)
LOG="$LOG_DIR/dream-$TS.log"

# Strip API keys so `claude` uses your Max-Plan session, not API billing.
unset ANTHROPIC_API_KEY
unset ANTHROPIC_AUTH_TOKEN

if [[ -z "${MEMORY_DIR:-}" ]]; then
  echo "MEMORY_DIR not set — aborting." >&2
  exit 2
fi

{
  echo "=== Dreaming run started $(date) ==="
  echo "MEMORY_DIR=$MEMORY_DIR"
  node ./dream.mjs
  echo ""
  echo "=== Auto-Apply (confidence >= ${APPLY_THRESHOLD:-0.85}) ==="
  node ./dream.mjs --apply "$(date +%F)"
  echo "=== Done $(date) ==="
} >> "$LOG" 2>&1

# Keep last 30 logs
ls -t "$LOG_DIR"/dream-*.log 2>/dev/null | tail -n +31 | xargs -r rm
