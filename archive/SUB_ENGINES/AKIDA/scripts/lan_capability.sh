#!/usr/bin/env bash
# lan_capability.sh — HW capability matrix (akida + fpga + arduino) 전 host
#
# pool on all + standard shell tools.
# constitution Principle I 정합.
#
# Usage:
#   ./lan_capability.sh                # 전 column
#   ./lan_capability.sh --filter akida # akida column 만

set -eu

FILTER="${2:-all}"
[ "${1:-}" = "--filter" ] || FILTER="all"

PROBE='
echo -n "akida: "
lspci 2>/dev/null | grep -qi akida && echo "✓" || echo "✗"
echo -n "fpga_tools: "
TOOLS=$(for t in iverilog yosys nextpnr-ice40 ecpprog; do
    command -v $t >/dev/null && echo $t
done | tr "\n" "," | sed "s/,$//")
[ -n "$TOOLS" ] && echo "$TOOLS" || echo "✗"
echo -n "arduino: "
arduino-cli version 2>/dev/null | head -1 | awk "{print \$3}" || echo "✗"
echo "---"
'

if [ "$FILTER" = "all" ]; then
    pool on all "$PROBE"
else
    pool on all "$PROBE" | grep -iE "^\[|^$FILTER|^---"
fi
