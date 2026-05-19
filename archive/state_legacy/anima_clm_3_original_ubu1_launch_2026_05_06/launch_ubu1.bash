#!/usr/bin/env bash
# anima CLM-3-original byte-level 55M ubu1 RTX 5070 launch (BG-EV spec)
# $0 hardware (owned), 5-10 days wall-clock, sm_120 torch 2.11.0+cu128
# Spec ref: docs/anima_clm_3_original_byte_level_redesign_spec_2026_05_05.md
# bash 3.2 compatible (mac default + ubu1 bash 5)
set -uo pipefail

err()  { printf '[beta-ubu1 ERR] %s\n' "$*" >&2; exit 1; }
log()  { printf '[beta-ubu1    ] %s\n' "$*"; }

# === PRE-FLIGHT (4 mandatory checks for $0 hardware) ===
log "PRE-FLIGHT 1/4: ubu1 ssh reachability"
if ! ssh -o ConnectTimeout=5 ubu1 'echo ok' 2>/dev/null | grep -q ok; then
    err "GATE 1 FAIL: ubu1 ssh unreachable (check ~/.ssh/config Host ubu1)"
fi
log "  GATE 1 PASS"

log "PRE-FLIGHT 2/4: venv_orchestrator present"
ssh ubu1 'ls /home/aiden/venv_orchestrator/bin/python 2>/dev/null' | grep -q python || \
    err "GATE 2 FAIL: /home/aiden/venv_orchestrator/bin/python missing"
log "  GATE 2 PASS"

log "PRE-FLIGHT 3/4: torch 2.11.0+cu128 + cuda available"
TORCH_CHECK=$(ssh ubu1 '/home/aiden/venv_orchestrator/bin/python -c "import torch; print(torch.__version__, torch.cuda.is_available())" 2>&1' | tail -1)
echo "  ubu1 torch report: $TORCH_CHECK"
case "$TORCH_CHECK" in
    *2.11.0*True*) log "  GATE 3 PASS" ;;
    *2.11.0*)      err "GATE 3 FAIL: torch 2.11.0 OK but cuda unavailable" ;;
    *)             err "GATE 3 FAIL: torch != 2.11.0+cu128 (got: $TORCH_CHECK)" ;;
esac

log "PRE-FLIGHT 4/4: anima repo on ubu1"
REPO_PATH=$(ssh ubu1 'if [ -d /home/aiden/core/anima ]; then echo /home/aiden/core/anima; elif [ -d /home/aiden/anima ]; then echo /home/aiden/anima; else echo MISSING; fi' 2>/dev/null)
[ "$REPO_PATH" = "MISSING" ] && err "GATE 4 FAIL: anima repo not found on ubu1"
log "  GATE 4 PASS (repo at $REPO_PATH)"

# === Falsifier sign-off (same 5 as H100 path) ===
log ""
log "5 falsifier sign-off (CLM-3-original byte-level redesign):"
echo "  F-CLM3-orig-1: spec_match (vocab=256 byte / d=768 / L=12 / fib growth 1,1,2,3,5,8,13,21,32)"
echo "  F-CLM3-orig-2: Phase 2 dialogue CE drop >= 30%"
echo "  F-CLM3-orig-3: Phi_real >= 11"
echo "  F-CLM3-orig-4: KO 5-prompt >= 3/5 coherent"
echo "  F-CLM3-orig-5: phi_star NO_FLIP"
read -rp "Type 'FALSIFIER-LOCK-UBU1' to acknowledge: " FCONFIRM
[ "$FCONFIRM" != "FALSIFIER-LOCK-UBU1" ] && err "GATE 5 FAIL: falsifier sign-off declined"
log "  GATE 5 PASS"

log "All 5 gates PASS. Emitting launch sequence..."

# === SSH + train fire (manual emit, user fires step 4) ===
RUN_NAME="clm3-original-byte-55m-ubu1-$(date +%Y%m%d-%H%M%S)"
log "Run name: $RUN_NAME"

LOG_DIR="/Users/ghost/core/anima/state/anima_clm_3_original_ubu1_launch_2026_05_06"
LOG="$LOG_DIR/launch.log"
mkdir -p "$LOG_DIR"

log "Step 1: corpus sync (run on mac)"
cat <<RSYNC_CMD
  rsync -avz --progress \\
    /Users/ghost/core/anima/data/corpus_mix_70wiki_30dialogue.txt \\
    ubu1:$REPO_PATH/data/
RSYNC_CMD

log "Step 2: launch on ubu1 (paste into separate shell after rsync OK)"
cat <<UBU_LAUNCH
  ssh ubu1 'cd $REPO_PATH && nohup /home/aiden/venv_orchestrator/bin/python \\
    ready/training/train_clm.py \\
    --vocab-size 256 \\
    --max-cells 32 \\
    --d-model 768 \\
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
    --output-dir runs/$RUN_NAME \\
    --falsifier-eval-every 10000 \\
    > runs/$RUN_NAME.log 2>&1 &'
UBU_LAUNCH

log "Step 3: monitor (every 30min)"
echo "  bash $LOG_DIR/monitor_ubu1.bash $RUN_NAME"

# audit trail
echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] UBU1_LAUNCH_INITIATED run=$RUN_NAME wall_estimate=5-10d gates=5/5_PASS" >> "$LOG"
log "Launch sequence emitted. Audit trail: $LOG"
log "NOTE: actual ssh+train fire is MANUAL (5 falsifier gates already locked)"
