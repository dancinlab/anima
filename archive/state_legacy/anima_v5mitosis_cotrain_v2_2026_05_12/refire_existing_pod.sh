#!/bin/bash
# state/anima_v5mitosis_cotrain_v2_2026_05_12/refire_existing_pod.sh
#
# Refire on retained pod 36617115 after OOM at step 100 (cells=42, batch=32,
# ctx=256, d=768, cells_max=128 → 93GB H100 NVL exhausted).
#
# Memory fix: batch 32 → 8 (4× reduction at stacked tensor), other hyperparams unchanged.
# Scale-up intent (corpus, d, cells, steps) preserved.

set -euo pipefail

PHASE_ID="v5mitosis_cotrain_v2"
LOCAL_DIR="/Users/ghost/core/anima/state/anima_v5mitosis_cotrain_v2_2026_05_12"
INSTANCE_ID=$(cat "$LOCAL_DIR/vast_instance_id.txt")
SSH_HOST_PORT=$(cat "$LOCAL_DIR/vast_ssh.txt")
SSH_HOST=$(echo "$SSH_HOST_PORT" | cut -d: -f1)
SSH_PORT=$(echo "$SSH_HOST_PORT" | cut -d: -f2)

VAST_SSH_KEY="/Users/ghost/.vast/ssh/vast-key"
VASTAI="/Users/ghost/.local/bin/vastai"
[ -x "$VASTAI" ] || VASTAI="/Users/ghost/Library/Python/3.14/bin/vastai"

SSH_OPTS="-i $VAST_SSH_KEY -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o ServerAliveInterval=60"
SSH_CMD="ssh $SSH_OPTS -p $SSH_PORT root@$SSH_HOST"
SCP_CMD="scp $SSH_OPTS -P $SSH_PORT -o ConnectTimeout=3600"

# Hyperparams (SCALE-UP preserved + batch reduced for OOM)
STEPS="${STEPS:-10000}"
BATCH="${BATCH:-8}"             # ← reduced from 32 (4× memory) for OOM fix
CTX="${CTX:-256}"
LR="${LR:-1e-4}"
WARMUP="${WARMUP:-1000}"
D_MODEL="${D_MODEL:-768}"
N_HEAD="${N_HEAD:-12}"
FFN_DIM="${FFN_DIM:-3072}"
INITIAL_CELLS="${INITIAL_CELLS:-2}"
MAX_CELLS="${MAX_CELLS:-128}"
READOUT_MODE="${READOUT_MODE:-a_minus_g}"
SEED="${SEED:-42}"
COST_CAP_USD="${COST_CAP_USD:-80.0}"
ESTIMATED_WALL_HR="${ESTIMATED_WALL_HR:-12.0}"
OFFER_DPH="${OFFER_DPH:-1.5201}"

cd "$LOCAL_DIR"

echo "=== refire on existing pod $INSTANCE_ID at $SSH_HOST:$SSH_PORT ==="
echo "  batch=$BATCH (reduced from 32 for OOM fix; other scale-up preserved)"
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

# 1) Sanity: verify scripts + corpus still on pod
echo "[1/4] Verify pod state..."
$SSH_CMD 'ls -la /workspace/anima/corpus/corpus_5cat_balanced.txt /workspace/anima/training/mitosis_model_v5.py /workspace/anima/training/train_v5mitosis_cotrain.py /workspace/anima/probe/identity_probe.jsonl 2>&1' | head -10

# Clear stale output dir (previous OOM left no ckpt anyway)
$SSH_CMD 'rm -rf /workspace/anima/output && mkdir -p /workspace/anima/output' 2>&1 | tail -2

# Set CUDA mem allocator config (helps fragmentation)
$SSH_CMD 'export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True; echo set'

# 2) Train (batch=8 OOM-safe)
echo "[2/4] Cotrain v2 refire ($STEPS steps, batch=$BATCH, ctx=$CTX, lr=$LR, d=$D_MODEL, max_cells=$MAX_CELLS)..."
$SSH_CMD "cd /workspace/anima && export PYTHONUNBUFFERED=1 PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True && python3 training/train_v5mitosis_cotrain.py \
    --corpus corpus/corpus_5cat_balanced.txt \
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
    --log-every 100 \
    --ckpt-every 2000 \
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
$SCP_CMD "root@$SSH_HOST:/workspace/anima/output/ckpt_step_10000.pt" "$LOCAL_DIR/ckpts/" 2>/dev/null || true
$SCP_CMD "root@$SSH_HOST:/workspace/anima/output/ckpt_step_8000.pt" "$LOCAL_DIR/ckpts/" 2>/dev/null || true

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
