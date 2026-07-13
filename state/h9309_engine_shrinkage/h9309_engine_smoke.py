#!/usr/bin/env python3
"""H_9309 — engine-native transfer of the H_9298/H_9301 shrinkage faculty.

Fires the LIVE engine faculties (core/engine_cli), not a private probe:
    jamo_head_grow         -- the existing flat count-MLE head   (H_1321 GREEN, untouched)
    jamo_head_grow_shrink  -- the NEW faculty: growth repair + Witten-Bell shrinkage head
    jamo_head_ce           -- the shared held-out CE scorer

Two frozen bars, each with its own positive control. A wiring that cannot be told apart from the
old faculty is not wired (wire-to-prod); a bar that a broken faculty would also pass is theatre.

  E1 GROWTH-UNCAPPED : on a stream whose max-variance axis is coarse (few distinct values), the OLD
                       grow hits a degenerate median split and the loop dies. The repaired faculty
                       must reach strictly MORE cells at the same budget.
                       KILL: equal cell counts => the repair is not live.

  E2 STARVATION-DISSOCIATION (the H_9301 finding, engine-native): grow the pool until the cells ARE
                       starved, then score held-out CE with each head over the SAME partition.
                       The FLAT head must DEGRADE as cells grow; the SHRINKAGE head must not.
                       KILL: flat does not degrade => starvation never engaged, bar unreadable
                             (a flat sweep means the axis is not engaged, not that there is no effect).
"""
import os, sys, json, math, random

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "core"))
import engine_cli as E                                        # the LIVE engine


def make_stream(n, n_sym, coarse, seed):
    """A 2-D context stream. `coarse` bounds the number of distinct values per axis, which is what
    manufactures the degenerate median split the old growth loop dies on."""
    rng = random.Random(seed)
    X, Y = [], []
    for _ in range(n):
        a = rng.randrange(coarse) / float(coarse)
        b = rng.randrange(coarse) / float(coarse)
        # a real (non-uniform) context->symbol law so the heads have something to learn
        base = int((a * 7 + b * 3) * n_sym) % n_sym
        y = base if rng.random() < 0.75 else rng.randrange(n_sym)
        X.append([a, b])
        Y.append(y)
    return X, Y


def run(X, Y, grow_max, vj, faculty):
    ntr = int(len(X) * 0.8)
    Xtr, Ytr, Xte, Yte = X[:ntr], Y[:ntr], X[ntr:], Y[ntr:]
    cfg = E.EngineConfig(True, True, True, True)   # mitosis ON -- p8 growth gate open
    jh = E.jamo_head_new([[0.3, 0.5], [0.7, 0.5]], vj, 2)
    grown = faculty(jh, Xtr, Ytr, len(Xtr), grow_max, 8, 0.05, 1.0, cfg)
    return E.jamo_head_cells(grown), E.jamo_head_ce(grown, Xte, Yte)


