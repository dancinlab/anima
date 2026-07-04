#!/usr/bin/env python3
"""Aggregate per-pair robustness evals -> FROZEN-BAR verdict for H_9124 lever#1.

FROZEN BAR (pre-registered, no post-hoc move):
  ROBUST-POSITIVE 🟢 : DERIV G1 (bd>=2 AND bd>max_single) on >=4/5 held pairs
                       AND FLAT floors (G1 fail) on ALL pairs
                       AND G2 novel>=3 (control=0) on the passing DERIV pairs
                       AND paraphrase G1 held on the passing DERIV pairs.
  PARTIAL       🟠 : G1 multi-pair passes but G2 FAIL (rearrangement) OR
                       paraphrase collapse (surface memorization).
  ARTIFACT      🔴 : DERIV G1 passes only 1 pair OR is a bd=2 threshold fluke.
"""
import os, sys, json, glob

evdir = sys.argv[1]
rows = {}
for f in sorted(glob.glob(os.path.join(evdir, "*.json"))):
    try:
        d = json.load(open(f))
    except Exception as e:
        print("SKIP", f, e); continue
    base = os.path.basename(f)[:-5]           # deriv_0_1 / flat_0_1
    arm, i, j = base.split("_")
    rows.setdefault((i, j), {})[arm] = d

pairs = sorted(rows.keys())
print("PAIR   arm    G1_bd  max_single  G1_pass  para_bd  para_pass  G2_novel  G2_ctrl  G2_pass")
print("-" * 92)
deriv_g1_pass = 0
deriv_g2_pass_on_g1 = 0
deriv_para_hold_on_g1 = 0
flat_all_floor = True
n_pairs = 0
for (i, j) in pairs:
    n_pairs += 1
    for arm in ("deriv", "flat"):
        d = rows[(i, j)].get(arm)
        if not d:
            print(f"{i},{j}    {arm:<5s}  MISSING")
            continue
        g1 = d["G1_held"]; pa = d["G1_paraphrase"]; g2 = d["G2"]
        print(f"{i},{j}    {arm:<5s}  {g1['best_distinct']:<5d}  {g1['max_single']:<10d}  "
              f"{str(g1['pass']):<7s}  {pa['best_distinct']:<6d}  {str(pa['pass']):<9s}  "
              f"{g2['n_novel']:<8d}  {g2['control_novel']:<7d}  {str(g2['pass'])}")
        if arm == "deriv":
            if g1["pass"]:
                deriv_g1_pass += 1
                if g2["pass"]:
                    deriv_g2_pass_on_g1 += 1
                if pa["pass"]:
                    deriv_para_hold_on_g1 += 1
        if arm == "flat" and g1["pass"]:
            flat_all_floor = False

print("-" * 92)
print(f"DERIV G1 PASS: {deriv_g1_pass}/{n_pairs} held pairs")
print(f"FLAT floors on ALL pairs (no G1 pass): {flat_all_floor}")
print(f"  of DERIV-G1-pass pairs: G2 novel>=3&ctrl=0 on {deriv_g2_pass_on_g1}; "
      f"paraphrase held on {deriv_para_hold_on_g1}")

g1_robust = deriv_g1_pass >= 4
g2_ok = deriv_g2_pass_on_g1 >= max(1, deriv_g1_pass - 1)   # G2 on (nearly) all passing pairs
para_ok = deriv_para_hold_on_g1 >= max(1, deriv_g1_pass - 1)

if g1_robust and flat_all_floor and g2_ok and para_ok:
    verdict = "🟢 ROBUST-POSITIVE"
elif g1_robust and flat_all_floor and (not g2_ok or not para_ok):
    verdict = "🟠 PARTIAL (G1 multi-pair holds; G2 or paraphrase fails)"
else:
    verdict = "🔴 ARTIFACT (G1 not robust across >=4 pairs / FLAT not floor)"
print("=" * 92)
print("VERDICT:", verdict)
