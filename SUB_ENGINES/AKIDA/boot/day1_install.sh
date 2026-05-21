#!/usr/bin/env bash
# AUX/AKIDA/boot/day1_install.sh — Pi 5 + AKD1000 fresh-boot installer.
#
# Day 1 outcome (per README §5):
#   - MetaTF SDK install (`pip install akida`)
#   - Akida Cloud trial 신청 ($1/day) — manual step, logged here
#   - `python -c "import akida; print(akida.__version__)"` PASS
#
# On Mac local (dry-run): falls through to mock fallback path.
set -eu

HERE="$(cd "$(dirname "$0")" && pwd)/.."
LOG_DIR="${HERE}/state/day1_install_$(date +%Y_%m_%d)"
mkdir -p "${LOG_DIR}"

echo "=== Day 1: install ==="
echo "[INFO] HERE=$HERE"
echo "[INFO] LOG_DIR=$LOG_DIR"

# 1. host probe -----------------------------------------------------------
{
    uname -a
    echo "---"
    if command -v lscpu >/dev/null 2>&1; then lscpu | head -10; fi
    if command -v sw_vers >/dev/null 2>&1; then sw_vers; fi
    echo "---"
    python3 --version
} >"${LOG_DIR}/host_probe.txt" 2>&1
echo "[OK] host probe → ${LOG_DIR}/host_probe.txt"

# 2. brew / apt (Pi 5 expects apt; Mac dry-run brew) ----------------------
if command -v apt-get >/dev/null 2>&1; then
    echo "[STEP] apt python3.11 + pip"
    sudo apt-get update -y >>"${LOG_DIR}/apt.log" 2>&1 || true
    sudo apt-get install -y python3.11 python3-pip >>"${LOG_DIR}/apt.log" 2>&1 || true
elif command -v brew >/dev/null 2>&1; then
    echo "[INFO] brew detected (Mac local) — dry-run, no apt"
else
    echo "[WARN] neither apt nor brew — manual Python install required"
fi

# 3. pip install akida (real HW SDK) --------------------------------------
echo "[STEP] pip install akida (optional)"
if [ -n "${VIRTUAL_ENV:-}" ] || [ -n "${CONDA_PREFIX:-}" ]; then
    PIP_FLAGS=""
else
    PIP_FLAGS="--break-system-packages"
fi
python3 -m pip install "akida>=2.0" ${PIP_FLAGS} >>"${LOG_DIR}/pip_akida.log" 2>&1 || {
    echo "[WARN] akida SDK install failed — mock fallback will be used"
}

# 4. INSTALL.sh chain ------------------------------------------------------
echo "[STEP] chain to AUX/AKIDA/INSTALL.sh"
bash "${HERE}/INSTALL.sh" 2>&1 | tee "${LOG_DIR}/install.log"

# 5. import probe ----------------------------------------------------------
python3 - <<'PY' | tee -a "${LOG_DIR}/import_probe.txt"
try:
    import akida
    print(f"VERIFY akida HW path: version={akida.__version__}")
except ImportError:
    print("VERIFY mock fallback path active (Mac local pre-arrival)")
PY

# 6. cloud-trial reminder --------------------------------------------------
cat <<EOF | tee "${LOG_DIR}/cloud_trial_reminder.txt"
[REMINDER] Akida Cloud trial — manual step, see:
  - AUX/AKIDA/README.md §5 Day 1
  - AUX/hw/PHASE_2_CLOUD_TRIAL.md §2.1
  - AUX/docs/akida_cloud_signup_guide.md
EOF

echo "=== Day 1: install OK ==="
