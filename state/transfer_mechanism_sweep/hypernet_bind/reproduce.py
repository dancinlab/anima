#!/usr/bin/env python3
"""
transfer_mechanism_sweep :: hypernet_bind (CORRECTED binding-dominant target, run-2)

SHARED SYNTHETIC TASK (reference-match, conv transfer-mechanism-sweep-workflow-js-1):
  concepts: vec = RandomState(0).randn(256,32)  (K=256, d=32 fixed vectors)
  disjoint split: TRAIN concepts 0-191 (192), TEST concepts 192-255 (64), overlap 0
  BINDING-DOMINANT non-commutative target (pure bilinear form, NO linear a/b terms):
      T = RandomState(1).randn(16,16,16)   (d=16, out=16)
      t(a,b) = tanh( einsum("kij,i,j->k", T, va16, vb16) )      va16 = vec[a][:16]
    -> additive (Wa@a+Wb@b) cannot express a bilinear form -> low R^2 floor
    -> T is (i,j)-asymmetric -> t(a,b) != t(b,a) (non-commutative)
    -> bilinear in the fixed vectors -> transfers to UNSEEN concepts (T fixed)
  TRAIN pairs: 3000 ordered pairs from TRAIN concepts (seed2)
  TEST  pairs: 3000 ordered pairs from TEST  concepts (unseen)  = CROSS-DISTRIBUTION
  measure: TEST cross R^2. controls: (a) ADDITIVE baseline (b) ORDER-SHUFFLE (swap a,b)
  ANCHOR-VALIDATION: slot_gated_write (E1 known escape) must clear cross >= additive+0.15,
    else task is still artifact -> verdict INCONCLUSIVE-task-artifact.
  verdict TRANSFER-EARNING iff cross(mech)-cross(additive) >= 0.15 AND shuffle drop >= 0.15.

MY MECHANISM = hypernet_bind:
  role a generates a small weight matrix M(a) (hypernetwork); apply to filler enc(b):
      filler = Wf @ vec[b]            (p,)
      M(a)   = reshape(Wh @ vec[a], (q,p))
      r      = M(a) @ filler          (q,)   -> role mediates transform = non-commutative bind
      pred   = tanh(Head @ r + bh)    (16,)

$0 numpy only. Manual backprop + full-batch Adam. mini-safe small synthetic.
"""
import json, os, shutil
import numpy as np

REPO_DIR = "/Users/mini/dancinlab/anima/state/transfer_mechanism_sweep/hypernet_bind"

K, D = 256, 32
DT = 16
vec = np.random.RandomState(0).randn(K, D)
T   = np.random.RandomState(1).randn(DT, DT, DT)

TRAIN_C = np.arange(0, 192)
TEST_C  = np.arange(192, 256)

def make_pairs(concepts, n, seed):
    rs = np.random.RandomState(seed)
    a = concepts[rs.randint(0, len(concepts), size=n)]
    b = concepts[rs.randint(0, len(concepts), size=n)]
    return a, b

def target(a, b):
    va = vec[a][:, :DT]; vb = vec[b][:, :DT]
    z  = np.einsum("kij,ni,nj->nk", T, va, vb)
    return np.tanh(z)

atr, btr = make_pairs(TRAIN_C, 3000, 2)
ate, bte = make_pairs(TEST_C, 3000, 2)
ttr = target(atr, btr); tte = target(ate, bte)
Xa_tr, Xb_tr = vec[atr], vec[btr]
Xa_te, Xb_te = vec[ate], vec[bte]
O = DT

def r2(pred, t):
    return 1.0 - np.sum((pred - t) ** 2) / np.sum((t - t.mean()) ** 2)

