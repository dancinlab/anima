#!/bin/bash
# tool/dispatch_vast_mac_template.sh — Mac-local canonical Vast.ai dispatch template.
#
# Reference: PASS_STRICT_SPONTANEOUS_CHAT.md §28 (2026-05-12 infra fix).
# Replaces prior Linux-remote-relay pattern (state/anima_phase1a2_*/dispatch_vast.sh)
# which carried 3 systemic bugs: Linux path hardcode, ssh-mac wrap, vastai pipefail crash.
#
# USAGE for new cycle (e.g. Phase 1A.4):
#   1. cp tool/dispatch_vast_mac_template.sh state/<new_phase_dir>/dispatch_vast.sh
#   2. PHASE_ID, LOCAL_DIR, PHASE_LABEL, COST_CAP, LR, STEPS 등 hyperparams 교체
#   3. corpus 파일명 + train script 명 교체
#   4. chmod +x state/<new_phase_dir>/dispatch_vast.sh
#   5. cd state/<new_phase_dir> && bash dispatch_vast.sh
#
# Provider: Vast.ai RTX 4090 (~$0.24-0.30/hr)
# Pre-fire 가드: cost cap budget breach 시 abort + report (memory feedback_active_resource_utilization).
set -euo pipefail

# ── CONFIG (Phase 1A.4 lr 5e-6 × 200 SFT — Lesson R-1A.2) ─────────────
PHASE_ID="phase1a4_lr5e6"
LOCAL_DIR="/Users/ghost/core/anima/state/anima_phase1a4_lr5e6_2026_05_12"
PHASE1A1_DIR="/Users/ghost/core/anima/state/anima_phase1a1_color_cosmology_2026_05_12"
TRAINING_DIR="/Users/ghost/core/anima/training"
PHASE_LABEL="phase1a4-lr5e6"          # Vast.ai instance label

# Hyperparams (overrideable via env or edit)
LR="${LR:-5e-6}"
STEPS="${STEPS:-200}"
BSZ="${BSZ:-2}"
GRAD_ACCUM="${GRAD_ACCUM:-8}"
CTX="${CTX:-1024}"
WARMUP="${WARMUP:-20}"
COST_CAP_USD="${COST_CAP_USD:-0.20}"
COST_PER_HR="${COST_PER_HR:-0.27}"

# corpus + train script (LOCAL_DIR 안 위치 가정)
CORPUS_FILE="${CORPUS_FILE:-corpus_anima_fact.txt}"
TRAIN_SCRIPT="${TRAIN_SCRIPT:-train_phase1a4.py}"

# Mac local binaries
VAST_SSH_KEY="/Users/ghost/.vast/ssh/vast-key"
VASTAI="/Users/ghost/.local/bin/vastai"
[ -x "$VASTAI" ] || VASTAI="/Users/ghost/Library/Python/3.14/bin/vastai"
[ -x "$VASTAI" ] || { echo "ERROR: vastai CLI not found"; exit 1; }
# ──────────────────────────────────────────────────────────────────────

cd "$LOCAL_DIR"

echo "=== ${PHASE_ID} vast.ai dispatch (Mac-local) ==="
date -u

# ── 1) Find best offer ──────────────────────────────────────────────────
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
# NOTE: vastai show instance <id> 가 start_date=None 일 때 TypeError crash 가능.
#       2>/dev/null + || INFO="{}" 로 guard.
echo "[3/8] Waiting for SSH ready..."
SSH_HOST=""
SSH_PORT=""
# Extended to 160 attempts (13 min total) — prior attempt 1 saw pod transition to
# 'running' at attempt 73/80, then SSH probe needed extra time for sshd to come up.
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
            # Probe SSH directly from Mac (no ssh-mac wrap)
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
    echo "ERROR: SSH not ready"; exit 1
fi

echo "$SSH_HOST:$SSH_PORT" > vast_ssh.txt

SSH_OPTS="-i $VAST_SSH_KEY -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null"
SSH_CMD="ssh $SSH_OPTS -p $SSH_PORT root@$SSH_HOST"
SCP_CMD="scp $SSH_OPTS -P $SSH_PORT"

# ── 4) Upload files directly Mac → vast ─────────────────────────────────
echo "[4/8] Uploading files (corpus + scripts + ckpt + arch) direct Mac→vast..."
$SSH_CMD 'mkdir -p /workspace/anima/training /workspace/anima/corpus /workspace/anima/ckpts /workspace/anima/output'

$SCP_CMD "$LOCAL_DIR/$TRAIN_SCRIPT" "$LOCAL_DIR/v58_4mode_eval.py" "$TRAINING_DIR/engine_a_g_arch.py" "root@$SSH_HOST:/workspace/anima/training/"
$SCP_CMD "$LOCAL_DIR/$CORPUS_FILE" "root@$SSH_HOST:/workspace/anima/corpus/"
$SCP_CMD "$PHASE1A1_DIR/ckpts/ckpt_phase1a1_sft.pt" "root@$SSH_HOST:/workspace/anima/ckpts/"

# ── 5) Sanity check torch + GPU ─────────────────────────────────────────
echo "[5/8] GPU + torch check..."
$SSH_CMD 'cd /workspace/anima && python3 -c "import torch; print(torch.__version__, torch.cuda.is_available(), torch.cuda.get_device_name(0))"' | head -3

# ── 6) Train ────────────────────────────────────────────────────────────
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

# ── 7) V5.8 4-mode eval ─────────────────────────────────────────────────
echo "[7/8] V5.8 4-mode eval..."
$SSH_CMD "cd /workspace/anima && export PYTHONUNBUFFERED=1 && python3 training/v58_4mode_eval.py \
    --ckpt output/ckpt_final.pt \
    --output v58_4mode_result.json \
    --substrate-id ${PHASE_ID} 2>&1 | tee v58.log" | tee v58_remote.log

# ── 8) Download artifacts directly vast → Mac ───────────────────────────
echo "[8/8] Downloading artifacts direct vast→Mac..."
mkdir -p "$LOCAL_DIR/ckpts"
$SCP_CMD "root@$SSH_HOST:/workspace/anima/output/ckpt_final.pt" "$LOCAL_DIR/ckpts/ckpt_${PHASE_ID}_sft.pt"
$SCP_CMD "root@$SSH_HOST:/workspace/anima/output/meta.json" "$LOCAL_DIR/meta.json"
$SCP_CMD "root@$SSH_HOST:/workspace/anima/v58_4mode_result.json" "$LOCAL_DIR/v58_4mode_result.json"
$SCP_CMD "root@$SSH_HOST:/workspace/anima/train.log" "$LOCAL_DIR/train.log"

echo "=== ${PHASE_ID} dispatch DONE ==="
date -u
echo "Result: $LOCAL_DIR/v58_4mode_result.json"
cat "$LOCAL_DIR/v58_4mode_result.json" | python3 -c "
import json, sys
d = json.load(sys.stdin)
print('=== ${PHASE_ID} V5.8 4-mode summary ===')
for mode, s in d['summary'].items():
    print(f'  {mode}: {s[\"n_pass\"]}/5 {s[\"verdict\"]}')
"
