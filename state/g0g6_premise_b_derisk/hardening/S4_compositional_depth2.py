"""
S4_compositional_depth2 — hardening stress on premise-(b) forward-slot lever E1.

STRESS: compositional depth-2. E1 tested depth-1 ORDERED pairs bind(a,b). Here we test
NESTED depth-2 composition bind(bind(a,b),c) = ordered TRIPLES (3 distinct concepts, order
matters). Real recombination = composition depth: does the slot (role-address write/read)
recover HELD-OUT nested triples, while additive (order/depth-blind sum a+b+c) collapses?

Setup reused from E1.py (K orthogonal-ish Gaussian concepts, d dims, frozen closed-form
ridge readout, held-out ORDERED combos, shuffle+ablate controls). Only the stress (depth-2)
is changed. frozen-first, no tune-to-green, honest (degradation = result).

Slot forms tested (two, to be honest about the DPI-relevant width cost):
  (A) CONCAT slot  = E1-faithful write/read into distinct addresses: r=[a;b;c], width = 3*d.
      This is UNBOUNDED width (each depth level appends d dims) — trivially separable but a
      fixed-width trunk residual cannot afford to grow width per composition level.
  (B) FIXED-WIDTH superposition slot = realistic trunk constraint: r = Q0 a + Q1 b + Q2 c,
      Qi fixed random ORTHOGONAL positional transforms, ALL in width d (same as additive).
      Order preserved by distinct Qi; crosstalk accumulates with depth. Capacity-MATCHED to
      additive (both width d) => the fair test of whether the win is STRUCTURAL not just dims.

additive control = a+b+c (Qi = I, order-blind superposition, width d).
reach = held-out fraction with ALL positions' concepts identified correctly (order-dependent).
controls: shuffle (permute the positional roles per example -> destroy order),
          ablate  (drop the last position -> reach must collapse since it needs all 3).
"""
import numpy as np, json

rng = np.random.default_rng(0)
K, d = 16, 64
lam = 1e-2

C = rng.standard_normal((K, d)); C /= np.linalg.norm(C, axis=1, keepdims=True)

def rand_orth(dim, r):
    A = r.standard_normal((dim, dim))
    Q, _ = np.linalg.qr(A)
    return Q

# fixed positional orthogonal transforms (roles), one per slot position, up to depth 3
Qrng = np.random.default_rng(7)
Q = [rand_orth(d, Qrng) for _ in range(3)]

def make_tuples(depth, r):
    # all ORDERED tuples of `depth` DISTINCT concepts
    if depth == 2:
        t = np.array([(a, b) for a in range(K) for b in range(K) if a != b])
    else:
        t = [(a, b, c) for a in range(K) for b in range(K) for c in range(K)
             if a != b and a != c and b != c]
        t = np.array(t)
    return t[r.permutation(len(t))]

def onehot(ids):
    Y = np.zeros((len(ids), K)); Y[np.arange(len(ids)), ids] = 1.0; return Y

def ridge_fit(X, Y):
    G = X.T @ X + lam * np.eye(X.shape[1])
    return np.linalg.solve(G, X.T @ Y)

def build(tuples, depth, mode, swap_rng=None):
    cols = [C[tuples[:, j]] for j in range(depth)]   # list of (n,d) concept vecs per position
    n = len(tuples)
    if mode == "additive":                 # order-blind sum, width d
        return sum(cols)
    if mode == "concat":                   # E1-faithful: distinct addresses, width depth*d
        return np.concatenate(cols, axis=1)
    if mode == "concat_shuffle":           # permute the d-blocks per example
        out = np.concatenate(cols, axis=1).copy()
        for i in range(n):
            p = swap_rng.permutation(depth)
            out[i] = np.concatenate([cols[p[j]][i] for j in range(depth)])
        return out
    if mode == "concat_ablate":            # zero last position block
        z = [cols[j] if j < depth - 1 else np.zeros_like(cols[j]) for j in range(depth)]
        return np.concatenate(z, axis=1)
    if mode == "super":                    # fixed-width positional superposition, width d
        return sum(cols[j] @ Q[j].T for j in range(depth))
    if mode == "super_shuffle":            # permute which Q each position gets per example
        out = np.zeros((n, d))
        for i in range(n):
            p = swap_rng.permutation(depth)
            out[i] = sum(cols[j][i] @ Q[p[j]].T for j in range(depth))
        return out
    if mode == "super_ablate":             # drop last position's bound term
        return sum(cols[j] @ Q[j].T for j in range(depth - 1))
    raise ValueError(mode)

