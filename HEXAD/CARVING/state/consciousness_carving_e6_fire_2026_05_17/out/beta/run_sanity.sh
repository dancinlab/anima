#!/bin/bash
set -uo pipefail
cd /workspace/anima
export PYTHONUNBUFFERED=1
python3 train_carving_4path.py --path beta --mode sanity --corpus corpus_carving.jsonl --out-dir out_sanity_beta --steps 60 2>&1 | tee sanity_beta.log
