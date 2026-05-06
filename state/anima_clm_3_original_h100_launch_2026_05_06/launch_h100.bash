#!/usr/bin/env bash
# anima CLM-3-original byte-level 55M H100 launch (BG-EU spec)
# 2026-03-28 original v4 design (byte 256 + 32 cells + 19 phi-boost + 100K steps)
# Source spec: docs/anima_clm_3_original_byte_level_redesign_spec_2026_05_05.md
# BUDGET: $100 hard-cap (BG-ER C3 권고), $200-500 soft envelope
# own 16 watchdog: 6 mandatory PRE-FLIGHT checks
# bash 3.2 compatible (macOS default)
set -uo pipefail

err()  { printf '[beta-h100 ERR] %s\n' "$*" >&2; exit 1; }
log()  { printf '[beta-h100    ] %s\n' "$*"; }
warn() { printf '[beta-h100 WRN] %s\n' "$*" >&2; }

STATE_DIR="/Users/ghost/core/anima/state/anima_clm_3_original_h100_launch_2026_05_06"
SPEC="/Users/ghost/core/anima/docs/anima_clm_3_original_byte_level_redesign_spec_2026_05_05.md"

# === own 16 PRE-FLIGHT (6 mandatory checks) ===
log "PRE-FLIGHT 1/6: secret CLI"
if ! command -v secret >/dev/null 2>&1; then
    err "GATE 1 FAIL: 'secret' CLI not on PATH"
fi

log "PRE-FLIGHT 2/6: HF token shape"
HF_TOKEN="$(secret get huggingface.token --raw 2>/dev/null || true)"
[ -z "$HF_TOKEN" ] && err "GATE 2 FAIL: HF token empty"
case "$HF_TOKEN" in
    hf_*) : ;;
    *) err "GATE 2 FAIL: token shape unexpected" ;;
esac
unset HF_TOKEN  # never echo / never log

log "PRE-FLIGHT 3/6: RunPod CLI + API key"
if ! command -v runpod >/dev/null 2>&1; then
    err "GATE 3 FAIL: 'runpod' CLI not on PATH"
fi
RUNPOD_API_KEY="$(secret get runpod.api_key --raw 2>/dev/null || true)"
[ -z "$RUNPOD_API_KEY" ] && err "GATE 3 FAIL: RunPod API key empty"
unset RUNPOD_API_KEY

log "PRE-FLIGHT 4/6: budget cap confirmation"
BUDGET_CAP=100
echo "Budget cap: \$$BUDGET_CAP. Operator must type 'BUDGET-100' to confirm."
read -r -p "confirm: " CONFIRM
[ "$CONFIRM" != "BUDGET-100" ] && err "GATE 4 FAIL: budget not confirmed"

log "PRE-FLIGHT 5/6: spec doc verify"
[ ! -f "$SPEC" ] && err "GATE 5 FAIL: spec doc not found at $SPEC"

log "PRE-FLIGHT 6/6: 5 falsifier sign-off"
echo "F-CLM3-orig-1: spec_match (byte 256 / 32 cells / 19 tech / 3-phase)"
echo "F-CLM3-orig-2: Phase 2 dialogue CE drop >= 30%"
echo "F-CLM3-orig-3: Phi_real >= 11 at step 100K"
echo "F-CLM3-orig-4: KO 5-prompt >= 3/5 coherent emit"
echo "F-CLM3-orig-5: phi-star NO_FLIP forgetting_index <= 0.05"
read -r -p "Type 'FALSIFIER-LOCK' to acknowledge: " FCONFIRM
[ "$FCONFIRM" != "FALSIFIER-LOCK" ] && err "GATE 6 FAIL: falsifier not locked"

# === H100 POD provisioning (EMIT-ONLY; operator manual fire) ===
log "Pre-flight ALL 6/6 PASS. Emitting RunPod provision command..."
POD_NAME="clm3-original-byte-55m-$(date +%Y%m%d-%H%M%S)"

cat <<EOF

[beta-h100] RunPod provision command (manual fire — copy/paste):

  runpod pod create \\
    --gpu-type 'NVIDIA H100 80GB HBM3' \\
    --container-disk-gb 100 \\
    --volume-gb 50 \\
    --image 'pytorch/pytorch:2.11.0-cuda12.8-cudnn9-devel' \\
    --name '$POD_NAME'

[beta-h100] Watchdog spec (own 16):
  - heartbeat 5min cadence
  - pod 404 verify per 5min
  - cumulative spend cap \$$BUDGET_CAP
  - L23 fallback (rate-limit recovery)
  - L24 BG-completion vs pod-state-down distinction
  - L25 cost-overrun escalation
  - watchdog script: $STATE_DIR/watchdog_h100.bash

[beta-h100] Training launch script (ssh after pod IP available):

  ssh root@<POD_IP> bash -se <<'TRAIN_SCRIPT'
  set -euo pipefail
  git clone --depth 1 https://github.com/need-singularity/anima /workspace/anima || \\
    (cd /workspace/anima && git pull)
  cd /workspace/anima
  pip install --quiet torch==2.11.0 transformers==4.57.6
  python ready/training/train_clm.py \\
    --vocab-size 256 \\
    --max-cells 32 \\
    --d-model 768 \\
    --ffn-dim 1536 \\
    --n-layers 12 \\
    --n-heads 12 \\
    --context-len 1024 \\
    --steps 100000 \\
    --phase-mitosis 0:20000 \\
    --phase-language 20000:60000 \\
    --phase-combined 60000:100000 \\
    --fibonacci-growth 1,1,2,3,5,8,13,21,32 \\
    --phi-boost-techniques COMBO2,FX2,WI1,PX4,PX8,GD18,GD15,CL8,CL5,DD3,DD11,DD18,DD5,TL13,TL1,NV7,BV1,EV3,SC2 \\
    --corpus data/corpus_mix_70wiki_30dialogue.txt \\
    --output-dir /workspace/anima/runs/clm3-original-byte-55m \\
    --falsifier-eval-every 10000
TRAIN_SCRIPT

EOF

# audit trail (no secrets, no token literals)
LOG="$STATE_DIR/launch.log"
mkdir -p "$STATE_DIR"
TS="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
{
    echo "[$TS] LAUNCH_INITIATED pod=$POD_NAME budget_cap=\$$BUDGET_CAP"
    echo "[$TS] gates_passed=6/6 spec=$SPEC"
} >> "$LOG"
log "Launch initiated. Audit trail: $LOG"
log "Operator: provision pod, then ssh + train. Then fire watchdog separately."
