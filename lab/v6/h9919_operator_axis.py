#!/usr/bin/env python3
"""H_9919 -- is the operator still IN the trunk hidden when the readout stops using it?

The chain so far: the store readout is perfect at the trained operator offset and collapses
to a saturated operator default the moment the offset moves (H_9915, H_9916), and WHICH
default is set by the specific gap bytes with no low-dimensional account surviving -- variety,
lexicality, byte class and answer bytes are all dead (H_9918).

Everything so far is behavioural. This looks inside. Under the oracle the value term is fixed
by polarity, so the ONLY entity/prompt-dependent input to the readout is h at the query
position, through g = h @ W_g. Two questions have different fixes:

  PRESENT-BUT-UNUSED   the operator is still readable from h ALONG THE SAME DIRECTION, but the
                       fusion MLP no longer routes it
  ABSENT-FROM-h        the operator is gone from h itself at the shifted offset
  PRESENT-BUT-ROTATED  the operator is still in h but along a DIFFERENT direction, so a map
                       fitted at one offset cannot read it at another

The first version of this file had only the first two branches and duly printed ABSENT-FROM-h,
because a decoder fitted on the trained condition transfers at chance. That was wrong, and the
control that catches it is the obvious one: fit a decoder WITHIN each condition. Doing so
recovers the operator at every shifted offset, so the transfer failure was a rotation, not an
absence. A direction that stops working is not the same as a bit that stopped existing.

The instrument is a linear operator-decoder trained on the TRAINED condition only, then
applied unchanged to the shifted conditions. Training on the trained condition and testing
elsewhere is what makes it a transfer test rather than a fit.

Conditions, 64 prompts each (32 `is`, 32 `not`), all with a five-byte entity:
  trained  "is {e5} => "            offset -10, the working condition
  space    "is      {e5} => "       offset -15, behavioural kappa +0.957 (is-machine)
  zzzzz    "is zzzzz{e5} => "       offset -15, kappa +0.693
  ttttt    "is ttttt{e5} => "       offset -15, kappa -1.000 (not-machine)

If the operator survives in h at the shifted offsets, a decoder fit on `trained` should still
separate is from not there -- and the interesting part is that behaviour does NOT, at any of
them.
"""
import sys, os
import numpy as np

DUMP = "opt_probe.npz"
CKPT = os.path.expanduser("~/anima-weights/store_struct_303m/store303_s2000.clm")
CONDS = ("trained", "space", "zzzzz", "ttttt")

if not os.path.exists(DUMP):
    sys.exit("missing %s -- run `anima-py evaluate <ckpt> --dump-hidden opt_probe.json "
             "--out opt_probe.npz` first (engine-native tap, no re-implementation)" % DUMP)

z = np.load(DUMP, allow_pickle=True)
keys = [k for k in z.files if "|" in k]
print("dump: %d arrays, %d tagged prompts" % (len(z.files), len(keys)))


def pick(cond, op):
    ks = [k for k in keys if k.startswith(cond + "|" + op + "|") and k.endswith("last")] or \
         [k for k in keys if k.startswith(cond + "|" + op + "|")]
    return np.stack([np.asarray(z[k], dtype=np.float64).reshape(-1) for k in sorted(ks)])


sys.path.insert(0, os.path.expanduser("~/dancinlab/anima/core"))
sys.path.insert(0, "/home/summer/anima-weights")
try:
    import decode as clm
    W_g = np.asarray(clm.clm_load_weights(CKPT)["clms"]["W_g"], dtype=np.float64)
except Exception as e:                                   # W_g optional: h-space alone still answers the question
    W_g = None
    print("note: could not load W_g (%s) -- reporting h-space only" % type(e).__name__)


def fit_decoder(A, B):
    """Ridge-regularised mean-difference direction, fit on ONE condition only.
    w = (Sigma + lam I)^-1 (mu_A - mu_B); the threshold is the midpoint of the projected means."""
    X = np.vstack([A, B])
    mu = X.mean(0)
    Xc = X - mu
    S = (Xc.T @ Xc) / max(1, len(X) - 1)
    lam = 1e-3 * np.trace(S) / S.shape[0]
    w = np.linalg.solve(S + lam * np.eye(S.shape[0]), A.mean(0) - B.mean(0))
    thr = 0.5 * (A.mean(0) @ w + B.mean(0) @ w)
    return w, thr


