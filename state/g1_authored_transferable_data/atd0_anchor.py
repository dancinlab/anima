#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ATD-0 VALID-ANCHOR — harness-validity hard gate (Fable spec · numpy ground-truth · NO LM · mini).

Validates the authored corpus BEFORE any GPU training: the composition must be held-out-transferable,
non-commutative, byte-learnable, and NOT additively/lookup-solvable. Any check fails => corpus INVALID
(fix the generator; NOT tune-to-green — the model bars stay frozen). All five pass => harness VALID,
downstream ATD-1..5 verdicts admissible.

Frozen bars (pre-registered):
  1. additive readout on ground-truth z  -> held-out-pair R2 <= 0.10   (pure-bilinear target: additive floors)
  2. bilinear readout on ground-truth z  -> held-out-pair R2 >= 0.90   (correct family CAN solve it)
  3. non-commutativity: median |corr(t(a,b), t(b,a))| <= 0.30
  4. name-byte leak: regress name-bytes -> z  ->  R2 <= 0.05           (no name<->z shortcut)
  5. eval pairs (C_ho x C_ho) never appear in the training corpus       (lookup at chance by construction)
"""
import os, sys, json
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
K, D, N_TAG_UNUSED = 96, 6, 16
Q = 16
TRAIN_C = list(range(72)); HELD_C = list(range(72, 96))

def latents(seed=0):
    rs = np.random.RandomState(seed)
    z = rs.randn(K, D); z /= (np.linalg.norm(z, axis=1, keepdims=True) + 1e-9)
    return z

def operator(z=None):
    # SHARED concept-agnostic operator. Distinct role-maps g!=h make role-1 vs role-2 structurally
    # asymmetric so t(a,b) and t(b,a) are genuinely different functions (decorrelated), while the target
    # stays PURE-bilinear in (z_a,z_b) (additive floors) and concept-agnostic (generalizes to unseen).
    T = np.random.RandomState(1).randn(D, D, D)
    g = np.random.RandomState(2).randn(D, D)
    h = np.random.RandomState(3).randn(D, D)
    OP = dict(T=T, g=g, h=h, scale=1.0)
    if z is not None:
        # calibrate pre-tanh to per-dim std=1 so tanh stays in its near-linear regime (gain 0.7)
        rs = np.random.RandomState(11)
        smp = [(int(rs.randint(K)), int(rs.randint(K))) for _ in range(2000)]
        raw = np.stack([np.einsum("kij,i,j->k", T, g @ z[a], h @ z[b]) for a, b in smp])
        OP["scale"] = 0.7 / (raw.std(0) + 1e-9)
    return OP

def target(z, OP, a, b):
    ra = OP["g"] @ z[a]; rb = OP["h"] @ z[b]                 # role-asymmetric encodings
    raw = np.einsum("kij,i,j->k", OP["T"], ra, rb) * OP["scale"]
    return np.tanh(raw)                                       # [D] pure-bilinear non-commutative, calibrated

def syllable(c):
    cons = "bkdfghjlmnprstvz"; vow = "aeiou"
    rs = np.random.RandomState(9000 + c)
    return cons[rs.randint(16)] + vow[rs.randint(5)] + cons[rs.randint(16)] + vow[rs.randint(5)]

def r2(pred, true):
    return 1.0 - np.sum((pred - true) ** 2) / np.sum((true - true.mean(0)) ** 2)

def ridge_fit(X, Y, lam=1.0):
    A = np.hstack([X, np.ones((len(X), 1))])
    return np.linalg.solve(A.T @ A + lam * np.eye(A.shape[1]), A.T @ Y)

def ridge_pred(w, X):
    return np.hstack([X, np.ones((len(X), 1))]) @ w

def gen_pairs(pool, n, rs):
    out = set()
    while len(out) < n:
        a, b = int(rs.choice(pool)), int(rs.choice(pool))
        if a != b: out.add((a, b))
    return list(out)

def main():
    z = latents(0); T = operator(z)
    rs = np.random.RandomState(42)
    trp = gen_pairs(TRAIN_C, 2000, rs)
    hop = [(a, b) for a in HELD_C for b in HELD_C if a != b]  # all 24x23 held-out pairs

    Ztr_a = z[[a for a, b in trp]]; Ztr_b = z[[b for a, b in trp]]
    Zho_a = z[[a for a, b in hop]]; Zho_b = z[[b for a, b in hop]]
    Ytr = np.stack([target(z, T, a, b) for a, b in trp])
    Yho = np.stack([target(z, T, a, b) for a, b in hop])

    # check 1: additive readout floors on held-out
    wa = ridge_fit(np.hstack([Ztr_a, Ztr_b]), Ytr)
    add_ho = r2(ridge_pred(wa, np.hstack([Zho_a, Zho_b])), Yho)

    # check 2: bilinear readout solves held-out  (feature = outer(z_a, z_b) flattened + linear)
    def bilfeat(A, B):
        outer = np.einsum("ni,nj->nij", A, B).reshape(len(A), -1)
        return np.hstack([outer, A, B])
    wb = ridge_fit(bilfeat(Ztr_a, Ztr_b), Ytr, lam=0.5)
    bil_ho = r2(ridge_pred(wb, bilfeat(Zho_a, Zho_b)), Yho)

    # check 3: non-commutativity — per output-dim, correlate t(a,b)[k] vs t(b,a)[k] ACROSS many pairs
    # (order-independent op => corr=1 per dim; genuine order-dependence => decorrelated). median over dims.
    ncp = gen_pairs(TRAIN_C, 800, np.random.RandomState(7))
    Tab = np.stack([target(z, T, a, b) for a, b in ncp])   # [P, D]
    Tba = np.stack([target(z, T, b, a) for a, b in ncp])   # [P, D]
    percol = [abs(np.corrcoef(Tab[:, k], Tba[:, k])[0, 1]) for k in range(D)]
    noncomm = float(np.median(percol))

    # check 4: name-byte leak -> z
    names = [syllable(c) for c in range(K)]
    NB = np.array([[b for b in n.encode()] for n in names], dtype=np.float64)
    NB = (NB - NB.mean(0)) / (NB.std(0) + 1e-9)
    # 5-fold-ish: fit on train concepts, test held
    wn = ridge_fit(NB[TRAIN_C], z[TRAIN_C], lam=1.0)
    nameleak = r2(ridge_pred(wn, NB[HELD_C]), z[HELD_C])

    # check 5: eval pairs never in corpus  (generator forbids held-held in TRAIN by construction)
    trp_set = set(trp); leaked = sum(1 for p in hop if p in trp_set)
    evalclean = (leaked == 0)

    checks = {
        "1_additive_heldout_r2": round(float(add_ho), 4),
        "2_bilinear_heldout_r2": round(float(bil_ho), 4),
        "3_noncommutativity_median_abscorr": round(noncomm, 4),
        "4_nameleak_r2": round(float(nameleak), 4),
        "5_eval_pairs_in_corpus": int(leaked),
    }
    passes = {
        "1_additive_le_0.10": add_ho <= 0.10,
        "2_bilinear_ge_0.90": bil_ho >= 0.90,
        "3_noncomm_le_0.30": noncomm <= 0.30,
        "4_nameleak_le_0.05": nameleak <= 0.05,
        "5_evalclean": evalclean,
    }
    valid = all(passes.values())
    out = {"probe": "ATD-0 VALID-ANCHOR (ground-truth z, no LM)", "K": K, "D": D,
           "n_train_pairs": len(trp), "n_heldout_pairs": len(hop),
           "checks": checks, "passes": {k: bool(v) for k, v in passes.items()},
           "harness_valid": bool(valid)}
    json.dump(out, open(os.path.join(HERE, "ATD0_RESULT.json"), "w"), ensure_ascii=False, indent=1)
    for k, v in checks.items():
        print(f"  {k:42s} = {v}   [{'PASS' if passes[[p for p in passes if p.startswith(k[0])][0]] else 'FAIL'}]")
    print(f"\nATD-0 harness_valid = {valid}")
    sys.exit(0 if valid else 3)

if __name__ == "__main__":
    main()
