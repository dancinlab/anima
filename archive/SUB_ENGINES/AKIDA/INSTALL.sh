#!/usr/bin/env bash
# AUX/AKIDA/INSTALL.sh — Pi 5 + AKD1000 first-boot installer.
#
# Run on the Pi 5 host once after AKD1000 Dev Kit insertion.  Idempotent.
# On Mac local (pre-arrival) this still runs — the import block falls back
# to the numpy mock (pack.mocks.metatf_mock) instead of the real SDK.
set -eu

HERE="$(cd "$(dirname "$0")" && pwd)"
echo "=== anima-akida-pack INSTALL ==="
echo "[INFO] pack root: $HERE"

# 1. Python 3.10+ check ------------------------------------------------------
echo "[STEP 1/4] Python version check"
python3 -c "import sys; assert sys.version_info >= (3, 10), \
  f'need Python >= 3.10, got {sys.version_info[:2]}'; \
  print(f'[OK] python {sys.version.split()[0]}')"

# 2. pip install (editable) --------------------------------------------------
echo "[STEP 2/4] pip install -e $HERE"
if [ -n "${VIRTUAL_ENV:-}" ] || [ -n "${CONDA_PREFIX:-}" ]; then
    PIP_FLAGS=""
else
    # Pi 5 (PEP 668) — system Python needs --break-system-packages.
    PIP_FLAGS="--break-system-packages"
fi
python3 -m pip install -e "$HERE" ${PIP_FLAGS} 1>/tmp/akida_pip.log 2>&1 || {
    echo "[FAIL] pip install -e failed — see /tmp/akida_pip.log"
    tail -20 /tmp/akida_pip.log
    exit 1
}
echo "[OK] pack installed (editable)"

# 3. try akida import (HW path), else mock fallback verified -----------------
echo "[STEP 3/4] akida import probe"
python3 - <<'PY'
try:
    import akida
    ver = getattr(akida, "__version__", "?")
    print(f"[OK] akida HW path, version={ver}")
except ImportError:
    print("[OK] mock fallback (Mac local pre-arrival)")
    try:
        from pack.runtime.metatf_runtime import get_runtime_info
        info = get_runtime_info()
        print(f"  runtime info: {info}")
    except Exception as exc:  # noqa: BLE001
        # runtime module may not be in place yet — fall back to mock directly
        from pack.mocks.metatf_mock import metatf_mock, _selftest
        print(f"  mock-only path: {metatf_mock!r}")
        print(f"  selftest: {_selftest()}")
PY

# 4. run falsifier aggregate ------------------------------------------------
echo "[STEP 4/4] F-AKIDA falsifier aggregate"
python3 -m pack.falsifiers.run_all || {
    echo "[WARN] falsifier aggregate non-zero exit — adapter pack may be incomplete"
}

echo "=== INSTALL complete ==="
