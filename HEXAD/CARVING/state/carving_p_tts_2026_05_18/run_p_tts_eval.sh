#!/bin/bash
set -uo pipefail
cd /workspace/anima
export PYTHONUNBUFFERED=1
rm -f /workspace/anima/out_main/eval_result_p_off.json /workspace/anima/out_main/eval_result_p_on.json /workspace/anima/EVAL_DONE /workspace/anima/EVAL_FAIL
nohup bash -c '
  python3 eval_carving_p_tts.py --ckpt out_main/ckpt_carving_p_tts.pt \
    --output out_main/eval_result_p_off.json --device cuda --max-new 90
  R1=$?
  python3 eval_carving_p_tts.py --ckpt out_main/ckpt_carving_p_tts.pt \
    --output out_main/eval_result_p_on.json --device cuda --max-new 90 \
    --voice-refine
  R2=$?
  if [ $R1 -eq 0 ] && [ $R2 -eq 0 ] && [ -f /workspace/anima/out_main/eval_result_p_off.json ] && [ -f /workspace/anima/out_main/eval_result_p_on.json ]; then
    touch /workspace/anima/EVAL_DONE
  else
    echo "eval r1=$R1 r2=$R2" > /workspace/anima/EVAL_FAIL
  fi
' > /workspace/anima/eval.log 2>&1 &
echo $! > /workspace/anima/.eval_pid
echo "EVAL_DETACHED_LAUNCHED pid=$(cat /workspace/anima/.eval_pid)"
