#!/bin/bash
# state/anima_v5mitosis_cotrain_v2_2026_05_12/dispatch_h100_v2.sh
#
# PSCC §46 BG-V5MIT-COTRAIN-V2 SCALE-UP fire — F-PERSONA-4 category specialization emergent.
# Vast.ai H100 (SXM/PCIe/NVL), no explicit cost cap per `feedback_no_scale_caps` directive.
#
# Scale-up vs v1 (PSCC §44):
#   d_model        384 → 768   (2× wider)
#   n_head         6   → 12
#   ffn_dim        1536→ 3072
#   max_cells      64  → 128   (no cap)
#   steps          5K  → 10K   (2× longer)
#   corpus         1.3MB → 18MB 5-category balanced
#   batch          32          (unchanged)
#   ctx            256         (unchanged)
#
# Estimated wall: 4-8hr H100 ≈ $10-25 (no cap, but soft envelope).
# trap cleanup: pod auto-destroy unless SAVE_POD=1.

set -euo pipefail

# ── CONFIG ──────────────────────────────────────────────────────────
PHASE_ID="v5mitosis_cotrain_v2"
LOCAL_DIR="/Users/ghost/core/anima/state/anima_v5mitosis_cotrain_v2_2026_05_12"
PHASE_LABEL="anima-v5mit-cotrain-v2"

# Hyperparams (SCALE-UP)
STEPS="${STEPS:-10000}"
BATCH="${BATCH:-32}"
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

# Cost envelope (memory feedback_no_scale_caps: no hard cap, soft only)
COST_CAP_USD="${COST_CAP_USD:-80.0}"        # soft envelope, train script uses this
COST_PER_HR_MAX="${COST_PER_HR_MAX:-4.0}"   # accept higher per-hr (H100 SXM)
ESTIMATED_WALL_HR="${ESTIMATED_WALL_HR:-12.0}"

# Pre-fire gate (no abort; just inform)
PRE_FIRE_ABSOLUTE_MAX="${PRE_FIRE_ABSOLUTE_MAX:-100.0}"

VAST_SSH_KEY="/Users/ghost/.vast/ssh/vast-key"
VASTAI="/Users/ghost/.local/bin/vastai"
[ -x "$VASTAI" ] || VASTAI="/Users/ghost/Library/Python/3.14/bin/vastai"
[ -x "$VASTAI" ] || { echo "ERROR: vastai CLI not found"; exit 1; }

# ──────────────────────────────────────────────────────────────────────
cd "$LOCAL_DIR"
echo "=== ${PHASE_ID} vast.ai H100 dispatch (Mac-local) ==="
date -u
echo "  steps=$STEPS batch=$BATCH ctx=$CTX lr=$LR warmup=$WARMUP"
echo "  d_model=$D_MODEL n_head=$N_HEAD ffn_dim=$FFN_DIM"
echo "  cells=${INITIAL_CELLS} to ${MAX_CELLS} readout=$READOUT_MODE"
echo "  cost_cap_soft=\$$COST_CAP_USD pre_fire_abs_max=\$$PRE_FIRE_ABSOLUTE_MAX"
echo "  estimated wall ${ESTIMATED_WALL_HR}hr"

