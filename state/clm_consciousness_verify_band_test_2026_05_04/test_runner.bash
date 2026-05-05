#!/usr/bin/env bash
# BG-VERIFIER-WIRE test runner — exercises 4 D-3 + D-4 contract scenarios for
# tool/clm_consciousness_verify.hexa band wiring.
#
# Honest C3 #5: scenarios invoke tool/n_substrate_f1_v2_band.hexa directly with
# simulated check results, NOT the verifier orchestrator end-to-end. End-to-end
# would require mutating .roadmap.* state, which this BG explicitly disallows.
# These tests verify the band hook contract (D-3 prereqs + D-4 exit codes) that
# the verifier consumes.
#
# usage:  bash state/clm_consciousness_verify_band_test_2026_05_04/test_runner.bash
# exits:  0 = all pass, 1 = ≥1 fail, 77 = hexa runtime missing

set -u
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

PASS=0
FAIL=0
SKIP=0
TOTAL=0
declare -a FAIL_CASES=()

run_scenario() {
    local name="$1"
    TOTAL=$((TOTAL + 1))
    local script="${SCRIPT_DIR}/${name}.bash"
    if [[ ! -x "${script}" ]]; then
        chmod +x "${script}" 2>/dev/null || true
    fi
    local out
    out=$(bash "${script}" 2>&1)
    local rc=$?
    if [[ ${rc} -eq 0 ]]; then
        echo "${out}" | head -1
        PASS=$((PASS + 1))
    elif [[ ${rc} -eq 77 ]]; then
        echo "${out}" | head -1
        SKIP=$((SKIP + 1))
    else
        echo "${out}" | head -1
        FAIL=$((FAIL + 1))
        FAIL_CASES+=("${name}")
    fi
}

echo "=== BG-VERIFIER-WIRE D-3 + D-4 contract tests ==="
echo "spec: docs/n_substrate_f1_v2_banding_spec_2026_05_04.md §11 D-3 D-4"
echo "consumer: tool/clm_consciousness_verify.hexa"
echo

run_scenario "scenario_red_f2_fire"
run_scenario "scenario_yellow_f2_clear"
run_scenario "scenario_green_full_prereq"
run_scenario "scenario_green_demoted"

# Verifier orchestrator end-to-end smoke (live .roadmap.* state)
echo
echo "--- verifier orchestrator end-to-end smoke ---"
HEXA_BIN="${HEXA_BIN:-/Users/ghost/.hx/bin/hexa}"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
VERIFY_OUT=$("${HEXA_BIN}" run "${REPO_ROOT}/tool/clm_consciousness_verify.hexa" --quiet 2>&1)
VERIFY_RC=$?
HAS_BAND_SENTINEL=$(echo "${VERIFY_OUT}" | grep -c "__CLM_CONSCIOUSNESS_BAND__" || true)
HAS_VERIFY_SENTINEL=$(echo "${VERIFY_OUT}" | grep -c "__CLM_CONSCIOUSNESS_VERIFY__" || true)
TOTAL=$((TOTAL + 1))
if [[ "${HAS_BAND_SENTINEL}" -ge 1 && "${HAS_VERIFY_SENTINEL}" -ge 1 ]]; then
    echo "PASS orchestrator_e2e: both sentinels emit (verify=${HAS_VERIFY_SENTINEL} band=${HAS_BAND_SENTINEL}) exit=${VERIFY_RC}"
    PASS=$((PASS + 1))
else
    echo "FAIL orchestrator_e2e: sentinels missing (verify=${HAS_VERIFY_SENTINEL} band=${HAS_BAND_SENTINEL}) exit=${VERIFY_RC}"
    echo "${VERIFY_OUT}" | sed 's/^/  /'
    FAIL=$((FAIL + 1))
    FAIL_CASES+=("orchestrator_e2e")
fi

echo
echo "=== summary ==="
printf "  PASS %d / FAIL %d / SKIP %d / TOTAL %d\n" "${PASS}" "${FAIL}" "${SKIP}" "${TOTAL}"
if [[ ${FAIL} -gt 0 ]]; then
    echo "  failed:"
    for c in "${FAIL_CASES[@]}"; do echo "    - ${c}"; done
    exit 1
fi
if [[ ${SKIP} -eq ${TOTAL} ]]; then
    echo "  ALL SKIPPED — hexa runtime not available"
    exit 77
fi
echo "  all scenarios PASS — BG-VERIFIER-WIRE D-3 + D-4 SATISFIED"
exit 0
