#!/usr/bin/env bash
set -uo pipefail
cd /root/.hx/src
export PATH=/root/.hx/bin:$PATH
echo "=== nuke ALL caches (user-binary + runtime.o + transpile) ==="
rm -rf /root/.hexa-cache /root/.hx/src/build/artifacts/* /tmp/.hexa-runtime/* 2>/dev/null
echo "=== env check ==="
echo "HEXA_CUDA_LINK=$HEXA_CUDA_LINK"
echo "=== full clean build+run, FULL output head ==="
CLM_PROD_EPOCHS=1 CLM_PROD_NSAMP=2 HEXA_LANG=/root/.hx/src timeout 300 /root/.hx/bin/hexa run stdlib/flame/clm_prod.hexa 2>&1 | head -40
echo "=== rc=$? ==="
echo "=== was runtime.o keyed .cuda? ==="
ls -la /root/.hexa-cache/runtime.*.o 2>/dev/null | head
echo "=== runtime_cuda.o produced? ==="
ls -la /root/.hx/src/self/cuda/runtime_cuda*.o 2>/dev/null | head
