"""H_9926 -- the 0.89 bottleneck is not a constraint on the real retrain: W_g trains too.

H_9924 measured a ceiling by fitting a linear decoder on g = h @ W_g with W_g FROZEN, and
H_9925 read the readout toy against that ceiling. Freezing W_g was the right isolation for
those questions, but it is NOT what a lane retrain does: cli/train.py:2351 shows --freeze-trunk
sets requires_grad on every parameter whose name starts with "clms.", and W_g is one of them.

So the real retrain moves the bottleneck itself, and the 0.89 ceiling never applied to it.

This measures what that buys. Same lane arithmetic, same calibrated step size, same held-out
splits -- the only change is that W_g is trainable, initialised at the checkpoint's own W_g
exactly as a continuation from that checkpoint would be. Two splits are enough for the
comparison that matters: one dense, one sparse, since H_9925 found coverage does not separate
them in the lane's own coordinates.

  frozen W_g   (H_9925)  held-mean 0.7542 (dense) / 0.7050 (sparse)
  trainable W_g          this file

If held-out rises materially, the fire calculus changes: the effect size H_9925 reported was
measured under a constraint the real run does not have. If it does not, the 0.70-0.75 estimate
stands and it stands for the right reason.
"""
import numpy as np, os, sys
import anima_py
sys.path.insert(0, os.path.join(os.path.dirname(anima_py.__file__), "core"))
import decode as clm

c = clm.clm_load_weights(os.path.join(os.path.expanduser("~"), "anima-weights",
                                      "store303_s2000.clm"))["clms"]
Wg0 = np.asarray(c["W_g"], dtype=np.float64)
val = np.asarray(c["val"], dtype=np.float64)
r = int(c["r"])
ZS = [np.load(f, allow_pickle=True) for f in ("rot_a.npz", "rot_b.npz", "rot_c.npz")]
LR, STEPS, MOM = 3e-3, 3000, 0.9
LR_G = 3e-3 / 34.0          # W_g sees h (row-norm ~34x that of g); scale its step accordingly


def pick(d, op):
    return np.stack([np.asarray(z[k], dtype=np.float64).reshape(-1)
                     for z in ZS for k in sorted(z.files)
                     if k.startswith("d%d|%s|" % (d, op)) and k.endswith("__last")])


D = list(range(9))
Hh = {d: {o: pick(d, o) for o in ("is", "not")} for d in D}
base = 0.5 * (val[0] + val[1])


def gelu(x):
    return 0.5 * x * (1.0 + np.tanh(0.7978845608 * (x + 0.044715 * x ** 3)))


def dgelu(x):
    t = np.tanh(0.7978845608 * (x + 0.044715 * x ** 3))
    return 0.5 * (1.0 + t) + 0.5 * x * (1.0 - t ** 2) * 0.7978845608 * (1.0 + 3 * 0.044715 * x ** 2)


def build(ds, seed):
    rr = np.random.default_rng(seed)
    hs, vs, ys = [], [], []
    for d in ds:
        for op, opv in (("is", 0), ("not", 1)):
            hh = Hh[d][op]
            pol = rr.integers(0, 2, len(hh))
            hs.append(hh); vs.append(val[pol] - base)
            ys.append(np.where((pol == 0) != (opv == 1), 1.0, -1.0))
    return np.vstack(hs), np.vstack(vs), np.concatenate(ys)


def train(ds, seed=7, shuffle=False, train_wg=True):
    Xh, Xv, y = build(ds, seed)
    rng = np.random.default_rng(seed)
    if shuffle:
        y = y[rng.permutation(len(y))]
    Wg = Wg0.copy()                                   # continue FROM the checkpoint, as a retrain does
    Wh = rng.normal(0, 0.126, (val.shape[1] + Wg.shape[1], r)); bh = np.zeros(r)
    Wo = rng.normal(0, 0.054, (r, 2))
    mg = np.zeros_like(Wg); mh = np.zeros_like(Wh); mo = np.zeros_like(Wo); mb = np.zeros_like(bh)
    for _ in range(STEPS):
        g = Xh @ Wg
        cat = np.concatenate([Xv, g], axis=1)
        pre = cat @ Wh + bh
        z = gelu(pre); s = z @ Wo; m = s[:, 0] - s[:, 1]
        p = 1.0 / (1.0 + np.exp(-np.clip(m * y, -60, 60)))
        gm = (-(1 - p) * y)[:, None] * np.array([1.0, -1.0])
        gz = gm @ Wo.T * dgelu(pre)
        mh = MOM * mh + cat.T @ gz / len(y)
        mo = MOM * mo + z.T @ gm / len(y)
        mb = MOM * mb + gz.mean(0)
        if train_wg:
            gcat = gz @ Wh.T                          # (n, d_s+d_g); the g half feeds W_g
            mg = MOM * mg + Xh.T @ gcat[:, val.shape[1]:] / len(y)
            Wg -= LR_G * mg
        Wh -= LR * mh; Wo -= LR * mo; bh -= LR * mb
    return Wg, Wh, bh, Wo


def sc(W, dd, seed=99):
    Wg, Wh, bh, Wo = W
    Xh, Xv, y = build(dd, seed)
    z = gelu(np.concatenate([Xv, Xh @ Wg], axis=1) @ Wh + bh); s = z @ Wo
    return float((np.sign(s[:, 0] - s[:, 1]) == y).mean())


print("  W_g TRAINABLE (as --freeze-trunk actually leaves it) vs H_9925's frozen-W_g numbers")
print("  %-22s %8s %10s %9s   %s" % ("train offsets", "seen", "held-mean", "held-min", "H_9925 held-mean"))
print("  " + "-" * 74)
for S, prev in (([0, 1, 2, 3, 5, 7], 0.7542), ([0, 2, 5, 8], 0.7050)):
    HO = [d for d in D if d not in S]
    W = train(S)
    held = [sc(W, [d]) for d in HO]
    print("  %-22s %8.4f %10.4f %9.4f   %.4f (frozen)"
          % (str(S), sc(W, S), float(np.mean(held)), min(held), prev))
S = [0, 1, 2, 3, 5, 7]
HO = [d for d in D if d not in S]
null = [float(np.mean([sc(train(S, seed=s, shuffle=True), [d]) for d in HO])) for s in (7, 11)]
print("  shuffled-label floor: mean %.4f  max %.4f" % (float(np.mean(null)), float(np.max(null))))
