#!/usr/bin/env bash
# S187-G post-train Eval 3 comparison runner.
# Runs eval3_mitosis.py on g_A_ctrl + g_A_mit ckpts (apples-to-apples vs
# attempt10 vA Eval 3 in EVAL_REPORT §6.4) and emits a JSON summary
# `g_eval3_compare.json` for the MITOSIS_TRAINING_ACTIVE.md table.
#
# Expects both ckpts present at:
#   g_A_ctrl/ckpt_s187g_A_ctrl.pt
#   g_A_mit/ckpt_s187g_A_mit.pt
#
# Usage:
#   bash eval3_compare_s187g.sh                 # Mac CPU local
#   bash eval3_compare_s187g.sh ubu-1           # remote ubu-1 (faster)
set -euo pipefail

SDIR="/Users/ghost/core/anima/HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21"
OUT="$SDIR/eval_out/s187g"
mkdir -p "$OUT"

REMOTE="${1:-local}"

for V in ctrl mit; do
  CKPT="$SDIR/g_A_$V/ckpt_s187g_A_$V.pt"
  if [ ! -s "$CKPT" ]; then
    echo "[skip] $CKPT missing"; continue
  fi
  echo "[eval3] running g_A_$V on $REMOTE"
  if [ "$REMOTE" = "local" ]; then
    cd "$SDIR" && python3 eval3_mitosis.py "$CKPT" "g_A_$V" "$OUT"
  else
    # ubu-1 path (scp ckpt + script over, run, scp result back)
    RSDIR="/tmp/s187g_eval"
    ssh "$REMOTE" "mkdir -p $RSDIR"
    scp "$SDIR/eval3_mitosis.py" "$SDIR/conscious_decoder.py" "$SDIR/train_s187_3b.py" "$SDIR/mitosis_lib.py" "$REMOTE:$RSDIR/"
    scp "$CKPT" "$REMOTE:$RSDIR/"
    ssh "$REMOTE" "cd $RSDIR && python3 eval3_mitosis.py $RSDIR/$(basename "$CKPT") g_A_$V $RSDIR/out"
    scp "$REMOTE:$RSDIR/out/g_A_${V}_eval3.json" "$OUT/"
  fi
done

echo "[eval3] writing comparison summary"
python3 <<PY
import json, os
out_dir = "$OUT"
rows = []
for v in ["ctrl", "mit"]:
    p = os.path.join(out_dir, f"g_A_{v}_eval3.json")
    if not os.path.exists(p):
        rows.append(dict(cell=f"g_A_{v}", status="MISSING"))
        continue
    d = json.load(open(p))
    rows.append(dict(
        cell=f"g_A_{v}",
        initial_cells=d.get("initial_cells"),
        final_cells=d.get("final_cells"),
        splits=d.get("n_split"),
        merges=d.get("n_merge"),
        next_id=d.get("next_id"),
        phi_initial=round(d.get("phi_initial", 0.0), 4),
        phi_final=round(d.get("phi_final", 0.0), 4),
        steps=d.get("steps_run"),
    ))
# attempt10 vA carry for apples-to-apples
rows.append(dict(cell="vA (attempt10)", initial_cells=2, final_cells=70,
                 splits=68, merges=0, next_id=70, phi_initial=0.6871,
                 phi_final=0.5477, steps=41))
summary = dict(eval="S187-G Eval 3 comparison",
               protocol="eval3_mitosis.py greedy 40 + post-hoc CellPool d_model=3072 seed=1337",
               rows=rows)
out_summary = os.path.join(out_dir, "g_eval3_compare.json")
with open(out_summary, "w") as f:
    json.dump(summary, f, indent=2)
print("=== S187-G Eval 3 comparison ===")
for r in rows:
    print(f"  {r}")
print(f"wrote {out_summary}")
PY
