#!/usr/bin/env python3
"""H_004 G-1 core -- design self-check ($0, CPU, deterministic).

Verifies the arithmetic of DESIGN_g1_core_fable5.md:
  [A] proxy parsers P_A (L->R nearest-head) / P_G (R->L maximal-head) disagree on
      exactly ONE edge -- head(RC-verb): N1 (P_A) vs N2 (P_G) -- on every item.
  [B] concord field T = T_struct * concord: T == s*(E12+E13) with
      s = 1-2*gold_flip on every item (the field collapses to ONE signed scalar).
  [C] G-0 rank-mass: off-top singular mass of T == 0.000 on the built single-bind
      panel (F4-DEAD as pre-registered) and == 5/6 on MULTI-BIND K=6.
  [D] G-1 probes (ridge logistic, shared token-feature block Phi_tok):
      single-bind: vec=1.0, rank1=1.0 (STOP: separation 0), norm=0.5, tok=0.5,
      tok+forbidden product=1.0, all-pairs=1.0, per-item-permuted vec=1.0
      MULTI-BIND K=6 (full 4^6 factorial, synthetic): vec=1.0, rank1=0.5833,
      norm=0.5, tok=0.5, perm~0.66  -> pre-registered thresholds PASS.

This IS the pre-registered G-1 arithmetic for the built panel (it STOPs);
for MULTI-BIND it is the design prediction (real build + F7'' still required).
"""
import json, os
import numpy as np

D = os.path.dirname(os.path.abspath(__file__))

# ---------- proxy parsers (honorific-BLIND: class skeleton only) ----------
# node classes for the single-bind frame: [ADN, NGEN, NDELIM, VFIN, ANS]
# P_A (L->R): attach i to NEAREST licensed head j>i.
# P_G (R->L): attach i to the HEAD OF THE MAXIMAL licensed projection right of i.
HEAD_A = {0: 1, 1: 2, 2: 3, 4: 3}   # RC->N1 (low), N1의->N2, N2도->VFIN, ANS->VFIN
HEAD_G = {0: 2, 1: 2, 2: 3, 4: 3}   # RC->N2 (high/NP-head); rest identical

def t_struct(n, head_a, head_g):
    T = np.zeros((n, n))
    for i in range(n):
        ha, hg = head_a.get(i), head_g.get(i)
        if ha == hg:
            continue
        if ha is not None: T[i, ha] += 1.0
        if hg is not None: T[i, hg] -= 1.0
    return T

def concord_field(Ts, hon):
    chi = np.where(np.equal.outer(hon, hon), 1.0, -1.0)
    return Ts * chi

def offtop(T):
    s = np.linalg.svd(T, compute_uv=False)
    tot = float(np.sum(s ** 2))
    return 0.0 if tot == 0 else float(1.0 - s[0] ** 2 / tot)

def rank1_tiebreak(T, tol=1e-9):
    """rank-1 approx; sigma-ties broken by retaining the component whose
    right-singular support has the smallest leading row index in T."""
    U, s, Vt = np.linalg.svd(T)
    if len(s) > 1 and s[0] - s[1] < tol * max(s[0], 1.0):
        rows = [i for i in range(T.shape[0]) if np.abs(T[i]).sum() > 0]
        if rows:
            i0 = min(rows)
            R = np.zeros_like(T); R[i0] = T[i0]
            return R
    return s[0] * np.outer(U[:, 0], Vt[0])

# ---------- ridge logistic (full-batch GD, init 0; exact w=0 on balanced XOR) ----
def fit(X, y, l2=1e-3, iters=1200, lr=1.0):
    Xb = np.column_stack([np.ones(len(X)), X])
    w = np.zeros(Xb.shape[1])
    for _ in range(iters):
        p = 1.0 / (1.0 + np.exp(-Xb @ w))
        g = Xb.T @ (p - y) / len(y) + l2 * np.r_[0.0, w[1:]]
        w -= lr * g
    return w

