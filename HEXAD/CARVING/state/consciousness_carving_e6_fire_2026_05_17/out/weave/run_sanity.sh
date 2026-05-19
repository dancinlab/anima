#!/bin/bash
set -uo pipefail
cd /workspace/anima
export PYTHONUNBUFFERED=1
python3 train_carving_4path.py --path weave --mode sanity --corpus corpus_carving.jsonl --out-dir out_sanity_weave --steps 60 2>&1 | tee sanity_weave.log
