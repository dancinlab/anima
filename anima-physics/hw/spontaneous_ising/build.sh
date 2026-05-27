#!/usr/bin/env bash
# build.sh — spontaneous_ising build pipeline (Path A + Path B)
#
# Usage:
#   ./build.sh sim       # iverilog simulation + VCD + sim.log (Path B)
#   ./build.sh synth     # yosys synth_ecp5 → ising_fsm.json (Path B)
#   ./build.sh adapters  # py_compile Toshiba SBM + Fujitsu DA adapters (Path A)
#   ./build.sh all       # sim + synth + adapters (Phase 1a $0 Mac local)

set -eu

HERE="$(cd "$(dirname "$0")" && pwd)"
SRC="$HERE/src"
STATE="$HERE/state"
mkdir -p "$STATE"

CMD="${1:-all}"

run_sim() {
    echo "=== sim: iverilog + vvp (Path B FSM) ==="
    iverilog -o "$STATE/ising_fsm_sim" \
        "$SRC/ising_fsm.v" \
        "$SRC/ising_fsm_tb.v"
    cd "$HERE"
    vvp "$STATE/ising_fsm_sim" | tee "$STATE/sim.log"
    echo "VCD: $STATE/ising_fsm.vcd · log: $STATE/sim.log"
}

run_synth() {
    echo "=== synth: yosys synth_ecp5 (Path B → ECP5 cell map) ==="
    yosys -p "
        read_verilog $SRC/ising_fsm.v
        synth_ecp5 -top ising_fsm -json $STATE/ising_fsm.json
        stat
    " 2>&1 | tee "$STATE/synth.log"
    echo "JSON: $STATE/ising_fsm.json · log: $STATE/synth.log"
}

run_adapters() {
    echo "=== adapters: py_compile (Path A cloud REST skeletons) ==="
    {
        echo "--- toshiba_sbm_adapter.py ---"
        python3 -m py_compile "$SRC/toshiba_sbm_adapter.py" && echo "PASS toshiba_sbm_adapter"
        echo "--- fujitsu_da_adapter.py ---"
        python3 -m py_compile "$SRC/fujitsu_da_adapter.py" && echo "PASS fujitsu_da_adapter"
    } 2>&1 | tee "$STATE/adapter_syntax.log"
}

case "$CMD" in
    sim)      run_sim ;;
    synth)    run_synth ;;
    adapters) run_adapters ;;
    all)      run_sim ; run_synth ; run_adapters ;;
    *)        echo "Usage: $0 {sim|synth|adapters|all}" ; exit 1 ;;
esac
