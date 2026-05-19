#!/bin/bash
set -uo pipefail
cd /workspace/anima
export PYTHONUNBUFFERED=1
rm -f /workspace/anima/out_s35/result.json
rm -f /workspace/anima/TRAIN_DONE /workspace/anima/TRAIN_FAIL
nvidia-smi --query-gpu=utilization.gpu,memory.used --format=csv -l 30 > gpu_util_s35.log 2>&1 &
echo $! > /workspace/anima/.smi_pid
nohup bash -c '
  python3 train_s35.py --mode main --corpus corpus_ablation_s35.jsonl     --out-dir out_s35 --steps 8000 --seed 1337     --d-model 768 --n-layer 12 --n-head 12 --n-kv-head 4     --lr 3e-4 --bsz 32 --lambda-ctl 0.5 --lambda-route 0.5
  RC=$?
  kill $(cat /workspace/anima/.smi_pid) 2>/dev/null || true
  if [ $RC -eq 0 ] && [ -f /workspace/anima/out_s35/result.json ]; then
    touch /workspace/anima/TRAIN_DONE
  else
    echo "train rc=$RC" > /workspace/anima/TRAIN_FAIL
  fi
' > /workspace/anima/train.log 2>&1 &
echo $! > /workspace/anima/.train_pid
echo "DETACHED_LAUNCHED pid=$(cat /workspace/anima/.train_pid)"