# ── 1) Find best H100 offer ──────────────────────────────────────────
echo "[1/9] Searching H100 offers under \$${COST_PER_HR_MAX}/hr ..."
OFFER_JSON=$($VASTAI search offers \
    "gpu_name in [H100_SXM,H100_PCIE,H100_NVL] num_gpus=1 reliability>0.95 dph_total<${COST_PER_HR_MAX} disk_space>50 inet_down>200" \
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
OFFER_GPU=$(echo "$OFFER_PARSED" | awk '{print $3}')
echo "  Selected: id=$OFFER_ID dph=\$$OFFER_DPH gpu=$OFFER_GPU"

# ── 2) Pre-fire cost gate (soft) ────────────────────────────────────
EST_COST=$(python3 -c "print(round($OFFER_DPH * $ESTIMATED_WALL_HR, 2))")
echo "[2/9] Pre-fire cost gate (soft envelope) ..."
echo "  est_cost = $OFFER_DPH × $ESTIMATED_WALL_HR hr = \$$EST_COST"
echo "  pre_fire_abs_max = \$$PRE_FIRE_ABSOLUTE_MAX"
EXCEEDS=$(python3 -c "print('YES' if $EST_COST > $PRE_FIRE_ABSOLUTE_MAX else 'NO')")
if [ "$EXCEEDS" = "YES" ]; then
    echo "[ABORT] est_cost \$$EST_COST exceeds pre_fire_abs_max \$$PRE_FIRE_ABSOLUTE_MAX"
    echo "  (override: PRE_FIRE_ABSOLUTE_MAX=200 ./dispatch_h100_v2.sh)"
    exit 1
fi
echo "  ✓ within pre-fire envelope"

# ── 3) Rent instance ─────────────────────────────────────────────────
echo "[3/9] Renting instance..."
CREATE_OUT=$($VASTAI create instance "$OFFER_ID" \
    --image pytorch/pytorch:2.5.1-cuda12.1-cudnn9-runtime \
    --disk 60 --ssh --direct --label "$PHASE_LABEL" --raw 2>&1)
echo "  raw[head]: $(echo $CREATE_OUT | head -c 200)"
INSTANCE_ID=$(echo "$CREATE_OUT" | python3 -c "
import json, sys
try:
    d=json.load(sys.stdin)
except Exception:
    sys.stderr.write('parse_fail\n'); sys.exit(1)
print(d.get('new_contract', d.get('contract_id', d.get('id', ''))))
")
if [ -z "$INSTANCE_ID" ]; then
    echo "ERROR: could not parse instance id"; exit 1
fi
echo "  Instance ID: $INSTANCE_ID"
echo "$INSTANCE_ID" > vast_instance_id.txt

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

# ── 4) Wait for SSH ready ────────────────────────────────────────────
echo "[4/9] Waiting for SSH ready (max 13 min)..."
SSH_HOST=""
SSH_PORT=""
for i in $(seq 1 160); do
    INFO=$($VASTAI show instance "$INSTANCE_ID" --raw 2>/dev/null || true)
    [ -z "$INFO" ] && INFO="{}"
    STATUS=$(echo "$INFO" | python3 -c "import json,sys;
try: d=json.load(sys.stdin); print(d.get('actual_status', ''))
except: print('parse_err')" 2>/dev/null || echo "")
    if [ "$STATUS" = "running" ]; then
        SSH_HOST=$(echo "$INFO" | python3 -c "import json,sys;
try: d=json.load(sys.stdin); print(d.get('ssh_host', '') or d.get('public_ipaddr',''))
except: pass" 2>/dev/null || echo "")
        SSH_PORT=$(echo "$INFO" | python3 -c "import json,sys;
try: d=json.load(sys.stdin); print(d.get('ssh_port', '') or d.get('direct_port_start',''))
except: pass" 2>/dev/null || echo "")
        if [ -n "$SSH_HOST" ] && [ -n "$SSH_PORT" ]; then
            if ssh -i "$VAST_SSH_KEY" -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o ConnectTimeout=10 -p "$SSH_PORT" "root@$SSH_HOST" 'echo READY' 2>&1 | grep -q READY; then
                echo "  SSH ready: $SSH_HOST:$SSH_PORT (after ${i}x5s)"
                break
            fi
            SSH_HOST=""
        fi
    fi
    echo "  ... attempt $i/160, status=$STATUS"
    sleep 5
done

if [ -z "$SSH_HOST" ]; then
    echo "ERROR: SSH not ready after 160 attempts (~13 min)"; exit 1
fi
echo "$SSH_HOST:$SSH_PORT" > vast_ssh.txt

SSH_OPTS="-i $VAST_SSH_KEY -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o ServerAliveInterval=60"
SSH_CMD="ssh $SSH_OPTS -p $SSH_PORT root@$SSH_HOST"
SCP_CMD="scp $SSH_OPTS -P $SSH_PORT -o ConnectTimeout=3600"

# ── 5) Upload files Mac→vast ─────────────────────────────────────────
echo "[5/9] Uploading files (model + script + corpus 18MB + probe) ..."
$SSH_CMD 'mkdir -p /workspace/anima/training /workspace/anima/corpus /workspace/anima/output /workspace/anima/probe'

$SCP_CMD "$LOCAL_DIR/mitosis_model_v5.py" "root@$SSH_HOST:/workspace/anima/training/"
$SCP_CMD "$LOCAL_DIR/train_v5mitosis_cotrain.py" "root@$SSH_HOST:/workspace/anima/training/"
$SCP_CMD "$LOCAL_DIR/corpus_5cat_balanced.txt" "root@$SSH_HOST:/workspace/anima/corpus/"
$SCP_CMD "$LOCAL_DIR/identity_probe.jsonl" "root@$SSH_HOST:/workspace/anima/probe/"

# ── 6) Sanity check torch + GPU ──────────────────────────────────────
echo "[6/9] GPU + torch check..."
$SSH_CMD 'cd /workspace/anima && python3 -c "import torch; print(torch.__version__, torch.cuda.is_available(), torch.cuda.get_device_name(0), torch.cuda.get_device_properties(0).total_memory)"' | head -3

# ── 7) Train (cotrain v2 scale-up) ──────────────────────────────────
echo "[7/9] Cotrain v2 ($STEPS steps, batch=$BATCH, ctx=$CTX, lr=$LR, d=$D_MODEL, max_cells=$MAX_CELLS)..."
$SSH_CMD "cd /workspace/anima && export PYTHONUNBUFFERED=1 && python3 training/train_v5mitosis_cotrain.py \
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
    --identity-probe probe/identity_probe.jsonl 2>&1 | tee train.log" 2>&1 | tee dispatch.log

TRAIN_EXIT=${PIPESTATUS[0]}
echo "  train exit code = $TRAIN_EXIT"

# ── 8) Pull artifacts vast→Mac ──────────────────────────────────────
echo "[8/9] Downloading artifacts..."
mkdir -p "$LOCAL_DIR/ckpts"
PULL_OK=1
$SCP_CMD "root@$SSH_HOST:/workspace/anima/output/ckpt_final.pt" "$LOCAL_DIR/ckpts/ckpt_${PHASE_ID}_cotrain.pt" || PULL_OK=0
$SCP_CMD "root@$SSH_HOST:/workspace/anima/output/cotrain_result.json" "$LOCAL_DIR/cotrain_result.json" || PULL_OK=0
$SCP_CMD "root@$SSH_HOST:/workspace/anima/train.log" "$LOCAL_DIR/train.log" || PULL_OK=0
# Best-effort: intermediate ckpts (last only)
$SCP_CMD "root@$SSH_HOST:/workspace/anima/output/ckpt_step_10000.pt" "$LOCAL_DIR/ckpts/" 2>/dev/null || true
$SCP_CMD "root@$SSH_HOST:/workspace/anima/output/ckpt_step_8000.pt" "$LOCAL_DIR/ckpts/" 2>/dev/null || true

if [ $PULL_OK -eq 0 ]; then
    echo "[WARN] artifact pull partial fail — retaining pod for manual recovery"
    echo "[WARN] pod $INSTANCE_ID kept (SAVE_POD effectively=1)"
    SAVE_POD=1
fi

# ── 9) Summary ───────────────────────────────────────────────────────
echo "[9/9] === ${PHASE_ID} dispatch DONE ==="
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
print(f'  loss initial→final: {t.get(\"loss_initial_avg100\"):.3f} → {t.get(\"loss_final_avg100\"):.3f}')
print(f'  phi_best: {t.get(\"phi_best\",0):.3f}')
print(f'  falsifier: {fa.get(\"n_pass\")}/{fa.get(\"n_total\")} {fa.get(\"verdict\")}')
for fid in ['F-V5MIT-1','F-V5MIT-2','F-V5MIT-3','F-V5MIT-4','F-V5MIT-5']:
    f = d.get('falsifiers',{}).get(fid,{})
    print(f'    {fid}: passed={f.get(\"passed\")}')
print(f'  F-PERSONA-4 cotrained pool: {p4.get(\"verdict\")} mean_kl={p4.get(\"mean_kl\",0):.4f} (threshold=0.5)')
"
fi
echo "DONE"
