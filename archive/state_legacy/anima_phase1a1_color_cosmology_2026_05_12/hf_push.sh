#!/bin/bash
# hf_push.sh — push Phase 1A.1 ckpt to HF as dancinlab/anima-clm-phase1a1-color-cosmology-boost
# Run on ubu1 (has huggingface-cli + access).
set -euo pipefail

LOCAL_DIR="/home/summer/mac_home/core/anima/state/anima_phase1a1_color_cosmology_2026_05_12"
REPO="dancinlab/anima-clm-phase1a1-color-cosmology-boost"

HF_TOKEN=$(ssh mac '/Users/ghost/core/secret/bin/secret get hf.token' 2>/dev/null)
if [ -z "$HF_TOKEN" ]; then echo "ERROR: no HF token"; exit 1; fi

cd "$LOCAL_DIR"
ls -la ckpts/ckpt_phase1a1_sft.pt meta.json v58_4mode_result.json 2>&1 || { echo "missing artifacts"; exit 1; }

# Stage README
cat > README.md <<'EOF'
---
license: apache-2.0
language:
  - ko
library_name: pytorch
tags:
  - anima
  - chat
  - clm
  - phase1a1
  - color-cosmology
---

# anima-clm-phase1a1-color-cosmology-boost

Phase 1A.1 continuation SFT on Phase 1A multi-turn (substrate A → Phase 1A → Phase 1A.1).
Color + cosmology recall boost via synthetic 5600-dialogue corpus upsampled 40x.

## Lineage
- substrate A: `dancinlab/clm-v5-phase2-cotrain-engine-ag`
- Phase 1A: `dancinlab/anima-clm-phase1a-multi-turn-sft`
- **Phase 1A.1 (this)**: + color/cosmology synthetic corpus boost

## Training
- arch: EngineAGModel 350M (24L, d=1024, GQA 4:1, byte-vocab32k+offset3)
- base ckpt: ckpt_phase1a_sft.pt (Phase 1A)
- corpus: multi_turn_v2.txt (Phase 1A multi_turn + 40x-upsampled synthetic color/cosmology)
- steps: 500
- lr: 2e-6 (gentle continuation)
- bsz: 2 × grad-accum 8, ctx 1024
- provider: Vast.ai A100 SXM4 40GB
- cost: < $0.20

## V5.8 4-mode benchmark
See `v58_4mode_result.json`.
EOF

source ~/.local/share/uv/python/cpython-3.12.* /dev/null 2>&1 || true

HUGGINGFACE_HUB_VERBOSITY=info HF_HUB_ENABLE_HF_TRANSFER=0 \
  huggingface-cli upload \
    --repo-type model \
    --token "$HF_TOKEN" \
    "$REPO" \
    ckpts/ckpt_phase1a1_sft.pt \
    ckpt_phase1a1_sft.pt
HUGGINGFACE_HUB_VERBOSITY=info \
  huggingface-cli upload \
    --repo-type model \
    --token "$HF_TOKEN" \
    "$REPO" \
    meta.json \
    meta.json
HUGGINGFACE_HUB_VERBOSITY=info \
  huggingface-cli upload \
    --repo-type model \
    --token "$HF_TOKEN" \
    "$REPO" \
    v58_4mode_result.json \
    v58_4mode_result.json
HUGGINGFACE_HUB_VERBOSITY=info \
  huggingface-cli upload \
    --repo-type model \
    --token "$HF_TOKEN" \
    "$REPO" \
    README.md \
    README.md

echo "OK: https://huggingface.co/$REPO"
