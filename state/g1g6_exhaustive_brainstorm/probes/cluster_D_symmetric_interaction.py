#!/usr/bin/env python3
"""Cluster D $0 probe -- SYMMETRIC interaction family DPI screen.

Covers the D sub-family that H_9131 S4 (interaction-in-reps, real 303M h1129) did NOT
test: S4 used the ANTISYMMETRIC residual r(a,b)=(P[a,b]-P[b,a])/tot only. The DPI
meta-law (lstsq-vs-lstsq structural proof) says commutative-bag targets are INERT, but
that proof was SYNTHETIC. This probe closes the gap on the FROZEN-real-corpus anchor Z
for SYMMETRIC / commutative interaction labels -- the label structure of:

  D2  intervention-equivariance  -> symmetric displacement-magnitude analogue
  D4  relation bottleneck        -> relation-class jointly decodable from (a,b)
  D12 mutual-information / total-correlation -> SYMMETRIC 2-way interaction info

DPI prediction (the wall): a commutative/symmetric interaction target is a function of
the exchangeable bag {a,b} -> additive baseline z_a+z_b captures it -> bind
(additive+symmetric bilinear) does NOT beat additive on held-out combos. If prediction
holds -> D2/D4/D12 are RETREAD of the floored interaction axis (no new lever).

FROZEN BAR (pre-registered BEFORE run, no tune-to-green, p7):
  PASS iff >=2/3 seeds {7,4302,4303} for a given label:
    (1) r2_bind - r2_additive >= DELTA on held-out, AND
    (2) r2_bind - r2_shuffle >= DELTA on held-out, AND
    (3) no leak (r2_bind != 1.0).
  DELTA = 0.10 (same as H_9131 S4 / derisk PREREG).

Inputs (frozen, reused 1:1, no model load):
  state/trunk_obj_step0/noncommutative_derisk/{P.npy,vocab.json}
Z rebuilt deterministically (seed-independent = frozen) exactly as derisk.py.
$0 CPU-local numpy, OMP_NUM_THREADS=4. optimizer-robust (closed-form lstsq).
"""
import os, json
import numpy as np

DERISK = "/Users/mini/dancinlab/anima/state/trunk_obj_step0/noncommutative_derisk"
OUT = "/Users/mini/dancinlab/anima/state/g1g6_exhaustive_brainstorm/probes"

MINC_TGT = 40
K_ANCHOR = 32
HELDOUT_FRAC = 0.20
DELTA = 0.10
SEEDS = [7, 4302, 4303]


def build_frozen():
    P = np.load(f"{DERISK}/P.npy")
    N = P.shape[0]
    tot = P + P.T
    deg = tot.sum(1)
    anchors = list(np.argsort(-deg)[:K_ANCHOR])
    anchor_set = set(int(a) for a in anchors)
    concepts = [i for i in range(N) if i not in anchor_set]
    Z = np.zeros((N, K_ANCHOR), dtype=np.float64)
    for c in range(N):
        for k, ak in enumerate(anchors):
            f, b = P[c, ak], P[ak, c]
            Z[c, k] = (f - b) / (f + b + 1.0)
    pairs = []
    for ci in range(len(concepts)):
        a = concepts[ci]
        for cj in range(ci + 1, len(concepts)):
            b = concepts[cj]
            m = tot[a, b]
            if m < MINC_TGT:
                continue
            pairs.append((a, b, float(m)))
    return P, Z, pairs, anchors, concepts


def sym_labels(P, pairs):
    N = P.shape[0]
    tot = P + P.T
    deg = tot.sum(1)
    exp = np.outer(deg, deg) / max(deg.sum(), 1.0)
    out = {"L_symresid": [], "L_pmi": [], "L_absdir": []}
    for a, b, m in pairs:
        e = exp[a, b]
        out["L_symresid"].append(float((m - e) / (m + e + 1.0)))
        out["L_pmi"].append(float(np.log((m + 1.0) / (e + 1.0))))
        out["L_absdir"].append(float(abs(P[a, b] - P[b, a]) / (m + 1.0)))
    for k in out:
        out[k] = np.array(out[k], dtype=np.float64)
    return out


def sym_bilinear(za, zb):
    n, K = za.shape
    iu = np.triu_indices(K, 0)
    out = np.empty((n, len(iu[0])), dtype=np.float64)
    for r in range(n):
        M = np.outer(za[r], zb[r]) + np.outer(zb[r], za[r])
        out[r] = M[iu]
    return out


def add_sym_feats(za, zb):
    return za + zb


def fit_eval(Xtr, ytr, Xte, yte):
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


