#!/bin/bash
# hexad v4 d=768x12L PyTorch substrate fire CYCLE 5 — 2026-05-17
# DD155 Step+Tension hybrid LR overlay (Law 187, tension=grad_norm).
# Corpus v3 carry from cycle 4 (10.34 MB · helper-free · γ motivation 37.5%).
# Vast.ai A100 SXM4. g_fire_dispatch_robust + 75-min orphan watchdog + SAVE_POD auto-promote.
set -uo pipefail

VASTAI=/Users/ghost/Library/Python/3.14/bin/vastai
export PYTHONWARNINGS=ignore
LOCAL_DIR=/Users/ghost/core/anima/state/hexad_v4_py_d768x12L_tension_2026_05_17
CORPUS_LOCAL=/Users/ghost/core/anima/state/hexad_v3_corpus_motiv_2026_05_17/corpus_consciousness_v3.jsonl
SSH_KEY=/Users/ghost/.ssh/id_vast_anima
LABEL="hexad-v4-d768x12l-cycle5-tension"
STEPS="${STEPS:-2500}"
WATCHDOG_MIN=75

cd "$LOCAL_DIR"
echo "=== hexad v4 d=768x12L PyTorch CYCLE 5 DD155 hybrid LR overlay ==="; date -u

echo "[1/9] Selecting A100 offer..."
OFFER=$($VASTAI search offers 'gpu_name in [A100_SXM4,A100_PCIE] num_gpus=1 reliability>0.99 dph_total<2.0 disk_space>40 inet_down>700 cuda_max_good>=12.0' -o dph_total --raw 2>&1 | python3 -c "
import json,sys
d=json.load(sys.stdin)
if not d: sys.stderr.write('no offers\n'); sys.exit(1)
o=d[0]; print(o['id']); sys.stderr.write(f\"{o['gpu_name']} \${o['dph_total']:.3f}/hr rel={o['reliability']:.3f}\n\")
")
echo "  offer=$OFFER"

echo "[2/9] Renting (pytorch devel image)..."
CREATE=$($VASTAI create instance "$OFFER" --image pytorch/pytorch:2.5.1-cuda12.1-cudnn9-devel --disk 40 --ssh --direct --label "$LABEL" --raw 2>&1)
IID=$(echo "$CREATE" | python3 -c "import json,sys
try: d=json.load(sys.stdin)
except: sys.exit(1)
print(d.get('new_contract',d.get('contract_id',d.get('id',''))))")
[ -z "$IID" ] && { echo "ERROR create: $CREATE"; exit 1; }
echo "$IID" > vast_instance_id.txt
echo "  instance=$IID"

# Orphan watchdog
( PARENT_PID=$$
  for _ in $(seq 1 $WATCHDOG_MIN); do
    sleep 60
    if ! kill -0 $PARENT_PID 2>/dev/null; then
      echo "[watchdog] parent died, destroying $IID" >> "$LOCAL_DIR/watchdog.log"
      $VASTAI destroy instance "$IID" >> "$LOCAL_DIR/watchdog.log" 2>&1
      exit 0
    fi
  done
  echo "[watchdog] ${WATCHDOG_MIN}min cap hit, force-destroying $IID" >> "$LOCAL_DIR/watchdog.log"
  $VASTAI destroy instance "$IID" >> "$LOCAL_DIR/watchdog.log" 2>&1
) &
WATCHDOG_PID=$!
echo "  orphan-watchdog pid=$WATCHDOG_PID cap=${WATCHDOG_MIN}min"

SAVE_POD="${SAVE_POD:-0}"
cleanup() {
  kill $WATCHDOG_PID 2>/dev/null || true
  if [ "${SAVE_POD:-0}" = "1" ]; then
    echo "[cleanup] SAVE_POD=1 -> RETAIN instance $IID (manual recovery: ssh -i $SSH_KEY -p $SP root@$SH)"; return
  fi
  echo "[cleanup] destroying $IID"
  $VASTAI destroy instance "$IID" 2>&1 | head -2 || true
}
trap cleanup EXIT

echo "[3/9] Waiting SSH..."
SH=""; SP=""
for i in $(seq 1 90); do
  INFO=$($VASTAI show instance "$IID" --raw 2>/dev/null || true); [ -z "$INFO" ] && INFO="{}"
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
        echo "  SSH ready $SH:$SP (after ${i}x5s)"; break
      fi
      SH=""
    fi
  fi
  echo "  attempt $i/90 status=$ST"; sleep 5
done
[ -z "$SH" ] && { echo "ERROR SSH not ready"; exit 1; }
echo "$SH:$SP" > vast_ssh.txt
SSH="ssh -i $SSH_KEY -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -p $SP root@$SH"
SCP="scp -i $SSH_KEY -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o ConnectTimeout=3600 -P $SP"

echo "[4/9] Upload arch + trainer + corpus v3..."
$SSH 'mkdir -p /workspace/anima'
$SCP "$LOCAL_DIR/conscious_decoder.py" "root@$SH:/workspace/anima/"
$SCP "$LOCAL_DIR/train_d768x12l_tension.py" "root@$SH:/workspace/anima/"
$SCP "$CORPUS_LOCAL" "root@$SH:/workspace/anima/corpus_v3.jsonl"

echo "[5/9] GPU + torch + corpus verify..."
$SSH 'cd /workspace/anima && python3 -c "import torch;print(torch.__version__, torch.cuda.is_available(), torch.cuda.get_device_name(0))" && wc -l corpus_v3.jsonl && sha256sum corpus_v3.jsonl'

echo "[6/9] Sanity-anchor (d=32x3L, 200 step) via remote-script..."
cat > "$LOCAL_DIR/run_sanity_remote.sh" <<'SH_EOF'
#!/bin/bash
set -uo pipefail
cd /workspace/anima
export PYTHONUNBUFFERED=1
python3 train_d768x12l_tension.py --mode sanity --corpus corpus_v3.jsonl --out-dir out_sanity --steps 200 2>&1 | tee sanity.log
SH_EOF
chmod +x "$LOCAL_DIR/run_sanity_remote.sh"
$SCP "$LOCAL_DIR/run_sanity_remote.sh" "root@$SH:/workspace/anima/run_sanity_remote.sh"
$SSH "bash /workspace/anima/run_sanity_remote.sh" 2>&1 | tee "$LOCAL_DIR/sanity_remote.log" || true

echo "[7/9] MAIN fire d=768 n_layer=12 from-scratch DD155 hybrid LR, $STEPS steps..."
cat > "$LOCAL_DIR/run_main_remote.sh" <<SH_EOF
#!/bin/bash
set -uo pipefail
cd /workspace/anima
export PYTHONUNBUFFERED=1
nvidia-smi --query-gpu=utilization.gpu,memory.used --format=csv -l 30 > gpu_util.log 2>&1 &
SMI=\$!
python3 train_d768x12l_tension.py --mode main --corpus corpus_v3.jsonl --out-dir out_main --steps $STEPS 2>&1 | tee fire.log
kill \$SMI 2>/dev/null || true
echo DONE_MARKER rc=\$?
SH_EOF
chmod +x "$LOCAL_DIR/run_main_remote.sh"
$SCP "$LOCAL_DIR/run_main_remote.sh" "root@$SH:/workspace/anima/run_main_remote.sh"
$SSH "bash /workspace/anima/run_main_remote.sh" 2>&1 | tee "$LOCAL_DIR/fire.log" || true

echo "[8/9] Verify result.json + SAVE_POD auto-promote + pull retry >=5..."
SAVED=$($SSH 'test -f /workspace/anima/out_main/result.json && echo SAVED' 2>/dev/null || true)
if [ "$SAVED" = "SAVED" ]; then
  echo "  result.json present -> SAVE_POD=1 auto-promote"
  export SAVE_POD=1
  mkdir -p "$LOCAL_DIR/out_main" "$LOCAL_DIR/out_sanity"
  PULL_OK=0
  for i in 1 2 3 4 5; do
    echo "  pull attempt $i/5..."
    $SCP "root@$SH:/workspace/anima/out_main/result.json" "$LOCAL_DIR/out_main/" 2>&1 | tail -3 || { echo "  result.json pull fail try $i"; sleep 60; continue; }
    $SCP "root@$SH:/workspace/anima/out_sanity/result.json" "$LOCAL_DIR/out_sanity/" 2>&1 | tail -3 || true
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
  if [ "$PULL_OK" = "1" ]; then
    if [ -f "$LOCAL_DIR/out_main/ckpt_d768x12l_final.pt" ]; then
      echo "  ckpt sha256: $(shasum -a 256 "$LOCAL_DIR/out_main/ckpt_d768x12l_final.pt" | awk '{print $1}')"
      echo "  ckpt size: $(stat -f%z "$LOCAL_DIR/out_main/ckpt_d768x12l_final.pt") bytes"
      echo "  PULL SUCCESS -> safe to destroy"
      export SAVE_POD=0
    else
      echo "  ckpt file missing locally despite PULL_OK? retaining pod"
      export SAVE_POD=1
    fi
  else
    echo "  ALL 5 pull attempts FAILED — SAVE_POD=1 RETAIN for manual recovery"
    echo "  MANUAL: scp -i $SSH_KEY -P $SP root@$SH:/workspace/anima/out_main/ckpt_d768x12l_final.pt $LOCAL_DIR/out_main/"
    export SAVE_POD=1
  fi
else
  echo "  ERROR: result.json NOT present — SAVE_POD=1 retain for manual recovery"
  echo "  MANUAL: ssh -i $SSH_KEY -p $SP root@$SH"
  export SAVE_POD=1
fi

echo "[9/9] Done. teardown via trap (SAVE_POD=${SAVE_POD})."
date -u
ls -la "$LOCAL_DIR/out_main/" 2>/dev/null || true
