#!/usr/bin/env python3
"""H_1834 TENSION-MOUTH -- DIRECTIONAL toy probe (numpy, from-scratch).

Implements the anima-native TENSION-MOUTH forward (spec
state/1834_tension_mouth_native/README.md sections 2-6) as a small trunk trained
with a hand-rolled numpy reverse-mode autograd + Adam. Targets the G1
recombination wall: a global multiplicative (bilinear) binding of two concept
codes, gated by the A<->G tension scalar Psi.

*** DIRECTIONAL ONLY *** This is a numpy mirror, NOT engine-native (no live
core/*.hexa A<->G decode). Per CLAUDE.md a_engine_native_learning the verdict is
auto-DIRECTIONAL and cannot be stamped terminal / GREEN-engine. Engine-native
re-measurement on live pure_field<->engine_g is required before any GREEN/wall
closure.

Run:  python3 tension_mouth_probe.py            # 3 arms x 3 seeds + gradcheck
"""

import numpy as np

# ----------------------------------------------------------------------------
# minimal reverse-mode autograd over numpy arrays
# ----------------------------------------------------------------------------

class T:
    __slots__ = ("data", "grad", "_parents", "_backward")

    def __init__(self, data, parents=(), backward=None):
        self.data = np.asarray(data, dtype=np.float64)
        self.grad = np.zeros_like(self.data)
        self._parents = parents
        self._backward = backward if backward is not None else (lambda: None)

    def backward(self):
        topo, seen = [], set()

        def build(v):
            if id(v) in seen:
                return
            seen.add(id(v))
            for p in v._parents:
                build(p)
            topo.append(v)

        build(self)
        self.grad = np.ones_like(self.data)
        for v in reversed(topo):
            v._backward()


def _unbroadcast(grad, shape):
    while grad.ndim > len(shape):
        grad = grad.sum(axis=0)
    for i, s in enumerate(shape):
        if s == 1 and grad.shape[i] != 1:
            grad = grad.sum(axis=i, keepdims=True)
    return grad


def add(x, y):
    out = T(x.data + y.data, (x, y))

    def bw():
        x.grad += _unbroadcast(out.grad, x.data.shape)
        y.grad += _unbroadcast(out.grad, y.data.shape)

    out._backward = bw
    return out


def mul(x, y):
    out = T(x.data * y.data, (x, y))

    def bw():
        x.grad += _unbroadcast(out.grad * y.data, x.data.shape)
        y.grad += _unbroadcast(out.grad * x.data, y.data.shape)

    out._backward = bw
    return out


def divide(x, y):
    out = T(x.data / y.data, (x, y))

    def bw():
        x.grad += _unbroadcast(out.grad / y.data, x.data.shape)
        y.grad += _unbroadcast(-out.grad * x.data / (y.data ** 2), y.data.shape)

    out._backward = bw
    return out


def add_scalar(x, c):
    out = T(x.data + c, (x,))

    def bw():
        x.grad += out.grad

    out._backward = bw
    return out


def mul_scalar(x, c):
    out = T(x.data * c, (x,))

    def bw():
        x.grad += out.grad * c

    out._backward = bw
    return out


def square(x):
    out = T(x.data ** 2, (x,))

    def bw():
        x.grad += out.grad * 2.0 * x.data

    out._backward = bw
    return out


def sqrtT(x):
    d = np.sqrt(x.data)
    out = T(d, (x,))

    def bw():
        x.grad += out.grad * 0.5 / d

    out._backward = bw
    return out


def tanhT(x):
    d = np.tanh(x.data)
    out = T(d, (x,))

    def bw():
        x.grad += out.grad * (1.0 - d ** 2)

    out._backward = bw
    return out


def sigmoidT(x):
    d = 1.0 / (1.0 + np.exp(-x.data))
    out = T(d, (x,))

    def bw():
        x.grad += out.grad * d * (1.0 - d)

    out._backward = bw
    return out


def ssum(x, axis=None, keepdims=False):
    out = T(x.data.sum(axis=axis, keepdims=keepdims), (x,))

    def bw():
        g = out.grad
        if axis is not None and not keepdims:
            g = np.expand_dims(g, axis)
        x.grad += np.broadcast_to(g, x.data.shape).copy()

    out._backward = bw
    return out


def linear(x, W):
    # x:(B,in)  W:(out,in) -> (B,out)
    out = T(x.data @ W.data.T, (x, W))

    def bw():
        x.grad += out.grad @ W.data
        W.grad += out.grad.T @ x.data

    out._backward = bw
    return out


def gather_rows(E, idx):
    # E:(V,d)  idx:(B,) -> (B,d)
    out = T(E.data[idx], (E,))

    def bw():
        np.add.at(E.grad, idx, out.grad)

    out._backward = bw
    return out


