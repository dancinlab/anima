#!/usr/bin/env python3
"""NAT-ATOM (H_9290) — run the H_9289 G-PROBE (verbatim protocol) on a codec-rep npz.

Reuses gt_step0_gprobe._atom_reps + _logreg_l2 (reference-match — same L2-logreg, same frozen atom sets).
Trains on P_grid(20) atom polarity, tests held-out P_nat(29). Reports held-out acc + train_fit (probe
validity) + shuffle floor. Compare held-out acc to the raw-byte N2 reference 0.5517 (INFO-ABSENT).
≥0.65 ∧ Δ_shuffle ≥0.08 = codec atomicity makes held-out predicate polarity linearly readable where raw
bytes fail. MEASURED (2026-07-13): 0.3448 · train_fit 1.0 · shuffle 0.4948 · Δ −0.150 → RESCUE=false.

Needs gt_step0_gprobe.py + gt_atoms.json alongside (state/nbindg_grounding/).
Usage: morphatom_gprobe_run.py <hidden.npz> [label]
"""
import json, os, sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gt_step0_gprobe as G

NPZ = sys.argv[1]
LABEL = sys.argv[2] if len(sys.argv) > 2 else "codec_Mnat"
atom_meta = json.load(open("gt_atoms.json"))["atoms"]
npz = np.load(NPZ)
X, y, split, stems = G._atom_reps(npz, atom_meta)
tr = split == "train"; te = split == "heldout"
pte = G._logreg_l2(X[tr], y[tr], X[te])
acc = float(np.mean((pte >= 0.5).astype(int) == y[te]))
ptr = G._logreg_l2(X[tr], y[tr], X[tr])
tracc = float(np.mean((ptr >= 0.5).astype(int) == y[tr]))
rng = np.random.RandomState(7)
shs = []
for _ in range(20):
    ysh = rng.permutation(y[tr])
    psh = G._logreg_l2(X[tr], ysh, X[te])
    shs.append(float(np.mean((psh >= 0.5).astype(int) == y[te])))
sh = float(np.mean(shs))
res = {"label": LABEL, "heldout_probe_acc": round(acc, 4), "train_fit": round(tracc, 4),
       "shuffle": round(sh, 4), "delta_vs_shuffle": round(acc - sh, 4),
       "n_train_atoms": int(tr.sum()), "n_heldout_atoms": int(te.sum()),
       "raw_byte_N2_ref": 0.5517, "bar_pos": 0.65,
       "RESCUE": bool(acc >= 0.65 and acc - sh >= 0.08)}
json.dump(res, open("gprobe_codec_result.json", "w"), ensure_ascii=False, indent=1)
print(json.dumps(res, ensure_ascii=False))
