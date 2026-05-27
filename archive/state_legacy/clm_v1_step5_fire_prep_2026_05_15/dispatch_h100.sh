#!/usr/bin/env bash
# .clm v1 fire dispatch — Vast.ai/RunPod H100 SXM × 1 × ~10-20 hr
# user verbatim approval required: "OK CLM V1 FROM-SCRATCH FIRE COST $10-30"
#
# spec frozen sha256: 972e9987cd09118533161d5625ebde67a10aa5ec7f2e498bdbfca008a0f36ee5
# W1 anchor: state/clm_v1_step4_spec_frozen_2026_05_15/spec_frozen.json
set -euo pipefail

if [ "${1:-}" != "OK CLM V1 FROM-SCRATCH FIRE COST \$10-30" ]; then
    echo "[ABORT] fire keyword 미확인. user verbatim required: 'OK CLM V1 FROM-SCRATCH FIRE COST \$10-30'"
    exit 1
fi
echo "[OK] fire keyword verified"

# Verify spec frozen sha256 unchanged
EXPECTED_SHA="972e9987cd09118533161d5625ebde67a10aa5ec7f2e498bdbfca008a0f36ee5"
ACTUAL_SHA=$(sha256sum state/clm_v1_step4_spec_frozen_2026_05_15/spec_frozen.json | awk '{print $1}')
if [ "$ACTUAL_SHA" != "$EXPECTED_SHA" ]; then
    echo "[ABORT] spec_frozen.json sha256 mismatch (W1 violation)"
    echo "  expected: $EXPECTED_SHA"
    echo "  actual:   $ACTUAL_SHA"
    exit 1
fi
echo "[OK] W1 spec sha256 verified"

# Verify entry conditions
test -f state/anima_phase1a4_lr5e6_2026_05_12/ckpts/ckpt_phase1a4_lr5e6_sft.pt || (echo "[ABORT] Phase 1A.4 anchor ckpt missing"; exit 1)
test -f state/anima_v5mitosis_cotrain_2026_05_12/ckpts/ckpt_v5mitosis_cotrain_cotrain.pt || (echo "[ABORT] v5-mitosis cond.5 anchor missing"; exit 1)
echo "[OK] anchor ckpts present (verification only, weights X)"

# Cost monitor: hard stop $50
HARD_STOP_USD=50
COST_LOG=/tmp/clm_v1_cost_monitor.log
echo "[INFO] hard_stop=\$$HARD_STOP_USD, cost_log=$COST_LOG"

# RunPod or Vast.ai dispatch (template)
PROVIDER="${PROVIDER:-vast}"  # 'vast' or 'runpod'
INSTANCE_TYPE="${INSTANCE_TYPE:-H100_SXM_80GB}"
WALL_HOURS="${WALL_HOURS:-20}"
echo "[INFO] provider=$PROVIDER, instance=$INSTANCE_TYPE, wall=${WALL_HOURS}h"

# Pre-upload artifacts
echo "[STEP] artifact prep: anima_persona_tier_a_v4 + Phase 1A.6 + tape corpus + training script"
# (artifact bundle script — to be filled per provider)

# Fire command template (filled with actual instance ID at runtime)
echo "[STEP] dispatch to $PROVIDER ..."
echo "  command: $PROVIDER instance create --type $INSTANCE_TYPE --image pytorch:2.0-cuda12 --bid_price 4.0"
echo "  (dry-run — actual fire requires PROVIDER credentials + bid)"

# Training loop (on instance):
#   cd /workspace/anima
#   pip install -r requirements.txt
#   python3 training/clm_v1_from_scratch.py \
#       --d_model 768 --n_layers 12 --n_cells 64 --n_heads 8 --kv_heads 4 \
#       --corpus state/corpus_bundle.tar.gz --seed 42 \
#       --total_steps 5000 --batch_per_device 8 --accum 2 --seq_len 1024 \
#       --lr_warmup 5e-4 --lr_target 5e-5 --bf16 \
#       --mitosis_hook_per_token --output_dir /workspace/ckpts \
#       --hard_stop_usd $HARD_STOP_USD --cost_log $COST_LOG \
#       2>&1 | tee /tmp/clm_v1_fire.log

# Post-fire pull
#   rsync /workspace/ckpts/ckpt_clm_v1_final.{pt,safetensors} → state/clm_v1_2026_05_*/ckpts/
#   gh-cli upload to dancinlab/anima-clm (HF revisions, private)

echo "[DRY-RUN COMPLETE] for actual fire, set PROVIDER + credentials"