def run_seed(seed, Z, A_idx, B_idx, labels):
    rng = np.random.default_rng(seed)
    n = len(A_idx)
    idx = np.arange(n)
    rng.shuffle(idx)
    n_hold = int(round(HELDOUT_FRAC * n))
    hold_cand = idx[:n_hold]
    train_idx = idx[n_hold:]
    train_concepts = set(A_idx[train_idx].tolist()) | set(B_idx[train_idx].tolist())
    train_pairset = set(zip(A_idx[train_idx].tolist(), B_idx[train_idx].tolist()))
    hold_idx = [i for i in hold_cand
                if (int(A_idx[i]), int(B_idx[i])) not in train_pairset
                and int(A_idx[i]) in train_concepts and int(B_idx[i]) in train_concepts]
    hold_idx = np.array(hold_idx)
    za_tr, zb_tr = Z[A_idx[train_idx]], Z[B_idx[train_idx]]
    za_te, zb_te = Z[A_idx[hold_idx]], Z[B_idx[hold_idx]]
    out = {"seed": seed, "n_train": int(len(train_idx)), "n_heldout": int(len(hold_idx))}
    for lname, Y in labels.items():
        y_tr, y_te = Y[train_idx], Y[hold_idx]
        add_tr, add_te = add_sym_feats(za_tr, zb_tr), add_sym_feats(za_te, zb_te)
        _, r2_add = fit_eval(add_tr, y_tr, add_te, y_te)
        bl_tr = np.hstack([add_tr, sym_bilinear(za_tr, zb_tr)])
        bl_te = np.hstack([add_te, sym_bilinear(za_te, zb_te)])
        r2_bind_tr, r2_bind = fit_eval(bl_tr, y_tr, bl_te, y_te)
        perm_tr = rng.permutation(len(train_idx))
        perm_te = rng.permutation(len(hold_idx))
        zb_tr_s, zb_te_s = zb_tr[perm_tr], zb_te[perm_te]
        sf_tr = np.hstack([add_sym_feats(za_tr, zb_tr_s), sym_bilinear(za_tr, zb_tr_s)])
        sf_te = np.hstack([add_sym_feats(za_te, zb_te_s), sym_bilinear(za_te, zb_te_s)])
        _, r2_sf = fit_eval(sf_tr, y_tr, sf_te, y_te)
        gap_add = r2_bind - r2_add
        gap_sf = r2_bind - r2_sf
        out[lname] = {
            "r2_bind": r2_bind, "r2_additive": r2_add, "r2_shuffle": r2_sf,
            "r2_bind_train": r2_bind_tr,
            "gap_bind_additive": gap_add, "gap_bind_shuffle": gap_sf,
            "pass": bool(gap_add >= DELTA and gap_sf >= DELTA and abs(r2_bind - 1.0) > 1e-9),
        }
    return out


def main():
    P, Z, pairs, anchors, concepts = build_frozen()
    A_idx = np.array([p[0] for p in pairs])
    B_idx = np.array([p[1] for p in pairs])
    labels = sym_labels(P, pairs)
    results = [run_seed(s, Z, A_idx, B_idx, labels) for s in SEEDS]
    agg = {}
    for ln in labels:
        n_pass = sum(r[ln]["pass"] for r in results)
        all_gap_neg = all(r[ln]["gap_bind_additive"] < 0 for r in results)
        verdict = ("DPI-CEILING-FLOORED" if (n_pass == 0 and all_gap_neg)
                   else "PASS-signal" if n_pass >= 2 else "DIRECTIONAL")
        agg[ln] = {
            "verdict": verdict, "n_pass_2of3": n_pass,
            "gaps_additive": [r[ln]["gap_bind_additive"] for r in results],
            "r2_bind_heldout": [r[ln]["r2_bind"] for r in results],
            "r2_additive_heldout": [r[ln]["r2_additive"] for r in results],
        }
    summary = {
        "probe": "cluster D symmetric-interaction DPI screen (D2/D4/D12 family)",
        "delta": DELTA, "seeds": SEEDS,
        "n_pairs": len(pairs), "n_concepts": len(concepts), "n_anchors": len(anchors),
        "label_structure": "all 3 labels are COMMUTATIVE functions of bag {a,b}",
        "dpi_prediction": "commutative target -> additive z_a+z_b captures it -> bind does not beat additive (INERT)",
        "per_label": agg,
        "honesty": "mini numpy on frozen corpus Z = NOT 303M engine-native (a_toy_scale_recheck). Any PASS = DIRECTIONAL toward a 303M forward, not GREEN closure.",
        "covers": ["D2 intervention-equivariance (symmetric displacement magnitude)",
                   "D4 relation-bottleneck (joint decode, commutative class signal)",
                   "D12 mutual-information / 2-way interaction-info (symmetric)"],
        "relation_to_h9131": "H_9131 S4 tested ANTISYMMETRIC residual only on real 303M; this tests the SYMMETRIC family on the frozen corpus Z (the untested cell).",
    }
    os.makedirs(OUT, exist_ok=True)
    with open(f"{OUT}/cluster_D_symmetric_interaction_RESULT.json", "w") as f:
        json.dump(summary, f, indent=2)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
