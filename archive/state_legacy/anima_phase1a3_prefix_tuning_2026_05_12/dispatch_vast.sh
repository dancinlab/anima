#!/bin/bash
# dispatch_vast.sh — Phase 1A.3 prefix-tuning on vast.ai RTX 4090.
#
# Strategy: load Phase 1A.1 ckpt frozen, train ONLY n_prefix=20 × d_model=1024 learnable
# prefix embeddings (Li & Liang 2021). Bypass markdown attractor via control-plane shift.
#
# Cost budget: $0.13 hard cap (~$0.27/hr × 25min — prefix-tuning is much faster than full SFT)
# Provider: Vast.ai RTX 4090
set -euo pipefail

LOCAL_DIR="/Users/ghost/core/anima/state/anima_phase1a3_prefix_tuning_2026_05_12"
PHASE1A1_DIR="/Users/ghost/core/anima/state/anima_phase1a1_color_cosmology_2026_05_12"
PHASE1A2_DIR="/Users/ghost/core/anima/state/anima_phase1a2_anima_fact_2026_05_12"
TRAINING_DIR="/Users/ghost/core/anima/training"

VAST_SSH_KEY="/Users/ghost/.vast/ssh/vast-key"
VASTAI="/Users/ghost/Library/Python/3.14/bin/vastai"

cd "$LOCAL_DIR"

