#!/bin/bash
# pod_bootstrap_train.sh — anima d768 forge-native CONVERGENCE on a fresh vast
# CUDA-devel pod (RTX 4090 sm_89). Builds a forge-CUDA-enabled hexa from
# hexa-lang main, then runs stdlib/flame/clm_prod.hexa (flame+forge, NO torch —
# a_train_flame_forge) on the 1.5GB 5-lang wiki corpus to CONVERGENCE, emitting a
# v0.2 (.clm, CLM\x01) checkpoint that anima_chat_cli can chat-decode.
#
# Proven recipe refs: state/laneg_d768_recover/README.md (forge-cuBLAS d768 fire),
# hexa-lang build/pod_build_run.sh (nvcc runtime_cuda.c + gcc -DHEXA_CUDA + link),
# commons g81 (build_aprime STAGE-0 bootstrap), clm_prod env knobs.
set -uo pipefail
LOG(){ echo "[$(date -u +%H:%M:%S)] $*"; }
WS=/workspace; mkdir -p "$WS"; cd "$WS"

# ── 1. build deps (CUDA-devel image already ships nvcc/cuda/gcc) ──────────────
LOG "apt deps"
apt-get update -qq && apt-get install -y -qq git build-essential clang ca-certificates >/dev/null 2>&1 || true

# ── 2. hexa-lang main ────────────────────────────────────────────────────────
if [ ! -d hexa-lang ]; then
  LOG "clone hexa-lang"
  git clone --depth 1 https://github.com/dancinlab/hexa-lang.git 2>&1 | tail -3
fi
cd hexa-lang
export HEXA_LANG="$PWD" HEXA_DIR="$PWD"

# ── 3. CPU hexa via build_aprime STAGE-0 (commons g81) ───────────────────────
# NOTE the later demo-aprime_cc `-arch` step fails on linux (hexa-lang handoff
# 4565ac05) — irrelevant: STAGE-0 emits self/runtime.c + runtime.a + build/hexat,
# which is all we need.
LOG "build_aprime STAGE-0 (CPU hexat)"
bash tool/build_aprime.sh > "$WS/build_aprime.log" 2>&1 || true
if [ ! -x build/hexat ]; then LOG "FATAL hexat not built — see $WS/build_aprime.log"; tail -25 "$WS/build_aprime.log"; exit 11; fi
LOG "hexat OK"; ./build/hexat --version 2>/dev/null | head -1 || true

# ── 4. forge-CUDA: compile runtime_cuda.c for this GPU's sm ───────────────────
DEV_CC=$(nvidia-smi --query-gpu=compute_cap --format=csv,noheader | head -1 | tr -d ".")
export HEXA_CUDA_ARCH="$DEV_CC"
LOG "DEV_CC=sm_${DEV_CC} (HEXA_CUDA_ARCH=$HEXA_CUDA_ARCH)"
CUDA_INC=$(dirname $(dirname $(which nvcc)))/include
nvcc -O2 -std=c++14 -DHEXA_CUDA -gencode arch=compute_${DEV_CC},code=sm_${DEV_CC} \
  -x cu -c self/cuda/runtime_cuda.c -o "$WS/runtime_cuda.o" 2>&1 | tail -15
[ -f "$WS/runtime_cuda.o" ] && LOG "runtime_cuda.o OK" || { LOG "FATAL nvcc runtime_cuda.c failed"; exit 12; }

# ── 5. forge-GPU descent smoke on the in-repo fixture (proves CUDA link) ──────
# clm_prod's own F-CLM-PROD-DESCENT on the tiny semantic_parallel fixture, GPU on.
# HEXA_FUSE_ALL=1 turns on the whole device-resident byte-eq forge stack.
LOG "forge-GPU smoke: clm_prod fixture descent"
export HEXA_CUDA=1 HEXA_FUSE_ALL=1
# the cuda link decision: hexa run must add -DHEXA_CUDA + runtime_cuda.o + cuda
# libs. The toolchain knob is HEXA_CUDA_LINK / HEXA_CUDA_ARCH (cuda_link_decision,
# hexa-lang 56e9fdad7). If `hexa run` does not auto-link, the sub-agent must wire
# the cc line (see hexa-lang build/pod_build_run.sh link step) — this is the one
# step that may need on-pod iteration.
export HEXA_CUDA_LINK=1
timeout 600 ./build/hexat self/test_hxcuda_matmul.hexa /tmp/hxc.c 2>&1 | tail -5 || true

# ── 6. corpus (transferred separately by orchestrator to $WS/corpus.txt) ──────
CORPUS="$WS/corpus_5lang_1p5gb.txt"
if [ ! -f "$CORPUS" ]; then LOG "WAIT: corpus not yet at $CORPUS — orchestrator pushes it"; fi

# ── 7. CONVERGENCE training (forge clm_prod) ─────────────────────────────────
# d768/E2 matches the golden v0.2 layout (chat-decodable). T=256 context.
# NSAMP large to cover the corpus; EPOCHS for CE to descend to coherence.
run_train(){
  export CLM_PROD_CORPUS="$CORPUS" CLM_PROD_D=768 CLM_PROD_E=2 CLM_PROD_T=256 \
         CLM_PROD_NSAMP=${NSAMP:-40000} CLM_PROD_EPOCHS=${EPOCHS:-3} \
         CLM_PROD_OUT="$WS/d768_5lang_converged.clm" \
         CLM_PROD_DEVFEED=1 CLM_PROD_BATCHED=1 HEXA_FUSE_ALL=1 HEXA_CUDA=1
  LOG "FIRE clm_prod d768/E2 T=256 NSAMP=$CLM_PROD_NSAMP EPOCHS=$CLM_PROD_EPOCHS"
  nohup ./build/hexat-run-or-hexa run stdlib/flame/clm_prod.hexa > "$WS/clm_prod_train.log" 2>&1 &
  echo $! > "$WS/train.pid"
  LOG "train PID $(cat $WS/train.pid) — tail $WS/clm_prod_train.log"
}
# orchestrator invokes run_train after corpus lands + smoke passes.
LOG "bootstrap done — build artifacts ready; awaiting corpus + train kick"
