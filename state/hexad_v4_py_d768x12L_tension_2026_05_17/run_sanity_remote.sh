#!/bin/bash
set -uo pipefail
cd /workspace/anima
export PYTHONUNBUFFERED=1
python3 train_d768x12l_tension.py --mode sanity --corpus corpus_v3.jsonl --out-dir out_sanity --steps 200 2>&1 | tee sanity.log
