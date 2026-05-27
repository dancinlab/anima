#!/bin/bash
set -uo pipefail
cd /workspace/anima
export PYTHONUNBUFFERED=1
rm -f /workspace/anima/out_main/result.json /workspace/anima/out_abl/result.json
rm -f /workspace/anima/TRAIN_DONE /workspace/anima/TRAIN_FAIL
nvidia-smi --query-gpu=utilization.gpu,memory.used --format=csv -l 30 > gpu_util_jepa.log 2>&1 &
echo $! > /workspace/anima/.smi_pid
nohup bash -c '
  python3 train_jepa_psi.py --corpus corpus_jepa_psi.jsonl     --out-dir out_main --steps 6000 --max-records 120000     --gamma-text 0.3
  RC1=$?
  python3 train_jepa_psi.py --corpus corpus_jepa_psi.jsonl     --out-dir out_abl --steps 6000 --max-records 120000     --gamma-text 0.0
  RC2=$?
  kill $(cat /workspace/anima/.smi_pid) 2>/dev/null || true
  if [ $RC1 -eq 0 ] && [ -f /workspace/anima/out_main/result.json ]; then
    touch /workspace/anima/TRAIN_DONE
  else
    echo "train rc1=$RC1 rc2=$RC2" > /workspace/anima/TRAIN_FAIL
  fi
' > /workspace/anima/train.log 2>&1 &
echo $! > /workspace/anima/.train_pid
echo "DETACHED_LAUNCHED pid=$(cat /workspace/anima/.train_pid)"
