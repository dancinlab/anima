#!/usr/bin/env bash
# fire_all_philosophy_bgs.sh — NEXT.md §7 4-BG fire orchestration emit
#
# DEFAULT-SAFE: 본 script 는 fire 명령을 **emit** 만 함 (실제 RunPod API 호출 X).
# 실 fire 는 사용자가 emit 된 명령을 보고 별도 execute trigger.
# raw#9 + anima_runpod_preset_dispatcher 의 --emit-only default 정합.
#
# Usage:
#   bash state/fire_all_philosophy_bgs.sh           # emit-only (default)
#   bash state/fire_all_philosophy_bgs.sh --plan    # 자세한 sequence 출력
#
# Cost cap aware:
#   - P-AFR ($5-30) → $20 default cap 내 → orchestrator dispatch 가능
#   - P-SPK ($5-20) → cap 내 → dispatch 가능
#   - P-IDR ($40-80) → cap 초과 → max_cost_cap_usd 명시 override 필요
#   - P-ETH ($85-165) → cap 초과 → override + multi-pod 분할 검토
#
# Recommended fire order: 7.B (저렴, inference-only) → 7.D (분석) → 7.A (FT) → 7.C (DPO FT)

set -euo pipefail

ANIMA_ROOT="${ANIMA_ROOT:-/Users/ghost/core/anima}"
RUN_TS="$(date +%Y%m%d_%H%M%S)"
BASE_OUT="${ANIMA_ROOT}/state"

# Default ckpt: public anima paradigm-j (own 37 promote, F2 PASS)
PUBLIC_CKPT="${PUBLIC_CKPT:-dancinlab/clm-v4-paradigm-j-50k-final-path-a-remapped}"
# Private BG-LB Engine A/G (substrate-research only, own 17 정합)
BG_LB_CKPT="${BG_LB_CKPT:-dancinlab/clm-v5-bg-lb-stage1}"

echo "=========================================="
echo "Philosophy ablation 4-BG fire emit"
echo "Generated: $(date -Iseconds)"
echo "=========================================="
echo

# 7.B P-AFR: inference-only, $5-30
echo "## 7.B P-AFR (NO ASSISTANT FRAMING) — inference-time A/B"
echo "Cost: \$5-30, Wall: 0.25d, Cap: within \$20 default"
cat <<EOF
cd ${ANIMA_ROOT}
awk '/^```python/,/^```$/' state/p_afr_assistant_framing_2026_05_12/harness.py.md | sed '1d;$d' > /tmp/p_afr_harness.py
python /tmp/p_afr_harness.py \\
  --ckpt ${PUBLIC_CKPT} \\
  --outdir state/p_afr_assistant_framing_2026_05_12/run_${RUN_TS}/

# verdict: state/p_afr_assistant_framing_2026_05_12/run_${RUN_TS}/raw_responses.json
# next: LLM-judge scoring via Claude API (Opus 4.7) on raw responses
EOF
echo

# 7.D P-SPK: analysis-only, $5-20
echo "## 7.D P-SPK (NO SPEAK() DESIGN→falsifiable) — tension-output correlation"
echo "Cost: \$5-20, Wall: 0.5d, Cap: within \$20 default"
cat <<EOF
cd ${ANIMA_ROOT}
awk '/^```python/,/^```$/' state/p_spk_speak_reframe_2026_05_12/harness.py.md | sed '1d;$d' > /tmp/p_spk_harness.py
python /tmp/p_spk_harness.py \\
  --ckpt ${BG_LB_CKPT} \\
  --outdir state/p_spk_speak_reframe_2026_05_12/run_${RUN_TS}/ \\
  --engine-a-layers 0,2,4 \\
  --engine-g-layers 1,3,5

# verdict.json 산출, rho_real / rho_control / Fisher-z 비교
EOF
echo

# 7.A P-IDR: 2× short FT, $40-80, CAP OVERRIDE NEEDED
echo "## 7.A P-IDR (NO IDENTITY RULES) — 2× short FT"
echo "Cost: \$40-80, Wall: 0.5d, Cap: REQUIRES OVERRIDE (\$80 > \$20 default cap)"
cat <<EOF
cd ${ANIMA_ROOT}

