#!/usr/bin/env python3
"""STEP-0.5 de-risk: frozen non-commutative residual R^2, 3-arm, closed-form lstsq.
Implements PREREG.md verbatim. $0 CPU-local numpy. No optimizer, no ridge, no tune.
"""
import json
import numpy as np

OUT = "/Users/mini/dancinlab/anima/state/trunk_obj_step0/noncommutative_derisk"

# ---- frozen structural constants (pre-registered) ----
MINC_TGT = 40
K_ANCHOR = 32
HELDOUT_FRAC = 0.20
DELTA = 0.10
SEEDS = [7, 4302, 4303]

def build_frozen():
    P = np.load(f"{OUT}/P.npy")
    N = P.shape[0]
    tot = P + P.T
    deg = tot.sum(1)
    # anchors = top-K by degree (deterministic, seed-independent = frozen)
    anchors = list(np.argsort(-deg)[:K_ANCHOR])
    anchor_set = set(int(a) for a in anchors)
    concepts = [i for i in range(N) if i not in anchor_set]  # disjoint universe

    # frozen per-concept anchor-relative directional profile z_c (dim K)
    Z = np.zeros((N, K_ANCHOR), dtype=np.float64)
    for c in range(N):
        for k, ak in enumerate(anchors):
            f, b = P[c, ak], P[ak, c]
            Z[c, k] = (f - b) / (f + b + 1.0)

    # frozen labels over concept-pairs with adequate mass, both endpoints non-anchor
    cset = set(concepts)
    pairs = []  # (a, b, y)
    for ci in range(len(concepts)):
        a = concepts[ci]
        for cj in range(ci + 1, len(concepts)):
            b = concepts[cj]
            m = tot[a, b]
            if m < MINC_TGT:
                continue
            y = (P[a, b] - P[b, a]) / m
            pairs.append((a, b, float(y)))
    return Z, np.array([p[0] for p in pairs]), np.array([p[1] for p in pairs]), \
           np.array([p[2] for p in pairs]), anchors, concepts

def antisym_bilinear(za, zb):
    # upper-tri (excl diag) of (za outer zb - zb outer za), per-row batch
    n, K = za.shape
    iu = np.triu_indices(K, 1)
    out = np.empty((n, len(iu[0])), dtype=np.float64)
    for r in range(n):
        M = np.outer(za[r], zb[r]) - np.outer(zb[r], za[r])
        out[r] = M[iu]
    return out

def add_feats(za, zb):
    return za - zb  # f(a)-f(b) total-order design

def fit_eval(Xtr, ytr, Xte, yte):
    # closed-form least squares (SVD, rank-safe); include intercept column
    def aug(X):
        return np.hstack([X, np.ones((X.shape[0], 1))])
    A = aug(Xtr)
    coef, *_ = np.linalg.lstsq(A, ytr, rcond=None)
    def r2(X, y):
        pred = aug(X) @ coef
        ssr = float(((y - pred) ** 2).sum())
        sst = float(((y - y.mean()) ** 2).sum())
        return 1.0 - ssr / sst if sst > 0 else float("nan")
    return r2(Xtr, ytr), r2(Xte, yte)

