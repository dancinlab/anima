#!/usr/bin/env bash
# run_phase_b.sh — wrapper for the §24 SPONTANEOUS Phase B first bounded-run.
#
# Emits:
#   audit_log.jsonl  (append-only via audit_logger.py Python sidecar)
#   result.json      (4-axis verdict)
#   run.log          (stdout + stderr from the run)
#
# $0 — Mac CPU local, no GPU, no dispatch.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$HERE"

# Make sure prior audit log (if any) is rotated by run_bounded.py itself,
# so we don't pollute the JSONL append-only invariant verification.

# Mode default: test (0.1s think interval, full run < 10s wall).
MODE="${MODE:-test}"
N_MAX="${N_MAX:-20}"
T_MAX="${T_MAX:-600}"

echo "─── §24 SPONTANEOUS Phase B first bounded-run ──────────────────"
echo "  mode             = ${MODE}"
echo "  n_max_steps      = ${N_MAX}"
echo "  t_max_wall_sec   = ${T_MAX}"
echo "  ANIMA_SPONT_OFF  = ${ANIMA_SPONT_OFF:-<unset>}"
echo "  audit_log        = ${HERE}/audit_log.jsonl"
echo "  result_json      = ${HERE}/result.json"
echo "─────────────────────────────────────────────────────────────────"

python3 run_bounded.py \
    --mode "${MODE}" \
    --n-max "${N_MAX}" \
    --t-max "${T_MAX}" \
    --audit-log "${HERE}/audit_log.jsonl" \
    --result-json "${HERE}/result.json" \
    2>&1 | tee "${HERE}/run.log"

echo "─── battery (B-PHASE-B-RUN-1..5) ───────────────────────────────"
python3 blue_falsifier_phase_b_run.py 2>&1 | tee -a "${HERE}/run.log"
echo "─── done ───────────────────────────────────────────────────────"
