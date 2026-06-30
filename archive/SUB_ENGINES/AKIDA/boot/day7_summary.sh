#!/usr/bin/env bash
# AUX/AKIDA/boot/day7_summary.sh — Day 1-6 결과 통합 + summary.md emit.
#
# Day 7 outcome (README §5):
#   - state/day7_summary.md (보조엔진 LANDED)
#   - state/power_log.json (1mW envelope verify)
#   - dual-role 16/16 + HW 1c
set -eu

HERE="$(cd "$(dirname "$0")" && pwd)/.."
STATE_DIR="${HERE}/state"
OUT_MD="${STATE_DIR}/day7_summary.md"
OUT_POWER="${STATE_DIR}/power_log.json"
mkdir -p "${STATE_DIR}"

echo "=== Day 7: summary ==="

# 1. collect per-day log dirs ---------------------------------------------
DAYS_FOUND=()
for d in 1 2 3 4 5 6; do
    matches=( "${STATE_DIR}/day${d}_"* )
    for m in "${matches[@]}"; do
        if [ -d "$m" ]; then DAYS_FOUND+=("$m"); fi
    done
done
echo "[INFO] day log dirs found: ${#DAYS_FOUND[@]}"

# 2. emit summary.md -------------------------------------------------------
{
    echo "# AKIDA Day 7 summary — $(date -u +%Y-%m-%dT%H:%M:%SZ)"
    echo ""
    echo "Per the README §5 Day 1-7 plan, this file aggregates Day 1-6 outputs."
    echo ""
    echo "## per-day artifacts"
    if [ "${#DAYS_FOUND[@]}" -eq 0 ]; then
        echo "_no day{1..6} log dirs found under \`${STATE_DIR}\` — please run BOOT.sh 1 6 first._"
    else
        for d in "${DAYS_FOUND[@]}"; do
            echo "- \`$d\`"
            find "$d" -maxdepth 1 -type f -printf '  - %f\n' 2>/dev/null \
                || find "$d" -maxdepth 1 -type f -exec basename {} \; \
                   | awk '{print "  - " $0}'
        done
    fi
    echo ""
    echo "## F-AKIDA aggregate"
    python3 -m pack.falsifiers.run_all --json 2>/dev/null \
        | python3 -c "import sys,json; \
          d=json.load(sys.stdin); \
          print(f'- adapters discovered: {d[\"adapters_discovered\"]}'); \
          print(f'- PASS: {d[\"pass_total\"]} / target {d[\"target_pass\"]}'); \
          print(f'- FAIL: {d[\"fail_total\"]}')" \
        || echo "_falsifier aggregate unavailable_"
    echo ""
    echo "## boot status"
    echo "- INSTALL.sh: $(test -x "${HERE}/INSTALL.sh" && echo OK || echo MISSING)"
    echo "- BOOT.sh:    $(test -x "${HERE}/BOOT.sh" && echo OK || echo MISSING)"
    echo "- 7 day-scripts: $(ls "${HERE}/boot/"day*_*.sh 2>/dev/null | wc -l | tr -d ' ')"
    echo ""
    echo "## honest C3"
    echo "1. Mac local pre-arrival: mock fallback path only (deterministic, no real spikes)."
    echo "2. Power envelope verified via design spec (~1 mW typical, AKD1000 datasheet),"
    echo "   not measured silicon — see \`power_log.json\` (mode=DESIGN_SPEC) below."
    echo "3. demiurge gate_state = CLOSED only when real \`akida\` SDK import succeeds."
} >"${OUT_MD}"
echo "[OK] summary → ${OUT_MD}"

# 3. emit power_log.json ---------------------------------------------------
python3 - <<PY
import json, os, time
log = {
    "timestamp": time.time(),
    "mode": "DESIGN_SPEC",  # DESIGN_SPEC | SILICON_MEASURED
    "envelope_mW": {
        "typical": 1.0,
        "peak": 100.0,
        "source": "BrainChip AKD1000 datasheet",
    },
    "host": {
        "platform": os.uname().sysname,
        "machine": os.uname().machine,
    },
    "notes": (
        "Pre-arrival baseline.  Day 7 power_log on real Pi 5 + AKD1000 "
        "must overwrite with mode=SILICON_MEASURED + per-day envelope rows."
    ),
}
with open("${OUT_POWER}", "w") as f:
    json.dump(log, f, indent=2)
print(json.dumps(log, indent=2))
PY
echo "[OK] power log → ${OUT_POWER}"

echo "=== Day 7: summary OK ==="
