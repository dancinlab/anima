#!/bin/bash
# dispatch_vast.sh — Phase 1A.2 anima_fact recover dispatch on vast.ai RTX 4090.
#
# Cost budget: $0.15 hard cap ($0.27/hr × ~30min)
# Provider: Vast.ai RTX 4090
set -euo pipefail

LOCAL_DIR="/home/summer/mac_home/core/anima/state/anima_phase1a2_anima_fact_2026_05_12"
PHASE1A1_DIR="/home/summer/mac_home/core/anima/state/anima_phase1a1_color_cosmology_2026_05_12"
TRAINING_DIR="/home/summer/mac_home/core/anima/training"

VAST_SSH_KEY="/Users/ghost/.vast/ssh/vast-key"
VASTAI="/Users/ghost/.local/bin/vastai"

cd "$LOCAL_DIR"

echo "=== Phase 1A.2 vast.ai dispatch ==="
date -u

# ── 1) Find best offer ──────────────────────────────────────────────────
echo "[1/8] Searching RTX 4090 offers under \$0.30/hr..."
OFFER=$(ssh mac "$VASTAI search offers 'gpu_name=RTX_4090 num_gpus=1 reliability>0.98 dph_total<0.30 disk_space>30 inet_down>500' -o dph_total --raw" 2>&1 | \
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
CREATE_OUT=$(ssh mac "$VASTAI create instance $OFFER --image pytorch/pytorch:2.5.1-cuda12.1-cudnn9-runtime --disk 30 --ssh --direct --label phase1a2-anima-fact --raw" 2>&1)
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
    ssh mac "$VASTAI destroy instance $INSTANCE_ID" 2>&1 | head -3 || true
}
trap cleanup EXIT

