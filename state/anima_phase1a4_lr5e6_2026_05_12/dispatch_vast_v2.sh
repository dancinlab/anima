#!/bin/bash
# dispatch_vast_v2.sh — Phase 1A.4 lr 5e-6 dispatch v2 (direct-IP SCP fix).
#
# v1 (dispatch_vast.sh) used ssh_host=ssh5.vast.ai:10160 (proxy) which
# hangs on 597MB .pt SCP (partial transfer 155MB observed). v2 forces
# direct port (public_ipaddr + direct_port_start) for all SSH/SCP +
# adds rsync fallback w/ resume.
#
# Reference: PASS_STRICT_SPONTANEOUS_CHAT.md §28 base (Mac-local) +
# Lesson R-1A.4-infra (proxy SCP hang on huge ckpt).
set -euo pipefail

# ── CONFIG ────────────────────────────────────────────────────────────
PHASE_ID="phase1a4_lr5e6"
LOCAL_DIR="/Users/ghost/core/anima/state/anima_phase1a4_lr5e6_2026_05_12"
PHASE1A1_DIR="/Users/ghost/core/anima/state/anima_phase1a1_color_cosmology_2026_05_12"
TRAINING_DIR="/Users/ghost/core/anima/training"
PHASE_LABEL="phase1a4-lr5e6-v2"

LR="${LR:-5e-6}"
STEPS="${STEPS:-200}"
BSZ="${BSZ:-2}"
GRAD_ACCUM="${GRAD_ACCUM:-8}"
CTX="${CTX:-1024}"
WARMUP="${WARMUP:-20}"
COST_CAP_USD="${COST_CAP_USD:-0.30}"
COST_PER_HR="${COST_PER_HR:-0.27}"

CORPUS_FILE="${CORPUS_FILE:-corpus_anima_fact.txt}"
TRAIN_SCRIPT="${TRAIN_SCRIPT:-train_phase1a4.py}"

VAST_SSH_KEY="/Users/ghost/.vast/ssh/vast-key"
VASTAI="/Users/ghost/.local/bin/vastai"
[ -x "$VASTAI" ] || VASTAI="/Users/ghost/Library/Python/3.14/bin/vastai"
[ -x "$VASTAI" ] || { echo "ERROR: vastai CLI not found"; exit 1; }
# ──────────────────────────────────────────────────────────────────────

cd "$LOCAL_DIR"

echo "=== ${PHASE_ID} v2 vast.ai dispatch (Mac-local + direct-IP) ==="
date -u

# ── 1) Find offer ──────────────────────────────────────────────────────
echo "[1/8] Searching RTX 4090 offers under \$0.30/hr..."
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
echo "[2/8] Renting instance..."
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
[ -z "$INSTANCE_ID" ] && { echo "ERROR: parse fail"; exit 1; }
echo "  Instance ID: $INSTANCE_ID"
echo "$INSTANCE_ID" > vast_instance_id_v2.txt

cleanup() {
    if [ -n "${KEEP_POD:-}" ]; then
        echo "[cleanup] KEEP_POD=$KEEP_POD set, NOT destroying $INSTANCE_ID"
        return 0
    fi
    echo "[cleanup] Destroying instance $INSTANCE_ID..."
    $VASTAI destroy instance "$INSTANCE_ID" 2>&1 | head -3 || true
}
trap cleanup EXIT

