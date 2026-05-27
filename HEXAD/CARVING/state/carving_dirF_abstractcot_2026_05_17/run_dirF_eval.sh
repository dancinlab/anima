#!/bin/bash
set -uo pipefail
cd /workspace/anima
export PYTHONUNBUFFERED=1
rm -f /workspace/anima/out_main_dirF/eval_result_dirF.json /workspace/anima/EVAL_DONE /workspace/anima/EVAL_FAIL
nohup bash -c '
  python3 eval_carving_dirF.py --ckpt out_main_dirF/ckpt_carving_dirF.pt \
    --output out_main_dirF/eval_result_dirF.json --device cuda --max-new 90
  RC=$?
  if [ $RC -eq 0 ] && [ -f /workspace/anima/out_main_dirF/eval_result_dirF.json ]; then
    touch /workspace/anima/EVAL_DONE
  else
    echo "eval rc=$RC" > /workspace/anima/EVAL_FAIL
  fi
' > /workspace/anima/eval.log 2>&1 &
echo $! > /workspace/anima/.eval_pid
echo "EVAL_DETACHED_LAUNCHED pid=$(cat /workspace/anima/.eval_pid)"
