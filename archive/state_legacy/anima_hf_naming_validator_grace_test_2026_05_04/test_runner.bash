#!/usr/bin/env bash
# anima/HF naming validator §3.7 grace-period harness
# spec: docs/anima_hf_naming_convention_mk2_spec_2026_05_03.md §3.7 + §8.1
# tool: tool/hf_upload_mk2.hexa  (validate-naming verb, patched 2026-05-04 by BG-NAMING-VALIDATOR-PATCH)
# sibling: docs/anima_hf_naming_clm_amendment_landed_2026_05_04.ai.md (cond.2 caveat C2)
#
# 4 unit tests:
#   T1: clm-v4-mk2-v1            → PASS via §3.7 grace (legacy `mk\d+-v\d+` variant)
#   T2: clm-v4-base              → PASS via existing strict enum (`base` is allowed prefix)
#   T3: clm-v4-garbagestage      → FAIL (over-permissive guard — neither strict enum nor §3.7 regex)
#   T4: clm-v4-mk1-v0            → PASS via regex generalization (`mk\d+-v\d+`)
#
# usage: bash state/anima_hf_naming_validator_grace_test_2026_05_04/test_runner.bash
# exits: 0 = all 4 PASS, 1 = ≥1 mismatch, 77 = hexa runtime not found (skip-status)
#
# REQUIRES: hexa runtime in PATH (or HEXA_BIN env override). Mac may not have
# hexa locally; runner emits HEXA_NOT_FOUND + exit 77 in that case.
# HEXA_LOCAL=1 fallback: per BG-MODEL-CARD discovery, some Mac envs ship a
# limited hexa binary that supports `validate-naming` directly. The runner
# probes for both invocation forms.

set -u

HEXA_BIN="${HEXA_BIN:-hexa}"
TOOL_REL="tool/hf_upload_mk2.hexa"

# HEXA_LOCAL=1 forces local-mode dispatch (route=local reason=hexa_local_set).
# Required for this hook because remote-mode shifts argv such that argv[2] = the
# script path (not the verb), which causes `--validate-naming` to be parsed as
# argv[3], breaking the verb-dispatch in tool/hf_upload_mk2.hexa main() (line 874).
# Mac local hexa interpreter handles this fine; remote pool does not.
# Discovered 2026-05-04 by BG-FIX-COMPLETE-DOCS during NAMING-VALIDATOR harness wiring.
export HEXA_LOCAL="${HEXA_LOCAL:-1}"

# anchor to repo root regardless of CWD
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
TOOL_ABS="${REPO_ROOT}/${TOOL_REL}"

if ! command -v "${HEXA_BIN}" >/dev/null 2>&1; then
    echo "[NAMING-VALIDATOR-GRACE] HEXA_NOT_FOUND — install hexa runtime or set HEXA_BIN env var"
    echo "[NAMING-VALIDATOR-GRACE] tool path that would be invoked: ${TOOL_ABS}"
    echo "[NAMING-VALIDATOR-GRACE] skip-status (exit 77)"
    exit 77
fi

if [[ ! -f "${TOOL_ABS}" ]]; then
    echo "[NAMING-VALIDATOR-GRACE] FATAL: ${TOOL_ABS} not found"
    exit 2
fi

PASS=0
FAIL=0
TOTAL=0
declare -a FAIL_CASES=()

# Invocation helpers ---------------------------------------------------------
#
# We exercise the --validate-naming verb (line ~891 of tool/hf_upload_mk2.hexa).
# The hexa hook signature is:
#   hexa run tool/hf_upload_mk2.hexa --validate-naming <org/name>
# It prints either `OK` (PASS) or `FAIL: <reason>` (reject) on stdout, then
# emits a sentinel `__ANIMA_HF_UPLOAD_MK2__ PASS|FAIL`. §3.7 grace fallback
# additionally prints `WARN: §3.7 grace-period: ...` on stdout BEFORE the OK
# line (raw#10 honest C3: stdout-warn blurs PASS contract — caller must check
# final sentinel, not first line).
#
# HEXA_LOCAL=1 fallback: per BG-MODEL-CARD discovery, some Mac envs hexa-resolve
# to remote ubu1; the runner accepts that transparently because both forms use
# the same `hexa run` invocation (no Mac-only second form needed for this verb).
#
# Repo names are validated as <org>/<name>; tests use `need-singularity` org
# (anima canonical HF org per BG-NAMING-AMEND).

