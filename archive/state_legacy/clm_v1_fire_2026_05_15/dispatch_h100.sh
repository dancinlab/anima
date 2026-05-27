#!/bin/bash
# state/clm_v1_fire_2026_05_15/dispatch_h100.sh — .clm v1 P2 fire dispatch
#
# User approval: "verbatim 없이 모두 승인" 2026-05-15 + "P2 all go H100 병렬 가능"
# W8 amendment: spec_frozen_v0.2 carry (n_layers=12 base only / kv_heads=8 MHA /
#                                        readout='a_only' / ctx 256 / cell_ffn=1024 / cells=2→64)
#
# Adapt of state/anima_v5mitosis_cotrain_2026_05_12/dispatch_h100.sh (proven $1.26 H100 SXM).
# Sources:
#   - training/clm_v1_model.py (ClmV1Model 12L base + mitosis branch)
#   - training/train_clm_v1_from_scratch.py (P2 trainer)
#   - state/anima_phase1a6_chat_v2_2026_05_15/corpus_v2.txt (121MB local)
#
# Cost envelope: $25-35 expected, $50 hard stop. CostGuard in trainer enforces in-job.
# Pod auto-destroy unless SAVE_POD=1.

set -euo pipefail

# ── CONFIG ──────────────────────────────────────────────────────────
PHASE_ID="clm_v1_fire"
LOCAL_DIR="/Users/ghost/core/anima/state/clm_v1_fire_2026_05_15"
ANIMA_ROOT="/Users/ghost/core/anima"
PHASE_LABEL="anima-clm-v1-fire"
CORPUS_LOCAL="$ANIMA_ROOT/state/anima_phase1a6_chat_v2_2026_05_15/corpus_v2.txt"

# Hyperparams (W8-amended spec)
STEPS="${STEPS:-5000}"
BATCH="${BATCH:-8}"
ACCUM="${ACCUM:-2}"
CTX="${CTX:-256}"
LR="${LR:-5e-4}"
WARMUP="${WARMUP:-500}"
D_MODEL="${D_MODEL:-768}"
N_LAYERS_BASE="${N_LAYERS_BASE:-12}"
N_HEAD="${N_HEAD:-8}"
FFN_DIM="${FFN_DIM:-3072}"
INITIAL_CELLS="${INITIAL_CELLS:-2}"
MAX_CELLS="${MAX_CELLS:-64}"
CELL_FFN_DIM="${CELL_FFN_DIM:-1024}"
SEED="${SEED:-42}"

# Cost envelope (user-approved cycle 88)
COST_CAP_USD="${COST_CAP_USD:-50.0}"
COST_PER_HR_MAX="${COST_PER_HR_MAX:-3.5}"
ESTIMATED_WALL_HR="${ESTIMATED_WALL_HR:-20.0}"  # A100 SXM4 ~30% slower than H100
ABSOLUTE_MAX_USD=$(python3 -c "print($COST_CAP_USD * 1.10)")

VAST_SSH_KEY="/Users/ghost/.vast/ssh/vast-key"
VASTAI="/Users/ghost/Library/Python/3.14/bin/vastai"
[ -x "$VASTAI" ] || { echo "ERROR: vastai CLI not found at $VASTAI"; exit 1; }
[ -f "$VAST_SSH_KEY" ] || { echo "ERROR: vast ssh key missing"; exit 1; }
[ -f "$CORPUS_LOCAL" ] || { echo "ERROR: corpus missing: $CORPUS_LOCAL"; exit 1; }

# Spec sha256 verify (W1 anchor)
EXPECTED_SHA="972e9987cd09118533161d5625ebde67a10aa5ec7f2e498bdbfca008a0f36ee5"
ACTUAL_SHA=$(shasum -a 256 "$ANIMA_ROOT/state/clm_v1_step4_spec_frozen_2026_05_15/spec_frozen.json" | awk '{print $1}')
if [ "$ACTUAL_SHA" != "$EXPECTED_SHA" ]; then
    echo "[ABORT] spec_frozen.json sha256 mismatch (W1 violation)"
    echo "  expected: $EXPECTED_SHA"; echo "  actual:   $ACTUAL_SHA"; exit 1
fi
echo "[OK] W1 spec sha256 verified ($EXPECTED_SHA)"

