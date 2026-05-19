#!/bin/bash
# dispatch_vast.sh — Phase 1A.4 cuda filter validation (eval-only).
#
# Derived from tool/dispatch_vast_mac_template.sh (PSCC §28 canonical).
# Purpose: validate anima_chat v2.3 markdown_filter on the §17 / §27-amendment
# cuda × bf16 × seed=42 path. NO SFT — Phase 1A.1 ckpt is used as-is.
#
# Provider: Vast.ai RTX 4090 (~$0.24-0.30/hr). Wall ~10-15min eval-only.
# Cost cap target: $0.10.
set -euo pipefail

# ── CONFIG ──────────────────────────────────────────────────────────────
PHASE_ID="phase1a4_cuda_filter_val"
LOCAL_DIR="/Users/ghost/core/anima/state/anima_phase1a4_cuda_filter_validation_2026_05_12"
PHASE1A1_DIR="/Users/ghost/core/anima/state/anima_phase1a1_color_cosmology_2026_05_12"
ANIMA_ROOT="/Users/ghost/core/anima"
TRAINING_DIR="$ANIMA_ROOT/training"
PHASE_LABEL="phase1a4-cuda-filter-val"

COST_CAP_USD="${COST_CAP_USD:-0.10}"
COST_PER_HR="${COST_PER_HR:-0.30}"
SEED="${SEED:-42}"

# Mac local binaries
VAST_SSH_KEY="/Users/ghost/.vast/ssh/vast-key"
VASTAI="/Users/ghost/.local/bin/vastai"
[ -x "$VASTAI" ] || VASTAI="/Users/ghost/Library/Python/3.14/bin/vastai"
[ -x "$VASTAI" ] || { echo "ERROR: vastai CLI not found"; exit 1; }
# ────────────────────────────────────────────────────────────────────────

cd "$LOCAL_DIR"

echo "=== ${PHASE_ID} vast.ai dispatch (Mac-local, EVAL-ONLY) ==="
date -u
echo "Cost cap: \$${COST_CAP_USD} | dph estimate: \$${COST_PER_HR}"

