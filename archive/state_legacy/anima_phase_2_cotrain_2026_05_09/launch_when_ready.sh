#!/bin/bash
# Phase 2 cotrain — launch when uploads complete on pod.
# This script polls pod for ckpt completeness then fires training via nohup.
SSH_HOST=205.196.17.170
SSH_PORT=18488
SSH_KEY=/Users/ghost/.runpod/ssh/RunPod-Key-Go
EXPECTED_CKPT_SZ=597614720

while true; do
  CKPT_SZ=$(ssh -i "$SSH_KEY" -p "$SSH_PORT" -o StrictHostKeyChecking=no -o ConnectTimeout=10 root@$SSH_HOST \
    'stat -c %s /workspace/anima_phase2/bg_lb_step_8000_final.pt 2>/dev/null' 2>/dev/null)
  CKPT_SZ=${CKPT_SZ:-0}
  echo "[wait $(date -u +%FT%TZ)] ckpt=$CKPT_SZ / $EXPECTED_CKPT_SZ"
  if [ "$CKPT_SZ" -ge "$EXPECTED_CKPT_SZ" ]; then
    echo "CKPT_UPLOAD_COMPLETE"
    break
  fi
  sleep 60
done

# Sanity check ckpt + corpora
ssh -i "$SSH_KEY" -p "$SSH_PORT" -o StrictHostKeyChecking=no root@$SSH_HOST \
  'ls -la /workspace/anima_phase2/{bg_lb_step_8000_final.pt,corpus_chat_template.txt,persona_tier_a_v4.txt,engine_a_g_arch.py,train_phase2_cotrain.py}'

# Launch training (nohup, runs detached)
ssh -i "$SSH_KEY" -p "$SSH_PORT" -o StrictHostKeyChecking=no root@$SSH_HOST << 'POD_EOF'
cd /workspace/anima_phase2
mkdir -p ckpts state
nohup python3 train_phase2_cotrain.py \
  --substrate-ckpt /workspace/anima_phase2/bg_lb_step_8000_final.pt \
  --consciousness-corpus /workspace/anima_phase2/persona_tier_a_v4.txt \
  --chat-corpus /workspace/anima_phase2/corpus_chat_template.txt \
  --output /workspace/anima_phase2/ckpts \
  --steps 6000 --bsz 4 --grad-accum 8 --ctx 1024 \
  --lr 1.5e-4 --warmup 200 --save-every 1500 \
  --cost-cap-usd 50.0 --cost-per-hr 3.07 \
  --w-start 0.3 --w-end 0.5 \
  > train.log 2>&1 &
TRAIN_PID=$!
echo "TRAIN_PID=$TRAIN_PID"
sleep 30
echo "--- first 30s log ---"
tail -20 train.log
POD_EOF

echo "TRAIN_LAUNCHED"
