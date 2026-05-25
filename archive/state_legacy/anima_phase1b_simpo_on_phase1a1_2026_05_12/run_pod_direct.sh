#!/usr/bin/env bash
# Direct run on already-running Vast.ai pod 36570949 @ ssh5.vast.ai:10948
# (Skip search/create; just upload + train + bench + pull + destroy)
set -euo pipefail

STATE="${STATE:-$HOME/core/anima/state/anima_phase1b_simpo_on_phase1a1_2026_05_12}"
PHASE1A1_CKPT="$HOME/core/anima/state/anima_phase1a1_color_cosmology_2026_05_12/ckpts/ckpt_phase1a1_sft.pt"
ENGINE_AG="$HOME/core/anima/training/engine_a_g_arch.py"
SSH_KEY="$HOME/.vast/ssh/vast-key"

INSTANCE_ID=36570949
SSH_HOST=ssh5.vast.ai
SSH_PORT=10948
DPH=0.29

export VAST_API_KEY=$(/Users/ghost/core/secret/bin/secret get vast.api_key)

POD_SSH="ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -i $SSH_KEY -p $SSH_PORT root@$SSH_HOST"
POD_SCP="scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -i $SSH_KEY -P $SSH_PORT"

trap "echo '[trap] destroying instance $INSTANCE_ID'; /Users/ghost/.local/bin/vastai destroy instance $INSTANCE_ID || true" EXIT

echo "=== [1/6] Setup pod dirs + verify GPU ==="
$POD_SSH "mkdir -p /workspace/anima/training /workspace/anima/data /workspace/anima/ckpts /workspace/anima/output && nvidia-smi -L"

echo "=== [2/6] Upload files ==="
$POD_SCP "$ENGINE_AG" "root@$SSH_HOST:/workspace/anima/training/"
$POD_SCP "$PHASE1A1_CKPT" "root@$SSH_HOST:/workspace/anima/ckpts/ckpt_phase1a1_sft.pt"
$POD_SCP "$STATE/preference_pairs.jsonl" "root@$SSH_HOST:/workspace/anima/data/"
$POD_SCP "$STATE/train_phase1b_simpo.py" "root@$SSH_HOST:/workspace/anima/"
$POD_SCP "$STATE/v58_4mode_eval.py" "root@$SSH_HOST:/workspace/anima/"

echo "=== [3/6] Sanity import ==="
$POD_SSH "cd /workspace/anima && python3 -c 'import sys; sys.path.insert(0, \"training\"); from engine_a_g_arch import EngineAGModel, EngineAGConfig; print(\"engine_a_g OK\")'"

echo "=== [4/6] SimPO train (500 steps, beta=0.05 gamma=0.3 w=0.9->1.0) ==="
$POD_SSH "cd /workspace/anima && python3 train_phase1b_simpo.py \
  --base-ckpt /workspace/anima/ckpts/ckpt_phase1a1_sft.pt \
  --pref-pairs /workspace/anima/data/preference_pairs.jsonl \
  --output /workspace/anima/output \
  --steps 500 --bsz 4 --grad-accum 4 --max-len 192 \
  --lr 5e-6 --beta 0.05 --gamma 0.3 \
  --w-start 0.9 --w-end 1.0 --warmup 25 \
  --cost-cap-usd 0.50 --cost-per-hr $DPH 2>&1 | tee /workspace/anima/train.log"

echo "=== [5/6] V5.8 4-mode bench ==="
$POD_SSH "cd /workspace/anima && python3 v58_4mode_eval.py \
  --ckpt /workspace/anima/output/ckpt_phase1b_simpo_on_phase1a1.pt \
  --output /workspace/anima/v58_4mode_result.json \
  --substrate-id phase1b_simpo_on_phase1a1 2>&1 | tee /workspace/anima/v58.log"

echo "=== [6/6] Pull artifacts ==="
mkdir -p "$STATE/output"
$POD_SCP "root@$SSH_HOST:/workspace/anima/output/ckpt_phase1b_simpo_on_phase1a1.pt" "$STATE/output/" || true
$POD_SCP "root@$SSH_HOST:/workspace/anima/output/meta.json" "$STATE/output/" || true
$POD_SCP "root@$SSH_HOST:/workspace/anima/v58_4mode_result.json" "$STATE/"
$POD_SCP "root@$SSH_HOST:/workspace/anima/train.log" "$STATE/"
$POD_SCP "root@$SSH_HOST:/workspace/anima/v58.log" "$STATE/"

echo "=== DESTROY ==="
/Users/ghost/.local/bin/vastai destroy instance $INSTANCE_ID
trap - EXIT

echo "DONE. Artifacts in $STATE"
echo "Result summary:"
/usr/bin/python3 -c "
import json
d = json.load(open('$STATE/v58_4mode_result.json'))
for mode, s in d['summary'].items():
    print(f'  {mode}: {s[\"n_pass\"]}/5 {s[\"verdict\"]}')
"
