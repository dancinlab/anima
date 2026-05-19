#!/bin/bash
# state/anima_v5mitosis_cotrain_2026_05_12/dispatch_h100_v3.sh
#
# Phase 3 follow-up — v3 entropy-reg ANNEAL (path-f) on H100.
# v2 (λ=0.1) collapsed back to monopoly by step 250 — CE gradient overpowers
# bounded entropy term once CE < 5. v3 path: high λ_init (50.0) anneal to low
# λ_final (0.5) via cosine, keeps cells uniform during early CE-large phase
# while gradually allowing per-cell specialization in late phase.
#
# This is a TEMPLATE, NOT FIRED by this BG. To fire:
#   bash dispatch_h100_v3.sh
# with optional env overrides:
#   LAMBDA_INIT (default 50.0)
#   LAMBDA_FINAL (default 0.5)
#   LAMBDA_SCHEDULE (default cosine)
#   STEPS, BATCH, CTX, COST_CAP_USD, etc.

set -euo pipefail

PHASE_ID="v5mitosis_cotrain_v3"
LOCAL_DIR="/Users/ghost/core/anima/state/anima_v5mitosis_cotrain_2026_05_12"
PHASE_LABEL="anima-v5mit-v3"

STEPS="${STEPS:-5000}"
BATCH="${BATCH:-32}"
CTX="${CTX:-256}"
LR="${LR:-1e-4}"
WARMUP="${WARMUP:-500}"
D_MODEL="${D_MODEL:-384}"
N_HEAD="${N_HEAD:-6}"
FFN_DIM="${FFN_DIM:-1536}"
INITIAL_CELLS="${INITIAL_CELLS:-2}"
MAX_CELLS="${MAX_CELLS:-64}"
READOUT_MODE="${READOUT_MODE:-a_minus_g}"
SEED="${SEED:-42}"
LAMBDA_INIT="${LAMBDA_INIT:-50.0}"
LAMBDA_FINAL="${LAMBDA_FINAL:-0.5}"
LAMBDA_SCHEDULE="${LAMBDA_SCHEDULE:-cosine}"
N_PERMS="${N_PERMS:-100}"

COST_CAP_USD="${COST_CAP_USD:-8.0}"
COST_PER_HR_MAX="${COST_PER_HR_MAX:-5.0}"
ESTIMATED_WALL_HR="${ESTIMATED_WALL_HR:-1.5}"
ABSOLUTE_MAX_USD=$(python3 -c "print($COST_CAP_USD * 1.10)")

VAST_SSH_KEY="/Users/ghost/.vast/ssh/vast-key"
VASTAI="/Users/ghost/.local/bin/vastai"
[ -x "$VASTAI" ] || VASTAI="/Users/ghost/Library/Python/3.14/bin/vastai"
[ -x "$VASTAI" ] || { echo "ERROR: vastai CLI not found"; exit 1; }

cd "$LOCAL_DIR"
echo "=== ${PHASE_ID} vast.ai H100 dispatch ==="
date -u
echo "  steps=$STEPS d_model=$D_MODEL cells=${INITIAL_CELLS}-${MAX_CELLS}"
echo "  LAMBDA_INIT=$LAMBDA_INIT LAMBDA_FINAL=$LAMBDA_FINAL SCHEDULE=$LAMBDA_SCHEDULE"
echo "  cost_cap=\$$COST_CAP_USD"

echo "[1/9] Searching H100 offers ..."
OFFER_JSON=$($VASTAI search offers \
    "gpu_name in [H100_SXM,H100_PCIE,H100_NVL] num_gpus=1 reliability>0.93 dph_total<${COST_PER_HR_MAX} disk_space>50 inet_down>100" \
    -o dph_total --raw 2>&1)

