#!/usr/bin/env python3
"""H_1837 TENSION-MOUTH ITERATED (deep-equilibrium) -- DIRECTIONAL toy probe.

Follow-on to H_1834 (state/1834_tension_mouth_native/tension_mouth_probe.py, NOT
modified; the autograd core + G1 recombination toy + composed_distinct metric are
re-derived here so the original is untouched per fleet-full isolation).

ABSTRACT ESCAPE UNDER TEST (temporal axis):
  H_1834 collapsed the tension-mouth to a 1-shot bilinear readout of a CE-trained
  feed-forward trunk-state -> INERT (composed_distinct = 0 @ every seed/arm). The
  data-processing inequality (DPI) META-LAW: a SINGLE-SHOT function of a CE-trained
  trunk-state cannot inject compositional mutual-information the trunk-state does not
  already carry. The only untested orthogonal axis is a *temporal* change to the
  learning-signal geometry.

  This probe reframes the mouth as a K-step DEEP-EQUILIBRIUM fixed-point map seeking
  the A<->G tension fixed point Psi = 1/2, drawing compositional depth from ITERATION
  COUNT rather than a 1-shot readout:

      h_{k+1} = f_A(h_k, x, e_k) - g_G(h_k, x, e_k)     (weight-shared A<->G fields)

  where at EVERY step the input x (the two concept codes) AND the emitted prefix e_k
  (soft expected emission fed back = deep-equilibrium input re-injection) are
  re-injected. Load-bearing claim: per-step input re-injection (re-conditioning),
  NOT bare iteration, is what could break the 1-shot DPI wall.

*** DIRECTIONAL ONLY *** numpy mirror, NOT engine-native. a_engine_native_learning ->
auto-DIRECTIONAL, cannot be stamped terminal. Engine-native re-measure on live
pure_field<->engine_g iterate is the gating follow-on IF a lift occurs.
"""

import json
import numpy as np

# ---------- minimal reverse-mode autograd (re-derived from H_1834) ----------

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


def sub(x, y):
    out = T(x.data - y.data, (x, y))

    def bw():
        x.grad += _unbroadcast(out.grad, x.data.shape)
        y.grad += _unbroadcast(-out.grad, y.data.shape)

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


def matmul(x, W):
    # x:(B,a)  W:(a,b) -> (B,b)
    out = T(x.data @ W.data, (x, W))

    def bw():
        x.grad += out.grad @ W.data.T
        W.grad += x.data.T @ out.grad

    out._backward = bw
    return out


def gather_rows(E, idx):
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


def softmax_ce(logits, target):
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


# ---------- G1 compositional-recombination toy (identical to H_1834) ----------

VSZ = 256
K = 4
A_TOK = [10 + m for m in range(K)]
B_TOK = [50 + n for n in range(K)]


def target_byte(m, n):
    return 100 + m * K + n


HELDOUT = [(0, 0), (1, 1), (2, 2), (3, 3)]
ALL_PAIRS = [(m, n) for m in range(K) for n in range(K)]
TRAIN_PAIRS = [p for p in ALL_PAIRS if p not in HELDOUT]


def build_dataset():
    A_idx = np.array([A_TOK[m] for (m, n) in TRAIN_PAIRS], dtype=np.int64)
    B_idx = np.array([B_TOK[n] for (m, n) in TRAIN_PAIRS], dtype=np.int64)
    tgt = np.array([target_byte(m, n) for (m, n) in TRAIN_PAIRS], dtype=np.int64)
    return A_idx, B_idx, tgt


def heldout_arrays():
    A_idx = np.array([A_TOK[m] for (m, n) in HELDOUT], dtype=np.int64)
    B_idx = np.array([B_TOK[n] for (m, n) in HELDOUT], dtype=np.int64)
    tgt = np.array([target_byte(m, n) for (m, n) in HELDOUT], dtype=np.int64)
    return A_idx, B_idx, tgt


# ---------- ITERATED TENSION-MOUTH (deep-equilibrium fixed-point map) ----------

KT = 4.0
EPS = 1e-6
EPS_CONV = 0.05
K_MAX = 16


class Params:
    def __init__(self, seed, d):
        rng = np.random.default_rng(seed)
        sc = lambda a, b: rng.standard_normal((a, b)) * (1.0 / np.sqrt(b))
        self.E = T(sc(VSZ, d))
        self.Wx = T(sc(d, d))
        self.Wfh = T(sc(d, d)); self.Wfx = T(sc(d, d)); self.Wfe = T(sc(d, d))
        self.Wgh = T(sc(d, d)); self.Wgx = T(sc(d, d)); self.Wge = T(sc(d, d))
        self.Wout = T(sc(VSZ, d))
        self.d = d

    def tensors(self):
        return [self.E, self.Wx, self.Wfh, self.Wfx, self.Wfe,
                self.Wgh, self.Wgx, self.Wge, self.Wout]


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


