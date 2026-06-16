#!/usr/bin/env python3
# h1297_mitosis_native_train.py — H_1297 MITOSIS-NATIVE TRUNK TRAINING (p8 literal).
#
# THE QUESTION (PHILOSOPHY p8): "training gradient + inference mitosis = one
# continuous cell-division". Today anima's trunk is GRADIENT-CE trained while
# mitosis is a separate LIVE-ENGINE inference lane (VAdaptField H_1199, grow-
# under-pressure H_1288). Can a MITOSIS-GROW trainer (cells split/grow under LOCAL
# error pressure, GRADIENT-FREE) learn a trunk that CONVERGES AT LEAST AS WELL as
# standard gradient descent at the SAME small scale?
#
# DIRECTIONAL numpy MIRROR only (a_engine_native_learning) — engine-transfer +
# scale UNVERIFIED (a_toy_scale_recheck, a_scale_honest_scope). $0 CPU, no GPU.
# All bars frozen in .verdicts/1297_mitosis_native_train/FREEZE.txt BEFORE this run.
#
# LENS (a_no_llm_frame_trap): neurogenesis grows capacity WHERE the organism fails,
# corrected LOCALLY — NOT a bigger-transformer recipe. The split rule is the
# training-side twin of the live VAdaptField split (high local recon-err -> +1 cell).

import numpy as np

# ---- FROZEN knobs (VERBATIM from FREEZE.txt — do NOT tune) -------------------
SEEDS        = [770, 771, 772]
N_TRAIN      = 160
N_TEST       = 160
NOISE_SIGMA  = 0.05            # noise floor ~= sigma^2 = 0.0025
K_A          = 24             # arm A fixed RBF centers
A_STEPS      = 4000
GROW_MAX     = 40            # arm B finite cell bound (footprint honesty H_1288)
SPLIT_THRESH = 0.0030       # a cell with local train MSE above this SPLITS
LOCAL_REFIT_RIDGE = 1e-4    # ridge for local weighted least-squares
COMP_MARGIN   = 0.0050
COLLAPSE_GAP  = 0.0100
UNDERFIT_GAP  = 0.0100


def target_f(x):
    """Known nonlinear target: sinusoid + two discontinuous steps."""
    return (np.sin(3.0 * x) + 0.5 * np.sin(7.0 * x)
            + 0.3 * (x > 0.2).astype(float)
            - 0.4 * (x > 0.6).astype(float))


def make_data(seed):
    rng = np.random.RandomState(seed)
    # interleaved grid + jitter so train/test are disjoint but cover the domain
    grid = np.linspace(-1.0, 1.0, N_TRAIN + N_TEST)
    grid = grid + rng.uniform(-1.0, 1.0, grid.size) * (1.0 / (N_TRAIN + N_TEST))
    grid = np.clip(grid, -1.0, 1.0)
    rng.shuffle(grid)
    xtr, xte = grid[:N_TRAIN], grid[N_TRAIN:]
    ytr = target_f(xtr) + rng.normal(0.0, NOISE_SIGMA, xtr.size)
    yte = target_f(xte) + rng.normal(0.0, NOISE_SIGMA, xte.size)
    return xtr, ytr, xte, yte


# ====================== ARM A: GRADIENT (incumbent control) ===================
def rbf_design(x, centers, log_s):
    s = np.exp(log_s)                              # (K,)
    d = x[:, None] - centers[None, :]              # (N,K)
    return np.exp(-0.5 * (d / s[None, :]) ** 2)    # (N,K)