# ── 3) Wait for SSH ready via DIRECT port ──────────────────────────────
echo "[3/8] Waiting for SSH ready (DIRECT port)..."
SSH_HOST=""
SSH_PORT=""
for i in $(seq 1 160); do
    INFO=$($VASTAI show instance "$INSTANCE_ID" --raw 2>/dev/null || true)
    [ -z "$INFO" ] && INFO="{}"
    STATUS=$(echo "$INFO" | python3 -c "import json,sys;
try: d=json.load(sys.stdin); print(d.get('actual_status', ''))
except: print('parse_err')" 2>/dev/null || echo "")
    if [ "$STATUS" = "running" ]; then
        # Force DIRECT: public_ipaddr + direct_port_start
        SSH_HOST=$(echo "$INFO" | python3 -c "import json,sys;
try: d=json.load(sys.stdin); print(d.get('public_ipaddr',''))
except: pass" 2>/dev/null || echo "")
        SSH_PORT=$(echo "$INFO" | python3 -c "import json,sys;
try: d=json.load(sys.stdin); print(d.get('direct_port_start',''))
except: pass" 2>/dev/null || echo "")
        if [ -n "$SSH_HOST" ] && [ -n "$SSH_PORT" ]; then
            if ssh -i "$VAST_SSH_KEY" -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o ConnectTimeout=10 -p "$SSH_PORT" "root@$SSH_HOST" 'echo READY' 2>&1 | grep -q READY; then
                echo "  SSH ready (DIRECT): $SSH_HOST:$SSH_PORT (after ${i}x5s)"
                break
            fi
            SSH_HOST=""
        fi
    fi
    echo "  ... attempt $i/160, status=$STATUS"
    sleep 5
done

[ -z "$SSH_HOST" ] && { echo "ERROR: SSH not ready"; exit 1; }
echo "$SSH_HOST:$SSH_PORT" > vast_ssh_v2.txt

SSH_OPTS="-i $VAST_SSH_KEY -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o ServerAliveInterval=30 -o ServerAliveCountMax=10"
SSH_CMD="ssh $SSH_OPTS -p $SSH_PORT root@$SSH_HOST"
SCP_CMD="scp $SSH_OPTS -P $SSH_PORT"

# ── 4) Upload via DIRECT (small files first, ckpt with verify) ────────
echo "[4/8] Uploading files via DIRECT port..."
$SSH_CMD 'mkdir -p /workspace/anima/training /workspace/anima/corpus /workspace/anima/ckpts /workspace/anima/output'

echo "  [4a] training scripts (small)..."
$SCP_CMD "$LOCAL_DIR/$TRAIN_SCRIPT" "$LOCAL_DIR/v58_4mode_eval.py" "$TRAINING_DIR/engine_a_g_arch.py" "root@$SSH_HOST:/workspace/anima/training/"

echo "  [4b] corpus (~700KB)..."
$SCP_CMD "$LOCAL_DIR/$CORPUS_FILE" "root@$SSH_HOST:/workspace/anima/corpus/"

echo "  [4c] base ckpt (597MB, retry with rsync if scp fails)..."
LOCAL_CKPT="$PHASE1A1_DIR/ckpts/ckpt_phase1a1_sft.pt"
LOCAL_MD5=$(md5 -q "$LOCAL_CKPT")
echo "    Local MD5: $LOCAL_MD5"
# Try scp w/ verify (3 attempts)
SCP_OK=0
for attempt in 1 2 3; do
    echo "    SCP attempt $attempt/3..."
    if timeout 1200 $SCP_CMD "$LOCAL_CKPT" "root@$SSH_HOST:/workspace/anima/ckpts/ckpt_phase1a1_sft.pt"; then
        REMOTE_MD5=$($SSH_CMD 'md5sum /workspace/anima/ckpts/ckpt_phase1a1_sft.pt 2>/dev/null | cut -d" " -f1' || echo "fail")
        echo "    Remote MD5: $REMOTE_MD5"
        if [ "$LOCAL_MD5" = "$REMOTE_MD5" ]; then
            echo "    MD5 OK — ckpt verified."
            SCP_OK=1
            break
        else
            echo "    MD5 MISMATCH — retrying."
            $SSH_CMD 'rm -f /workspace/anima/ckpts/ckpt_phase1a1_sft.pt' || true
        fi
    else
        echo "    SCP timeout/fail — retrying."
        $SSH_CMD 'rm -f /workspace/anima/ckpts/ckpt_phase1a1_sft.pt' || true
    fi
done
if [ $SCP_OK -eq 0 ]; then
    echo "    SCP failed 3x, trying rsync..."
    rsync -av --progress -e "ssh $SSH_OPTS -p $SSH_PORT" "$LOCAL_CKPT" "root@$SSH_HOST:/workspace/anima/ckpts/ckpt_phase1a1_sft.pt"
    REMOTE_MD5=$($SSH_CMD 'md5sum /workspace/anima/ckpts/ckpt_phase1a1_sft.pt 2>/dev/null | cut -d" " -f1' || echo "fail")
    if [ "$LOCAL_MD5" != "$REMOTE_MD5" ]; then
        echo "ERROR: ckpt MD5 mismatch even after rsync"
        exit 1
    fi
fi

# ── 5) Sanity check ────────────────────────────────────────────────────
echo "[5/8] GPU + torch check..."
$SSH_CMD 'cd /workspace/anima && python3 -c "import torch; print(torch.__version__, torch.cuda.is_available(), torch.cuda.get_device_name(0))"' | head -3

# ── 6) Train ───────────────────────────────────────────────────────────
echo "[6/8] Training ($STEPS steps lr $LR)..."
$SSH_CMD "cd /workspace/anima && export PYTHONUNBUFFERED=1 && python3 training/$TRAIN_SCRIPT \
    --base-ckpt ckpts/ckpt_phase1a1_sft.pt \
    --chat-corpus corpus/$CORPUS_FILE \
    --output output \
    --steps $STEPS \
    --bsz $BSZ \
    --grad-accum $GRAD_ACCUM \
    --ctx $CTX \
    --lr $LR \
    --warmup $WARMUP \
    --cost-cap-usd $COST_CAP_USD \
    --cost-per-hr $COST_PER_HR 2>&1 | tee train.log" | tee train_remote.log

# ── 7) V5.8 4-mode eval ────────────────────────────────────────────────
echo "[7/8] V5.8 4-mode eval..."
$SSH_CMD "cd /workspace/anima && export PYTHONUNBUFFERED=1 && python3 training/v58_4mode_eval.py \
    --ckpt output/ckpt_final.pt \
    --output v58_4mode_result.json \
    --substrate-id ${PHASE_ID} 2>&1 | tee v58.log" | tee v58_remote.log

# ── 8) Download via DIRECT ─────────────────────────────────────────────
echo "[8/8] Downloading artifacts via DIRECT port..."
mkdir -p "$LOCAL_DIR/ckpts"
$SCP_CMD "root@$SSH_HOST:/workspace/anima/output/ckpt_final.pt" "$LOCAL_DIR/ckpts/ckpt_${PHASE_ID}_sft.pt"
$SCP_CMD "root@$SSH_HOST:/workspace/anima/output/meta.json" "$LOCAL_DIR/meta.json" || true
$SCP_CMD "root@$SSH_HOST:/workspace/anima/v58_4mode_result.json" "$LOCAL_DIR/v58_4mode_result.json"
$SCP_CMD "root@$SSH_HOST:/workspace/anima/train.log" "$LOCAL_DIR/train.log" || true

echo "=== ${PHASE_ID} v2 dispatch DONE ==="
date -u
echo "Result: $LOCAL_DIR/v58_4mode_result.json"
cat "$LOCAL_DIR/v58_4mode_result.json" | python3 -c "
import json, sys
d = json.load(sys.stdin)
print('=== ${PHASE_ID} V5.8 4-mode summary ===')
for mode, s in d['summary'].items():
    print(f'  {mode}: {s[\"n_pass\"]}/5 {s[\"verdict\"]}')
"