def _norm(v):
    return sqrtT(add_scalar(ssum(square(v), axis=1), EPS))


def unroll(P, A_idx, B_idx, K_steps, reinject_input=True):
    """K-step deep-equilibrium unroll -> (logits_T, psi_devs_list).

    reinject_input=True  -> input x re-injected EVERY step (deep-equilibrium).
    reinject_input=False -> SAME-STATE ablation: x only at step 0 (bare iteration).
    """
    bagA = gather_rows(P.E, A_idx)
    bagB = gather_rows(P.E, B_idx)
    x = add(bagA, bagB)
    B = x.data.shape[0]
    zero_x = T(np.zeros((B, P.d)))
    h = tanhT(matmul(x, P.Wx))
    psi_devs = []
    for k in range(K_steps):
        emit = softmax(linear(h, P.Wout), axis=1)
        e = matmul(emit, P.E)
        xk = x if reinject_input else zero_x
        pre_f = add(add(matmul(h, P.Wfh), matmul(xk, P.Wfx)), matmul(e, P.Wfe))
        pre_g = add(add(matmul(h, P.Wgh), matmul(xk, P.Wgx)), matmul(e, P.Wge))
        fA = tanhT(pre_f)
        gG = tanhT(pre_g)
        na = _norm(fA)
        ng = _norm(gG)
        t = divide(na, add_scalar(ng, EPS))
        psi = sigmoidT(mul_scalar(add_scalar(t, -1.0), KT))
        psi_devs.append(float(np.abs(psi.data - 0.5).mean()))
        h = sub(fA, gG)
    logits = linear(h, P.Wout)
    return logits, psi_devs


def train(seed, K_steps, reinject_input=True, d=128, epochs=2500, lr=0.01):
    A_idx, B_idx, tgt = build_dataset()
    P = Params(seed, d)
    opt = Adam(P.tensors(), lr=lr)
    for ep in range(epochs):
        opt.zero_grad()
        logits, _ = unroll(P, A_idx, B_idx, K_steps, reinject_input)
        loss, _ = softmax_ce(logits, tgt)
        loss.backward()
        opt.step()
    return P


def eval_at(P, K_steps, reinject_input=True, shuffle_heldout=False):
    A_idx, B_idx, tgt = heldout_arrays()
    if shuffle_heldout:
        B_idx = np.roll(B_idx, 1)
    logits, psi_devs = unroll(P, A_idx, B_idx, K_steps, reinject_input)
    pred = logits.data.argmax(axis=1)
    correct = pred == tgt
    composed_distinct = len(set(tgt[correct].tolist()))
    Atr, Btr, ttr = build_dataset()
    ltr, _ = unroll(P, Atr, Btr, K_steps, reinject_input)
    train_acc = float((ltr.data.argmax(axis=1) == ttr).mean())
    return dict(composed_distinct=composed_distinct,
                heldout_acc=float(correct.mean()),
                train_acc=train_acc,
                psi_dev_final=psi_devs[-1] if psi_devs else None,
                psi_traj=psi_devs,
                pred=pred.tolist(), tgt=tgt.tolist())


def _np_softmax(z):
    z = z - z.max(1, keepdims=True)
    e = np.exp(z)
    return e / e.sum(1, keepdims=True)


def eval_converge(P, reinject_input=True):
    A_idx, B_idx, tgt = heldout_arrays()
    x = P.E.data[A_idx] + P.E.data[B_idx]
    B = x.shape[0]
    zero_x = np.zeros((B, P.d))
    h = np.tanh(x @ P.Wx.data)
    stop_k = K_MAX
    psi = np.full(B, 0.5)
    for k in range(1, K_MAX + 1):
        emit = _np_softmax(h @ P.Wout.data.T)
        e = emit @ P.E.data
        xk = x if reinject_input else zero_x
        fA = np.tanh(h @ P.Wfh.data.T + xk @ P.Wfx.data.T + e @ P.Wfe.data.T)
        gG = np.tanh(h @ P.Wgh.data.T + xk @ P.Wgx.data.T + e @ P.Wge.data.T)
        na = np.sqrt((fA ** 2).sum(1) + EPS)
        ng = np.sqrt((gG ** 2).sum(1) + EPS)
        t = na / (ng + EPS)
        psi = 1.0 / (1.0 + np.exp(-KT * (t - 1.0)))
        h = fA - gG
        if np.abs(psi - 0.5).max() <= EPS_CONV:
            stop_k = k
            break
    logits = h @ P.Wout.data.T
    pred = logits.argmax(1)
    correct = pred == tgt
    return dict(composed_distinct=len(set(tgt[correct].tolist())),
                stop_k=stop_k,
                psi_dev_final=float(np.abs(psi - 0.5).mean()))


