#!/usr/bin/env bash
set -uo pipefail
cd /root/.hx/src
export PATH=/root/.hx/bin:$PATH
echo "=== cuda_link_decision wiring in main.hexa ==="
grep -n 'cuda_link_decision' self/main.hexa | head
echo "=== clear hexa build cache ==="
rm -rf /root/.hexa-cache/* /root/.hx/src/build/artifacts/* /tmp/.hexa-runtime/* 2>/dev/null
echo "=== clean rebuild+run with HEXA_CUDA_LINK=1 (verbose grep) ==="
CLM_PROD_EPOCHS=1 CLM_PROD_NSAMP=2 HEXA_CUDA_LINK=1 HEXA_LANG=/root/.hx/src timeout 300 /root/.hx/bin/hexa run stdlib/flame/clm_prod.hexa 2>&1 | grep -iE 'cuda|nvcc|cublas|forge|link|sm_|engaged|cpu-only|mean CE' | head -20
echo "=== rc=$? ==="
