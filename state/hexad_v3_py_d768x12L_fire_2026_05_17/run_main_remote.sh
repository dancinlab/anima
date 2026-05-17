#!/bin/bash
set -uo pipefail
cd /workspace/anima
export PYTHONUNBUFFERED=1
nvidia-smi --query-gpu=utilization.gpu,memory.used --format=csv -l 30 > gpu_util.log 2>&1 &
SMI=$!
python3 train_d768x12l.py --mode main --corpus corpus_v3.jsonl --out-dir out_main --steps 2500 2>&1 | tee fire.log
kill $SMI 2>/dev/null || true
echo DONE_MARKER rc=$?
