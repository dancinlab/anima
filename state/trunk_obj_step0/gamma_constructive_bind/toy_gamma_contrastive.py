#!/usr/bin/env python3
"""STEP-0 screen for candidate (1) gamma trained-constructive-bind (contrastive trunk loss).

torch-free numpy micro-autograd => DIRECTIONAL only (a_engine_native_learning).
Frozen bar = FREEZE.md (pre-registered before run). No bar changes post-run (p7/c9/c2).

World = non-abelian group S_4 (24 elts). Input = ordered pair (a,b); target = group product a.b.
Non-commutativity is a WORLD property (Cayley table), NOT a planted input feature.

Arms (fixed order-capable concat-MLP trunk; vary only the LOSS):
  ADD     order-blind rep E[a]+E[b] + CE          (provable DPI floor)
  CE      MLP trunk + CE only (gamma=0)           (CE=echo baseline)
  G_trunk MLP trunk + CE + gamma*InfoNCE(trunk)   (candidate (1))
  G_read  MLP trunk + CE + gamma*InfoNCE(detached anchor => readout U only) (H_1602 repro)
"""
import argparse, json, math
import numpy as np

# ----------------------------- micro reverse-mode autograd -----------------------------
class V:
    __slots__ = ("data", "grad", "_back", "_prev")
    def __init__(self, data, prev=()):
        self.data = np.asarray(data, dtype=np.float64)
        self.grad = np.zeros_like(self.data)
        self._back = lambda: None
        self._prev = prev
    def backward(self):
        topo, seen = [], set()
        def build(n):
            if id(n) in seen: return
            seen.add(id(n))
            for p in n._prev: build(p)
            topo.append(n)
        build(self)
        self.grad = np.ones_like(self.data)
        for n in reversed(topo):
            n._back()

def _unbroadcast(g, shape):
    while g.ndim > len(shape):
        g = g.sum(axis=0)
    for i, s in enumerate(shape):
        if s == 1 and g.shape[i] != 1:
            g = g.sum(axis=i, keepdims=True)
    return g

def matmul(a, b):
    out = V(a.data @ b.data, (a, b))
    def back():
        a.grad += out.grad @ b.data.T
        b.grad += a.data.T @ out.grad
    out._back = back
    return out

def add(a, b):
    out = V(a.data + b.data, (a, b))
    def back():
        a.grad += _unbroadcast(out.grad, a.data.shape)
        b.grad += _unbroadcast(out.grad, b.data.shape)
    out._back = back
    return out

def mul(a, b):
    out = V(a.data * b.data, (a, b))
    def back():
        a.grad += _unbroadcast(out.grad * b.data, a.data.shape)
        b.grad += _unbroadcast(out.grad * a.data, b.data.shape)
    out._back = back
    return out

def tanh(a):
    t = np.tanh(a.data)
    out = V(t, (a,))
    def back():
        a.grad += out.grad * (1 - t * t)
    out._back = back
    return out

def gather(E, idx):
    idx = np.asarray(idx)
    out = V(E.data[idx], (E,))
    def back():
        np.add.at(E.grad, idx, out.grad)
    out._back = back
    return out

def concat(nodes, axis=1):
    out = V(np.concatenate([n.data for n in nodes], axis=axis), tuple(nodes))
    sizes = [n.data.shape[axis] for n in nodes]
    def back():
        i = 0
        for n, s in zip(nodes, sizes):
            sl = [slice(None)] * out.grad.ndim
            sl[axis] = slice(i, i + s)
            n.grad += out.grad[tuple(sl)]
            i += s
    out._back = back
    return out

def rowdot(a, b):  # (B,d)x(B,d) -> (B,1)
    out = V((a.data * b.data).sum(axis=1, keepdims=True), (a, b))
    def back():
        a.grad += out.grad * b.data
        b.grad += out.grad * a.data
    out._back = back
    return out

def l2norm(a, eps=1e-8):
    n = np.sqrt((a.data * a.data).sum(axis=1, keepdims=True)) + eps
    y = a.data / n
    out = V(y, (a,))
    def back():
        g = out.grad
        a.grad += (g - y * (y * g).sum(axis=1, keepdims=True)) / n
    out._back = back
    return out

def detach(a):
    return V(a.data.copy())  # fresh leaf, no prev => stops gradient

def softmax_ce(logits, targets):  # fused, returns scalar mean loss
    z = logits.data
    z = z - z.max(axis=1, keepdims=True)
    ez = np.exp(z)
    p = ez / ez.sum(axis=1, keepdims=True)
    B = z.shape[0]
    loss = -np.log(p[np.arange(B), targets] + 1e-12).mean()
    out = V(loss, (logits,))
    def back():
        g = p.copy()
        g[np.arange(B), targets] -= 1.0
        logits.grad += out.grad * g / B
    out._back = back
    return out