def main():
    VJ = 12
    X, Y = make_stream(4000, VJ, coarse=6, seed=9307)
    out = {"id": "H_9309"}

    # ---- E1 GROWTH-UNCAPPED -------------------------------------------------------------
    old_cells, old_ce = run(X, Y, 64, VJ, E.jamo_head_grow)
    new_cells, new_ce = run(X, Y, 64, VJ, E.jamo_head_grow_shrink)
    e1 = new_cells > old_cells
    print(f"[E1] grow_max=64   OLD cells={old_cells}   REPAIRED cells={new_cells}   -> {'PASS' if e1 else 'KILL'}")
    out["E1"] = {"old_cells": old_cells, "repaired_cells": new_cells, "pass": bool(e1)}
    if not e1:
        print("  KILL: the repair is not live (a degenerate split still caps the pool the same way).")

    # ---- E2 STARVATION-DISSOCIATION ------------------------------------------------------
    # Isolate the HEAD: grow ONCE with the repaired faculty, then score the SAME partition twice --
    # once with the flat Laplace head, once with the shrinkage head -- rebuilding each with the
    # engine's OWN _jh_counts / _jh_counts_wb over the engine's OWN _jh_assign. Same centers, same
    # owners, same test set; the estimator is the only difference.
    print("\n[E2] SAME partition, two heads (grown once, heads rebuilt) -- the head is the only change.")
    # STARVATION REGIME. Witten-Bell only has something to buy when T (distinct next-symbol TYPES
    # seen in a cell) is comparable to n (tokens owned by it) -- lam = n/(n+T). The mirror's regime
    # was Vj=323 with ~130 pts/cell (lam ~ 0.7). A first pass ran this smoke at VJ=12, where a
    # Laplace-12 flat head is already well-conditioned at 9 pts/cell: no starvation to fix, the
    # FLAT head never degraded, and the E2 guard correctly refused to read the bar. The bar is
    # unchanged; the STREAM is what was failing to reach the regime the bar is about.
    VJ2 = 200
    Xs, Ys = make_stream(2500, VJ2, coarse=50, seed=93072)
    ntr = int(len(Xs) * 0.8)
    Xtr, Ytr, Xte, Yte = Xs[:ntr], Ys[:ntr], Xs[ntr:], Ys[ntr:]
    cfg = E.EngineConfig(True, True, True, True)

    rows = []
    for gm in [4, 16, 64]:
        jh0 = E.jamo_head_new([[0.3, 0.5], [0.7, 0.5]], VJ2, 2)
        g = E.jamo_head_grow_shrink(jh0, Xtr, Ytr, len(Xtr), gm, 8, 0.05, 1.0, cfg)
        af = E._jh_field(g.centers, len(g.centers))
        own = E._jh_assign(af, Xtr)
        pooled = E._jh_pooled(Ytr, len(Xtr), VJ2, 1.0)
        flat_heads, wb_heads = [], []
        for k in range(len(g.centers)):
            flat_heads.append(E._jh_counts(Ytr, own, k, len(Xtr), VJ2, 1.0))
            wb_heads.append(E._jh_counts_wb(Ytr, own, k, len(Xtr), VJ2, pooled))
        ce_f = E.jamo_head_ce(E.JamoHead(g.centers, flat_heads, VJ2, 2), Xte, Yte)
        ce_w = E.jamo_head_ce(E.JamoHead(g.centers, wb_heads, VJ2, 2), Xte, Yte)
        cells = len(g.centers)
        rows.append({"grow_max": gm, "cells": cells, "flat_ce": ce_f, "wb_ce": ce_w})
        print(f"  grow_max={gm:4d}  cells={cells:3d}  ~{len(Xtr)//max(cells,1):4d} pts/cell   "
              f"FLAT ce={ce_f:.5f}   SHRINK ce={ce_w:.5f}   d={ce_w-ce_f:+.5f}")
    out["E2_sweep"] = rows

    flat_deg = rows[-1]["flat_ce"] - rows[0]["flat_ce"]      # >0 = degraded under starvation
    wb_deg = rows[-1]["wb_ce"] - rows[0]["wb_ce"]
    print(f"\n  FLAT   change over the sweep = {flat_deg:+.5f} nats  (must be > 0 = starvation engaged)")
    print(f"  SHRINK change over the sweep = {wb_deg:+.5f} nats")

    if flat_deg <= 0.0:
        v = ("KILL/UNREADABLE - the FLAT head never degraded => starvation was never engaged on this "
             "stream; the bar is UNREADABLE. A flat sweep means the axis is not engaged, not that "
             "there is no effect.")
        e2 = False
    else:
        e2 = wb_deg < flat_deg
        v = ("PASS - the engine reproduces the H_9301 dissociation on its OWN partition: the flat "
             "head degrades under starvation, the shrinkage head degrades less." if e2 else
             "KILL - shrinkage degrades as much as the flat head => the faculty is not doing its job.")
    print(f"[E2] -> {v}")
    out["E2"] = {"flat_degradation": flat_deg, "shrink_degradation": wb_deg, "pass": bool(e2)}

    green = bool(e1 and e2)
    out["GREEN"] = green
    out["verdict"] = ("ENGINE-NATIVE WIRED - both faculties fire live in core/engine_cli" if green
                      else "NOT WIRED / KILL - see bars")
    print(f"\nVERDICT: {out['verdict']}")
    json.dump(out, open(os.path.join(os.path.dirname(__file__), "h9309_smoke_result.json"), "w"),
              indent=2, ensure_ascii=False)
    sys.exit(0 if green else 1)


if __name__ == "__main__":
    main()
