#!/usr/bin/env python3
"""
Transfer-mechanism sweep — MECH = slot_gated_write (E1 anchor / known escape).

CORRECTED binding-dominant shared task (conv transfer-mechanism-sweep-workflow-js-1):
the 1st-run additive-dominant target was a task-artifact; this uses a PURE BILINEAR
non-commutative target so additive is structurally floored.

Shared task (identical across all agents; mechanism only is swapped):
  - K=256 concepts, d=32 fixed vectors: np.random.RandomState(0).randn(256,32).
  - DISJOINT split: TRAIN idx 0-191 (192), TEST idx 192-255 (64). overlap 0.
  - TARGET (pure bilinear, non-commutative, no linear a/b terms):
        T = np.random.RandomState(1).randn(16,16,16)      # d=16, out=16
        t(a,b) = tanh( einsum("kij,i,j->k", T, a16, b16) )
    where a16 = vec[a][:16], b16 = vec[b][:16] (T is 16-dim; concepts are 32-dim).
    T asymmetric in (i,j) => t(a,b) != t(b,a). Bilinear form fixed by T => transfers to
    unseen concept vectors. additive(Wa@a+Wb@b) cannot represent a bilinear form.
  - TRAIN pairs: 3000 ordered pairs within TRAIN concepts (seed 2).
  - TEST  pairs: 3000 ordered pairs within TEST  concepts (seed 3) = CROSS-DISTRIBUTION.
  - Mechanism params + linear head trained end-to-end (numpy Adam), MSE, ~3000 epoch.

MECHANISM = SLOT / gated-write (E1):
  role a decides the ADDRESS (soft gate over N slots), filler b provides the VALUE;
  binding = outer(gate, value) written into an N x Dv slot memory, read out flat.
      q=Wq@a ; gate=softmax_k(q.slot_k) ; v=Wv@b ; M=outer(gate,v) ; pred=Whead@vec(M)+b
  Asymmetric (a->gate via Wq, b->value via Wv) => order-sensitive by construction.

Controls (pre-registered, frozen):
  (a) ADDITIVE baseline: optimal linear pred = W@[a;b]+c (closed-form OLS on same inputs).
  (b) ORDER-SHUFFLE: trained mech on TEST pairs with a,b swapped, scored vs TRUE target.

Verdict (frozen): TRANSFER-EARNING iff
      cross_R2 - additive_R2 >= 0.15  AND  (cross_R2 - shuffle_R2) >= 0.15. else NO-TRANSFER.
Anchor role: slot IS the known escape; if it fails the bar the task is under-powered.
$0 numpy only. Deterministic.
"""
import numpy as np, json, os

K, D = 256, 32
vec = np.random.RandomState(0).randn(K, D).astype(np.float64)
TD  = 16
T   = np.random.RandomState(1).randn(TD, TD, TD).astype(np.float64)
TRAIN_IDX = np.arange(0, 192)
TEST_IDX  = np.arange(192, 256)

def target(a_idx, b_idx):
    a16 = vec[a_idx][:, :TD]; b16 = vec[b_idx][:, :TD]
    return np.tanh(np.einsum("kij,ni,nj->nk", T, a16, b16))

def make_pairs(pool, n, seed):
    rng = np.random.RandomState(seed)
    return rng.choice(pool, size=n), rng.choice(pool, size=n)

aTr, bTr = make_pairs(TRAIN_IDX, 3000, 2)
aTe, bTe = make_pairs(TEST_IDX,  3000, 3)
Xa_tr, Xb_tr = vec[aTr], vec[bTr]
Xa_te, Xb_te = vec[aTe], vec[bTe]
Ytr, Yte = target(aTr, bTr), target(aTe, bTe)

def r2(pred, true):
    return 1.0 - np.sum((pred - true) ** 2) / np.sum((true - true.mean()) ** 2)

def additive_baseline():
    Phi_tr = np.concatenate([Xa_tr, Xb_tr, np.ones((len(Xa_tr), 1))], 1)
    Phi_te = np.concatenate([Xa_te, Xb_te, np.ones((len(Xa_te), 1))], 1)
    A = Phi_tr.T @ Phi_tr + 1e-6 * np.eye(Phi_tr.shape[1])
    W = np.linalg.solve(A, Phi_tr.T @ Ytr)
    return r2(Phi_te @ W, Yte)

N_SLOT, H, DV, OUT = 8, 32, 32, TD

def init_params(seed=7):
    rng = np.random.RandomState(seed)
    return {"Wq": rng.randn(H, D)/np.sqrt(D), "slot": rng.randn(N_SLOT, H)/np.sqrt(H),
            "Wv": rng.randn(DV, D)/np.sqrt(D),
            "Whead": rng.randn(OUT, N_SLOT*DV)/np.sqrt(N_SLOT*DV), "bhead": np.zeros(OUT)}

def softmax(l):
    e = np.exp(l - l.max(1, keepdims=True)); return e / e.sum(1, keepdims=True)

