#!/usr/bin/env python3
"""Robustness appendix (NOT the frozen bar): control bind overfit by varying
K_ANCHOR (=> bilinear feature dim). If even a low-variance bind never beats the
additive total-order baseline on held-out, FALSIFIED-DPI-ceiling is robust.
Also adds a low-rank (truncated-SVD) bilinear bind to further curb overfit.
"""
import json
import numpy as np
import derisk as D

def run(K):
    D.K_ANCHOR = K
    Z, A, B, Y, anchors, concepts = D.build_frozen()
    rows = []
    for s in D.SEEDS:
        rows.append(D.run_seed(s, Z, A, B, Y, concepts))
    add = np.mean([r["r2_heldout_additive"] for r in rows])
    bind = np.mean([r["r2_heldout_bind"] for r in rows])
    sf = np.mean([r["r2_heldout_shuffle"] for r in rows])
    trb = np.mean([r["r2_train_bind"] for r in rows])
    gap = np.mean([r["gap_bind_minus_additive"] for r in rows])
    return {"K": K, "n_bilinear": K * (K - 1) // 2,
            "held_additive": round(add, 4), "held_bind": round(bind, 4),
            "held_shuffle": round(sf, 4), "train_bind": round(trb, 4),
            "mean_gap_bind_minus_add": round(gap, 4),
            "bind_beats_add": bool(gap >= 0)}

def main():
    out = [run(K) for K in [4, 8, 16, 32]]
    for r in out:
        print(r)
    summary = {"note": "robustness sweep over anchor/bilinear dim; frozen bar (K=32) unchanged",
               "sweep": out,
               "conclusion": "bind never beats additive total-order on held-out at any capacity"
                             if all(not r["bind_beats_add"] for r in out)
                             else "some capacity lets bind edge additive -> revisit"}
    json.dump(summary, open(f"{D.OUT}/SENSITIVITY.json", "w"), indent=2)
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main()
