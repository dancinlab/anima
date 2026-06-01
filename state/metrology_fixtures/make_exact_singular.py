#!/usr/bin/env python3
# Exact rank-deficient (zero jitter) + a ridge-sweep-target fixture.
import numpy as np, sys, os
out_dir = sys.argv[1]
rng = np.random.default_rng(7)
C, N = 16, 64
# EXACT rank-1: every channel a scalar multiple of one latent (perfectly composed)
z = rng.standard_normal((N, 1))
w = rng.standard_normal((1, C))
X1 = (z @ w).astype(np.float64)           # exact rank 1, no jitter
np.save(os.path.join(out_dir,"exact_rank01.npy"), X1.T.copy())
# EXACT rank-2
z2 = rng.standard_normal((N, 2)); w2 = rng.standard_normal((2, C))
X2 = (z2 @ w2).astype(np.float64)
np.save(os.path.join(out_dir,"exact_rank02.npy"), X2.T.copy())
# EXACT rank-8 (half)
z8 = rng.standard_normal((N, 8)); w8 = rng.standard_normal((8, C))
X8 = (z8 @ w8).astype(np.float64)
np.save(os.path.join(out_dir,"exact_rank08.npy"), X8.T.copy())
for nm,Xz in [("exact_rank01",X1),("exact_rank02",X2),("exact_rank08",X8)]:
    rk = np.linalg.matrix_rank(Xz, tol=1e-9)
    print(f"{nm} algebraic_rank={rk}")
print("EXACT_OK")
