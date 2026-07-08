"""residual-lift probe (Fable divergence #8) — the decisive gamma scout.

Idea (from the DPI meta-diagnosis): every dead G1 lever failed because the
primary loss stayed additive-solvable, so a "binding" aux term was satisfied
trivially (FORM) without earning the joint. This probe makes additive a
LITERAL frozen control and asks whether the RESIDUAL (y - additive_pred)
carries held-out recombination signal that a low-rank bilinear combiner can
recover. shuffle-collapse is the built-in THEATER control.

What it demonstrates (toy · DIRECTIONAL, method-validation only — not a 303M
verdict; real corpus + engine-native decode is the GPU-gated follow-on):
  1. positive control: interaction_strength=0  -> residual is pure additive
     leftover -> held-out bilinear lift ~ 0 (FORM alive, no false-positive).
  2. earned bind: interaction_strength>0 with LOW-RANK structure -> residual
     lift > 0 on held-out (unseen A×B) cells -> genuine recombination.
  3. destruction control: shuffle B within pairs -> interaction becomes noise
     -> lift collapses to ~0 (proves the lift was the joint, not overfit).

Held-out = whole (A,B) combination cells removed from train. A model can only
score on them by GENERALIZING structure (recombination), never by cell lookup.
"""
import numpy as np

SEED = 12345
K = 12          # levels per concept (A has K, B has K)
RANK = 3        # true interaction rank
N_PER_CELL = 40 # samples per observed (A,B) cell
NOISE = 0.15
HOLDOUT_FRAC = 0.30


def make_world(rng, interaction_strength):
    """Ground-truth generator: y = a_main[A] + b_main[B] + s * <u[A], v[B]>."""
    a_main = rng.normal(size=K)
    b_main = rng.normal(size=K)
    # low-rank bilinear interaction: U (K,RANK) x V (K,RANK)
    U = rng.normal(size=(K, RANK))
    V = rng.normal(size=(K, RANK))
    inter = (U @ V.T) * interaction_strength      # (K,K) non-additive part
    return a_main, b_main, inter


def sample(rng, a_main, b_main, inter, cells):
    A, B, Y = [], [], []
    for (i, j) in cells:
        for _ in range(N_PER_CELL):
            y = a_main[i] + b_main[j] + inter[i, j] + rng.normal() * NOISE
            A.append(i); B.append(j); Y.append(y)
    return np.array(A), np.array(B), np.array(Y)


def fit_additive(A, B, Y):
    """Best least-squares additive model: y ~ onehot(A) + onehot(B)."""
    X = np.concatenate([np.eye(K)[A], np.eye(K)[B]], axis=1)  # (N, 2K)
    w = np.linalg.solve(X.T @ X + 1e-6 * np.eye(2 * K), X.T @ Y)
    return w


def additive_pred(w, A, B):
    X = np.concatenate([np.eye(K)[A], np.eye(K)[B]], axis=1)
    return X @ w


def fit_lowrank_residual(A, B, resid, rank, iters=400, reg=1e-3):
    """Recover residual as <p[A], q[B]> via alternating ridge (low-rank bilinear
    combiner). Generalizes to UNSEEN cells iff the residual is low-rank."""
    rng = np.random.default_rng(SEED + 7)
    P = rng.normal(size=(K, rank)) * 0.1
    Q = rng.normal(size=(K, rank)) * 0.1
    for _ in range(iters):
        for i in range(K):
            m = A == i
            if not m.any():
                continue
            Qb = Q[B[m]]                      # (n_i, rank)
            P[i] = np.linalg.solve(Qb.T @ Qb + reg * np.eye(rank), Qb.T @ resid[m])
        for j in range(K):
            m = B == j
            if not m.any():
                continue
            Pa = P[A[m]]
            Q[j] = np.linalg.solve(Pa.T @ Pa + reg * np.eye(rank), Pa.T @ resid[m])
    return P, Q


