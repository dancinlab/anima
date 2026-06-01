#!/usr/bin/env bash
set -uo pipefail
cd /root/.hx/src
export PATH=/root/.hx/bin:$PATH
echo "=== nuke ALL caches ==="
rm -rf /root/.hexa-cache /tmp/.hexa-runtime/* /root/.hx/src/self/cuda/runtime_cuda*.o 2>/dev/null
echo "=== hexa BUILD directly (cmd_build -> cuda_link_decision), HEXA_CUDA_LINK=$HEXA_CUDA_LINK ==="
HEXA_LANG=/root/.hx/src timeout 360 /root/.hx/bin/hexa build stdlib/flame/clm_prod.hexa /workspace/clm_prod_bin 2>&1 | grep -iE 'cuda|nvcc|cublas|forge|sm_|engaged|cpu-only|error|runtime.o|ENGAGED' | head -25
echo "=== build rc done; binary? ==="
ls -la /workspace/clm_prod_bin 2>/dev/null
echo "=== runtime_cuda.o produced? ==="
ls -la /root/.hx/src/self/cuda/runtime_cuda*.o 2>/dev/null
echo "=== .cuda-tagged runtime.o? ==="
ls -la /root/.hexa-cache/runtime.*.cuda.o 2>/dev/null
