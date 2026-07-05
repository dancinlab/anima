#!/usr/bin/env python3
"""Cluster D9 $0 probe -- hard-negative additive-separability (DPI screen for D9).

D9: hard negative = same entities, wrong relation/condition; random negative forbidden.
Falsifier (brainstorm): random-negative arm vs hard-negative arm -> gate improvement.

The ONLY thing a $0 numpy probe can decide here (pre-registered, optimizer-robust):
  Is the "correct relation vs same-entity hard-negative" signal linearly separable from
  ADDITIVE features [z_a, z_b] alone, on held-out combos? If YES -> a contrastive/
  hard-negative objective collapses to the additive solution (DPI INERT) -> D9 is a
  RETREAD of the floored additive/interaction axis, no new lever. If NO (bilinear bind
  beats additive by >=delta) -> genuine signal worth a trunk retrain.

Construction (frozen, deterministic, reuses noncommutative_derisk P.npy + anchor Z):
  For each (a,b) with adequate mass, the SAME-ENTITY HARD NEGATIVE is (a, b*) where b*
  is a's other partner with the most OPPOSITE directional profile (b* = argmin over a's
  partners of signed P-direction agreement). Label y=1 for the true forward-strong pair,
  y=0 for the hard negative. This is exactly "same entities (shared a), wrong relation".

FROZEN BAR (pre-registered BEFORE run, no tune-to-green):
  DPI-INERT-CONFIRMED (-> RETREAD) iff >=2/3 seeds:
    (1) additive held-out accuracy >= 0.75 (hard-neg signal is additively separable), OR
    (2) bind held-out acc - additive held-out acc < DELTA (bilinear does not help).
  PASS-signal (-> worth GPU) iff >=2/3 seeds: bind acc - additive acc >= DELTA AND
    additive acc < 0.75 (genuinely needs the joint term).
  DELTA = 0.10. seeds {7,4302,4303}. Held-out = combo unseen, both concepts seen singly.

$0 CPU-local numpy. optimizer-robust (closed-form lstsq on binary label -> linear prob).
"""
import os, json
import numpy as np

DERISK = "/Users/mini/dancinlab/anima/state/trunk_obj_step0/noncommutative_derisk"
OUT = "/Users/mini/dancinlab/anima/state/g1g6_exhaustive_brainstorm/probes"

MINC_TGT = 40
K_ANCHOR = 32
HELDOUT_FRAC = 0.20
DELTA = 0.10
ACC_INERT = 0.75
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
    return P, Z, anchors, concepts


def build_hardneg_pairs(P, concepts):
    """For each (a,b) true pair, find a same-a hard-negative partner b* (opposite direction).
    Returns array of (a, b_pos, a, b_neg) rows -> features paired with y=1 / y=0."""
    N = P.shape[0]
    tot = P + P.T
    cset = set(concepts)
    # for each concept, its partner set with adequate mass
    partners = {c: [j for j in concepts if j != c and tot[c, j] >= MINC_TGT] for c in concepts}
    rows = []  # (a, b, y)
    for a in concepts:
        ps = partners[a]
        if len(ps) < 2:
            continue
        for b in ps:
            # true forward-strong signal: P[a,b] > P[b,a] (a->b direction)
            if P[a, b] <= P[b, a]:
                continue
            # hard negative: the partner b* of a with the most NEGATIVE direction (b*->a)
            d = {bb: P[a, bb] - P[bb, a] for bb in ps}
            b_star = min(ps, key=lambda bb: d[bb])
            if b_star == b or d[b_star] >= 0:
                continue
            rows.append((a, b, 1))
            rows.append((a, b_star, 0))
    return rows


def add_feats(za, zb):
    return np.hstack([za, zb])  # symmetric additive (commutative bag)


def bind_feats(za, zb):
    n, K = za.shape
    iu = np.triu_indices(K, 0)
    sym = np.empty((n, len(iu[0])), dtype=np.float64)
    for r in range(n):
        M = np.outer(za[r], zb[r]) + np.outer(zb[r], za[r])
        sym[r] = M[iu]
    return np.hstack([za, zb, sym])


