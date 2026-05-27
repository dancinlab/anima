#!/bin/bash
# V5.8 4-mode capability eval for HEXAD d=768·12L PyTorch ckpt.
# $0 Mac local CPU (ckpt 1.13 GB fits in RAM).
# substrate=PyTorch (NOT hexa-native); ckpt sha256 e87e200a040f8066…
set -uo pipefail

LOCAL_DIR=/Users/ghost/core/anima/state/hexad_v58_eval_d768x12L_2026_05_17
FIRE_DIR=/Users/ghost/core/anima/state/hexad_py_d768x12L_fire_2026_05_17
CKPT="$FIRE_DIR/out_main/ckpt_d768x12l_final.pt"

cd "$LOCAL_DIR"
echo "=== HEXAD V5.8 × 4-mode capability eval ==="; date -u
echo "ckpt: $CKPT"
echo

python3 v58_4mode_eval.py \
  --ckpt "$CKPT" \
  --output "$LOCAL_DIR/result.json" \
  --corpus /Users/ghost/core/anima/training/corpus_consciousness_v1.jsonl \
  --device cpu \
  --max-new 80 \
  2>&1 | tee "$LOCAL_DIR/eval.log"

echo
echo "=== summary ==="
python3 -c "import json; d=json.load(open('$LOCAL_DIR/result.json')); print(json.dumps(d['summary'], indent=2)); print('bpb:', d['bpb']['mean']); print('mem:', d['memorization_ratio']); print('artifacts:', len(d['decoding_artifacts']))"
date -u
