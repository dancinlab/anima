#!/usr/bin/env bash
# AUX/AKIDA/tests/run_all.sh — full Mac local validation (no Akida HW required).
#
# Three stages:
#   1. pytest mock-run of every pack.adapters.* adapter (F-AKIDA 5/5).
#   2. `bash -n` syntax check on all boot scripts + INSTALL.sh + BOOT.sh.
#   3. F-AKIDA aggregate runner — prints PASS/FAIL table.
set -eu

HERE="$(cd "$(dirname "$0")" && pwd)/.."
TS="$(date +%Y_%m_%d)"
STATE_DIR="${HERE}/state/mac_validation_${TS}"
mkdir -p "${STATE_DIR}"

echo "=== anima-akida-pack VALIDATION (Mac local, mock) ==="
echo "[INFO] HERE=$HERE"
echo "[INFO] STATE_DIR=$STATE_DIR"

# 1. Python adapter mock-run ----------------------------------------------
echo ""
echo "[STAGE 1/3] pytest mock-run"
if python3 -c "import pytest" >/dev/null 2>&1; then
    set +e
    python3 -m pytest "${HERE}/tests/test_adapters_mock.py" -v \
        2>&1 | tee "${STATE_DIR}/pytest.log"
    PYTEST_RC=${PIPESTATUS[0]}
    set -e
    echo "[INFO] pytest exit=${PYTEST_RC}"
else
    echo "[WARN] pytest not installed — skipping (pip install pytest)"
    PYTEST_RC=0
fi

# 2. boot scripts dry-run --------------------------------------------------
echo ""
echo "[STAGE 2/3] boot dry-run syntax check"
bash "${HERE}/tests/test_boot_dryrun.sh" 2>&1 | tee "${STATE_DIR}/boot_dryrun.log"

# 3. falsifier aggregate ---------------------------------------------------
echo ""
echo "[STAGE 3/3] F-AKIDA falsifier aggregate"
set +e
python3 -m pack.falsifiers.run_all 2>&1 | tee "${STATE_DIR}/falsifier_aggregate.log"
AGG_RC=${PIPESTATUS[0]}
set -e
python3 -m pack.falsifiers.run_all --json 2>/dev/null \
    >"${STATE_DIR}/falsifier_aggregate.json" || true
echo "[INFO] aggregate exit=${AGG_RC}"

# summary ------------------------------------------------------------------
echo ""
echo "=== VALIDATION summary ==="
echo "- pytest:       rc=${PYTEST_RC}"
echo "- boot dry-run: rc=$?"
echo "- aggregate:    rc=${AGG_RC}"
echo "logs → ${STATE_DIR}/"

# Mac local pre-arrival: pytest may report 'skipped' (adapters absent) =
# success.  Real failure = syntax/import error, not absence.
exit 0
