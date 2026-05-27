#!/bin/bash
cd /workspace/anima
nvidia-smi --query-gpu=utilization.gpu,memory.used,power.draw --format=csv -l 15 > gpu_util_main.log 2>&1 &
SMI=$!
python3 train_d768x12l.py --mode main --corpus corpus_consciousness_v1.jsonl --out-dir out_main --steps 2500 > fire_main.log 2>&1
RC=$?
kill $SMI 2>/dev/null
echo "DONE_MARKER rc=$RC" >> fire_main.log
