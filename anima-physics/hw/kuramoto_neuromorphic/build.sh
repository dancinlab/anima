#!/usr/bin/env bash
# build.sh — kuramoto_neuromorphic build pipeline (anima-physics HW #3)
#
# Usage:
#   ./build.sh sim       # numpy oscillator sim + F-HW-KU-1..5 falsifier
#   ./build.sh adapters  # py_compile Loihi 2 + Akida adapters (syntax only)
#   ./build.sh all       # sim + adapters (Phase 1a Mac local $0)
#
# Phase 1b (cloud submit) is NOT covered here — see DESIGN.md §6.

set -eu

HERE="$(cd "$(dirname "$0")" && pwd)"
SRC="$HERE/src"
STATE="$HERE/state"
mkdir -p "$STATE"

PY="${PYTHON:-python3}"

CMD="${1:-all}"

run_sim() {
    echo "=== sim: numpy Kuramoto N-oscillator local sim ==="
    "$PY" "$SRC/kuramoto_local_sim.py" 2>&1 | tee "$STATE/sim.log"
    echo "log: $STATE/sim.log"
}

run_adapters() {
    echo "=== adapters: py_compile syntax check (Loihi 2 + Akida) ==="
    {
        echo "--- kuramoto_loihi2_adapter.py ---"
        "$PY" -m py_compile "$SRC/kuramoto_loihi2_adapter.py" \
            && echo "OK: kuramoto_loihi2_adapter.py syntax PASS" \
            || { echo "FAIL: kuramoto_loihi2_adapter.py syntax"; exit 1; }
        echo ""
        echo "--- kuramoto_akida_adapter.py ---"
        "$PY" -m py_compile "$SRC/kuramoto_akida_adapter.py" \
            && echo "OK: kuramoto_akida_adapter.py syntax PASS" \
            || { echo "FAIL: kuramoto_akida_adapter.py syntax"; exit 1; }
        echo ""
        echo "--- import-gate dry run (no --submit; expects AVAILABLE=False on Mac) ---"
        "$PY" "$SRC/kuramoto_loihi2_adapter.py" --n 8 --k 2.0 --steps 1000
        echo ""
        "$PY" "$SRC/kuramoto_akida_adapter.py" --n 8 --k 2.0 --steps 1000
    } 2>&1 | tee "$STATE/adapter_syntax.log"
    echo "log: $STATE/adapter_syntax.log"
}

case "$CMD" in
    sim)      run_sim ;;
    adapters) run_adapters ;;
    all)      run_sim ; run_adapters ;;
    *)        echo "Usage: $0 {sim|adapters|all}" ; exit 1 ;;
esac
