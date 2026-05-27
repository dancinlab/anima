#!/bin/bash
# state/anima_v5mitosis_cotrain_v4_scaleup_2026_05_12/refire_existing_pod.sh
#
# Refire v5-mitosis cotrain v4 on the retained pod (A100 SXM4 80GB) after OOM at step ~150
# (cells=66, batch=8, ctx=512, d=1024, cells_max=256 → 77.6 GB exhausted at `torch.stack(cell_outs)`).
#
# Two fixes:
#  (1) MEMORY: batch 8→2, ctx 512→256 (d=1024 / cells=256 headline PRESERVED — per-cell
#      activation graph at cells→256 dominates VRAM, so back off batch & ctx, not d/cells).
#      ~256 cells × (B×T×ffn_dim activation graph) at B=2 T=256 ≈ ~40-55 GB on 80 GB.
#  (2) WORKING OOM-RETRY: the original dispatch_h100_v4.sh OOM-retry was broken — the remote
#      `python ... 2>&1 | tee log` returns tee's exit (0) even when python OOM-crashes, so
#      the loop saw "rc=0" and never retried. FIX: remote `set -o pipefail` so the pipeline
#      exit = python's non-zero on crash. Plus an explicit log-grep for "out of memory".
#
# To fire:  bash refire_existing_pod.sh
# Env overrides: STEPS BATCH CTX LR WARMUP D_MODEL N_HEAD FFN_DIM MAX_CELLS INITIAL_CELLS
#                TOP_K AUX_ALPHA LAMBDA_INIT LAMBDA_FINAL LAMBDA_SCHEDULE CKPT_EVERY N_PERMS
#                OFFER_DPH ESTIMATED_WALL_HR COST_CAP_USD SAVE_POD=1 (keep pod)

set -euo pipefail

PHASE_ID="v5mitosis_cotrain_v4_scaleup"
LOCAL_DIR="/Users/ghost/core/anima/state/anima_v5mitosis_cotrain_v4_scaleup_2026_05_12"
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

# ── Hyperparams (d=1024 / cells=256 headline PRESERVED; batch & ctx backed off for OOM) ──
STEPS="${STEPS:-20000}"
BATCH="${BATCH:-2}"            # ← from 8 (OOM at cells=66); retry halves but min 1 here
CTX="${CTX:-256}"             # ← from 512 (halves per-cell activation graph)
LR="${LR:-1e-4}"
WARMUP="${WARMUP:-2000}"
D_MODEL="${D_MODEL:-1024}"
N_HEAD="${N_HEAD:-16}"
FFN_DIM="${FFN_DIM:-4096}"
INITIAL_CELLS="${INITIAL_CELLS:-2}"
MAX_CELLS="${MAX_CELLS:-256}"
READOUT_MODE="${READOUT_MODE:-a_minus_g}"
SEED="${SEED:-42}"
TOP_K="${TOP_K:-8}"
AUX_ALPHA="${AUX_ALPHA:-0.01}"
LAMBDA_INIT="${LAMBDA_INIT:-1.0}"
LAMBDA_FINAL="${LAMBDA_FINAL:-0.01}"
LAMBDA_SCHEDULE="${LAMBDA_SCHEDULE:-cosine}"
CKPT_EVERY="${CKPT_EVERY:-5000}"
N_PERMS="${N_PERMS:-100}"
COST_CAP_USD="${COST_CAP_USD:-40.0}"
ESTIMATED_WALL_HR="${ESTIMATED_WALL_HR:-12.0}"
OFFER_DPH="${OFFER_DPH:-0.9380}"

cd "$LOCAL_DIR"
echo "=== ${PHASE_ID} refire on existing pod $INSTANCE_ID at $SSH_HOST:$SSH_PORT ==="
echo "  d=$D_MODEL n_head=$N_HEAD ffn=$FFN_DIM cells=${INITIAL_CELLS}-${MAX_CELLS} batch=$BATCH ctx=$CTX steps=$STEPS"
echo "  ROUTING: top_k=$TOP_K aux_alpha=$AUX_ALPHA λ_init=$LAMBDA_INIT λ_final=$LAMBDA_FINAL"
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

echo "[1/4] Verify pod state + re-upload trainer (in case it was edited) ..."
$SSH_CMD 'ls -la /workspace/anima/corpus/corpus_5cat_balanced.txt /workspace/anima/training/mitosis_model_v5.py /workspace/anima/probe/identity_probe.jsonl 2>&1' | head -5
$SCP_CMD "/Users/ghost/core/anima/training/cotrain_v5mitosis_v4.py" "root@$SSH_HOST:/workspace/anima/training/"
$SSH_CMD 'rm -rf /workspace/anima/output && mkdir -p /workspace/anima/output' 2>&1 | tail -1

