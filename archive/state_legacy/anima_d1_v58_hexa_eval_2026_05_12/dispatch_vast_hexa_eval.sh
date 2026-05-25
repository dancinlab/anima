#!/bin/bash
# state/anima_d1_v58_hexa_eval_2026_05_12/dispatch_vast_hexa_eval.sh
#
# Vast.ai dispatch for V5.8 hexa eval (deferred deliverable).
#
# STATUS (2026-05-12 KST)
#   NOT FIRED — wall-budget analysis showed the full 20-cell V5.8 matrix
#   requires ~8 hr × $0.241/hr = ~$1.93, which is 6× the $0.30 cost cap.
#   hexa interp is CPU-only (RFC 032 farr_matmul has no CUDA backend),
#   so RTX 4090 rental provides no acceleration — the EPYC 7B13 cores
#   on the same instance run hexa-interp at ~1.5× slower than Apple Silicon.
#
#   This script is a deferred deliverable. Fire only when one of:
#     - GPU farr backend (RFC 040+) lands and hexa-interp gains CUDA path.
#     - User explicitly approves the budget overage for full matrix.
#     - A pure CPU Vast.ai offer < $0.10/hr appears (currently NO OFFERS).
#
# REFERENCE
#   tool/dispatch_vast_mac_template.sh (PSCC §28 canonical infra)
#
# CONFIG (matches BG scope)
PHASE_ID="d1_v58_hexa_eval"
LOCAL_DIR="/Users/ghost/core/anima/state/anima_d1_v58_hexa_eval_2026_05_12"
PHASE1A1_DIR="/Users/ghost/core/anima/state/anima_phase1a1_color_cosmology_2026_05_12"
ANIMA_DIR="/Users/ghost/core/anima"
HEXA_DIR="/Users/ghost/core/hexa-lang"
PHASE_LABEL="d1-v58-hexa-eval"
COST_CAP_USD="${COST_CAP_USD:-0.30}"
COST_PER_HR="${COST_PER_HR:-0.27}"

# Mac local binaries
VAST_SSH_KEY="/Users/ghost/.vast/ssh/vast-key"
VASTAI="/Users/ghost/.local/bin/vastai"
[ -x "$VASTAI" ] || VASTAI="/Users/ghost/Library/Python/3.14/bin/vastai"
[ -x "$VASTAI" ] || { echo "ERROR: vastai CLI not found"; exit 1; }

set -euo pipefail
cd "$LOCAL_DIR"

echo "=== ${PHASE_ID} vast.ai dispatch ==="
echo "WARNING: cost cap analysis (2026-05-12) projects full eval ≈ \$1.93"
echo "         which is 6× the \$${COST_CAP_USD} cap. Fire only with override."
date -u