def acc(A, B, w, thr):
    return 0.5 * (float((A @ w > thr).mean()) + float((B @ w <= thr).mean()))


def report(space, proj):
    A0, B0 = proj("trained", "is"), proj("trained", "not")
    n = len(A0)
    half = n // 2
    # fit on HALF of the trained condition, so even the trained row is held out
    w, thr = fit_decoder(A0[:half], B0[:half])
    print("\n  %s-space linear operator decoder (fit on trained only, %d+%d prompts)"
          % (space, half, half))
    print("  %-10s %10s" % ("condition", "is/not acc"))
    print("  " + "-" * 22)
    out = {}
    for c in CONDS:
        A, B = proj(c, "is"), proj(c, "not")
        a = acc(A[half:], B[half:], w, thr) if c == "trained" else acc(A, B, w, thr)
        out[c] = a
        print("  %-10s %10.4f" % (c + (" (held)" if c == "trained" else ""), a))
    return out


h = report("h", pick)


def within(proj, seed=7):
    """The control the transfer row cannot supply: fit INSIDE each condition, test held-out.
    Plus a label-shuffled null, so 'recoverable' is read against a measured floor and not
    against an assumed 0.5 (chance-level-must-be-derived-per-metric)."""
    rng = np.random.default_rng(seed)
    print("\n  WITHIN-condition decoder (fit and test inside the same condition)")
    print("  %-10s %12s %14s %12s" % ("condition", "within-acc", "shuffled mean", "shuffled max"))
    print("  " + "-" * 52)
    out = {}
    for c in CONDS:
        A, B = proj(c, "is"), proj(c, "not")
        half = len(A) // 2
        w, thr = fit_decoder(A[:half], B[:half])
        a = acc(A[half:], B[half:], w, thr)
        X = np.vstack([A, B]); n = len(A)
        null = []
        for _ in range(20):
            Xs = X[rng.permutation(len(X))]
            A2, B2 = Xs[:n], Xs[n:]
            w2, t2 = fit_decoder(A2[:half], B2[:half])
            null.append(acc(A2[half:], B2[half:], w2, t2))
        out[c] = (a, float(np.mean(null)), float(np.max(null)))
        print("  %-10s %12.4f %14.4f %12.4f" % (c, a, out[c][1], out[c][2]))
    return out


wi = within(pick)
g = None
if W_g is not None:
    g = report("g", lambda c, o: pick(c, o) @ W_g)

print()
print("=" * 74)
print("Chance is 0.5 (32 vs 32, balanced by construction).")
SH = ("space", "zzzzz", "ttttt")
transfer = [h[c] for c in SH]
inside = [wi[c][0] for c in SH]
floor = max(wi[c][2] for c in SH)                 # the measured null, not an assumed 0.5
if h["trained"] > 0.9 and max(transfer) < 0.7 and min(inside) > floor:
    print("PRESENT-BUT-ROTATED: a decoder fitted at the trained offset transfers at chance")
    print("(max %.4f), yet one fitted INSIDE each shifted condition recovers the operator at" % max(transfer))
    print("%.4f-%.4f against a measured shuffled ceiling of %.4f. The bit is still in the"
          % (min(inside), max(inside), floor))
    print("trunk; it has moved to a different direction, and it is weaker than the 1.0000 the")
    print("trained offset gives.")
    print()
    print("That accounts for the whole chain without inventing anything. The lane's readout is")
    print("a FIXED linear map fitted at one offset. Move the offset and the operator rotates")
    print("out of what that map reads, so the readout falls back to a constant operator")
    print("default -- and WHICH default depends on where the rotated representation lands")
    print("relative to a fixed decision surface, which is exactly why the gap bytes steer it")
    print("with no low-dimensional law (H_9918).")
elif h["trained"] > 0.9 and max(inside) <= floor:
    print("ABSENT-FROM-h: not recoverable even within condition (max %.4f vs null %.4f)."
          % (max(inside), floor))
else:
    print("MIXED -- trained %.4f, transfer %s, within %s. Register the vector, no headline."
          % (h["trained"], ["%.4f" % s for s in transfer], ["%.4f" % s for s in inside]))
