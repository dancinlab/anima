#!/bin/bash
set -uo pipefail
cd /workspace/anima
export PYTHONUNBUFFERED=1
rm -f /workspace/anima/out_main/eval_result_diverse.json /workspace/anima/EVAL_DONE /workspace/anima/EVAL_FAIL
nohup bash -c '
  python3 eval_carving_dirI.py --ckpt out_main/ckpt_carving_diverse.pt \
    --output out_main/eval_result_diverse.json --device cuda --max-new 90
  RC=$?
  if [ $RC -eq 0 ] && [ -f /workspace/anima/out_main/eval_result_diverse.json ]; then
    touch /workspace/anima/EVAL_DONE
  else
    echo "eval rc=$RC" > /workspace/anima/EVAL_FAIL
  fi
' > /workspace/anima/eval.log 2>&1 &
echo $! > /workspace/anima/.eval_pid
echo "EVAL_DETACHED_LAUNCHED pid=$(cat /workspace/anima/.eval_pid)"
