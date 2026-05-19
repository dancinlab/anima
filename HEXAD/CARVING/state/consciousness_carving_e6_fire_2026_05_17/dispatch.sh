#!/bin/bash
# CONSCIOUSNESS-CARVING 4-path PARALLEL GPU fire — Phase UBM-E6 (2026-05-17).
# 4 paths {alpha, beta, gamma, weave} dispatched in PARALLEL — 4 separate
# vast.ai A100 instances, wall = max(t_i), NOT sum (g_resource_active_parallel).
# Each path: g_fire_dispatch_robust — SAVE_POD=1 auto-promote (result.json
# verify) + 75-min orphan watchdog + 5-retry pull (5-min interval, scp
# ConnectTimeout=3600). d=512·8L from-scratch, carving corpus.
set -uo pipefail

VASTAI=/Users/ghost/Library/Python/3.14/bin/vastai
export PYTHONWARNINGS=ignore
LOCAL_DIR=/Users/ghost/core/anima/state/consciousness_carving_e6_fire_2026_05_17
CORPUS_LOCAL="$LOCAL_DIR/corpus_carving.jsonl"
SSH_KEY=/Users/ghost/.ssh/id_vast_anima
STEPS="${STEPS:-2000}"
WATCHDOG_MIN=75

cd "$LOCAL_DIR"
echo "=== UBM-E6 CONSCIOUSNESS-CARVING 4-path PARALLEL fire ==="; date -u