# ----------------------------- S_4 group world -----------------------------
def make_group():
    from itertools import permutations
    elts = list(permutations(range(4)))          # 24 permutations as tuples
    idx = {e: i for i, e in enumerate(elts)}
    N = len(elts)
    def comp(p, q):                                # (p.q)(i) = p(q(i))
        return tuple(p[q[i]] for i in range(4))
    table = np.zeros((N, N), dtype=np.int64)
    for i, p in enumerate(elts):
        for j, q in enumerate(elts):
            table[i, j] = idx[comp(p, q)]
    return N, table

def build_task(seed, table, shuffle):
    N = table.shape[0]
    rng = np.random.default_rng(seed)
    if shuffle:                                    # random function table (destroys group structure)
        tab = rng.integers(0, N, size=(N, N))
    else:
        tab = table
    pairs = [(a, b) for a in range(N) for b in range(N)]
    labels = np.array([tab[a, b] for a, b in pairs])
    order = rng.permutation(len(pairs))
    ntr = int(round(0.40 * len(pairs)))
    tr = set(order[:ntr].tolist())
    # ensure every element covered as operand-a and operand-b in train
    cova, covb = set(), set()
    for k in tr:
        a, b = pairs[k]; cova.add(a); covb.add(b)
    for k in order:
        a, b = pairs[k]
        if a not in cova or b not in covb:
            tr.add(k); cova.add(a); covb.add(b)
    tr = sorted(tr)
    ho = [k for k in range(len(pairs)) if k not in set(tr)]
    return pairs, labels, tr, ho, tab

# ----------------------------- model -----------------------------
def init_params(N, d, h, seed, arm):
    rng = np.random.default_rng(seed + 999)
    P = {}
    P["E"] = V(rng.standard_normal((N, d)) * 0.3)
    P["U"] = V(rng.standard_normal((N, d)) * 0.3)
    if arm != "ADD":
        P["W1"] = V(rng.standard_normal((2 * d, h)) * (1 / math.sqrt(2 * d)))
        P["b1"] = V(np.zeros(h))
        P["W2"] = V(rng.standard_normal((h, d)) * (1 / math.sqrt(h)))
        P["b2"] = V(np.zeros(d))
    if arm in ("G_trunk", "G_read"):
        P["Pa"] = V(np.eye(d) + rng.standard_normal((d, d)) * 0.01)  # additive-anchor projection
    return P

def trunk_rep(P, a_idx, b_idx, arm):
    Ea = gather(P["E"], a_idx); Eb = gather(P["E"], b_idx)
    if arm == "ADD":
        return l2norm(add(Ea, Eb))
    x = concat([Ea, Eb], axis=1)
    hpre = add(matmul(x, P["W1"]), P["b1"])
    hidn = tanh(hpre)
    r = add(matmul(hidn, P["W2"]), P["b2"])
    return l2norm(r)

def forward_loss(P, a_idx, b_idx, y, arm, tau, gamma):
    Un = l2norm(P["U"])
    r = trunk_rep(P, a_idx, b_idx, arm)
    scale = V(np.array(1.0 / tau))
    logits = mul(matmul(r, tp(Un)), scale)         # (B,N) cosine/tau
    Lmain = softmax_ce(logits, y)
    if arm not in ("G_trunk", "G_read"):
        return Lmain
    # gamma InfoNCE: positive U[y], + structural negatives swap-rep & additive-anchor
    r_sw = trunk_rep(P, b_idx, a_idx, arm)          # swapped-order trunk rep
    Ea = gather(P["E"], a_idx); Eb = gather(P["E"], b_idx)
    r_add = l2norm(matmul(add(Ea, Eb), P["Pa"]))    # additive-bag anchor
    anchor = r if arm == "G_trunk" else detach(r)   # G_read: gamma grad does NOT reach trunk
    if arm == "G_read":
        r_sw = detach(r_sw)
    s_cls = mul(matmul(anchor, tp(Un)), scale)      # (B,N)
    s_sw = mul(rowdot(anchor, r_sw), scale)         # (B,1) negative
    s_add = mul(rowdot(anchor, r_add), scale)       # (B,1) negative
    ext = concat([s_cls, s_sw, s_add], axis=1)      # (B,N+2), positive index = y (in 0..N-1)
    Linfo = softmax_ce(ext, y)
    return add(Lmain, mul(Linfo, V(np.array(gamma))))

