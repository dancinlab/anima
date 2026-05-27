#!/bin/bash
set -uo pipefail
cd /workspace/anima
export PYTHONUNBUFFERED=1
nvidia-smi --query-gpu=utilization.gpu,memory.used --format=csv -l 30 > gpu_util_alpha.log 2>&1 &
SMI=$!
python3 train_carving_4path.py --path alpha --mode main --corpus corpus_carving.jsonl --out-dir out_main_alpha --steps 2000 --d-model 512 --n-layer 8 --n-head 8 --n-kv-head 4 2>&1 | tee fire_alpha.log
kill $SMI 2>/dev/null || true
echo DONE_MARKER rc=$?
