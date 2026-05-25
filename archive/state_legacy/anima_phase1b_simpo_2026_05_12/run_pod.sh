#!/usr/bin/env bash
# Phase 1B SimPO on pod — full pipeline: upload → train → bench → pull → terminate
# Run from Mac side after pod SSH is ready.

set -e

POD_IP="103.207.149.116"
POD_PORT="13909"
POD_ID="97wjr7cb7gdt3n"
SSH_KEY="$HOME/.runpod/ssh/RunPod-Key-Go"
SSH_OPTS="-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -i $SSH_KEY"
SCP_OPTS="-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -i $SSH_KEY -P $POD_PORT"

POD_SSH="ssh $SSH_OPTS -p $POD_PORT root@$POD_IP"

LOCAL_STATE="$HOME/core/anima/state/anima_phase1b_simpo_2026_05_12"
PHASE1A_CKPT="$HOME/core/anima/state/anima_phase1a_alt_2026_05_12/ckpts/ckpt_phase1a_sft.pt"

echo "[1/8] Setup pod dirs..."
$POD_SSH "mkdir -p /workspace/anima/training /workspace/anima/data /workspace/anima/ckpts /workspace/anima/output && nvidia-smi -L && python3 -c 'import torch; print(\"torch\", torch.__version__, \"cuda\", torch.cuda.is_available())'"

echo "[2/8] Upload engine_a_g_arch.py..."
scp $SCP_OPTS "$HOME/core/anima/training/engine_a_g_arch.py" root@$POD_IP:/workspace/anima/training/

echo "[3/8] Upload Phase 1A ckpt (570MB)..."
scp $SCP_OPTS "$PHASE1A_CKPT" root@$POD_IP:/workspace/anima/ckpts/ckpt_phase1a_sft.pt

echo "[4/8] Upload preference pairs + scripts..."
scp $SCP_OPTS "$LOCAL_STATE/preference_pairs.jsonl" root@$POD_IP:/workspace/anima/data/
scp $SCP_OPTS "$LOCAL_STATE/train_phase1b_simpo.py" root@$POD_IP:/workspace/anima/
scp $SCP_OPTS "$LOCAL_STATE/v58_4mode_bench.py" root@$POD_IP:/workspace/anima/

echo "[5/8] Verify torch on pod..."
$POD_SSH "cd /workspace/anima && python3 -c 'import sys; sys.path.insert(0, \"training\"); from engine_a_g_arch import EngineAGModel, EngineAGConfig; print(\"engine_a_g import OK\")'"

echo "[6/8] Train SimPO (600 steps, cost cap \$8)..."
$POD_SSH "cd /workspace/anima && python3 train_phase1b_simpo.py \
  --phase1a-ckpt /workspace/anima/ckpts/ckpt_phase1a_sft.pt \
  --pref-pairs /workspace/anima/data/preference_pairs.jsonl \
  --output /workspace/anima/output \
  --steps 600 --bsz 4 --grad-accum 4 --max-len 160 \
  --lr 5e-6 --beta 2.5 --gamma 1.4 \
  --cost-cap-usd 8.0 --cost-per-hr 2.99 2>&1 | tee /workspace/anima/train.log"

echo "[7/8] V5.8 4-mode bench..."
$POD_SSH "cd /workspace/anima && python3 v58_4mode_bench.py \
  --ckpt /workspace/anima/output/ckpt_phase1b_simpo.pt \
  --out /workspace/anima/v58_4mode_result.json 2>&1 | tee /workspace/anima/v58.log"

echo "[8/8] Pull artifacts..."
mkdir -p "$LOCAL_STATE/ckpts"
scp $SCP_OPTS root@$POD_IP:/workspace/anima/output/ckpt_phase1b_simpo.pt "$LOCAL_STATE/ckpts/"
scp $SCP_OPTS root@$POD_IP:/workspace/anima/output/meta.json "$LOCAL_STATE/" || true
scp $SCP_OPTS root@$POD_IP:/workspace/anima/v58_4mode_result.json "$LOCAL_STATE/"
scp $SCP_OPTS root@$POD_IP:/workspace/anima/train.log "$LOCAL_STATE/"
scp $SCP_OPTS root@$POD_IP:/workspace/anima/v58.log "$LOCAL_STATE/"

echo "DONE. Artifacts in $LOCAL_STATE"
echo "Pod ID for manual terminate: $POD_ID"
