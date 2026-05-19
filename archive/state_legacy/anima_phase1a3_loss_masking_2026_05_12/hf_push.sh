#!/bin/bash
# hf_push.sh — push Phase 1A.3 ckpt to HF (conditional on 5/5 PASS)
# Repo: dancinlab/anima-clm-phase1a3-loss-masking
set -euo pipefail

LOCAL_DIR="/home/summer/mac_home/core/anima/state/anima_phase1a3_loss_masking_2026_05_12"
REPO="dancinlab/anima-clm-phase1a3-loss-masking"

HF_TOKEN=$(ssh mac '/Users/ghost/core/secret/bin/secret get hf.token' 2>/dev/null)
if [ -z "$HF_TOKEN" ]; then echo "ERROR: no HF token"; exit 1; fi

cd "$LOCAL_DIR"
ls -la ckpts/ckpt_phase1a3_sft.pt meta.json v58_4mode_result.json 2>&1 || { echo "missing artifacts"; exit 1; }

# Gate: require std_greedy 5/5 before pushing.
N_PASS=$(python3 -c "
import json
d = json.load(open('v58_4mode_result.json'))
print(d['summary']['standard_greedy']['n_pass'])
")
if [ "$N_PASS" != "5" ]; then
    echo "GATE FAIL: std_greedy=$N_PASS/5 (expected 5/5) — HF push aborted"
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
  - loss-masking
---

# anima-clm-phase1a3-loss-masking

Phase 1A.3 continuation SFT on Phase 1A.1 with **response-only loss masking**:
gradient is computed only on `도우미:` response bytes, not on `사용자:` prompt
bytes. Lesson R-1A.2 lane B.

## Lineage
- substrate A: `dancinlab/clm-v5-phase2-cotrain-engine-ag`
- Phase 1A: `dancinlab/anima-clm-phase1a-multi-turn-sft`
- Phase 1A.1: `dancinlab/anima-clm-phase1a1-color-cosmology-boost`
- **Phase 1A.3 (this)**: + loss-mask response-only

## Mission
Phase 1A.1 V5.8 std_greedy: 4/5 PASS (anima_fact FAIL, markdown drift).
Phase 1A.2 (lr 1e-6, no mask): 4/5 — failed to break attractor.
Phase 1A.3 targets 5/5 via sharper response-only gradient.

## Training
- arch: EngineAGModel 350M (24L, d=1024, GQA 4:1, byte-vocab32k+offset3)
- base ckpt: ckpt_phase1a1_sft.pt
- corpus: corpus_anima_fact.txt (2700 dialogues, reused from Phase 1A.2)
- steps: 200
- lr: 2e-6 (matches Phase 1A.1; isolates masking effect)
- loss: cross_entropy with response-token mask (도우미: body bytes only)
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
