#!/usr/bin/env bash
# n_substrate_putnam_check.hexa unit test runner (raw#9 — bash thin wrapper to
# invoke hexa runtime; not a python script).
#
# Verifies F-PUTNAM-1 (reproducibility — re-runs each fixture 3× and asserts
# identical exit codes) AND the basic 3-tier exit code mapping (PASS=0,
# PARTIAL=1, FAIL=2).
#
# Usage:
#   bash state/n_substrate_putnam_check_fixtures_2026_05_04/test_runner.bash
# Optional env:
#   HEXA_BIN  override hexa binary path (default: `hexa` on PATH or
#             /Users/<user>/core/hexa-lang/hexa)
#
# raw#10 honest C3: this runner asserts decision-rule + exit-code mapping in
# fixture mode only. It does NOT validate real .roadmap.n_substrate evidence
# parsing — that path is exercised by the production verifier when invoked
# without --selftest and with a real roadmap file.
set -u

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
TOOL="$ROOT/tool/n_substrate_putnam_check.hexa"
FIXTURES_DIR="$ROOT/state/n_substrate_putnam_check_fixtures_2026_05_04"

HEXA="${HEXA_BIN:-}"
if [[ -z "$HEXA" ]]; then
  if command -v hexa >/dev/null 2>&1; then
    HEXA="$(command -v hexa)"
  elif [[ -x "$HOME/core/hexa-lang/hexa" ]]; then
    HEXA="$HOME/core/hexa-lang/hexa"
  else
    echo "FAIL: hexa binary not found (set HEXA_BIN or install hexa-lang)" >&2
    exit 4
  fi
fi

declare -a SCENARIOS=("scenario_pass.json:0:PASS" "scenario_partial.json:1:PARTIAL" "scenario_fail.json:2:FAIL")
PASS_CT=0
FAIL_CT=0
TOTAL=0

echo "── n_substrate_putnam_check fixture runner ──"
echo "  hexa=$HEXA"
echo "  tool=$TOOL"
echo "  fixtures_dir=$FIXTURES_DIR"
echo ""

for entry in "${SCENARIOS[@]}"; do
  IFS=":" read -r fname expected_exit expected_verdict <<< "$entry"
  fpath="$FIXTURES_DIR/$fname"
  for run in 1 2 3; do
    TOTAL=$((TOTAL+1))
    out="$("$HEXA" run "$TOOL" --roadmap "$fpath" --bin "$ROOT/tool" --no-cache --quiet 2>&1)"
    rc=$?
    sentinel_line="$(echo "$out" | grep '^__N_SUBSTRATE_PUTNAM__' | tail -1)"
    if [[ "$rc" == "$expected_exit" ]]; then
      PASS_CT=$((PASS_CT+1))
      echo "  [OK] $fname run=$run exit=$rc (expected=$expected_exit) sentinel='$sentinel_line'"
    else
      FAIL_CT=$((FAIL_CT+1))
      echo "  [FAIL] $fname run=$run exit=$rc (expected=$expected_exit) sentinel='$sentinel_line'"
      echo "    full_output:"
      echo "$out" | sed 's/^/      /'
    fi
  done
done

echo ""
echo "summary: pass=$PASS_CT fail=$FAIL_CT total=$TOTAL"
echo "F-PUTNAM-1 reproducibility: $( [[ $FAIL_CT -eq 0 ]] && echo PASS || echo FAIL )"

if [[ $FAIL_CT -gt 0 ]]; then
  exit 1
fi
exit 0
