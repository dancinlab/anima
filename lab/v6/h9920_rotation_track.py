#!/usr/bin/env python3
"""H_9920 -- is the operator's rotation SMOOTH in the offset, or arbitrary?

H_9919 established that the operator bit survives in the trunk hidden at shifted offsets but
along a different direction: a decoder fitted at the trained offset transfers at chance, while
one fitted inside each shifted condition recovers it at 0.75-0.81 against a measured shuffled
ceiling of 0.6875.

That makes the obvious repair -- an offset-invariant readout -- conditional on the SHAPE of
the rotation, which is what this measures:

  SMOOTH     the direction turns gradually with delta, so one aligned map could read every
             offset and the repair is realignment
  ARBITRARY  each delta lands somewhere unrelated, so alignment cannot work and the repair
             has to be a per-offset readout or a different representation

Per delta in 0..8, fit a within-condition linear operator decoder w_delta on 96 prompts
(48 `is`, 48 `not`), then read two similarities:

  adjacent  cos(w_delta, w_delta+1)     continuity
  baseline  cos(w_0, w_delta)           distance travelled from the trained offset

Two directions fitted in 3784 dimensions from 96 points are NOT orthogonal by chance, so the
floor is measured, not assumed: refit both members of a pair on SHUFFLED labels and take the
maximum cosine over 20 draws (chance-level-must-be-derived-per-metric).
"""
import os, sys
import numpy as np

DUMP = os.environ.get("H9920_DUMP", "rot_probe.npz")
DELTAS = range(0, 9)
SEED = 7

if not os.path.exists(DUMP):
    sys.exit("missing %s -- run `anima-py evaluate <ckpt> --dump-hidden rot_probe.json "
             "--out %s` first (engine-native tap)" % (DUMP, DUMP))

z = np.load(DUMP, allow_pickle=True)


def pick(d, op):
    ks = sorted(k for k in z.files
                if k.startswith("d%d|%s|" % (d, op)) and k.endswith("__last"))
    return np.stack([np.asarray(z[k], dtype=np.float64).reshape(-1) for k in ks])


def fit(A, B):
    X = np.vstack([A, B])
    Xc = X - X.mean(0)
    S = (Xc.T @ Xc) / max(1, len(X) - 1)
    lam = 1e-3 * np.trace(S) / S.shape[0]
    w = np.linalg.solve(S + lam * np.eye(S.shape[0]), A.mean(0) - B.mean(0))
    return w, 0.5 * (A.mean(0) @ w + B.mean(0) @ w)


def acc(A, B, w, t):
    return 0.5 * (float((A @ w > t).mean()) + float((B @ w <= t).mean()))


def cos(a, b):
    return float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-12))


rng = np.random.default_rng(SEED)
W, ACC = {}, {}
for d in DELTAS:
    A, B = pick(d, "is"), pick(d, "not")
    h = len(A) // 2
    w, t = fit(A[:h], B[:h])
    W[d] = w
    ACC[d] = acc(A[h:], B[h:], w, t)

# measured floor: cosine between two directions fitted on SHUFFLED labels
null = []
for _ in range(20):
    ws = []
    for d in (0, 1):
        A, B = pick(d, "is"), pick(d, "not")
        X = np.vstack([A, B])
        Xs = X[rng.permutation(len(X))]
        n, h = len(A), len(A) // 2
        w, _t = fit(Xs[:n][:h], Xs[n:][:h])
        ws.append(w)
    null.append(abs(cos(ws[0], ws[1])))
F = float(np.max(null))

# per-delta identifiability floor, same idiom as H_9919
acc_null = []
for _ in range(20):
    A, B = pick(0, "is"), pick(0, "not")
    X = np.vstack([A, B]); n, h = len(A), len(A) // 2
    Xs = X[rng.permutation(len(X))]
    w, t = fit(Xs[:n][:h], Xs[n:][:h])
    acc_null.append(acc(Xs[:n][h:], Xs[n:][h:], w, t))
AF = float(np.max(acc_null))

print("measured floors: cosine |cos| max over 20 shuffled fits = %.4f · "
      "within-acc shuffled max = %.4f" % (F, AF))
print()
print("  %-6s %10s %14s %14s" % ("delta", "within-acc", "cos(w0,wd)", "cos(wd-1,wd)"))
print("  " + "-" * 48)
ok = []
for d in DELTAS:
    base = cos(W[0], W[d])
    adj = cos(W[d - 1], W[d]) if d > 0 else float("nan")
    flag = "" if ACC[d] > AF else "   <- direction UNIDENTIFIED (acc at/below floor)"
    ok.append(ACC[d] > AF)
    print("  %-6d %10.4f %14.4f %14s%s"
          % (d, ACC[d], base, ("%.4f" % adj) if d else "--", flag))

print()
print("=" * 74)
ident = [d for d in DELTAS if ACC[d] > AF]
adj_ok = [cos(W[d - 1], W[d]) for d in DELTAS if d > 0 and d in ident and (d - 1) in ident]
base_seq = [cos(W[0], W[d]) for d in ident if d > 0]
mono = all(base_seq[i] >= base_seq[i + 1] - 1e-9 for i in range(len(base_seq) - 1))

if ACC[0] <= 0.90:
    print("INSTRUMENT-DEAD: delta=0 within-accuracy is %.4f, below the 0.90 gate." % ACC[0])
elif adj_ok and min(adj_ok) > F and mono:
    print("SMOOTH: every adjacent cosine clears the measured floor %.4f (min %.4f) and the"
          % (F, min(adj_ok)))
    print("distance from the trained direction falls monotonically. The rotation is gradual,")
    print("so a single realigned map could in principle read every offset -- the repair is")
    print("alignment, and the offset-invariant readout is worth prototyping.")
elif adj_ok and max(adj_ok) <= F:
    print("ARBITRARY: no adjacent pair clears the measured floor %.4f (max %.4f). Each offset" % (F, max(adj_ok)))
    print("puts the operator somewhere unrelated to its neighbour, so no alignment can carry")
    print("one map across offsets. The repair has to be a per-offset readout or a different")
    print("representation -- do NOT prototype realignment.")
elif adj_ok and min(adj_ok) > F:
    print("SMOOTH-LOCAL: adjacent cosines clear the floor %.4f (min %.4f) but the distance"
          % (F, min(adj_ok)))
    print("from the trained direction is NOT monotone, so local continuity does not buy global")
    print("alignment. Any prototype should be scoped to a local window of offsets.")
else:
    print("PENDING: identified deltas %s, adjacent cosines %s against floor %.4f. Register the"
          % (ident, ["%.3f" % a for a in adj_ok], F))
    print("matrix; do not headline a shape.")
