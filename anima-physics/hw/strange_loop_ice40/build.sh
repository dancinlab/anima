#!/usr/bin/env bash
# build.sh — strange_loop_ice40 build pipeline
#
# Usage:
#   ./build.sh sim    # iverilog simulation + VCD + state_dump
#   ./build.sh synth  # yosys RTL → iCE40 cell mapping + stats
#   ./build.sh pnr    # nextpnr-ice40 (Phase 1b, requires brew install)
#   ./build.sh pack   # icepack → bitstream (Phase 1b)
#   ./build.sh prog   # iceprog → flash UP5K board (Phase 1b)
#   ./build.sh all    # sim + synth (Phase 1a $0 Mac local)

set -eu

HERE="$(cd "$(dirname "$0")" && pwd)"
SRC="$HERE/src"
STATE="$HERE/state"
mkdir -p "$STATE"

CMD="${1:-all}"

run_sim() {
    echo "=== sim: iverilog + vvp ==="
    iverilog -o "$STATE/strange_loop_sim" \
        "$SRC/mix4.v" \
        "$SRC/strange_loop_top.v" \
        "$SRC/strange_loop_tb.v"
    cd "$HERE"
    vvp "$STATE/strange_loop_sim" | tee "$STATE/sim.log"
    echo "VCD: $STATE/strange_loop.vcd · log: $STATE/sim.log"
}

run_synth() {
    echo "=== synth: yosys → iCE40 cell map ==="
    yosys -p "
        read_verilog $SRC/mix4.v $SRC/strange_loop_top.v
        synth_ice40 -top strange_loop_top -json $STATE/strange_loop.json
        stat
    " 2>&1 | tee "$STATE/synth.log"
    echo "JSON: $STATE/strange_loop.json · log: $STATE/synth.log"
}

run_pnr() {
    echo "=== pnr: nextpnr-ice40 ==="
    if ! command -v nextpnr-ice40 >/dev/null; then
        echo "ERROR: nextpnr-ice40 not installed (brew install icestorm nextpnr-ice40)"
        exit 1
    fi
    nextpnr-ice40 --up5k --package sg48 \
        --json "$STATE/strange_loop.json" \
        --pcf "$HERE/constraints/ice40up5k_sg48.pcf" \
        --asc "$STATE/strange_loop.asc" \
        2>&1 | tee "$STATE/pnr.log"
}

run_pack() {
    echo "=== pack: icepack ==="
    icepack "$STATE/strange_loop.asc" "$STATE/strange_loop.bin"
    echo "bitstream: $STATE/strange_loop.bin"
}

run_prog() {
    echo "=== prog: iceprog ==="
    iceprog "$STATE/strange_loop.bin"
}

case "$CMD" in
    sim)   run_sim ;;
    synth) run_synth ;;
    pnr)   run_pnr ;;
    pack)  run_pack ;;
    prog)  run_prog ;;
    all)   run_sim ; run_synth ;;
    *)     echo "Usage: $0 {sim|synth|pnr|pack|prog|all}" ; exit 1 ;;
esac