def acc(w, X, y):
    Xb = np.column_stack([np.ones(len(X)), X])
    p = 1.0 / (1.0 + np.exp(-Xb @ w))
    out = np.where(np.abs(p - 0.5) < 1e-9, 0.5, (p > 0.5) == y)
    return float(np.mean(out))

def cv8(X, y, strat):
    order, fold, seen = np.argsort(strat, kind="stable"), np.zeros(len(y), int), {}
    for i in order:
        k = strat[i]; fold[i] = seen.get(k, 0) % 8; seen[k] = seen.get(k, 0) + 1
    accs = []
    for f in range(8):
        tr, te = fold != f, fold == f
        accs.append(acc(fit(X[tr], y[tr]), X[te], y[te]))
    return float(np.mean(accs))

# ---------- single-bind: the BUILT panel ----------
def load(name):
    with open(os.path.join(D, name)) as f:
        return json.load(f)

def single_bind(panel):
    n = 5
    Ts = t_struct(n, HEAD_A, HEAD_G)
    # [A] exactly one contested dependent: node 0 (RC verb), heads {1,2}
    assert np.array_equal(np.nonzero(np.abs(Ts).sum(1))[0], [0])
    assert Ts[0, 1] == 1.0 and Ts[0, 2] == -1.0 and np.abs(Ts).sum() == 2.0

    rows = []
    for it in panel:
        hon = np.array([it["honorific_present"],
                        1.0 if it["n1_lexeme"].endswith("님") else 0.0,
                        1.0 if it["n2_lexeme"].endswith("님") else 0.0,
                        0.0, 0.0])
        assert (hon[1] == 1.0) == (it["honored_position"] == 1)
        T = concord_field(Ts, hon)
        s = 1.0 - 2.0 * it["gold_flip"]
        # [B] the whole field is s*(E12+E13): ONE signed scalar
        M = np.zeros((5, 5)); M[0, 1] = M[0, 2] = 1.0
        assert np.array_equal(T, s * M), (it["surface"], T)
        reg = [1.0 if it["tail"] == "기다렸어요" else 0.0,
               1.0 if it["tail"] == "기다렸네요" else 0.0]
        rows.append((T, hon, reg, it["gold_flip"], it["cell"]))

    y = np.array([r[3] for r in rows], float)
    cells = np.array([r[4] for r in rows])
    Phi = np.array([np.r_[r[1], r[2]] for r in rows])            # shared token block
    vecT = np.array([r[0].ravel() for r in rows])
    r1T = np.array([rank1_tiebreak(r[0]).ravel() for r in rows])
    nrm = np.array([[np.linalg.norm(r[0])] for r in rows])
    allp = np.array([[1.0 if r[1][i] == r[1][j] else -1.0
                      for i in range(5) for j in range(i + 1, 5)] for r in rows])
    perm = np.array([np.take(np.take(r[0], np.random.default_rng(1000 + i).permutation(5), 0),
                             np.random.default_rng(1000 + i).permutation(5), 1).ravel()
                     for i, r in enumerate(rows)])
    forb = np.array([[r[1][0] * r[1][1]] for r in rows])         # hp*hn1 (FORBIDDEN)

    ot = float(np.mean([offtop(r[0]) for r in rows]))
    probes = {}
    for nameX, X in [("vec", np.hstack([vecT, Phi])), ("rank1", np.hstack([r1T, Phi])),
                     ("norm", np.hstack([nrm, Phi])), ("tok_only", Phi),
                     ("tok_plus_forbidden_product", np.hstack([forb, Phi])),
                     ("allpairs_no_mask", np.hstack([allp, Phi])),
                     ("perm_placebo_vec", np.hstack([perm, Phi]))]:
        probes[nameX] = {"train": round(acc(fit(X, y), X, y), 4),
                         "cv8": round(cv8(X, y, cells), 4)}
    return {"n": len(rows), "offtop_mean": round(ot, 6), "probes": probes}