def tp(a):  # transpose 2D node
    out = V(a.data.T, (a,))
    def back(): a.grad += out.grad.T
    out._back = back
    return out

# ----------------------------- train/eval -----------------------------
def train(P, pairs, labels, tr, arm, tau, gamma, steps, lr):
    a_idx = np.array([pairs[k][0] for k in tr])
    b_idx = np.array([pairs[k][1] for k in tr])
    y = labels[tr]
    keys = list(P.keys())
    m = {k: np.zeros_like(P[k].data) for k in keys}
    v = {k: np.zeros_like(P[k].data) for k in keys}
    b1, b2, eps = 0.9, 0.999, 1e-8
    for t in range(1, steps + 1):
        for k in keys: P[k].grad = np.zeros_like(P[k].data)
        loss = forward_loss(P, a_idx, b_idx, y, arm, tau, gamma)
        loss.backward()
        for k in keys:
            g = P[k].grad
            m[k] = b1 * m[k] + (1 - b1) * g
            v[k] = b2 * v[k] + (1 - b2) * (g * g)
            mh = m[k] / (1 - b1 ** t); vh = v[k] / (1 - b2 ** t)
            P[k].data -= lr * mh / (np.sqrt(vh) + eps)
    return float(loss.data)

def evaluate(P, pairs, labels, idxs, arm, tau):
    a_idx = np.array([pairs[k][0] for k in idxs])
    b_idx = np.array([pairs[k][1] for k in idxs])
    y = labels[idxs]
    Un = l2norm(P["U"]).data
    r = trunk_rep(P, a_idx, b_idx, arm).data
    logits = (r @ Un.T) / tau
    z = logits - logits.max(1, keepdims=True); ez = np.exp(z); p = ez / ez.sum(1, keepdims=True)
    pred = logits.argmax(1)
    acc = float((pred == y).mean())
    reach = float(p[np.arange(len(y)), y].mean())
    mask = np.ones_like(p); mask[np.arange(len(y)), y] = 0
    unreach = float((p * mask).sum(1).mean() / max(p.shape[1] - 1, 1))
    return acc, reach, unreach, pred, y

