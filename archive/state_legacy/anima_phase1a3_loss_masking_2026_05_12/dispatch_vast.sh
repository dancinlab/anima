#!/bin/bash
# dispatch_vast.sh — Phase 1A.3 loss-masking SFT dispatch on Vast.ai RTX 4090.
#
# Cost budget: $0.15 hard cap ($0.27/hr × ~30min)
# Strategy: Phase 1A.1 ckpt → continue SFT with Phase 1A.2 corpus, but
#          cross-entropy masked to anima response bytes only (Lesson R-1A.2
#          lane B). lr 2e-6 (Phase 1A.1 match) isolates masking effect.
# Provider: Vast.ai RTX 4090
#
# Runs LOCALLY on the Mac (vastai installed at ~/Library/Python/3.14/bin).
# Files live on Mac at /Users/ghost/core/anima/...
set -euo pipefail

LOCAL_DIR="/Users/ghost/core/anima/state/anima_phase1a3_loss_masking_2026_05_12"
PHASE1A1_DIR="/Users/ghost/core/anima/state/anima_phase1a1_color_cosmology_2026_05_12"
TRAINING_DIR="/Users/ghost/core/anima/training"

VAST_SSH_KEY="/Users/ghost/.vast/ssh/vast-key"
VASTAI="/Users/ghost/Library/Python/3.14/bin/vastai"

cd "$LOCAL_DIR"

echo "=== Phase 1A.3 vast.ai dispatch (loss-masking) ==="
date -u

# ── 1) Find best offer ──────────────────────────────────────────────────
echo "[1/8] Searching RTX 4090 offers under \$0.30/hr..."
OFFER=$("$VASTAI" search offers 'gpu_name=RTX_4090 num_gpus=1 reliability>0.98 dph_total<0.30 disk_space>30 inet_down>500' -o dph_total --raw 2>&1 | \
    python3 -c "
import json, sys
data = json.load(sys.stdin)
if not data:
    sys.stderr.write('no offers\n'); sys.exit(1)
print(data[0]['id'])
")
echo "  Selected offer ID: $OFFER"

# ── 2) Rent ─────────────────────────────────────────────────────────────
echo "[2/8] Renting instance..."
CREATE_OUT=$("$VASTAI" create instance "$OFFER" --image pytorch/pytorch:2.5.1-cuda12.1-cudnn9-runtime --disk 30 --ssh --direct --label phase1a3-loss-masking --raw 2>&1)
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
    "$VASTAI" destroy instance "$INSTANCE_ID" 2>&1 | head -3 || true
}
trap cleanup EXIT

