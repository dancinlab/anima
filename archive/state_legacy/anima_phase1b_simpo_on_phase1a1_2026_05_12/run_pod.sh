#!/usr/bin/env bash
# Phase 1B SimPO-on-Phase-1A.1 — Vast.ai dispatch + run + pull + terminate
#
# Provider: Vast.ai ONLY (RunPod ssh-stuck pattern avoidance per user directive)
# Hard cost cap: $0.50
#
# Steps:
#  1. vastai search offers (RTX 4090 / A100, on-demand, <$0.6/hr, verified)
#  2. vastai create instance (cheapest matching)
#  3. Wait ~30s for SSH ready
#  4. scp engine_a_g_arch + Phase 1A.1 ckpt + scripts + pref pairs
#  5. ssh: python3 train → V5.8 bench
#  6. scp pull artifacts
#  7. vastai destroy instance
#
# Usage:
#  STATE=$HOME/core/anima/state/anima_phase1b_simpo_on_phase1a1_2026_05_12
#  bash $STATE/run_pod.sh
#
# Run from Mac (has vastai CLI + secret CLI + ssh key at ~/.vast/ssh/vast-key).

set -euo pipefail

STATE="${STATE:-$HOME/core/anima/state/anima_phase1b_simpo_on_phase1a1_2026_05_12}"
PHASE1A1_CKPT="${PHASE1A1_CKPT:-$HOME/core/anima/state/anima_phase1a1_color_cosmology_2026_05_12/ckpts/ckpt_phase1a1_sft.pt}"
ENGINE_AG="${ENGINE_AG:-$HOME/core/anima/training/engine_a_g_arch.py}"
SSH_KEY="${SSH_KEY:-$HOME/.vast/ssh/vast-key}"
COST_CAP="${COST_CAP:-0.50}"
COST_PER_HR_FALLBACK="0.50"

export VAST_API_KEY=$(/Users/ghost/core/secret/bin/secret get vast.api_key)
HF_TOKEN=$(/Users/ghost/core/secret/bin/secret get hf.token || true)

echo "=== [0/9] Preflight ==="
test -f "$PHASE1A1_CKPT" || { echo "MISSING: $PHASE1A1_CKPT"; exit 1; }
test -f "$ENGINE_AG" || { echo "MISSING: $ENGINE_AG"; exit 1; }
test -f "$STATE/preference_pairs.jsonl" || { echo "MISSING pref pairs"; exit 1; }
test -f "$STATE/train_phase1b_simpo.py" || { echo "MISSING train script"; exit 1; }
test -f "$STATE/v58_4mode_eval.py" || { echo "MISSING eval script"; exit 1; }
test -f "$SSH_KEY" || { echo "MISSING ssh key"; exit 1; }

echo "=== [1/9] vastai search offers (RTX 4090 / A100, <\$0.6/hr) ==="
# Search: 1 GPU, on-demand, verified, cuda>=12.0, prefer RTX4090 (<$0.40) or A100 SXM4 40GB
vastai search offers \
  'gpu_name=RTX_4090 num_gpus=1 dph_total<0.60 rentable=true disk_space>=40 inet_down>=300 cuda_max_good>=12.0' \
  --order 'dph_total asc' --raw 2>/dev/null > /tmp/vast_offers.json