# ── 3) Wait for SSH ready ───────────────────────────────────────────────
echo "[3/8] Waiting for SSH ready..."
SSH_HOST=""
SSH_PORT=""
for i in $(seq 1 80); do
    INFO=$(ssh mac "$VASTAI show instance $INSTANCE_ID --raw" 2>&1)
    STATUS=$(echo "$INFO" | python3 -c "import json,sys;
try: d=json.load(sys.stdin); print(d.get('actual_status', ''))
except: print('parse_err')" 2>/dev/null)
    if [ "$STATUS" = "running" ]; then
        SSH_HOST=$(echo "$INFO" | python3 -c "import json,sys;
try: d=json.load(sys.stdin); print(d.get('ssh_host', '') or d.get('public_ipaddr',''))
except: pass")
        SSH_PORT=$(echo "$INFO" | python3 -c "import json,sys;
try: d=json.load(sys.stdin); print(d.get('ssh_port', '') or d.get('direct_port_start',''))
except: pass")
        if [ -n "$SSH_HOST" ] && [ -n "$SSH_PORT" ]; then
            # Probe SSH
            if ssh mac "ssh -i $VAST_SSH_KEY -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o ConnectTimeout=10 -p $SSH_PORT root@$SSH_HOST 'echo READY'" 2>&1 | grep -q READY; then
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

# ── 4) Upload files ─────────────────────────────────────────────────────
echo "[4/8] Uploading files (corpus + scripts + ckpt + arch)..."
# Stage on mac
ssh mac "mkdir -p /tmp/phase1a2_upload"
scp "$LOCAL_DIR/corpus_anima_fact.txt" "$LOCAL_DIR/train_phase1a2.py" "$LOCAL_DIR/v58_4mode_eval.py" "$TRAINING_DIR/engine_a_g_arch.py" mac:/tmp/phase1a2_upload/
scp "$PHASE1A1_DIR/ckpts/ckpt_phase1a1_sft.pt" mac:/tmp/phase1a2_upload/

# Create dirs
ssh mac "$SSH_CMD 'mkdir -p /workspace/anima/training /workspace/anima/corpus /workspace/anima/ckpts /workspace/anima/output'"

# Upload via Mac→vast
ssh mac "$SCP_CMD /tmp/phase1a2_upload/engine_a_g_arch.py /tmp/phase1a2_upload/train_phase1a2.py /tmp/phase1a2_upload/v58_4mode_eval.py root@$SSH_HOST:/workspace/anima/training/"
ssh mac "$SCP_CMD /tmp/phase1a2_upload/corpus_anima_fact.txt root@$SSH_HOST:/workspace/anima/corpus/"
ssh mac "$SCP_CMD /tmp/phase1a2_upload/ckpt_phase1a1_sft.pt root@$SSH_HOST:/workspace/anima/ckpts/"

ssh mac "rm -rf /tmp/phase1a2_upload"

# ── 5) Sanity check torch + GPU ─────────────────────────────────────────
echo "[5/8] GPU + torch check..."
ssh mac "$SSH_CMD 'cd /workspace/anima && python3 -c \"import torch; print(torch.__version__, torch.cuda.is_available(), torch.cuda.get_device_name(0))\"'" | head -3

# ── 6) Train ────────────────────────────────────────────────────────────
echo "[6/8] Training (200 steps lr 1e-6)..."
ssh mac "$SSH_CMD 'cd /workspace/anima && export PYTHONUNBUFFERED=1 && python3 training/train_phase1a2.py \
    --base-ckpt ckpts/ckpt_phase1a1_sft.pt \
    --chat-corpus corpus/corpus_anima_fact.txt \
    --output output \
    --steps 200 \
    --bsz 2 \
    --grad-accum 8 \
    --ctx 1024 \
    --lr 1e-6 \
    --warmup 20 \
    --cost-cap-usd 0.15 \
    --cost-per-hr 0.27 2>&1 | tee train.log'" | tee train_remote.log

# ── 7) V5.8 4-mode eval ─────────────────────────────────────────────────
echo "[7/8] V5.8 4-mode eval..."
ssh mac "$SSH_CMD 'cd /workspace/anima && export PYTHONUNBUFFERED=1 && python3 training/v58_4mode_eval.py \
    --ckpt output/ckpt_final.pt \
    --output v58_4mode_result.json \
    --substrate-id phase1a2_anima_fact_recover 2>&1 | tee v58.log'" | tee v58_remote.log

# ── 8) Download artifacts ───────────────────────────────────────────────
echo "[8/8] Downloading artifacts..."
mkdir -p "$LOCAL_DIR/ckpts"
ssh mac "$SCP_CMD root@$SSH_HOST:/workspace/anima/output/ckpt_final.pt /tmp/phase1a2_ckpt_final.pt"
ssh mac "$SCP_CMD root@$SSH_HOST:/workspace/anima/output/meta.json /tmp/phase1a2_meta.json"
ssh mac "$SCP_CMD root@$SSH_HOST:/workspace/anima/v58_4mode_result.json /tmp/phase1a2_v58.json"
ssh mac "$SCP_CMD root@$SSH_HOST:/workspace/anima/train.log /tmp/phase1a2_train.log"

scp mac:/tmp/phase1a2_ckpt_final.pt "$LOCAL_DIR/ckpts/ckpt_phase1a2_sft.pt"
scp mac:/tmp/phase1a2_meta.json "$LOCAL_DIR/meta.json"
scp mac:/tmp/phase1a2_v58.json "$LOCAL_DIR/v58_4mode_result.json"
scp mac:/tmp/phase1a2_train.log "$LOCAL_DIR/train.log"

ssh mac "rm -f /tmp/phase1a2_ckpt_final.pt /tmp/phase1a2_meta.json /tmp/phase1a2_v58.json /tmp/phase1a2_train.log"

echo "=== Phase 1A.2 dispatch DONE ==="
date -u
echo "Result: $LOCAL_DIR/v58_4mode_result.json"
cat "$LOCAL_DIR/v58_4mode_result.json" | python3 -c "
import json, sys
d = json.load(sys.stdin)
print('=== Phase 1A.2 V5.8 4-mode summary ===')
for mode, s in d['summary'].items():
    print(f'  {mode}: {s[\"n_pass\"]}/5 {s[\"verdict\"]}')
"
