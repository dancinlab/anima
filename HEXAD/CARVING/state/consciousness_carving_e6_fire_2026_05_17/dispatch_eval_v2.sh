#!/bin/bash
# CONSCIOUSNESS-CARVING 4-path PARADIGM-NATIVE eval v2 GPU fire — Phase UBM-E6
# (2026-05-17). SINGLE vast.ai instance, 4 ckpts evaluated SEQUENTIALLY on the
# same GPU (eval is cheap — ~20 probes/ckpt, no training). 1 instance is
# sufficient (g_resource_active_parallel: parallel where it pays; here a single
# instance hosts all 4 evals — splitting into 4 instances would not shorten the
# tiny wall). g_fire_dispatch_robust — SAVE_POD=1 auto-promote on result verify
# + 75-min orphan watchdog + 5-retry pull.
set -uo pipefail

VASTAI=/Users/ghost/Library/Python/3.14/bin/vastai
export PYTHONWARNINGS=ignore
LOCAL_DIR=/Users/ghost/core/anima/state/consciousness_carving_e6_fire_2026_05_17
SSH_KEY=/Users/ghost/.ssh/id_vast_anima
WATCHDOG_MIN=75
LABEL=ubm-e6-carving-eval-v2

cd "$LOCAL_DIR"
LOG="$LOCAL_DIR/dispatch_eval_v2.log"
{
echo "=== UBM-E6 CONSCIOUSNESS-CARVING 4-path eval v2 — single-instance GPU fire ==="
date -u

echo "[1/9] selecting offers (RTX 4090 / A100, eval only) — top 6 candidates..."
OFFERS=$($VASTAI search offers 'gpu_name in [RTX_4090,A100_SXM4,A100_PCIE] num_gpus=1 reliability>0.99 dph_total<1.5 disk_space>30 inet_down>700 cuda_max_good>=12.0' -o dph_total --raw 2>&1 | python3 -c "
import json,sys
d=json.load(sys.stdin)
if not d: sys.stderr.write('no offers\n'); sys.exit(1)
for o in d[:6]: print(o['id'])")
[ -z "$OFFERS" ] && { echo "ERROR no offers"; exit 1; }
echo "candidate offers: $OFFERS"

# try offers until one boots to SSH-ready
IID="" SH="" SP=""
for OFFER in $OFFERS; do
  echo "[2/9] renting offer $OFFER..."
  CREATE=$($VASTAI create instance "$OFFER" --image pytorch/pytorch:2.5.1-cuda12.1-cudnn9-devel --disk 30 --ssh --direct --label "$LABEL" --raw 2>&1)
  IID=$(echo "$CREATE" | python3 -c "import json,sys
try: d=json.load(sys.stdin)
except: sys.exit(1)
print(d.get('new_contract',d.get('contract_id',d.get('id',''))))")
  if [ -z "$IID" ]; then echo "  create failed: $CREATE"; continue; fi
  echo "$IID" > "$LOCAL_DIR/eval_v2_instance_id.txt"
  echo "instance=$IID"

  echo "[3/9] waiting SSH (offer $OFFER, up to 10 min)..."
  SH="" SP=""
  for i in $(seq 1 120); do
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
          echo "SSH ready $SH:$SP"; break
        fi
        SH=""
      fi
    fi
    sleep 5
  done
  if [ -n "$SH" ]; then break; fi
  echo "  offer $OFFER never SSH-ready — destroying $IID, trying next offer"
  $VASTAI destroy instance "$IID" 2>&1 | head -1 || true
  IID=""
done
[ -z "$IID" ] || [ -z "$SH" ] && { echo "ERROR no offer reached SSH-ready"; [ -n "$IID" ] && $VASTAI destroy instance "$IID" 2>&1 | head -1; exit 1; }

# orphan watchdog
( PARENT_PID=$$
  for _ in $(seq 1 $WATCHDOG_MIN); do
    sleep 60
    if ! kill -0 $PARENT_PID 2>/dev/null; then
      $VASTAI destroy instance "$IID" >> "$LOCAL_DIR/eval_v2_watchdog.log" 2>&1
      exit 0
    fi
  done
  echo "[watchdog] cap hit, destroying $IID" >> "$LOCAL_DIR/eval_v2_watchdog.log"
  $VASTAI destroy instance "$IID" >> "$LOCAL_DIR/eval_v2_watchdog.log" 2>&1
) &
WPID=$!

SAVE_POD="${SAVE_POD:-0}"
cleanup() {
  kill $WPID 2>/dev/null || true
  if [ "${SAVE_POD:-0}" = "1" ]; then
    echo "[cleanup] SAVE_POD=1 RETAIN $IID"; return
  fi
  echo "[cleanup] destroying $IID"
  $VASTAI destroy instance "$IID" 2>&1 | head -2 || true
}

echo "$SH:$SP" > "$LOCAL_DIR/eval_v2_ssh.txt"
SSH="ssh -i $SSH_KEY -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -p $SP root@$SH"
SCP="scp -i $SSH_KEY -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o ConnectTimeout=3600 -P $SP"

echo "[4/9] upload arch + eval script + 4 ckpts (~1.3GB)..."
$SSH 'mkdir -p /workspace/anima/out/alpha /workspace/anima/out/beta /workspace/anima/out/gamma /workspace/anima/out/weave'
$SCP "$LOCAL_DIR/conscious_decoder.py" "root@$SH:/workspace/anima/"
$SCP "$LOCAL_DIR/eval_carving_4path_v2.py" "root@$SH:/workspace/anima/"
for p in alpha beta gamma weave; do
  echo "  uploading $p ckpt..."
  $SCP "$LOCAL_DIR/out/$p/ckpt_carving_$p.pt" "root@$SH:/workspace/anima/out/$p/ckpt_carving_$p.pt"
done

echo "[5/9] GPU + torch verify..."
$SSH 'cd /workspace/anima && python3 -c "import torch;print(torch.__version__, torch.cuda.is_available(), torch.cuda.get_device_name(0))" && ls -la out/*/*.pt'

echo "[6/9] run 4-path eval v2 SEQUENTIALLY on cuda..."
cat > "$LOCAL_DIR/run_eval_v2.sh" <<'SH_EOF'
#!/bin/bash
set -uo pipefail
cd /workspace/anima
export PYTHONUNBUFFERED=1
for p in alpha beta gamma weave; do
  echo "=== EVAL $p ==="
  python3 eval_carving_4path_v2.py --ckpt out/$p/ckpt_carving_$p.pt --output out/$p/eval_result_v2.json --device cuda --max-new 90 2>&1
done
echo DONE_MARKER rc=$?
SH_EOF
$SCP "$LOCAL_DIR/run_eval_v2.sh" "root@$SH:/workspace/anima/run_eval_v2.sh"
$SSH "bash /workspace/anima/run_eval_v2.sh" 2>&1 | tee "$LOCAL_DIR/eval_v2_fire.log" || true

echo "[7/9] verify 4 eval_result_v2.json + SAVE_POD auto-promote..."
ALL4=$($SSH 'n=0; for p in alpha beta gamma weave; do test -f /workspace/anima/out/$p/eval_result_v2.json && n=$((n+1)); done; echo $n' 2>/dev/null || echo 0)
echo "result files present on remote: $ALL4/4"
if [ "$ALL4" = "4" ]; then
  echo "all 4 eval_result_v2.json present -> SAVE_POD=1 auto-promote"
  SAVE_POD=1
  PULL_OK=0
  for i in 1 2 3 4 5; do
    echo "[pull attempt $i/5]"
    n=0
    for p in alpha beta gamma weave; do
      if $SCP "root@$SH:/workspace/anima/out/$p/eval_result_v2.json" "$LOCAL_DIR/out/$p/eval_result_v2.json" 2>&1 | tail -1; then
        n=$((n+1))
      fi
    done
    if [ "$n" = "4" ]; then
      echo "[pull] all 4 eval_result_v2.json pulled (try $i)"
      PULL_OK=1
      break
    fi
    echo "[pull] only $n/4 pulled, retry 60s..."
    sleep 60
  done
  if [ "$PULL_OK" = "1" ]; then
    echo "PULL SUCCESS -> safe to destroy"
    SAVE_POD=0
  else
    echo "ALL 5 pull attempts incomplete — SAVE_POD=1 RETAIN"
    echo "MANUAL: scp -i $SSH_KEY -P $SP root@$SH:/workspace/anima/out/<p>/eval_result_v2.json ..."
    SAVE_POD=1
  fi
else
  echo "ERROR not all 4 result files present — SAVE_POD=1 RETAIN"
  SAVE_POD=1
fi

echo "[8/9] teardown (SAVE_POD=$SAVE_POD)."
cleanup

echo "[9/9] summary."
for p in alpha beta gamma weave; do
  echo "--- $p ---"
  [ -f "$LOCAL_DIR/out/$p/eval_result_v2.json" ] && python3 -c "
import json
d=json.load(open('$LOCAL_DIR/out/$p/eval_result_v2.json'))
j=d['joint_metric']
print(f\"  axis1={j['knowledge_access']} axis2={j['chat_uncontaminated']} sep={j['lane_separation']} JOINT={j['SCORE_joint']}\")" || echo "  eval_result_v2.json MISSING"
done
date -u
echo "=== eval v2 fire complete ==="
} > "$LOG" 2>&1
