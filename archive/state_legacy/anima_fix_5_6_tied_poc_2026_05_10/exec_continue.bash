#!/bin/bash
# Continuation orchestrator — pod already provisioned, just stage + run.
# Use existing pod from POD_INFO env or argv.

set -uo pipefail

ANIMA_ROOT="/Users/ghost/core/anima"
STATE_DIR="${ANIMA_ROOT}/state/anima_fix_5_6_tied_poc_2026_05_10"
RESULTS_DIR="${STATE_DIR}/results"
LOG_DIR="${STATE_DIR}/logs"
RUN_LOG="${LOG_DIR}/run.log"
POD_INFO="${STATE_DIR}/pod_info.json"

ARCH_PY="${ANIMA_ROOT}/training/engine_a_g_arch.py"
TRAIN_PY="${ANIMA_ROOT}/tool/transient_py/anima_fix_5_6_tied_poc_h100.py"
BG_LB_CKPT="${HOME}/.cache/anima/clm_v5_remapped/bg_lb_350m_pretrain/ckpts/step_8000_final.pt"
CORPUS="${ANIMA_ROOT}/state/bg_lb_engine_ag_2026_05_09/big_corpus.txt"

SSH_KEY="${HOME}/.runpod/ssh/RunPod-Key-Go"

PY3=/opt/homebrew/bin/python3.real
if [ ! -x "$PY3" ]; then PY3=/usr/bin/python3; fi

POD_ID="${POD_ID:-${1:-}}"
if [ -z "$POD_ID" ]; then
    echo "usage: POD_ID=<id> $0   OR   $0 <pod_id>"; exit 1
fi

BUDGET_HARD_CAP_USD=15
COST_PER_HOUR=2.99
START_EPOCH=$(date -u +%s)
POD_NAME="fix56-tied-poc-cont-$(date +%s)"

mkdir -p "$STATE_DIR" "$RESULTS_DIR" "$LOG_DIR" "$RESULTS_DIR/ckpts" "$RESULTS_DIR/state"

log() { echo "[$(date -u +%FT%TZ)] $*" | tee -a "$RUN_LOG"; }

log "=== fix-5/6 PoC CONTINUATION (pod_id=${POD_ID}) ==="

MAX_WALL_MIN=$($PY3 "${STATE_DIR}/calc_max_wall.py")
log "budget_cap=\$${BUDGET_HARD_CAP_USD} max_wall_min=${MAX_WALL_MIN}"

# Wait for SSH info
log "=== waiting for pod SSH info ==="
SSH_HOST=""
SSH_PORT=""
for i in $(seq 1 30); do
    runpodctl pod get "$POD_ID" > "${STATE_DIR}/_pod_state.json" 2>&1
    SSH_HOST=$($PY3 "${STATE_DIR}/parse_pod_ssh.py" "${STATE_DIR}/_pod_state.json" host)
    SSH_PORT=$($PY3 "${STATE_DIR}/parse_pod_ssh.py" "${STATE_DIR}/_pod_state.json" port)
    log "ssh_info try $i: host=${SSH_HOST} port=${SSH_PORT}"
    if [ -n "$SSH_HOST" ] && [ -n "$SSH_PORT" ]; then
        break
    fi
    sleep 10
done
if [ -z "$SSH_HOST" ] || [ -z "$SSH_PORT" ]; then
    log "FATAL: SSH info not available after 5min"
    exit 5
fi
log "ssh=${SSH_HOST}:${SSH_PORT}"
echo "{\"pod_id\":\"$POD_ID\",\"ssh_host\":\"$SSH_HOST\",\"ssh_port\":\"$SSH_PORT\"}" > "$POD_INFO"

# Phase 2: SSH smoke + stage
log "=== Phase 2: SSH smoke + stage artifacts ==="
SSH_RETRIES=0
SSH_OK=0
while [ $SSH_RETRIES -lt 12 ]; do
    if ssh -i "$SSH_KEY" -p "$SSH_PORT" -o StrictHostKeyChecking=no -o ConnectTimeout=10 root@"$SSH_HOST" 'echo SSH_OK' 2>&1 | tee -a "$RUN_LOG" | grep -q SSH_OK; then
        SSH_OK=1
        break
    fi
    SSH_RETRIES=$((SSH_RETRIES + 1))
    log "ssh retry $SSH_RETRIES/12"
    sleep 15
done
if [ "$SSH_OK" -ne 1 ]; then
    log "FATAL: SSH never came up"
    exit 6
fi

ssh -i "$SSH_KEY" -p "$SSH_PORT" -o StrictHostKeyChecking=no root@"$SSH_HOST" 'nvidia-smi -L' 2>&1 | tee -a "$RUN_LOG"
ssh -i "$SSH_KEY" -p "$SSH_PORT" -o StrictHostKeyChecking=no root@"$SSH_HOST" 'mkdir -p /workspace/anima_fix_5_6_poc/ckpts /workspace/anima_fix_5_6_poc/state && touch /workspace/anima_fix_5_6_poc/_pod_marker'

scp -i "$SSH_KEY" -P "$SSH_PORT" -o StrictHostKeyChecking=no "$ARCH_PY"     root@"$SSH_HOST":/workspace/anima_fix_5_6_poc/engine_a_g_arch.py
scp -i "$SSH_KEY" -P "$SSH_PORT" -o StrictHostKeyChecking=no "$TRAIN_PY"    root@"$SSH_HOST":/workspace/anima_fix_5_6_poc/anima_fix_5_6_tied_poc_h100.py
scp -i "$SSH_KEY" -P "$SSH_PORT" -o StrictHostKeyChecking=no "$BG_LB_CKPT"  root@"$SSH_HOST":/workspace/anima_fix_5_6_poc/bg_lb_step_8000_final.pt
scp -i "$SSH_KEY" -P "$SSH_PORT" -o StrictHostKeyChecking=no "$CORPUS"      root@"$SSH_HOST":/workspace/anima_fix_5_6_poc/big_corpus.txt
log "stage complete"

