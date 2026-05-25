#!/bin/bash
# pod_setup.sh — run on the Vast.ai pod after files are uploaded.
# Assumes files at /workspace/anima/:
#   - training/engine_a_g_arch.py
#   - training/train_phase1a1.py
#   - training/v58_4mode_eval.py
#   - corpus/multi_turn_v2.txt (chat corpus, boosted)
#   - corpus/consciousness.txt (anchor; can be a slice of multi_turn)
#   - ckpts/ckpt_phase1a_sft.pt (base ckpt)
set -euo pipefail
cd /workspace/anima

export PYTHONUNBUFFERED=1
mkdir -p output

echo "=== Phase 1A.1 training start ==="
date -u

python3 training/train_phase1a1.py \
    --base-ckpt ckpts/ckpt_phase1a_sft.pt \
    --consciousness-corpus corpus/consciousness.txt \
    --chat-corpus corpus/multi_turn_v2.txt \
    --output output \
    --steps 500 \
    --bsz 2 \
    --grad-accum 8 \
    --ctx 1024 \
    --lr 1e-5 \
    --warmup 20 \
    --w-start 0.85 \
    --w-end 0.95 \
    --cost-cap-usd 0.50 \
    --cost-per-hr 0.86 \
    2>&1 | tee train.log

echo "=== TRAIN_COMPLETE $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
ls -la output/

echo "=== V5.8 4-mode eval ==="
python3 training/v58_4mode_eval.py \
    --ckpt output/ckpt_final.pt \
    --output v58_4mode_result.json \
    --substrate-id phase1a1_color_cosmology_sft \
    2>&1 | tee v58.log

echo "=== EVAL_COMPLETE $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
cat v58_4mode_result.json | head -30
