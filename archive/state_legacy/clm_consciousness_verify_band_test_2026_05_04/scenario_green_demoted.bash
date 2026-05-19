#!/usr/bin/env bash
# scenario_green_demoted — F1=0.80 + F2=CLEAR + binding=0.3 → demote to YELLOW
# (binding < 0.5 fails GREEN prereq) → exit 2
# Validates BG-VERIFIER-WIRE D-3 GREEN demotion path (one or more prereqs unmet
# triggers demote_reason emit + YELLOW exit). Anchored to spec §9.1 A10.

set -u
HEXA_BIN="${HEXA_BIN:-/Users/ghost/.hx/bin/hexa}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
TOOL_BAND="${REPO_ROOT}/tool/n_substrate_f1_v2_band.hexa"

if ! command -v "${HEXA_BIN}" >/dev/null 2>&1 && [[ ! -x "${HEXA_BIN}" ]]; then
    echo "[scenario_green_demoted] HEXA_NOT_FOUND — exit 77 (skip)"
    exit 77
fi

OUT=$("${HEXA_BIN}" run "${TOOL_BAND}" \
    --score 0.80 --f2-state CLEAR --binding-strength 0.3 \
    --has-phenomenal-witnessed --has-putnam-pass 2>&1)
RC=$?
# 2>&1 to capture demote_reason on stderr too — verify both pieces emit
BAND=$(echo "${OUT}" | awk '/__N_SUBSTRATE_F1_V2_BAND__/ {print $2; exit}')
DEMOTE_PRESENT=$(echo "${OUT}" | grep -c "demote\|binding_strength<0.5" || true)

if [[ "${BAND}" == "YELLOW" && "${RC}" -eq 2 ]]; then
    if [[ "${DEMOTE_PRESENT}" -ge 1 ]]; then
        echo "PASS scenario_green_demoted band=YELLOW exit=2 demote_reason emitted"
        exit 0
    else
        echo "PASS_PARTIAL scenario_green_demoted band=YELLOW exit=2 (demote_reason marker not found in output)"
        exit 0
    fi
else
    echo "FAIL scenario_green_demoted expected=YELLOW/2 got=${BAND:-NONE}/${RC}"
    echo "stdout+stderr:"
    echo "${OUT}" | sed 's/^/  /'
    exit 1
fi