# Phase 3: deps
log "=== Phase 3: install deps ==="
ssh -i "$SSH_KEY" -p "$SSH_PORT" -o StrictHostKeyChecking=no root@"$SSH_HOST" \
    'pip install --break-system-packages transformers safetensors 2>&1 | tail -5' 2>&1 | tee -a "$RUN_LOG"

# Phase 4: launch
log "=== Phase 4: launch 3-branch sequential training ==="
ssh -i "$SSH_KEY" -p "$SSH_PORT" -o StrictHostKeyChecking=no root@"$SSH_HOST" \
    'cd /workspace/anima_fix_5_6_poc && nohup python3 anima_fix_5_6_tied_poc_h100.py --branches a,b,c > train.log 2>&1 &'

# Phase 5: heartbeat
log "=== Phase 5: heartbeat monitor (\$$BUDGET_HARD_CAP_USD hard cap) ==="
ELAPSED=0
HEARTBEAT_S=180
HARD_KILL_S=$((MAX_WALL_MIN * 60))
while [ "$ELAPSED" -lt "$HARD_KILL_S" ]; do
    sleep "$HEARTBEAT_S"
    NOW=$(date -u +%s)
    ELAPSED=$((NOW - START_EPOCH))
    COST=$($PY3 "${STATE_DIR}/calc_cost.py" "$ELAPSED" "$COST_PER_HOUR")
    log "hb t=${ELAPSED}s cost=\$${COST} pod=${POD_ID}"
    if $PY3 "${STATE_DIR}/check_cost_over.py" "$COST" "$BUDGET_HARD_CAP_USD"; then
        log "COST_OVERRUN — \$${COST} > \$${BUDGET_HARD_CAP_USD}; aborting"
        break
    fi
    if $PY3 "${STATE_DIR}/check_cost_over.py" "$COST" "13.5"; then
        log "WARN: cost \$${COST} > \$13.5 pre-cap; aborting next heartbeat"
        break
    fi
    DONE=$(ssh -i "$SSH_KEY" -p "$SSH_PORT" -o StrictHostKeyChecking=no root@"$SSH_HOST" 'test -f /workspace/anima_fix_5_6_poc/state/COMPLETE.sentinel && echo done || echo running' 2>/dev/null || echo running)
    if [ "$DONE" = "done" ]; then
        log "COMPLETE.sentinel detected"
        break
    fi
    PROGRESS=$(ssh -i "$SSH_KEY" -p "$SSH_PORT" -o StrictHostKeyChecking=no root@"$SSH_HOST" 'cat /workspace/anima_fix_5_6_poc/state/progress.json 2>/dev/null' 2>/dev/null || echo '')
    if [ -n "$PROGRESS" ]; then
        log "progress: $PROGRESS"
    fi
done

# Phase 6: pull
log "=== Phase 6: ckpt pull (own 30) ==="
scp -i "$SSH_KEY" -P "$SSH_PORT" -o StrictHostKeyChecking=no -r -o ConnectTimeout=3600 \
    root@"$SSH_HOST":/workspace/anima_fix_5_6_poc/ckpts/. \
    "$RESULTS_DIR/ckpts/" 2>&1 | tee -a "$RUN_LOG"
PULL_RC=${PIPESTATUS[0]}
scp -i "$SSH_KEY" -P "$SSH_PORT" -o StrictHostKeyChecking=no -r \
    root@"$SSH_HOST":/workspace/anima_fix_5_6_poc/state/. \
    "$RESULTS_DIR/state/" 2>&1 | tee -a "$RUN_LOG"
scp -i "$SSH_KEY" -P "$SSH_PORT" -o StrictHostKeyChecking=no \
    root@"$SSH_HOST":/workspace/anima_fix_5_6_poc/train.log \
    "$LOG_DIR/pod_train.log" 2>&1 | tee -a "$RUN_LOG"

POD_SZ=$(ssh -i "$SSH_KEY" -p "$SSH_PORT" -o StrictHostKeyChecking=no root@"$SSH_HOST" 'du -sb /workspace/anima_fix_5_6_poc/ckpts | cut -f1' 2>/dev/null || echo 0)
LOCAL_SZ=$(du -sb "$RESULTS_DIR/ckpts" 2>/dev/null | cut -f1 || echo 0)
log "size check: pod=$POD_SZ local=$LOCAL_SZ"

if [ "$PULL_RC" -eq 0 ] && [ "$LOCAL_SZ" != "0" ]; then
    log "=== Phase 8: pod delete ($POD_ID) ==="
    runpodctl pod delete "$POD_ID" 2>&1 | tee -a "$RUN_LOG"
else
    log "PULL FAILED OR EMPTY — POD RETAINED $POD_ID"
fi

COST_FINAL=$($PY3 "${STATE_DIR}/calc_cost.py" "$ELAPSED" "$COST_PER_HOUR")
log "=== Phase 9: ledger (cost_final=\$${COST_FINAL}) ==="
LEDGER="${ANIMA_ROOT}/state/anima_model_attempts_ledger.jsonl"
$PY3 "${STATE_DIR}/append_ledger.py" "$LEDGER" "$POD_ID" "$POD_NAME" "$ELAPSED" "$COST_FINAL" 2>&1 | tee -a "$RUN_LOG"

log "=== fix-5/6 PoC continuation DONE (cost=\$${COST_FINAL}) ==="
