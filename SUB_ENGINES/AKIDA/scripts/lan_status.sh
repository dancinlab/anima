#!/usr/bin/env bash
# lan_status.sh — anima pack 가용성 4-axis health probe (전 pool host)
#
# pool 의 generic `pool on all` primitive 위에 anima-specific 4-axis probe wrap.
# constitution Principle I 정합 (pool 의 zero domain knowledge 보존).
#
# Usage:
#   ./lan_status.sh                    # 전 enabled host parallel probe
#   ./lan_status.sh --host <name>      # 단일 host

set -eu

HOST_FILTER=""
if [ "${1:-}" = "--host" ] && [ -n "${2:-}" ]; then
    HOST_FILTER="$2"
fi

# 4-axis anima health probe
PROBE='
echo -n "anima_repo: "
if [ -d ~/anima ]; then echo "✓"; else echo "✗"; fi
echo -n "SUB_ENGINES: "
ls ~/anima/SUB_ENGINES/ 2>/dev/null | tr "\n" "," | sed "s/,$//" || echo "(none)"
echo -n "akida_sdk: "
python3 -c "import akida; print(akida.__version__)" 2>&1 | grep -vE "Traceback|Error" || echo "✗"
echo -n "akd1000: "
lspci 2>/dev/null | grep -qi akida && echo "✓" || echo "✗"
echo "---"
'

if [ -n "$HOST_FILTER" ]; then
    pool on "$HOST_FILTER" "$PROBE"
else
    pool on all "$PROBE"
fi
