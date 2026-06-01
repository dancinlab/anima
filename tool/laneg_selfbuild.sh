#!/usr/bin/env bash
# Rebuild hexa FROM SOURCE on the pod via the canonical self-host stage build,
# so cuda_link_decision (the forge-GPU link fix, present in self/main.hexa but
# ABSENT from the prebuilt release hexa.real) is actually IN the binary. The
# fresh binary links the system 2.35 libc natively → NO glibc shim needed for it.
set -uo pipefail
cd /root/.hx/src
export PATH=/root/.hx/bin:$PATH
echo "=== seed .c present? (need runtime.c + hexa_cc.c + native + forge) ==="
ls self/runtime.c self/native/hexa_cc.c self/forge/forge_tier_v1.c 2>/dev/null
echo "=== run canonical self-host stage build -> /workspace/hexa_fresh ==="
CC=clang LIBS="-lm -lpthread -ldl" OUT_HEXA=/workspace/hexa_fresh \
  timeout 1200 bash tool/stage_build_hexa 2>&1 | grep -vE '^\s*$' | tail -40
echo "=== fresh binary? ==="
ls -la /workspace/hexa_fresh 2>/dev/null
echo "=== does fresh binary contain cuda_link_decision? ==="
strings /workspace/hexa_fresh 2>/dev/null | grep -c 'CUDA link ENGAGED'
strings /workspace/hexa_fresh 2>/dev/null | grep -iE 'CUDA link ENGAGED|building CPU-only' | head -3
echo "=== fresh binary glibc need ==="
/workspace/hexa_fresh --version 2>&1 | head -2
