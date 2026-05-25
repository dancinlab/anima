#!/bin/bash
set -uo pipefail
cd /workspace/anima
export PYTHONUNBUFFERED=1
rm -f /workspace/anima/EVAL_DONE /workspace/anima/EVAL_FAIL
nohup bash -c '
  python3 eval_jepa_psi.py --ckpt out_main/ckpt_jepa_psi.pt \
    --output out_main/eval_result_jepa.json --device cuda --max-new 90
  RC1=$?
  python3 eval_jepa_psi.py --ckpt out_abl/ckpt_jepa_psi.pt \
    --output out_abl/eval_result_jepa.json --device cuda --max-new 90
  RC2=$?
  if [ $RC1 -eq 0 ] && [ -f /workspace/anima/out_main/eval_result_jepa.json ]; then
    touch /workspace/anima/EVAL_DONE
  else
    echo "eval rc1=$RC1 rc2=$RC2" > /workspace/anima/EVAL_FAIL
  fi
' > /workspace/anima/eval.log 2>&1 &
echo $! > /workspace/anima/.eval_pid
echo "EVAL_DETACHED_LAUNCHED pid=$(cat /workspace/anima/.eval_pid)"
