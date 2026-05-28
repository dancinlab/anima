#!/usr/bin/env bash
# pod_build_fire.sh — M4b longtrain decisive fire (pod-side build + fire)
# Runs on the H100 pod. Builds trainer.c+glue.c against the hexa-lang runtime
# (cuBLAS engaged via glue.c strong override + -lcuda), then fires the trainer
# with the per-pod M4B_EPOCHS budget. Writes /work/DONE when finished.
set -uo pipefail
cd /work
echo "=== M4b longtrain pod build+fire — $(date -u) ==="
echo "M4B_EPOCHS=${M4B_EPOCHS:-<unset>}  M4B_TAG=${M4B_TAG:-?}"

# ── unpack runtime tree ──
mkdir -p /work
tar xzf /work/self.tar.gz -C /work
echo "self/ unpacked: $(ls /work/self | tr '\n' ' ')"

# ── stage data/BPE on the trainer-expected pod paths ──
mkdir -p /opt/qwen /opt/corpus /opt/anima/state/m4b_longtrain
cp /work/merges.txt /opt/qwen/merges.txt
cp /work/vocab.json /opt/qwen/vocab.json
cp /work/corpus_consciousness_v2_diverse.jsonl /opt/corpus/corpus_consciousness_v2_diverse.jsonl
echo "data staged: merges=$(wc -l </opt/qwen/merges.txt) corpus=$(wc -l </opt/corpus/corpus_consciousness_v2_diverse.jsonl)"

# ── build: cuBLAS-engaged (glue.c strong hexa_cuda_available + -lcuda) ──
echo "=== build: nvcc runtime_cuda.o ==="
nvcc -O2 -std=c++14 -DHEXA_CUDA -arch=sm_90 -x cu -c self/cuda/runtime_cuda.c -o runtime_cuda.o > build_cuda.log 2>&1
NVCC_RC=$?
echo "nvcc rc=$NVCC_RC"; tail -5 build_cuda.log
if [ $NVCC_RC -ne 0 ]; then echo "BUILD_FAIL nvcc"; echo "BUILD_FAIL nvcc" > /work/DONE; exit 1; fi

echo "=== build: clang link (cuBLAS + driver) ==="
clang -O2 -D_GNU_SOURCE -D_XOPEN_SOURCE=600 -DHEXA_CUDA \
  -I self -I /usr/local/cuda/include -Wno-trigraphs -fbracket-depth=8192 \
  trainer.c glue.c self/runtime.c runtime_cuda.o \
  -L/usr/local/cuda/lib64 -L/usr/lib/x86_64-linux-gnu \
  -lcublas -lcudart -lcudart_static -lcuda -ldl -lrt -lm -lpthread -lstdc++ \
  -o trainer > build_link.log 2>&1
LINK_RC=$?
echo "clang rc=$LINK_RC"; tail -15 build_link.log
if [ $LINK_RC -ne 0 ] || [ ! -x /work/trainer ]; then echo "BUILD_FAIL link"; echo "BUILD_FAIL link" > /work/DONE; exit 1; fi
echo "trainer built: $(ls -la /work/trainer | awk '{print $5}') bytes"

# ── cuBLAS-engage sanity (nvidia-smi) ──
nvidia-smi --query-gpu=name,memory.total,utilization.gpu --format=csv 2>&1 | head -3

# ── nvidia-smi telemetry in background (bounded by trainer wall) ──
( while [ ! -f /work/DONE ]; do
    nvidia-smi --query-gpu=timestamp,utilization.gpu,utilization.memory,memory.used --format=csv,noheader 2>/dev/null
    sleep 15
  done ) > /work/nvidia_smi_during.csv 2>&1 &
SMI_PID=$!

# ── fire ──
echo "=== fire: M4B_EPOCHS=${M4B_EPOCHS:-default} ==="
/usr/bin/time -v env M4B_EPOCHS="${M4B_EPOCHS:-}" ./trainer > trainer.out 2> trainer.err
TRC=$?
echo "trainer_rc=$TRC" > trainer_meta.txt
echo "wall: see trainer.err GNU time block" >> trainer_meta.txt
echo "M4B_EPOCHS=${M4B_EPOCHS:-default} tag=${M4B_TAG:-?}" >> trainer_meta.txt
kill $SMI_PID 2>/dev/null
echo "=== trainer tail ==="; tail -25 trainer.out
echo "=== result.json ==="; cat /opt/anima/state/m4b_longtrain/result.json 2>&1
cp /opt/anima/state/m4b_longtrain/result.json /work/result.json 2>/dev/null
echo "trainer_rc=$TRC" > /work/DONE
echo "=== DONE rc=$TRC ==="
