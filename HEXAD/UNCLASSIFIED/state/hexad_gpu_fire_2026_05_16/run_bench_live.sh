#!/bin/bash
# run_bench_live.sh — run the Phase D cuBLAS bench on the ALREADY-RUNNING
# H100 SXM (instance 36871902, 209.20.157.9:27989) that a parallel
# "retry" attempt provisioned. Single SSH session: build (nvcc) + run +
# nvidia-smi-during + result.json cat + runtime_cuda.c compile-test.
set -uo pipefail
LOCAL_DIR="/Users/ghost/core/anima/state/hexad_gpu_fire_2026_05_16"
KEY="/Users/ghost/.vast/ssh/vast-key"
HOST="209.20.157.9"
PORT="27989"
SSH_OPTS=(-i "$KEY" -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o ServerAliveInterval=30)

echo "=== Phase D cuBLAS bench on live H100 SXM (36871902) ==="
date -u

echo "[1/4] Upload sources..."
ssh "${SSH_OPTS[@]}" -o ConnectTimeout=15 -p "$PORT" "root@$HOST" 'mkdir -p /workspace/gpu_fire' 2>&1 | grep -vE "Warning: Permanently|Welcome to vast|Have fun"
scp "${SSH_OPTS[@]}" -o ConnectTimeout=120 -P "$PORT" "$LOCAL_DIR/gpu_matmul_bench.c" "root@$HOST:/workspace/gpu_fire/" 2>&1 | grep -vE "Warning: Permanently|Welcome to vast|Have fun" | tail -1
scp "${SSH_OPTS[@]}" -o ConnectTimeout=120 -P "$PORT" "$LOCAL_DIR/runtime_cuda.c"     "root@$HOST:/workspace/gpu_fire/" 2>&1 | grep -vE "Warning: Permanently|Welcome to vast|Have fun" | tail -1

echo "[2/4] Build + bench + runtime_cuda compile — ONE session..."
ssh "${SSH_OPTS[@]}" -o ConnectTimeout=15 -p "$PORT" "root@$HOST" 'set +e
  echo "=== HW ==="; nvidia-smi --query-gpu=name,memory.total,driver_version,compute_cap --format=csv,noheader
  nvcc --version | tail -2
  cd /workspace/gpu_fire
  echo "=== build bench (nvcc -x cu) ==="
  nvcc -O2 -x cu gpu_matmul_bench.c -lcublas -lcudart -o gpu_matmul_bench 2>&1 | tail -12
  echo "BENCH_BUILD_RC=$?"
  ls -la gpu_matmul_bench 2>&1
  echo "=== run bench (nvidia-smi sampled 1Hz during) ==="
  rm -f nvidia_smi_during.csv
  ( for k in $(seq 1 120); do nvidia-smi --query-gpu=utilization.gpu,memory.used,power.draw --format=csv,noheader >> nvidia_smi_during.csv; sleep 1; done ) &
  SMIPID=$!
  LD_LIBRARY_PATH=/usr/local/cuda/lib64 ./gpu_matmul_bench
  echo "BENCH_RUN_RC=$?"
  kill $SMIPID 2>/dev/null
  echo "=== gpu_matmul_bench_result.json (INLINE — captured in local log) ==="
  cat /workspace/gpu_fire/gpu_matmul_bench_result.json 2>&1
  echo ""
  echo "=== nvidia-smi peak during (top util desc, 8) ==="
  sort -t, -k1 -rn nvidia_smi_during.csv 2>/dev/null | head -8
  echo "=== runtime_cuda.c compile-test (nvcc, links cublas) ==="
  nvcc -O2 -x cu -c runtime_cuda.c -o runtime_cuda.o 2>&1 | tail -8
  echo "RUNTIME_CUDA_RC=$?"
  ls -la runtime_cuda.o 2>&1
  nm runtime_cuda.o 2>&1 | grep -E "_hx_cuda_|cublas|cudaMalloc" | head -20
  echo "ALLDONE"' 2>&1 | grep -vE "Warning: Permanently|Welcome to vast|Have fun" | tee "$LOCAL_DIR/h100_live_session.log"

echo "[3/4] Pull artifacts..."
for f in gpu_matmul_bench_result.json nvidia_smi_during.csv runtime_cuda.o; do
  scp "${SSH_OPTS[@]}" -o ConnectTimeout=120 -P "$PORT" "root@$HOST:/workspace/gpu_fire/$f" "$LOCAL_DIR/${f/.csv/_h100.csv}" 2>&1 | grep -vE "Warning: Permanently|Welcome to vast|Have fun" | tail -1 && echo "  pulled $f" || echo "  PULL-FAIL $f"
done

echo "[4/4] === bench DONE === (instance kept running for d_corpus follow-on)"
date -u
