#!/bin/bash
# state/anima_v5mitosis_cotrain_v3_routing_2026_05_12/dispatch_h100_v3_routing.sh
#
# Phase 3 follow-up — v3 ARCHITECTURAL ROUTING FIX on H100 (path g).
#
# v1 (PSCC §44) / v2 entropy-reg λ=0.1 (PSCC §45-FINAL) / per-cat SMALL (§48) /
# softmax-T sweep (§47): ALL hit F-PERSONA-4a routing KL≈0 (winner-take-all
# softmax over scalar cell tensions, no learnable router). Root cause = the
# routing layer has (a) no input-dependence and (b) plain saturating softmax.
#
# v3-routing fix (recommended g2+g3 = Switch/Mixtral pattern):
#   - learnable Linear router on the pooled cell-input embedding (input-dependent!)
#   - HARD TOP-K MoE gating (top-K=4 active cells per input, renormalized)
#   - load-balancing aux loss (Switch style, α=0.01)
#   - + annealed gate-entropy reg λ_init=1.0 → λ_final=0.01 (cosine) as 2nd pressure
#
# Reference: dispatch_h100_v3.sh + dispatch_h100_v2.sh (PSCC §45 infra) +
#   state/anima_phase1a4_lr5e6_2026_05_12/dispatch_vast_v2.sh (PSCC §46 direct-IP fix)
#   memory feedback_no_scale_caps + feedback_orchestrator_h100_gotchas +
#   feedback_dispatch_vast_template_gotchas.
#
# To fire:  bash dispatch_h100_v3_routing.sh
# Env overrides: STEPS BATCH CTX LR WARMUP D_MODEL N_HEAD FFN_DIM MAX_CELLS
#                TOP_K AUX_ALPHA LAMBDA_INIT LAMBDA_FINAL LAMBDA_SCHEDULE
#                COST_CAP_USD COST_PER_HR_MAX SEED N_PERMS  SAVE_POD=1 (keep pod)

set -euo pipefail

PHASE_ID="${PHASE_ID:-v5mitosis_cotrain_v3_routing}"
LOCAL_DIR="${LOCAL_DIR:-/Users/ghost/core/anima/state/anima_v5mitosis_cotrain_v3_routing_2026_05_12}"
SRC_DIR="${SRC_DIR:-/Users/ghost/core/anima/state/anima_v5mitosis_cotrain_2026_05_12}"
PHASE_LABEL="${PHASE_LABEL:-anima-v5mit-v3routing}"

# ── arch (no scale caps — modest d=384/cells=64 for clean v1/v2 comparison;
#    bump D_MODEL=768 MAX_CELLS=128 STEPS=10000 via env if desired) ──
STEPS="${STEPS:-8000}"
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
# ── routing fix ──
TOP_K="${TOP_K:-4}"
AUX_ALPHA="${AUX_ALPHA:-0.01}"
LAMBDA_INIT="${LAMBDA_INIT:-1.0}"
LAMBDA_FINAL="${LAMBDA_FINAL:-0.01}"
LAMBDA_SCHEDULE="${LAMBDA_SCHEDULE:-cosine}"
N_PERMS="${N_PERMS:-100}"

COST_CAP_USD="${COST_CAP_USD:-8.0}"
COST_PER_HR_MAX="${COST_PER_HR_MAX:-5.0}"
ESTIMATED_WALL_HR="${ESTIMATED_WALL_HR:-1.5}"
ABSOLUTE_MAX_USD=$(python3 -c "print($COST_CAP_USD * 1.10)")
# GPU class filter: prefer H100, fall back to A100 SXM (H100 SXM marketplace
# frequently empty within reliability+budget). d=384/cells=64 run fits A100 40GB easily.
GPU_FILTER="${GPU_FILTER:-gpu_name in [H100_SXM,H100_PCIE,H100_NVL,A100_SXM4,A100_PCIE,H200] num_gpus=1 reliability>0.95 dph_total<${COST_PER_HR_MAX} disk_space>50 inet_down>100}"

VAST_SSH_KEY="/Users/ghost/.vast/ssh/vast-key"
VASTAI="/Users/ghost/.local/bin/vastai"
[ -x "$VASTAI" ] || VASTAI="/Users/ghost/Library/Python/3.14/bin/vastai"
[ -x "$VASTAI" ] || VASTAI="/Users/ghost/Library/Python/3.13/bin/vastai"
[ -x "$VASTAI" ] || { echo "ERROR: vastai CLI not found"; exit 1; }

mkdir -p "$LOCAL_DIR/ckpts"
cd "$LOCAL_DIR"
echo "=== ${PHASE_ID} vast.ai H100 dispatch (routing fix g2+g3) ==="
date -u
echo "  steps=$STEPS d_model=$D_MODEL cells=${INITIAL_CELLS}-${MAX_CELLS} batch=$BATCH ctx=$CTX"
echo "  ROUTING: top_k=$TOP_K aux_alpha=$AUX_ALPHA λ_init=$LAMBDA_INIT λ_final=$LAMBDA_FINAL sched=$LAMBDA_SCHEDULE"
echo "  cost_cap=\$$COST_CAP_USD absolute_max=\$$ABSOLUTE_MAX_USD"