class Adam:
    def __init__(self, params, lr):
        self.p = params; self.lr = lr
        self.m = {k: np.zeros_like(v) for k, v in params.items()}
        self.v = {k: np.zeros_like(v) for k, v in params.items()}
        self.t = 0; self.b1 = 0.9; self.b2 = 0.999; self.eps = 1e-8
    def step(self, g):
        self.t += 1
        for k in self.p:
            self.m[k] = self.b1 * self.m[k] + (1 - self.b1) * g[k]
            self.v[k] = self.b2 * self.v[k] + (1 - self.b2) * g[k] ** 2
            mh = self.m[k] / (1 - self.b1 ** self.t)
            vh = self.v[k] / (1 - self.b2 ** self.t)
            self.p[k] -= self.lr * mh / (np.sqrt(vh) + self.eps)

def head_forward(r, P):
    z = r @ P["Head"].T + P["bh"]
    return z, np.tanh(z)

def head_backward(dpred, z, pred, r, P, g):
    dz = dpred * (1 - pred ** 2)
    g["Head"] = dz.T @ r
    g["bh"]   = dz.sum(0)
    return dz @ P["Head"]

def init_additive(R, seed):
    rs = np.random.RandomState(seed)
    return {"Wa": rs.randn(R, D)*0.1, "Wb": rs.randn(R, D)*0.1,
            "Head": rs.randn(O, R)*0.1, "bh": np.zeros(O)}, R
def fwd_additive(P, Xa, Xb):
    return Xa @ P["Wa"].T + Xb @ P["Wb"].T, (Xa, Xb)
def bwd_additive(dr, cache, P, g):
    Xa, Xb = cache; g["Wa"] = dr.T @ Xa; g["Wb"] = dr.T @ Xb

def init_hypernet(q, p, seed):
    rs = np.random.RandomState(seed)
    return {"Wh": rs.randn(q*p, D)*0.1, "Wf": rs.randn(p, D)*0.1,
            "Head": rs.randn(O, q)*0.1, "bh": np.zeros(O), "_q": q, "_p": p}, q
def fwd_hypernet(P, Xa, Xb):
    q, p = P["_q"], P["_p"]; n = Xa.shape[0]
    filler = Xb @ P["Wf"].T
    M = (Xa @ P["Wh"].T).reshape(n, q, p)
    r = np.einsum("nqp,np->nq", M, filler)
    return r, (Xa, Xb, filler, M, q, p, n)
def bwd_hypernet(dr, cache, P, g):
    Xa, Xb, filler, M, q, p, n = cache
    dM      = np.einsum("nq,np->nqp", dr, filler)
    dfiller = np.einsum("nq,nqp->np", dr, M)
    g["Wh"] = dM.reshape(n, q*p).T @ Xa
    g["Wf"] = dfiller.T @ Xb

def init_slot(N, m, seed):
    rs = np.random.RandomState(seed)
    return {"Wg": rs.randn(N, D)*0.1, "Wv": rs.randn(m, D)*0.1,
            "Head": rs.randn(O, N*m)*0.1, "bh": np.zeros(O), "_N": N, "_m": m}, N*m
def fwd_slot(P, Xa, Xb):
    N, m = P["_N"], P["_m"]; n = Xa.shape[0]
    pre = Xa @ P["Wg"].T; pre = pre - pre.max(1, keepdims=True)
    e = np.exp(pre); gsoft = e / e.sum(1, keepdims=True)
    v = Xb @ P["Wv"].T
    S = np.einsum("nN,nm->nNm", gsoft, v)
    return S.reshape(n, N*m), (Xa, Xb, gsoft, v, N, m, n)
def bwd_slot(dr, cache, P, g):
    Xa, Xb, gsoft, v, N, m, n = cache
    dS = dr.reshape(n, N, m)
    dg = np.einsum("nNm,nm->nN", dS, v)
    dv = np.einsum("nNm,nN->nm", dS, gsoft)
    dpre = gsoft * (dg - (gsoft * dg).sum(1, keepdims=True))
    g["Wg"] = dpre.T @ Xa; g["Wv"] = dv.T @ Xb