# ---------- gradient check through the K-step unroll ----------

def gradcheck():
    global VSZ
    saved = VSZ
    VSZ = 12
    d = 6
    A_idx = np.array([2, 3, 4, 5], dtype=np.int64)
    B_idx = np.array([6, 7, 8, 9], dtype=np.int64)
    tgt = np.array([1, 0, 11, 5], dtype=np.int64)

    def loss_of(P, K_steps, reinj):
        logits, _ = unroll(P, A_idx, B_idx, K_steps, reinj)
        loss, _ = softmax_ce(logits, tgt)
        return loss

    worst = 0.0
    for K_steps, reinj in [(1, True), (2, True), (3, True), (3, False)]:
        P = Params(123, d)
        L = loss_of(P, K_steps, reinj)
        for t in P.tensors():
            t.grad = np.zeros_like(t.data)
        L.backward()
        rng = np.random.default_rng(7)
        for t in P.tensors():
            flat = t.data.reshape(-1)
            for _ in range(3):
                k = int(rng.integers(0, flat.size))
                orig = flat[k]
                hh = 1e-5
                flat[k] = orig + hh
                lp = loss_of(P, K_steps, reinj).data
                flat[k] = orig - hh
                lm = loss_of(P, K_steps, reinj).data
                flat[k] = orig
                num = (lp - lm) / (2 * hh)
                ana = t.grad.reshape(-1)[k]
                worst = max(worst, abs(num - ana))
    VSZ = saved
    ok = worst < 1e-4
    print(f"[gradcheck] max |numeric-analytic| through unroll = {worst:.2e}  "
          f"({'PASS' if ok else 'FAIL'})")
    return ok, worst


# ---------- main experiment ----------

SEEDS = [7, 4302, 4303]
K_SWEEP = [1, 2, 4, 8]


