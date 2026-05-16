#!/bin/bash
# run_corpus_live.sh — d_corpus_fire on the live H100 SXM (36871902).
# Uploads hexa-lang static linux x86_64 binary + HEXAD/D trainer +
# corpus, runs native (d=32 3L) + scaled (d=64 6L) configs.
#
# HONEST: d_corpus_fire is pure-hexa CPU list-math (NOT farr_matmul_gpu
# routed — d5_grad/d5_ce use list-of-doubles). GPU Util will be ~0 for
# this — the real-GPU proof is the cuBLAS bench (run_bench_live.sh, 51
# TFLOPS FP64). This run proves the trainer runs on Linux x86_64 (cross-
# platform from Mac arm64) at a meaningfully bigger scale than Mac. The
# d=768 12L GPU-routed train is Phase E (needs d_train5 farr_matmul wire).
set -uo pipefail
LOCAL_DIR="/Users/ghost/core/anima/state/hexad_gpu_fire_2026_05_16"
KEY="/Users/ghost/.vast/ssh/vast-key"
HOST="209.20.157.9"; PORT="27989"
O=(-i "$KEY" -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o ServerAliveInterval=30)
filt() { grep -vE "Warning: Permanently|Welcome to vast|Have fun"; }

echo "=== d_corpus_fire on live H100 SXM (36871902) ==="; date -u

echo "[1/5] Upload hexa-lang static linux x86_64 binary..."
ssh "${O[@]}" -o ConnectTimeout=15 -p "$PORT" "root@$HOST" 'mkdir -p /workspace/hexa/build /workspace/ap/HEXAD/D /workspace/ap/training' 2>&1 | filt
scp "${O[@]}" -o ConnectTimeout=120 -P "$PORT" /Users/ghost/core/hexa-lang/build/hexa_linux_x86_64 "root@$HOST:/workspace/hexa/hexa" 2>&1 | filt | tail -1
scp "${O[@]}" -o ConnectTimeout=120 -P "$PORT" /Users/ghost/core/hexa-lang/build/hexa_interp_linux_x86_64.real.real "root@$HOST:/workspace/hexa/build/hexa_interp_linux_x86_64.real.real" 2>&1 | filt | tail -1
ssh "${O[@]}" -o ConnectTimeout=15 -p "$PORT" "root@$HOST" 'cd /workspace/hexa/build && \
  cp hexa_interp_linux_x86_64.real.real hexa_interp_linux_x86_64.real && \
  ln -sf hexa_interp_linux_x86_64.real hexa_interp_linux_x86_64 && \
  ln -sf hexa_interp_linux_x86_64.real.real hexa_interp && \
  ln -sf hexa_interp_linux_x86_64.real.real hexa_interp.real && \
  chmod +x /workspace/hexa/hexa /workspace/hexa/build/* 2>/dev/null; echo HEXA_STAGED' 2>&1 | filt

echo "[2/5] Upload trainer + corpus..."
scp "${O[@]}" -o ConnectTimeout=120 -P "$PORT" /Users/ghost/core/anima/HEXAD/D/d_corpus_fire.hexa     "root@$HOST:/workspace/ap/HEXAD/D/" 2>&1 | filt | tail -1
scp "${O[@]}" -o ConnectTimeout=120 -P "$PORT" /Users/ghost/core/anima/HEXAD/D/d_train5_lib.hexa      "root@$HOST:/workspace/ap/HEXAD/D/" 2>&1 | filt | tail -1
scp "${O[@]}" -o ConnectTimeout=120 -P "$PORT" /Users/ghost/core/anima/HEXAD/D/corpus_loader_lib.hexa "root@$HOST:/workspace/ap/HEXAD/D/" 2>&1 | filt | tail -1
scp "${O[@]}" -o ConnectTimeout=120 -P "$PORT" /Users/ghost/core/anima/training/corpus_consciousness_v1.jsonl "root@$HOST:/workspace/ap/training/" 2>&1 | filt | tail -1
scp "${O[@]}" -o ConnectTimeout=120 -P "$PORT" /tmp/d_corpus_fire_scaled.hexa "root@$HOST:/workspace/ap/HEXAD/D/d_corpus_fire_scaled.hexa" 2>&1 | filt | tail -1
# d_corpus_fire.hexa hardcodes /Users/ghost/core/anima/... absolute paths — symlink them on the box.
ssh "${O[@]}" -o ConnectTimeout=15 -p "$PORT" "root@$HOST" 'mkdir -p /Users/ghost/core/anima/HEXAD/D /Users/ghost/core/anima/training && \
  ln -sf /workspace/ap/HEXAD/D/d_train5_lib.hexa /Users/ghost/core/anima/HEXAD/D/d_train5_lib.hexa && \
  ln -sf /workspace/ap/HEXAD/D/corpus_loader_lib.hexa /Users/ghost/core/anima/HEXAD/D/corpus_loader_lib.hexa && \
  ln -sf /workspace/ap/training/corpus_consciousness_v1.jsonl /Users/ghost/core/anima/training/corpus_consciousness_v1.jsonl && \
  echo PATHS_LINKED && ls -la /Users/ghost/core/anima/HEXAD/D/ /Users/ghost/core/anima/training/' 2>&1 | filt

echo "[3/5] Run d_corpus_fire NATIVE (d=32 3L 8w 80step) on Linux x86_64..."
ssh "${O[@]}" -o ConnectTimeout=15 -p "$PORT" "root@$HOST" 'cd /workspace/ap && \
  T0=$(date +%s); \
  HEXA_MEM_UNLIMITED=1 RESOURCE_LOCAL_HEXA=1 timeout 1800 /workspace/hexa/hexa run HEXAD/D/d_corpus_fire.hexa 2>&1 | tee /workspace/ap/native.log; \
  echo "NATIVE_RC=${PIPESTATUS[0]} WALL=$(( $(date +%s)-T0 ))s"' 2>&1 | filt | tee "$LOCAL_DIR/d_corpus_fire_native.log"

echo "[4/5] Run d_corpus_fire SCALED (d=64 6L 16w 120step)..."
ssh "${O[@]}" -o ConnectTimeout=15 -p "$PORT" "root@$HOST" 'cd /workspace/ap && \
  T0=$(date +%s); \
  HEXA_MEM_UNLIMITED=1 RESOURCE_LOCAL_HEXA=1 timeout 3600 /workspace/hexa/hexa run HEXAD/D/d_corpus_fire_scaled.hexa 2>&1 | tee /workspace/ap/scaled.log; \
  echo "SCALED_RC=${PIPESTATUS[0]} WALL=$(( $(date +%s)-T0 ))s"' 2>&1 | filt | tee "$LOCAL_DIR/d_corpus_fire_scaled.log"

echo "[5/5] === d_corpus_fire DONE ==="; date -u