OFFER_PARSED=$(echo "$OFFER_JSON" | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
except Exception as e:
    sys.stderr.write(f'parse_err: {e}\n')
    sys.exit(1)
if not data:
    sys.stderr.write('no_offers\n')
    sys.exit(1)
best = data[0]
print(f'{best[\"id\"]} {best[\"dph_total\"]:.4f} {best[\"gpu_name\"]} {best.get(\"reliability\",0):.3f}')
")
OFFER_ID=$(echo "$OFFER_PARSED" | awk '{print $1}')
OFFER_DPH=$(echo "$OFFER_PARSED" | awk '{print $2}')
echo "  Selected: id=$OFFER_ID dph=\$$OFFER_DPH"

EST_COST=$(python3 -c "print(round($OFFER_DPH * $ESTIMATED_WALL_HR, 2))")
EXCEEDS=$(python3 -c "print('YES' if $EST_COST > $ABSOLUTE_MAX_USD else 'NO')")
if [ "$EXCEEDS" = "YES" ]; then
    echo "[ABORT] est_cost \$$EST_COST > absolute_max \$$ABSOLUTE_MAX_USD"; exit 1
fi

echo "[3/9] Renting..."
CREATE_OUT=$($VASTAI create instance "$OFFER_ID" \
    --image pytorch/pytorch:2.5.1-cuda12.1-cudnn9-runtime \
    --disk 50 --ssh --direct --label "$PHASE_LABEL" --raw 2>&1)
INSTANCE_ID=$(echo "$CREATE_OUT" | python3 -c "
import json, sys
try:
    d=json.load(sys.stdin)
except Exception:
    sys.stderr.write('parse_fail\n'); sys.exit(1)
print(d.get('new_contract', d.get('contract_id', d.get('id', ''))))
")
[ -z "$INSTANCE_ID" ] && { echo "ERROR: parse instance id"; exit 1; }
echo "  Instance ID: $INSTANCE_ID"
echo "$INSTANCE_ID" > vast_instance_id_v3.txt

cleanup() {
    local exit_code=$?
    if [ "${SAVE_POD:-0}" = "1" ]; then
        echo "[cleanup] SAVE_POD=1 — keeping $INSTANCE_ID"
    else
        echo "[cleanup] Destroying $INSTANCE_ID..."
        $VASTAI destroy instance "$INSTANCE_ID" 2>&1 | head -3 || true
    fi
}
trap cleanup EXIT INT TERM

echo "[4/9] Waiting SSH ..."
SSH_HOST=""; SSH_PORT=""
for i in $(seq 1 160); do
    INFO=$($VASTAI show instance "$INSTANCE_ID" --raw 2>/dev/null || true)
    [ -z "$INFO" ] && INFO="{}"
    STATUS=$(echo "$INFO" | python3 -c "import json,sys;
try: d=json.load(sys.stdin); print(d.get('actual_status', ''))
except: print('parse_err')" 2>/dev/null || echo "")
    if [ "$STATUS" = "running" ]; then
        SSH_HOST=$(echo "$INFO" | python3 -c "import json,sys;
try: d=json.load(sys.stdin); print(d.get('ssh_host','') or d.get('public_ipaddr',''))
except: pass" 2>/dev/null || echo "")
        SSH_PORT=$(echo "$INFO" | python3 -c "import json,sys;
try: d=json.load(sys.stdin); print(d.get('ssh_port','') or d.get('direct_port_start',''))
except: pass" 2>/dev/null || echo "")
        if [ -n "$SSH_HOST" ] && [ -n "$SSH_PORT" ]; then
            if ssh -i "$VAST_SSH_KEY" -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o ConnectTimeout=10 -p "$SSH_PORT" "root@$SSH_HOST" 'echo READY' 2>&1 | grep -q READY; then
                echo "  SSH ready: $SSH_HOST:$SSH_PORT (${i}x5s)"
                break
            fi
            SSH_HOST=""
        fi
    fi
    echo "  ... $i/160 status=$STATUS"
    sleep 5
done
[ -z "$SSH_HOST" ] && { echo "ERROR: SSH not ready"; exit 1; }

SSH_OPTS="-i $VAST_SSH_KEY -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o ServerAliveInterval=60"
SSH_CMD="ssh $SSH_OPTS -p $SSH_PORT root@$SSH_HOST"
SCP_CMD="scp $SSH_OPTS -P $SSH_PORT -o ConnectTimeout=3600"

echo "[5/9] Uploading v3 ..."
$SSH_CMD 'mkdir -p /workspace/anima/training /workspace/anima/corpus /workspace/anima/output /workspace/anima/probe'
$SCP_CMD "$LOCAL_DIR/mitosis_model_v5.py" "root@$SSH_HOST:/workspace/anima/training/"
$SCP_CMD "$LOCAL_DIR/train_v5mitosis_cotrain_v2.py" "root@$SSH_HOST:/workspace/anima/training/"
$SCP_CMD "$LOCAL_DIR/train_v5mitosis_cotrain_v3.py" "root@$SSH_HOST:/workspace/anima/training/"
$SCP_CMD "$LOCAL_DIR/corpus_persona_balanced.txt" "root@$SSH_HOST:/workspace/anima/corpus/"
$SCP_CMD "$LOCAL_DIR/identity_probe.jsonl" "root@$SSH_HOST:/workspace/anima/probe/"

echo "[7/9] Train v3 (anneal $LAMBDA_INIT → $LAMBDA_FINAL via $LAMBDA_SCHEDULE)..."
$SSH_CMD "cd /workspace/anima && export PYTHONUNBUFFERED=1 && python3 training/train_v5mitosis_cotrain_v3.py \
    --corpus corpus/corpus_persona_balanced.txt \
    --output-dir output \
    --steps $STEPS \
    --batch $BATCH \
    --ctx $CTX \
    --lr $LR \
    --warmup $WARMUP \
    --d-model $D_MODEL \
    --n-head $N_HEAD \
    --ffn-dim $FFN_DIM \
    --initial-cells $INITIAL_CELLS \
    --max-cells $MAX_CELLS \
    --readout-mode $READOUT_MODE \
    --seed $SEED \
    --log-every 50 \
    --ckpt-every 5000 \
    --cost-cap-usd $COST_CAP_USD \
    --cost-per-hr $OFFER_DPH \
    --estimated-wall-hr $ESTIMATED_WALL_HR \
    --identity-probe probe/identity_probe.jsonl \
    --lambda-init $LAMBDA_INIT \
    --lambda-final $LAMBDA_FINAL \
    --lambda-schedule $LAMBDA_SCHEDULE \
    --n-perms $N_PERMS 2>&1 | tee train_v3.log" 2>&1 | tee dispatch_v3.log

echo "[8/9] Downloading..."
mkdir -p "$LOCAL_DIR/ckpts"
PULL_OK=1
$SCP_CMD "root@$SSH_HOST:/workspace/anima/output/ckpt_final.pt" "$LOCAL_DIR/ckpts/ckpt_v5mitosis_cotrain_v3.pt" || PULL_OK=0
$SCP_CMD "root@$SSH_HOST:/workspace/anima/output/cotrain_v3_result.json" "$LOCAL_DIR/cotrain_v3_result.json" || PULL_OK=0
$SCP_CMD "root@$SSH_HOST:/workspace/anima/train_v3.log" "$LOCAL_DIR/train_v3.log" || PULL_OK=0
[ $PULL_OK -eq 0 ] && SAVE_POD=1

echo "[9/9] DONE"
date -u
if [ -f "$LOCAL_DIR/cotrain_v3_result.json" ]; then
    python3 -c "
import json
d = json.load(open('$LOCAL_DIR/cotrain_v3_result.json'))
t = d.get('training', {})
p4 = d.get('f_persona_4_with_null', {})
print(f'  wall={t.get(\"wall_hours\",0):.2f}hr cost=\${t.get(\"cost_usd_actual\",0):.2f}')
print(f'  ce={t.get(\"ce_final_avg100\",0):.3f} ent={t.get(\"ent_final_avg100\",0):.3f}/{t.get(\"log_N_target\",0):.3f}')
print(f'  wmax={t.get(\"wmax_final_avg100\",0):.4f} λ_final={t.get(\"lambda_final_avg100\",0):.3f}')
print(f'  F-PERSONA-4: {p4.get(\"verdict\")} KL={p4.get(\"mean_kl\",0):.4f} z={p4.get(\"z_score_vs_null\",0):.2f} p={p4.get(\"p_value_one_sided\",0):.4f}')
"
fi
