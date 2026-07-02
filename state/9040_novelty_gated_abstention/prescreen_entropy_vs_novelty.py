#!/usr/bin/env python3
# DIRECTIONAL numpy pre-screen (B4 novelty-gated honest abstention).
# NOT engine-native -> verdict here is DIRECTIONAL only (a_engine_native_learning).
# Purpose: validate the falsifier DESIGN before wiring the engine op.
#
# H_1142 wall recap: entropy signal AUROC(unfamiliar)=0.436 INVERTED, because next-byte
# entropy tracks LOCAL token-predictability (frequent patterns = false confidence) NOT
# global sequence-novelty. The signal CHOICE was wrong.
#
# Vector analog of H_1142's "common-word salad" (locally typical, globally novel):
#   familiar clusters at all-0 and all-1 corners.
#   unfamiliar "salad" = Hamming-balanced half-0/half-1 corners (IDENTICAL per-dim marginals,
#   yet the JOINT vector sits in an unoccupied gap far from every stored cell).
# WRONG signal (entropy-analog) = per-dim MARGINAL distance to the manifold centroid (ignores
#   joint geometry, like per-token entropy). RIGHT signal (novelty) = JOINT L2 recon-err to the
#   nearest stored prototype (the engine's vadapt_field_recon_err / SS Novelty lane).
import numpy as np

D = 6
rng = np.random.default_rng(20260702)

def jitter(v, n, s=0.06):
    return v[None, :] + rng.normal(0, s, size=(n, D))

# ---- substrate manifold: prototypes at the two familiar corners ----
protos = np.array([np.zeros(D), np.ones(D)], dtype=float)   # (0..0) and (1..1)

# ---- probes ----
n = 60
fam = np.vstack([jitter(np.zeros(D), n // 2), jitter(np.ones(D), n // 2)])   # near stored corners
# salad: exactly D/2 ones, D/2 zeros -> same per-dim marginals, joint gap corner
salad_bases = []
for _ in range(n):
    b = np.zeros(D); b[rng.choice(D, D // 2, replace=False)] = 1.0
    salad_bases.append(b)
unf = np.array(salad_bases) + rng.normal(0, 0.06, size=(n, D))

def recon_err(X):                         # JOINT L2 to nearest prototype = novelty (RIGHT)
    return np.min(np.linalg.norm(X[:, None, :] - protos[None, :, :], axis=2), axis=1)

centroid = protos.mean(0)
def marginal_dist(X):                     # per-dim |x-centroid| mean = entropy-analog (WRONG)
    return np.mean(np.abs(X - centroid[None, :]), axis=1)

def auroc(pos, neg):                      # Mann-Whitney, pos=unfamiliar (label 1)
    wins = sum((p > q) + 0.5 * (p == q) for p in pos for q in neg)
    return wins / (len(pos) * len(neg))

nov_pos, nov_neg = recon_err(unf), recon_err(fam)
mar_pos, mar_neg = marginal_dist(unf), marginal_dist(fam)

print(f"F1 novelty(joint recon-err) AUROC(unfamiliar) = {auroc(nov_pos, nov_neg):.3f}  (bar >= 0.70)")
print(f"F2 entropy-analog(marginal) AUROC(unfamiliar) = {auroc(mar_pos, mar_neg):.3f}  (reproduces H_1142 ~0.436 inverted/chance)")
print(f"   mean novelty  fam={nov_neg.mean():.3f} unf={nov_pos.mean():.3f}")
print(f"   mean marginal fam={mar_neg.mean():.3f} unf={mar_pos.mean():.3f}")

# F3 anti-Goodhart: untrained substrate = single seed cell at origin (no clonal cells formed)
proto_untrained = np.array([np.zeros(D)])
def recon_err_untrained(X):
    return np.min(np.linalg.norm(X[:, None, :] - proto_untrained[None, :, :], axis=2), axis=1)
u_pos, u_neg = recon_err_untrained(unf), recon_err_untrained(fam)
print(f"F3 novelty AUROC on UNTRAINED substrate (1 seed cell) = {auroc(u_pos, u_neg):.3f}  (bar <= 0.60 collapse)")
