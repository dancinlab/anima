#!/usr/bin/env python3
"""H_9921 -- can ONE fixed readout cover every offset, or does each need its own?

H_9920 at full resolution: the operator reads at 1.0000 from the trunk hidden at every offset
delta 0..8, while behaviour there is 0.51-0.60. The information loss is exactly zero and the
failure is entirely on the reading side. It also found the per-offset decoder directions to be
near-orthogonal -- cos(w0, wd) sits at or below a measured floor of 0.1387 everywhere -- which
makes the obvious worry concrete: if the nine directions are mutually unrelated, maybe no
single fixed map can serve them all, and the repair would need a per-offset readout.

That worry is testable with data already on disk, and this tests it. Fit ONE linear decoder on
the pooled training halves of all nine offsets, then score each offset's held-out half with
that same map. Chance is 0.5 by construction; the floor is measured by refitting the pooled
decoder on shuffled labels.

Near-orthogonal per-offset directions do NOT imply that no shared map exists: in 3784
dimensions a single w can hold an adequate projection onto nine mutually near-orthogonal
directions at once. Which of those two worlds we are in is an empirical question, not one to
reason out.
"""
import os, sys
import numpy as np

DUMPS = os.environ.get("H9921_DUMPS", "rot_a.npz,rot_b.npz,rot_c.npz")
DELTAS = range(0, 9)
SEED = 7

PARTS = [p.strip() for p in DUMPS.split(",") if p.strip()]
missing = [p for p in PARTS if not os.path.exists(p)]
if missing:
    sys.exit("missing %s -- take the hidden dumps first with `anima-py evaluate <ckpt> "
             "--dump-hidden <spec>.json --out <dump>.npz`" % ", ".join(missing))
ZS = [np.load(p, allow_pickle=True) for p in PARTS]


def pick(d, op):
    rows = []
    for z in ZS:
        for k in sorted(z.files):
            if k.startswith("d%d|%s|" % (d, op)) and k.endswith("__last"):
                rows.append(np.asarray(z[k], dtype=np.float64).reshape(-1))
    if not rows:
        sys.exit("no prompts for delta=%d op=%s" % (d, op))
    return np.stack(rows)


def fit(A, B):
    X = np.vstack([A, B])
    Xc = X - X.mean(0)
    S = (Xc.T @ Xc) / max(1, len(X) - 1)
    lam = 1e-3 * np.trace(S) / S.shape[0]
    w = np.linalg.solve(S + lam * np.eye(S.shape[0]), A.mean(0) - B.mean(0))
    return w, 0.5 * (A.mean(0) @ w + B.mean(0) @ w)


def acc(A, B, w, t):
    return 0.5 * (float((A @ w > t).mean()) + float((B @ w <= t).mean()))


trA, trB, teA, teB = [], [], {}, {}
for d in DELTAS:
    A, B = pick(d, "is"), pick(d, "not")
    h = len(A) // 2
    trA.append(A[:h]); trB.append(B[:h]); teA[d] = A[h:]; teB[d] = B[h:]

w, t = fit(np.vstack(trA), np.vstack(trB))
print("  ONE pooled decoder (fitted on the train halves of ALL nine offsets)")
print("  %-6s %14s" % ("delta", "held-out acc"))
print("  " + "-" * 22)
accs = []
for d in DELTAS:
    a = acc(teA[d], teB[d], w, t)
    accs.append(a)
    print("  %-6d %14.4f" % (d, a))

rng = np.random.default_rng(SEED)
X = np.vstack([np.vstack(trA), np.vstack(trB)])
n = len(np.vstack(trA))
null = []
for _ in range(20):
    Xs = X[rng.permutation(len(X))]
    w2, t2 = fit(Xs[:n], Xs[n:])
    null.append(float(np.mean([acc(teA[d], teB[d], w2, t2) for d in DELTAS])))
F = float(np.max(null))

print()
print("  pooled mean %.4f · min %.4f  |  shuffled-fit mean %.4f · max %.4f"
      % (float(np.mean(accs)), min(accs), float(np.mean(null)), F))
print()
print("=" * 74)
if min(accs) > F:
    print("ONE MAP SUFFICES. A single linear readout, fitted across offsets, reads the operator")
    print("at %.4f-%.4f everywhere, against a measured shuffled ceiling of %.4f. The per-offset"
          % (min(accs), max(accs), F))
    print("directions being near-orthogonal did NOT prevent a shared map -- 3784 dimensions")
    print("leave room for one w to project onto all nine.")
    print()
    print("So the failure is a FITTING-RANGE problem, not a representational one. No alignment,")
    print("no rotation compensation, no trunk retraining, no architecture change is implied.")
    print("The lane's readout has to be fitted with the offset VARIED, and the drill corpus")
    print("held it at exactly one value.")
else:
    print("NO SHARED MAP: pooled accuracy falls to %.4f at its worst, against floor %.4f."
          % (min(accs), F))
    print("A single fixed readout cannot serve every offset; a per-offset or non-linear readout")
    print("is required, and the fitting-range prescription does not survive.")
