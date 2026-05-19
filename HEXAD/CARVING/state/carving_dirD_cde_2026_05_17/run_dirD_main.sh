#!/bin/bash
set -uo pipefail
cd /workspace/anima
export PYTHONUNBUFFERED=1
rm -f /workspace/anima/out_main_cde/result.json /workspace/anima/TRAIN_DONE /workspace/anima/TRAIN_FAIL
nvidia-smi --query-gpu=utilization.gpu,memory.used --format=csv -l 30 > gpu_util_dirD.log 2>&1 &
echo $! > /workspace/anima/.smi_pid
nohup bash -c '
  python3 train_carving_cde.py --mode main --corpus corpus_carving_e7.jsonl     --out-dir out_main_cde --steps 2000     --d-model 768 --n-layer 12 --n-head 12 --n-kv-head 4     --bsz 32 --lr 3e-4 --vacuum-lambda 0.1     --cde-kappa 0.5 --cde-w-actor 0.7 --cde-w-critic 0.3
  RC=$?
  kill $(cat /workspace/anima/.smi_pid) 2>/dev/null || true
  if [ $RC -eq 0 ] && [ -f /workspace/anima/out_main_cde/result.json ]; then
    touch /workspace/anima/TRAIN_DONE
  else
    echo "train rc=$RC" > /workspace/anima/TRAIN_FAIL
  fi
' > /workspace/anima/train.log 2>&1 &
echo $! > /workspace/anima/.train_pid
echo "DETACHED_LAUNCHED pid=$(cat /workspace/anima/.train_pid)"
