#!/usr/bin/env bash
# scenario_green_full_prereq — F1=0.80 + F2=CLEAR + binding=0.6 + phenomenal +
# putnam_pass + no falsifier → GREEN, exit 0
# Validates BG-VERIFIER-WIRE D-3 GREEN tier ALL prereqs satisfied + D-4 GREEN
# exit code (=0 — UNIX 0=success inverted intentionally per spec §11). Anchored
# to spec §9.1 A9 hypothetical anchor.

set -u
HEXA_BIN="${HEXA_BIN:-/Users/ghost/.hx/bin/hexa}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
TOOL_BAND="${REPO_ROOT}/tool/n_substrate_f1_v2_band.hexa"

if ! command -v "${HEXA_BIN}" >/dev/null 2>&1 && [[ ! -x "${HEXA_BIN}" ]]; then
    echo "[scenario_green_full_prereq] HEXA_NOT_FOUND — exit 77 (skip)"
    exit 77
fi

OUT=$("${HEXA_BIN}" run "${TOOL_BAND}" \
    --score 0.80 --f2-state CLEAR --binding-strength 0.6 \
    --has-phenomenal-witnessed --has-putnam-pass 2>/dev/null)
RC=$?
BAND=$(echo "${OUT}" | awk '/__N_SUBSTRATE_F1_V2_BAND__/ {print $2; exit}')

if [[ "${BAND}" == "GREEN" && "${RC}" -eq 0 ]]; then
    echo "PASS scenario_green_full_prereq band=GREEN exit=0"
    exit 0
else
    echo "FAIL scenario_green_full_prereq expected=GREEN/0 got=${BAND:-NONE}/${RC}"
    echo "stdout:"
    echo "${OUT}" | sed 's/^/  /'
    exit 1
fi