echo "[2/4] Train v4 (OOM-retry: batch halves on CUDA OOM down to 1; FIXED with remote set -o pipefail) ..."
TRAIN_RC=99
CUR_BATCH=$BATCH
for attempt in 1 2 3; do
    echo "  >>> attempt $attempt: batch=$CUR_BATCH ctx=$CTX"
    set +e
    $SSH_CMD "set -o pipefail; cd /workspace/anima && export PYTHONUNBUFFERED=1 PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True && python3 training/cotrain_v5mitosis_v4.py \
        --corpus corpus/corpus_5cat_balanced.txt \
        --output-dir output \
        --steps $STEPS --batch $CUR_BATCH --ctx $CTX --lr $LR --warmup $WARMUP \
        --d-model $D_MODEL --n-head $N_HEAD --ffn-dim $FFN_DIM \
        --initial-cells $INITIAL_CELLS --max-cells $MAX_CELLS --readout-mode $READOUT_MODE \
        --seed $SEED --log-every 50 --ckpt-every $CKPT_EVERY \
        --cost-cap-usd $COST_CAP_USD --cost-per-hr $OFFER_DPH --estimated-wall-hr $ESTIMATED_WALL_HR \
        --identity-probe probe/identity_probe.jsonl \
        --top-k $TOP_K --aux-alpha $AUX_ALPHA \
        --lambda-init $LAMBDA_INIT --lambda-final $LAMBDA_FINAL --lambda-schedule $LAMBDA_SCHEDULE \
        --n-perms $N_PERMS 2>&1 | tee train_v4_scaleup.log" 2>&1 | tee -a dispatch_v4_scaleup.log
    TRAIN_RC=${PIPESTATUS[0]}
    set -e
    OOM=$($SSH_CMD "grep -ci 'out of memory\|CUDA out of memory\|OutOfMemoryError' /workspace/anima/train_v4_scaleup.log 2>/dev/null || echo 0" 2>/dev/null || echo 0)
    if [ "$TRAIN_RC" = "0" ] && [ "${OOM:-0}" -eq 0 ]; then echo "  train OK (rc=0, no OOM)"; break; fi
    if [ "${OOM:-0}" -gt 0 ] && [ "$CUR_BATCH" -gt 1 ]; then
        CUR_BATCH=$(( CUR_BATCH / 2 )); [ "$CUR_BATCH" -lt 1 ] && CUR_BATCH=1
        echo "  [OOM detected] retry with batch=$CUR_BATCH"
        $SSH_CMD 'rm -rf /workspace/anima/output && mkdir -p /workspace/anima/output' 2>&1 | tail -1
        continue
    fi
    echo "  train rc=$TRAIN_RC oom_count=$OOM — no further retry"
    break
done

echo "[3/4] Pull artifacts (MANDATORY before pod delete) ..."
mkdir -p "$LOCAL_DIR/ckpts"
PULL_OK=1
$SCP_CMD "root@$SSH_HOST:/workspace/anima/output/ckpt_final.pt" "$LOCAL_DIR/ckpts/ckpt_v5mitosis_cotrain_v4_scaleup.pt" || PULL_OK=0
$SCP_CMD "root@$SSH_HOST:/workspace/anima/output/cotrain_v4_scaleup_result.json" "$LOCAL_DIR/cotrain_v4_scaleup_result.json" || PULL_OK=0
$SCP_CMD "root@$SSH_HOST:/workspace/anima/train_v4_scaleup.log" "$LOCAL_DIR/train_v4_scaleup.log" || PULL_OK=0
$SCP_CMD "root@$SSH_HOST:/workspace/anima/output/ckpt_step_*.pt" "$LOCAL_DIR/ckpts/" 2>/dev/null || true
if [ $PULL_OK -eq 0 ]; then echo "[WARN] pull failed — SETTING SAVE_POD=1 (pod retained)"; SAVE_POD=1; fi

echo "[4/4] === ${PHASE_ID} refire DONE ==="
date -u
if [ -f "$LOCAL_DIR/cotrain_v4_scaleup_result.json" ]; then
    python3 -c "
import json
d = json.load(open('$LOCAL_DIR/cotrain_v4_scaleup_result.json'))
t = d.get('training', {}); rf = d.get('routing_fix', {}); cfg = d.get('config', {})
a = d.get('f_persona_4a_routing', {}); aw = a.get('topk_weights', {})
b = d.get('f_persona_4b_content', {}); fv = d.get('f_v5mit_regression', {})
print(f'  arch: d={cfg.get(\"d_model\")} n_head={cfg.get(\"n_head\")} ffn={cfg.get(\"ffn_dim\")} cells_max={cfg.get(\"max_cells\")} ctx={cfg.get(\"max_seq\")}  n_params={d.get(\"n_params\")}')
print(f'  routing: top_k={rf.get(\"top_k\")} aux_alpha={rf.get(\"aux_alpha\")} λ {rf.get(\"lambda_init\")}→{rf.get(\"lambda_final\")}')
print(f'  wall={t.get(\"wall_hours\",0):.2f}hr cost=\${t.get(\"cost_usd_actual\",0):.2f} ce={t.get(\"ce_final_avg100\",0):.3f} cost_aborted={t.get(\"cost_aborted\")}')
print(f'  cells {cfg.get(\"initial_cells\")}->{t.get(\"n_cells_final\")} splits={t.get(\"splits\")} phi={t.get(\"phi_final\",0):.3f} phi_best={t.get(\"phi_best\",0):.3f}')
print(f'  wmax={t.get(\"wmax_final_avg100\",0):.4f} active>.01={t.get(\"n_active_gt01_final_avg100\",0):.1f}/{t.get(\"n_cells_final\")} gate_max={t.get(\"gate_max_final_avg100\",0):.3f} aux={t.get(\"aux_final_avg100\",0):.3f}')
print(f'  F-PERSONA-4a routing: {a.get(\"verdict\")} KL={aw.get(\"mean_kl\",0):.4f} z={aw.get(\"z_score_vs_null\",0):.2f} p={aw.get(\"p_value_one_sided\",0):.4f}')
sg = a.get(\"soft_gate\")
if sg: print(f'  F-PERSONA-4a soft gate: KL={sg.get(\"mean_kl\",0):.4f} z={sg.get(\"z_score_vs_null\",0):.2f}')
print(f'  F-PERSONA-4b content (M4 aggregated cosine): {b.get(\"verdict\")} z={b.get(\"z_score_vs_null\",0):.2f} (v2 carry z={b.get(\"v2_carry_z\",0):.2f})')
print(f'  F-V5MIT-1..5: {fv.get(\"verdict\")}')
"
fi
echo "DONE"
