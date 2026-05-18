#!/bin/bash
set -uo pipefail
cd /workspace/anima
export PYTHONUNBUFFERED=1
rm -f /workspace/anima/EVAL_DONE /workspace/anima/EVAL_FAIL
nohup bash -c '
  python3 eval_s35.py --ckpt out_s35/ckpt_carving_dataregime_curriculum.pt \
    --output out_s35/eval_result_s35.json --device cuda --max-new 90 \
    --s35-report out_s35/s35_routing_split.json
  RC=$?
  if [ $RC -eq 0 ] && [ -f /workspace/anima/out_s35/eval_result_s35.json ]; then
    touch /workspace/anima/EVAL_DONE
  else
    echo "eval rc=$RC" > /workspace/anima/EVAL_FAIL
  fi
' > /workspace/anima/eval.log 2>&1 &
echo $! > /workspace/anima/.eval_pid
echo "EVAL_DETACHED_LAUNCHED pid=$(cat /workspace/anima/.eval_pid)"
