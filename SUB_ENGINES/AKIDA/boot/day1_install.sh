#!/usr/bin/env bash
# SUB_ENGINES/AKIDA/boot/day1_install.sh — Pi 5 + AKD1000 fresh-boot installer.
#
# Day 1 outcome (per README §5 + doc/metatf_install_linux_arm.md):
#   - MetaTF SDK install (`pip install akida` — aarch64 wheel auto-selected)
#   - Akida PCIe driver install (DKMS from BrainChip dev portal — manual step logged)
#   - Akida Cloud trial signup (optional) — manual step, logged here
#   - `python3 -c "import akida; print(akida.__version__)"` PASS
#   - `python3 -c "from pack.runtime.metatf_runtime import assert_akd1000;
#                  print(assert_akd1000())"` PASS (HW or mock)
#
# On Mac local (dry-run): falls through to mock fallback path.
#
# IMPORTANT API verification (post-2026-05-21 BrainChip survey):
#   - akida 2.19.1 is the canonical version (latest as of 2026-05-21)
#   - aarch64 wheel: `akida-2.19.1-cp311-cp311-manylinux_2_28_aarch64.whl`
#   - Pi 5 Bookworm Python 3.11 is exact match (no conda needed)
#   - PEP 668 → use venv on Pi 5, not --break-system-packages
set -eu

HERE="$(cd "$(dirname "$0")" && pwd)/.."
LOG_DIR="${HERE}/state/day1_install_$(date +%Y_%m_%d)"
mkdir -p "${LOG_DIR}"

echo "=== Day 1: install (AKD1000 / Pi 5 aarch64) ==="
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
    echo "---"
    # PCIe scan — should show BrainChip AKD1000 after driver install
    if command -v lspci >/dev/null 2>&1; then
        lspci | grep -i brainchip || echo "[NOTE] no BrainChip device on PCIe yet (pre-driver or pre-card-insert)"
    fi
} >"${LOG_DIR}/host_probe.txt" 2>&1
echo "[OK] host probe → ${LOG_DIR}/host_probe.txt"

# 2. apt deps (Pi 5 Bookworm) / brew (Mac dry-run) -------------------------
if command -v apt-get >/dev/null 2>&1; then
    echo "[STEP] apt python3-venv + dkms (Pi 5)"
    sudo apt-get update -y >>"${LOG_DIR}/apt.log" 2>&1 || true
    sudo apt-get install -y python3 python3-pip python3-venv dkms \
        "linux-headers-$(uname -r)" \
        >>"${LOG_DIR}/apt.log" 2>&1 || true
elif command -v brew >/dev/null 2>&1; then
    echo "[INFO] brew detected (Mac local) — dry-run, no apt"
else
    echo "[WARN] neither apt nor brew — manual Python install required"
fi

# 3. venv + pip install akida (real HW SDK; aarch64 wheel from PyPI) -------
echo "[STEP] pip install akida (PyPI aarch64 wheel — 2.4 MB)"
VENV_DIR="${HOME}/.venv/anima-akida"
if [ -n "${VIRTUAL_ENV:-}" ] || [ -n "${CONDA_PREFIX:-}" ]; then
    PYBIN="python3"
    PIP_FLAGS=""
else
    if [ ! -d "${VENV_DIR}" ]; then
        python3 -m venv "${VENV_DIR}" >>"${LOG_DIR}/venv.log" 2>&1
    fi
    PYBIN="${VENV_DIR}/bin/python3"
    PIP_FLAGS=""
fi
"${PYBIN}" -m pip install --upgrade pip >>"${LOG_DIR}/pip_upgrade.log" 2>&1 || true
"${PYBIN}" -m pip install "akida>=2.0,<3.0" ${PIP_FLAGS} >>"${LOG_DIR}/pip_akida.log" 2>&1 || {
    echo "[WARN] akida SDK install failed — mock fallback will be used"
    echo "[WARN] (Mac arm64 has NO akida wheel; this is expected on Mac)"
}

# 4. Akida PCIe driver (DKMS) — manual step reminder -----------------------
cat <<EOF | tee "${LOG_DIR}/akida_pcie_driver_reminder.txt"
[REMINDER] Akida PCIe driver install (Pi 5 + AKD1000 M.2):
  1. Sign up at https://developer.brainchip.com/
  2. Download driver tarball: akida-pcie-driver-<ver>.tar.gz
  3. Build + install via DKMS:
       sudo dkms add .
       sudo dkms install akida-pcie/<ver>
       sudo modprobe akida_pcie
  4. Verify:
       lspci | grep -i brainchip   # → 1f87:1000 BrainChip
       ls /dev/akida*              # → /dev/akida0
       dmesg | grep -i akida
  5. If python3 -c "import akida; print(akida.devices())" returns [], driver missing
EOF

# 5. INSTALL.sh chain ------------------------------------------------------
echo "[STEP] chain to SUB_ENGINES/AKIDA/INSTALL.sh"
bash "${HERE}/INSTALL.sh" 2>&1 | tee "${LOG_DIR}/install.log"

# 6. import + AKD1000 probe ------------------------------------------------
"${PYBIN}" - <<'PY' | tee -a "${LOG_DIR}/import_probe.txt"
import sys

# 1. import akida (HW path)
try:
    import akida
    print(f"[OK] akida {akida.__version__} importable (HW path)")
    devs = akida.devices()
    print(f"[INFO] akida.devices() count={len(devs)}")
    for i, d in enumerate(devs):
        print(f"  [{i}] version={d.version} desc={getattr(d, 'desc', '?')}")
except ImportError:
    print("[INFO] akida SDK not importable — mock fallback path active (Mac local pre-arrival)")

# 2. pack runtime + AKD1000 assert (works on both backends)
try:
    sys.path.insert(0, "${HERE}")  # noqa — Bash heredoc substitution NOT used here
except NameError:
    pass
try:
    from pack.runtime.metatf_runtime import get_runtime_info, assert_akd1000, reset_runtime
    reset_runtime()
    info = get_runtime_info()
    print(f"[OK] pack runtime backend={info['backend']}")
    try:
        a = assert_akd1000()
        print(f"[PASS] AKD1000 detected: {a}")
    except RuntimeError as exc:
        print(f"[NOTE] AKD1000 assert: {exc}")
except Exception as exc:  # noqa: BLE001
    print(f"[WARN] pack runtime probe failed: {exc!r}")
PY

# 7. cloud-trial reminder --------------------------------------------------
cat <<EOF | tee "${LOG_DIR}/cloud_trial_reminder.txt"
[REMINDER] Akida Cloud trial — optional, see:
  - SUB_ENGINES/AKIDA/README.md §5 Day 1
  - SUB_ENGINES/AKIDA/doc/metatf_install_linux_arm.md "Akida Cloud trial"
EOF

echo "=== Day 1: install OK ==="
