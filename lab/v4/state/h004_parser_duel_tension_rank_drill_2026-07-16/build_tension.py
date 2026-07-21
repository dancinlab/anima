#!/usr/bin/env python3
"""H_004 G-0/G-1 on the BUILT MULTI-BIND panel (verify-done, $0).

DESIGN_g1_core_fable5.md §7/§8 gate step: "re-run G-0/G-1 on the BUILT f2''". The
earlier g1_core_check.py measured rank-mass + probe separation on a SYNTHETIC 4^6
factorial. This runs the identical tension pipeline on the REAL Korean panel that
build_honbind_multi.py emitted (panel_f2doubleprime.json, n=192, GF(4)-decorrelated),
reusing g1_core_check's proxy-parser / field / probe primitives verbatim.

Confirms, on the built panel:
  G-0 rank-mass : off-top ||T||^2 fraction >= 0.20  (single-bind was 0.000 -> F4-DEAD)
  G-1 probes    : probe(vec) >= 0.75 AND probe(rank-1) <= 0.60 AND separation > 0.05

Run:  python3 state/h004_parser_duel_tension_rank_drill_2026-07-16/build_tension.py
Exit: 0 iff both gates pass on the built panel.
"""

from __future__ import annotations

import json
import os
import sys

import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
import g1_core_check as gc            # reuse t_struct / concord_field / offtop / rank1_tiebreak / fit / acc

K = 6
N_NODES = 3 * K + 2                   # 20


def _heads():
    head_a, head_g = {}, {}
    for k in range(K):
        r = 3 * k
        head_a[r], head_g[r] = r + 1, r + 2          # contested RC edge
        head_a[r + 1] = head_g[r + 1] = r + 2        # Nk1의 -> Nk2
        head_a[r + 2] = head_g[r + 2] = 3 * K        # Nk2도 -> VFIN
    head_a[3 * K + 1] = head_g[3 * K + 1] = 3 * K    # ANS -> VFIN
    return head_a, head_g


def main() -> int:
    panel = json.load(open(os.path.join(_HERE, "panel_f2doubleprime.json"), encoding="utf-8"))
    head_a, head_g = _heads()
    Ts = gc.t_struct(N_NODES, head_a, head_g)

    Tlist, gold, Phi, strat = [], [], [], []
    for it in panel:
        hon = np.zeros(N_NODES)
        g = np.zeros(K)
        for k, c in enumerate(it["conjuncts"]):
            hp = int(c["hp"])
            pos1 = 1.0 if int(c["honored_position"]) == 1 else 0.0   # honored noun at Nk1?
            hon[3 * k] = hp
            hon[3 * k + 1] = pos1
            hon[3 * k + 2] = 1.0 - pos1
            g[k] = float(hp ^ int(pos1))               # == gold_flip (verified consistent)
            assert g[k] == c["gold_flip"], (g[k], c["gold_flip"])
        Tlist.append(gc.concord_field(Ts, hon))
        gold.append(g)
        Phi.append(hon.copy())                          # unary token features, shared by all probes
        strat.append(it["gold_pattern"])                # 16 patterns → CV stratification key
    gold = np.array(gold)
    Phi = np.array(Phi)
    strat = np.array(strat)

    offtop_mean = float(np.mean([gc.offtop(T) for T in Tlist]))
    vecT = np.array([T.ravel() for T in Tlist])
    r1T = np.array([gc.rank1_tiebreak(T).ravel() for T in Tlist])
    nrm = np.array([[np.linalg.norm(T)] for T in Tlist])
    perm = np.array([np.take(np.take(T, np.random.default_rng(7000 + i).permutation(N_NODES), 0),
                             np.random.default_rng(7000 + i).permutation(N_NODES), 1).ravel()
                     for i, T in enumerate(Tlist)])

    # train=test overfits on n=192 with high-dim T features; cv8 (stratified by the 16
    # gold-patterns) is the honest estimate (verdict-integrity — suspect the measurement
    # on a train/factorial divergence like perm-placebo 1.0 vs 0.711).
    probes = {}
    for nameX, X in [("vec", np.hstack([vecT, Phi])), ("rank1", np.hstack([r1T, Phi])),
                     ("norm", np.hstack([nrm, Phi])), ("tok_only", Phi),
                     ("perm_placebo_vec", np.hstack([perm, Phi]))]:
        tr = [gc.acc(gc.fit(X, gold[:, k]), X, gold[:, k]) for k in range(K)]
        cv = [gc.cv8(X, gold[:, k], strat) for k in range(K)]
        probes[nameX] = {"train_per_slot": [round(a, 4) for a in tr],
                         "train_mean": round(float(np.mean(tr)), 4),
                         "cv8_per_slot": [round(a, 4) for a in cv],
                         "cv8_mean": round(float(np.mean(cv)), 4)}

    # gates read the CV mean (the honest, non-overfit number)
    sep = round(probes["vec"]["cv8_mean"] - probes["rank1"]["cv8_mean"], 4)
    placebo_headroom = round(probes["vec"]["cv8_mean"] - probes["perm_placebo_vec"]["cv8_mean"], 4)
    g0_pass = offtop_mean >= 0.20
    g1_pass = (probes["vec"]["cv8_mean"] >= 0.75 and probes["rank1"]["cv8_mean"] <= 0.60 and sep > 0.05)
    f6_pass = placebo_headroom > 0.05
    ok = g0_pass and g1_pass and f6_pass

    print("=" * 74)
    print("H_004 G-0/G-1 on the BUILT MULTI-BIND panel (verify-done, not the factorial)")
    print("=" * 74)
    print(f"n={len(panel)} · K={K} · nodes={N_NODES}")
    print(f"\nG-0 rank-mass off-top = {round(offtop_mean,6)}  (>= 0.20 ? {g0_pass})   "
          f"[single-bind was 0.000 -> F4-DEAD]")
    print("G-1 probes (train_mean / cv8_mean — gates read cv8):")
    for nm in ("vec", "rank1", "norm", "tok_only", "perm_placebo_vec"):
        print(f"  {nm:18s} train={probes[nm]['train_mean']}  cv8={probes[nm]['cv8_mean']}")
    print(f"\nseparation vec - rank1 (cv8) = {sep}  (> 0.05 ? {sep>0.05})")
    print(f"F6 perm-placebo headroom (cv8) = {placebo_headroom}  (> 0.05 ? {f6_pass})")
    print("\nVERDICT:", "PASS — the BUILT MULTI-BIND panel clears G-0 rank-mass, G-1 separation, "
          "AND F6 placebo on cross-validated probes; training spend justified"
          if ok else "FAIL — a gate did not clear on the built panel (cv8)")

    out = {"n": len(panel), "K": K, "offtop_mean": round(offtop_mean, 6),
           "probes": probes, "separation_cv8": sep, "placebo_headroom_cv8": placebo_headroom,
           "g0_pass": g0_pass, "g1_pass": g1_pass, "f6_pass": f6_pass, "verdict_pass": ok,
           "prediction_factorial": {"offtop": 0.8333, "vec": 1.0, "rank1": 0.5833, "sep": 0.4167}}
    with open(os.path.join(_HERE, "build_tension.json"), "w") as fh:
        json.dump(out, fh, indent=2, ensure_ascii=False)
    print("\nwrote build_tension.json")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