echo "[1/9] Searching GPU offers ($GPU_FILTER) ..."
OFFER_JSON=$($VASTAI search offers "$GPU_FILTER" -o dph_total --raw 2>&1)
OFFER_PARSED=$(echo "$OFFER_JSON" | python3 -c "
import json, sys
try: data = json.load(sys.stdin)
except Exception as e: sys.stderr.write(f'parse_err: {e}\n'); sys.exit(1)
if not data: sys.stderr.write('no_offers\n'); sys.exit(1)
b = data[0]
print(f'{b[\"id\"]} {b[\"dph_total\"]:.4f} {b[\"gpu_name\"]} {b.get(\"reliability\",0):.3f}')
")
OFFER_ID=$(echo "$OFFER_PARSED" | awk '{print $1}')
OFFER_DPH=$(echo "$OFFER_PARSED" | awk '{print $2}')
echo "  Selected: id=$OFFER_ID dph=\$$OFFER_DPH gpu=$(echo "$OFFER_PARSED" | awk '{print $3}')"

EST_COST=$(python3 -c "print(round($OFFER_DPH * $ESTIMATED_WALL_HR, 2))")
EXCEEDS=$(python3 -c "print('YES' if $EST_COST > $ABSOLUTE_MAX_USD else 'NO')")
if [ "$EXCEEDS" = "YES" ]; then echo "[ABORT] est_cost \$$EST_COST > absolute_max \$$ABSOLUTE_MAX_USD"; exit 1; fi
echo "[2/9] cost gate OK (est \$$EST_COST)"

echo "[3/9] Renting..."
CREATE_OUT=$($VASTAI create instance "$OFFER_ID" \
    --image pytorch/pytorch:2.5.1-cuda12.1-cudnn9-runtime \
    --disk 50 --ssh --direct --label "$PHASE_LABEL" --raw 2>&1)
INSTANCE_ID=$(echo "$CREATE_OUT" | python3 -c "
import json, sys
try: d=json.load(sys.stdin)
except Exception: sys.stderr.write('parse_fail\n'); sys.exit(1)
print(d.get('new_contract', d.get('contract_id', d.get('id', ''))))
")
[ -z "$INSTANCE_ID" ] && { echo "ERROR: parse instance id from: $CREATE_OUT"; exit 1; }
echo "  Instance ID: $INSTANCE_ID"
echo "$INSTANCE_ID" > vast_instance_id.txt

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

echo "[4/9] Waiting SSH (direct-IP) ..."
SSH_HOST=""; SSH_PORT=""
for i in $(seq 1 160); do
    INFO=$($VASTAI show instance "$INSTANCE_ID" --raw 2>/dev/null || true)
    [ -z "$INFO" ] && INFO="{}"
    STATUS=$(echo "$INFO" | python3 -c "import json,sys
try: d=json.load(sys.stdin); print(d.get('actual_status',''))
except: print('parse_err')" 2>/dev/null || echo "")
    if [ "$STATUS" = "running" ]; then
        SSH_HOST=$(echo "$INFO" | python3 -c "import json,sys
try:
 d=json.load(sys.stdin); print(d.get('public_ipaddr','') or d.get('ssh_host',''))
except: pass" 2>/dev/null || echo "")
        SSH_PORT=$(echo "$INFO" | python3 -c "import json,sys
try:
 d=json.load(sys.stdin)
 p=d.get('direct_port_start','')
 if not p:
  pm=d.get('ports',{}) or {}
  v=pm.get('22/tcp') or pm.get('22/tcp'.replace('/tcp',''))
  if v and isinstance(v,list) and v: p=v[0].get('HostPort','')
 if not p: p=d.get('ssh_port','')
 print(p)
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
[ -z "$SSH_HOST" ] && { echo "ERROR: SSH not ready"; SAVE_POD=1; exit 1; }
echo "$SSH_HOST:$SSH_PORT" > vast_ssh.txt

SSH_OPTS="-i $VAST_SSH_KEY -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o ServerAliveInterval=60"
SSH_CMD="ssh $SSH_OPTS -p $SSH_PORT root@$SSH_HOST"
SCP_CMD="scp $SSH_OPTS -P $SSH_PORT -o ConnectTimeout=3600"

echo "[5/9] Uploading code+corpus+probe ..."
$SSH_CMD 'mkdir -p /workspace/anima/training /workspace/anima/corpus /workspace/anima/output /workspace/anima/probe'
$SCP_CMD "$SRC_DIR/mitosis_model_v5.py" "root@$SSH_HOST:/workspace/anima/training/"
$SCP_CMD "$LOCAL_DIR/train_v5mitosis_cotrain_v3_routing.py" "root@$SSH_HOST:/workspace/anima/training/"
$SCP_CMD "$SRC_DIR/corpus_persona_balanced.txt" "root@$SSH_HOST:/workspace/anima/corpus/"
$SCP_CMD "$SRC_DIR/identity_probe.jsonl" "root@$SSH_HOST:/workspace/anima/probe/"

echo "[6/9] (image already has torch — skip pip install)"

echo "[7/9] Train v3-routing ..."
$SSH_CMD "cd /workspace/anima && export PYTHONUNBUFFERED=1 && python3 training/train_v5mitosis_cotrain_v3_routing.py \
    --corpus corpus/corpus_persona_balanced.txt \
    --output-dir output \
    --steps $STEPS --batch $BATCH --ctx $CTX --lr $LR --warmup $WARMUP \
    --d-model $D_MODEL --n-head $N_HEAD --ffn-dim $FFN_DIM \
    --initial-cells $INITIAL_CELLS --max-cells $MAX_CELLS --readout-mode $READOUT_MODE \
    --seed $SEED --log-every 50 --ckpt-every 2000 \
    --cost-cap-usd $COST_CAP_USD --cost-per-hr $OFFER_DPH --estimated-wall-hr $ESTIMATED_WALL_HR \
    --identity-probe probe/identity_probe.jsonl \
    --top-k $TOP_K --aux-alpha $AUX_ALPHA \
    --lambda-init $LAMBDA_INIT --lambda-final $LAMBDA_FINAL --lambda-schedule $LAMBDA_SCHEDULE \
    --n-perms $N_PERMS 2>&1 | tee train_v3_routing.log" 2>&1 | tee dispatch_v3_routing.log

echo "[8/9] Downloading (MANDATORY before pod delete — memory feedback_orchestrator_h100_gotchas) ..."
PULL_OK=1
$SCP_CMD "root@$SSH_HOST:/workspace/anima/output/ckpt_final.pt" "$LOCAL_DIR/ckpts/ckpt_v5mitosis_cotrain_v3_routing.pt" || PULL_OK=0
$SCP_CMD "root@$SSH_HOST:/workspace/anima/output/cotrain_v3_routing_result.json" "$LOCAL_DIR/cotrain_v3_routing_result.json" || PULL_OK=0
$SCP_CMD "root@$SSH_HOST:/workspace/anima/train_v3_routing.log" "$LOCAL_DIR/train_v3_routing.log" || PULL_OK=0
# bonus: mid-run ckpts (best-effort)
$SCP_CMD "root@$SSH_HOST:/workspace/anima/output/ckpt_step_*.pt" "$LOCAL_DIR/ckpts/" 2>/dev/null || true
if [ $PULL_OK -eq 0 ]; then
    echo "[WARN] pull failed — SETTING SAVE_POD=1 (pod retained for manual recovery)"
    SAVE_POD=1
fi

echo "[9/9] DONE"
date -u
if [ -f "$LOCAL_DIR/cotrain_v3_routing_result.json" ]; then
    python3 -c "
import json
d = json.load(open('$LOCAL_DIR/cotrain_v3_routing_result.json'))
t = d.get('training', {}); rf = d.get('routing_fix', {})
a = d.get('f_persona_4a_routing', {}); aw = a.get('topk_weights', {})
b = d.get('f_persona_4b_content', {}); fv = d.get('f_v5mit_regression', {})
print(f'  routing: top_k={rf.get(\"top_k\")} aux_alpha={rf.get(\"aux_alpha\")} λ {rf.get(\"lambda_init\")}→{rf.get(\"lambda_final\")}')
print(f'  wall={t.get(\"wall_hours\",0):.2f}hr cost=\${t.get(\"cost_usd_actual\",0):.2f} ce={t.get(\"ce_final_avg100\",0):.3f}')
print(f'  wmax={t.get(\"wmax_final_avg100\",0):.4f} active>.01={t.get(\"n_active_gt01_final_avg100\",0):.1f}/{t.get(\"n_cells_final\")} gate_max={t.get(\"gate_max_final_avg100\",0):.3f} aux={t.get(\"aux_final_avg100\",0):.3f}')
print(f'  F-PERSONA-4a routing: {a.get(\"verdict\")} KL={aw.get(\"mean_kl\",0):.4f} z={aw.get(\"z_score_vs_null\",0):.2f} p={aw.get(\"p_value_one_sided\",0):.4f}')
print(f'  F-PERSONA-4b content: {b.get(\"verdict\")} z={b.get(\"z_score_vs_null\",0):.2f} (v2 carry z={b.get(\"v2_carry_z\",0):.2f})')
print(f'  F-V5MIT-1..5: {fv.get(\"verdict\")}')
"
fi
