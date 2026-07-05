"""
S2_nonorthogonal_noise — E1 slot-vs-additive de-risk under a REALISTIC dictionary.

Stress vs E1 (which used clean orthogonal-ish random Gaussian concepts):
  (1) NON-ORTHOGONAL concepts: correlated Gaussian dictionary with mean pairwise
      cosine overlap ~0.2 (real learned embeddings are NOT orthogonal — they share
      a dominant common direction / anisotropy). Built by mixing each atom with a
      shared direction, weight tuned so measured mean|cos| ~ 0.2.
  (2) ADDITIVE NOISE: at read time each concept vector gets iid Gaussian noise
      (sigma * unit) added — models embedding jitter / channel noise. Applied to
      BOTH slot and additive, identical draws, so the comparison stays fair.
      Interpretability: noisy-clean cosine = 1/sqrt(1 + d*sigma^2).
        sigma 0.05 -> cos 0.93 (mild jitter) ; 0.15 -> 0.64 (aggressive, recoverable)
        sigma 0.30 -> 0.38 (noise floor, task unlearnable for ALL forms).

Everything else = E1 verbatim: K ordered concepts, frozen closed-form ridge readout
fit on train pairs only, held-out ORDERED pair reach (both role AND filler correct),
slot_shuffle + slot_ablate + outer controls. NO tuning of representation. frozen-first,
no tune-to-green, honesty (degradation = a result).

survives=True iff at the discriminating stress point (mean cos~0.2, aggressive-but-
recoverable noise sigma=0.15) slot still beats additive by a meaningful margin AND
slot_shuffle collapses toward additive. If additive catches up or slot crumbles under
non-orthogonality -> survives=False (the GPU-HOLD basis, a complete result).
"""
import numpy as np, json

def make_dict(rng, K, d, target_cos):
    """Correlated dictionary: atom = sqrt(1-w) z_i + sqrt(w) shared, unit-normed.
    Tune w so mean pairwise |cos| ~ target_cos."""
    shared = rng.standard_normal(d); shared /= np.linalg.norm(shared)
    def build(w):
        Cc = np.sqrt(1 - w) * rng2.standard_normal((K, d)) + np.sqrt(w) * shared[None, :]
        Cc /= np.linalg.norm(Cc, axis=1, keepdims=True)
        return Cc
    lo, hi = 0.0, 0.95
    for _ in range(40):
        w = 0.5 * (lo + hi)
        rng2 = np.random.default_rng(12345)
        Cc = build(w)
        iu = np.triu_indices(K, 1)
        mc = float(np.mean(np.abs((Cc @ Cc.T)[iu])))
        if mc < target_cos: lo = w
        else: hi = w
    return Cc, mc

def onehot(ids, K):
    Y = np.zeros((len(ids), K)); Y[np.arange(len(ids)), ids] = 1.0; return Y

def run(target_cos, sigma, seed=0, K=16, d=64, lam=1e-2):
    rng = np.random.default_rng(seed)
    C, meas_cos = make_dict(rng, K, d, target_cos)
    pairs = np.array([(a, b) for a in range(K) for b in range(K) if a != b])
    pairs = pairs[rng.permutation(len(pairs))]
    n = len(pairs); n_tr = int(0.70 * n)
    train_pairs, held_pairs = pairs[:n_tr], pairs[n_tr:]
    assert set(train_pairs[:, 0]) == set(range(K)) and set(train_pairs[:, 1]) == set(range(K)), "coverage gap"

    def rep(prs, mode, nz_rng, swap_rng=None):
        a = C[prs[:, 0]].copy(); b = C[prs[:, 1]].copy()
        if sigma > 0:
            a = a + sigma * nz_rng.standard_normal(a.shape)
            b = b + sigma * nz_rng.standard_normal(b.shape)
        if mode == "additive": return a + b
        if mode == "slot":     return np.concatenate([a, b], axis=1)
        if mode == "slot_shuffle":
            m = swap_rng.random(len(prs)) < 0.5
            A = a.copy(); B = b.copy(); A[m], B[m] = b[m], a[m]
            return np.concatenate([A, B], axis=1)
        if mode == "slot_ablate":
            return np.concatenate([a, np.zeros_like(b)], axis=1)
        if mode == "outer":
            return (a[:, :, None] * b[:, None, :]).reshape(len(prs), -1)
        if mode == "outer_shuffle":
            m = swap_rng.random(len(prs)) < 0.5
            A = a.copy(); B = b.copy(); A[m], B[m] = b[m], a[m]
            return (A[:, :, None] * B[:, None, :]).reshape(len(prs), -1)
        raise ValueError(mode)

    def ridge_fit(X, Y):
        return np.linalg.solve(X.T @ X + lam * np.eye(X.shape[1]), X.T @ Y)

    def both_acc(mode, swap_seed=1):
        Xtr = rep(train_pairs, mode, np.random.default_rng(swap_seed + 7000),
                  np.random.default_rng(swap_seed))
        Wr = ridge_fit(Xtr, onehot(train_pairs[:, 0], K))
        Wf = ridge_fit(Xtr, onehot(train_pairs[:, 1], K))
        Xhe = rep(held_pairs, mode, np.random.default_rng(swap_seed + 8000),
                  np.random.default_rng(swap_seed + 100))
        pr = (Xhe @ Wr).argmax(1); pf = (Xhe @ Wf).argmax(1)
        return dict(both=float(np.mean((pr == held_pairs[:, 0]) & (pf == held_pairs[:, 1]))),
                    role=float(np.mean(pr == held_pairs[:, 0])),
                    filler=float(np.mean(pf == held_pairs[:, 1])))

    res = {m: both_acc(m) for m in
           ["additive", "slot", "slot_shuffle", "slot_ablate", "outer", "outer_shuffle"]}
    return dict(measured_mean_cos=meas_cos, n=int(n), n_tr=int(n_tr),
                n_he=int(n - n_tr), random_both=1.0 / (K * K), res=res)

