"""
E1 — CE-deleted forward-slot reachability probe ($0 numpy, DIRECTIONAL).

DPI premise under test: next-byte = fn((a)CE-trained, (b)FEEDFORWARD, (c)single-trunk).
E1 attacks premise-(b): replace additive residual combine (a+b, order-blind) with an
EXPLICIT forward binding SLOT (gated write/read into distinct role/filler addresses, or
outer-product TPR). Claim: an explicit slot lets a FROZEN structure linearly recover
held-out ORDERED combinations that additive combine cannot, and slot ablation collapses it.

Method (per task spec):
  - K atomic concepts = random Gaussian d-vectors (dictionary C).
  - combination = ORDERED pair (role a, filler b), a!=b.
  - train = subset of pairs; held-out = pairs never seen in training.
  - representation forms (frozen / closed-form, NO tuning of the representation):
      * additive   (control)      : r = a + b                      (order-blind sum)
      * slot-concat(lever E1)      : r = [a ; b]  (gated write/read: role slot | filler slot)
      * outer-prod (lever E1 alt)  : r = vec(a b^T) (TPR)
  - controls on the LEVER:
      * shuffle : randomly swap the two slots per example (destroy role assignment)
      * ablate  : zero the filler slot at read time (remove one slot) -> binding must collapse
  - readout = FROZEN linear ridge from r -> onehot(role) and r -> onehot(filler),
    fit ONLY on train pairs, evaluated on HELD-OUT pairs. Same readout treatment for all.
  - reach = held-out fraction with BOTH role AND filler concept identified correctly
    (order-dependent -> requires real binding). unreach/random both-acc = 1/K^2.

GO iff  lever_reach > additive_reach  AND  shuffle collapses (->~additive) AND ablation collapses.
This is a DIRECTIONAL GPU-fire signal, not a terminal verdict. frozen-first, no tune-to-green, p7.
"""
import numpy as np, json

rng = np.random.default_rng(0)
K, d = 16, 64
lam = 1e-2

# ---- atomic concept dictionary (random Gaussian, unit norm) ----
C = rng.standard_normal((K, d))
C /= np.linalg.norm(C, axis=1, keepdims=True)

# ---- all ordered pairs (role a, filler b), a != b ----
pairs = np.array([(a, b) for a in range(K) for b in range(K) if a != b])
perm = rng.permutation(len(pairs))
pairs = pairs[perm]
n = len(pairs)
n_tr = int(0.70 * n)
train_pairs, held_pairs = pairs[:n_tr], pairs[n_tr:]

# sanity: every concept appears as BOTH role and filler in train (else decode undefined)
tr_roles = set(train_pairs[:, 0].tolist()); tr_fill = set(train_pairs[:, 1].tolist())
assert tr_roles == set(range(K)) and tr_fill == set(range(K)), "coverage gap"

def onehot(ids):
    Y = np.zeros((len(ids), K)); Y[np.arange(len(ids)), ids] = 1.0; return Y

def build_rep(prs, mode, swap_rng=None):
    a = C[prs[:, 0]]; b = C[prs[:, 1]]
    if mode == "additive":
        return a + b
    if mode == "slot":                    # [role | filler]
        return np.concatenate([a, b], axis=1)
    if mode == "slot_shuffle":            # randomly swap the two slots per example
        m = swap_rng.random(len(prs)) < 0.5
        A = a.copy(); B = b.copy()
        A[m], B[m] = b[m], a[m]
        return np.concatenate([A, B], axis=1)
    if mode == "slot_ablate":             # zero the filler slot (remove one slot)
        return np.concatenate([a, np.zeros_like(b)], axis=1)
    if mode == "outer":                   # TPR: vec(a b^T)
        return (a[:, :, None] * b[:, None, :]).reshape(len(prs), -1)
    if mode == "outer_shuffle":           # symmetrize -> destroy order
        m = swap_rng.random(len(prs)) < 0.5
        A = a.copy(); B = b.copy(); A[m], B[m] = b[m], a[m]
        return (A[:, :, None] * B[:, None, :]).reshape(len(prs), -1)
    raise ValueError(mode)

def ridge_fit(X, Y):
    G = X.T @ X + lam * np.eye(X.shape[1])
    return np.linalg.solve(G, X.T @ Y)

def both_acc(mode, swap_seed=1):
    sr = np.random.default_rng(swap_seed)
    Xtr = build_rep(train_pairs, mode, sr)
    # role/filler decoders share the representation; fit on train only
    Wr = ridge_fit(Xtr, onehot(train_pairs[:, 0]))
    Wf = ridge_fit(Xtr, onehot(train_pairs[:, 1]))
    sr2 = np.random.default_rng(swap_seed + 100)
    Xhe = build_rep(held_pairs, mode, sr2)
    pr = (Xhe @ Wr).argmax(1); pf = (Xhe @ Wf).argmax(1)
    both = np.mean((pr == held_pairs[:, 0]) & (pf == held_pairs[:, 1]))
    role = np.mean(pr == held_pairs[:, 0]); fill = np.mean(pf == held_pairs[:, 1])
    return dict(both=float(both), role=float(role), filler=float(fill))

random_both = 1.0 / (K * K)
res = {
    "additive":     both_acc("additive"),
    "slot":         both_acc("slot"),
    "slot_shuffle": both_acc("slot_shuffle"),
    "slot_ablate":  both_acc("slot_ablate"),
    "outer":        both_acc("outer"),
    "outer_shuffle":both_acc("outer_shuffle"),
}

lever_reach = max(res["slot"]["both"], res["outer"]["both"])
best_form = "slot" if res["slot"]["both"] >= res["outer"]["both"] else "outer"
additive_reach = res["additive"]["both"]
shuffle_reach = res["slot_shuffle"]["both"] if best_form == "slot" else res["outer_shuffle"]["both"]
ablate_reach = res["slot_ablate"]["both"]

beats = lever_reach > additive_reach + 0.05
# shuffle "collapses" = falls back near the additive floor (loses >=60% of lever's lift)
lift = lever_reach - additive_reach
shuffle_collapses = (shuffle_reach - additive_reach) < 0.4 * lift if lift > 0 else False
ablate_collapses = (ablate_reach - additive_reach) < 0.4 * lift if lift > 0 else False
verdict = "GO" if (beats and shuffle_collapses and ablate_collapses) else "NO-GO"

out = {
    "lever_id": "E1",
    "params": {"K": K, "d": d, "ridge_lambda": lam,
               "n_pairs": int(n), "n_train": int(n_tr), "n_heldout": int(n - n_tr),
               "random_both_acc": random_both},
    "results_both_role_filler": res,
    "best_lever_form": best_form,
    "heldout_reach": float(lever_reach),
    "additive_control_reach": float(additive_reach),
    "shuffle_control_reach": float(shuffle_reach),
    "ablate_control_reach": float(ablate_reach),
    "lift_over_additive": float(lift),
    "beats_additive": bool(beats),
    "shuffle_collapses": bool(shuffle_collapses),
    "ablate_collapses": bool(ablate_collapses),
    "directional_verdict": verdict,
}
print(json.dumps(out, indent=2))
with open("/Users/mini/dancinlab/anima/state/g0g6_premise_b_derisk/E1.json", "w") as f:
    json.dump(out, f, indent=2)
