"""H_9924 follow-through: the readout toy, CALIBRATED, finally allowed to answer.

The toy sat below the g-space linear ceiling until now, so its numbers were unreadable. The
whole cause was the step size: the fusion input has row-norm 34.14 (g rms 4.71 over 64 dims),
so a learning rate tuned on normalised inputs is ~34x too large. Swept it -- 3e-1 and 3e-2
never leave chance, 3e-3 reaches seen-acc 0.8953 which IS the ~0.89 ceiling, and below that it
just undertrains. Nothing about the architecture was wrong; gelu and the checkpoint-scale init
were already right.

Now it can be asked the question the chain has been building toward: with the lane's own
arithmetic and its own frozen bottleneck, does a readout fitted on some offsets generalise to
offsets it never saw?
"""
import numpy as np, os, sys
import anima_py
sys.path.insert(0, os.path.join(os.path.dirname(anima_py.__file__), "core"))
import decode as clm

c = clm.clm_load_weights(os.path.join(os.path.expanduser("~"), "anima-weights",
                                      "store303_s2000.clm"))["clms"]
Wg = np.asarray(c["W_g"], dtype=np.float64)
val = np.asarray(c["val"], dtype=np.float64)
r = int(c["r"])
ZS = [np.load(f, allow_pickle=True) for f in ("rot_a.npz", "rot_b.npz", "rot_c.npz")]
LR, STEPS, MOM = 3e-3, 6000, 0.9


def pick(d, op):
    return np.stack([np.asarray(z[k], dtype=np.float64).reshape(-1)
                     for z in ZS for k in sorted(z.files)
                     if k.startswith("d%d|%s|" % (d, op)) and k.endswith("__last")])


D = list(range(9))
G = {d: {o: pick(d, o) @ Wg for o in ("is", "not")} for d in D}
base = 0.5 * (val[0] + val[1])


def gelu(x):
    return 0.5 * x * (1.0 + np.tanh(0.7978845608 * (x + 0.044715 * x ** 3)))


def dgelu(x):
    t = np.tanh(0.7978845608 * (x + 0.044715 * x ** 3))
    return 0.5 * (1.0 + t) + 0.5 * x * (1.0 - t ** 2) * 0.7978845608 * (1.0 + 3 * 0.044715 * x ** 2)


def build(ds, seed):
    rr = np.random.default_rng(seed)
    gs, vs, ys = [], [], []
    for d in ds:
        for op, opv in (("is", 0), ("not", 1)):
            gg = G[d][op]
            pol = rr.integers(0, 2, len(gg))
            gs.append(gg); vs.append(val[pol] - base)
            ys.append(np.where((pol == 0) != (opv == 1), 1.0, -1.0))
    return np.concatenate([np.vstack(vs), np.vstack(gs)], axis=1), np.concatenate(ys)


def train(ds, seed=7, shuffle=False):
    cat, y = build(ds, seed)
    rng = np.random.default_rng(seed)
    if shuffle:
        y = y[rng.permutation(len(y))]
    Wh = rng.normal(0, 0.126, (cat.shape[1], r)); bh = np.zeros(r)
    Wo = rng.normal(0, 0.054, (r, 2))
    mh = np.zeros_like(Wh); mo = np.zeros_like(Wo); mb = np.zeros_like(bh)
    for _ in range(STEPS):
        pre = cat @ Wh + bh
        z = gelu(pre); s = z @ Wo; m = s[:, 0] - s[:, 1]
        p = 1.0 / (1.0 + np.exp(-np.clip(m * y, -60, 60)))
        gm = (-(1 - p) * y)[:, None] * np.array([1.0, -1.0])
        mh = MOM * mh + cat.T @ (gm @ Wo.T * dgelu(pre)) / len(y)
        mo = MOM * mo + z.T @ gm / len(y)
        mb = MOM * mb + (gm @ Wo.T * dgelu(pre)).mean(0)
        Wh -= LR * mh; Wo -= LR * mo; bh -= LR * mb
    return Wh, bh, Wo


def sc(W, dd, seed=99):
    Wh, bh, Wo = W
    cat, y = build(dd, seed)
    z = gelu(cat @ Wh + bh); s = z @ Wo
    return float((np.sign(s[:, 0] - s[:, 1]) == y).mean())


print("  CALIBRATED readout toy (lane arithmetic · gelu · ckpt-scale init · lr 3e-3)")
print("  g-space LINEAR ceiling on these offsets: ~0.89")
print("  %-22s %9s %11s %10s" % ("train offsets", "seen", "held-mean", "held-min"))
print("  " + "-" * 56)
for S in ([0, 1, 2, 3, 5, 7], [0, 1, 2, 4, 6, 8], [0, 2, 4, 6, 8], [0, 2, 5, 8]):
    HO = [d for d in D if d not in S]
    W = train(S)
    held = [sc(W, [d]) for d in HO]
    print("  %-22s %9.4f %11.4f %10.4f"
          % (str(S), sc(W, S), float(np.mean(held)), min(held)))
S = [0, 1, 2, 3, 5, 7]
HO = [d for d in D if d not in S]
null = [float(np.mean([sc(train(S, seed=s, shuffle=True), [d]) for d in HO])) for s in (7, 11, 23)]
print("  shuffled-label floor: mean %.4f  max %.4f" % (float(np.mean(null)), float(np.max(null))))
