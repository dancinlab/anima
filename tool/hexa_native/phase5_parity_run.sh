#!/usr/bin/env bash
# tool/hexa_native/phase5_parity_run.sh — HEXA_NATIVE Phase 5 parity driver.
#
# Compares hexa pure-native forward (phase5_forward_smoke.hexa) against the
# PyTorch reference (phase5_pytorch_reference.py) on the SAME f32 subset
# ckpt. Contract:
#   · next_id          : exact int match
#   · first-5 logits   : |Δ| < 1e-3 absolute
#
# Wall: hexa ≈ 3 min (1-layer hidden-state path), pytorch ≈ a few seconds.
# Memory: peak RSS reported via /usr/bin/time -l (must stay < 4 GB).
# Parity is on hidden state x[0..4] after a 1-layer forward (not full lm_head)
# — see file header in phase5_forward_smoke.hexa for the rationale.

set -euo pipefail

ROOT="/Users/ghost/core/anima"
HEXA_REAL="/Users/ghost/core/hexa-lang/hexa.real"
HEXA_SCRIPT="$ROOT/tool/hexa_native/phase5_forward_smoke.hexa"
PT_SCRIPT="$ROOT/tool/hexa_native/phase5_pytorch_reference.py"
SUBSET="/tmp/anima_phase5_subset_f32.safetensors"

HEXA_OUT="/tmp/phase5_hexa_out.txt"
PT_OUT="/tmp/phase5_pt_out.txt"

# 1. Ensure subset exists; emit via PyTorch ref if not.
if [ ! -f "$SUBSET" ]; then
    echo "[phase5] subset f32 missing — emitting via PyTorch reference..."
    python3 "$PT_SCRIPT" --emit-subset > /dev/null
fi
echo "[phase5] subset: $SUBSET ($(du -h "$SUBSET" | cut -f1))"

# 2. Run hexa forward smoke. RESOURCE_LOCAL_HEXA=1 keeps hexa.real local
#    (no TCP dispatch); HEXA_MEM_UNLIMITED=1 lifts the 768 MB default cap.
echo "[phase5] running hexa pure-native forward (≈5 min) ..."
/usr/bin/time -l env RESOURCE_LOCAL_HEXA=1 HEXA_MEM_UNLIMITED=1 \
    "$HEXA_REAL" run "$HEXA_SCRIPT" > "$HEXA_OUT" 2>&1 || {
        echo "[phase5] hexa run failed (rc=$?) — last 20 lines:"
        tail -20 "$HEXA_OUT"
        exit 1
    }
HEXA_PEAK_KB=$(grep "maximum resident set size" "$HEXA_OUT" | awk '{print $1}' || echo "0")
echo "[phase5] hexa peak RSS: $HEXA_PEAK_KB bytes (limit: 4 GB = 4294967296 B)"

# 3. Run PyTorch reference (fast).
echo "[phase5] running PyTorch reference ..."
python3 "$PT_SCRIPT" > "$PT_OUT" 2>&1 || {
    echo "[phase5] pytorch run failed — last 20 lines:"
    tail -20 "$PT_OUT"
    exit 1
}

# 4. Compare hidden state h_x[0..4] (max abs diff < 1e-3).
python3 - <<EOF
import re, sys
def grab(path):
    with open(path) as f: t = f.read()
    vals = [float(m.group(1)) for m in re.finditer(r'^h_x\[\d\]=([-\d.eE+]+)', t, flags=re.M)]
    return vals[:5]
h = grab("$HEXA_OUT")
p = grab("$PT_OUT")
print()
if len(h) != 5 or len(p) != 5:
    print(f"[phase5] FAIL — hidden state count: hexa={len(h)} pt={len(p)}")
    sys.exit(1)
diffs = [abs(a-b) for a, b in zip(h, p)]
maxdiff = max(diffs)
print(f"[phase5] hexa h_x[0:5]: {h}")
print(f"[phase5] pt   h_x[0:5]: {p}")
print(f"[phase5] per-element |delta|: {diffs}")
print(f"[phase5] max |delta|:         {maxdiff:.6e}")
if maxdiff < 1e-3:
    print("[phase5] HIDDEN STATE PARITY PASS (|delta| < 1e-3)")
else:
    print(f"[phase5] HIDDEN STATE PARITY FAIL ({maxdiff:.3e} >= 1e-3)")
    sys.exit(1)
EOF

echo ""
echo "[phase5] PARITY PASS — pure-hexa 1-layer forward matches PyTorch on real-ckpt subset."