def run_seed(seed, Z, A, B, Y, concepts):
    rng = np.random.default_rng(seed)
    n = len(Y)
    idx = np.arange(n)
    rng.shuffle(idx)
    n_hold = int(round(HELDOUT_FRAC * n))
    hold_cand = idx[:n_hold]
    train_idx = idx[n_hold:]

    train_concepts = set(A[train_idx].tolist()) | set(B[train_idx].tolist())
    train_pairset = set(zip(A[train_idx].tolist(), B[train_idx].tolist()))

    # G1 guard: held-out combo unseen in train AND both endpoints seen in train
    hold_idx = [i for i in hold_cand
                if (int(A[i]), int(B[i])) not in train_pairset
                and int(A[i]) in train_concepts and int(B[i]) in train_concepts]
    hold_idx = np.array(hold_idx)

    # leak asserts
    assert len(train_pairset & set(zip(A[hold_idx].tolist(), B[hold_idx].tolist()))) == 0
    for i in hold_idx:
        assert int(A[i]) in train_concepts and int(B[i]) in train_concepts

    za_tr, zb_tr = Z[A[train_idx]], Z[B[train_idx]]
    za_te, zb_te = Z[A[hold_idx]], Z[B[hold_idx]]
    y_tr, y_te = Y[train_idx], Y[hold_idx]

    # arm (ii) additive/total-order
    add_tr, add_te = add_feats(za_tr, zb_tr), add_feats(za_te, zb_te)
    r2_add_tr, r2_add = fit_eval(add_tr, y_tr, add_te, y_te)

    # arm (i) bind = [additive , antisym-bilinear]  (nested, so gap = interaction)
    bl_tr = np.hstack([add_tr, antisym_bilinear(za_tr, zb_tr)])
    bl_te = np.hstack([add_te, antisym_bilinear(za_te, zb_te)])
    r2_bind_tr, r2_bind = fit_eval(bl_tr, y_tr, bl_te, y_te)

    # arm (iii) shuffle = bind with partner scrambled (label kept)
    perm_tr = rng.permutation(len(train_idx))
    perm_te = rng.permutation(len(hold_idx))
    zb_tr_s, zb_te_s = zb_tr[perm_tr], zb_te[perm_te]
    sf_tr = np.hstack([add_feats(za_tr, zb_tr_s), antisym_bilinear(za_tr, zb_tr_s)])
    sf_te = np.hstack([add_feats(za_te, zb_te_s), antisym_bilinear(za_te, zb_te_s)])
    r2_sf_tr, r2_sf = fit_eval(sf_tr, y_tr, sf_te, y_te)

    # secondary: pure symmetric z_a+z_b additive (reference floor, not in bar)
    sym_tr, sym_te = za_tr + zb_tr, za_te + zb_te
    _, r2_sym = fit_eval(sym_tr, y_tr, sym_te, y_te)

    gap_add = r2_bind - r2_add
    gap_sf = r2_bind - r2_sf
    return {
        "seed": seed, "n_pairs": int(n), "n_train": int(len(train_idx)), "n_heldout": int(len(hold_idx)),
        "r2_heldout_bind": r2_bind, "r2_heldout_additive": r2_add, "r2_heldout_shuffle": r2_sf,
        "r2_heldout_sym_ref": r2_sym,
        "r2_train_bind": r2_bind_tr, "r2_train_additive": r2_add_tr,
        "gap_bind_minus_additive": gap_add, "gap_bind_minus_shuffle": gap_sf,
        "pass_gap_add": bool(gap_add >= DELTA), "pass_gap_sf": bool(gap_sf >= DELTA),
        "pass_both": bool(gap_add >= DELTA and gap_sf >= DELTA),
        "leak_flag_bind_exact1": bool(abs(r2_bind - 1.0) < 1e-9),
        "leak_flag_shuffle_high": bool(r2_sf >= DELTA),
    }

def main():
    Z, A, B, Y, anchors, concepts = build_frozen()
    results = [run_seed(s, Z, A, B, Y, concepts) for s in SEEDS]
    n_pass = sum(r["pass_both"] for r in results)
    any_leak = any(r["leak_flag_bind_exact1"] or r["leak_flag_shuffle_high"] for r in results)

    if any_leak:
        verdict = "INVALID-LEAK"
    elif n_pass >= 2:
        verdict = "REWARDS-RECOMB-signal"
    elif n_pass == 0 and all((not r["pass_gap_add"]) or (not r["pass_gap_sf"]) for r in results):
        # additive or shuffle caught up in all seeds
        verdict = "FALSIFIED-DPI-ceiling"
    else:
        verdict = "DIRECTIONAL"

    summary = {
        "verdict": verdict, "delta": DELTA, "seeds": SEEDS, "n_pass_2of3": n_pass,
        "n_concepts": len(concepts), "n_anchors": len(anchors),
        "cycle_frac_census": json.load(open(f"{OUT}/census.json"))["cycle_frac"],
        "results": results,
        "honesty": "mini numpy = NOT 303M engine-native -> any PASS is DIRECTIONAL toward STEP-1 justification, not GREEN closure.",
    }
    with open(f"{OUT}/RESULT.json", "w") as f:
        json.dump(summary, f, indent=2)
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main()
