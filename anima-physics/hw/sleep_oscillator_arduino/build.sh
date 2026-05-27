#!/usr/bin/env bash
# build.sh — sleep_oscillator_arduino build pipeline
#
# Usage:
#   ./build.sh sim     # Python phase-accumulator sim → state/sim.log
#   ./build.sh lint    # cat src/*.ino + .h + .cpp (arduino-cli 없이 eyeball)
#   ./build.sh compile # arduino-cli compile (Phase 1b, requires brew install)
#   ./build.sh upload  # arduino-cli upload  (Phase 1b)
#   ./build.sh all     # sim + lint   (Phase 1a $0 Mac local)

set -eu

HERE="$(cd "$(dirname "$0")" && pwd)"
SRC="$HERE/src"
STATE="$HERE/state"
mkdir -p "$STATE"

CMD="${1:-all}"

run_sim() {
    echo "=== sim: Python phase-accumulator sim (numpy) ==="
    python3 "$SRC/sleep_oscillator_local_sim.py" 2>&1 | tee "$STATE/sim.log"
    echo "log: $STATE/sim.log"
}

run_lint() {
    echo "=== lint: arduino source syntax-eyeball (arduino-cli 미설치 fallback) ==="
    local lint_log="$STATE/lint.log"
    : > "$lint_log"
    local files=( "$SRC/sleep_oscillator.ino" "$SRC/ad9833_driver.h" "$SRC/ad9833_driver.cpp" )
    local total_loc=0
    for f in "${files[@]}"; do
        if [[ ! -f "$f" ]]; then
            echo "MISSING: $f" | tee -a "$lint_log"
            continue
        fi
        local loc; loc=$(wc -l < "$f" | tr -d ' ')
        total_loc=$(( total_loc + loc ))
        echo "----- ${f#$HERE/} (${loc} LoC) -----" | tee -a "$lint_log"
    done
    # Basic syntax sanity: balanced braces in each file
    local fail=0
    for f in "${files[@]}"; do
        [[ -f "$f" ]] || continue
        local opens; opens=$(tr -cd '{' < "$f" | wc -c | tr -d ' ')
        local closes; closes=$(tr -cd '}' < "$f" | wc -c | tr -d ' ')
        if [[ "$opens" != "$closes" ]]; then
            echo "UNBALANCED BRACES in ${f#$HERE/}: open=$opens close=$closes" | tee -a "$lint_log"
            fail=$(( fail + 1 ))
        else
            echo "braces OK  ${f#$HERE/}  ({}=$opens)" | tee -a "$lint_log"
        fi
    done
    echo "total Arduino-side LoC: ${total_loc}" | tee -a "$lint_log"
    if (( fail > 0 )); then
        echo "lint FAIL ($fail file(s))" | tee -a "$lint_log"
        return 1
    fi
    echo "lint PASS — full arduino-cli compile requires:" | tee -a "$lint_log"
    echo "    brew install arduino-cli && arduino-cli core install arduino:avr" | tee -a "$lint_log"
}

run_compile() {
    echo "=== compile: arduino-cli compile (Phase 1b) ==="
    if ! command -v arduino-cli >/dev/null; then
        echo "ERROR: arduino-cli not installed."
        echo "       brew install arduino-cli"
        echo "       arduino-cli core install arduino:avr"
        exit 1
    fi
    arduino-cli compile --fqbn arduino:avr:uno "$SRC/sleep_oscillator.ino" \
        2>&1 | tee "$STATE/compile.log"
}

run_upload() {
    echo "=== upload: arduino-cli upload (Phase 1b) ==="
    if ! command -v arduino-cli >/dev/null; then
        echo "ERROR: arduino-cli not installed."
        exit 1
    fi
    local port="${PORT:-}"
    if [[ -z "$port" ]]; then
        port=$(ls /dev/cu.usbmodem* 2>/dev/null | head -1 || true)
        [[ -n "$port" ]] || { echo "ERROR: no /dev/cu.usbmodem* found; set PORT=/dev/..."; exit 1; }
    fi
    arduino-cli upload --fqbn arduino:avr:uno -p "$port" "$SRC/sleep_oscillator.ino" \
        2>&1 | tee "$STATE/upload.log"
}

case "$CMD" in
    sim)     run_sim ;;
    lint)    run_lint ;;
    compile) run_compile ;;
    upload)  run_upload ;;
    all)     run_sim ; run_lint ;;
    *)       echo "Usage: $0 {sim|lint|compile|upload|all}" ; exit 1 ;;
esac
