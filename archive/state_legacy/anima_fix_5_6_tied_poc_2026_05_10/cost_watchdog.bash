#!/bin/bash
# External cost watchdog — independent of orchestrator clock.
# Polls actual balance every 60s; aborts if total spend > threshold.
# When threshold hit:
#   1) signal training to stop (touch /workspace/anima_fix_5_6_poc/state/ABORT.sentinel)
#   2) pull all current ckpts (whatever exists)
#   3) delete pod
#
set -uo pipefail

POD_ID="${1:-v8v694g06he7fm}"
# Total cumulative spend cap from pod create (already ~$4 spent during stage)
TOTAL_HARD_CAP=14.5      # leave $0.50 for pull operations (over $15 ceiling)
TOTAL_SOFT_CAP=12.5      # at this point, signal abort to training
# Pod creation balance baseline (full cycle spend tracking)
POD_CREATE_BALANCE="${POD_CREATE_BALANCE:-323.859245206}"  # known balance pre-create
SSH_HOST="${SSH_HOST:-103.207.149.153}"
SSH_PORT="${SSH_PORT:-11535}"
SSH_KEY="${SSH_KEY:-/Users/ghost/.runpod/ssh/RunPod-Key-Go}"

ANIMA_ROOT="/Users/ghost/core/anima"
STATE_DIR="${ANIMA_ROOT}/state/anima_fix_5_6_tied_poc_2026_05_10"
RESULTS_DIR="${STATE_DIR}/results"
LOG_FILE="${STATE_DIR}/logs/watchdog.log"

PY3=/opt/homebrew/bin/python3.real
if [ ! -x "$PY3" ]; then PY3=/usr/bin/python3; fi

echo "[$(date -u +%FT%TZ)] watchdog START | pod=$POD_ID create_baseline=\$$POD_CREATE_BALANCE total_soft_cap=\$$TOTAL_SOFT_CAP total_hard_cap=\$$TOTAL_HARD_CAP" | tee -a "$LOG_FILE"

ABORT_SIGNALED=0
while true; do
    sleep 60
    NOW_BALANCE=$(runpodctl me 2>&1 | grep clientBalance | awk -F: '{print $2}' | tr -d ', ')
    # Total spend = cumulative spend from pod create (NOT from watchdog start)
    SPENT=$($PY3 -c "print(round($POD_CREATE_BALANCE - $NOW_BALANCE, 4))" 2>/dev/null || echo "??")
    echo "[$(date -u +%FT%TZ)] total_spent=\$$SPENT balance=\$$NOW_BALANCE" | tee -a "$LOG_FILE"

    # Check soft cap
    if [ "$ABORT_SIGNALED" -eq 0 ]; then
        if $PY3 -c "import sys; sys.exit(0 if $SPENT >= $TOTAL_SOFT_CAP else 1)"; then
            echo "[$(date -u +%FT%TZ)] TOTAL_SOFT_CAP hit at \$$SPENT — signaling abort" | tee -a "$LOG_FILE"
            ssh -i "$SSH_KEY" -p "$SSH_PORT" -o StrictHostKeyChecking=no root@"$SSH_HOST" \
                'touch /workspace/anima_fix_5_6_poc/state/ABORT.sentinel' 2>/dev/null || true
            ABORT_SIGNALED=1
        fi
    fi

    # Check hard cap — force pull + delete
    if $PY3 -c "import sys; sys.exit(0 if $SPENT >= $TOTAL_HARD_CAP else 1)"; then
        echo "[$(date -u +%FT%TZ)] HARD_CAP hit at \$$SPENT — emergency pull + delete" | tee -a "$LOG_FILE"
        # Pull ckpts
        scp -i "$SSH_KEY" -P "$SSH_PORT" -o StrictHostKeyChecking=no -r \
            root@"$SSH_HOST":/workspace/anima_fix_5_6_poc/ckpts/. \
            "$RESULTS_DIR/ckpts_emergency/" 2>&1 | tee -a "$LOG_FILE" || true
        scp -i "$SSH_KEY" -P "$SSH_PORT" -o StrictHostKeyChecking=no -r \
            root@"$SSH_HOST":/workspace/anima_fix_5_6_poc/state/. \
            "$RESULTS_DIR/state_emergency/" 2>&1 | tee -a "$LOG_FILE" || true
        scp -i "$SSH_KEY" -P "$SSH_PORT" -o StrictHostKeyChecking=no \
            root@"$SSH_HOST":/workspace/anima_fix_5_6_poc/train.log \
            "${STATE_DIR}/logs/pod_train_emergency.log" 2>&1 | tee -a "$LOG_FILE" || true
        # Delete pod
        runpodctl pod delete "$POD_ID" 2>&1 | tee -a "$LOG_FILE"
        echo "[$(date -u +%FT%TZ)] watchdog DONE — pod deleted" | tee -a "$LOG_FILE"
        # Kill the main orchestrator
        pkill -f "exec_continue.bash" 2>/dev/null || true
        exit 0
    fi
done
