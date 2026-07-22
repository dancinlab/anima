#!/usr/bin/env python3
"""H_9924 -- everything so far was a LINEAR PROBE. Does the lane's actual readout do the same?

H_9921 through H_9923 all fitted a linear decoder on the trunk hidden h and read the operator
off it. That establishes the information is linearly available. It says nothing about whether
the lane's real readout, trained by gradient descent on its own objective, finds it -- and the
whole prescription ("fit the readout with the offset varied") rests on exactly that step.

This measures the gap, for free, on dumps already taken. The toy reproduces the lane's readout
arithmetic verbatim from core/clms.py:183-190 for lane_type 3:

    v = a @ V_slots                      oracle => a = one_hot(target), so v = val[pol] - mean
    g = h @ W_g                          FROZEN, straight from the checkpoint
    z = gelu(concat([v, g]) @ W_h + b_h)
    s = z @ W_out                        answer read as the g/b margin

W_g is frozen exactly as --freeze-trunk would leave it; W_h, b_h and W_out are trained, which
is precisely the parameter set a lane-only retrain would move. Trained on the SAME held-out
offset splits the linear probe used, so the two are directly comparable.

RESULT, and the honest reading of it: the toy reaches only 0.72-0.77 on the offsets it TRAINED
on, where a linear probe on h reaches 1.0000. Two different things cause that, and they had to
be separated before anything could be read:

  1. REAL -- the frozen W_g projection loses operator information. A linear decoder fitted on
     g = h @ W_g reads 1.0000 at delta 0 but only 0.7375 to 0.9750 at shifted offsets, mean
     ~0.89. The lane never sees h; g is its actual input. So every number in H_9921 through
     H_9923 was measured upstream of the bottleneck the readout actually looks through.
  2. MY FAULT -- the toy lands BELOW even that degraded ceiling (0.72-0.77 against ~0.89), so
     it is not extracting what is present in g. Its held-out numbers are INSTRUMENT-INSUFFICIENT
     and are not read as evidence about what a trained readout can do.

The file is kept because (1) is worth having and because the gap between the toy and the
linear-on-g ceiling is the calibration a future version has to close first.
"""
import os, sys
import numpy as np

DUMPS = os.environ.get("H9924_DUMPS", "rot_a.npz,rot_b.npz,rot_c.npz")
WEIGHTS = os.environ.get("ANIMA_WEIGHTS", os.path.join(os.path.expanduser("~"), "anima-weights"))
CKPT = os.environ.get("H9924_CKPT", os.path.join(WEIGHTS, "store303_s2000.clm"))
D = list(range(9))
STEPS, LR, SEED = 4000, 3e-2, 7
G_BYTE, B_BYTE = 103, 98

PARTS = [p.strip() for p in DUMPS.split(",") if p.strip()]
miss = [p for p in PARTS if not os.path.exists(p)]
if miss:
    sys.exit("missing %s" % ", ".join(miss))
ZS = [np.load(p, allow_pickle=True) for p in PARTS]

# The engine's own loader, wherever it lives: the repo checkout's core/, or the installed
# anima_py package (the pool host has the wheel, not the repo). Never a machine-specific path.
_cands = [os.environ.get("ANIMA_CORE"),
          os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "core")]
try:
    import anima_py
    _cands.append(os.path.join(os.path.dirname(anima_py.__file__), "core"))
except Exception:
    pass
for _p in _cands:
    if _p and os.path.isdir(_p):
        sys.path.insert(0, _p)
import decode as clm

clms = clm.clm_load_weights(CKPT)["clms"]
W_g = np.asarray(clms["W_g"], dtype=np.float64)          # (d, d_g) FROZEN
val = np.asarray(clms["val"], dtype=np.float64)          # (2, d_s)
n_slot = int(clms["n_slot"])
d_g, d_s, r = W_g.shape[1], val.shape[1], int(clms["r"])
print("readout toy: d_g=%d d_s=%d r=%d n_slot=%d (W_g frozen from the ckpt)"
      % (d_g, d_s, r, n_slot))


def pick(d, op):
    rows = []
    for z in ZS:
        for k in sorted(z.files):
            if k.startswith("d%d|%s|" % (d, op)) and k.endswith("__last"):
                rows.append(np.asarray(z[k], dtype=np.float64).reshape(-1))
    return np.stack(rows)


