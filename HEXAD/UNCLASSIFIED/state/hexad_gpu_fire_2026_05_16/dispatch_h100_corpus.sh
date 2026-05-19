#!/bin/bash
# state/hexad_gpu_fire_2026_05_16/dispatch_h100_corpus.sh
# Phase D follow-on: run d_corpus_fire (real-corpus from-scratch hexa-lang
# trainer) on the H100 box that dispatch_h100.sh already provisioned.
#
# Reads instance ID + SSH host:port from vast_instance_id.txt + vast_ssh.txt
# (written by dispatch_h100.sh step 3). Uploads:
#   - hexa-lang static linux x86_64 binary + interp
#   - HEXAD/D/d_corpus_fire.hexa + d_train5_lib.hexa + corpus_loader_lib.hexa
#   - training/corpus_consciousness_v1.jsonl (152 KB)
#   - scaled variant d_corpus_fire_scaled.hexa (d=64 6L T=32 16w 120 step)
#
# Then runs:
#   - native config (d=32 3L 8w 80 step) — proves x86_64 linux compat
#   - scaled config (d=64 6L 16w 120 step) — meaningfully bigger than Mac
#
# NOTE — d=768 12L target from mission: pure-hexa CPU-list math, not GPU-
# routed (file's own honest C3: "기질 한계 — pure-hexa = CPU farr 연산,
# GPU CUDA 커널 없음. 진짜 d=768·12L 언어모델 학습은 GPU 텐서커널 필요
# ⟹ d=768·12L 실-규모 학습은 pure-hexa CPU 기질에서 비현실적").
# d=64 6L is the meaningful-scale upper bound for pure-hexa CPU; honest
# Phase D = bench (real H100 cuBLAS) + scaled corpus train (Linux x86_64
# CPU-native). d=768 GPU-routed = Phase E (d_train5 needs farr_matmul wire).

set -uo pipefail

LOCAL_DIR="/Users/ghost/core/anima/state/hexad_gpu_fire_2026_05_16"
VAST_SSH_KEY="/Users/ghost/.vast/ssh/vast-key"
VASTAI="/Users/ghost/Library/Python/3.14/bin/vastai"

[ -f "$LOCAL_DIR/vast_instance_id.txt" ] || { echo "ERR: vast_instance_id.txt missing — dispatch_h100.sh must reach [3/9] first"; exit 1; }
[ -f "$LOCAL_DIR/vast_ssh.txt" ]         || { echo "ERR: vast_ssh.txt missing — dispatch_h100.sh must reach [3/9] first"; exit 1; }
INSTANCE_ID=$(cat "$LOCAL_DIR/vast_instance_id.txt")
SSH_LINE=$(cat "$LOCAL_DIR/vast_ssh.txt")     # host:port
SSH_HOST="${SSH_LINE%:*}"
SSH_PORT="${SSH_LINE##*:}"
SSH_OPTS="-i $VAST_SSH_KEY -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o ServerAliveInterval=60"
SSH_CMD="ssh $SSH_OPTS -p $SSH_PORT root@$SSH_HOST"
SCP_CMD="scp $SSH_OPTS -P $SSH_PORT -o ConnectTimeout=3600"

echo "=== d_corpus_fire on H100 box (Phase D corpus follow-on) ==="
echo "  Instance: $INSTANCE_ID  SSH: $SSH_HOST:$SSH_PORT"
date -u

# ── 1) Wait for SSH ready (in case main dispatch still on step 3) ────
echo "[1/6] Verify SSH alive..."
if ! $SSH_CMD 'echo READY' 2>&1 | grep -q READY; then
    echo "ERR: SSH not responding — wait for dispatch_h100.sh to reach [4/9]"; exit 1
fi

# ── 2) Upload hexa-lang static linux binary + interp ─────────────────
echo "[2/6] Upload hexa-lang static linux x86_64 binaries..."
$SSH_CMD 'mkdir -p /workspace/hexa/build'
$SCP_CMD /Users/ghost/core/hexa-lang/build/hexa_linux_x86_64 \
    "root@$SSH_HOST:/workspace/hexa/hexa"
$SCP_CMD /Users/ghost/core/hexa-lang/build/hexa_interp_linux_x86_64.real.real \
    "root@$SSH_HOST:/workspace/hexa/build/hexa_interp_linux_x86_64.real.real"
# The dispatcher (hexa_linux_x86_64) resolves sidecar via dirname(argv0)+/build/
# Also provide the names the dispatcher looks for
$SSH_CMD 'cd /workspace/hexa/build && cp hexa_interp_linux_x86_64.real.real hexa_interp_linux_x86_64.real && \
          ln -sf hexa_interp_linux_x86_64.real hexa_interp_linux_x86_64 && \
          ln -sf hexa_interp_linux_x86_64.real.real hexa_interp && \
          ln -sf hexa_interp_linux_x86_64.real.real hexa_interp.real && \
          chmod +x /workspace/hexa/hexa /workspace/hexa/build/* && ls -la /workspace/hexa/ /workspace/hexa/build/'