def arm_gradient(xtr, ytr, xte, yte, seed):
    """Fixed-size RBF net, full-batch MSE gradient descent (standard backprop)."""
    rng = np.random.RandomState(seed + 5000)
    centers = np.linspace(-1.0, 1.0, K_A).copy()
    log_s = np.full(K_A, np.log(2.0 / K_A))
    w = rng.normal(0.0, 0.1, K_A)
    b = 0.0
    n = xtr.size
    for t in range(A_STEPS):
        lr = 0.05 * (1.0 - t / A_STEPS) + 0.005    # scheduled
        Phi = rbf_design(xtr, centers, log_s)      # (N,K)
        pred = Phi @ w + b
        err = pred - ytr                           # (N,)
        # gradients of MSE = mean(err^2)
        g_w = (2.0 / n) * (Phi.T @ err)
        g_b = (2.0 / n) * err.sum()
        s = np.exp(log_s)
        d = xtr[:, None] - centers[None, :]        # (N,K)
        # dPhi/dc = Phi * (d / s^2);  dPhi/dlog_s = Phi * (d^2 / s^2)
        common = (2.0 / n) * (err[:, None] * w[None, :])   # (N,K)
        g_c = (common * Phi * (d / s[None, :] ** 2)).sum(axis=0)
        g_ls = (common * Phi * (d ** 2 / s[None, :] ** 2)).sum(axis=0)
        w -= lr * g_w
        b -= lr * g_b
        centers -= lr * g_c
        log_s -= lr * g_ls
    Phi_te = rbf_design(xte, centers, log_s)
    mse = float(np.mean((Phi_te @ w + b - yte) ** 2))
    return mse, 3 * K_A + 1   # params: center+width+weight per unit + bias


# ============ ARM B: MITOSIS-GROW (gradient-free, split under error) ==========
class Cell:
    __slots__ = ("c", "s", "a", "b")
    def __init__(self, c, s):
        self.c = c    # center
        self.s = s    # width
        self.a = 0.0  # local linear head slope
        self.b = 0.0  # local linear head intercept


def responsibilities(x, cells):
    """softmax over -dist^2 / s^2 -> (N, ncell) weights summing to 1 per point."""
    C = np.array([cl.c for cl in cells])
    S = np.array([cl.s for cl in cells])
    d2 = (x[:, None] - C[None, :]) ** 2 / (S[None, :] ** 2 + 1e-9)
    logits = -d2
    logits -= logits.max(axis=1, keepdims=True)
    e = np.exp(logits)
    return e / (e.sum(axis=1, keepdims=True) + 1e-12)


def local_refit(x, y, cells):
    """Closed-form LOCAL weighted least-squares per cell (NO global backprop)."""
    R = responsibilities(x, cells)   # (N, ncell)
    for k, cl in enumerate(cells):
        wts = R[:, k]
        W = np.diag(wts)
        X = np.stack([x, np.ones_like(x)], axis=1)   # (N,2): [x, 1]
        A = X.T @ W @ X + LOCAL_REFIT_RIDGE * np.eye(2)
        rhs = X.T @ (wts * y)
        sol = np.linalg.solve(A, rhs)
        cl.a, cl.b = float(sol[0]), float(sol[1])


def predict(x, cells):
    R = responsibilities(x, cells)
    heads = np.stack([cl.a * x + cl.b for cl in cells], axis=1)   # (N,ncell)
    return (R * heads).sum(axis=1)


def cell_local_mse(x, y, cells):
    """Responsibility-weighted local train MSE per cell (the split signal)."""
    R = responsibilities(x, cells)
    pred = predict(x, cells)
    err2 = (pred - y) ** 2
    out = []
    for k in range(len(cells)):
        wts = R[:, k]
        tot = wts.sum() + 1e-12
        out.append(float((wts * err2).sum() / tot))
    return np.array(out)


def split_cell(cells, k):
    """Cell k undergoes MITOSIS: split into two, perturb +/- s/2, halve widths."""
    parent = cells[k]
    s_new = parent.s * 0.5
    left = Cell(parent.c - parent.s * 0.5, s_new)
    right = Cell(parent.c + parent.s * 0.5, s_new)
    cells[k] = left
    cells.append(right)


