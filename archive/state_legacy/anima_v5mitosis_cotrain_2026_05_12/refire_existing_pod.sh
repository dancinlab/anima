#!/bin/bash
# refire_existing_pod.sh — re-fire training on already-rented pod
# (pod was retained by SAVE_POD=1 trap after device-mismatch fix).
#
# usage: bash refire_existing_pod.sh

set -euo pipefail

PHASE_ID="v5mitosis_cotrain"
LOCAL_DIR="/Users/ghost/core/anima/state/anima_v5mitosis_cotrain_2026_05_12"
INSTANCE_ID=$(cat "$LOCAL_DIR/vast_instance_id.txt")
SSH_HOST_PORT=$(cat "$LOCAL_DIR/vast_ssh.txt")
SSH_HOST=$(echo "$SSH_HOST_PORT" | cut -d: -f1)
SSH_PORT=$(echo "$SSH_HOST_PORT" | cut -d: -f2)

VAST_SSH_KEY="/Users/ghost/.vast/ssh/vast-key"
VASTAI="/Users/ghost/Library/Python/3.14/bin/vastai"

SSH_OPTS="-i $VAST_SSH_KEY -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o ServerAliveInterval=60"
SSH_CMD="ssh $SSH_OPTS -p $SSH_PORT root@$SSH_HOST"
SCP_CMD="scp $SSH_OPTS -P $SSH_PORT -o ConnectTimeout=3600"

# Hyperparams (same as dispatch_h100.sh)
STEPS=5000
BATCH=32
CTX=256
LR=1e-4
WARMUP=500
D_MODEL=384
N_HEAD=6
FFN_DIM=1536
INITIAL_CELLS=2
MAX_CELLS=64
READOUT_MODE=a_minus_g
SEED=42
COST_CAP_USD=40.0
ESTIMATED_WALL_HR=10.0
OFFER_DPH=2.2814

cd "$LOCAL_DIR"

echo "=== refire on existing pod $INSTANCE_ID at $SSH_HOST:$SSH_PORT ==="
date -u

cleanup() {
    local exit_code=$?
    if [ "${SAVE_POD:-0}" = "1" ]; then
        echo "[cleanup] SAVE_POD=1 — keeping instance $INSTANCE_ID (manual destroy required)"
    else
        echo "[cleanup] Destroying instance $INSTANCE_ID (exit=$exit_code)..."
        $VASTAI destroy instance "$INSTANCE_ID" 2>&1 | head -3 || true
    fi
}
trap cleanup EXIT INT TERM

# 1) Sanity verify fix is on pod
echo "[1/4] Verify device fix on pod..."
$SSH_CMD 'grep -c "Move child to parent" /workspace/anima/training/mitosis_model_v5.py' | head -1
echo

# Also re-upload the train script if it has any path-related changes (defensive)
echo "[1b] Re-upload train_v5mitosis_cotrain.py (defensive)..."
$SCP_CMD "$LOCAL_DIR/train_v5mitosis_cotrain.py" "root@$SSH_HOST:/workspace/anima/training/" 2>&1 | tail -2

# Clear stale output dir
$SSH_CMD 'rm -rf /workspace/anima/output && mkdir -p /workspace/anima/output' 2>&1 | tail -2

# 2) Train
echo "[2/4] Cotrain ($STEPS steps, batch=$BATCH, ctx=$CTX, lr=$LR)..."
$SSH_CMD "cd /workspace/anima && export PYTHONUNBUFFERED=1 && python3 training/train_v5mitosis_cotrain.py \
    --corpus corpus/corpus_color_cosmology.txt \
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
    --ckpt-every 1000 \
    --cost-cap-usd $COST_CAP_USD \
    --cost-per-hr $OFFER_DPH \
    --estimated-wall-hr $ESTIMATED_WALL_HR \
    --identity-probe probe/identity_probe.jsonl 2>&1 | tee train.log" 2>&1 | tee dispatch_refire.log

TRAIN_EXIT=${PIPESTATUS[0]}
echo "  train exit code = $TRAIN_EXIT"

# 3) Pull artifacts
echo "[3/4] Downloading artifacts..."
mkdir -p "$LOCAL_DIR/ckpts"
PULL_OK=1
$SCP_CMD "root@$SSH_HOST:/workspace/anima/output/ckpt_final.pt" "$LOCAL_DIR/ckpts/ckpt_${PHASE_ID}_cotrain.pt" || PULL_OK=0
$SCP_CMD "root@$SSH_HOST:/workspace/anima/output/cotrain_result.json" "$LOCAL_DIR/cotrain_result.json" || PULL_OK=0
$SCP_CMD "root@$SSH_HOST:/workspace/anima/train.log" "$LOCAL_DIR/train.log" || PULL_OK=0
$SCP_CMD "root@$SSH_HOST:/workspace/anima/output/ckpt_step_5000.pt" "$LOCAL_DIR/ckpts/" 2>/dev/null || true

if [ $PULL_OK -eq 0 ]; then
    echo "[WARN] artifact pull partial fail — retaining pod for manual recovery"
    SAVE_POD=1
fi

# 4) Summary
echo "[4/4] === ${PHASE_ID} refire DONE ==="
date -u
if [ -f "$LOCAL_DIR/cotrain_result.json" ]; then
    echo "Result summary:"
    python3 -c "
import json
with open('$LOCAL_DIR/cotrain_result.json') as f:
    d = json.load(f)
t = d.get('training', {})
fa = d.get('falsifier_aggregate', {})
p4 = d.get('f_persona_4_remeasure', {})
print(f'  wall: {t.get(\"wall_hours\",0):.2f}hr')
print(f'  cost: \${t.get(\"cost_usd_actual\",0):.2f}')
print(f'  cost_aborted: {t.get(\"cost_aborted\")}')
print(f'  steps actual: {t.get(\"steps_actual\")}')
print(f'  n_cells_final: {t.get(\"n_cells_final\")}')
print(f'  splits: {t.get(\"splits\")} merges: {t.get(\"merges\")}')
print(f'  loss initial->final: {t.get(\"loss_initial_avg100\"):.3f} -> {t.get(\"loss_final_avg100\"):.3f}')
print(f'  phi_best: {t.get(\"phi_best\",0):.3f}')
print(f'  falsifier: {fa.get(\"n_pass\")}/{fa.get(\"n_total\")} {fa.get(\"verdict\")}')
for fid in ['F-V5MIT-1','F-V5MIT-2','F-V5MIT-3','F-V5MIT-4','F-V5MIT-5']:
    f = d.get('falsifiers',{}).get(fid,{})
    print(f'    {fid}: passed={f.get(\"passed\")}')
print(f'  F-PERSONA-4 cotrained pool: {p4.get(\"verdict\")} mean_kl={p4.get(\"mean_kl\",0):.4f} (threshold=0.5)')
"
fi
echo "DONE"