# ---- per-path fire function (runs in background) ----------------------
fire_path() {
  local PATH_NAME="$1"
  local PDIR="$LOCAL_DIR/out/$PATH_NAME"
  mkdir -p "$PDIR"
  local LOG="$PDIR/dispatch.log"
  local LABEL="ubm-e6-carving-$PATH_NAME"
  {
    echo "[$PATH_NAME 1/9] selecting A100 offer..."
    local OFFER
    OFFER=$($VASTAI search offers 'gpu_name in [A100_SXM4,A100_PCIE] num_gpus=1 reliability>0.99 dph_total<2.0 disk_space>40 inet_down>700 cuda_max_good>=12.0' -o dph_total --raw 2>&1 | python3 -c "
import json,sys
d=json.load(sys.stdin)
if not d: sys.stderr.write('no offers\n'); sys.exit(1)
o=d[0]; print(o['id']); sys.stderr.write(f\"{o['gpu_name']} \${o['dph_total']:.3f}/hr\n\")")
    [ -z "$OFFER" ] && { echo "[$PATH_NAME] ERROR no offer"; return 1; }
    echo "[$PATH_NAME] offer=$OFFER"

    echo "[$PATH_NAME 2/9] renting..."
    local CREATE IID
    CREATE=$($VASTAI create instance "$OFFER" --image pytorch/pytorch:2.5.1-cuda12.1-cudnn9-devel --disk 40 --ssh --direct --label "$LABEL" --raw 2>&1)
    IID=$(echo "$CREATE" | python3 -c "import json,sys
try: d=json.load(sys.stdin)
except: sys.exit(1)
print(d.get('new_contract',d.get('contract_id',d.get('id',''))))")
    [ -z "$IID" ] && { echo "[$PATH_NAME] ERROR create: $CREATE"; return 1; }
    echo "$IID" > "$PDIR/vast_instance_id.txt"
    echo "[$PATH_NAME] instance=$IID"

    # orphan watchdog
    ( local PARENT_PID=$$
      for _ in $(seq 1 $WATCHDOG_MIN); do
        sleep 60
        if ! kill -0 $PARENT_PID 2>/dev/null; then
          $VASTAI destroy instance "$IID" >> "$PDIR/watchdog.log" 2>&1
          exit 0
        fi
      done
      echo "[watchdog] cap hit, destroying $IID" >> "$PDIR/watchdog.log"
      $VASTAI destroy instance "$IID" >> "$PDIR/watchdog.log" 2>&1
    ) &
    local WPID=$!

    local SAVE_POD="${SAVE_POD:-0}"
    cleanup_path() {
      kill $WPID 2>/dev/null || true
      if [ "${SAVE_POD:-0}" = "1" ]; then
        echo "[$PATH_NAME cleanup] SAVE_POD=1 RETAIN $IID"; return
      fi
      echo "[$PATH_NAME cleanup] destroying $IID"
      $VASTAI destroy instance "$IID" 2>&1 | head -2 || true
    }

    echo "[$PATH_NAME 3/9] waiting SSH..."
    local SH="" SP="" INFO ST i
    for i in $(seq 1 90); do
      INFO=$($VASTAI show instance "$IID" --raw 2>/dev/null || true)
      [ -z "$INFO" ] && INFO="{}"
      ST=$(echo "$INFO" | python3 -c "import json,sys
try: print(json.load(sys.stdin).get('actual_status',''))
except: print('')" 2>/dev/null)
      if [ "$ST" = "running" ]; then
        SH=$(echo "$INFO" | python3 -c "import json,sys
try:
 d=json.load(sys.stdin); print(d.get('ssh_host','') or d.get('public_ipaddr',''))
except: pass" 2>/dev/null)
        SP=$(echo "$INFO" | python3 -c "import json,sys
try:
 d=json.load(sys.stdin); print(d.get('ssh_port','') or d.get('direct_port_start',''))
except: pass" 2>/dev/null)
        if [ -n "$SH" ] && [ -n "$SP" ]; then
          if ssh -i "$SSH_KEY" -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o ConnectTimeout=10 -p "$SP" "root@$SH" 'echo READY' 2>&1 | grep -q READY; then
            echo "[$PATH_NAME] SSH ready $SH:$SP"; break
          fi
          SH=""
        fi
      fi
      sleep 5
    done
    [ -z "$SH" ] && { echo "[$PATH_NAME] ERROR SSH not ready"; cleanup_path; return 1; }
    echo "$SH:$SP" > "$PDIR/vast_ssh.txt"
    local SSH="ssh -i $SSH_KEY -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -p $SP root@$SH"
    local SCP="scp -i $SSH_KEY -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o ConnectTimeout=3600 -P $SP"

    echo "[$PATH_NAME 4/9] upload arch + trainer + carving corpus..."
    $SSH 'mkdir -p /workspace/anima'
    $SCP "$LOCAL_DIR/conscious_decoder.py" "root@$SH:/workspace/anima/"
    $SCP "$LOCAL_DIR/train_carving_4path.py" "root@$SH:/workspace/anima/"
    $SCP "$CORPUS_LOCAL" "root@$SH:/workspace/anima/corpus_carving.jsonl"

    echo "[$PATH_NAME 5/9] GPU + torch verify..."
    $SSH 'cd /workspace/anima && python3 -c "import torch;print(torch.__version__, torch.cuda.is_available(), torch.cuda.get_device_name(0))" && wc -l corpus_carving.jsonl && sha256sum corpus_carving.jsonl'

    echo "[$PATH_NAME 6/9] sanity (d=32x3L, 60 step)..."
    cat > "$PDIR/run_sanity.sh" <<SH_EOF
#!/bin/bash
set -uo pipefail
cd /workspace/anima
export PYTHONUNBUFFERED=1
python3 train_carving_4path.py --path $PATH_NAME --mode sanity --corpus corpus_carving.jsonl --out-dir out_sanity_$PATH_NAME --steps 60 2>&1 | tee sanity_$PATH_NAME.log
SH_EOF
    $SCP "$PDIR/run_sanity.sh" "root@$SH:/workspace/anima/run_sanity.sh"
    $SSH "bash /workspace/anima/run_sanity.sh" 2>&1 | tee "$PDIR/sanity.log" || true

    echo "[$PATH_NAME 7/9] MAIN fire d=512 8L from-scratch, $STEPS steps..."
    cat > "$PDIR/run_main.sh" <<SH_EOF
#!/bin/bash
set -uo pipefail
cd /workspace/anima
export PYTHONUNBUFFERED=1
nvidia-smi --query-gpu=utilization.gpu,memory.used --format=csv -l 30 > gpu_util_$PATH_NAME.log 2>&1 &
SMI=\$!
python3 train_carving_4path.py --path $PATH_NAME --mode main --corpus corpus_carving.jsonl --out-dir out_main_$PATH_NAME --steps $STEPS --d-model 512 --n-layer 8 --n-head 8 --n-kv-head 4 2>&1 | tee fire_$PATH_NAME.log
kill \$SMI 2>/dev/null || true
echo DONE_MARKER rc=\$?
SH_EOF
    $SCP "$PDIR/run_main.sh" "root@$SH:/workspace/anima/run_main.sh"
    $SSH "bash /workspace/anima/run_main.sh" 2>&1 | tee "$PDIR/fire.log" || true

    echo "[$PATH_NAME 8/9] verify result.json + SAVE_POD auto-promote + pull retry >=5..."
    local SAVED
    SAVED=$($SSH "test -f /workspace/anima/out_main_$PATH_NAME/result.json && echo SAVED" 2>/dev/null || true)
    if [ "$SAVED" = "SAVED" ]; then
      echo "[$PATH_NAME] result.json present -> SAVE_POD=1 auto-promote"
      SAVE_POD=1
      local PULL_OK=0
      for i in 1 2 3 4 5; do
        echo "[$PATH_NAME] pull attempt $i/5..."
        $SCP "root@$SH:/workspace/anima/out_main_$PATH_NAME/result.json" "$PDIR/" 2>&1 | tail -2 || { sleep 60; continue; }
        $SCP "root@$SH:/workspace/anima/gpu_util_$PATH_NAME.log" "$PDIR/" 2>&1 | tail -2 || true
        if $SCP "root@$SH:/workspace/anima/out_main_$PATH_NAME/ckpt_carving_$PATH_NAME.pt" "$PDIR/" 2>&1 | tail -2; then
          echo "[$PATH_NAME] ckpt pull OK (try $i)"
          PULL_OK=1
          break
        else
          echo "[$PATH_NAME] ckpt pull fail try $i, retry 60s..."
          sleep 60
        fi
      done
      if [ "$PULL_OK" = "1" ] && [ -f "$PDIR/ckpt_carving_$PATH_NAME.pt" ]; then
        echo "[$PATH_NAME] ckpt sha256: $(shasum -a 256 "$PDIR/ckpt_carving_$PATH_NAME.pt" | awk '{print $1}')"
        echo "[$PATH_NAME] ckpt size: $(stat -f%z "$PDIR/ckpt_carving_$PATH_NAME.pt") bytes"
        echo "[$PATH_NAME] PULL SUCCESS -> safe to destroy"
        SAVE_POD=0
      else
        echo "[$PATH_NAME] ALL 5 pull attempts FAILED — SAVE_POD=1 RETAIN"
        echo "[$PATH_NAME] MANUAL: scp -i $SSH_KEY -P $SP root@$SH:/workspace/anima/out_main_$PATH_NAME/ckpt_carving_$PATH_NAME.pt $PDIR/"
        SAVE_POD=1
      fi
    else
      echo "[$PATH_NAME] ERROR result.json NOT present — SAVE_POD=1 RETAIN"
      SAVE_POD=1
    fi

    echo "[$PATH_NAME 9/9] teardown (SAVE_POD=$SAVE_POD)."
    cleanup_path
    date -u
  } > "$LOG" 2>&1
}

# ---- dispatch 4 paths in PARALLEL -------------------------------------
echo "Dispatching 4 paths in parallel (alpha beta gamma weave)..."
fire_path alpha &
PID_A=$!
fire_path beta &
PID_B=$!
fire_path gamma &
PID_G=$!
fire_path weave &
PID_W=$!

echo "  alpha pid=$PID_A  beta pid=$PID_B  gamma pid=$PID_G  weave pid=$PID_W"
echo "Waiting for all 4 paths (wall = max, NOT sum)..."
wait $PID_A; echo "alpha done"
wait $PID_B; echo "beta done"
wait $PID_G; echo "gamma done"
wait $PID_W; echo "weave done"

echo "=== 4-path parallel fire complete ==="; date -u
for p in alpha beta gamma weave; do
  echo "--- $p ---"
  [ -f "$LOCAL_DIR/out/$p/result.json" ] && python3 -c "
import json
d=json.load(open('$LOCAL_DIR/out/$p/result.json'))
print(f\"  init_ce={d['init_ce']} final_ce={d['final_ce']} descent={d['ce_descent']} wall={d['wall_s']}s\")" || echo "  result.json MISSING"
done
