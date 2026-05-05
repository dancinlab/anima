#!/usr/bin/env bash
# scenario_yellow_f2_clear — F1=0.62 + F2=CLEAR + binding=0.4 → YELLOW, exit 2
# Validates BG-VERIFIER-WIRE D-1 YELLOW band threshold (0.50 ≤ score < 0.75)
# + D-4 YELLOW exit code (=2). Anchored to spec §9.1 A7 (post-AKIDA F1_C 62%).

set -u
HEXA_BIN="${HEXA_BIN:-/Users/ghost/.hx/bin/hexa}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
TOOL_BAND="${REPO_ROOT}/tool/n_substrate_f1_v2_band.hexa"

if ! command -v "${HEXA_BIN}" >/dev/null 2>&1 && [[ ! -x "${HEXA_BIN}" ]]; then
    echo "[scenario_yellow_f2_clear] HEXA_NOT_FOUND — exit 77 (skip)"
    exit 77
fi

OUT=$("${HEXA_BIN}" run "${TOOL_BAND}" \
    --score 0.62 --f2-state CLEAR --binding-strength 0.4 2>/dev/null)
RC=$?
BAND=$(echo "${OUT}" | awk '/__N_SUBSTRATE_F1_V2_BAND__/ {print $2; exit}')

if [[ "${BAND}" == "YELLOW" && "${RC}" -eq 2 ]]; then
    echo "PASS scenario_yellow_f2_clear band=YELLOW exit=2"
    exit 0
else
    echo "FAIL scenario_yellow_f2_clear expected=YELLOW/2 got=${BAND:-NONE}/${RC}"
    echo "stdout:"
    echo "${OUT}" | sed 's/^/  /'
    exit 1
fi
