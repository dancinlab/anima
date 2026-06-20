#!/usr/bin/env bash
set -uo pipefail
export G6_PROBES=/workspace/g6/probes
export G6_CKPT=/workspace/g6/ckpt/h1129c_chat.pt
export G6_CORPUS=/workspace/g6/probes/corpus.txt
export G6_OUT=/workspace/g6/out
cd /workspace/g6/probes
[ -f "$G6_CORPUS" ] || echo "placeholder corpus for novelty grep" > "$G6_CORPUS"
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader || true
echo "==== H_1456 idea-metacognition (base+trained+shuffle-ctrl, 3 seeds) ===="
python3 h1456_idea_metacognition.py --device cuda:0 --steps 400 --lines 4000 \
  2>&1 | tee /workspace/g6/out/h1456.log
echo "==== H_1456 DONE ===="