# ── 3) Wait for SSH ready ───────────────────────────────────────────────
echo "[3/8] Waiting for SSH ready..."
SSH_HOST=""
SSH_PORT=""
for i in $(seq 1 80); do
    set +e
    INFO=$("$VASTAI" show instance "$INSTANCE_ID" --raw 2>/dev/null)
    if [ -z "$INFO" ]; then INFO="{}"; fi
    STATUS=$(printf '%s' "$INFO" | python3 -c "
import json, sys
try:
    d = json.load(sys.stdin)
    print(d.get('actual_status') or '')
except Exception:
    print('parse_err')
" 2>/dev/null)
    set -e
    if [ "$STATUS" = "running" ]; then
        set +e
        SSH_HOST=$(printf '%s' "$INFO" | python3 -c "
import json, sys
try:
    d = json.load(sys.stdin)
    print((d.get('ssh_host') or d.get('public_ipaddr') or '').strip())
except Exception:
    print('')
" 2>/dev/null)
        SSH_PORT=$(printf '%s' "$INFO" | python3 -c "
import json, sys
try:
    d = json.load(sys.stdin)
    port = d.get('ssh_port') or d.get('direct_port_start') or ''
    print(str(port).strip())
except Exception:
    print('')
" 2>/dev/null)
        set -e
        if [ -n "$SSH_HOST" ] && [ -n "$SSH_PORT" ]; then
            set +e
            ssh -i "$VAST_SSH_KEY" -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o ConnectTimeout=10 -p "$SSH_PORT" "root@$SSH_HOST" 'echo READY' 2>&1 | grep -q READY
            PROBE_RC=$?
            set -e
            if [ "$PROBE_RC" = "0" ]; then
                echo "  SSH ready: $SSH_HOST:$SSH_PORT (after ${i}x5s)"
                break
            fi
            SSH_HOST=""
        fi
    fi
    echo "  ... attempt $i/80, status=$STATUS host=${SSH_HOST:-?} port=${SSH_PORT:-?}"
    sleep 5
done

if [ -z "$SSH_HOST" ]; then
    echo "ERROR: SSH not ready"; exit 1
fi

echo "$SSH_HOST:$SSH_PORT" > vast_ssh.txt

SSH_OPTS=(-i "$VAST_SSH_KEY" -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null)
SSH_CMD=(ssh "${SSH_OPTS[@]}" -p "$SSH_PORT" "root@$SSH_HOST")
SCP_CMD=(scp "${SSH_OPTS[@]}" -P "$SSH_PORT")

# ── 4) Upload files ─────────────────────────────────────────────────────
echo "[4/8] Uploading files (corpus + scripts + ckpt + arch)..."
"${SSH_CMD[@]}" 'mkdir -p /workspace/anima/training /workspace/anima/corpus /workspace/anima/ckpts /workspace/anima/output'

"${SCP_CMD[@]}" "$TRAINING_DIR/engine_a_g_arch.py" "$LOCAL_DIR/train_phase1a3.py" "$LOCAL_DIR/v58_4mode_eval.py" "root@$SSH_HOST:/workspace/anima/training/"
"${SCP_CMD[@]}" "$LOCAL_DIR/corpus_anima_fact.txt" "root@$SSH_HOST:/workspace/anima/corpus/"
"${SCP_CMD[@]}" "$PHASE1A1_DIR/ckpts/ckpt_phase1a1_sft.pt" "root@$SSH_HOST:/workspace/anima/ckpts/"

# ── 5) Sanity check torch + GPU ─────────────────────────────────────────
echo "[5/8] GPU + torch check..."
"${SSH_CMD[@]}" 'cd /workspace/anima && python3 -c "import torch; print(torch.__version__, torch.cuda.is_available(), torch.cuda.get_device_name(0))"' | head -3

# ── 6) Train ────────────────────────────────────────────────────────────
echo "[6/8] Training (200 steps lr 2e-6, response-only loss mask)..."
"${SSH_CMD[@]}" 'cd /workspace/anima && export PYTHONUNBUFFERED=1 && python3 training/train_phase1a3.py \
    --base-ckpt ckpts/ckpt_phase1a1_sft.pt \
    --chat-corpus corpus/corpus_anima_fact.txt \
    --output output \
    --steps 200 \
    --bsz 2 \
    --grad-accum 8 \
    --ctx 1024 \
    --lr 2e-6 \
    --warmup 20 \
    --cost-cap-usd 0.15 \
    --cost-per-hr 0.27 2>&1 | tee train.log' | tee train_remote.log

# ── 7) V5.8 4-mode eval ─────────────────────────────────────────────────
echo "[7/8] V5.8 4-mode eval..."
"${SSH_CMD[@]}" 'cd /workspace/anima && export PYTHONUNBUFFERED=1 && python3 training/v58_4mode_eval.py \
    --ckpt output/ckpt_final.pt \
    --output v58_4mode_result.json \
    --substrate-id phase1a3_loss_masking 2>&1 | tee v58.log' | tee v58_remote.log

# ── 8) Download artifacts ───────────────────────────────────────────────
echo "[8/8] Downloading artifacts..."
mkdir -p "$LOCAL_DIR/ckpts"
"${SCP_CMD[@]}" "root@$SSH_HOST:/workspace/anima/output/ckpt_final.pt" "$LOCAL_DIR/ckpts/ckpt_phase1a3_sft.pt"
"${SCP_CMD[@]}" "root@$SSH_HOST:/workspace/anima/output/meta.json" "$LOCAL_DIR/meta.json"
"${SCP_CMD[@]}" "root@$SSH_HOST:/workspace/anima/v58_4mode_result.json" "$LOCAL_DIR/v58_4mode_result.json"
"${SCP_CMD[@]}" "root@$SSH_HOST:/workspace/anima/train.log" "$LOCAL_DIR/train.log"

echo "=== Phase 1A.3 dispatch DONE ==="
date -u
echo "Result: $LOCAL_DIR/v58_4mode_result.json"
cat "$LOCAL_DIR/v58_4mode_result.json" | python3 -c "
import json, sys
d = json.load(sys.stdin)
print('=== Phase 1A.3 V5.8 4-mode summary ===')
for mode, s in d['summary'].items():
    print(f'  {mode}: {s[\"n_pass\"]}/5 {s[\"verdict\"]}')
"
