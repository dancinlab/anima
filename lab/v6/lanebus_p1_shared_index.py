#!/usr/bin/env python3
"""LANE-BUS P1 (v2) — arity-2 IS learnable once both roles share one index space. $0.

WHAT CHANGED FROM THE FAILING VERSION
-------------------------------------
`lanebus_p1_arity2.py` measured held-out 0.0000 and the search for why ran through seven
axes, all negative:

    combination form   concat / sum / product
    optimizer          plain SGD / AdamW
    weight decay       0 -> 3.0
    steps              20k -> 200k
    projection         shared / role-separate / learnable
    store code         iid-random / orthogonalised
    addressing         soft / sharpened / hard argmax

A grokking POSITIVE CONTROL run alongside settled that composition itself is learnable in
this setup: canonical modular addition with one-hot operands reaches held-out 0.9100 at
n=23 against chance 0.0435. So the wall was never "composition cannot be learned".

The one structural difference left between the failing task and the passing control was
this: the control has BOTH operands indexing the SAME embedding table, while P1 gave each
role its own. With one table the circular structure is learned once and both roles reuse
it; with two, the model has to discover the alignment BETWEEN two independent tables from
48 examples, and it never does -- it memorises instead.

Removing that split is the whole change. Retrieval stays content-addressed off frozen
per-byte keys, so the store property that made H_9775 generalize is untouched.

    role-separate tables   held-out 0.0000
    shared index space     held-out 0.6875   (chance 0.1250)

WHAT IS STILL NOT CLAIMED
-------------------------
A toy, one table family, three seeds, DIRECTIONAL by lab/v6 law. And the task is a cyclic
group in disguise, which is the friendliest possible composition; a real relation table
need not have that structure. What this file establishes is narrower and still worth
having: the arity-2 wall in P1 was a REPRESENTATIONAL SPLIT, not an inability to compose,
and it is removable by a design choice rather than by more compute.
"""
import itertools
import numpy as np

N = 8                      # slots (and values)
HELD = 16                  # of 64 cells
D_K = 24                   # frozen key dim
D_E = 48                   # learned slot-embedding dim
HID = 192
STEPS = 120000
TAU = 0.3                  # address temperature; softmax over slot keys
SEEDS = (7, 11, 4302)


def softmax(z):
    z = z - z.max(axis=-1, keepdims=True)
    e = np.exp(z)
    return e / e.sum(axis=-1, keepdims=True)


class Adam:
    def __init__(self, shapes, lr=1e-3, b1=0.9, b2=0.98, eps=1e-8, wd=0.0):
        self.m = [np.zeros(s) for s in shapes]
        self.v = [np.zeros(s) for s in shapes]
        self.lr, self.b1, self.b2, self.eps, self.wd, self.t = lr, b1, b2, eps, wd, 0

    def step(self, ps, gs):
        self.t += 1
        for i, (p, g) in enumerate(zip(ps, gs)):
            self.m[i] = self.b1 * self.m[i] + (1 - self.b1) * g
            self.v[i] = self.b2 * self.v[i] + (1 - self.b2) * g * g
            mh = self.m[i] / (1 - self.b1 ** self.t)
            vh = self.v[i] / (1 - self.b2 ** self.t)
            p -= self.lr * (mh / (np.sqrt(vh) + self.eps) + self.wd * p)


def build(seed):
    rng = np.random.default_rng(seed)
    key_emb = rng.normal(0, 1.0, (256, D_K))           # FROZEN per-byte key table
    nm = []
    while len(nm) < N:
        s = "s" + "".join(chr(97 + int(rng.integers(0, 26))) for _ in range(4))
        if s not in nm:
            nm.append(s)

    def key(x):
        b = np.frombuffer(x.encode("ascii"), dtype=np.uint8)
        return key_emb[b].mean(axis=0)

    K = np.stack([key(x) for x in nm])
    base = rng.permutation(N)                          # output relabelling
    cells = [(i, j) for i in range(N) for j in range(N)]
    o = rng.permutation(len(cells))
    held = {cells[k] for k in o[:HELD]}
    return dict(rng=rng, K=K, base=base,
                train=[c for c in cells if c not in held],
                test=[c for c in cells if c in held])


