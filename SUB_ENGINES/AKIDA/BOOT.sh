#!/usr/bin/env bash
# AUX/AKIDA/BOOT.sh — Day 1-7 sequential boot runner (Pi 5 + AKD1000).
#
# Usage:
#   ./BOOT.sh              # Day 1 → Day 7 (full sequence)
#   ./BOOT.sh 3            # Day 3 → Day 7
#   ./BOOT.sh 2 4          # Day 2 → Day 4
#
# Each step is `bash boot/dayN_*.sh`; abort on first non-zero exit.
set -eu

HERE="$(cd "$(dirname "$0")" && pwd)"
START_DAY="${1:-1}"
END_DAY="${2:-7}"

echo "=== anima-akida-pack BOOT — Day ${START_DAY} → Day ${END_DAY} ==="
echo "[INFO] pack root: $HERE"

for d in $(seq "$START_DAY" "$END_DAY"); do
    pattern="$HERE/boot/day${d}_"*.sh
    echo ""
    echo "=== BOOT Day $d ==="
    if compgen -G "$pattern" > /dev/null; then
        for script in $pattern; do
            echo "[RUN] $script"
            bash "$script" || {
                echo "[FAIL] Day $d ($script) — abort"
                exit 1
            }
        done
    else
        echo "[SKIP] Day $d script missing (pattern: boot/day${d}_*.sh)"
    fi
done

echo ""
echo "=== Day ${START_DAY}-${END_DAY} complete ==="
