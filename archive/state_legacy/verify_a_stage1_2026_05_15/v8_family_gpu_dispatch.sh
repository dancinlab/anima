#!/usr/bin/env bash
# V8 family GPU sweep dispatch — 5 hypotheses (H_182/183/185/186/187)
# Stage 2 INSUFFICIENT 5 가설 의 GPU fire 작업
#
# 사용자 directive 2026-05-15 "GPU 제한없음 go / all bg go"
# Cost: $200-600 estimate (Vast.ai H100 or 4×A100, ~6-12hr wall)
#
# 본 script 는 *작성 only* — actual dispatch 는 사용자 verbatim 'V8 FIRE COST'
# 발화 후 실행 (CLM.tape §7.5 g6 cost-bearing 정합)

set -euo pipefail

# Config
BUDGET_MAX=600
WALL_MAX_HR=12
GPU="A100_80GB"
BG_NAME="v8_family_sweep_$(date +%Y%m%d_%H%M)"

# V8 family targets:
#   H_182 V8 B-family bio (10 Hc)
#   H_183 V8 Q-family quantum (5 Hc)
#   H_185 V8 U-family fusion (5 Hc)
#   H_186 V8 architectural (8 Hc)
#   H_187 Trinity/TB/DOM (12 Hc)
# Total: 5 family × ≥5 sub-Hc = ≥25 mechanism graft sims

# Per-mechanism design:
#   anima v5-mitosis 1L baseline + V8 mechanism graft
#   cells ∈ {8, 16, 32, 64} × 5-seed × 4 mechanism per family
#   Φ measurement (anima Φ★ proxy + PyPhi 1.2.0 small-cells)
#   verdict: PASS if max-Φ ≥ baseline + 25% (or matches V8 spec claim)

echo "V8 family GPU dispatch script — DRAFT"
echo "Status: SCRIPT-READY, awaiting user verbatim 'V8 FIRE COST'"
echo ""
echo "Targets:"
echo "  H_182 V8 B-family bio (10 Hc)"
echo "  H_183 V8 Q-family quantum (5 Hc)"
echo "  H_185 V8 U-family fusion (5 Hc)"
echo "  H_186 V8 architectural (8 Hc)"
echo "  H_187 Trinity/TB/DOM (12 Hc)"
echo ""
echo "Budget: ${BUDGET_MAX} USD"
echo "Wall: ${WALL_MAX_HR}hr max"
echo "GPU: ${GPU}"
echo "BG name: ${BG_NAME}"
echo ""
echo "Dispatch path: tool/dispatch_vast_mac_template.sh (anima existing)"
echo "Per-pod: 4×A100 ≈ \$3.2/hr × 8-12hr ≈ \$25-40 per family"
echo "Aggregate 5 family: \$125-200 (parallel pods) or \$200-400 (serial)"
echo ""
echo "Awaiting user fire keyword:"
echo "  'V8 FIRE COST \$200-600' verbatim 발화 → dispatch_vast_*.sh 실행"
