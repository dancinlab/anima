#!/usr/bin/env bash
# §41 manual poll + pull recovery script — the original dispatch's
# inline SSH-training-launch hung because SSH doesn't disconnect even
# when the remote process is backgrounded with nohup. The training is
# still running on pod s2p9efumbskz94 (verified python pid 175 alive
# with GPU 100%). This script polls for completion (ckpt + result.json)
# and pulls when done.
set -euo pipefail
HERE="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"
cd "$HERE"

POD_ID="${POD_ID:-s2p9efumbskz94}"
IP="${IP:-216.81.248.113}"
PORT="${PORT:-13492}"
RUNPOD_KEY="$(secret get runpod.api_key 2>/dev/null)"
export RUNPODCTL_API_KEY="$RUNPOD_KEY"

# Use BatchMode + ConnectTimeout to prevent hang on flaky SSH; pipe to
# /dev/null on the remote stdout/stderr so SSH disconnects cleanly.
SSH_OPTS=(-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null
          -o BatchMode=yes -o ConnectTimeout=15 -o ServerAliveInterval=30
          -o ServerAliveCountMax=3 -p "$PORT")
SSH=(ssh "${SSH_OPTS[@]}" "root@$IP")
SCP=(scp "${SSH_OPTS[@]/-p $PORT/-P $PORT}" -o ConnectTimeout=3600)

# Poll for training completion (ckpt + result.json + train_complete_pending_eval).
echo "[§41 poll] starting poll loop (90s interval, 30 iters = 45min ceiling)"
TRAIN_DONE=""
for i in $(seq 1 30); do
    sleep 90
    OUT="$("${SSH[@]}" 'test -f /workspace/s41/ckpt_s41.pt && grep -q train_complete_pending_eval /workspace/s41/result.json 2>/dev/null && echo TRAIN_DONE' 2>/dev/null || true)"
    TRAIN_DONE="$OUT"
    echo "[§41 poll] iter $i/30  done=${TRAIN_DONE:-pending}  $(date +%H:%M:%S)"
    [ "$TRAIN_DONE" = "TRAIN_DONE" ] && break
done

if [ "$TRAIN_DONE" != "TRAIN_DONE" ]; then
    echo "[§41 poll] training timeout — pod retained for manual recovery"
    exit 5
fi

# Launch eval (detached background, then poll for completion).
echo "[§41 poll] launching eval"
"${SSH[@]}" 'cd /workspace/s41 && nohup python3 -u eval_s41.py --ckpt ckpt_s41.pt --result result.json > eval.log 2>&1 < /dev/null & disown'
sleep 5  # let nohup take

EVAL_DONE=""
for i in $(seq 1 20); do
    sleep 90
    OUT="$("${SSH[@]}" 'grep -q "\"phase\": \"complete\"" /workspace/s41/result.json 2>/dev/null && echo EVAL_DONE' 2>/dev/null || true)"
    EVAL_DONE="$OUT"
    echo "[§41 poll] eval iter $i/20  done=${EVAL_DONE:-pending}  $(date +%H:%M:%S)"
    [ "$EVAL_DONE" = "EVAL_DONE" ] && break
done

if [ "$EVAL_DONE" != "EVAL_DONE" ]; then
    echo "[§41 poll] eval timeout — pod retained for manual recovery"
    exit 6
fi

# Pull artifacts (5-retry per g_fire_dispatch_robust).
echo "[§41 poll] eval complete — pulling artifacts"
PULL_OK=0
for try in 1 2 3 4 5; do
    if "${SCP[@]}" "root@$IP:/workspace/s41/result.json" ./result.json \
       && "${SCP[@]}" "root@$IP:/workspace/s41/ckpt_s41.pt" ./ckpt_s41.pt \
       && "${SCP[@]}" "root@$IP:/workspace/s41/train.log" ./train.log \
       && "${SCP[@]}" "root@$IP:/workspace/s41/eval.log" ./eval.log; then
        PULL_OK=1; break
    fi
    echo "[§41 poll] pull try $try FAILED — retry in 60s"
    sleep 60
done

[ "$PULL_OK" = "1" ] || { echo "[§41 poll] PULL FAILED — pod retained"; exit 7; }

CKPT_SHA="$(python3 -c 'import hashlib;print(hashlib.sha256(open("ckpt_s41.pt","rb").read()).hexdigest())')"
echo "[§41 poll] local ckpt sha256=$CKPT_SHA"

# Terminate pod (SAVE_POD=0 implicit after successful pull).
python3 -c "import runpod, os; runpod.api_key=os.environ['RUNPODCTL_API_KEY']; runpod.terminate_pod(\"$POD_ID\")" || true
echo "[§41 poll] pod terminated — complete"