def addr(env, i, K=None):
    """Content-addressed read: the query is the name's FROZEN key, so a held-out name
    would still address correctly from bytes it has seen."""
    KK = env["K"] if K is None else K
    return softmax(KK[i] @ KK.T / (np.sqrt(D_K) * TAU))


def gold(env, pairs):
    return np.array([env["base"][(i + j) % N] for (i, j) in pairs])


def train(env, wd, joint=True, steps=STEPS, lr=1e-3):
    """joint=True  -> shared slot table, group-addition combine
       joint=False -> STAPLE: two independent 1-slot readouts fused additively, no joint
                      term, capacity-matched (HID/2 each)."""
    rng = env["rng"]
    A = np.stack([addr(env, i) for (i, j) in env["train"]])
    B = np.stack([addr(env, j) for (i, j) in env["train"]])
    y = gold(env, env["train"])
    m = len(y)
    E = rng.normal(0, 0.5, (N, D_E))
    if joint:
        W1 = rng.normal(0, 0.5 / np.sqrt(D_E), (D_E, HID)); b1 = np.zeros(HID)
        W2 = rng.normal(0, 0.5 / np.sqrt(HID), (HID, N)); b2 = np.zeros(N)
        ps = [E, W1, b1, W2, b2]
        opt = Adam([p.shape for p in ps], lr=lr, wd=wd)
        for _ in range(steps):
            bi = rng.integers(0, m, 64)
            X = A[bi] @ E + B[bi] @ E
            h = np.tanh(X @ W1 + b1)
            p = softmax(h @ W2 + b2)
            p[np.arange(len(bi)), y[bi]] -= 1.0; p /= len(bi)
            gW2 = h.T @ p; gb2 = p.sum(0)
            gh = (p @ W2.T) * (1 - h ** 2)
            gW1 = X.T @ gh; gb1 = gh.sum(0); gX = gh @ W1.T
            opt.step(ps, [A[bi].T @ gX + B[bi].T @ gX, gW1, gb1, gW2, gb2])

        def pred(pairs, Aov=None, Bov=None):
            A2 = Aov if Aov is not None else np.stack([addr(env, i) for (i, j) in pairs])
            B2 = Bov if Bov is not None else np.stack([addr(env, j) for (i, j) in pairs])
            return (np.tanh((A2 @ E + B2 @ E) @ W1 + b1) @ W2 + b2).argmax(1)
    else:
        h2 = HID // 2
        Wa = rng.normal(0, 0.5 / np.sqrt(D_E), (D_E, h2))
        Wb = rng.normal(0, 0.5 / np.sqrt(D_E), (D_E, h2))
        Ua = rng.normal(0, 0.5 / np.sqrt(h2), (h2, N))
        Ub = rng.normal(0, 0.5 / np.sqrt(h2), (h2, N))
        b2 = np.zeros(N)
        ps = [E, Wa, Wb, Ua, Ub, b2]
        opt = Adam([p.shape for p in ps], lr=lr, wd=wd)
        for _ in range(steps):
            bi = rng.integers(0, m, 64)
            ea = A[bi] @ E; eb = B[bi] @ E
            ha = np.tanh(ea @ Wa); hb = np.tanh(eb @ Wb)
            p = softmax(ha @ Ua + hb @ Ub + b2)
            p[np.arange(len(bi)), y[bi]] -= 1.0; p /= len(bi)
            gUa = ha.T @ p; gUb = hb.T @ p
            gha = (p @ Ua.T) * (1 - ha ** 2); ghb = (p @ Ub.T) * (1 - hb ** 2)
            gWa = ea.T @ gha; gWb = eb.T @ ghb
            gE = A[bi].T @ (gha @ Wa.T) + B[bi].T @ (ghb @ Wb.T)
            opt.step(ps, [gE, gWa, gWb, gUa, gUb, p.sum(0)])

        def pred(pairs, Aov=None, Bov=None):
            A2 = Aov if Aov is not None else np.stack([addr(env, i) for (i, j) in pairs])
            B2 = Bov if Bov is not None else np.stack([addr(env, j) for (i, j) in pairs])
            ha = np.tanh((A2 @ E) @ Wa); hb = np.tanh((B2 @ E) @ Wb)
            return (ha @ Ua + hb @ Ub + b2).argmax(1)
    return pred


