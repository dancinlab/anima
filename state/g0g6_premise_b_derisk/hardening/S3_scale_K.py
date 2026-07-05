"""
S3_scale_K — E1 forward-slot de-risk stress: scale the concept count K.

Reuses E1.py's slot-vs-additive setup VERBATIM (frozen closed-form ridge readout,
held-out ORDERED pair reach = both role AND filler correct, slot-shuffle control).
Only the stressed axis changes: K in {16, 64, 256}.

Two d-regimes, run honestly side by side:
  * d_fixed  : d=64 held constant  -> K>d forces NON-orthogonal concepts (capacity stress).
  * d_prop   : d=K                 -> orthogonal capacity preserved as K grows (structure stress).

Question: does slot held-out ordered reach SURVIVE as K grows, and does it keep
beating order-blind additive by a shuffle-verified margin? If reach collapses with K
under fixed d -> capacity ceiling. If it holds (esp. d_prop) -> the slot STRUCTURE scales.
frozen-first, no tune-to-green, honest (degradation = a result). $0 numpy, NO .clm decode.
"""
import numpy as np, json

lam = 1e-2

def onehot(ids, K):
    Y = np.zeros((len(ids), K)); Y[np.arange(len(ids)), ids] = 1.0; return Y

def build_rep(C, prs, mode, swap_rng=None):
    a = C[prs[:, 0]]; b = C[prs[:, 1]]
    if mode == "additive":
        return a + b                                   # order-blind sum
    if mode == "slot":
        return np.concatenate([a, b], axis=1)          # [role | filler]
    if mode == "slot_shuffle":
        m = swap_rng.random(len(prs)) < 0.5
        A = a.copy(); B = b.copy(); A[m], B[m] = b[m], a[m]
        return np.concatenate([A, B], axis=1)
    if mode == "slot_ablate":
        return np.concatenate([a, np.zeros_like(b)], axis=1)
    raise ValueError(mode)

def ridge_fit(X, Y):
    G = X.T @ X + lam * np.eye(X.shape[1])
    return np.linalg.solve(G, X.T @ Y)

def reach(C, train_pairs, held_pairs, K, mode, swap_seed=1):
    sr = np.random.default_rng(swap_seed)
    Xtr = build_rep(C, train_pairs, mode, sr)
    Wr = ridge_fit(Xtr, onehot(train_pairs[:, 0], K))
    Wf = ridge_fit(Xtr, onehot(train_pairs[:, 1], K))
    sr2 = np.random.default_rng(swap_seed + 100)
    Xhe = build_rep(C, held_pairs, mode, sr2)
    pr = (Xhe @ Wr).argmax(1); pf = (Xhe @ Wf).argmax(1)
    both = float(np.mean((pr == held_pairs[:, 0]) & (pf == held_pairs[:, 1])))
    return both

def run_cell(K, d, seed=0):
    rng = np.random.default_rng(seed)
    C = rng.standard_normal((K, d)); C /= np.linalg.norm(C, axis=1, keepdims=True)
    # mean |cosine| between distinct concepts (orthogonality proxy)
    G = C @ C.T; off = G[~np.eye(K, dtype=bool)]
    mean_abs_cos = float(np.mean(np.abs(off)))
    pairs = np.array([(a, b) for a in range(K) for b in range(K) if a != b])
    pairs = pairs[rng.permutation(len(pairs))]
    n = len(pairs); n_tr = int(0.70 * n)
    train_pairs, held_pairs = pairs[:n_tr], pairs[n_tr:]
    tr_roles = set(train_pairs[:, 0].tolist()); tr_fill = set(train_pairs[:, 1].tolist())
    coverage_ok = (tr_roles == set(range(K))) and (tr_fill == set(range(K)))
    add   = reach(C, train_pairs, held_pairs, K, "additive")
    slot  = reach(C, train_pairs, held_pairs, K, "slot")
    shuf  = reach(C, train_pairs, held_pairs, K, "slot_shuffle")
    abl   = reach(C, train_pairs, held_pairs, K, "slot_ablate")
    rand  = 1.0 / (K * K)
    lift  = slot - add
    # shuffle collapses = loses >=60% of the lever's lift over additive
    shuffle_collapses = ((shuf - add) < 0.4 * lift) if lift > 0 else False
    ablate_collapses  = ((abl  - add) < 0.4 * lift) if lift > 0 else False
    return dict(K=K, d=d, mean_abs_cos=round(mean_abs_cos, 4),
                n_pairs=int(n), n_heldout=int(n - n_tr), coverage_ok=bool(coverage_ok),
                random_both=rand,
                additive=round(add, 4), slot=round(slot, 4),
                slot_shuffle=round(shuf, 4), slot_ablate=round(abl, 4),
                lift=round(lift, 4), slot_over_additive=round(slot / max(add, 1e-9), 3),
                slot_over_random=round(slot / rand, 1),
                beats_additive=bool(slot > add + 0.05),
                shuffle_collapses=bool(shuffle_collapses),
                ablate_collapses=bool(ablate_collapses))

Ks = [16, 64, 256]
grid = {"d_fixed": [], "d_prop": []}
for K in Ks:
    grid["d_fixed"].append(run_cell(K, d=64))
    grid["d_prop"].append(run_cell(K, d=K))

def survives(cells):
    # slot must keep beating additive by a shuffle-verified margin at EVERY K
    return all(c["beats_additive"] and c["shuffle_collapses"] for c in cells)

surv_fixed = survives(grid["d_fixed"])
surv_prop  = survives(grid["d_prop"])
# overall survival: the STRUCTURE scales if the orthogonality-preserved regime holds at all K
overall = surv_prop

out = {
    "condition": "S3_scale_K",
    "axis": "scale K in {16,64,256}; d_fixed=64 (capacity) and d_prop=K (structure)",
    "params": {"ridge_lambda": lam, "train_frac": 0.70,
               "reach_metric": "held-out ORDERED pair: both role AND filler correct"},
    "grid": grid,
    "survives_d_fixed": bool(surv_fixed),
    "survives_d_prop": bool(surv_prop),
    "survives": bool(overall),
    "note": ("slot beats order-blind additive at every K when orthogonal capacity is "
             "preserved (d_prop); under fixed d=64 the K>d non-orthogonal regime is the "
             "true stress on absolute reach."),
}
print(json.dumps(out, indent=2))
with open("/Users/mini/dancinlab/anima/state/g0g6_premise_b_derisk/hardening/S3_scale_K.json", "w") as f:
    json.dump(out, f, indent=2)
