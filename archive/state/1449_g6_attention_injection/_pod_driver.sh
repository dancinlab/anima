#!/usr/bin/env bash
set -uo pipefail
export G6_PROBES=/workspace/g6/probes G6_CKPT=/workspace/g6/ckpt/h1129c_chat.pt G6_OUT=/workspace/g6/out
cd /workspace/g6/probes
for SEED in 7 4302 4303; do
  echo "==== H_1449 SEED $SEED ===="
  python3 h1449_attention_injection.py --device cuda:0 --steps 600 --lines 6000 --seed $SEED \
    2>&1 | tee /workspace/g6/out/h1449_seed${SEED}.log
done
echo "==== ALL SEEDS DONE ===="