def fit_joint(A, B, Y, rank, iters=300, reg=1e-3):
    """Jointly fit y = a[A] + b[B] + <P[A],Q[B]> (additive + bilinear together).
    Removes the frozen-additive contamination confound: additive effects and the
    low-rank interaction are estimated simultaneously, so neither steals the
    other's variance on held-out cells."""
    rng = np.random.default_rng(SEED + 11)
    a = np.zeros(K); b = np.zeros(K)
    P = rng.normal(size=(K, rank)) * 0.1
    Q = rng.normal(size=(K, rank)) * 0.1
    for _ in range(iters):
        inter = np.sum(P[A] * Q[B], axis=1)
        r = Y - inter
        w = fit_additive(A, B, r)
        a, b = w[:K], w[K:]
        r2 = Y - (a[A] + b[B])                # residual for bilinear
        for i in range(K):
            m = A == i
            if not m.any():
                continue
            Qb = Q[B[m]]
            P[i] = np.linalg.solve(Qb.T @ Qb + reg * np.eye(rank), Qb.T @ r2[m])
        for j in range(K):
            m = B == j
            if not m.any():
                continue
            Pa = P[A[m]]
            Q[j] = np.linalg.solve(Pa.T @ Pa + reg * np.eye(rank), Pa.T @ r2[m])
    return a, b, P, Q


def rmse(pred, y):
    return float(np.sqrt(np.mean((pred - y) ** 2)))


def run(interaction_strength, shuffle_B=False):
    rng = np.random.default_rng(SEED)
    a_main, b_main, inter = make_world(rng, interaction_strength)

    all_cells = [(i, j) for i in range(K) for j in range(K)]
    rng.shuffle(all_cells)
    n_hold = int(len(all_cells) * HOLDOUT_FRAC)
    hold_cells = all_cells[:n_hold]
    train_cells = all_cells[n_hold:]

    Atr, Btr, Ytr = sample(rng, a_main, b_main, inter, train_cells)
    Ate, Bte, Yte = sample(rng, a_main, b_main, inter, hold_cells)

    if shuffle_B:
        # destroy the pairing: B no longer matched to its A -> interaction = noise
        Btr = rng.permutation(Btr)

    # 1) frozen additive control
    w = fit_additive(Atr, Btr, Ytr)
    add_te = additive_pred(w, Ate, Bte)
    add_rmse_hold = rmse(add_te, Yte)

    # 2) residual -> low-rank bilinear combiner
    resid_tr = Ytr - additive_pred(w, Atr, Btr)
    P, Q = fit_lowrank_residual(Atr, Btr, resid_tr, RANK)
    resid_pred_te = np.sum(P[Ate] * Q[Bte], axis=1)
    comb_rmse_hold = rmse(add_te + resid_pred_te, Yte)

    lift = add_rmse_hold - comb_rmse_hold  # >0 = residual model helps held-out

    # 3) joint-fit variant (no frozen-additive contamination)
    aj, bj, Pj, Qj = fit_joint(Atr, Btr, Ytr, RANK)
    joint_te = aj[Ate] + bj[Bte] + np.sum(Pj[Ate] * Qj[Bte], axis=1)
    joint_rmse_hold = rmse(joint_te, Yte)
    joint_lift = add_rmse_hold - joint_rmse_hold

    return dict(strength=interaction_strength, shuffle=shuffle_B,
                add_rmse=add_rmse_hold, comb_rmse=comb_rmse_hold, lift=lift,
                joint_rmse=joint_rmse_hold, joint_lift=joint_lift)


if __name__ == "__main__":
    print(f"# residual-lift probe (K={K} rank={RANK} holdout={HOLDOUT_FRAC})")
    print("# lift = additive_heldout_RMSE - (additive+residual)_heldout_RMSE   [>0 = earned bind]\n")
    header = (f"{'strength':>9} {'shuffle':>8} {'add_rmse':>9} "
              f"{'2stage_lift':>12} {'joint_lift':>11}  verdict(joint)")
    print(header)
    print("-" * len(header))
    for s in [0.0, 0.5, 1.0, 2.0]:
        for sh in [False, True]:
            r = run(s, shuffle_B=sh)
            v = ""
            if r["strength"] == 0.0 and not sh:
                v = "POS-CTRL (expect ~0)"
            elif not sh:
                v = "EARNED BIND" if r["joint_lift"] > 0.1 else ("weak" if r["joint_lift"] > 0.03 else "FLOOR")
            elif sh:
                v = "THEATER-CTRL (expect collapse)"
            print(f"{r['strength']:>9.1f} {str(r['shuffle']):>8} "
                  f"{r['add_rmse']:>9.3f} {r['lift']:>12.3f} {r['joint_lift']:>11.3f}  {v}")
    print("\n# 2stage_lift = frozen-additive then residual bilinear (Fable #8 literal).")
    print("# joint_lift  = additive+bilinear fit together (confound-free).")
    print("# read: joint no-shuffle strength>0 lift>0 = recombination recoverable;")
    print("#       shuffle rows must collapse ->~0; strength=0 must be ~0 (no false-positive).")