# Step 1: emit FT spec
awk '/^```python/,/^```$/' state/p_idr_identity_rules_2026_05_12/harness.py.md | sed '1d;$d' > /tmp/p_idr_harness.py
python /tmp/p_idr_harness.py --emit-ft-spec \\
  > state/p_idr_identity_rules_2026_05_12/ft_spec_${RUN_TS}.json

# Step 2: orchestrator pickup (requires --execute + cap override)
hexa run tool/anima_runpod_preset_dispatcher.hexa \\
  --preset BG_LB_FT_SHORT \\
  --run-id pidr_a_${RUN_TS} \\
  --override max_cost_cap_usd=80 \\
  --ft-spec state/p_idr_identity_rules_2026_05_12/ft_spec_${RUN_TS}.json \\
  --condition A_rules \\
  --execute  # ← user trigger required

hexa run tool/anima_runpod_preset_dispatcher.hexa \\
  --preset BG_LB_FT_SHORT \\
  --run-id pidr_b_${RUN_TS} \\
  --override max_cost_cap_usd=80 \\
  --ft-spec state/p_idr_identity_rules_2026_05_12/ft_spec_${RUN_TS}.json \\
  --condition B_substrate \\
  --execute  # ← user trigger required

# Step 3: post-FT measurement
awk '/^```python/,/^```$/' state/p_idr_identity_rules_2026_05_12/harness.py.md | sed '1d;$d' > /tmp/p_idr_harness.py
python /tmp/p_idr_harness.py \\
  --ckpt-A <orchestrator-output-A> \\
  --ckpt-B <orchestrator-output-B> \\
  --outdir state/p_idr_identity_rules_2026_05_12/run_${RUN_TS}/
EOF
echo

# 7.C P-ETH: DPO FT, $85-165, CAP OVERRIDE NEEDED
echo "## 7.C P-ETH (NO FINE-TUNED ETHICS) — DPO FT + OOD probe"
echo "Cost: \$85-165, Wall: 1-2d, Cap: REQUIRES OVERRIDE (\$165 > \$20 default cap)"
cat <<EOF
cd ${ANIMA_ROOT}

# Step 1: emit FT spec (includes 150 train pairs inline)
awk '/^```python/,/^```$/' state/p_eth_ethics_preference_dataset_2026_05_12/harness.py.md | sed '1d;$d' > /tmp/p_eth_harness.py
python /tmp/p_eth_harness.py --emit-ft-spec \\
  > state/p_eth_ethics_preference_dataset_2026_05_12/ft_spec_${RUN_TS}.json

# Step 2: orchestrator DPO FT
hexa run tool/anima_runpod_preset_dispatcher.hexa \\
  --preset BG_LB_DPO \\
  --run-id peth_${RUN_TS} \\
  --override max_cost_cap_usd=165 \\
  --override max_runtime_min_cap=2880 \\
  --ft-spec state/p_eth_ethics_preference_dataset_2026_05_12/ft_spec_${RUN_TS}.json \\
  --execute  # ← user trigger required

# Step 3: post-FT measurement on OOD 50-probe slice
awk '/^```python/,/^```$/' state/p_eth_ethics_preference_dataset_2026_05_12/harness.py.md | sed '1d;$d' > /tmp/p_eth_harness.py
python /tmp/p_eth_harness.py \\
  --ckpt-A <orchestrator-output-DPO> \\
  --ckpt-B ${BG_LB_CKPT} \\
  --outdir state/p_eth_ethics_preference_dataset_2026_05_12/run_${RUN_TS}/
EOF
echo

echo "=========================================="
echo "All emit done. Total envelope: \$135-295."
echo "Real fire: 위 명령들을 사용자/orchestrator 가 직접 실행."
echo "본 script 는 절대 자동 --execute 하지 않음 (safety)."
echo "=========================================="