cd "$LOCAL_DIR"
echo "=== ${PHASE_ID} vast.ai H100 dispatch (cycle 88, 2026-05-15) ==="
date -u
echo "  steps=$STEPS batch=$BATCH accum=$ACCUM eff_batch=$((BATCH*ACCUM)) ctx=$CTX"
echo "  d_model=$D_MODEL layers_base=$N_LAYERS_BASE n_head=$N_HEAD ffn=$FFN_DIM"
echo "  cells=${INITIAL_CELLS}→${MAX_CELLS} cell_ffn=$CELL_FFN_DIM"
echo "  lr=$LR warmup=$WARMUP seed=$SEED"
echo "  cost_cap=\$$COST_CAP_USD absolute_max=\$$ABSOLUTE_MAX_USD"
echo "  estimated wall ${ESTIMATED_WALL_HR}hr"

# ── 1) GPU offer search (H100 → A100 SXM4 fallback if H100 unavailable) ──
echo "[1/9] Searching H100/A100 offers under \$${COST_PER_HR_MAX}/hr ..."
OFFER_JSON=$($VASTAI search offers \
    "gpu_name in [H100_SXM,H100_PCIE,H100_NVL,A100_SXM4,A100_PCIE] num_gpus=1 reliability>0.95 dph_total<${COST_PER_HR_MAX} disk_space>50 inet_down>200" \
    -o dph_total --raw 2>&1)
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
OFFER_GPU=$(echo "$OFFER_PARSED" | awk '{print $3}')
echo "  Selected: id=$OFFER_ID dph=\$$OFFER_DPH gpu=$OFFER_GPU"

# ── 2) Pre-fire cost gate ────────────────────────────────────────────
EST_COST=$(python3 -c "print(round($OFFER_DPH * $ESTIMATED_WALL_HR, 2))")
echo "[2/9] cost gate: est=\$$EST_COST  absolute_max=\$$ABSOLUTE_MAX_USD"
EXCEEDS=$(python3 -c "print('YES' if $EST_COST > $ABSOLUTE_MAX_USD else 'NO')")
if [ "$EXCEEDS" = "YES" ]; then
    echo "[ABORT] est_cost \$$EST_COST exceeds \$$ABSOLUTE_MAX_USD"; exit 1
fi
echo "  ✓ within budget"

# ── 3) Rent instance ─────────────────────────────────────────────────
echo "[3/9] Renting instance..."
CREATE_OUT=$($VASTAI create instance "$OFFER_ID" \
    --image pytorch/pytorch:2.5.1-cuda12.1-cudnn9-runtime \
    --disk 50 --ssh --direct --label "$PHASE_LABEL" --raw 2>&1)
