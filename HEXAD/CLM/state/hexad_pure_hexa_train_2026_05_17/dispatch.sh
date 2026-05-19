#!/usr/bin/env bash
# state/hexad_pure_hexa_train_2026_05_17/dispatch.sh
# pure-hexa hexa-cpu training-to-convergence FIRE recipe (Mac local, $0)
# ──────────────────────────────────────────────────────────────────────────────
#
#  Goal: first **captured FINAL gn2 in pure-hexa AT A LARGER SCALE THAN
#        Phase E2's d=32·3L·80-step CPU-equiv anchor**.
#
#  Substrate: compiled-native CPU pure-hexa (NOT .py, NOT GPU).
#  Anchor chain: Phase E2 (cpu_equiv_e2.log d=32·3L·80-step BIT-EQUAL)
#                → this fire (d=64·3L·300-step + d=128·4L·200-step FINAL).
#  Build gate: HEXA_MAC_BUILD_OK=1 (2026-04-20 kernel panic guard bypass).
#  Mem gate:   HEXA_MEM_UNLIMITED=1 (AdamW loop intermediate alloc > 4GB cap).
# ──────────────────────────────────────────────────────────────────────────────
set -euo pipefail

cd /Users/ghost/core/anima

OUT=state/hexad_pure_hexa_train_2026_05_17
mkdir -p /tmp/hexa_converge_build "$OUT"

# ── Fire #1: d=64·n_layer=3·300step (Mac local, ~360s wall) ───────────────
echo "=== d=64·3L·300step build ==="
HEXA_MAC_BUILD_OK=1 hexa build HEXAD/D/d_converge_fire.hexa \
    -o /tmp/hexa_converge_build/d_converge_fire 2>&1 | tail -3

echo "=== d=64·3L·300step run ==="
HEXA_MEM_UNLIMITED=1 /usr/bin/time -l \
    /tmp/hexa_converge_build/d_converge_fire 2>&1 | tee "$OUT/train_d64.log"

# ── Fire #2: d=128·n_layer=4·200step (Mac local, ~30 min estimate) ────────
echo "=== d=128·4L·200step build ==="
HEXA_MAC_BUILD_OK=1 hexa build "$OUT/d_converge_fire_d128.hexa" \
    -o /tmp/hexa_converge_build/d_converge_fire_d128 2>&1 | tail -3

echo "=== d=128·4L·200step run ==="
HEXA_MEM_UNLIMITED=1 /usr/bin/time -l \
    /tmp/hexa_converge_build/d_converge_fire_d128 2>&1 | tee "$OUT/train_d128.log"

echo "=== dispatch complete ==="
