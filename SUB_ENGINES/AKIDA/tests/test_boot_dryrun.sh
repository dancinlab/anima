#!/usr/bin/env bash
# AUX/AKIDA/tests/test_boot_dryrun.sh — `bash -n` syntax check every boot script.
#
# Mac local 에서는 boot 스크립트들의 실 fire 없이 syntax 만 검증.
set -eu

HERE="$(cd "$(dirname "$0")" && pwd)/.."

echo "=== boot dry-run syntax check ==="

FAIL=0
for s in \
    "${HERE}"/boot/day*_*.sh \
    "${HERE}"/INSTALL.sh \
    "${HERE}"/BOOT.sh \
    "${HERE}"/tests/run_all.sh \
    "${HERE}"/tests/test_boot_dryrun.sh
do
    if [ ! -f "$s" ]; then
        echo "[SKIP] $s (missing)"
        continue
    fi
    if bash -n "$s"; then
        echo "[OK]   $s"
    else
        echo "[FAIL] $s"
        FAIL=$((FAIL + 1))
    fi
done

if [ "$FAIL" -gt 0 ]; then
    echo "=== boot dry-run: $FAIL syntax error(s) ==="
    exit 1
fi
echo "=== boot dry-run: all OK ==="