def train(P, R, fwd, bwd, epochs, lr):
    keys = [k for k in P if not k.startswith("_")]
    opt = Adam({k: P[k] for k in keys}, lr)
    n = Xa_tr.shape[0]
    for _ in range(epochs):
        r, cache = fwd(P, Xa_tr, Xb_tr)
        z, pred = head_forward(r, P)
        dpred = (2.0 / (n * O)) * (pred - ttr)
        g = {}
        dr = head_backward(dpred, z, pred, r, P, g)
        bwd(dr, cache, P, g)
        opt.step({k: g[k] for k in keys})
    r, _ = fwd(P, Xa_tr, Xb_tr); _, ptr = head_forward(r, P)
    r, _ = fwd(P, Xa_te, Xb_te); _, pte = head_forward(r, P)
    r, _ = fwd(P, Xb_te, Xa_te); _, psh = head_forward(r, P)
    return r2(ptr, ttr), r2(pte, tte), r2(psh, tte)

np.seterr(all="ignore")
EP, LR = 4000, 3e-3

Padd, Radd = init_additive(64, 7)
add_tr, add_cross, add_sh = train(Padd, Radd, fwd_additive, bwd_additive, EP, LR)
Phyp, Rhyp = init_hypernet(16, 16, 11)
hyp_tr, hyp_cross, hyp_sh = train(Phyp, Rhyp, fwd_hypernet, bwd_hypernet, EP, LR)
Pslot, Rslot = init_slot(8, 16, 13)
slot_tr, slot_cross, slot_sh = train(Pslot, Rslot, fwd_slot, bwd_slot, EP, LR)

GAP, DROP = 0.15, 0.15
anchor_ok = (slot_cross - add_cross) >= GAP and (slot_cross - slot_sh) >= DROP
def judge(cross, sh):
    return "TRANSFER-EARNING" if (cross - add_cross) >= GAP and (cross - sh) >= DROP else "NO-TRANSFER"
verdict = judge(hyp_cross, hyp_sh) if anchor_ok else "INCONCLUSIVE-task-artifact"

out = {
    "mechanism": "hypernet_bind",
    "run": "run-2 CORRECTED binding-dominant pure-bilinear target",
    "spec": "role a -> M(a)=reshape(Wh@a); filler=Wf@b; r=M(a)@filler; pred=tanh(Head@r+bh)",
    "task": {
        "K": K, "d": D, "target_dim": DT,
        "target": "tanh(einsum('kij,i,j->k', T~N(0,1)(16,16,16), va[:16], vb[:16])) pure bilinear non-commutative",
        "train_concepts": [0, 191], "test_concepts": [192, 255], "overlap": 0,
        "n_train_pairs": 3000, "n_test_pairs": 3000,
        "epochs": EP, "opt": "Adam full-batch", "lr": LR, "hypernet_dims": {"q": 16, "p": 16},
    },
    "thresholds": {"gap_vs_additive_min": GAP, "shuffle_drop_min": DROP},
    "additive_baseline": {"train_r2": round(add_tr, 4), "cross_r2": round(add_cross, 4), "shuffle_r2": round(add_sh, 4)},
    "anchor_slot_gated_write": {
        "train_r2": round(slot_tr, 4), "cross_r2": round(slot_cross, 4), "shuffle_r2": round(slot_sh, 4),
        "gap_vs_additive": round(slot_cross - add_cross, 4), "shuffle_drop": round(slot_cross - slot_sh, 4),
        "passes_anchor": bool(anchor_ok),
    },
    "hypernet_bind": {
        "train_r2": round(hyp_tr, 4), "cross_r2": round(hyp_cross, 4), "shuffle_r2": round(hyp_sh, 4),
        "gap_vs_additive": round(hyp_cross - add_cross, 4), "shuffle_drop": round(hyp_cross - hyp_sh, 4),
    },
    "verdict": verdict,
}
print(json.dumps(out, indent=2))
os.makedirs(REPO_DIR, exist_ok=True)
with open(os.path.join(REPO_DIR, "RESULT.json"), "w") as f:
    json.dump(out, f, indent=2)
shutil.copy(os.path.abspath(__file__), os.path.join(REPO_DIR, "reproduce.py"))