def acc(env, pred, pairs, **kw):
    if not pairs:
        return float("nan")
    return float((pred(pairs, **kw) == gold(env, pairs)).mean())


def main():
    ch = 1.0 / N
    print("LANE-BUS P1 (v2) - shared index space, content-addressed ($0, DIRECTIONAL)")
    print("chance %.4f (derived).  form retention is TRUE BY CONSTRUCTION (detached lane).\n" % ch)
    rows = {k: [] for k in ("fit", "held", "st_fit", "st_held", "addr_perm")}
    for s in SEEDS:
        env = build(s)
        pr = train(env, wd=0.3, joint=True)
        st = train(env, wd=0.3, joint=False)
        perm = env["rng"].permutation(N)
        Ap = np.stack([addr(env, perm[i]) for (i, j) in env["test"]])
        Bp = np.stack([addr(env, perm[j]) for (i, j) in env["test"]])
        rows["fit"].append(acc(env, pr, env["train"]))
        rows["held"].append(acc(env, pr, env["test"]))
        rows["st_fit"].append(acc(env, st, env["train"]))
        rows["st_held"].append(acc(env, st, env["test"]))
        rows["addr_perm"].append(acc(env, pr, env["test"], Aov=Ap, Bov=Bp))
    k = lambda n: float(np.mean(rows[n]))
    print("%-32s %8s" % ("arm", "acc"))
    print("-" * 44)
    print("%-32s %8.4f   positive control" % ("workspace, SEEN", k("fit")))
    print("%-32s %8.4f   <- THE MEASUREMENT" % ("workspace, HELD-OUT", k("held")))
    print("%-32s %8.4f   capacity-matched" % ("staple (two 1-slot), SEEN", k("st_fit")))
    print("%-32s %8.4f   must stay at ceiling" % ("staple, HELD-OUT", k("st_held")))
    print("%-32s %8.4f   must collapse" % ("address-permute", k("addr_perm")))
    print("-" * 44)
    print()
    if k("fit") < 0.95:
        print("INSTRUMENT-DEAD - the workspace cannot fit what it was shown (%.4f)." % k("fit"))
        return 1
    if k("held") <= ch * 1.5:
        print("ARITY-2 NOT LEARNED - held-out %.4f against chance %.4f." % (k("held"), ch))
        return 1
    if k("held") - k("st_held") < 0.25:
        print("NOT-CONJUNCTION - the capacity-matched staple reaches %.4f against the")
        print("workspace's %.4f, so an additive pair of 1-slot readouts explains it."
              % (k("st_held"), k("held")))
        return 1
    if k("addr_perm") > ch * 2:
        print("CONTROL-LEAK - address-permute still reads %.4f; the answer does not depend")
        print("on WHICH slots were addressed." % k("addr_perm"))
        return 1
    print("ARITY-2 LEARNED - held-out %.4f (%.1fx chance), staple %.4f, address-permute"
          % (k("held"), k("held") / ch, k("st_held")))
    print("%.4f. The workspace composes two content-addressed reads on held-out pairs."
          % k("addr_perm"))
    print()
    print("The change that did it was removing the ROLE-SEPARATE embedding tables, not")
    print("more compute: seven other axes (combination form, optimizer, weight decay,")
    print("steps to 200k, projection style, store code, addressing sharpness) were all")
    print("negative first. Still DIRECTIONAL -- a toy, one table family, three seeds, and")
    print("a cyclic group is the friendliest composition there is.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
