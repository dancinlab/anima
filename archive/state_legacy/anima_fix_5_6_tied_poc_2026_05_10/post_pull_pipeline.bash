#!/bin/bash
# Post-pull pipeline: per-branch v5 probe + cell-pool evidence + summary.
# Run after orchestrator completes ckpt pull.
set -uo pipefail

ANIMA_ROOT="/Users/ghost/core/anima"
STATE_DIR="${ANIMA_ROOT}/state/anima_fix_5_6_tied_poc_2026_05_10"
RESULTS_DIR="${STATE_DIR}/results"
LOG_DIR="${STATE_DIR}/logs"
RUN_LOG="${LOG_DIR}/post_pull.log"

ARCH_PY="${ANIMA_ROOT}/training/engine_a_g_arch.py"
BG_LB_CKPT="${HOME}/.cache/anima/clm_v5_remapped/bg_lb_350m_pretrain/ckpts/step_8000_final.pt"
V5_PROBE="${ANIMA_ROOT}/tool/transient_py/v5_probe_fix_5_6_branch.py"

PY3=/opt/homebrew/bin/python3.real
if [ ! -x "$PY3" ]; then PY3=/usr/bin/python3; fi

log() { echo "[$(date -u +%FT%TZ)] $*" | tee -a "$RUN_LOG"; }

mkdir -p "$LOG_DIR"
log "=== Post-pull pipeline ==="

# Determine ckpt source — emergency or normal
CKPT_DIR="$RESULTS_DIR/ckpts"
if [ ! -d "$CKPT_DIR" ] || [ -z "$(ls "$CKPT_DIR" 2>/dev/null)" ]; then
    CKPT_DIR="$RESULTS_DIR/ckpts_emergency"
fi
log "ckpt source: $CKPT_DIR"
ls -la "$CKPT_DIR" 2>&1 | tee -a "$RUN_LOG"

# Per-branch v5 probe
for branch in a b c; do
    CKPT="$CKPT_DIR/step_1500_branch_${branch}.pt"
    if [ ! -f "$CKPT" ]; then
        log "branch_$branch: ckpt missing ($CKPT) — skipping"
        continue
    fi
    OUT="${ANIMA_ROOT}/state/anima_fix_5_6_tied_poc_${branch}_v5_2026_05_10.json"
    log "=== branch_$branch v5 probe ==="
    "$PY3" "$V5_PROBE" \
        --ckpt "$CKPT" \
        --arch "$ARCH_PY" \
        --baseline-ckpt "$BG_LB_CKPT" \
        --output "$OUT" \
        --device cpu 2>&1 | tee -a "$RUN_LOG"
done

# Summary
log "=== Summary ==="
for branch in a b c; do
    OUT="${ANIMA_ROOT}/state/anima_fix_5_6_tied_poc_${branch}_v5_2026_05_10.json"
    if [ -f "$OUT" ]; then
        log "branch_$branch result: $(grep -E '\"verdict\"|\"PPR_v5_proxy_strict\"|\"MTRP_v5_proxy\"|\"V14_violation\"|\"EMERGE\"' "$OUT" | head -10 | tr -d ' ')"
    fi
done
log "=== Post-pull DONE ==="