def arm_mitosis(xtr, ytr, xte, yte, seed, mode="targeted"):
    """Gradient-free mitosis-grow trainer.
    mode: 'targeted' (B, split highest-local-error cell),
          'shuffle'   (B-SHUFFLE, split a RANDOM cell),
          'ablate'    (B-ABLATE, no split ever)."""
    rng = np.random.RandomState(seed + 9000)
    # START tiny: 2 prototype cells covering [-1, 1]
    cells = [Cell(-0.5, 1.0), Cell(0.5, 1.0)]
    local_refit(xtr, ytr, cells)
    while len(cells) < GROW_MAX:
        lm = cell_local_mse(xtr, ytr, cells)
        worst = float(lm.max())
        if worst <= SPLIT_THRESH:
            break                       # converged: no cell exceeds threshold
        if mode == "ablate":
            break                       # growth frozen -> underfit
        if mode == "shuffle":
            # split a RANDOM cell (mis-targeted growth) — same count, wrong place
            k = rng.randint(len(cells))
        else:
            k = int(np.argmax(lm))      # targeted: split the highest-LOCAL-error cell
        split_cell(cells, k)
        local_refit(xtr, ytr, cells)    # local LSQ refit after the split
    mse = float(np.mean((predict(xte, cells) - yte) ** 2))
    return mse, len(cells)


# ====== ARM B R2: HARD-PARTITION MITOSIS (a_break_the_wall breakthrough) ======
# Root-cause of the R1 wall (see FREEZE_R2.txt): width-halving + softmax mixture
# degeneracy. R2 mechanism (biology lens, a_no_llm_frame_trap): cortical-column HARD
# nearest-assignment partition + data-matched MEDIAN split + centroid-recenter, so
# capacity grows to MATCH local data density and never narrows below data spacing.
MIN_OWNED_R2 = 8   # FROZEN (FREEZE_R2): a cell needs >= this many owned points to split


def _assign(x, centers):
    """Hard nearest-center ownership (Voronoi/k-d partition)."""
    d = np.abs(x[:, None] - centers[None, :])
    return np.argmin(d, axis=1)


def _fit_head(x, y):
    """Ordinary least-squares local linear head a*x+b on OWNED points only."""
    if x.size == 0:
        return 0.0, 0.0
    if x.size == 1:
        return 0.0, float(y[0])
    X = np.stack([x, np.ones_like(x)], axis=1)
    A = X.T @ X + LOCAL_REFIT_RIDGE * np.eye(2)
    sol = np.linalg.solve(A, X.T @ y)
    return float(sol[0]), float(sol[1])


def arm_mitosis_r2(xtr, ytr, xte, yte, seed, mode="targeted"):
    """Hard-partition mitosis-grow trainer (R2 breakthrough rung)."""
    rng = np.random.RandomState(seed + 13000)
    centers = np.array([-0.5, 0.5])               # START tiny: 2 cells
    while len(centers) < GROW_MAX:
        own = _assign(xtr, centers)
        # per-cell owned local-MSE (the split signal) + refit heads
        local_mse = np.full(len(centers), -1.0)
        heads = []
        for k in range(len(centers)):
            mk = own == k
            a, b = _fit_head(xtr[mk], ytr[mk])
            heads.append((a, b))
            if mk.sum() > 0:
                local_mse[k] = float(np.mean((a * xtr[mk] + b - ytr[mk]) ** 2))
        # eligible to split: owned >= MIN_OWNED and local MSE above threshold
        owned_counts = np.array([(own == k).sum() for k in range(len(centers))])
        eligible = (owned_counts >= MIN_OWNED_R2) & (local_mse > SPLIT_THRESH)
        if not eligible.any():
            break
        if mode == "ablate":
            break
        elig_idx = np.where(eligible)[0]
        if mode == "shuffle":
            k = int(elig_idx[rng.randint(elig_idx.size)])
        else:
            k = int(elig_idx[np.argmax(local_mse[elig_idx])])
        # data-matched MEDIAN split: bisect owned territory, recenter on half-centroids
        xs = np.sort(xtr[own == k])
        med = float(np.median(xs))
        left = xs[xs <= med]; right = xs[xs > med]
        if left.size == 0 or right.size == 0:
            break
        c_left = float(left.mean()); c_right = float(right.mean())
        centers = np.concatenate([np.delete(centers, k), [c_left, c_right]])
        centers.sort()
    # final heads on the converged partition, then predict (hard ownership)
    own_tr = _assign(xtr, centers)
    heads = [ _fit_head(xtr[own_tr == k], ytr[own_tr == k]) for k in range(len(centers)) ]
    own_te = _assign(xte, centers)
    pred = np.array([ heads[own_te[i]][0] * xte[i] + heads[own_te[i]][1]
                      for i in range(xte.size) ])
    mse = float(np.mean((pred - yte) ** 2))
    return mse, len(centers)