# ── 1) Find best RTX 4090 offer ─────────────────────────────────────────
echo "[1/7] Searching RTX 4090 offers under \$0.30/hr..."
OFFER=$($VASTAI search offers 'gpu_name=RTX_4090 num_gpus=1 reliability>0.98 dph_total<0.30 disk_space>30 inet_down>500' -o dph_total --raw 2>&1 | \
    python3 -c "
import json, sys
data = json.load(sys.stdin)
if not data:
    sys.stderr.write('no offers\n'); sys.exit(1)
print(data[0]['id'])
")
echo "  Selected offer ID: $OFFER"

# ── 2) Rent ─────────────────────────────────────────────────────────────
echo "[2/7] Renting instance..."
CREATE_OUT=$($VASTAI create instance "$OFFER" --image pytorch/pytorch:2.5.1-cuda12.1-cudnn9-runtime --disk 30 --ssh --direct --label "$PHASE_LABEL" --raw 2>&1)
echo "  raw: $CREATE_OUT" | head -2
INSTANCE_ID=$(echo "$CREATE_OUT" | python3 -c "
import json, sys
try:
    d=json.load(sys.stdin)
except Exception:
    sys.stderr.write('parse fail\n'); sys.exit(1)
print(d.get('new_contract', d.get('contract_id', d.get('id', ''))))
")
if [ -z "$INSTANCE_ID" ]; then
    echo "ERROR: could not parse instance id"; exit 1
fi
echo "  Instance ID: $INSTANCE_ID"
echo "$INSTANCE_ID" > vast_instance_id.txt

cleanup() {
    echo "[cleanup] Destroying instance $INSTANCE_ID..."
    $VASTAI destroy instance "$INSTANCE_ID" 2>&1 | head -3 || true
}
trap cleanup EXIT

# ── 3) Wait for SSH ready ───────────────────────────────────────────────
echo "[3/7] Waiting for SSH ready..."
SSH_HOST=""
SSH_PORT=""
for i in $(seq 1 80); do
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
    echo "  ... attempt $i/80, status=$STATUS"
    sleep 5
done

if [ -z "$SSH_HOST" ]; then
    echo "ERROR: SSH not ready"; exit 1
fi
echo "$SSH_HOST:$SSH_PORT" > vast_ssh.txt

SSH_OPTS="-i $VAST_SSH_KEY -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null"
SSH_CMD="ssh $SSH_OPTS -p $SSH_PORT root@$SSH_HOST"
SCP_CMD="scp $SSH_OPTS -P $SSH_PORT"

# ── 4) Upload eval script + anima_chat + arch + ckpt ────────────────────
echo "[4/7] Uploading files (eval script + anima_chat.py + arch + ckpt) Mac→vast..."
$SSH_CMD 'mkdir -p /workspace/anima/training /workspace/anima/ckpts /workspace/anima/output'

# anima_chat.py expects `from training.engine_a_g_arch import ...` so we mirror
# the local layout: /workspace/anima/anima_chat.py + /workspace/anima/training/engine_a_g_arch.py
$SCP_CMD "$ANIMA_ROOT/anima_chat.py" "root@$SSH_HOST:/workspace/anima/"
$SCP_CMD "$TRAINING_DIR/engine_a_g_arch.py" "root@$SSH_HOST:/workspace/anima/training/"
$SSH_CMD 'touch /workspace/anima/training/__init__.py'
$SCP_CMD "$LOCAL_DIR/v58_cuda_filter_compare.py" "root@$SSH_HOST:/workspace/anima/"
$SCP_CMD "$PHASE1A1_DIR/ckpts/ckpt_phase1a1_sft.pt" "root@$SSH_HOST:/workspace/anima/ckpts/"

# ── 5) Sanity: torch + GPU + anima_chat import ──────────────────────────
echo "[5/7] GPU + torch + anima_chat import sanity..."
$SSH_CMD 'cd /workspace/anima && python3 -c "import torch; print(torch.__version__, torch.cuda.is_available(), torch.cuda.get_device_name(0))"' | head -3
$SSH_CMD 'cd /workspace/anima && ANIMA_ROOT=/workspace/anima python3 -c "import sys; sys.path.insert(0,\"/workspace/anima\"); from anima_chat import AnimaChat; print(\"anima_chat OK\")"' | head -3

# ── 6) Eval (NO TRAIN) — cuda bf16 seed=42 filter on/off ───────────────
echo "[6/7] V5.8 4-mode × markdown_filter on/off eval (cuda bf16 seed=$SEED)..."
$SSH_CMD "cd /workspace/anima && export PYTHONUNBUFFERED=1 && export ANIMA_ROOT=/workspace/anima && python3 v58_cuda_filter_compare.py \
    --ckpt ckpts/ckpt_phase1a1_sft.pt \
    --output v58_4mode_cuda_filter_compare.json \
    --anima-root /workspace/anima \
    --seed $SEED 2>&1 | tee v58_cuda_filter.log" | tee v58_cuda_filter_remote.log

# ── 7) Download artifacts ───────────────────────────────────────────────
echo "[7/7] Downloading artifacts vast→Mac..."
$SCP_CMD "root@$SSH_HOST:/workspace/anima/v58_4mode_cuda_filter_compare.json" "$LOCAL_DIR/v58_4mode_cuda_filter_compare.json"
$SCP_CMD "root@$SSH_HOST:/workspace/anima/v58_cuda_filter.log" "$LOCAL_DIR/v58_cuda_filter.log" || true

echo "=== ${PHASE_ID} dispatch DONE ==="
date -u
echo "Result: $LOCAL_DIR/v58_4mode_cuda_filter_compare.json"
python3 -c "
import json
d = json.load(open('$LOCAL_DIR/v58_4mode_cuda_filter_compare.json'))
print()
print('=== ${PHASE_ID} V5.8 4-mode summary (cuda bf16 seed=$SEED) ===')
for mode in ['standard_greedy', 'standard_sample', 'M3_rep_penalty', 'M4_force_include']:
    off = d['filter_off']['summary'][mode]
    on  = d['filter_on']['summary'][mode]
    print(f'  {mode:20} OFF {off[\"n_pass\"]}/5 {off[\"verdict\"]:4}  ON {on[\"n_pass\"]}/5 {on[\"verdict\"]}')
ev = d['phase1a4_anima_fact_evidence']
print()
print('=== anima_fact / std_greedy 3-축 conjunction evidence ===')
print(f'  filter_off_markdown_drift: {ev[\"filter_off_markdown_drift\"]}')
print(f'  filter_on_markdown_drift:  {ev[\"filter_on_markdown_drift\"]}')
print(f'  filter_off_recalled:       {ev[\"filter_off_recalled\"]}')
print(f'  filter_on_recalled:        {ev[\"filter_on_recalled\"]}')
print(f'  conjunction_3axis_confirmed: {ev[\"conjunction_3axis_confirmed\"]}')
print(f'  filter_actually_fires:       {ev[\"filter_actually_fires\"]}')
print(f'  filter_unlocks_recall:       {ev[\"filter_unlocks_recall\"]}')
"