# ── 3) Upload anima HEXAD/D sources + corpus + scaled variant ────────
echo "[3/6] Upload anima d_corpus_fire payload..."
$SSH_CMD 'mkdir -p /workspace/anima_payload/HEXAD/D /workspace/anima_payload/training'
$SCP_CMD /Users/ghost/core/anima/HEXAD/D/d_corpus_fire.hexa \
    "root@$SSH_HOST:/workspace/anima_payload/HEXAD/D/"
$SCP_CMD /Users/ghost/core/anima/HEXAD/D/d_train5_lib.hexa \
    "root@$SSH_HOST:/workspace/anima_payload/HEXAD/D/"
$SCP_CMD /Users/ghost/core/anima/HEXAD/D/corpus_loader_lib.hexa \
    "root@$SSH_HOST:/workspace/anima_payload/HEXAD/D/"
$SCP_CMD /Users/ghost/core/anima/training/corpus_consciousness_v1.jsonl \
    "root@$SSH_HOST:/workspace/anima_payload/training/"
$SCP_CMD /tmp/d_corpus_fire_scaled.hexa \
    "root@$SSH_HOST:/workspace/anima_payload/HEXAD/D/d_corpus_fire_scaled.hexa"

# The d_corpus_fire.hexa hardcodes /Users/ghost/core/anima/training/corpus_*.jsonl
# Replicate that path on the linux box via symlink so the import + file open work.
$SSH_CMD 'mkdir -p /Users/ghost/core/anima/HEXAD/D /Users/ghost/core/anima/training && \
          ln -sf /workspace/anima_payload/HEXAD/D/d_train5_lib.hexa /Users/ghost/core/anima/HEXAD/D/d_train5_lib.hexa && \
          ln -sf /workspace/anima_payload/HEXAD/D/corpus_loader_lib.hexa /Users/ghost/core/anima/HEXAD/D/corpus_loader_lib.hexa && \
          ln -sf /workspace/anima_payload/training/corpus_consciousness_v1.jsonl /Users/ghost/core/anima/training/corpus_consciousness_v1.jsonl && \
          ls -la /Users/ghost/core/anima/HEXAD/D/ /Users/ghost/core/anima/training/'

# ── 4) Run d_corpus_fire NATIVE config (d=32 3L 8w 80step) ───────────
echo "[4/6] Run d_corpus_fire native config (d=32 3L 8w 80step) on Linux x86_64..."
$SSH_CMD 'cd /workspace/anima_payload && \
    nvidia-smi --query-gpu=memory.used,utilization.gpu --format=csv,noheader > /tmp/nvidia_smi_dcorpus_pre.csv ; \
    PATH=/workspace/hexa:$PATH HEXA_MEM_UNLIMITED=1 RESOURCE_LOCAL_HEXA=1 \
    timeout 1800 /workspace/hexa/hexa run HEXAD/D/d_corpus_fire.hexa 2>&1 | tee /workspace/anima_payload/d_corpus_fire_native.log ; \
    echo NATIVE_RC=$? ; \
    nvidia-smi --query-gpu=memory.used,utilization.gpu --format=csv,noheader > /tmp/nvidia_smi_dcorpus_post.csv ; \
    cat /tmp/nvidia_smi_dcorpus_post.csv' 2>&1 | tee "$LOCAL_DIR/dispatch_corpus_native.log"

# ── 5) Run d_corpus_fire SCALED config (d=64 6L 16w 120step) ─────────
echo "[5/6] Run d_corpus_fire scaled config (d=64 6L 16w 120step)..."
$SSH_CMD 'cd /workspace/anima_payload && \
    PATH=/workspace/hexa:$PATH HEXA_MEM_UNLIMITED=1 RESOURCE_LOCAL_HEXA=1 \
    timeout 3600 /workspace/hexa/hexa run HEXAD/D/d_corpus_fire_scaled.hexa 2>&1 | tee /workspace/anima_payload/d_corpus_fire_scaled.log ; \
    echo SCALED_RC=$?' 2>&1 | tee "$LOCAL_DIR/dispatch_corpus_scaled.log"

# ── 6) Pull artifacts ────────────────────────────────────────────────
echo "[6/6] Pull d_corpus_fire artifacts..."
pull() { $SCP_CMD "root@$SSH_HOST:$1" "$2" 2>&1 | head -3 || echo "  pull-fail $1"; }
pull "/workspace/anima_payload/d_corpus_fire_native.log" "$LOCAL_DIR/d_corpus_fire_native.log"
pull "/workspace/anima_payload/d_corpus_fire_scaled.log" "$LOCAL_DIR/d_corpus_fire_scaled.log"

echo "=== Phase D corpus follow-on DONE ==="
date -u
echo "  native log: $LOCAL_DIR/d_corpus_fire_native.log"
echo "  scaled log: $LOCAL_DIR/d_corpus_fire_scaled.log"
