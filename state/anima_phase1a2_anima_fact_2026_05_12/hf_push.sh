#!/bin/bash
# hf_push.sh — push Phase 1A.2 ckpt to HF as dancinlab/anima-clm-phase1a2-anima-fact-recover
set -euo pipefail

LOCAL_DIR="/home/summer/mac_home/core/anima/state/anima_phase1a2_anima_fact_2026_05_12"
REPO="dancinlab/anima-clm-phase1a2-anima-fact-recover"

HF_TOKEN=$(ssh mac '/Users/ghost/core/secret/bin/secret get hf.token' 2>/dev/null)
if [ -z "$HF_TOKEN" ]; then echo "ERROR: no HF token"; exit 1; fi

cd "$LOCAL_DIR"
ls -la ckpts/ckpt_phase1a2_sft.pt meta.json v58_4mode_result.json 2>&1 || { echo "missing artifacts"; exit 1; }

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
  - phase1a2
  - anima-fact-recover
---

# anima-clm-phase1a2-anima-fact-recover

Phase 1A.2 continuation SFT on Phase 1A.1 (substrate A → Phase 1A → Phase 1A.1 → Phase 1A.2).
anima_fact recall recovery from Phase 1A.1's 4/5 std_greedy regression (markdown drift).

## Lineage
- substrate A: `dancinlab/clm-v5-phase2-cotrain-engine-ag`
- Phase 1A: `dancinlab/anima-clm-phase1a-multi-turn-sft`
- Phase 1A.1: `dancinlab/anima-clm-phase1a1-color-cosmology-boost`
- **Phase 1A.2 (this)**: + anima self-statement corpus boost

## Mission
Phase 1A.1 V5.8 std_greedy: 4/5 PASS (color/profession/day/cosmology PASS, anima_fact FAIL with markdown drift).
Phase 1A.2 targets full 5/5 PASS via anima self-statement augment corpus.

## Training
- arch: EngineAGModel 350M (24L, d=1024, GQA 4:1, byte-vocab32k+offset3)
- base ckpt: ckpt_phase1a1_sft.pt (Phase 1A.1)
- corpus: corpus_anima_fact.txt (2700 dialogues: 1500 anima 2-turn + 1000 V5.8-exact + 200 anti-forgetting color/cosmo refresh)
- steps: 200
- lr: 1e-6 (super-conservative; Phase 1A.1 4/5 보존 목적)
- bsz: 2 × grad-accum 8, ctx 1024
- provider: Vast.ai RTX 4090
- cost: < $0.15

## V5.8 4-mode benchmark
See `v58_4mode_result.json`.
EOF

source ~/.local/share/uv/python/cpython-3.12.* /dev/null 2>&1 || true

HUGGINGFACE_HUB_VERBOSITY=info HF_HUB_ENABLE_HF_TRANSFER=0 \
  huggingface-cli upload \
    --repo-type model \
    --token "$HF_TOKEN" \
    "$REPO" \
    ckpts/ckpt_phase1a2_sft.pt \
    ckpt_phase1a2_sft.pt
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
