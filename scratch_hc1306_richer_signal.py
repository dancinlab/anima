#!/usr/bin/env python3
# Hc_1306 — F-1306-SIGNAL: re-score the SAME Lane A on-chip traces (raw.npz par_fwd/con_fwd)
# with richer signals vs the 1-bit Hamming baseline, breakdown-floor guarded (Hc_1302 confound).
import numpy as np, json
rng = np.random.default_rng(20260602)
z = np.load("raw.npz", allow_pickle=True)
par = z["par_fwd"].astype(float)   # (25,32) analog forward spike-count trace, parallel encoding
con = z["con_fwd"].astype(float)   # (25,32) concat encoding
concept = np.array([i // 5 for i in range(25)])  # 5 concepts x 5 langs, concept-major

def dmat(X, kind):
    n = X.shape[0]
    if kind == "hamming":
        A = (X > np.median(X)).astype(float)
        return np.array([[np.sum(A[i] != A[j]) for j in range(n)] for i in range(n)])
    if kind == "l1":
        return np.sum(np.abs(X[:, None] - X[None]), 2)
    if kind == "cosine":
        Xn = X / (np.linalg.norm(X, axis=1, keepdims=True) + 1e-9)
        return 1 - Xn @ Xn.T

def margin(X, kind, lab):
    D = dmat(X, kind); n = X.shape[0]; w = []; b = []
    for i in range(n):
        for j in range(i + 1, n):
            (w if lab[i] == lab[j] else b).append(D[i, j])
    return (np.mean(b) - np.mean(w)) if (w and b) else 0.0

def phi_mip_proxy(X):
    # faithful-Phi proxy: gaussian MI across a balanced unit-bipartition of trace covariance.
    # Cholesky breakdown-floor guard (Hc_1302): if cov not PD, signal is at its floor.
    C = np.cov((X - X.mean(0)).T) + 1e-6 * np.eye(X.shape[1])
    try:
        np.linalg.cholesky(C)
    except np.linalg.LinAlgError:
        return None, True
    _, ld = np.linalg.slogdet(C)
    h = C.shape[0] // 2
    _, la = np.linalg.slogdet(C[:h, :h] + 1e-9 * np.eye(h))
    _, lb = np.linalg.slogdet(C[h:, h:] + 1e-9 * np.eye(C.shape[0] - h))
    return 0.5 * (la + lb - ld), False

print("trace", par.shape, "concept-major labels ok:", concept[:7].tolist())

# breakdown-floor check
for nm, X in [("parallel", par), ("concat", con)]:
    mi, broke = phi_mip_proxy(X)
    print("phi-MIP proxy %-9s = %s  cholesky_broke=%s" % (nm, "FLOOR" if mi is None else "%+.5f" % mi, broke))
pp, bp = phi_mip_proxy(par); pc, bc = phi_mip_proxy(con)
phi_floor = bp or bc
print("phi-MIP cross-encoding lift (par-con) = %s  at_floor=%s" %
      ("UNDECIDABLE" if phi_floor else "%+.5f" % (pp - pc), phi_floor))
print()

print("=== F-1306-SIGNAL: richer-signal re-score, lift = par_margin - con_margin, bootstrap CI n=2000 ===")
out = {}
for kind in ["hamming", "l1", "cosine"]:
    base = margin(par, kind, concept) - margin(con, kind, concept)
    lifts = []
    for _ in range(2000):
        idx = rng.integers(0, 25, 25); cc = concept[idx]
        lifts.append(margin(par[idx], kind, cc) - margin(con[idx], kind, cc))
    lo, hi = np.percentile(lifts, [2.5, 97.5])
    gt0 = bool(lo > 0)
    out[kind] = dict(lift=base, ci=[lo, hi], ci_lo_gt0=gt0)
    tag = "1bit-Hamming(BASELINE)" if kind == "hamming" else ("multibit-L1(RICHER)" if kind == "l1" else "cosine(RICHER)")
    print("%-22s LIFT=%+.4f  CI95=[%+.4f,%+.4f]  ci_lo_gt0=%s" % (tag, base, lo, hi, gt0))

print()
any_richer_gt0 = out["l1"]["ci_lo_gt0"] or out["cosine"]["ci_lo_gt0"]
print("ANY richer signal clears 0 (latent lift Hamming missed)?", any_richer_gt0)
print("phi-MIP at breakdown floor (undecidable branch)?", phi_floor)
if any_richer_gt0:
    print("F-1306 OUTCOME = (A) CONFIRMED — richer signal reveals latent lift")
elif not phi_floor:
    print("F-1306 OUTCOME = (B) CLOSED-NEGATIVE — richer signal ALSO shows no lift, above breakdown floor")
else:
    print("F-1306 OUTCOME = UN-DECIDABLE (phi proxy at floor)")