def softmax(x, axis=1):
    z = x.data - x.data.max(axis=axis, keepdims=True)
    e = np.exp(z)
    s = e / e.sum(axis=axis, keepdims=True)
    out = T(s, (x,))

    def bw():
        dot = (out.grad * s).sum(axis=axis, keepdims=True)
        x.grad += s * (out.grad - dot)

    out._backward = bw
    return out


def outer_bind(pA, pB):
    # pA,pB:(B,r) -> (B,r*r)  bind[b,i,j] = pA[b,i]*pB[b,j]
    B, r = pA.data.shape
    bind = pA.data[:, :, None] * pB.data[:, None, :]
    out = T(bind.reshape(B, r * r), (pA, pB))

    def bw():
        G = out.grad.reshape(B, r, r)
        pA.grad += (G * pB.data[:, None, :]).sum(axis=2)
        pB.grad += (G * pA.data[:, :, None]).sum(axis=1)

    out._backward = bw
    return out


def col(x):
    # (B,) -> (B,1)
    out = T(x.data.reshape(-1, 1), (x,))

    def bw():
        x.grad += out.grad.reshape(-1)

    out._backward = bw
    return out


def softmax_ce(logits, target):
    # logits:(B,V) target:(B,) -> scalar mean CE
    B = logits.data.shape[0]
    z = logits.data - logits.data.max(axis=1, keepdims=True)
    e = np.exp(z)
    p = e / e.sum(axis=1, keepdims=True)
    loss = -np.log(p[np.arange(B), target] + 1e-12).mean()
    out = T(loss, (logits,))

    def bw():
        d = p.copy()
        d[np.arange(B), target] -= 1.0
        logits.grad += out.grad * d / B

    out._backward = bw
    return out, p


# ----------------------------------------------------------------------------
# G1 compositional-recombination toy (spec section 4)
# ----------------------------------------------------------------------------
# concept A_m at one slot, concept B_n at another; target = compose(A,B) = a
# distinct byte 100+m*K+n that is ABSENT from the training corpus for held-out
# (m,n). Held-out pairs are a compositional split: every m and every n is seen in
# training (with other partners) but the specific combo is novel. Distance
# between the two concept slots is varied; binding is RF-free (bag pooling of the
# two concept embeddings), so distance does not enter the combination operator.

VSZ = 256
K = 4                          # 4 A-concepts x 4 B-concepts = 16 pairs
A_TOK = [10 + m for m in range(K)]
B_TOK = [50 + n for n in range(K)]

def target_byte(m, n):
    return 100 + m * K + n     # 16 distinct composed bytes, 100..115

HELDOUT = [(0, 0), (1, 1), (2, 2), (3, 3)]      # diagonal compositional split
ALL_PAIRS = [(m, n) for m in range(K) for n in range(K)]
TRAIN_PAIRS = [p for p in ALL_PAIRS if p not in HELDOUT]


def build_dataset():
    A_idx = np.array([A_TOK[m] for (m, n) in TRAIN_PAIRS], dtype=np.int64)
    B_idx = np.array([B_TOK[n] for (m, n) in TRAIN_PAIRS], dtype=np.int64)
    tgt = np.array([target_byte(m, n) for (m, n) in TRAIN_PAIRS], dtype=np.int64)
    return A_idx, B_idx, tgt


# ----------------------------------------------------------------------------
# TENSION-MOUTH model (spec section 2/3) with 3 arms (section 5)
# ----------------------------------------------------------------------------

class Params:
    def __init__(self, seed, d, r):
        rng = np.random.default_rng(seed)
        sc = lambda a, b: rng.standard_normal((a, b)) * (1.0 / np.sqrt(b))
        self.E = T(sc(VSZ, d))
        self.Wh = T(sc(d, d))
        self.WA = T(sc(VSZ, d))
        self.WG = T(sc(VSZ, d))
        self.PA = T(sc(r, d))
        self.PB = T(sc(r, d))
        self.Wbind = T(sc(VSZ, r * r))

    def tensors(self):
        return [self.E, self.Wh, self.WA, self.WG, self.PA, self.PB, self.Wbind]


class Adam:
    def __init__(self, tensors, lr=0.01, b1=0.9, b2=0.999, eps=1e-8):
        self.ts = tensors
        self.lr, self.b1, self.b2, self.eps = lr, b1, b2, eps
        self.m = [np.zeros_like(t.data) for t in tensors]
        self.v = [np.zeros_like(t.data) for t in tensors]
        self.t = 0

    def zero_grad(self):
        for t in self.ts:
            t.grad = np.zeros_like(t.data)

    def step(self):
        self.t += 1
        for i, t in enumerate(self.ts):
            self.m[i] = self.b1 * self.m[i] + (1 - self.b1) * t.grad
            self.v[i] = self.b2 * self.v[i] + (1 - self.b2) * (t.grad ** 2)
            mh = self.m[i] / (1 - self.b1 ** self.t)
            vh = self.v[i] / (1 - self.b2 ** self.t)
            t.data -= self.lr * mh / (np.sqrt(vh) + self.eps)