rng = np.random.default_rng(SEED)
H = {d: {o: pick(d, o) for o in ("is", "not")} for d in D}
NPD = len(H[0]["is"])


def make_v(n, rng):
    """Oracle value term: a balanced 4/4 store, a = one_hot(target), lane_type 3 centring.
    v = val[pol_target] - mean(val[pols]); with 4/4 balance the mean is the same either way,
    so v takes exactly two values -- which is what the real lane sees under the oracle."""
    pol = rng.integers(0, 2, n)
    base = 0.5 * (val[0] + val[1])
    return val[pol] - base, pol


# W_g is FROZEN, so g = h @ W_g is computed ONCE per split rather than inside the loop.
# The first version recomputed a 1920x3784 by 3784x64 product every one of 4000 steps and the
# host killed it; the fix is not an approximation, it is the same arithmetic hoisted.
def forward(gg, vv, Wh, bh, Wo):
    z = np.tanh(np.concatenate([vv, gg], axis=1) @ Wh + bh)  # saturating fusion, as the lane has
    s = z @ Wo
    return s, z


G = {d: {o: (H[d][o] @ W_g) for o in ("is", "not")} for d in D}   # frozen projection, once


def build(ds):
    gs, vs, ys = [], [], []
    for d in ds:
        for op, opv in (("is", 0), ("not", 1)):
            gg = G[d][op]
            vv, pol = make_v(len(gg), rng)
            # gold = good iff (pol==0) XOR (op==not); margin target +1 for good, -1 for bad
            good = ((pol == 0) != (opv == 1))
            gs.append(gg); vs.append(vv); ys.append(np.where(good, 1.0, -1.0))
    return np.vstack(gs), np.vstack(vs), np.concatenate(ys)


def _step(cat, y, Wh, bh, Wo):
    z = np.tanh(cat @ Wh + bh)
    s = z @ Wo
    m = s[:, 0] - s[:, 1]
    p = 1.0 / (1.0 + np.exp(-np.clip(m * y, -60, 60)))
    gm = (-(1 - p) * y)[:, None] * np.array([1.0, -1.0])
    gWo = z.T @ gm / len(y)
    gz = gm @ Wo.T * (1 - z ** 2)
    return Wh - LR * (cat.T @ gz / len(y)), bh - LR * gz.mean(0), Wo - LR * gWo


def train(ds, shuffle=False):
    Xg, Xv, y = build(ds)
    if shuffle:
        y = y[rng.permutation(len(y))]
    cat = np.concatenate([Xv, Xg], axis=1)
    Wh = rng.normal(0, 0.05, (d_s + d_g, r))
    bh = np.zeros(r)
    Wo = rng.normal(0, 0.05, (r, 2))                     # 2 logits = the g/b answer pair
    for _ in range(STEPS):
        Wh, bh, Wo = _step(cat, y, Wh, bh, Wo)
    return Wh, bh, Wo


def score(Wh, bh, Wo, ds):
    Xg, Xv, y = build(ds)
    s, _ = forward(Xg, Xv, Wh, bh, Wo)
    return float((np.sign(s[:, 0] - s[:, 1]) == y).mean())


print()
print("  %-24s %10s %11s %10s" % ("train offsets", "seen-acc", "held-mean", "held-min"))
print("  " + "-" * 58)
for S in ([0, 1, 2, 3, 5, 7], [0, 1, 2, 4, 6, 8], [0, 2, 4, 6, 8], [0, 2, 5, 8], list(range(9))):
    HO = [d for d in D if d not in S]
    Wh, bh, Wo = train(S)
    seen = score(Wh, bh, Wo, S)
    held = [score(Wh, bh, Wo, [d]) for d in HO] or [float("nan")]
    print("  %-24s %10.4f %11.4f %10.4f"
          % (str(S), seen, float(np.mean(held)), min(held)))

# shuffled-label floor, same architecture and schedule
S = [0, 1, 2, 3, 5, 7]
HO = [d for d in D if d not in S]
null = []
for _ in range(5):
    Wh, bh, Wo = train(S, shuffle=True)
    null.append(float(np.mean([score(Wh, bh, Wo, [d]) for d in HO])))
print("\n  shuffled-label floor (same arch/schedule): mean %.4f  max %.4f"
      % (float(np.mean(null)), float(np.max(null))))
