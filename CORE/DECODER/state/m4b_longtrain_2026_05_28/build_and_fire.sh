#!/bin/bash
# M4b longtrain — pod build + fire (run on the H100 pod)
set -e
export PATH=/usr/local/cuda/bin:$PATH
# RunPod pytorch image ships CUDA_VISIBLE_DEVICES="" (empty = hide-all) which
# breaks cudaSetDevice/cublasCreate — force device 0 visible.
export CUDA_VISIBLE_DEVICES=0
# dec_undertrain budget: 6 epochs over the full 1.2M-token corpus =
# ~7.3M token-presentations ≈ 47× V (the toy's "tens × vocab" escape regime).
export M4B_EPOCHS=6
cd /work
echo "=== M4b longtrain pod build + fire ==="
date -u
echo "nvcc: $(command -v nvcc)  CUDA_VISIBLE_DEVICES=$CUDA_VISIBLE_DEVICES  M4B_EPOCHS=$M4B_EPOCHS"

# pod-side dir_create codegen-gap is gone (we use fs_mkdir_p), but pre-create
# the output dir as belt-and-suspenders so the result write never fails.
mkdir -p /opt/anima/state/m4b_longtrain

# trim sed already applied on Mac (rt_str_trim). dir_create already → fs_mkdir_p.

echo "=== nvcc compile runtime_cuda.c (sm_90) ==="
nvcc -O2 -std=c++14 -DHEXA_CUDA -arch=sm_90 -x cu -c self/cuda/runtime_cuda.c -o runtime_cuda.o 2> build_cuda.log || { echo "NVCC_FAIL"; tail -30 build_cuda.log; exit 11; }
echo "runtime_cuda.o: $(ls -la runtime_cuda.o | awk '{print $5}') bytes"

echo "=== link trainer (cuBLAS; fresh runtime has real cuda_available under -DHEXA_CUDA — NO glue.c) ==="
# clang is required (-fbracket-depth is clang-only; gcc lacks it)
CC=clang
echo "using CC=$CC"
$CC -O2 -D_GNU_SOURCE -D_XOPEN_SOURCE=600 -DHEXA_CUDA \
  -I self -I /usr/local/cuda/include -Wno-trigraphs -fbracket-depth=4096 \
  -Wno-incompatible-pointer-types-discards-qualifiers -Wno-macro-redefined \
  trainer.c self/runtime.c runtime_cuda.o \
  -L/usr/local/cuda/lib64 -L/usr/lib/x86_64-linux-gnu \
  -lcublas -lcudart -lcudart_static -lcuda -ldl -lrt -lm -lpthread -lstdc++ \
  -o trainer 2> build_link.log || { echo "LINK_FAIL"; tail -40 build_link.log; exit 12; }
echo "trainer: $(ls -la trainer | awk '{print $5}') bytes"

echo "=== GPU preflight (cuda_available smoke) ==="
nvidia-smi --query-gpu=name,memory.total,memory.used --format=csv,noheader

echo "=== FIRE (nohup, detached) ==="
# M4B_EPOCHS unset → trainer auto-scales to ~3M token-presentations (≫ V).
nohup ./trainer > /opt/anima/state/m4b_longtrain/train.log 2>&1 &
echo "REMOTE_PID=$!"
echo "FIRE_LAUNCHED"
