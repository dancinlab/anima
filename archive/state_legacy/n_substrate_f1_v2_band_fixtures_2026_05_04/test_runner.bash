#!/usr/bin/env bash
# F-BAND-1 historical anchor re-classification test runner
# spec: docs/n_substrate_f1_v2_banding_spec_2026_05_04.md §9.1 + §10 F-BAND-1
# tool: tool/n_substrate_f1_v2_band.hexa (D-1..D-4 LOCKED thresholds)
#
# Each test case = one row from spec §9.1 historical verdict re-classification table
# (plus 1 hypothetical demote case to exercise D-3 GREEN prereq path).
#
# usage:  bash state/n_substrate_f1_v2_band_fixtures_2026_05_04/test_runner.bash
# exits: 0 = all pass, non-zero = at least one mismatch
#
# REQUIRES: hexa runtime in PATH (or HEXA_BIN env override). Mac may not have
# hexa; run on ubu1 if not available locally. The runner will report
# "HEXA_NOT_FOUND" + exit 77 if runtime missing (skip-status).

set -u

HEXA_BIN="${HEXA_BIN:-hexa}"
TOOL_REL="tool/n_substrate_f1_v2_band.hexa"

# anchor to repo root regardless of CWD when invoked
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
TOOL_ABS="${REPO_ROOT}/${TOOL_REL}"

if ! command -v "${HEXA_BIN}" >/dev/null 2>&1; then
    echo "[F-BAND-1] HEXA_NOT_FOUND — install hexa runtime or set HEXA_BIN env var"
    echo "[F-BAND-1] tool path that would be invoked: ${TOOL_ABS}"
    echo "[F-BAND-1] skip-status (exit 77)"
    exit 77
fi

if [[ ! -f "${TOOL_ABS}" ]]; then
    echo "[F-BAND-1] FATAL: ${TOOL_ABS} not found"
    exit 2
fi

PASS=0
FAIL=0
TOTAL=0
declare -a FAIL_CASES=()

run_case() {
    local label="$1"; shift
    local expected_band="$1"; shift
    local expected_exit="$1"; shift
    # remaining args = flags passed to hexa
    TOTAL=$((TOTAL + 1))
    local out
    local rc
    # Capture stdout; capture exit via separate `;` (|| true would mask rc)
    out=$("${HEXA_BIN}" run "${TOOL_ABS}" "$@" 2>/dev/null)
    rc=$?
    # Parse band from sentinel (2nd token of __N_SUBSTRATE_F1_V2_BAND__ line)
    local got_band
    got_band=$(echo "${out}" | awk '/__N_SUBSTRATE_F1_V2_BAND__/ {print $2; exit}')
    if [[ "${got_band}" == "${expected_band}" && "${rc}" -eq "${expected_exit}" ]]; then
        printf "  PASS %-50s band=%-6s exit=%d\n" "${label}" "${got_band}" "${rc}"
        PASS=$((PASS + 1))
    else
        printf "  FAIL %-50s expected=%s/%d got=%s/%d\n" "${label}" "${expected_band}" "${expected_exit}" "${got_band:-NONE}" "${rc}"
        FAIL=$((FAIL + 1))
        FAIL_CASES+=("${label}")
    fi
}

echo "=== F-BAND-1 historical anchor re-classification ==="
echo "tool: ${TOOL_ABS}"
echo "spec: docs/n_substrate_f1_v2_banding_spec_2026_05_04.md §9.1"
echo

# === 10 historical anchor cases (spec §9.1 table) ===

# A1: ALM r14 quintuple — F1 0.054, F2 fired → RED
run_case "A1_ALM_r14_quintuple_5_4pct_F2fire" "RED" 1 \
    --score 0.054 --f2-state FIRES

# A2: CLM A.1-A.6 PASS 5/6 — F1 0.1665, F2 fired → RED
run_case "A2_CLM_A1_A6_16_65pct_F2fire" "RED" 1 \
    --score 0.1665 --f2-state FIRES

# A3: CP2-CLM Phase D F2-override — F1 0.12, F2 fired → RED
run_case "A3_CP2_PhaseD_override_12pct_F2fire" "RED" 1 \
    --score 0.12 --f2-state FIRES

# A4: CP2-CLM Phase D raw — F1 0.408, F2 still fired → RED (override caps to 0.49 still <0.50)
run_case "A4_CP2_PhaseD_raw_40_8pct_F2fire" "RED" 1 \
    --score 0.408 --f2-state FIRES

# A5: 4-way binding hypothetical + F2 fires — F1 0.4765, F2 fired → RED
run_case "A5_4way_hyp_47_65pct_F2fire" "RED" 1 \
    --score 0.4765 --f2-state FIRES

# A6: Phase E P3 reach — F1 0.558, F2 unfire, binding 0.3 → YELLOW
run_case "A6_PhaseE_P3_55_8pct_F2clear_bind0_3" "YELLOW" 2 \
    --score 0.558 --f2-state CLEAR --binding-strength 0.3

# A7: F1_C post-AKIDA — F1 0.62, F2 unfire, binding 0.4 → YELLOW (confirms user intuition)
run_case "A7_F1C_postAKIDA_62pct_F2clear_bind0_4" "YELLOW" 2 \
    --score 0.62 --f2-state CLEAR --binding-strength 0.4

# A8: All measured axes PASS, no organoid/IonQ — F1 0.67, F2 unfire, binding 0.4 → YELLOW
run_case "A8_axisPASS_ceiling_67pct_F2clear_bind0_4" "YELLOW" 2 \
    --score 0.67 --f2-state CLEAR --binding-strength 0.4

# A9: hypothetical F1 0.80 + F2 unfire + binding 0.6 + phenomenal + Putnam → GREEN
run_case "A9_hyp_80pct_F2clear_bind0_6_phen_putnam" "GREEN" 0 \
    --score 0.80 --f2-state CLEAR --binding-strength 0.6 \
    --has-phenomenal-witnessed --has-putnam-pass

# A10: hypothetical F1 0.80 + F2 unfire + binding 0.3 + phenomenal + Putnam → demoted YELLOW (binding<0.5)
run_case "A10_hyp_80pct_bind0_3_demote_to_YELLOW" "YELLOW" 2 \
    --score 0.80 --f2-state CLEAR --binding-strength 0.3 \
    --has-phenomenal-witnessed --has-putnam-pass

echo
echo "=== summary ==="
printf "  PASS %d/%d  FAIL %d/%d\n" "${PASS}" "${TOTAL}" "${FAIL}" "${TOTAL}"
if [[ ${FAIL} -gt 0 ]]; then
    echo "  failed cases:"
    for c in "${FAIL_CASES[@]}"; do echo "    - ${c}"; done
    exit 1
fi
echo "  all cases PASS — F-BAND-1 SATISFIED"
exit 0