def gradcheck():
    rng = np.random.default_rng(0)
    P = {"E": V(rng.standard_normal((5, 4))), "U": V(rng.standard_normal((5, 4))),
         "W1": V(rng.standard_normal((8, 6))), "b1": V(rng.standard_normal(6)),
         "W2": V(rng.standard_normal((6, 4))), "b2": V(rng.standard_normal(4)),
         "Pa": V(rng.standard_normal((4, 4)))}
    a_idx = np.array([0, 1, 2]); b_idx = np.array([3, 4, 0]); y = np.array([1, 2, 3])
    def L():
        return forward_loss(P, a_idx, b_idx, y, "G_trunk", 0.1, 1.0).data
    for k in ["E", "W1", "b2", "U", "Pa"]:
        for k2 in P: P[k2].grad = np.zeros_like(P[k2].data)
        loss = forward_loss(P, a_idx, b_idx, y, "G_trunk", 0.1, 1.0); loss.backward()
        ana = P[k].grad.copy()
        num = np.zeros_like(P[k].data); h = 1e-5
        it = np.nditer(P[k].data, flags=["multi_index"])
        while not it.finished:
            mi = it.multi_index; orig = P[k].data[mi]
            P[k].data[mi] = orig + h; lp = L()
            P[k].data[mi] = orig - h; lm = L()
            P[k].data[mi] = orig; num[mi] = (lp - lm) / (2 * h); it.iternext()
        err = np.abs(ana - num).max()
        print(f"  gradcheck {k:3s}: max|ana-num|={err:.2e}", flush=True)
        assert err < 1e-4, f"gradcheck FAILED for {k}"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, nargs="*", default=[0, 1, 2, 3])
    ap.add_argument("--d", type=int, default=24)
    ap.add_argument("--h", type=int, default=64)
    ap.add_argument("--steps", type=int, default=4000)
    ap.add_argument("--lr", type=float, default=3e-3)
    ap.add_argument("--tau", type=float, default=0.1)
    ap.add_argument("--gamma", type=float, default=1.0)
    ap.add_argument("--out", default="result.json")
    A = ap.parse_args()

    print("=== finite-difference gradcheck (G_trunk loss) ===", flush=True)
    gradcheck()

    N, table = make_group()
    ARMS = ["ADD", "CE", "G_trunk", "G_read"]
    out = {"config": vars(A), "N": N, "chance": 1.0 / N, "runs": {}}
    for shuffle in (False, True):
        tag = "SHUFFLE" if shuffle else "GROUP"
        print(f"\n########## {tag} target (S_4, N={N}, chance={1/N:.4f}) ##########", flush=True)
        out["runs"][tag] = {}
        for seed in A.seeds:
            pairs, labels, tr, ho, tab = build_task(seed, table, shuffle)
            # per-pair non-commuting mask on held-out: a.b != b.a
            noncomm = [k for k in ho if tab[pairs[k][0], pairs[k][1]] != tab[pairs[k][1], pairs[k][0]]]
            out["runs"][tag][seed] = {"n_train": len(tr), "n_ho": len(ho), "n_ho_noncomm": len(noncomm)}
            print(f"-- seed {seed} | train={len(tr)} heldout={len(ho)} (noncomm={len(noncomm)}) --", flush=True)
            for arm in ARMS:
                P = init_params(N, A.d, A.h, seed, arm)
                fl = train(P, pairs, labels, tr, arm, A.tau, A.gamma if arm != "CE" else 0.0, A.steps, A.lr)
                tr_acc, _, _, _, _ = evaluate(P, pairs, labels, tr, arm, A.tau)
                ho_acc, reach, unreach, pred, y = evaluate(P, pairs, labels, ho, arm, A.tau)
                # non-commuting held-out accuracy
                nc_acc = float("nan")
                if noncomm:
                    nca, _, _, _, _ = evaluate(P, pairs, labels, noncomm, arm, A.tau)
                    nc_acc = nca
                distinct = int(np.unique(pred[pred == y]).size)
                rec = {"train_acc": round(tr_acc, 4), "ho_acc": round(ho_acc, 4),
                       "ho_noncomm_acc": round(nc_acc, 4), "reach": round(reach, 4),
                       "unreach": round(unreach, 5), "distinct": distinct, "final_loss": round(fl, 4)}
                out["runs"][tag][seed][arm] = rec
                print(f"   {arm:8s} train={tr_acc:.3f} ho={ho_acc:.3f} ho_nc={nc_acc:.3f} "
                      f"reach={reach:.3f} unreach={unreach:.4f} distinct={distinct:2d}", flush=True)

    # ------------- frozen-bar evaluation (FREEZE.md) -------------
    def col(tag, arm, field):
        return [out["runs"][tag][s][arm][field] for s in A.seeds]
    g = out["runs"]["GROUP"]
    c1 = sum(g[s]["G_trunk"]["ho_acc"] >= g[s]["CE"]["ho_acc"] + 0.10 for s in A.seeds)
    c2a = sum(g[s]["G_trunk"]["ho_acc"] >= g[s]["ADD"]["ho_acc"] + 0.15 for s in A.seeds)
    c2b = sum((g[s]["ADD"]["ho_noncomm_acc"] <= 0.55) and
              (g[s]["G_trunk"]["ho_noncomm_acc"] > g[s]["ADD"]["ho_noncomm_acc"] + 0.15) for s in A.seeds)
    c3 = sum(g[s]["G_trunk"]["ho_acc"] >= g[s]["G_read"]["ho_acc"] + 0.08 for s in A.seeds)
    sh = out["runs"]["SHUFFLE"]
    c4_advantage = sum(sh[s]["G_trunk"]["ho_acc"] >= sh[s]["CE"]["ho_acc"] + 0.10 for s in A.seeds)
    ns = len(A.seeds)
    clauses = {
        "c1_reach_earned_ge_CE+.10": f"{c1}/{ns}",
        "c2a_DPI_escape_ge_ADD+.15": f"{c2a}/{ns}",
        "c2b_noncomm_ADD<=.55_and_Gtrunk>ADD+.15": f"{c2b}/{ns}",
        "c3_trunk_ne_readout_ge_Gread+.08": f"{c3}/{ns}",
        "c4_SHUFFLE_advantage_must_vanish (want 0)": f"{c4_advantage}/{ns}",
    }
    passed = (c1 >= 3) and (c2a >= 3) and (c2b >= 3) and (c3 >= 3) and (c4_advantage == 0)
    out["frozen_bar"] = {"clauses": clauses, "verdict": "PASS" if passed else "FAIL",
                         "step1_gpu_authorized": passed}
    print("\n=== FROZEN BAR (FREEZE.md) ===", flush=True)
    for k, v in clauses.items():
        print(f"  {k}: {v}", flush=True)
    print(f"  => VERDICT: {'PASS' if passed else 'FAIL'} | STEP-1 engine-native authorized: {passed}", flush=True)
    with open(A.out, "w") as f:
        json.dump(out, f, indent=2)
    print(f"wrote {A.out}", flush=True)

if __name__ == "__main__":
    main()