# ── 1) Find best offer ─────────────────────────────────────────────────────
echo "[1/8] Searching RTX 4090 offers under \$0.30/hr (note: GPU unused by hexa-interp)..."
OFFER=$($VASTAI search offers 'gpu_name=RTX_4090 num_gpus=1 reliability>0.98 dph_total<0.30 disk_space>30 inet_down>500' -o dph_total --raw 2>&1 | \
    python3 -c "
import json, sys
data = json.load(sys.stdin)
if not data: sys.stderr.write('no offers\n'); sys.exit(1)
print(data[0]['id'])
")
echo "  Selected offer ID: $OFFER"

# ── 2) Rent ────────────────────────────────────────────────────────────────
echo "[2/8] Renting instance..."
CREATE_OUT=$($VASTAI create instance "$OFFER" --image pytorch/pytorch:2.5.1-cuda12.1-cudnn9-runtime --disk 30 --ssh --direct --label "$PHASE_LABEL" --raw 2>&1)
INSTANCE_ID=$(echo "$CREATE_OUT" | python3 -c "
import json, sys
try: d=json.load(sys.stdin)
except: sys.stderr.write('parse fail\n'); sys.exit(1)
print(d.get('new_contract', d.get('contract_id', d.get('id', ''))))
")
[ -z "$INSTANCE_ID" ] && { echo "ERROR: no instance id"; exit 1; }
echo "  Instance ID: $INSTANCE_ID"
echo "$INSTANCE_ID" > vast_instance_id.txt

cleanup() {
    echo "[cleanup] Destroying instance $INSTANCE_ID..."
    $VASTAI destroy instance "$INSTANCE_ID" 2>&1 | head -3 || true
}
trap cleanup EXIT

# ── 3) Wait for SSH ready ──────────────────────────────────────────────────
echo "[3/8] Waiting for SSH ready..."
SSH_HOST=""; SSH_PORT=""
for i in $(seq 1 80); do
    INFO=$($VASTAI show instance "$INSTANCE_ID" --raw 2>/dev/null || true)
    [ -z "$INFO" ] && INFO="{}"
    STATUS=$(echo "$INFO" | python3 -c "import json,sys
try: d=json.load(sys.stdin); print(d.get('actual_status', ''))
except: print('')" 2>/dev/null || echo "")
    if [ "$STATUS" = "running" ]; then
        SSH_HOST=$(echo "$INFO" | python3 -c "import json,sys
try: d=json.load(sys.stdin); print(d.get('ssh_host','') or d.get('public_ipaddr',''))
except: pass" 2>/dev/null || echo "")
        SSH_PORT=$(echo "$INFO" | python3 -c "import json,sys
try: d=json.load(sys.stdin); print(d.get('ssh_port','') or d.get('direct_port_start',''))
except: pass" 2>/dev/null || echo "")
        if [ -n "$SSH_HOST" ] && [ -n "$SSH_PORT" ]; then
            if ssh -i "$VAST_SSH_KEY" -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o ConnectTimeout=10 -p "$SSH_PORT" "root@$SSH_HOST" 'echo READY' 2>&1 | grep -q READY; then
                echo "  SSH ready: $SSH_HOST:$SSH_PORT"
                break
            fi
            SSH_HOST=""
        fi
    fi
    echo "  ... attempt $i/80 status=$STATUS"
    sleep 5
done
[ -z "$SSH_HOST" ] && { echo "ERROR: SSH not ready"; exit 1; }
echo "$SSH_HOST:$SSH_PORT" > vast_ssh.txt

SSH_OPTS="-i $VAST_SSH_KEY -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null"
SSH_CMD="ssh $SSH_OPTS -p $SSH_PORT root@$SSH_HOST"
SCP_CMD="scp $SSH_OPTS -P $SSH_PORT"

# ── 4) Upload files: hexa binary + anima source + ckpt ─────────────────────
echo "[4/8] Uploading hexa interp binary (Linux x86_64, ELF 2MB, RFC 025/030/031/032/033)..."
$SSH_CMD 'mkdir -p /workspace/anima/state /workspace/anima/tool /workspace/anima/state/anima_phase1a1_color_cosmology_2026_05_12/ckpts /workspace/anima/state/anima_d1_v58_hexa_eval_2026_05_12 /workspace/anima/state/anima_d1_v58_parity_2026_05_12 /workspace/hexa-lang/build /workspace/hexa-lang/stdlib'

# ELF static binary (no shell-script wrapper)
$SCP_CMD "$HEXA_DIR/build/hexa_interp_linux_x86_64.real.real" "root@$SSH_HOST:/workspace/hexa-lang/build/hexa_interp"
$SSH_CMD 'chmod +x /workspace/hexa-lang/build/hexa_interp'

# hexa stdlib (if needed by anima_chat.hexa imports)
$SCP_CMD -r "$HEXA_DIR/stdlib" "root@$SSH_HOST:/workspace/hexa-lang/" || true

# anima_chat.hexa + harness
$SCP_CMD "$ANIMA_DIR/anima_chat.hexa" "root@$SSH_HOST:/workspace/anima/"
$SCP_CMD -r "$ANIMA_DIR/tool/hexa_native" "root@$SSH_HOST:/workspace/anima/tool/" || true

# State dirs (harness + parity baseline)
$SCP_CMD "$LOCAL_DIR/v58_hexa_4mode_5cell.hexa" "root@$SSH_HOST:/workspace/anima/state/anima_d1_v58_hexa_eval_2026_05_12/"
$SCP_CMD "$ANIMA_DIR/state/anima_d1_v58_parity_2026_05_12/python_first_token.json" "$ANIMA_DIR/state/anima_d1_v58_parity_2026_05_12/python_first_token_bos.json" "$ANIMA_DIR/state/anima_d1_v58_parity_2026_05_12/python_multi_token.json" "root@$SSH_HOST:/workspace/anima/state/anima_d1_v58_parity_2026_05_12/" || true

# Phase 1A.1 safetensors (570 MB, ~2 min upload at 500 Mbps)
$SCP_CMD "$PHASE1A1_DIR/ckpts/ckpt_phase1a1_sft.safetensors" "root@$SSH_HOST:/workspace/anima/state/anima_phase1a1_color_cosmology_2026_05_12/ckpts/"

# ── 5) Sanity check ───────────────────────────────────────────────────────
echo "[5/8] hexa interp binary check..."
$SSH_CMD '/workspace/hexa-lang/build/hexa_interp --help 2>&1 | head -3 || /workspace/hexa-lang/build/hexa_interp 2>&1 | head -3'

# ── 6) Parse harness ──────────────────────────────────────────────────────
echo "[6/8] Parse harness..."
$SSH_CMD 'cd /workspace/anima && /workspace/hexa-lang/build/hexa_interp parse state/anima_d1_v58_hexa_eval_2026_05_12/v58_hexa_4mode_5cell.hexa 2>&1 | head -5'

# ── 7) Run V5.8 hexa eval ─────────────────────────────────────────────────
echo "[7/8] Running V5.8 hexa eval (envelope: 1 cell × max_new=8 ≈ 60-80 min EPYC CPU)..."
$SSH_CMD 'cd /workspace/anima && HEXA_MEM_UNLIMITED=1 ANIMA_ROOT=/workspace/anima /workspace/hexa-lang/build/hexa_interp run state/anima_d1_v58_hexa_eval_2026_05_12/v58_hexa_4mode_5cell.hexa 2>&1 | tee state/anima_d1_v58_hexa_eval_2026_05_12/v58_hexa_remote.log' | tee v58_hexa_remote_tee.log

# ── 8) Download artifacts ─────────────────────────────────────────────────
echo "[8/8] Downloading artifacts..."
$SCP_CMD "root@$SSH_HOST:/workspace/anima/state/anima_d1_v58_hexa_eval_2026_05_12/v58_hexa_remote.log" "$LOCAL_DIR/v58_hexa_remote.log" || true

echo "=== ${PHASE_ID} dispatch DONE ==="
date -u
echo "Result: $LOCAL_DIR/v58_hexa_remote.log"
tail -20 "$LOCAL_DIR/v58_hexa_remote.log"
