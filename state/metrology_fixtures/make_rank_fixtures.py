#!/usr/bin/env python3
# METROLOGY Hc_1307 — rank/condition-number boundary fixtures for phi_proxy_native.
# Emits 16ch x 64samp matrices (channels-major orientation handled by the .hexa helper)
# of controlled rank r = 16,12,8,4,2,1. Higher correlation => lower effective rank =>
# more "composed/integrated". Deterministic (seed=42).
import numpy as np, sys, os
out_dir = sys.argv[1] if len(sys.argv) > 1 else "."
os.makedirs(out_dir, exist_ok=True)
rng = np.random.default_rng(42)
C, N = 16, 64
eps = 1e-3   # fixed jitter floor; control axis is effective rank r -> cov kappa
print(f"# C={C} N={N} eps={eps}")
print("rank cov_kappa min_eig max_eig rank_np_tol1e-6")
for r in [16, 12, 8, 4, 2, 1]:
    base = rng.standard_normal((N, C))
    U, S, Vt = np.linalg.svd(base, full_matrices=False)
    S2 = S.copy()
    if r < len(S2):
        S2[r:] = 0.0
    Xr = (U * S2) @ Vt                 # exact algebraic rank min(r,C)
    Xr = Xr / (np.std(Xr) + 1e-12)     # unit scale (no overflow)
    X = (Xr + eps * rng.standard_normal((N, C))).astype(np.float64)
    # save (C, N) channels-major (rows in {16,32,..}) to match helper heuristic
    np.save(os.path.join(out_dir, f"rank_{r:02d}.npy"), X.T.copy())
    cov = np.cov(X.T)
    eig = np.clip(np.linalg.eigvalsh(cov), 1e-30, None)
    kappa = eig.max() / eig.min()
    rk = np.linalg.matrix_rank(X, tol=1e-6)
    print(f"{r:4d} {kappa:.4e} {eig.min():.4e} {eig.max():.4e} {rk}")
print("FIXTURES_OK")
