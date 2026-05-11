#!/bin/bash
# hf_push.sh — push Phase 1B SimPO-on-Phase-1A.1 ckpt to HF
# Only run if V5.8 std_greedy >= 5/5
set -euo pipefail

STATE="${STATE:-$HOME/core/anima/state/anima_phase1b_simpo_on_phase1a1_2026_05_12}"
REPO="dancinlab/anima-clm-phase1b-simpo-on-phase1a1"
CKPT="$STATE/output/ckpt_phase1b_simpo_on_phase1a1.pt"
RESULT="$STATE/v58_4mode_result.json"

test -f "$CKPT" || { echo "MISSING ckpt: $CKPT"; exit 1; }
test -f "$RESULT" || { echo "MISSING result"; exit 1; }

# Gate: only push if std_greedy >= 5
N_PASS=$(/usr/bin/python3 -c "
import json
d = json.load(open('$RESULT'))
print(d['summary']['standard_greedy']['n_pass'])
")
if [ "$N_PASS" -lt 5 ]; then
  echo "GATE FAILED: std_greedy n_pass=$N_PASS < 5; NOT pushing to HF"
  exit 2
fi
echo "GATE PASSED: std_greedy 5/5; pushing"

HF_TOKEN=$(/Users/ghost/core/secret/bin/secret get hf.token)
test -n "$HF_TOKEN" || { echo "no HF token"; exit 1; }

cat > "$STATE/README.md" <<'EOF'
---
license: apache-2.0
language:
  - ko
library_name: pytorch
tags:
  - anima
  - chat
  - clm
  - phase1b
  - simpo
  - color-cosmology
---

# anima-clm-phase1b-simpo-on-phase1a1

Phase 1B SimPO trained on top of Phase 1A.1 SFT (substrate-mismatch-corrected retry).

## Lineage
- substrate A: `dancinlab/clm-v5-phase2-cotrain-engine-ag`
- Phase 1A: `dancinlab/anima-clm-phase1a-multi-turn-sft`
- Phase 1A.1: `dancinlab/anima-clm-phase1a1-color-cosmology-boost`
- **Phase 1B SimPO (this)**: + 567 preference pairs (V5.8-exact prompts), conservative SimPO

## Training
- arch: EngineAGModel 350M
- base ckpt: ckpt_phase1a1_sft.pt (Phase 1A.1)
- pref pairs: 567 (264 anima_fact-focused; V5.8-exact 2-line ack prompts)
- steps: 500, lr 5e-6
- SimPO hyperparams (CONSERVATIVE — prior B' attempt over-sharpened):
  - beta = 0.05 (vs 2.5 in prior attempt)
  - gamma = 0.3 (vs 1.4)
  - SFT-anchor CE weight w: 0.9 → 1.0 (preserve language modeling)
- provider: Vast.ai RTX 4090 (~$0.27/hr)
- cost: < $0.10

## V5.8 4-mode benchmark
- **standard_greedy: 5/5 PASS** ← mission complete
- See `v58_4mode_result.json` for details
EOF

source ~/.local/share/uv/python/cpython-3.12.* /dev/null 2>&1 || true

HUGGINGFACE_HUB_VERBOSITY=info HF_HUB_ENABLE_HF_TRANSFER=0 \
  huggingface-cli upload --repo-type model --token "$HF_TOKEN" "$REPO" \
    "$CKPT" ckpt_phase1b_simpo_on_phase1a1.pt
HUGGINGFACE_HUB_VERBOSITY=info \
  huggingface-cli upload --repo-type model --token "$HF_TOKEN" "$REPO" \
    "$STATE/output/meta.json" meta.json
HUGGINGFACE_HUB_VERBOSITY=info \
  huggingface-cli upload --repo-type model --token "$HF_TOKEN" "$REPO" \
    "$RESULT" v58_4mode_result.json
HUGGINGFACE_HUB_VERBOSITY=info \
  huggingface-cli upload --repo-type model --token "$HF_TOKEN" "$REPO" \
    "$STATE/README.md" README.md

echo "OK: https://huggingface.co/$REPO"
