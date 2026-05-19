#!/bin/bash
# remote_fire.sh — runs ON the RunPod A100 box. One session: GPU smoke +
# d=256·4L seed=44 d_corpus_fire + nvidia-smi sampling. Results cat'd inline.
set +e
export PATH=/usr/local/cuda/bin:/workspace/hexa:$PATH
echo "=== HOST ==="; hostname; date -u
nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv,noheader
nvcc --version | tail -2

echo "=== stage hexa binary + sidecar ==="
cd /workspace
cp hexa_linux_x86_64 /workspace/hexa/hexa
cp hexa_interp_linux_x86_64.real.real /workspace/hexa/build/hexa_interp_linux_x86_64.real.real
cd /workspace/hexa/build
cp hexa_interp_linux_x86_64.real.real hexa_interp_linux_x86_64.real
ln -sf hexa_interp_linux_x86_64.real hexa_interp_linux_x86_64
ln -sf hexa_interp_linux_x86_64.real.real hexa_interp
ln -sf hexa_interp_linux_x86_64.real.real hexa_interp.real
chmod +x /workspace/hexa/hexa /workspace/hexa/build/*
cd /workspace
# Place anima sources at the hardcoded path the .hexa file imports/opens
cp HEXAD/D/d_train5_lib.hexa     /Users/ghost/core/anima/HEXAD/D/d_train5_lib.hexa
cp HEXAD/D/corpus_loader_lib.hexa /Users/ghost/core/anima/HEXAD/D/corpus_loader_lib.hexa
cp training/corpus_consciousness_v1.jsonl /Users/ghost/core/anima/training/corpus_consciousness_v1.jsonl
ls -la /Users/ghost/core/anima/HEXAD/D/ /Users/ghost/core/anima/training/

echo "=== [GPU SMOKE] build runtime_cuda.c (nvcc, links cublas) — rfc040 real-GPU proof ==="
cd /workspace/gpu_fire
cp /workspace/runtime_cuda.c .
cp /workspace/gpu_matmul_bench.c .
nvcc -O2 -x cu -c runtime_cuda.c -o runtime_cuda.o 2>&1 | tail -8
echo "RUNTIME_CUDA_COMPILE_RC=$?"
ls -la runtime_cuda.o 2>&1
nm runtime_cuda.o 2>&1 | grep -E "_hx_cuda_|cublas|cudaMalloc" | head -20
echo "=== [GPU SMOKE] cuBLAS matmul bench (5 shapes) — nvidia-smi util>0 proof ==="
nvcc -O2 -x cu gpu_matmul_bench.c -lcublas -lcudart -o gpu_matmul_bench 2>&1 | tail -8
echo "BENCH_BUILD_RC=$?"
rm -f nvidia_smi_during.csv
( for k in $(seq 1 60); do nvidia-smi --query-gpu=utilization.gpu,memory.used,power.draw --format=csv,noheader >> nvidia_smi_during.csv; sleep 1; done ) &
SMIPID=$!
LD_LIBRARY_PATH=/usr/local/cuda/lib64 ./gpu_matmul_bench
echo "BENCH_RUN_RC=$?"
kill $SMIPID 2>/dev/null
echo "=== gpu_matmul_bench_result.json ==="
cat /workspace/gpu_fire/gpu_matmul_bench_result.json 2>&1
echo "=== nvidia-smi during-bench (top 8 by util) ==="
sort -t, -k1 -rn nvidia_smi_during.csv 2>/dev/null | head -8

echo "=== [d_corpus_fire] d=256 4L nh=4 nkv=2 h=512 T=64 nsamp=16 80step seed=44 ==="
cd /workspace
cp d_corpus_fire_d256_4L.hexa /Users/ghost/core/anima/HEXAD/D/d_corpus_fire_d256_4L.hexa
nvidia-smi --query-gpu=memory.used,utilization.gpu --format=csv,noheader > /workspace/nvsmi_dcorpus_pre.csv
( for k in $(seq 1 1200); do nvidia-smi --query-gpu=utilization.gpu,memory.used,power.draw --format=csv,noheader >> /workspace/nvsmi_dcorpus_during.csv; sleep 2; done ) &
DSMIPID=$!
cd /workspace
PATH=/workspace/hexa:$PATH HEXA_MEM_UNLIMITED=1 RESOURCE_LOCAL_HEXA=1 \
  timeout 6000 /workspace/hexa/hexa run /Users/ghost/core/anima/HEXAD/D/d_corpus_fire_d256_4L.hexa 2>&1 | tee /workspace/d_corpus_fire_d256_4L.log
echo "DCORPUS_RC=$?"
kill $DSMIPID 2>/dev/null
nvidia-smi --query-gpu=memory.used,utilization.gpu --format=csv,noheader > /workspace/nvsmi_dcorpus_post.csv
echo "=== nvsmi d_corpus (top 8 by util) ==="
sort -t, -k1 -rn /workspace/nvsmi_dcorpus_during.csv 2>/dev/null | head -8
echo "=== d_corpus_fire_d256_4L.log (full) ==="
cat /workspace/d_corpus_fire_d256_4L.log 2>&1
echo "ALLDONE"; date -u