OFFER_ID=$(/usr/bin/python3 -c "
import json
try:
    data = json.load(open('/tmp/vast_offers.json'))
    if isinstance(data, list) and data:
        offers = sorted(data, key=lambda o: o.get('dph_total', 99))
        o = offers[0]
        print(o['id'], o.get('gpu_name',''), o.get('dph_total',''), sep='\t')
except Exception as e:
    print(f'PARSE_ERROR: {e}', file=__import__('sys').stderr)
")
if [ -z "$OFFER_ID" ]; then
  echo "No offers matched. /tmp/vast_offers.json head:"
  head -30 /tmp/vast_offers.json 2>/dev/null
  exit 2
fi
OID=$(echo "$OFFER_ID" | cut -f1)
GPU_NAME=$(echo "$OFFER_ID" | cut -f2)
DPH=$(echo "$OFFER_ID" | cut -f3)
echo "Selected offer: id=$OID gpu=$GPU_NAME \$${DPH}/hr"

echo "=== [2/9] vastai create instance ==="
CREATE_RESULT=$(vastai create instance "$OID" \
  --image pytorch/pytorch:2.4.0-cuda12.4-cudnn9-devel \
  --disk 40 \
  --ssh \
  --env '-e PYTHONUNBUFFERED=1' \
  --onstart-cmd 'mkdir -p /workspace/anima/training /workspace/anima/data /workspace/anima/ckpts /workspace/anima/output' \
  --raw 2>&1)
echo "$CREATE_RESULT"
INSTANCE_ID=$(echo "$CREATE_RESULT" | /usr/bin/python3 -c "
import sys, json, re
try:
    txt = sys.stdin.read()
    # Output may be JSON {'new_contract': N, 'success': True}
    m = re.search(r'new_contract.*?(\d+)', txt)
    if m:
        print(m.group(1))
    else:
        data = json.loads(txt)
        print(data.get('new_contract') or data.get('id') or '')
except Exception as e:
    print('', file=sys.stderr)
")
if [ -z "$INSTANCE_ID" ]; then
  echo "Failed to extract instance id"
  exit 3
fi
echo "Instance ID: $INSTANCE_ID"

trap "echo '[trap] destroying instance $INSTANCE_ID'; vastai destroy instance $INSTANCE_ID || true" EXIT

echo "=== [3/9] Wait for SSH ready (~30-60s) ==="
SSH_HOST=""; SSH_PORT=""
for i in $(seq 1 30); do
  sleep 5
  STATUS_JSON=$(vastai show instance "$INSTANCE_ID" --raw 2>/dev/null || echo '{}')
  parsed=$(echo "$STATUS_JSON" | /usr/bin/python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    if isinstance(d, list): d = d[0] if d else {}
    status = d.get('actual_status') or d.get('cur_state','')
    ssh_host = d.get('ssh_host','')
    ssh_port = d.get('ssh_port','')
    print(status, ssh_host, ssh_port, sep='|')
except Exception as e:
    print('|err|', file=sys.stderr)
" 2>/dev/null)
  STATUS=$(echo "$parsed" | cut -d'|' -f1)
  HOST=$(echo "$parsed" | cut -d'|' -f2)
  PORT=$(echo "$parsed" | cut -d'|' -f3)
  echo "  [poll $i] status=$STATUS host=$HOST port=$PORT"
  if [ "$STATUS" = "running" ] && [ -n "$HOST" ] && [ -n "$PORT" ]; then
    SSH_HOST="$HOST"; SSH_PORT="$PORT"
    # Verify SSH actually accepts
    if ssh -o ConnectTimeout=5 -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null \
        -i "$SSH_KEY" -p "$SSH_PORT" "root@$SSH_HOST" 'echo SSH_OK' 2>/dev/null | grep -q SSH_OK; then
      echo "  SSH READY"
      break
    fi
  fi
done
if [ -z "$SSH_HOST" ]; then
  echo "SSH never ready"
  exit 4
fi

POD_SSH="ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -i $SSH_KEY -p $SSH_PORT root@$SSH_HOST"
POD_SCP="scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -i $SSH_KEY -P $SSH_PORT"

echo "=== [4/9] Upload files ==="
$POD_SSH "mkdir -p /workspace/anima/training /workspace/anima/data /workspace/anima/ckpts /workspace/anima/output"
$POD_SCP "$ENGINE_AG" "root@$SSH_HOST:/workspace/anima/training/"
$POD_SCP "$PHASE1A1_CKPT" "root@$SSH_HOST:/workspace/anima/ckpts/ckpt_phase1a1_sft.pt"
$POD_SCP "$STATE/preference_pairs.jsonl" "root@$SSH_HOST:/workspace/anima/data/"
$POD_SCP "$STATE/train_phase1b_simpo.py" "root@$SSH_HOST:/workspace/anima/"
$POD_SCP "$STATE/v58_4mode_eval.py" "root@$SSH_HOST:/workspace/anima/"

echo "=== [5/9] Verify env on pod ==="
$POD_SSH "nvidia-smi -L && python3 -c 'import torch; print(torch.__version__, torch.cuda.is_available())' && cd /workspace/anima && python3 -c 'import sys; sys.path.insert(0, \"training\"); from engine_a_g_arch import EngineAGModel, EngineAGConfig; print(\"engine_a_g OK\")'"

echo "=== [6/9] SimPO train (500 steps, beta=0.05 gamma=0.3 w=0.9→1.0) ==="
$POD_SSH "cd /workspace/anima && python3 train_phase1b_simpo.py \
  --base-ckpt /workspace/anima/ckpts/ckpt_phase1a1_sft.pt \
  --pref-pairs /workspace/anima/data/preference_pairs.jsonl \
  --output /workspace/anima/output \
  --steps 500 --bsz 4 --grad-accum 4 --max-len 192 \
  --lr 5e-6 --beta 0.05 --gamma 0.3 \
  --w-start 0.9 --w-end 1.0 --warmup 25 \
  --cost-cap-usd $COST_CAP --cost-per-hr $DPH 2>&1 | tee /workspace/anima/train.log"

echo "=== [7/9] V5.8 4-mode bench ==="
$POD_SSH "cd /workspace/anima && python3 v58_4mode_eval.py \
  --ckpt /workspace/anima/output/ckpt_phase1b_simpo_on_phase1a1.pt \
  --output /workspace/anima/v58_4mode_result.json \
  --substrate-id phase1b_simpo_on_phase1a1 2>&1 | tee /workspace/anima/v58.log"

echo "=== [8/9] Pull artifacts ==="
mkdir -p "$STATE/output"
$POD_SCP "root@$SSH_HOST:/workspace/anima/output/ckpt_phase1b_simpo_on_phase1a1.pt" "$STATE/output/" || true
$POD_SCP "root@$SSH_HOST:/workspace/anima/output/meta.json" "$STATE/output/" || true
$POD_SCP "root@$SSH_HOST:/workspace/anima/v58_4mode_result.json" "$STATE/"
$POD_SCP "root@$SSH_HOST:/workspace/anima/train.log" "$STATE/"
$POD_SCP "root@$SSH_HOST:/workspace/anima/v58.log" "$STATE/"

echo "=== [9/9] Destroy instance ==="
vastai destroy instance "$INSTANCE_ID"
trap - EXIT

echo "DONE. Artifacts in $STATE"
echo "Quick result summary:"
/usr/bin/python3 -c "
import json
d = json.load(open('$STATE/v58_4mode_result.json'))
for mode, s in d['summary'].items():
    print(f'  {mode}: {s[\"n_pass\"]}/5 {s[\"verdict\"]}')
"