def reach(depth, mode, swap_seed=1):
    r = np.random.default_rng(42)
    tup = make_tuples(depth, r)
    n = len(tup); n_tr = int(0.70 * n)
    tr, he = tup[:n_tr], tup[n_tr:]
    # coverage: every concept appears in every position in train
    for j in range(depth):
        assert set(tr[:, j].tolist()) == set(range(K)), "coverage gap"
    sr = np.random.default_rng(swap_seed)
    Xtr = build(tr, depth, mode, sr)
    Ws = [ridge_fit(Xtr, onehot(tr[:, j])) for j in range(depth)]
    sr2 = np.random.default_rng(swap_seed + 100)
    Xhe = build(he, depth, mode, sr2)
    preds = [(Xhe @ Ws[j]).argmax(1) for j in range(depth)]
    allc = np.ones(len(he), bool)
    per = []
    for j in range(depth):
        ok = preds[j] == he[:, j]; per.append(float(np.mean(ok))); allc &= ok
    return dict(reach_all=float(np.mean(allc)), per_pos=per,
                n=n, n_tr=n_tr, n_he=n - n_tr)

res = {}
# depth-1 (E1 replication, same fixed-width methods) for the depth-degradation reference
res["d1_additive"] = reach(2, "additive")   # depth passed as tuple-arity; d1 == pairs (arity2)
# NOTE: arity-2 tuples == E1 depth-1 pairs. depth-2 nested == arity-3 triples below.
res["d1_concat"]   = reach(2, "concat")
res["d1_super"]    = reach(2, "super")
# depth-2 nested (arity-3 triples)
res["d2_additive"]        = reach(3, "additive")
res["d2_concat"]          = reach(3, "concat")
res["d2_concat_shuffle"]  = reach(3, "concat_shuffle")
res["d2_concat_ablate"]   = reach(3, "concat_ablate")
res["d2_super"]           = reach(3, "super")
res["d2_super_shuffle"]   = reach(3, "super_shuffle")
res["d2_super_ablate"]    = reach(3, "super_ablate")

# primary = E1-faithful concat slot at depth-2 vs additive at depth-2
slot_reach = res["d2_concat"]["reach_all"]
additive_reach = res["d2_additive"]["reach_all"]
# honest secondary = fixed-width (realistic trunk) superposition slot at depth-2
slot_fixedwidth_reach = res["d2_super"]["reach_all"]

random_all = 1.0 / (K * (K - 1) * (K - 2))
gap = slot_reach - additive_reach
gap_fixedwidth = slot_fixedwidth_reach - additive_reach

beats = slot_reach > additive_reach + 0.05
lift = slot_reach - additive_reach
sh = res["d2_concat_shuffle"]["reach_all"]
ab = res["d2_concat_ablate"]["reach_all"]
shuffle_collapses = (sh - additive_reach) < 0.4 * lift if lift > 0 else False
ablate_collapses  = (ab - additive_reach) < 0.4 * lift if lift > 0 else False

# fixed-width honesty: does the realistic (capacity-matched) slot ALSO beat additive?
fw_beats = slot_fixedwidth_reach > additive_reach + 0.05
fw_lift = slot_fixedwidth_reach - additive_reach
fw_sh = res["d2_super_shuffle"]["reach_all"]
fw_shuffle_collapses = (fw_sh - additive_reach) < 0.4 * fw_lift if fw_lift > 0 else False

# depth-degradation: how much does slot lose going depth1->depth2?
d1_concat = res["d1_concat"]["reach_all"]; d1_super = res["d1_super"]["reach_all"]
survives = bool(beats and shuffle_collapses and ablate_collapses and fw_beats)

out = {
    "condition": "S4_compositional_depth2",
    "params": {"K": K, "d": d, "ridge_lambda": lam, "random_all_pos_acc": random_all},
    "results": res,
    "slot_reach_concat_d2": float(slot_reach),
    "slot_reach_fixedwidth_super_d2": float(slot_fixedwidth_reach),
    "additive_reach_d2": float(additive_reach),
    "gap_concat": float(gap),
    "gap_fixedwidth": float(gap_fixedwidth),
    "beats_additive_concat": bool(beats),
    "shuffle_collapses_concat": bool(shuffle_collapses),
    "ablate_collapses_concat": bool(ablate_collapses),
    "fixedwidth_beats_additive": bool(fw_beats),
    "fixedwidth_shuffle_collapses": bool(fw_shuffle_collapses),
    "depth_degradation_concat_d1_to_d2": float(d1_concat - slot_reach),
    "depth_degradation_super_d1_to_d2": float(d1_super - slot_fixedwidth_reach),
    "survives": survives,
}
print(json.dumps(out, indent=2))
with open("/Users/mini/dancinlab/anima/state/g0g6_premise_b_derisk/hardening/S4_compositional_depth2.json", "w") as f:
    json.dump(out, f, indent=2)
