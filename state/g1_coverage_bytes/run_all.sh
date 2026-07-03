#!/bin/bash
set -e
cd "$(dirname "$0")"
python3 gen_corpus.py --outdir .
for arm in high low shuffle; do
  OMP_NUM_THREADS=4 python3 -u bt.py --arm $arm --arch attn --steps 3000 > log_attn_$arm.txt 2>&1
  echo "attn $arm done"
done
for arm in high low shuffle; do
  OMP_NUM_THREADS=4 python3 -u bt.py --arm $arm --arch convd --steps 3000 > log_convd_$arm.txt 2>&1
  echo "convd $arm done"
done
echo "=== ALL DONE ==="