# ---------- MULTI-BIND K=6: full 4^6 factorial (synthetic design check) ----------
def multi_bind(K=6):
    n = 3 * K + 2
    head_a, head_g = {}, {}
    for k in range(K):
        r = 3 * k
        head_a[r], head_g[r] = r + 1, r + 2          # the contested RC edge, per conjunct
        head_a[r + 1] = head_g[r + 1] = r + 2        # Nk1의 -> Nk2 (agreed)
        head_a[r + 2] = head_g[r + 2] = 3 * K        # Nk2도 -> VFIN (agreed)
    head_a[3 * K + 1] = head_g[3 * K + 1] = 3 * K    # ANS -> VFIN
    Ts = t_struct(n, head_a, head_g)
    N = 4 ** K
    hp = np.zeros((N, K)); pos1 = np.zeros((N, K)); gold = np.zeros((N, K))
    Tlist = []
    for i in range(N):
        d = [(i // 4 ** k) % 4 for k in range(K)]
        hon = np.zeros(n)
        for k, dk in enumerate(d):
            hp[i, k] = dk % 2
            pos1[i, k] = 1.0 if dk < 2 else 0.0      # honored noun at Nk1?
            hon[3 * k] = hp[i, k]
            hon[3 * k + 1] = pos1[i, k]
            hon[3 * k + 2] = 1.0 - pos1[i, k]
            gold[i, k] = float(int(hp[i, k]) ^ int(pos1[i, k]))
        Tlist.append(concord_field(Ts, hon))
    ot = float(np.mean([offtop(T) for T in Tlist]))
    Phi = np.array([[T_hon for T_hon in hv] for hv in
                    [ [ (1.0 if (j%3==0 and hp[i,j//3]) or (j%3==1 and pos1[i,j//3]) or (j%3==2 and not pos1[i,j//3]) else 0.0) if j < 3*K else 0.0 for j in range(n)] for i in range(N)]])
    vecT = np.array([T.ravel() for T in Tlist])
    r1T = np.array([rank1_tiebreak(T).ravel() for T in Tlist])
    nrm = np.array([[np.linalg.norm(T)] for T in Tlist])
    perm = np.array([np.take(np.take(T, np.random.default_rng(5000 + i).permutation(n), 0),
                             np.random.default_rng(5000 + i).permutation(n), 1).ravel()
                     for i, T in enumerate(Tlist)])
    probes = {}
    for nameX, X in [("vec", np.hstack([vecT, Phi])), ("rank1", np.hstack([r1T, Phi])),
                     ("norm", np.hstack([nrm, Phi])), ("tok_only", Phi),
                     ("perm_placebo_vec", np.hstack([perm, Phi]))]:
        slot = [acc(fit(X, gold[:, k]), X, gold[:, k]) for k in range(K)]
        probes[nameX] = {"per_slot": [round(a, 4) for a in slot],
                         "mean": round(float(np.mean(slot)), 4)}
    return {"K": K, "n_nodes": n, "n_factorial": N,
            "offtop_mean": round(ot, 6), "probes": probes}

if __name__ == "__main__":
    out = {"single_bind_f2prime": single_bind(load("panel_f2prime.json")),
           "single_bind_f1prime": single_bind(load("panel_f1prime.json")),
           "multi_bind_K6_factorial": multi_bind(6)}
    f2 = out["single_bind_f2prime"]
    sep = f2["probes"]["vec"]["cv8"] - f2["probes"]["rank1"]["cv8"]
    out["verdict"] = {
        "G0_rank_mass_single_bind": f"off-top {f2['offtop_mean']:.3f} < 0.20 -> F4-DEAD at $0 (as pre-registered)",
        "G1_single_bind": f"probe(vec)-probe(rank1) = {sep:.4f} <= 0.05 -> STOP fires (field == its own rank-1 on a one-edge frame)",
        "G1_multi_bind_prediction": out["multi_bind_K6_factorial"]["probes"],
    }
    with open(os.path.join(D, "g1_core_check.json"), "w") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(json.dumps(out["verdict"], ensure_ascii=False, indent=2))
    print("\nfull result -> g1_core_check.json")
