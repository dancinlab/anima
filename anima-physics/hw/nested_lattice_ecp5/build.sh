#!/usr/bin/env bash
# build.sh — nested_lattice_ecp5 build pipeline
#
# Usage:
#   ./build.sh sim    # iverilog simulation + VCD + state dump
#   ./build.sh synth  # yosys → ECP5 cell mapping (synth_ecp5) + stats
#   ./build.sh pnr    # nextpnr-ecp5 (Phase 1b, requires brew install)
#   ./build.sh pack   # ecppack → bitstream (Phase 1b)
#   ./build.sh all    # sim + synth (Phase 1a $0 Mac local)
#
# SW source: anima-physics/fpga/nested_lattice.hexa (PHYS-P8-1, 3-level hierarchy)
# Target:    Lattice ECP5-EVN dev board (LFE5UM5G-85F-8BG381C)
# Sibling:   ../strange_loop_ice40/build.sh (HW target #1, P5 strange loop)

set -eu

HERE="$(cd "$(dirname "$0")" && pwd)"
SRC="$HERE/src"
STATE="$HERE/state"
mkdir -p "$STATE"

CMD="${1:-all}"

run_sim() {
    echo "=== sim: iverilog + vvp ==="
    iverilog -g2012 -o "$STATE/nested_lattice_sim" \
        "$SRC/mix3.v" \
        "$SRC/nested_lattice_top.v" \
        "$SRC/nested_lattice_tb.v"
    cd "$HERE"
    vvp "$STATE/nested_lattice_sim" | tee "$STATE/sim.log"
    echo "VCD: $STATE/nested_lattice.vcd · log: $STATE/sim.log"
}

run_synth() {
    echo "=== synth: yosys → ECP5 cell map (synth_ecp5) ==="
    yosys -p "
        read_verilog $SRC/mix3.v $SRC/nested_lattice_top.v
        synth_ecp5 -top nested_lattice_top -json $STATE/nested_lattice.json
        stat
    " 2>&1 | tee "$STATE/synth.log"
    echo "JSON: $STATE/nested_lattice.json · log: $STATE/synth.log"
}

run_pnr() {
    echo "=== pnr: nextpnr-ecp5 ==="
    if ! command -v nextpnr-ecp5 >/dev/null; then
        echo "ERROR: nextpnr-ecp5 not installed (brew install nextpnr-ecp5 prjtrellis)"
        exit 1
    fi
    nextpnr-ecp5 --um5g-85k --package CABGA381 --speed 8 \
        --json "$STATE/nested_lattice.json" \
        --lpf "$HERE/constraints/ecp5_evn.lpf" \
        --textcfg "$STATE/nested_lattice.config" \
        2>&1 | tee "$STATE/pnr.log"
}

run_pack() {
    echo "=== pack: ecppack ==="
    ecppack --input "$STATE/nested_lattice.config" --bit "$STATE/nested_lattice.bit"
    echo "bitstream: $STATE/nested_lattice.bit"
}

case "$CMD" in
    sim)   run_sim ;;
    synth) run_synth ;;
    pnr)   run_pnr ;;
    pack)  run_pack ;;
    all)   run_sim ; run_synth ;;
    *)     echo "Usage: $0 {sim|synth|pnr|pack|all}" ; exit 1 ;;
esac
