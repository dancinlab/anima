#!/usr/bin/env bash
# scenario_red_f2_fire — F1=0.40 + F2=FIRES → band=RED, exit 1
# Validates BG-VERIFIER-WIRE D-4 RED exit code semantics + D-2 F2 override cap
# (raw 0.40 with F2 FIRES → capped to 0.49 ceiling → RED region).
#
# This fixture invokes the band hexa hook directly with simulated check
# results that the verifier orchestrator would produce. Honest C3 #5: this is
# shape-only verification (band hook contract), not full verifier orchestrator
# end-to-end (which reads real .roadmap.* state).

set -u
HEXA_BIN="${HEXA_BIN:-/Users/ghost/.hx/bin/hexa}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
TOOL_BAND="${REPO_ROOT}/tool/n_substrate_f1_v2_band.hexa"

if ! command -v "${HEXA_BIN}" >/dev/null 2>&1 && [[ ! -x "${HEXA_BIN}" ]]; then
    echo "[scenario_red_f2_fire] HEXA_NOT_FOUND — exit 77 (skip)"
    exit 77
fi

OUT=$("${HEXA_BIN}" run "${TOOL_BAND}" \
    --score 0.40 --f2-state FIRES 2>/dev/null)
RC=$?
BAND=$(echo "${OUT}" | awk '/__N_SUBSTRATE_F1_V2_BAND__/ {print $2; exit}')

if [[ "${BAND}" == "RED" && "${RC}" -eq 1 ]]; then
    echo "PASS scenario_red_f2_fire band=RED exit=1"
    exit 0
else
    echo "FAIL scenario_red_f2_fire expected=RED/1 got=${BAND:-NONE}/${RC}"
    echo "stdout:"
    echo "${OUT}" | sed 's/^/  /'
    exit 1
fi
