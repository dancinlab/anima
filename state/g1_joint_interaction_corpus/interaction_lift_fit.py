"""Offline joint interaction-lift fit (H_9255, Fable §3 Y1) — consumes the engine-
native NLL surface from `anima evaluate --interaction-lift` and asks whether the
303M model's per-cell NLL over the (A,B) content-pair grid carries non-additive
structure (interaction the model's output represents beyond additive main effects).

  additive:  Y[a,b] ≈ μ + α_a + β_b                 (main-effect least squares)
  joint:     Y[a,b] ≈ μ + α_a + β_b + <u_a, v_b>    (+ rank-R bilinear, ALS)
  lift = (RMSE_add − RMSE_joint) / RMSE_add on HELD-OUT cells (20% cells, seed=7)
  null = Freedman-Lane residual permutation ×200 (additive structure preserved,
         interaction destroyed) → lift_null 95pct.

Verdict: held-out lift > null95 → the model's NLL surface has non-additive (A,B)
interaction structure. This is Y1 of Fable's 해석 매트릭스 (pair with Y3 model-free
corpus). Engine-native (py 2-production numpy · a_eval_py_canonical). NOT a G1
verdict — a data-side alibi lens on the CONFIRMED-TERMINAL census (re-confirm/re-open).
"""
import sys, json, math
import numpy as np

SEED = 7
RANK = 3
HOLDOUT = 0.20
PERM = 200


def load_surface(path):
    d = json.load(open(path))
    cells = d["cells"]                       # {"a,b": [nll,...]}
    A = sorted({int(k.split(",")[0]) for k in cells})
    B = sorted({int(k.split(",")[1]) for k in cells})
    ai = {a: i for i, a in enumerate(A)}
    bi = {b: i for i, b in enumerate(B)}
    Y = np.full((len(A), len(B)), np.nan)
    mask = np.zeros((len(A), len(B)), dtype=bool)
    for k, v in cells.items():
        a, b = map(int, k.split(","))
        vv = np.array(v)
        Y[ai[a], bi[b]] = float(np.median(vv))    # robust mean
        mask[ai[a], bi[b]] = True
    return Y, mask, len(A), len(B)


def fit_additive(Y, mask, iters=300):
    """μ + α + β via alternating means over observed cells."""
    na, nb = Y.shape
    mu = np.nanmean(Y[mask])
    al = np.zeros(na); be = np.zeros(nb)
    for _ in range(iters):
        for i in range(na):
            m = mask[i]
            if m.any():
                al[i] = np.mean(Y[i, m] - mu - be[m])
        for j in range(nb):
            m = mask[:, j]
            if m.any():
                be[j] = np.mean(Y[m, j] - mu - al[m])
    pred = mu + al[:, None] + be[None, :]
    return pred


def fit_joint(Y, mask, rank, iters=300, reg=1e-3):
    """additive + <u_a,v_b> via ALS (co-optimized, no freeze-then-bolt · H_9225)."""
    na, nb = Y.shape
    rng = np.random.default_rng(SEED)
    U = rng.normal(size=(na, rank)) * 0.05
    V = rng.normal(size=(nb, rank)) * 0.05
    mu = np.nanmean(Y[mask]); al = np.zeros(na); be = np.zeros(nb)
    for _ in range(iters):
        inter = U @ V.T
        R = Y - inter
        for i in range(na):
            m = mask[i]
            if m.any():
                al[i] = np.mean(R[i, m] - mu - be[m])
        for j in range(nb):
            m = mask[:, j]
            if m.any():
                be[j] = np.mean(R[m, j] - mu - al[m])
        base = mu + al[:, None] + be[None, :]
        Rb = Y - base
        for i in range(na):
            m = mask[i]
            if m.sum() >= rank:
                Vm = V[m]
                U[i] = np.linalg.solve(Vm.T @ Vm + reg * np.eye(rank), Vm.T @ Rb[i, m])
        for j in range(nb):
            m = mask[:, j]
            if m.sum() >= rank:
                Um = U[m]
                V[j] = np.linalg.solve(Um.T @ Um + reg * np.eye(rank), Um.T @ Rb[m, j])
    return mu + al[:, None] + be[None, :] + U @ V.T


def rmse(pred, Y, cells):
    e = [(pred[i, j] - Y[i, j]) ** 2 for (i, j) in cells]
    return math.sqrt(sum(e) / len(e)) if e else 0.0


def held_out_lift(Y, mask, rank, rng):
    obs = [(i, j) for i in range(Y.shape[0]) for j in range(Y.shape[1]) if mask[i, j]]
    rng.shuffle(obs)
    nh = int(len(obs) * HOLDOUT)
    hold = obs[:nh]; train = obs[nh:]
    tm = np.zeros_like(mask);
    for (i, j) in train: tm[i, j] = True
    add = fit_additive(Y, tm)
    joint = fit_joint(Y, tm, rank)
    ra = rmse(add, Y, hold); rj = rmse(joint, Y, hold)
    return (ra - rj) / ra if ra > 0 else 0.0, ra, rj


if __name__ == "__main__":
    path = sys.argv[1]
    Y, mask, na, nb = load_surface(path)
    print(f"# interaction-lift fit · grid {na}x{nb} · {int(mask.sum())} observed cells")
    rng = np.random.default_rng(SEED)
    lift, ra, rj = held_out_lift(Y, mask, RANK, rng)
    print(f"# held-out: additive RMSE={ra:.4f} joint RMSE={rj:.4f} lift={lift:.4f}")

    # Freedman-Lane null: fit additive on ALL cells, permute residuals across cells,
    # re-measure held-out lift → the interaction is destroyed, main effects kept.
    add_full = fit_additive(Y, mask)
    resid = Y - add_full
    obs = [(i, j) for i in range(na) for j in range(nb) if mask[i, j]]
    rvals = np.array([resid[i, j] for (i, j) in obs])
    null = []
    for p in range(PERM):
        rp = np.random.default_rng(SEED + 1 + p).permutation(rvals)
        Yp = add_full.copy()
        for k, (i, j) in enumerate(obs):
            Yp[i, j] = add_full[i, j] + rp[k]
        l, _, _ = held_out_lift(Yp, mask, RANK, np.random.default_rng(SEED + 1000 + p))
        null.append(l)
    null.sort()
    n95 = null[int(0.95 * len(null))]
    verdict = "NON-ADDITIVE structure in model NLL surface (Y1 signal)" if lift > n95 \
        else "NO non-additive signal (additive-explained)"
    print(f"# Freedman-Lane null: lift95={n95:.4f} (mean {sum(null)/len(null):.4f})")
    print(f"# VERDICT: lift={lift:.4f} vs null95={n95:.4f} → {verdict}")
    json.dump({"grid": [na, nb], "n_cells": int(mask.sum()), "lift": lift,
               "rmse_add": ra, "rmse_joint": rj, "null95": n95,
               "null_mean": sum(null) / len(null), "signal": bool(lift > n95)},
              open("state/g1_joint_interaction_corpus/ilift_fit_result.json", "w"),
              ensure_ascii=False, indent=1)
