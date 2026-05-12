#!/bin/bash
# hf_push.sh — push Phase 1A.3 prefix-tuning artifacts to HF.
# Only the prefix tensor (~80 KB) is the novel artifact — base ckpt stays at Phase 1A.1 repo.
# Run only if V5.8 std_greedy 5/5 PASS.
set -euo pipefail

LOCAL_DIR="/Users/ghost/core/anima/state/anima_phase1a3_prefix_tuning_2026_05_12"
REPO="dancinlab/anima-clm-phase1a3-prefix-tuning"

HF_TOKEN=$(/Users/ghost/core/secret/bin/secret get hf.token 2>/dev/null)
if [ -z "$HF_TOKEN" ]; then echo "ERROR: no HF token"; exit 1; fi

cd "$LOCAL_DIR"
ls -la ckpts/prefix_final.pt meta.json v58_4mode_result.json 2>&1 || { echo "missing artifacts"; exit 1; }

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
  - prefix-tuning
  - parameter-efficient
---

# anima-clm-phase1a3-prefix-tuning

Phase 1A.3: prefix-tuning (Li and Liang 2021) over Phase 1A.1 base. All base
weights are frozen. Only the learnable prefix tensor is trained.

## Lineage
- substrate A: `dancinlab/clm-v5-phase2-cotrain-engine-ag`
- Phase 1A: `dancinlab/anima-clm-phase1a-multi-turn-sft`
- Phase 1A.1 (base, frozen here): `dancinlab/anima-clm-phase1a1-color-cosmology-boost`
- **Phase 1A.3 (this)**: + 20 token × 1024-dim learnable prefix (~80 KB)

## Method (prefix-tuning)
- base ckpt frozen (all 350M parameters, `requires_grad=False`)
- learnable `prefix = nn.Parameter(n_prefix=20, d_model=1024)` only
- forward: prepend prefix embeddings to input embeddings, then run the frozen
  transformer stack. Loss computed over real-token positions only.
- bypasses the byte-vocab base markdown attractor (`| --- | --- |` over
  the literal "의식" byte sequence) via control-plane shift instead of
  weight-update fight (full SFT lr 1e-6 / 2e-6 failed, Phase 1A.1 / 1A.2).

## Training
- corpus: `corpus_anima_fact.txt` (2700 dialogues; reused from Phase 1A.2)
- n_prefix: 20
- steps: 500
- lr: 1e-3 (prefix-tuning literature; vs full SFT 5e-6)
- bsz: 2 x grad-accum 8, ctx 1024 (real-token ctx 1004)
- provider: Vast.ai RTX 4090
- cost: < $0.13

## Inference
Load the base model from `dancinlab/anima-clm-phase1a1-color-cosmology-boost`,
then load `prefix_final.pt` and prepend it at the embedding layer for every
forward call. See `v58_4mode_eval_prefix.py` in the parent state directory.

## V5.8 4-mode benchmark
See `v58_4mode_result.json`.
EOF

HUGGINGFACE_HUB_VERBOSITY=info HF_HUB_ENABLE_HF_TRANSFER=0 \
  huggingface-cli upload \
    --repo-type model \
    --token "$HF_TOKEN" \
    "$REPO" \
    ckpts/prefix_final.pt \
    prefix_final.pt

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