INSTANCE_ID=$(echo "$CREATE_OUT" | python3 -c "
import json, sys
try: d=json.load(sys.stdin)
except: sys.stderr.write('parse_fail\n'); sys.exit(1)
print(d.get('new_contract', d.get('contract_id', d.get('id', ''))))
")
[ -z "$INSTANCE_ID" ] && { echo "ERROR: instance id parse failed"; exit 1; }
echo "  Instance ID: $INSTANCE_ID"
echo "$INSTANCE_ID" > vast_instance_id.txt

cleanup() {
    local rc=$?
    if [ "${SAVE_POD:-0}" = "1" ]; then
        echo "[cleanup] SAVE_POD=1 — keep instance $INSTANCE_ID"
    else
        echo "[cleanup] Destroying instance $INSTANCE_ID (exit=$rc)..."
        $VASTAI destroy instance "$INSTANCE_ID" 2>&1 | head -3 || true
    fi
}
trap cleanup EXIT INT TERM

# ── 4) Wait for SSH ──────────────────────────────────────────────────
echo "[4/9] Waiting for SSH (max 13 min)..."
SSH_HOST=""; SSH_PORT=""
for i in $(seq 1 160); do
    INFO=$($VASTAI show instance "$INSTANCE_ID" --raw 2>/dev/null || true)
    [ -z "$INFO" ] && INFO="{}"
    STATUS=$(echo "$INFO" | python3 -c "import json,sys
try: d=json.load(sys.stdin); print(d.get('actual_status',''))
except: print('parse_err')" 2>/dev/null || echo "")
    if [ "$STATUS" = "running" ]; then
        SSH_HOST=$(echo "$INFO" | python3 -c "import json,sys
try: d=json.load(sys.stdin); print(d.get('ssh_host','') or d.get('public_ipaddr',''))
except: pass" 2>/dev/null || echo "")
        SSH_PORT=$(echo "$INFO" | python3 -c "import json,sys
try: d=json.load(sys.stdin); print(d.get('ssh_port','') or d.get('direct_port_start',''))
except: pass" 2>/dev/null || echo "")
        if [ -n "$SSH_HOST" ] && [ -n "$SSH_PORT" ]; then
            if ssh -i "$VAST_SSH_KEY" -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null \
                -o ConnectTimeout=10 -p "$SSH_PORT" "root@$SSH_HOST" 'echo READY' 2>&1 | grep -q READY; then
                echo "  SSH ready: $SSH_HOST:$SSH_PORT (after ${i}x5s)"
                break
            fi
            SSH_HOST=""
        fi
    fi
    echo "  ... attempt $i/160 status=$STATUS"
    sleep 5
done
[ -z "$SSH_HOST" ] && { echo "ERROR: SSH not ready"; exit 1; }
echo "$SSH_HOST:$SSH_PORT" > vast_ssh.txt
SSH_OPTS="-i $VAST_SSH_KEY -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o ServerAliveInterval=60"
SSH_CMD="ssh $SSH_OPTS -p $SSH_PORT root@$SSH_HOST"
SCP_CMD="scp $SSH_OPTS -P $SSH_PORT -o ConnectTimeout=3600"

# ── 5) Upload ────────────────────────────────────────────────────────
echo "[5/9] Uploading sources + corpus..."
$SSH_CMD 'mkdir -p /workspace/anima/training /workspace/anima/corpus /workspace/anima/output'
$SCP_CMD "$ANIMA_ROOT/training/clm_v1_model.py" "root@$SSH_HOST:/workspace/anima/training/"
$SCP_CMD "$ANIMA_ROOT/training/train_clm_v1_from_scratch.py" "root@$SSH_HOST:/workspace/anima/training/"
$SCP_CMD "$CORPUS_LOCAL" "root@$SSH_HOST:/workspace/anima/corpus/corpus_v2.txt"
$SSH_CMD 'ls -la /workspace/anima/training /workspace/anima/corpus | head -10'

# ── 6) GPU + torch check ─────────────────────────────────────────────
echo "[6/9] GPU + torch sanity..."
$SSH_CMD 'cd /workspace/anima && python3 -c "import torch; print(torch.__version__, torch.cuda.is_available(), torch.cuda.get_device_name(0))"' | head -3

# ── 7) Train ─────────────────────────────────────────────────────────
echo "[7/9] Training ($STEPS steps batch=$BATCH accum=$ACCUM ctx=$CTX lr=$LR)..."
$SSH_CMD "cd /workspace/anima && export PYTHONUNBUFFERED=1 && python3 training/train_clm_v1_from_scratch.py \
    --corpus corpus/corpus_v2.txt \
    --output-dir output \
    --steps $STEPS \
    --batch $BATCH \
    --accum $ACCUM \
    --ctx $CTX \
    --lr $LR \
    --warmup $WARMUP \
    --d-model $D_MODEL \
    --n-layers-base $N_LAYERS_BASE \
    --n-head $N_HEAD \
    --ffn-dim $FFN_DIM \
    --initial-cells $INITIAL_CELLS \
    --max-cells $MAX_CELLS \
    --cell-ffn-dim $CELL_FFN_DIM \
    --seed $SEED \
    --log-every 50 \
    --ckpt-every 1000 \
    --bf16 \
    --cost-cap-usd $COST_CAP_USD \
    --cost-per-hr $OFFER_DPH \
    --estimated-wall-hr $ESTIMATED_WALL_HR 2>&1 | tee train.log" 2>&1 | tee dispatch.log || true
# g_fire_dispatch_robust: `|| true` neutralizes set -e false-positive
# (SSH pipe spurious exit 1 destroyed ckpt in cycle 88)

TRAIN_EXIT=${PIPESTATUS[0]:-0}
echo "  train exit code = $TRAIN_EXIT"

# ── 8) Pull artifacts (g_fire_dispatch_robust) ───────────────────────
echo "[8/9] Verifying result.json on remote + SAVE_POD auto-promote..."
SAVED=$($SSH_CMD 'test -f /workspace/anima/output/clm_v1_result.json && echo SAVED' 2>/dev/null || true)
if [ "$SAVED" = "SAVED" ]; then
    echo "  ✓ result.json exists on remote — SAVE_POD=1 auto-promote (ckpt protected until pulled)"
    SAVE_POD=1
else
    echo "  ⚠ result.json NOT found on remote — training may have failed (still SAVE_POD=1 for inspection)"
    SAVE_POD=1
fi

mkdir -p "$LOCAL_DIR/ckpts"
echo "[8/9] Pull artifacts (retry ≥3, 60s interval)..."
pull_with_retry() {
    local src="$1" dst="$2" tries=0
    while [ $tries -lt 3 ]; do
        if $SCP_CMD "root@$SSH_HOST:$src" "$dst" 2>&1; then
            echo "  ✓ pulled $src (try $((tries+1)))"
            return 0
        fi
        tries=$((tries+1))
        echo "  ... pull retry $tries/3 for $src"
        [ $tries -lt 3 ] && sleep 60
    done
    echo "  ✗ pull FAILED after 3 tries: $src"
    return 1
}
PULL_OK=1
pull_with_retry "/workspace/anima/output/ckpt_final.pt" "$LOCAL_DIR/ckpts/ckpt_${PHASE_ID}_final.pt" || PULL_OK=0
pull_with_retry "/workspace/anima/output/clm_v1_result.json" "$LOCAL_DIR/clm_v1_result.json" || PULL_OK=0
pull_with_retry "/workspace/anima/train.log" "$LOCAL_DIR/train.log" || PULL_OK=0
$SCP_CMD "root@$SSH_HOST:/workspace/anima/output/ckpt_step_5000.pt" "$LOCAL_DIR/ckpts/" 2>/dev/null || true

if [ $PULL_OK -eq 0 ]; then
    echo "[WARN] artifact pull partial fail — pod RETAINED (SAVE_POD=1)"
    echo "[WARN] manual recovery: ssh -i $VAST_SSH_KEY -p $SSH_PORT root@$SSH_HOST"
    echo "[WARN] then scp /workspace/anima/output/ckpt_final.pt locally + destroy instance $INSTANCE_ID"
    SAVE_POD=1
else
    echo "[OK] all artifacts pulled — destroying instance now (explicit, pre-trap)"
    $VASTAI destroy instance "$INSTANCE_ID" 2>&1 | head -3 || true
    SAVE_POD=1  # trap skip (already destroyed explicitly above)
fi

# ── 9) Summary ───────────────────────────────────────────────────────
echo "[9/9] === ${PHASE_ID} DONE ==="
date -u
if [ -f "$LOCAL_DIR/clm_v1_result.json" ]; then
    python3 -c "
import json
with open('$LOCAL_DIR/clm_v1_result.json') as f: d = json.load(f)
t = d.get('training', {}); fa = d.get('falsifier_aggregate', {})
print(f'  wall: {t.get(\"wall_hours\",0):.2f}hr')
print(f'  cost: \${t.get(\"cost_usd_actual\",0):.2f}')
print(f'  cost_aborted: {t.get(\"cost_aborted\")}')
print(f'  steps: {t.get(\"steps_actual\")} cells_final: {t.get(\"n_cells_final\")}')
print(f'  splits: {t.get(\"splits\")} merges: {t.get(\"merges\")}')
print(f'  loss: {t.get(\"loss_initial_avg100\"):.3f} → {t.get(\"loss_final_avg100\"):.3f}')
print(f'  phi_best: {t.get(\"phi_best\",0):.3f}')
print(f'  verdict: {fa.get(\"n_pass\")}/{fa.get(\"n_total\")} {fa.get(\"verdict\")}')
for fid in ['F-V5MIT-1','F-V5MIT-2','F-V5MIT-3','F-V5MIT-4','F-V5MIT-5']:
    f = d.get('falsifiers',{}).get(fid,{}); print(f'    {fid}: passed={f.get(\"passed\")}')
"
fi
echo "DONE"
