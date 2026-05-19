#!/usr/bin/env bash
# tool/own_16_preflight.hexa selftest runner
#
# Parses the canonical __OWN_16_PREFLIGHT__ verdict line from STDOUT
# (hexa runner does not propagate main() return as POSIX exit code, so we
# assert on the verdict line marker instead — same convention as
# tool/h100_cost_watchdog.hexa selftest scenarios).
#
# Exit 0 = all 3 scenarios match expected verdicts
# Exit 1 = one or more mismatches

set -u

REPO_ROOT="${REPO_ROOT:-/Users/ghost/core/anima}"
HEXA="${HEXA:-hexa}"
TOOL="$REPO_ROOT/tool/own_16_preflight.hexa"
TEST_DIR="$REPO_ROOT/state/own_16_preflight_test_2026_05_05"

S1_PATH="$TEST_DIR/scenario_full_pass.txt"
S2_PATH="$TEST_DIR/scenario_partial_fail.txt"
S3_PATH="$TEST_DIR/scenario_zero_cost_optional.txt"

PASS_COUNT=0
FAIL_COUNT=0
RESULTS=()

assert_verdict() {
    local label="$1"
    local prompt_path="$2"
    local expect_verdict="$3"
    local expect_score="$4"

    local out
    out=$("$HEXA" run "$TOOL" --validate-prompt "$prompt_path" 2>/dev/null)
    local marker_line
    marker_line=$(echo "$out" | grep '^__OWN_16_PREFLIGHT__' | head -1)

    if [[ -z "$marker_line" ]]; then
        echo "  [$label] FAIL — no __OWN_16_PREFLIGHT__ marker emitted"
        FAIL_COUNT=$((FAIL_COUNT + 1))
        RESULTS+=("{\"label\":\"$label\",\"status\":\"FAIL\",\"reason\":\"no_marker\",\"got\":\"\"}")
        return
    fi

    local got_verdict
    got_verdict=$(echo "$marker_line" | awk '{print $2}')
    local got_score
    got_score=$(echo "$marker_line" | grep -oE 'score=[0-9]+/6' | head -1)

    if [[ "$got_verdict" == "$expect_verdict" && "$got_score" == "score=$expect_score" ]]; then
        echo "  [$label] PASS — verdict=$got_verdict $got_score"
        PASS_COUNT=$((PASS_COUNT + 1))
        RESULTS+=("{\"label\":\"$label\",\"status\":\"PASS\",\"verdict\":\"$got_verdict\",\"score\":\"$got_score\"}")
    else
        echo "  [$label] FAIL — got verdict=$got_verdict $got_score, expected verdict=$expect_verdict score=$expect_score"
        FAIL_COUNT=$((FAIL_COUNT + 1))
        RESULTS+=("{\"label\":\"$label\",\"status\":\"FAIL\",\"verdict\":\"$got_verdict\",\"score\":\"$got_score\",\"expect_verdict\":\"$expect_verdict\",\"expect_score\":\"score=$expect_score\"}")
    fi
}

echo "── own_16_preflight test_runner.bash ──"
echo "tool: $TOOL"
echo "test_dir: $TEST_DIR"
echo ""

# Bootstrap the scenarios first (selftest writes them as a side-effect)
"$HEXA" run "$TOOL" --selftest >/dev/null 2>&1 || true

echo ""
echo "─ scenario assertions ─"
assert_verdict "S1_full_pass"          "$S1_PATH" "PASS" "6/6"
assert_verdict "S2_partial_fail_at_5"  "$S2_PATH" "FAIL" "4/6"
assert_verdict "S3_zero_cost_optional" "$S3_PATH" "PASS" "0/6"

echo ""
echo "summary: $PASS_COUNT/3 PASS, $FAIL_COUNT FAIL"

# emit JSON summary for verdict.json consumption
{
    echo "{"
    echo "  \"ts_utc\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\","
    echo "  \"pass_count\": $PASS_COUNT,"
    echo "  \"fail_count\": $FAIL_COUNT,"
    echo "  \"results\": ["
    for i in "${!RESULTS[@]}"; do
        if [[ $i -gt 0 ]]; then echo "    ,"; fi
        echo "    ${RESULTS[$i]}"
    done
    echo "  ]"
    echo "}"
} > "$TEST_DIR/test_runner_results.json"

if [[ $FAIL_COUNT -gt 0 ]]; then
    exit 1
fi
exit 0
