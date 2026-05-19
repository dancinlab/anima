#!/usr/bin/env bash
# anima CLM-3-original byte-level ubu1 30min interval monitor
# Usage: bash monitor_ubu1.bash <run_name>
# bash 3.2 compatible
set -uo pipefail

if [ $# -lt 1 ]; then
    echo "Usage: $0 <run_name>" >&2
    echo "  e.g. $0 clm3-original-byte-55m-ubu1-20260506-123456" >&2
    exit 2
fi

RUN_NAME="$1"
REPO_PATH=$(ssh ubu1 'if [ -d /home/aiden/core/anima ]; then echo /home/aiden/core/anima; elif [ -d /home/aiden/anima ]; then echo /home/aiden/anima; fi' 2>/dev/null)
[ -z "$REPO_PATH" ] && { echo "ERR: anima repo not found on ubu1" >&2; exit 1; }

echo "=== monitor $RUN_NAME @ $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
echo ""

echo "[1/4] tail -20 log"
ssh ubu1 "tail -20 $REPO_PATH/runs/$RUN_NAME.log 2>&1 || echo 'log missing'"
echo ""

echo "[2/4] checkpoint listing"
ssh ubu1 "ls -la $REPO_PATH/runs/$RUN_NAME/ 2>&1 | head -20 || echo 'output dir missing'"
echo ""

echo "[3/4] GPU state (RTX 5070)"
ssh ubu1 "nvidia-smi --query-gpu=memory.used,memory.total,utilization.gpu,temperature.gpu --format=csv,noheader 2>&1"
echo ""

echo "[4/4] process check (train_clm.py PID + start time)"
ssh ubu1 "ps -eo pid,etime,cmd | grep -E 'train_clm.py' | grep -v grep || echo 'no train process'"
echo ""

echo "=== monitor end ==="
