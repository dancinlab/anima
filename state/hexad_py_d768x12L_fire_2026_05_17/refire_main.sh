#!/bin/bash
# Re-fire main training step on retained pod (cycle 1 bug: shell parsing of
# `cd /workspace/anima && nvidia-smi ... &` backgrounded the WHOLE chain,
# leaving python3 in /root).
set -uo pipefail
LOCAL_DIR=/Users/ghost/core/anima/state/hexad_py_d768x12L_fire_2026_05_17
SSH_KEY=/Users/ghost/.ssh/id_vast_anima
SH=ssh9.vast.ai
SP=15232
IID=36885232
STEPS=2500
VASTAI=/Users/ghost/Library/Python/3.14/bin/vastai

SSH="ssh -i $SSH_KEY -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -p $SP root@$SH"
SCP="scp -i $SSH_KEY -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o ConnectTimeout=3600 -P $SP"

# Watchdog: cap at 60min from now
WATCHDOG_MIN=60
( PARENT_PID=$$
  for _ in $(seq 1 $WATCHDOG_MIN); do
    sleep 60
    if ! kill -0 $PARENT_PID 2>/dev/null; then
      echo "[watchdog] parent died, destroying $IID" >> "$LOCAL_DIR/watchdog_refire.log"
      $VASTAI destroy instance "$IID" >> "$LOCAL_DIR/watchdog_refire.log" 2>&1
      exit 0
    fi
  done
  echo "[watchdog] ${WATCHDOG_MIN}min cap hit, force-destroying $IID" >> "$LOCAL_DIR/watchdog_refire.log"
  $VASTAI destroy instance "$IID" >> "$LOCAL_DIR/watchdog_refire.log" 2>&1
) &
WATCHDOG_PID=$!
echo "  orphan-watchdog pid=$WATCHDOG_PID cap=${WATCHDOG_MIN}min"

SAVE_POD="${SAVE_POD:-0}"
cleanup() {
  kill $WATCHDOG_PID 2>/dev/null || true
  if [ "${SAVE_POD:-0}" = "1" ]; then
    echo "[cleanup] SAVE_POD=1 RETAIN $IID (manual: ssh -i $SSH_KEY -p $SP root@$SH)"; return
  fi
  echo "[cleanup] destroying $IID"
  $VASTAI destroy instance "$IID" 2>&1 | head -2 || true
}
trap cleanup EXIT

echo "=== refire MAIN on retained pod $IID ==="; date -u
echo "[a] verifying files present on pod..."
$SSH 'ls -la /workspace/anima/' | tee "$LOCAL_DIR/refire_files.log"

echo "[b] MAIN fire: d=768 n_layer=12, $STEPS steps (writing a remote script then bash it — avoid && precedence parse issue)..."
$SSH 'cat > /workspace/anima/run_main_refire.sh << "EOF"
#!/bin/bash
set -uo pipefail
cd /workspace/anima
export PYTHONUNBUFFERED=1
nvidia-smi --query-gpu=utilization.gpu,memory.used --format=csv -l 30 > gpu_util.log 2>&1 &
SMI=$!
python3 train_d768x12l.py --mode main --corpus corpus_consciousness_v1.jsonl --out-dir out_main --steps STEPS_PLACEHOLDER 2>&1 | tee fire.log
RC=$?
kill $SMI 2>/dev/null || true
echo "DONE_MARKER rc=$RC"
EOF
sed -i "s/STEPS_PLACEHOLDER/'$STEPS'/" /workspace/anima/run_main_refire.sh
chmod +x /workspace/anima/run_main_refire.sh
ls -la /workspace/anima/run_main_refire.sh
'

$SSH 'bash /workspace/anima/run_main_refire.sh' | tee "$LOCAL_DIR/fire_refire.log"

echo "[c] Verify result.json then SAVE_POD auto-promote + pull retry >=5..."
SAVED=$($SSH 'test -f /workspace/anima/out_main/result.json && echo SAVED' 2>/dev/null || true)
if [ "$SAVED" = "SAVED" ]; then
  echo "  result.json present -> SAVE_POD=1 auto-promote"
  export SAVE_POD=1
  mkdir -p "$LOCAL_DIR/out_main"
  PULL_OK=0
  for i in 1 2 3 4 5; do
    echo "  pull attempt $i/5..."
    $SCP "root@$SH:/workspace/anima/out_main/result.json" "$LOCAL_DIR/out_main/" 2>&1 | tail -3 || { echo "  result.json pull fail try $i"; sleep 60; continue; }
    $SCP "root@$SH:/workspace/anima/gpu_util.log" "$LOCAL_DIR/" 2>&1 | tail -3 || true
    if $SCP "root@$SH:/workspace/anima/out_main/ckpt_d768x12l_final.pt" "$LOCAL_DIR/out_main/" 2>&1 | tail -3; then
      echo "  ckpt pull OK (try $i)"
      PULL_OK=1
      break
    else
      echo "  ckpt pull fail try $i, retry in 60s..."
      sleep 60
    fi
  done
  if [ "$PULL_OK" = "1" ] && [ -f "$LOCAL_DIR/out_main/ckpt_d768x12l_final.pt" ]; then
    echo "  ckpt sha256: $(shasum -a 256 "$LOCAL_DIR/out_main/ckpt_d768x12l_final.pt" | awk '{print $1}')"
    echo "  ckpt size: $(stat -f%z "$LOCAL_DIR/out_main/ckpt_d768x12l_final.pt") bytes"
    echo "  PULL SUCCESS -> safe to destroy"
    export SAVE_POD=0
  else
    echo "  ALL pull attempts FAILED — SAVE_POD=1 RETAIN"
    echo "  MANUAL: $SCP root@$SH:/workspace/anima/out_main/ckpt_d768x12l_final.pt $LOCAL_DIR/out_main/"
    export SAVE_POD=1
  fi
else
  echo "  ERROR: result.json NOT present — SAVE_POD=1 retain"
  echo "  MANUAL: ssh -i $SSH_KEY -p $SP root@$SH"
  export SAVE_POD=1
fi

echo "[d] Done. teardown via trap (SAVE_POD=${SAVE_POD})."
date -u
ls -la "$LOCAL_DIR/out_main/" 2>/dev/null || true