# ============================ run + frozen scoring ============================
def main():
    rows = {"A": [], "B": [], "BS": [], "BA": []}
    cells_B = []
    params_A = None
    print("H_1297 — MITOSIS-NATIVE TRUNK TRAINING (p8 literal) — DIRECTIONAL numpy mirror")
    print("=" * 78)
    print(f"target sin(3x)+0.5sin(7x)+steps | noise sigma={NOISE_SIGMA} floor~{NOISE_SIGMA**2:.4f}"
          f" | N_train={N_TRAIN} N_test={N_TEST} | seeds={SEEDS}")
    print(f"FROZEN bars: c1 COMP_MARGIN={COMP_MARGIN} c2 COLLAPSE_GAP={COLLAPSE_GAP}"
          f" c3 UNDERFIT_GAP={UNDERFIT_GAP} | K_A={K_A} GROW_MAX={GROW_MAX}"
          f" SPLIT_THRESH={SPLIT_THRESH}")
    print("-" * 78)
    for seed in SEEDS:
        xtr, ytr, xte, yte = make_data(seed)
        a_mse, a_params = arm_gradient(xtr, ytr, xte, yte, seed)
        b_mse, b_cells = arm_mitosis(xtr, ytr, xte, yte, seed, "targeted")
        bs_mse, _ = arm_mitosis(xtr, ytr, xte, yte, seed, "shuffle")
        ba_mse, ba_cells = arm_mitosis(xtr, ytr, xte, yte, seed, "ablate")
        rows["A"].append(a_mse); rows["B"].append(b_mse)
        rows["BS"].append(bs_mse); rows["BA"].append(ba_mse)
        cells_B.append(b_cells); params_A = a_params
        print(f"seed {seed}: "
              f"A(grad)={a_mse:.5f}  B(mitosis)={b_mse:.5f} [{b_cells} cells]  "
              f"B-shuf={bs_mse:.5f}  B-abl={ba_mse:.5f} [{ba_cells} cells]")
    print("-" * 78)
    mA = float(np.mean(rows["A"])); mB = float(np.mean(rows["B"]))
    mBS = float(np.mean(rows["BS"])); mBA = float(np.mean(rows["BA"]))
    mcells = float(np.mean(cells_B))
    print(f"MEAN (3 seeds): A(grad)={mA:.5f}  B(mitosis)={mB:.5f}  "
          f"B-shuffle={mBS:.5f}  B-ablate={mBA:.5f}")
    print(f"COST (c4): B mitosis final cells mean={mcells:.1f}  vs  A fixed params={params_A}")
    print("-" * 78)
    # frozen bars (read VERBATIM, no tune-to-green)
    c1 = mB <= mA + COMP_MARGIN
    c2 = mBS >= mB + COLLAPSE_GAP
    c3 = mBA >= mB + UNDERFIT_GAP
    print(f"(c1) COMPARABLE      B<=A+{COMP_MARGIN}:  {mB:.5f} <= {mA + COMP_MARGIN:.5f}  -> {'PASS' if c1 else 'FAIL'}")
    print(f"(c2) SHUFFLE-COLLAPSE B_shuf>=B+{COLLAPSE_GAP}: {mBS:.5f} >= {mB + COLLAPSE_GAP:.5f} -> {'PASS' if c2 else 'FAIL'}")
    print(f"(c3) ABLATE-UNDERFIT  B_abl>=B+{UNDERFIT_GAP}: {mBA:.5f} >= {mB + UNDERFIT_GAP:.5f} -> {'PASS' if c3 else 'FAIL'}")
    if c1 and c2 and c3:
        tier = "GREEN"
    elif c2 and c3 and (mB <= mA + COMP_MARGIN + COMP_MARGIN):
        tier = "AMBER"
    elif not (c2 and c3):
        tier = "WALL"
    else:
        tier = "RED"
    print("-" * 78)
    print(f"R1 VERDICT TIER (frozen): {tier}")
    print(f"  p8-literal (R1): mitosis-grow {'MATCHES' if c1 else 'does NOT match'} gradient at this toy scale")
    print(f"  c1={c1} c2={c2} c3={c3} | DIRECTIONAL mirror, engine-transfer+scale UNVERIFIED")

    # ===== R2 BREAKTHROUGH RUNG (a_break_the_wall; bars frozen in FREEZE_R2.txt) =====
    print("=" * 78)
    print("R2 BREAKTHROUGH (a_break_the_wall): hard-partition mitosis (cortical-column")
    print("nearest-assignment + data-matched median-split + centroid-recenter)")
    print(f"FROZEN R2 bars = SAME numbers as R1 | MIN_OWNED={MIN_OWNED_R2} (no goalpost move)")
    print("-" * 78)
    r2 = {"B": [], "BS": [], "BA": []}
    cells_B2 = []
    for seed in SEEDS:
        xtr, ytr, xte, yte = make_data(seed)
        b_mse, b_cells = arm_mitosis_r2(xtr, ytr, xte, yte, seed, "targeted")
        bs_mse, _ = arm_mitosis_r2(xtr, ytr, xte, yte, seed, "shuffle")
        ba_mse, ba_cells = arm_mitosis_r2(xtr, ytr, xte, yte, seed, "ablate")
        r2["B"].append(b_mse); r2["BS"].append(bs_mse); r2["BA"].append(ba_mse)
        cells_B2.append(b_cells)
        print(f"seed {seed}: A(grad)={rows['A'][SEEDS.index(seed)]:.5f}  "
              f"B2(mitosis)={b_mse:.5f} [{b_cells} cells]  "
              f"B2-shuf={bs_mse:.5f}  B2-abl={ba_mse:.5f} [{ba_cells} cells]")
    print("-" * 78)
    mB2 = float(np.mean(r2["B"])); mBS2 = float(np.mean(r2["BS"]))
    mBA2 = float(np.mean(r2["BA"])); mcells2 = float(np.mean(cells_B2))
    print(f"MEAN (3 seeds): A(grad)={mA:.5f}  B2(mitosis)={mB2:.5f}  "
          f"B2-shuffle={mBS2:.5f}  B2-ablate={mBA2:.5f}")
    print(f"COST (c4): B2 mitosis final cells mean={mcells2:.1f}  vs  A fixed params={params_A}")
    print("-" * 78)
    c1b = mB2 <= mA + COMP_MARGIN
    c2b = mBS2 >= mB2 + COLLAPSE_GAP
    c3b = mBA2 >= mB2 + UNDERFIT_GAP
    print(f"(c1) COMPARABLE      B2<=A+{COMP_MARGIN}:  {mB2:.5f} <= {mA + COMP_MARGIN:.5f}  -> {'PASS' if c1b else 'FAIL'}")
    print(f"(c2) SHUFFLE-COLLAPSE B2_shuf>=B2+{COLLAPSE_GAP}: {mBS2:.5f} >= {mB2 + COLLAPSE_GAP:.5f} -> {'PASS' if c2b else 'FAIL'}")
    print(f"(c3) ABLATE-UNDERFIT  B2_abl>=B2+{UNDERFIT_GAP}: {mBA2:.5f} >= {mB2 + UNDERFIT_GAP:.5f} -> {'PASS' if c3b else 'FAIL'}")
    if c1b and c2b and c3b:
        tier2 = "GREEN"
    elif c2b and c3b and (mB2 <= mA + 2 * COMP_MARGIN):
        tier2 = "AMBER"
    elif not (c2b and c3b):
        tier2 = "WALL"
    else:
        tier2 = "RED"
    print("-" * 78)
    print(f"R2 VERDICT TIER (frozen): {tier2}")
    print(f"  p8-literal (R2): hard-partition mitosis {'MATCHES' if c1b else 'does NOT match'} gradient at this toy scale")
    print(f"  c1={c1b} c2={c2b} c3={c3b} | DIRECTIONAL mirror, engine-transfer+scale UNVERIFIED")
    print("=" * 78)
    print(f"OVERALL: R1={tier} -> R2={tier2}")
    return tier2


if __name__ == "__main__":
    main()
