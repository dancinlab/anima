#!/bin/bash
# BG-LA monitor — wait for sentinel or step_2000 ckpt (whichever first)
SSH_HOST=87.120.211.205
SSH_PORT=10025
SSH_KEY=/Users/ghost/.runpod/ssh/RunPod-Key-Go
START=$(date -u +%s)
until ssh -i "$SSH_KEY" -p "$SSH_PORT" -o StrictHostKeyChecking=no root@$SSH_HOST \
    'test -f /workspace/anima_clm_la/state/COMPLETE.sentinel || ls /workspace/anima_clm_la/ckpts/step_2000.pt 2>/dev/null' 2>/dev/null; do
    sleep 300
    NOW=$(date -u +%s)
    ELAPSED=$((NOW - START))
    COST=$(echo "scale=2; $ELAPSED * 2.99 / 3600" | bc)
    echo "[hb t=${ELAPSED}s cost_this_session=\$$COST]"
    ssh -i "$SSH_KEY" -p "$SSH_PORT" -o StrictHostKeyChecking=no root@$SSH_HOST \
        'tail -2 /workspace/anima_clm_la/train.log; ls /workspace/anima_clm_la/ckpts/ 2>/dev/null | wc -l | xargs echo ckpts:'
done
echo "MONITOR_TRIGGERED"
ssh -i "$SSH_KEY" -p "$SSH_PORT" -o StrictHostKeyChecking=no root@$SSH_HOST \
    'tail -10 /workspace/anima_clm_la/train.log; ls -la /workspace/anima_clm_la/ckpts/'
