#!/usr/bin/env bash
# local_bench.sh — run AFTER pulling mid_convmoe.clm back. Engine-mount + 3-axis.
# AXIS-2 (CE-descent) via CORE/clm_ce_descent_probe.hexa (config-agnostic decode,
#   CLM_CE_PROBE_CKPT override). AXIS-1/AXIS-3 via three_axis_probe (substrate).
# brain_smoke WARN check. All VERBATIM. Run from the worktree root.
set -uo pipefail
WT="$(git rev-parse --show-toplevel)"
cd "$WT"
CLM="${1:-$WT/state/mid_convmoe_fire/mid_convmoe.clm}"
OUT="$WT/state/mid_convmoe_fire/bench"
mkdir -p "$OUT"
echo "=== MID ConvMoE engine-mount 3-axis bench: $CLM ==="

echo "--- verify_clm_v2 (clm_decodable) ---" | tee "$OUT/00_verify.txt"
python3 - <<PY 2>&1 | tee -a "$OUT/00_verify.txt"
import sys; sys.path.insert(0,'CLM/model')
from verify_clm_v2 import clm_decodable, parse_clm
p="$CLM"
dec=clm_decodable(p); g=parse_clm(p)
print("MID_CLM_DECODABLE","TRUE" if dec else "FALSE","nblk",g["nblk"],
      "clmx",g["clmx_found"],"n_ext",g["n_ext"],
      "block0",g["blocks"][0] if g["blocks"] else None,"exact_eof",g.get("exact_eof"))
PY

echo "--- AXIS-2 CE-descent (clm_ce_descent_probe.hexa, config-agnostic decode) ---" | tee "$OUT/axis2_ce.txt"
CLM_CE_PROBE_CKPT="$CLM" hexa run CORE/clm_ce_descent_probe.hexa 2>&1 | tee -a "$OUT/axis2_ce.txt"

echo "--- AXIS-1+3 substrate (three_axis_probe.hexa) ---" | tee "$OUT/axis13_substrate.txt"
hexa run CORE/three_axis_probe.hexa 2>&1 | tee -a "$OUT/axis13_substrate.txt"

echo "--- brain_smoke (WARN must be 0) ---" | tee "$OUT/brain_smoke.txt"
hexa run CORE/brain_smoke.hexa 2>&1 | tee -a "$OUT/brain_smoke.txt"

echo "=== BENCH DONE — outputs in $OUT ==="
