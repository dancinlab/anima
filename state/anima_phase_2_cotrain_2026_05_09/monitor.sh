#!/bin/bash
# Phase 2 cotrain monitor — emit progress + cost watchdog.
# Usage: ./monitor.sh
SSH_HOST=205.196.17.170
SSH_PORT=18488
SSH_KEY=/Users/ghost/.runpod/ssh/RunPod-Key-Go
COST_PER_HR=3.07
COST_HARD_CAP=60
START_EPOCH=$(date -u -d "2026-05-09T13:57:29Z" +%s 2>/dev/null || python3 -c "import datetime; print(int(datetime.datetime.fromisoformat('2026-05-09T13:57:29+00:00').timestamp()))")
NOW=$(date -u +%s)
ELAPSED=$((NOW - START_EPOCH))
COST=$(python3 -c "print(round($ELAPSED/3600 * $COST_PER_HR, 2))")
echo "[mon $(date -u +%FT%TZ)] elapsed=${ELAPSED}s cost=\$$COST cap=\$$COST_HARD_CAP"
ssh -i "$SSH_KEY" -p "$SSH_PORT" -o StrictHostKeyChecking=no -o ConnectTimeout=10 root@$SSH_HOST \
    'tail -3 /workspace/anima_phase2/train.log 2>/dev/null; \
     echo "---"; \
     ls -1 /workspace/anima_phase2/ckpts/ 2>/dev/null; \
     echo "---"; \
     test -f /workspace/anima_phase2/state/COMPLETE.sentinel && echo COMPLETE || echo RUNNING'