def main():
    print("H_1837 TENSION-MOUTH ITERATED (deep-equilibrium) -- DIRECTIONAL toy probe")
    print("*** DIRECTIONAL only (numpy mirror, NOT engine-native) ***\n")

    ok, worst = gradcheck()
    print()

    out = {"gradcheck_worst": worst, "gradcheck_pass": bool(ok),
           "seeds": SEEDS, "k_sweep": K_SWEEP, "arms": {}}

    print("=" * 78)
    print("ARM 1  FULL deep-equilibrium (input x + emit-prefix re-injected EVERY step)")
    print("=" * 78)
    full = {}
    for K_steps in K_SWEEP:
        row = []
        for seed in SEEDS:
            P = train(seed, K_steps, reinject_input=True)
            r = eval_at(P, K_steps, reinject_input=True)
            row.append(r)
            print(f"  K={K_steps:2d} seed={seed:5d}  cd={r['composed_distinct']}/4  "
                  f"train_acc={r['train_acc']:.2f}  |Psi-.5|={r['psi_dev_final']:.4f}")
        full[str(K_steps)] = [dict(seed=s, **{k: v for k, v in r.items()
                                              if k != 'psi_traj'})
                              for s, r in zip(SEEDS, row)]
        print()
    print("  --- converge (train K_MAX=%d, eval iterate-to-Psi<=%.2f) ---" %
          (K_MAX, EPS_CONV))
    conv = []
    for seed in SEEDS:
        P = train(seed, K_MAX, reinject_input=True)
        r = eval_converge(P, reinject_input=True)
        conv.append(dict(seed=seed, **r))
        print(f"  converge seed={seed:5d}  cd={r['composed_distinct']}/4  "
              f"stop_k={r['stop_k']}  |Psi-.5|={r['psi_dev_final']:.4f}")
    full["converge"] = conv
    out["arms"]["FULL_reinject_ON"] = full
    print()

    print("=" * 78)
    print("CONTROL A  SAME-STATE ablation (input re-inject OFF; bare map iteration)")
    print("=" * 78)
    abl = {}
    for K_steps in K_SWEEP:
        row = []
        for seed in SEEDS:
            P = train(seed, K_steps, reinject_input=False)
            r = eval_at(P, K_steps, reinject_input=False)
            row.append(r)
            print(f"  K={K_steps:2d} seed={seed:5d}  cd={r['composed_distinct']}/4  "
                  f"train_acc={r['train_acc']:.2f}  |Psi-.5|={r['psi_dev_final']:.4f}")
        abl[str(K_steps)] = [dict(seed=s, composed_distinct=r['composed_distinct'],
                                  train_acc=r['train_acc'],
                                  psi_dev_final=r['psi_dev_final'])
                             for s, r in zip(SEEDS, row)]
        print()
    out["arms"]["CTRL_A_same_state_reinject_OFF"] = abl

    print("=" * 78)
    print("CONTROL B  SHUFFLE (break A<->B held-out pairing) on FULL reinject, K=8")
    print("=" * 78)
    shuf = []
    for seed in SEEDS:
        P = train(seed, 8, reinject_input=True)
        r = eval_at(P, 8, reinject_input=True, shuffle_heldout=True)
        shuf.append(dict(seed=seed, composed_distinct=r['composed_distinct'],
                         train_acc=r['train_acc']))
        print(f"  shuffle seed={seed:5d}  cd={r['composed_distinct']}/4  "
              f"train_acc={r['train_acc']:.2f}")
    out["arms"]["CTRL_B_shuffle"] = shuf
    print()

    P = train(7, K_MAX, reinject_input=True)
    Ah, Bh, _ = heldout_arrays()
    _, traj = unroll(P, Ah, Bh, K_MAX, True)
    out["psi_trajectory_seed7_Kmax"] = traj
    print("Psi(K) trajectory (mean |Psi-0.5| per step, FULL reinject, seed 7, K_MAX):")
    print("  " + "  ".join(f"k{i+1}={v:.3f}" for i, v in enumerate(traj)))
    print()

    def cd_list(arm, key):
        return [e['composed_distinct'] for e in out["arms"][arm][key]]

    k1 = cd_list("FULL_reinject_ON", "1")
    anchor_ok = all(c == 0 for c in k1)
    full_curve = {k: cd_list("FULL_reinject_ON", str(k)) for k in K_SWEEP}
    full_curve["converge"] = [e['composed_distinct']
                              for e in out["arms"]["FULL_reinject_ON"]["converge"]]
    lift_any = any(sum(1 for c in cds if c >= 1) >= 2
                   for k, cds in full_curve.items() if k != 1)
    order = [1, 2, 4, 8, "converge"]
    means = [float(np.mean(full_curve[k])) for k in order]
    monotone = all(means[i + 1] >= means[i] - 1e-9 for i in range(len(means) - 1))
    abl_all0 = all(c == 0 for k in K_SWEEP
                   for c in cd_list("CTRL_A_same_state_reinject_OFF", str(k)))
    shuf_all0 = all(e['composed_distinct'] == 0 for e in out["arms"]["CTRL_B_shuffle"])

    green = lift_any and monotone and abl_all0 and shuf_all0 and anchor_ok
    verdict = "GREEN-DIRECTIONAL" if green else "WALL-DIRECTIONAL (DPI confirmed)"
    out["verdict"] = {
        "anchor_cd0_at_K1": anchor_ok,
        "full_curve_cd": {str(k): full_curve[k] for k in order},
        "curve_means": {str(k): m for k, m in zip(order, means)},
        "lift_any_ge2seeds_Kge2": bool(lift_any),
        "monotone_nondecreasing": bool(monotone),
        "same_state_ablation_all0": bool(abl_all0),
        "shuffle_all0": bool(shuf_all0),
        "verdict": verdict,
    }

    print("=" * 78)
    print("VERDICT (DIRECTIONAL, frozen bar unchanged)")
    print("=" * 78)
    print(f"  K=1 anchor cd=0 (H_1834 reproduced): {anchor_ok}  ({k1})")
    print(f"  FULL cd curve (mean over seeds): " +
          ", ".join(f"K{k}={m:.2f}" for k, m in zip(order, means)))
    print(f"  lift (cd>=1 on >=2/3 seed at some K>=2): {lift_any}")
    print(f"  monotone non-decreasing in K:            {monotone}")
    print(f"  same-state ablation all 0 (INERT):       {abl_all0}")
    print(f"  shuffle-control all 0:                   {shuf_all0}")
    print(f"  => {verdict}")

    with open("H_1837_result.json", "w") as f:
        json.dump(out, f, indent=2)
    print("\n  wrote H_1837_result.json")
    return out


if __name__ == "__main__":
    main()