def noisy_clean_cos(sigma, d=64):
    return 1.0 / np.sqrt(1.0 + d * sigma * sigma)

# ---- discriminating realistic stress point: mean|cos|~0.2 + aggressive-but-recoverable
#      noise sigma=0.15 (noisy-clean cos ~0.64). sigma>=0.3 is a NOISE FLOOR where BOTH
#      forms collapse (task unlearnable for anyone; additive never overtakes slot) -> not
#      a discriminating stress. Report the discriminating point + full sweep honestly. ----
TARGET_COS, SIGMA = 0.20, 0.15
main = run(TARGET_COS, SIGMA)
res = main["res"]

slot_reach = res["slot"]["both"]; additive_reach = res["additive"]["both"]
shuffle_reach = res["slot_shuffle"]["both"]; ablate_reach = res["slot_ablate"]["both"]
gap = slot_reach - additive_reach; lift = gap
shuffle_collapses = (shuffle_reach - additive_reach) < 0.4 * lift if lift > 0 else False
ablate_collapses = (ablate_reach - additive_reach) < 0.4 * lift if lift > 0 else False
slot_beats_additive = slot_reach > additive_reach + 0.05
survives = bool(slot_beats_additive and gap > 0.10 and shuffle_collapses)

# additive never overtakes slot at ANY (cos,sigma)? key structural invariant
sweep = []
additive_ever_wins = False
for tc in [0.0, 0.1, 0.2, 0.4]:
    for sg in [0.0, 0.05, 0.10, 0.15, 0.30, 0.5]:
        r = run(tc, sg); rr = r["res"]
        g = rr["slot"]["both"] - rr["additive"]["both"]
        if rr["additive"]["both"] > rr["slot"]["both"] + 1e-9: additive_ever_wins = True
        sweep.append(dict(target_cos=tc, meas_cos=round(r["measured_mean_cos"], 3),
                          sigma=sg, noisy_clean_cos=round(noisy_clean_cos(sg), 3),
                          slot=round(rr["slot"]["both"], 3),
                          additive=round(rr["additive"]["both"], 3),
                          shuffle=round(rr["slot_shuffle"]["both"], 3),
                          gap=round(g, 3)))

out = {
    "cond": "S2_nonorthogonal_noise",
    "stress_point": {"target_mean_cos": TARGET_COS, "measured_mean_cos": round(main["measured_mean_cos"], 4),
                     "noise_sigma": SIGMA, "noisy_clean_cos": round(noisy_clean_cos(SIGMA), 3)},
    "params": {"K": 16, "d": 64, "ridge_lambda": 1e-2, "n_pairs": main["n"],
               "n_train": main["n_tr"], "n_heldout": main["n_he"], "random_both_acc": main["random_both"]},
    "results_both_role_filler": res,
    "slot_reach": slot_reach, "additive_reach": additive_reach,
    "shuffle_control_reach": shuffle_reach, "ablate_control_reach": ablate_reach,
    "gap_slot_minus_additive": gap,
    "slot_beats_additive": slot_beats_additive,
    "shuffle_collapses": bool(shuffle_collapses), "ablate_collapses": bool(ablate_collapses),
    "additive_ever_beats_slot": additive_ever_wins,
    "survives": survives,
    "sweep": sweep,
}
print(json.dumps(out, indent=2))
with open("/Users/mini/dancinlab/anima/state/g0g6_premise_b_derisk/hardening/S2_nonorthogonal_noise.json", "w") as f:
    json.dump(out, f, indent=2)