echo "=== Phase 1A.3 prefix-tuning vast.ai dispatch ==="
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
CREATE_OUT=$("$VASTAI" create instance "$OFFER" --image pytorch/pytorch:2.5.1-cuda12.1-cudnn9-runtime --disk 30 --ssh --direct --label phase1a3-prefix-tuning --raw 2>&1)
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
# Use 'show instances' (list mode) — 'show instance <ID>' has a vastai-cli bug
# that crashes with TypeError when start_date is None during the transient
# loading→running phase. List endpoint is safe.
for i in $(seq 1 80); do
    INFO=$("$VASTAI" show instances --raw 2>&1 || echo '[]')
    STATUS=$(echo "$INFO" | python3 -c "
import json, sys, os
iid = int(os.environ['INSTANCE_ID'])
try:
    d = json.load(sys.stdin)
    me = next((x for x in d if x.get('id') == iid), None)
    print(me.get('actual_status', '') if me else 'gone')
except Exception:
    print('parse_err')
" INSTANCE_ID="$INSTANCE_ID" 2>/dev/null || echo "exc")
    if [ "$STATUS" = "running" ]; then
        ENDPOINTS=$(echo "$INFO" | python3 -c "
import json, sys, os
iid = int(os.environ['INSTANCE_ID'])
try:
    d = json.load(sys.stdin)
    me = next((x for x in d if x.get('id') == iid), None)
    if me:
        host = me.get('ssh_host', '') or me.get('public_ipaddr', '')
        port = me.get('ssh_port', '') or me.get('direct_port_start', '')
        print(f'{host}|{port}')
    else:
        print('|')
except Exception:
    print('|')
" INSTANCE_ID="$INSTANCE_ID" 2>/dev/null || echo "|")
        SSH_HOST="${ENDPOINTS%|*}"
        SSH_PORT="${ENDPOINTS#*|}"
        if [ -n "$SSH_HOST" ] && [ -n "$SSH_PORT" ]; then
            # Probe SSH
            if ssh -i "$VAST_SSH_KEY" -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o ConnectTimeout=10 -p "$SSH_PORT" root@"$SSH_HOST" 'echo READY' 2>&1 | grep -q READY; then
                echo "  SSH ready: $SSH_HOST:$SSH_PORT (after ${i}x5s)"
                break
            fi
            SSH_HOST=""
        fi
    fi
    if [ "$STATUS" = "gone" ]; then
        echo "ERROR: instance disappeared (vast.ai destroyed it externally)"; exit 1
    fi
    echo "  ... attempt $i/80, status=$STATUS"
    sleep 5
done

if [ -z "$SSH_HOST" ]; then
    echo "ERROR: SSH not ready after 80 attempts"; exit 1
fi

echo "$SSH_HOST:$SSH_PORT" > vast_ssh.txt

SSH_OPTS="-i $VAST_SSH_KEY -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null"
SSH_CMD="ssh $SSH_OPTS -p $SSH_PORT root@$SSH_HOST"
SCP_CMD="scp $SSH_OPTS -P $SSH_PORT"

# ── 4) Upload files ─────────────────────────────────────────────────────
echo "[4/8] Uploading files (corpus + scripts + ckpt + arch)..."

# Create dirs on remote
$SSH_CMD 'mkdir -p /workspace/anima/training /workspace/anima/corpus /workspace/anima/ckpts /workspace/anima/output'

# Upload serially with retry — large ckpt (570MB) over fresh vast.ai SSH is fragile.
upload_with_retry() {
    local src="$1"
    local dst="$2"
    local label="$3"
    local max_tries=3
    local try
    for try in $(seq 1 $max_tries); do
        echo "  [upload $label try $try/$max_tries] $(basename "$src") -> $dst"
        if $SCP_CMD "$src" "root@$SSH_HOST:$dst"; then
            echo "  [upload $label] OK"
            return 0
        fi
        echo "  [upload $label] FAIL (try $try/$max_tries), retrying in 15s..."
        sleep 15
    done
    echo "ERROR: upload $label failed after $max_tries tries"
    return 1
}

# Small files first (scripts + corpus)
upload_with_retry "$TRAINING_DIR/engine_a_g_arch.py"        "/workspace/anima/training/" "engine_arch"
upload_with_retry "$LOCAL_DIR/train_phase1a3.py"            "/workspace/anima/training/" "train_script"
upload_with_retry "$LOCAL_DIR/v58_4mode_eval_prefix.py"     "/workspace/anima/training/" "eval_script"
upload_with_retry "$PHASE1A2_DIR/corpus_anima_fact.txt"     "/workspace/anima/corpus/"   "corpus"
# Big ckpt last — keeps the connection fresh and isolated
upload_with_retry "$PHASE1A1_DIR/ckpts/ckpt_phase1a1_sft.pt" "/workspace/anima/ckpts/"   "phase1a1_ckpt"

# ── 5) Sanity check torch + GPU ─────────────────────────────────────────
echo "[5/8] GPU + torch check..."
$SSH_CMD 'cd /workspace/anima && python3 -c "import torch; print(torch.__version__, torch.cuda.is_available(), torch.cuda.get_device_name(0))"' | head -3

# ── 6) Train (prefix-tuning) ────────────────────────────────────────────
echo "[6/8] Training (prefix-tuning, n_prefix=20, lr 1e-3, 500 steps)..."
$SSH_CMD "cd /workspace/anima && export PYTHONUNBUFFERED=1 && python3 training/train_phase1a3.py \
    --base-ckpt ckpts/ckpt_phase1a1_sft.pt \
    --chat-corpus corpus/corpus_anima_fact.txt \
    --output output \
    --n-prefix 20 \
    --steps 500 \
    --bsz 2 \
    --grad-accum 8 \
    --ctx 1024 \
    --lr 1e-3 \
    --warmup 50 \
    --cost-cap-usd 0.13 \
    --cost-per-hr 0.27 2>&1 | tee train.log" | tee train_remote.log

# ── 7) V5.8 4-mode eval ─────────────────────────────────────────────────
echo "[7/8] V5.8 4-mode eval (prefix-tuned)..."
$SSH_CMD "cd /workspace/anima && export PYTHONUNBUFFERED=1 && python3 training/v58_4mode_eval_prefix.py \
    --base-ckpt ckpts/ckpt_phase1a1_sft.pt \
    --prefix-ckpt output/prefix_final.pt \
    --output v58_4mode_result.json \
    --substrate-id phase1a3_prefix_tuning 2>&1 | tee v58.log" | tee v58_remote.log

# ── 8) Download artifacts ───────────────────────────────────────────────
echo "[8/8] Downloading artifacts..."
mkdir -p "$LOCAL_DIR/ckpts"
$SCP_CMD "root@$SSH_HOST:/workspace/anima/output/prefix_final.pt" "$LOCAL_DIR/ckpts/prefix_final.pt"
$SCP_CMD "root@$SSH_HOST:/workspace/anima/output/meta.json" "$LOCAL_DIR/meta.json"
$SCP_CMD "root@$SSH_HOST:/workspace/anima/v58_4mode_result.json" "$LOCAL_DIR/v58_4mode_result.json"
$SCP_CMD "root@$SSH_HOST:/workspace/anima/train.log" "$LOCAL_DIR/train.log"

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