def forward(P, A, B):
    n = A.shape[0]
    q = A @ P["Wq"].T
    gate = softmax(q @ P["slot"].T / np.sqrt(H))
    v = B @ P["Wv"].T
    M = gate[:, :, None] * v[:, None, :]
    r = M.reshape(n, N_SLOT*DV)
    pred = r @ P["Whead"].T + P["bhead"]
    return pred, (A, B, q, gate, v, r)

def backward(P, cache, dpred):
    A, B, q, gate, v, r = cache
    g = {}
    g["Whead"] = dpred.T @ r
    g["bhead"] = dpred.sum(0)
    dM = (dpred @ P["Whead"]).reshape(-1, N_SLOT, DV)
    dgate = np.einsum("nkd,nd->nk", dM, v)
    dv    = np.einsum("nkd,nk->nd", dM, gate)
    g["Wv"] = dv.T @ B
    dlogit = gate * (dgate - (gate*dgate).sum(1, keepdims=True)) / np.sqrt(H)
    g["slot"] = dlogit.T @ q
    g["Wq"] = (dlogit @ P["slot"]).T @ A
    return g

def loss_and_grad(P, A, B, Y):
    pred, cache = forward(P, A, B)
    diff = pred - Y
    return np.mean(diff**2), backward(P, cache, 2.0*diff/(A.shape[0]*OUT))

def grad_check():
    rng = np.random.RandomState(99)
    P = init_params(3)
    A = vec[rng.choice(TRAIN_IDX, 12)]; B = vec[rng.choice(TRAIN_IDX, 12)]
    Y = np.tanh(rng.randn(12, OUT))
    _, g = loss_and_grad(P, A, B, Y)
    eps, worst = 1e-6, 0.0
    for name in ["Wq", "slot", "Wv", "Whead", "bhead"]:
        Wf, gf = P[name].ravel(), g[name].ravel()
        for i in np.random.RandomState(4).choice(len(Wf), min(6, len(Wf)), replace=False):
            old = Wf[i]
            Wf[i] = old+eps; lp, _ = loss_and_grad(P, A, B, Y)
            Wf[i] = old-eps; lm, _ = loss_and_grad(P, A, B, Y)
            Wf[i] = old
            num = (lp-lm)/(2*eps)
            worst = max(worst, abs(num-gf[i])/(abs(num)+abs(gf[i])+1e-12))
    return worst

def train(epochs=3000, lr=3e-3):
    P = init_params(7)
    m = {k: np.zeros_like(v) for k, v in P.items()}
    vv = {k: np.zeros_like(v) for k, v in P.items()}
    b1, b2, eps = 0.9, 0.999, 1e-8
    for t in range(1, epochs+1):
        _, g = loss_and_grad(P, Xa_tr, Xb_tr, Ytr)
        for k in P:
            m[k] = b1*m[k] + (1-b1)*g[k]
            vv[k] = b2*vv[k] + (1-b2)*g[k]**2
            P[k] -= lr * (m[k]/(1-b1**t)) / (np.sqrt(vv[k]/(1-b2**t)) + eps)
    return P

if __name__ == "__main__":
    gc_rel = grad_check()
    add_r2 = additive_baseline()
    P = train()
    pred_tr, _ = forward(P, Xa_tr, Xb_tr)
    pred_te, _ = forward(P, Xa_te, Xb_te)
    train_r2, cross_r2 = r2(pred_tr, Ytr), r2(pred_te, Yte)
    pred_sh, _ = forward(P, Xb_te, Xa_te)
    shuffle_r2 = r2(pred_sh, Yte)
    delta_add, shuffle_drop = cross_r2 - add_r2, cross_r2 - shuffle_r2
    te = (delta_add >= 0.15) and (shuffle_drop >= 0.15)
    out = {"mechanism": "slot_gated_write", "role": "E1 anchor (known escape / control)",
           "task": "corrected pure-bilinear non-commutative t(a,b)=tanh(einsum(kij,i,j->k,T,a16,b16))",
           "task_params": {"K": K, "d_concept": D, "d_target": TD, "out": OUT, "T_seed": 1,
                           "vec_seed": 0, "train_idx": "0-191", "test_idx": "192-255",
                           "train_pairs": 3000, "test_pairs": 3000, "pair_seeds": [2, 3]},
           "mech_params": {"N_slots": N_SLOT, "H": H, "Dv": DV, "epochs": 3000,
                           "opt": "adam", "lr": 3e-3, "init_seed": 7},
           "gradcheck_rel_err": float(gc_rel), "train_r2": float(train_r2),
           "cross_r2": float(cross_r2), "additive_r2": float(add_r2),
           "shuffle_r2": float(shuffle_r2), "delta_vs_additive": float(delta_add),
           "shuffle_drop": float(shuffle_drop),
           "bar_delta_add>=0.15": bool(delta_add >= 0.15),
           "bar_shuffle_drop>=0.15": bool(shuffle_drop >= 0.15),
           "anchor_clears_bar": bool(delta_add >= 0.15),
           "verdict": "TRANSFER-EARNING" if te else "NO-TRANSFER"}
    print(json.dumps(out, indent=2))
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "RESULT.json"), "w") as f:
        json.dump(out, f, indent=2)