def fit_acc(Xtr, ytr, Xte, yte):
    A = np.hstack([Xtr, np.ones((Xtr.shape[0], 1))])
    coef, *_ = np.linalg.lstsq(A, ytr, rcond=None)
    pred_tr = (np.hstack([Xtr, np.ones((Xtr.shape[0], 1))]) @ coef)
    pred_te = (np.hstack([Xte, np.ones((Xte.shape[0], 1))]) @ coef)
    acc_tr = float(((pred_tr > 0.5).astype(int) == ytr).mean())
    acc_te = float(((pred_te > 0.5).astype(int) == yte).mean())
    # AUC (rank-based, threshold-free)
    order = np.argsort(-pred_te)
    ranks = np.empty(len(pred_te), dtype=np.float64)
    ranks[order] = np.arange(len(pred_te))
    n1 = float((yte == 1).sum()); n0 = float((yte == 0).sum())
    auc = (ranks[yte == 0].sum() - n0 * (n0 - 1) / 2) / (n0 * n1) if n0 > 0 and n1 > 0 else float("nan")
    # auc convention: prob a random positive scores higher than a random negative
    auc = 1.0 - auc if auc < 0.5 else auc
    return acc_tr, acc_te, auc


def run_seed(seed, Z, A, B, Y):
    rng = np.random.default_rng(seed)
    n = len(Y)
    idx = np.arange(n)
    rng.shuffle(idx)
    n_hold = int(round(HELDOUT_FRAC * n))
    hold_cand = idx[:n_hold]
    train_idx = idx[n_hold:]
    train_concepts = set(A[train_idx].tolist()) | set(B[train_idx].tolist())
    train_pairset = set(zip(A[train_idx].tolist(), B[train_idx].tolist()))
    hold_idx = [i for i in hold_cand
                if (int(A[i]), int(B[i])) not in train_pairset
                and int(A[i]) in train_concepts and int(B[i]) in train_concepts]
    hold_idx = np.array(hold_idx)
    za_tr, zb_tr = Z[A[train_idx]], Z[B[train_idx]]
    za_te, zb_te = Z[A[hold_idx]], Z[B[hold_idx]]
    y_tr, y_te = Y[train_idx], Y[hold_idx]
    add_tr, add_te = add_feats(za_tr, zb_tr), add_feats(za_te, zb_te)
    _, acc_add, auc_add = fit_acc(add_tr, y_tr, add_te, y_te)
    bnd_tr, bnd_te = bind_feats(za_tr, zb_tr), bind_feats(za_te, zb_te)
    acc_bnd_tr, acc_bnd, auc_bnd = fit_acc(bnd_tr, y_tr, bnd_te, y_te)
    gap = acc_bnd - acc_add
    inert = (acc_add >= ACC_INERT) or (gap < DELTA)
    return {
        "seed": seed, "n_train": int(len(train_idx)), "n_heldout": int(len(hold_idx)),
        "acc_additive": acc_add, "acc_bind": acc_bnd, "auc_additive": auc_add, "auc_bind": auc_bnd,
        "gap_bind_additive": gap, "additive_already_separates": bool(acc_add >= ACC_INERT),
        "dpi_inert": bool(inert),
    }


def main():
    P, Z, anchors, concepts = build_frozen()
    rows = build_hardneg_pairs(P, concepts)
    A = np.array([r[0] for r in rows]); B = np.array([r[1] for r in rows]); Y = np.array([r[2] for r in rows])
    results = [run_seed(s, Z, A, B, Y) for s in SEEDS]
    n_inert = sum(r["dpi_inert"] for r in results)
    n_pass = sum((not r["dpi_inert"]) and (r["gap_bind_additive"] >= DELTA) for r in results)
    if n_inert >= 2:
        verdict = "DPI-INERT-CONFIRMED (D9 RETREAD)"
    elif n_pass >= 2:
        verdict = "PASS-signal (worth GPU)"
    else:
        verdict = "DIRECTIONAL"
    summary = {
        "probe": "cluster D9 hard-negative additive-separability",
        "delta": DELTA, "acc_inert_threshold": ACC_INERT, "seeds": SEEDS,
        "n_rows": len(rows), "n_pos": int((Y == 1).sum()), "n_neg": int((Y == 0).sum()),
        "n_concepts": len(concepts), "n_anchors": len(anchors),
        "verdict": verdict, "n_inert_seeds": n_inert, "n_pass_seeds": n_pass,
        "results": results,
        "honesty": "mini numpy on frozen corpus Z = NOT 303M engine-native. DIRECTIONAL only.",
        "dpi_reasoning": "If the same-entity/wrong-relation signal is linearly separable from "
                         "additive [z_a,z_b], a hard-negative contrastive objective collapses to "
                         "the additive solution -> no escape from the DPI ceiling.",
    }
    os.makedirs(OUT, exist_ok=True)
    with open(f"{OUT}/cluster_D9_hardneg_RESULT.json", "w") as f:
        json.dump(summary, f, indent=2)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
