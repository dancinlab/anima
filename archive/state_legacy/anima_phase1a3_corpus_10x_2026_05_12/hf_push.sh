#!/bin/bash
# hf_push.sh — push Phase 1A.3 ckpt to HF as dancinlab/anima-clm-phase1a3-corpus-10x
#
# Only run when V5.8 std_greedy 5/5 PASS.
set -euo pipefail

LOCAL_DIR="/Users/ghost/core/anima/state/anima_phase1a3_corpus_10x_2026_05_12"
REPO="dancinlab/anima-clm-phase1a3-corpus-10x"

HF_TOKEN=$(/Users/ghost/core/secret/bin/secret get hf.token 2>/dev/null)
if [ -z "$HF_TOKEN" ]; then echo "ERROR: no HF token"; exit 1; fi

cd "$LOCAL_DIR"
ls -la ckpts/ckpt_phase1a3_sft.pt meta.json v58_4mode_result.json 2>&1 || { echo "missing artifacts"; exit 1; }

# Gate: only push if std_greedy 5/5
N_PASS=$(python3 -c "
import json
with open('v58_4mode_result.json') as f:
    d = json.load(f)
print(d['summary']['standard_greedy']['n_pass'])
")
echo "std_greedy n_pass = $N_PASS"
if [ "$N_PASS" -lt 5 ]; then
    echo "ABORT: std_greedy < 5/5, HF push gated"
    exit 2
fi

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
  - phase1a3
  - corpus-10x
---

# anima-clm-phase1a3-corpus-10x

Phase 1A.3 continuation SFT on Phase 1A.1: anima_fact recall via corpus 10x scale (data-scale isolation).

## Lineage
- substrate A: `dancinlab/clm-v5-phase2-cotrain-engine-ag`
- Phase 1A: `dancinlab/anima-clm-phase1a-multi-turn-sft`
- Phase 1A.1: `dancinlab/anima-clm-phase1a1-color-cosmology-boost`
- **Phase 1A.3 (this)**: + anima_fact corpus 10x (27000 dialogues)

## Mission
Phase 1A.1 V5.8 std_greedy: 4/5 PASS (anima_fact FAIL: markdown drift).
Phase 1A.2 (2700 dialogues × lr 1e-6): FAILED to break markdown attractor.
Phase 1A.3 strategy: same lr/steps, 10x corpus dialogues → brute-force intensity.

## Training
- arch: EngineAGModel 350M (24L, d=1024, GQA 4:1, byte-vocab32k+offset3)
- base ckpt: ckpt_phase1a1_sft.pt (Phase 1A.1)
- corpus: corpus_anima_fact_10x.txt (27000 dialogues)
  - 16000 anima 2-turn (80 base × 200 templates)
  - 8000 V5.8-exact-anchor
  - 2000 anti-forgetting (color/profession/day/cosmology)
  - 1000 natural-prose chat tail (markdown-free)
- steps: 200
- lr: 1e-6 (same as Phase 1A.2; data scale isolation)
- bsz: 2 × grad-accum 8, ctx 1024
- provider: Vast.ai RTX 4090

## V5.8 4-mode benchmark
See `v58_4mode_result.json`.
EOF

source ~/.local/share/uv/python/cpython-3.12.* /dev/null 2>&1 || true

HUGGINGFACE_HUB_VERBOSITY=info HF_HUB_ENABLE_HF_TRANSFER=0 \
  huggingface-cli upload \
    --repo-type model \
    --token "$HF_TOKEN" \
    "$REPO" \
    ckpts/ckpt_phase1a3_sft.pt \
    ckpt_phase1a3_sft.pt
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
