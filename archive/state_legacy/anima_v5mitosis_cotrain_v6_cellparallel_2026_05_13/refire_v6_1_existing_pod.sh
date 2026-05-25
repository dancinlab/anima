#!/bin/bash
# state/anima_v5mitosis_cotrain_v6_cellparallel_2026_05_13/refire_v6_1_existing_pod.sh
#
# v6.1 REFIRE — same retained pod 36635479, fix applied:
#   v6.0 crashed at step ~1000-1500 because rank-0-only mid-run SNAP +
#   final F-PERSONA called engine(x) (collective-dependent) while ranks 1-3
#   blocked at trailing dist.barrier(). NCCL watchdog 600s timeout fired.
#   v6.1 fix: removed mid-run SNAP; final F-PERSONA on ALL ranks (rank 0
#   computes stats, ranks 1-3 discard but participate in collectives).
#
# Resumes from ckpt_step_1000_rank{r}.pt? NO — fresh init for v6.1 (sharded
# ckpt load is TODO[ckpt-distribute]; cheaper to redo 1000 step than write
# the loader). Total cost: ~$25-30 (we lost ~$5 to v6.0 crash + retry).

set -euo pipefail

LOCAL_DIR="/Users/ghost/core/anima/state/anima_v5mitosis_cotrain_v6_cellparallel_2026_05_13"
TRAINING_DIR="/Users/ghost/core/anima/training"
SRC_DIR="/Users/ghost/core/anima/state/anima_v5mitosis_cotrain_2026_05_12"
SRC_V2_DIR="/Users/ghost/core/anima/state/anima_v5mitosis_cotrain_v2_2026_05_12"

INSTANCE_ID=$(cat "$LOCAL_DIR/vast_instance_id.txt")
SSH_HOST_PORT=$(cat "$LOCAL_DIR/vast_ssh.txt")
SSH_HOST=$(echo "$SSH_HOST_PORT" | cut -d: -f1)
SSH_PORT=$(echo "$SSH_HOST_PORT" | cut -d: -f2)

VAST_SSH_KEY="/Users/ghost/.vast/ssh/vast-key"
VASTAI="/Users/ghost/.local/bin/vastai"
[ -x "$VASTAI" ] || VASTAI="/Users/ghost/Library/Python/3.14/bin/vastai"
[ -x "$VASTAI" ] || VASTAI="/Users/ghost/Library/Python/3.13/bin/vastai"

SSH_OPTS="-i $VAST_SSH_KEY -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o ServerAliveInterval=60"
SSH_CMD="ssh $SSH_OPTS -p $SSH_PORT root@$SSH_HOST"
SCP_CMD="scp $SSH_OPTS -P $SSH_PORT -o ConnectTimeout=3600"

NUM_GPUS="${NUM_GPUS:-4}"
STEPS="${STEPS:-5000}"
BATCH="${BATCH:-8}"
CTX="${CTX:-512}"
LR="${LR:-1e-4}"
WARMUP="${WARMUP:-500}"
D_MODEL="${D_MODEL:-1024}"
N_HEAD="${N_HEAD:-16}"
FFN_DIM="${FFN_DIM:-4096}"
INITIAL_CELLS="${INITIAL_CELLS:-4}"
MAX_CELLS="${MAX_CELLS:-256}"
READOUT_MODE="${READOUT_MODE:-a_minus_g}"
SEED="${SEED:-42}"
TOP_K="${TOP_K:-8}"
AUX_ALPHA="${AUX_ALPHA:-0.01}"
LAMBDA_INIT="${LAMBDA_INIT:-1.0}"
LAMBDA_FINAL="${LAMBDA_FINAL:-0.01}"
LAMBDA_SCHEDULE="${LAMBDA_SCHEDULE:-cosine}"
N_PERMS="${N_PERMS:-100}"
CKPT_EVERY="${CKPT_EVERY:-1000}"
COST_CAP_USD="${COST_CAP_USD:-80.0}"
ESTIMATED_WALL_HR="${ESTIMATED_WALL_HR:-5.0}"

echo "=== v6.1 REFIRE on retained pod $INSTANCE_ID ($SSH_HOST:$SSH_PORT) ==="
date -u

cleanup() {
    local exit_code=$?
    if [ "${SAVE_POD:-0}" = "1" ]; then
        echo "[cleanup] SAVE_POD=1 — keeping instance $INSTANCE_ID (exit=$exit_code)"
    else
        echo "[cleanup] Destroying instance $INSTANCE_ID (exit=$exit_code)..."
        $VASTAI destroy instance "$INSTANCE_ID" 2>&1 | head -3 || true
    fi
}
trap cleanup EXIT INT TERM

echo "[1/5] Re-uploading v6.1 fixed trainer ..."
$SCP_CMD "$TRAINING_DIR/cotrain_v5mitosis_v6_cellparallel.py" "root@$SSH_HOST:/workspace/anima/training/"

