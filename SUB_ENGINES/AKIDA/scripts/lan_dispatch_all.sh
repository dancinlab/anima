#!/usr/bin/env bash
# lan_dispatch_all.sh — 전 anima-repo 보유 host 에 SUB_ENGINES/AKIDA BOOT.sh
#
# 1) lan_status.sh 의 anima_repo:✓ host 추출
# 2) 각 host 에 lan_boot.sh dispatch
#
# Usage:
#   ./lan_dispatch_all.sh                # = ./BOOT.sh 1 7 on every anima-repo host
#   ./lan_dispatch_all.sh --days 3-5

set -eu

HERE="$(cd "$(dirname "$0")" && pwd)"
DAYS_ARG=""
if [ "${1:-}" = "--days" ] && [ -n "${2:-}" ]; then
    DAYS_ARG="--days $2"
fi

# Step 1: anima-repo 보유 host 추출 (parallel probe via pool on all)
echo "=== probing anima-repo presence ==="
HOSTS=$(pool on all 'test -d ~/anima && echo HAS_ANIMA' 2>&1 \
    | grep "HAS_ANIMA" \
    | sed -E 's/^\[([^ ]+).*\].*/\1/' \
    | tr -d ' ')

if [ -z "$HOSTS" ]; then
    echo "no anima-repo host found"
    exit 0
fi

# Step 2: 각 host 에 BOOT dispatch
echo "=== dispatching to $(echo "$HOSTS" | wc -l | tr -d ' ') host ==="
for h in $HOSTS; do
    echo "--- $h ---"
    "$HERE/lan_boot.sh" "$h" $DAYS_ARG || echo "[$h] FAIL exit $?"
done