ORG="need-singularity"

invoke_validate() {
    local name="$1"
    local repo="${ORG}/${name}"
    "${HEXA_BIN}" run "${TOOL_ABS}" --validate-naming "${repo}" 2>&1
}

# Result classification ------------------------------------------------------
# Returns one of: PASS, PASS_WITH_WARNING, FAIL
# Looks at:
#   __ANIMA_HF_UPLOAD_MK2__ PASS|FAIL  (canonical sentinel — line ~887/895)
#   FAIL: <reason>                       (reject reason — line 261-339)
#   WARN: §3.7 grace-period: ...         (grace fallback — line 334)
classify_output() {
    local out="$1"
    local final_sentinel
    final_sentinel=$(echo "${out}" | awk '/__ANIMA_HF_UPLOAD_MK2__/ {print $2; exit}')
    local has_warn=0
    if echo "${out}" | grep -q "WARN: §3.7 grace-period"; then
        has_warn=1
    fi
    if [[ "${final_sentinel}" == "PASS" ]]; then
        if [[ ${has_warn} -eq 1 ]]; then
            echo "PASS_WITH_WARNING"
        else
            echo "PASS"
        fi
        return
    fi
    if [[ "${final_sentinel}" == "FAIL" ]]; then
        echo "FAIL"
        return
    fi
    # Fallback heuristics if sentinel missing
    if echo "${out}" | grep -q "FAIL:"; then
        echo "FAIL"
        return
    fi
    if echo "${out}" | grep -qE "^OK$"; then
        if [[ ${has_warn} -eq 1 ]]; then
            echo "PASS_WITH_WARNING"
        else
            echo "PASS"
        fi
        return
    fi
    # Unknown shape — treat as FAIL for safety
    echo "FAIL"
}

run_case() {
    local label="$1"
    local name="$2"
    local expected="$3"   # PASS | PASS_WITH_WARNING | FAIL
    TOTAL=$((TOTAL + 1))
    local out
    out=$(invoke_validate "${name}")
    local got
    got=$(classify_output "${out}")
    if [[ "${got}" == "${expected}" ]]; then
        printf "  PASS %-50s name=%-30s expected=%s got=%s\n" \
            "${label}" "${name}" "${expected}" "${got}"
        PASS=$((PASS + 1))
    else
        printf "  FAIL %-50s name=%-30s expected=%s got=%s\n" \
            "${label}" "${name}" "${expected}" "${got}"
        echo "    raw_output: ${out}"
        FAIL=$((FAIL + 1))
        FAIL_CASES+=("${label}")
    fi
}

echo "=== anima/HF naming validator §3.7 grace-period harness ==="
echo "tool: ${TOOL_ABS}"
echo "spec: docs/anima_hf_naming_convention_mk2_spec_2026_05_03.md §3.7 + §8.1"
echo "grace_expiry: 2026-06-02"
echo

# T1: §3.7 grace fallback — legacy `mk\d+-v\d+` variant slot
run_case "T1_clm_v4_mk2_v1_grace_pass" \
    "clm-v4-mk2-v1" \
    "PASS_WITH_WARNING"

# T2: existing strict enum — `base` is allowed stage prefix per §3.5
run_case "T2_clm_v4_base_strict_enum_pass" \
    "clm-v4-base" \
    "PASS"

# T3: over-permissive guard — neither strict enum nor §3.7 regex
run_case "T3_clm_v4_garbagestage_strict_fail" \
    "clm-v4-garbagestage" \
    "FAIL"

# T4: regex generalization — `mk1-v0` also admitted by §3.7 regex
run_case "T4_clm_v4_mk1_v0_grace_pass" \
    "clm-v4-mk1-v0" \
    "PASS_WITH_WARNING"

echo
echo "=== summary ==="
printf "  PASS %d/%d  FAIL %d/%d\n" "${PASS}" "${TOTAL}" "${FAIL}" "${TOTAL}"
if [[ ${FAIL} -gt 0 ]]; then
    echo "  failed cases:"
    for c in "${FAIL_CASES[@]}"; do echo "    - ${c}"; done
    exit 1
fi
echo "  all cases PASS — §3.7 grace-period harness SATISFIED"
exit 0
