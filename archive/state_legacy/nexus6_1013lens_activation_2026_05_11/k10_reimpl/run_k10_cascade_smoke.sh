#!/bin/bash
# =============================================================================
# run_k10_cascade_smoke.sh — NEXUS-6 1013-lens K=10 cascade smoke (actual run)
# =============================================================================
# spec: state/nexus6_1013lens_activation_2026_05_11/spec.md §3.1, §4 (C1/F1)
# parent verdict: state/.../k10_reimpl/phase1_verdict_2026_05_12.md (Phase 1 PASS)
# task: NEXT.md §4 — K=10 reimpl cascade actual measurement entry
#
# Deterministic seed: ANIMA_LENS_SEED — value derived from canonical label
# "0xnexus6smoke" (not a valid hex literal; mapped to int 1735289110 via
# stable sum-of-char-codes for deterministic LCG seeding). Same seed → same
# 256-sample LCG x synthesized inside each v2 lens.
#
# Whitelist: spec §3.1 canonical 10 lens (binding via aggregator built-in).
# Hard constraints (NEXT.md §4):
#   - $0 CPU only (no Mistral-7B forward, no RunPod)
#   - wall < 30 min (K=10 actual ≈ 2.6 s historical)
#   - no chflags / chattr / --no-verify
# =============================================================================

set -u
set -o pipefail

REPO=/home/summer/mac_home/core/anima
LENS_DIR=$REPO/state/nexus6_1013lens_activation_2026_05_11/k10_reimpl
DATE=2026_05_12
OUT_JSON=$LENS_DIR/k10_cascade_smoke_results_$DATE.json

# Seed derived from "0xnexus6smoke" (canonical NEXUS-6 smoke label)
# sum of ASCII codes: 0=48 x=120 n=110 e=101 x=120 u=117 s=115 6=54 s=115 m=109 o=111 k=107 e=101
# = 48+120+110+101+120+117+115+54+115+109+111+107+101 = 1428 → multiplied by 1234567 for spread = 1762741476
# But to_int(...) inside the hexa needs to handle the literal as integer text.
SEED=1762741476

echo "[k10_cascade_smoke] start spec=nexus6_1013lens_activation_2026_05_11 K=10 seed=$SEED"
echo "[k10_cascade_smoke] lens_dir=$LENS_DIR"
echo "[k10_cascade_smoke] output=$OUT_JSON"

# 1. Emit helper via aggregator (idempotent)
/home/summer/.hx/bin/hexa run "$REPO/tool/anima_nexus_1013lens_cascade.hexa" --selftest \
  > /tmp/anima_k10_cascade_smoke_selftest.log 2>&1

# 2. Run the K=10 cascade with v2 lens dir + deterministic seed (no x_file)
NEXUS_LENSES_DIR="$LENS_DIR" \
  ANIMA_K=10 \
  ANIMA_LENS_SEED="$SEED" \
  ANIMA_OUTPUT="$OUT_JSON" \
  ANIMA_HEXA_BIN=/home/summer/.hx/bin/hexa \
  python3 /tmp/anima_nexus_1013lens_cascade_helper.hexa_tmp

RC=$?
echo "[k10_cascade_smoke] cascade rc=$RC -> $OUT_JSON"
exit $RC
