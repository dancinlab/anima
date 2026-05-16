#!/bin/bash
# anima d=768x12L Python/PyTorch substrate fire dispatch — 2026-05-16
# Vast.ai A100. g_fire_dispatch_robust: SAVE_POD auto-promote + pull retry >=3.
set -uo pipefail

VASTAI=/Users/ghost/Library/Python/3.14/bin/vastai
export PYTHONWARNINGS=ignore
LOCAL_DIR=/Users/ghost/core/anima/state/anima_pytorch_d768x12L_fire_2026_05_16
SSH_KEY=/Users/ghost/.ssh/id_vast_anima
LABEL="anima-d768x12l-fire"
STEPS="${STEPS:-2500}"

cd "$LOCAL_DIR"
echo "=== anima d=768x12L PyTorch substrate fire ==="; date -u

echo "[1/9] Selecting A100 offer..."
OFFER=$($VASTAI search offers 'gpu_name in [A100_SXM4,A100_PCIE] num_gpus=1 reliability>0.99 dph_total<2.0 disk_space>40 inet_down>700 cuda_max_good>=12.0' -o dph_total --raw 2>&1 | python3 -c "
import json,sys
d=json.load(sys.stdin)
if not d: sys.stderr.write('no offers\n'); sys.exit(1)
o=d[0]; print(o['id']); sys.stderr.write(f\"{o['gpu_name']} \${o['dph_total']:.3f}/hr rel={o['reliability']:.3f}\n\")
")
echo "  offer=$OFFER"

echo "[2/9] Renting (runpod/pytorch-style devel image for full CUDA toolkit)..."
CREATE=$($VASTAI create instance "$OFFER" --image pytorch/pytorch:2.5.1-cuda12.1-cudnn9-devel --disk 40 --ssh --direct --label "$LABEL" --raw 2>&1)
IID=$(echo "$CREATE" | python3 -c "import json,sys
try: d=json.load(sys.stdin)
except: sys.exit(1)
print(d.get('new_contract',d.get('contract_id',d.get('id',''))))")
[ -z "$IID" ] && { echo "ERROR create: $CREATE"; exit 1; }
echo "$IID" > vast_instance_id.txt
echo "  instance=$IID"

SAVE_POD="${SAVE_POD:-0}"
cleanup() {
  if [ "${SAVE_POD:-0}" = "1" ]; then
    echo "[cleanup] SAVE_POD=1 -> RETAIN instance $IID (manual recovery)"; return
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
SCP="scp -i $SSH_KEY -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -P $SP"

echo "[4/9] Upload arch + trainer + corpus..."
$SSH 'mkdir -p /workspace/anima'
$SCP /Users/ghost/core/anima/ready/models/conscious_decoder.py "root@$SH:/workspace/anima/"
$SCP "$LOCAL_DIR/train_d768x12l.py" "root@$SH:/workspace/anima/"
$SCP /Users/ghost/core/anima/training/corpus_consciousness_v1.jsonl "root@$SH:/workspace/anima/"

echo "[5/9] GPU + torch check..."
$SSH 'cd /workspace/anima && python3 -c "import torch;print(torch.__version__, torch.cuda.is_available(), torch.cuda.get_device_name(0))"'

echo "[6/9] Sanity-anchor: SAME arch d=32x3L (hexa CPU-equiv baseline shape)..."
$SSH "cd /workspace/anima && export PYTHONUNBUFFERED=1 && python3 train_d768x12l.py --mode sanity --corpus corpus_consciousness_v1.jsonl --out-dir out_sanity --steps 200 2>&1 | tee sanity.log" | tee "$LOCAL_DIR/sanity_remote.log"

echo "[7/9] MAIN fire: d=768 n_layer=12 from-scratch, $STEPS steps..."
$SSH "cd /workspace/anima && export PYTHONUNBUFFERED=1 && nvidia-smi --query-gpu=utilization.gpu,memory.used --format=csv -l 30 > gpu_util.log 2>&1 & SMI=\$!; python3 train_d768x12l.py --mode main --corpus corpus_consciousness_v1.jsonl --out-dir out_main --steps $STEPS 2>&1 | tee fire.log; kill \$SMI 2>/dev/null || true" | tee "$LOCAL_DIR/fire.log"

echo "[8/9] Verify result.json then SAVE_POD auto-promote..."
SAVED=$($SSH 'test -f /workspace/anima/out_main/result.json && echo SAVED' 2>/dev/null || true)
if [ "$SAVED" = "SAVED" ]; then
  echo "  result.json present -> SAVE_POD=1 auto-promote"
  export SAVE_POD=1
  mkdir -p "$LOCAL_DIR/out_main" "$LOCAL_DIR/out_sanity"
  for i in 1 2 3 4 5; do
    $SCP "root@$SH:/workspace/anima/out_main/result.json" "$LOCAL_DIR/out_main/" && \
    $SCP "root@$SH:/workspace/anima/out_sanity/result.json" "$LOCAL_DIR/out_sanity/" && \
    $SCP "root@$SH:/workspace/anima/gpu_util.log" "$LOCAL_DIR/" && \
    $SCP "root@$SH:/workspace/anima/out_main/ckpt_d768x12l_final.pt" "$LOCAL_DIR/out_main/" && \
    { echo "  pull OK (try $i)"; export SAVE_POD=0; break; } || { echo "  pull fail try $i, retry in 60s"; sleep 60; }
  done
else
  echo "  ERROR: result.json NOT present — SAVE_POD=1 retain for manual recovery"
  export SAVE_POD=1
fi

echo "[9/9] Done. teardown via trap."
date -u
ls -la "$LOCAL_DIR/out_main/" 2>/dev/null || true