K_TENSION = 4.0     # tension steepness (spec: psi = sigmoid(k*(t-1)))
EPS = 1e-6


def trunk(P, A_idx, B_idx):
    """bag pooling of the two concept embeddings -> hidden context h (RF-free)."""
    bag = add(gather_rows(P.E, A_idx), gather_rows(P.E, B_idx))
    h = tanhT(linear(bag, P.Wh))
    return h


def forward(P, A_idx, B_idx, arm):
    """Return (logits_T, psi_T_or_None)."""
    h = trunk(P, A_idx, B_idx)
    a = linear(h, P.WA)                       # forward field A over V

    if arm == "TENSION-OFF":
        # g removed entirely: pure forward field, no reverse constraint / bilinear
        return a, None

    g = linear(h, P.WG)                       # reverse constraint field G over V

    if arm == "ADDITIVE":
        # tension NOT resolved: plain additive combination a + g (spec ablation)
        return add(a, g), None

    # FULL: tension resolution (spec section 2)
    na = sqrtT(add_scalar(ssum(square(a), axis=1), EPS))         # ||a||
    ng = sqrtT(add_scalar(ssum(square(g), axis=1), EPS))         # ||g||
    t = divide(na, add_scalar(ng, EPS))                          # tension scalar
    psi = sigmoidT(mul_scalar(add_scalar(t, -1.0), K_TENSION))   # Psi; t=1 -> 1/2

    local = mul(a, softmax(g, axis=1))                           # local re-weight
    # global bilinear binding: two concept codes bound multiplicatively (RF-free)
    pA = linear(h, P.PA)
    pB = linear(h, P.PB)
    bil = linear(outer_bind(pA, pB), P.Wbind)                    # -> V
    logits = add(local, mul(col(psi), bil))
    return logits, psi


LAMBDA_PSI = 1.0


def train_arm(seed, arm, d=128, r=16, epochs=3000, lr=0.01, verbose=False):
    A_idx, B_idx, tgt = build_dataset()
    P = Params(seed, d, r)
    opt = Adam(P.tensors(), lr=lr)

    for ep in range(epochs):
        opt.zero_grad()
        logits, psi = forward(P, A_idx, B_idx, arm)
        loss, _ = softmax_ce(logits, tgt)
        if psi is not None:
            mean_psi = mul_scalar(ssum(psi), 1.0 / psi.data.shape[0])
            lpsi = square(add_scalar(mean_psi, -0.5))
            total = add(loss, mul_scalar(lpsi, LAMBDA_PSI))
        else:
            total = loss
        total.backward()
        opt.step()
        if verbose and ep % 500 == 0:
            print(f"    ep{ep} loss={loss.data:.4f}")

    return P


def evaluate(P, arm):
    """composed_distinct on held-out pairs + Psi deviation.

    composed_distinct = number of DISTINCT correct composed target bytes produced
    (greedy argmax next byte) over the held-out (unseen-combination) pairs. Each
    correct held-out target counts once; targets are absent from training, so a
    correct output is a genuine recombination. Range 0..len(HELDOUT)=4.
    """
    A_idx = np.array([A_TOK[m] for (m, n) in HELDOUT], dtype=np.int64)
    B_idx = np.array([B_TOK[n] for (m, n) in HELDOUT], dtype=np.int64)
    tgt = np.array([target_byte(m, n) for (m, n) in HELDOUT], dtype=np.int64)

    logits, psi = forward(P, A_idx, B_idx, arm)
    pred = logits.data.argmax(axis=1)
    correct = pred == tgt
    composed_distinct = len(set(tgt[correct].tolist()))

    if psi is not None:
        psi_mean = float(psi.data.mean())
        psi_dev = abs(psi_mean - 0.5)
    else:
        psi_mean, psi_dev = None, None

    Atr = np.array([A_TOK[m] for (m, n) in TRAIN_PAIRS], dtype=np.int64)
    Btr = np.array([B_TOK[n] for (m, n) in TRAIN_PAIRS], dtype=np.int64)
    ttr = np.array([target_byte(m, n) for (m, n) in TRAIN_PAIRS], dtype=np.int64)
    ltr, _ = forward(P, Atr, Btr, arm)
    train_acc = float((ltr.data.argmax(axis=1) == ttr).mean())

    return dict(composed_distinct=composed_distinct,
                heldout_acc=float(correct.mean()),
                train_acc=train_acc,
                psi_mean=psi_mean, psi_dev=psi_dev,
                pred=pred.tolist(), tgt=tgt.tolist())


