#!/bin/bash
# hf_push.sh — push Phase 1A.4 ckpt to HF as dancinlab/anima-clm-phase1a4-lr5e6-strict-pass
# (only if V5.8 std_greedy 5/5 PASS)
set -euo pipefail

LOCAL_DIR="/Users/ghost/core/anima/state/anima_phase1a4_lr5e6_2026_05_12"
REPO="dancinlab/anima-clm-phase1a4-lr5e6-strict-pass"

HF_TOKEN=$(/Users/ghost/core/secret/bin/secret get hf.token 2>/dev/null)
if [ -z "$HF_TOKEN" ]; then echo "ERROR: no HF token"; exit 1; fi

cd "$LOCAL_DIR"
ls -la ckpts/ckpt_phase1a4_lr5e6_sft.pt meta.json v58_4mode_result.json 2>&1 || { echo "missing artifacts"; exit 1; }

# Gate: only push if std_greedy 5/5
N_PASS=$(python3 -c "import json; d=json.load(open('v58_4mode_result.json')); print(d['summary']['standard_greedy']['n_pass'])")
if [ "$N_PASS" != "5" ]; then
    echo "ABORT: std_greedy n_pass=$N_PASS (need 5 for HF push)"
    exit 1
fi
echo "OK: std_greedy 5/5 confirmed, proceeding with HF push to $REPO"

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
  - phase1a4
  - strict-pass
  - lr5e6
---

# anima-clm-phase1a4-lr5e6-strict-pass

Phase 1A.4 continuation SFT on Phase 1A.1 — first ckpt to achieve V5.8 standard_greedy 5/5 PASS in the anima CLM saga (Lesson R-1A.2 first path).

## Lineage
- substrate A: `dancinlab/clm-v5-phase2-cotrain-engine-ag`
- Phase 1A: `dancinlab/anima-clm-phase1a-multi-turn-sft` (std_greedy 3/5)
- Phase 1A.1: `dancinlab/anima-clm-phase1a1-color-cosmology-boost` (std_greedy 4/5)
- Phase 1A.2: `dancinlab/anima-clm-phase1a2-anima-fact-recover` (std_greedy 4/5, lr 1e-6 too small)
- **Phase 1A.4 (this)**: lr 5e-6 × 200 SFT → std_greedy 5/5 PASS

## Mission
PSCC §25b Lesson R-1A.2 prescribed lr ≥ 5e-6 OR steps ≥ 1000 OR loss masking after Phase 1A.2 lr=1e-6 failed to break the anima_fact markdown attractor. Phase 1A.4 = lr 5e-6 path.

## Training
- arch: EngineAGModel 350M (24L, d=1024, GQA 4:1, byte-vocab32k+offset3)
- base ckpt: ckpt_phase1a1_sft.pt (Phase 1A.1)
- corpus: corpus_anima_fact.txt (2700 dialogues: 1500 anima 2-turn + 1000 V5.8-exact-anchor + 200 anti-forgetting refresh)
- steps: 200
- lr: 5e-6 (5x Phase 1A.2's 1e-6; Lesson R-1A.2 prescribed floor)
- bsz: 2 x grad-accum 8, ctx 1024
- provider: Vast.ai RTX 4090
- cost: ~$0.02

## V5.8 4-mode benchmark
See `v58_4mode_result.json`.
EOF

HUGGINGFACE_HUB_VERBOSITY=info HF_HUB_ENABLE_HF_TRANSFER=0 \
  huggingface-cli upload \
    --repo-type model \
    --token "$HF_TOKEN" \
    --private \
    "$REPO" \
    ckpts/ckpt_phase1a4_lr5e6_sft.pt \
    ckpt_phase1a4_lr5e6_sft.pt
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