echo "[2/5] Cleaning old output ..."
$SSH_CMD 'rm -rf /workspace/anima/output && mkdir -p /workspace/anima/output' 2>&1 | tail -1

# Pod cost so far check
COST_NOW=$($VASTAI show instance "$INSTANCE_ID" --raw 2>/dev/null | python3 -c "
import json, sys
try:
    d = json.load(sys.stdin)
    cph = d.get('dph_total', 0)
    started = d.get('start_date', 0) or 0
    import time
    elapsed_hr = (time.time() - started) / 3600.0 if started else 0
    print(f'{cph * elapsed_hr:.2f}')
except: print('0.0')
" 2>/dev/null || echo "0.0")
echo "  pod cost so far: ~\$$COST_NOW"

echo "[3/5] Train v6.1 ..."
TRAIN_RC=99
set +e
$SSH_CMD "set -o pipefail; cd /workspace/anima && export PYTHONUNBUFFERED=1 PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True && torchrun --nproc_per_node=$NUM_GPUS --rdzv-backend=c10d --rdzv-endpoint=localhost:29500 training/cotrain_v5mitosis_v6_cellparallel.py \
    --corpus corpus/corpus_5cat_balanced.txt \
    --output-dir output \
    --steps $STEPS --batch $BATCH --ctx $CTX --lr $LR --warmup $WARMUP \
    --d-model $D_MODEL --n-head $N_HEAD --ffn-dim $FFN_DIM \
    --initial-cells $INITIAL_CELLS --max-cells $MAX_CELLS --readout-mode $READOUT_MODE \
    --seed $SEED --log-every 50 --ckpt-every $CKPT_EVERY \
    --cost-cap-usd $COST_CAP_USD --cost-per-hr 6.6993 --estimated-wall-hr $ESTIMATED_WALL_HR \
    --identity-probe probe/identity_probe.jsonl \
    --top-k $TOP_K --aux-alpha $AUX_ALPHA \
    --lambda-init $LAMBDA_INIT --lambda-final $LAMBDA_FINAL --lambda-schedule $LAMBDA_SCHEDULE \
    --n-perms $N_PERMS 2>&1 | tee train_v6_1_cellparallel.log" 2>&1 | tee -a refire_v6_1_bg.log
TRAIN_RC=${PIPESTATUS[0]}
set -e
echo "[3/5] train rc=$TRAIN_RC"

echo "[4/5] Downloading artifacts ..."
PULL_OK=1
$SCP_CMD "root@$SSH_HOST:/workspace/anima/output/ckpt_final_rank*.pt" "$LOCAL_DIR/ckpts/" || PULL_OK=0
$SCP_CMD "root@$SSH_HOST:/workspace/anima/output/cotrain_v6_cellparallel_result.json" "$LOCAL_DIR/cotrain_v6_1_cellparallel_result.json" || PULL_OK=0
$SCP_CMD "root@$SSH_HOST:/workspace/anima/train_v6_1_cellparallel.log" "$LOCAL_DIR/train_v6_1_cellparallel.log" || PULL_OK=0
if [ $PULL_OK -eq 0 ]; then
    echo "[WARN] pull failed — SETTING SAVE_POD=1"
    SAVE_POD=1
fi

echo "[5/5] DONE"
date -u
if [ -f "$LOCAL_DIR/cotrain_v6_1_cellparallel_result.json" ]; then
    python3 -c "
import json
d = json.load(open('$LOCAL_DIR/cotrain_v6_1_cellparallel_result.json'))
t = d.get('training', {}); rf = d.get('routing_fix', {}); cfg = d.get('config', {})
a = d.get('f_persona_4a_routing', {}); aw = a.get('topk_weights', {})
b = d.get('f_persona_4b_content', {}); fv = d.get('f_v5mit_regression', {})
print(f'  arch: d={cfg.get(\"d_model\")} n_head={cfg.get(\"n_head\")} cells_max={cfg.get(\"max_cells\")}')
print(f'  distribution: world_size={d.get(\"world_size\")}')
print(f'  wall={t.get(\"wall_hours\",0):.2f}hr cost=\${t.get(\"cost_usd_actual\",0):.2f} ce={t.get(\"ce_final_avg100\",0):.3f}')
print(f'  step_wall_avg={t.get(\"step_wall_avg_seconds\",0)*1000:.0f}ms p50={t.get(\"step_wall_p50_ms\",0):.0f}ms')
print(f'  cells {cfg.get(\"initial_cells\")}->{t.get(\"n_cells_final\")} splits={t.get(\"splits\")}')
print(f'  F-PERSONA-4a routing: {a.get(\"verdict\")} KL={aw.get(\"mean_kl\",0):.4f} z={aw.get(\"z_score_vs_null\",0):.2f}')
print(f'  F-PERSONA-4b content: {b.get(\"verdict\")} z={b.get(\"z_score_vs_null\",0):.2f}')
print(f'  F-V5MIT-1..5: {fv.get(\"verdict\")}')
"
fi