# ----------------------------------------------------------------------------
# gradient check (finite differences) on a tiny instance -> autograd sanity
# ----------------------------------------------------------------------------

def gradcheck():
    global VSZ
    saved = VSZ
    VSZ = 12
    d, r = 6, 3
    A_idx = np.array([2, 3, 4, 5], dtype=np.int64)
    B_idx = np.array([6, 7, 8, 9], dtype=np.int64)
    tgt = np.array([1, 0, 11, 5], dtype=np.int64)

    def loss_of(P, arm):
        logits, psi = forward(P, A_idx, B_idx, arm)
        loss, _ = softmax_ce(logits, tgt)
        if psi is not None:
            mean_psi = mul_scalar(ssum(psi), 1.0 / psi.data.shape[0])
            lpsi = square(add_scalar(mean_psi, -0.5))
            return add(loss, mul_scalar(lpsi, LAMBDA_PSI))
        return loss

    worst = 0.0
    for arm in ("FULL", "TENSION-OFF", "ADDITIVE"):
        P = Params(123, d, r)
        L = loss_of(P, arm)
        for t in P.tensors():
            t.grad = np.zeros_like(t.data)
        L.backward()
        rng = np.random.default_rng(7)
        for t in P.tensors():
            flat = t.data.reshape(-1)
            for _ in range(4):
                k = int(rng.integers(0, flat.size))
                orig = flat[k]
                h = 1e-5
                flat[k] = orig + h
                lp = loss_of(P, arm).data
                flat[k] = orig - h
                lm = loss_of(P, arm).data
                flat[k] = orig
                num = (lp - lm) / (2 * h)
                ana = t.grad.reshape(-1)[k]
                worst = max(worst, abs(num - ana))
    VSZ = saved
    print(f"[gradcheck] max |numeric-analytic| over 3 arms = {worst:.2e}  "
          f"({'PASS' if worst < 1e-4 else 'FAIL'})")
    return worst < 1e-4


# ----------------------------------------------------------------------------
# main
# ----------------------------------------------------------------------------

def main():
    print("H_1834 TENSION-MOUTH -- DIRECTIONAL toy probe (numpy, from-scratch)")
    print("*** DIRECTIONAL only (numpy mirror, NOT engine-native) ***\n")

    ok = gradcheck()
    if not ok:
        print("WARNING: gradcheck failed -- results unreliable.")
    print()

    seeds = [7, 4302, 4303]
    arms = ["FULL", "TENSION-OFF", "ADDITIVE"]
    results = {a: [] for a in arms}

    for seed in seeds:
        for arm in arms:
            P = train_arm(seed, arm)
            r = evaluate(P, arm)
            results[arm].append((seed, r))
            pd = "  -  " if r["psi_dev"] is None else f"{r['psi_dev']:.4f}"
            print(f"seed={seed:5d}  {arm:11s}  "
                  f"composed_distinct={r['composed_distinct']}/4  "
                  f"heldout_acc={r['heldout_acc']:.2f}  "
                  f"train_acc={r['train_acc']:.2f}  "
                  f"|Psi-0.5|={pd}")
        print()

    print("=" * 68)
    print("AGGREGATE (mean over seeds 7/4302/4303)")
    print("=" * 68)
    for arm in arms:
        cds = [r["composed_distinct"] for _, r in results[arm]]
        devs = [r["psi_dev"] for _, r in results[arm] if r["psi_dev"] is not None]
        mean_cd = np.mean(cds)
        dev_s = "  -  " if not devs else f"{np.mean(devs):.4f}"
        print(f"  {arm:11s}  composed_distinct mean={mean_cd:.2f}  "
              f"(seeds {cds})   |Psi-0.5| mean={dev_s}")

    print()
    print("Frozen bar (pre-registered, p7): GREEN iff cd>=3 AND |Psi-0.5|<=0.05 ; "
          "ORANGE cd>=3 & dev>0.05 ; WALL cd<=2")
    for (seed, r) in results["FULL"]:
        cd, dev = r["composed_distinct"], r["psi_dev"]
        if cd >= 3 and dev is not None and dev <= 0.05:
            v = "GREEN"
        elif cd >= 3:
            v = "ORANGE"
        else:
            v = "WALL(brick/red)"
        print(f"  FULL seed={seed:5d}: cd={cd} dev={dev:.4f} -> {v}")


if __name__ == "__main__":
    main()
