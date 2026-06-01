#!/usr/bin/env python3
# Hc_1308 shuffle-NULL (full-rank so phi is FINITE -> comparison is meaningful).
# Key invariance: cov(X) is invariant under row(sample) permutation. A Gaussian
# covariance-Phi therefore CANNOT distinguish a temporally-integrated signal from
# its sample-shuffled NULL -> phi(orig) == phi(rowshuf) EXACTLY. That is the
# decisive variance-artifact discriminator: the metric measures only the static
# covariance, blind to sample-order (temporal) integration.
import numpy as np, sys, os
out_dir = sys.argv[1]
rng = np.random.default_rng(123)
C, N = 16, 64
# FULL-RANK integrated input: AR(1) over 16 latents (full rank), mild cross-mix.
lat = np.zeros((N, C))
for t in range(1, N):
    lat[t] = 0.8*lat[t-1] + rng.standard_normal(C)
M = np.eye(C) + 0.15*rng.standard_normal((C, C))   # full-rank mixing
X = (lat @ M + 0.3*rng.standard_normal((N, C))).astype(np.float64)
np.save(os.path.join(out_dir,"null_orig.npy"), X.T.copy())
perm = rng.permutation(N)
Xs = X[perm, :]                                     # row (sample) shuffle
np.save(os.path.join(out_dir,"null_rowshuf.npy"), Xs.T.copy())
Xc = np.empty_like(X)                               # per-channel independent shuffle
for c in range(C):
    Xc[:, c] = X[rng.permutation(N), c]
np.save(os.path.join(out_dir,"null_colindep.npy"), Xc.T.copy())
print(f"matrix_rank orig={np.linalg.matrix_rank(X,tol=1e-6)} (want 16)")
print(f"cov_identical_orig_vs_rowshuf={np.allclose(np.cov(X.T), np.cov(Xs.T))}")
print(f"cov_fro orig={np.linalg.norm(np.cov(X.T)):.4f} colindep={np.linalg.norm(np.cov(Xc.T)):.4f}")
print("NULL_OK")
