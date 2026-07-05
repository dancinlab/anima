#!/usr/bin/env python3
"""
Transfer-mechanism sweep — MECHANISM = tensor_product (Smolensky TPR / E4).
CORRECTED BINDING-DOMINANT TASK (pure bilinear einsum target, no linear a/b terms).
$0 numpy only.
"""
import json
import numpy as np

# task build
K, D = 256, 32
vec = np.random.RandomState(0).randn(K, D)
TDIM = 16
vec16 = vec[:, :TDIM]
T = np.random.RandomState(1).randn(TDIM, TDIM, TDIM)
TRAIN_IDX = np.arange(0, 192)
TEST_IDX = np.arange(192, 256)

def target(a_idx, b_idx):
    va = vec16[a_idx]; vb = vec16[b_idx]
    return np.tanh(np.einsum("kij,ni,nj->nk", T, va, vb))

def make_pairs(concept_idx, n, seed):
    rs = np.random.RandomState(seed)
    a = concept_idx[rs.randint(0, len(concept_idx), size=n)]
    b = concept_idx[rs.randint(0, len(concept_idx), size=n)]
    return a, b

ta, tb = make_pairs(TRAIN_IDX, 3000, 2)
va_, vb_ = make_pairs(TEST_IDX, 3000, 2)
A_tr, B_tr = vec[ta], vec[tb]
A_te, B_te = vec[va_], vec[vb_]
Y_tr = target(ta, tb)
Y_te = target(va_, vb_)
OUT = TDIM

def r2(pred, y):
    ss_res = np.sum((pred - y) ** 2)
    ss_tot = np.sum((y - y.mean(axis=0, keepdims=True)) ** 2)
    return 1.0 - ss_res / ss_tot

class Adam:
    def __init__(self, params, lr=1e-2, b1=0.9, b2=0.999, eps=1e-8):
        self.p, self.lr, self.b1, self.b2, self.eps = params, lr, b1, b2, eps
        self.m = {k: np.zeros_like(v) for k, v in params.items()}
        self.v = {k: np.zeros_like(v) for k, v in params.items()}
        self.t = 0
    def step(self, grads):
        self.t += 1
        for k in self.p:
            g = grads[k]
            self.m[k] = self.b1 * self.m[k] + (1 - self.b1) * g
            self.v[k] = self.b2 * self.v[k] + (1 - self.b2) * (g * g)
            mh = self.m[k] / (1 - self.b1 ** self.t)
            vh = self.v[k] / (1 - self.b2 ** self.t)
            self.p[k] -= self.lr * mh / (np.sqrt(vh) + self.eps)

EPOCHS, LR = 3000, 1e-2
RS = np.random.RandomState(42)

def train_additive():
    H = 64
    P = {"Wa": RS.randn(H, D) * 0.1, "Wb": RS.randn(H, D) * 0.1,
         "Wh": RS.randn(OUT, H) * 0.1, "bh": np.zeros(OUT)}
    opt = Adam(P, lr=LR); N = A_tr.shape[0]
    for _ in range(EPOCHS):
        EA = A_tr @ P["Wa"].T; EB = B_tr @ P["Wb"].T; R = EA + EB
        Pr = R @ P["Wh"].T + P["bh"]
        G = (Pr - Y_tr) * (2.0 / N)
        dWh = G.T @ R; dbh = G.sum(0); dR = G @ P["Wh"]
        opt.step({"Wa": dR.T @ A_tr, "Wb": dR.T @ B_tr, "Wh": dWh, "bh": dbh})
    return lambda A, B: (A @ P["Wa"].T + B @ P["Wb"].T) @ P["Wh"].T + P["bh"]

def train_tpr(p=16):
    P = {"Ra": RS.randn(p, D) * 0.1, "Rb": RS.randn(p, D) * 0.1,
         "Wh": RS.randn(OUT, p * p) * 0.05, "bh": np.zeros(OUT)}
    opt = Adam(P, lr=LR); N = A_tr.shape[0]
    for _ in range(EPOCHS):
        EA = A_tr @ P["Ra"].T
        EB = B_tr @ P["Rb"].T
        R3 = np.einsum("np,nq->npq", EA, EB)
        R = R3.reshape(N, p * p)
        Pr = R @ P["Wh"].T + P["bh"]
        G = (Pr - Y_tr) * (2.0 / N)
        dWh = G.T @ R; dbh = G.sum(0)
        dR = (G @ P["Wh"]).reshape(N, p, p)
        dEA = np.einsum("npq,nq->np", dR, EB)
        dEB = np.einsum("npq,np->nq", dR, EA)
        opt.step({"Ra": dEA.T @ A_tr, "Rb": dEB.T @ B_tr, "Wh": dWh, "bh": dbh})
    def fwd(A, B):
        EA = A @ P["Ra"].T; EB = B @ P["Rb"].T
        R = np.einsum("np,nq->npq", EA, EB).reshape(A.shape[0], p * p)
        return R @ P["Wh"].T + P["bh"]
    return fwd

def softmax(x):
    x = x - x.max(axis=1, keepdims=True); e = np.exp(x)
    return e / e.sum(axis=1, keepdims=True)

def train_slot(S=16, dv=16):
    P = {"Wk": RS.randn(S, D) * 0.1, "Wv": RS.randn(dv, D) * 0.1,
         "Wh": RS.randn(OUT, S * dv) * 0.05, "bh": np.zeros(OUT)}
    opt = Adam(P, lr=LR); N = A_tr.shape[0]
    for _ in range(EPOCHS):
        Kk = A_tr @ P["Wk"].T; alpha = softmax(Kk)
        V = B_tr @ P["Wv"].T
        R3 = np.einsum("ns,nv->nsv", alpha, V)
        R = R3.reshape(N, S * dv)
        Pr = R @ P["Wh"].T + P["bh"]
        G = (Pr - Y_tr) * (2.0 / N)
        dWh = G.T @ R; dbh = G.sum(0)
        dR = (G @ P["Wh"]).reshape(N, S, dv)
        dalpha = np.einsum("nsv,nv->ns", dR, V)
        dV = np.einsum("nsv,ns->nv", dR, alpha)
        dK = alpha * (dalpha - (dalpha * alpha).sum(axis=1, keepdims=True))
        opt.step({"Wk": dK.T @ A_tr, "Wv": dV.T @ B_tr, "Wh": dWh, "bh": dbh})
    def fwd(A, B):
        alpha = softmax(A @ P["Wk"].T); V = B @ P["Wv"].T
        R = np.einsum("ns,nv->nsv", alpha, V).reshape(A.shape[0], S * dv)
        return R @ P["Wh"].T + P["bh"]
    return fwd

def evaluate(fwd):
    return (r2(fwd(A_tr, B_tr), Y_tr),
            r2(fwd(A_te, B_te), Y_te),
            r2(fwd(B_te, A_te), Y_te))

print("training additive ..."); add_tr, add_cross, add_shuf = evaluate(train_additive())
print("training tensor_product ..."); tpr_tr, tpr_cross, tpr_shuf = evaluate(train_tpr())
print("training slot (anchor) ..."); slot_tr, slot_cross, slot_shuf = evaluate(train_slot())

anchor_ok = slot_cross >= add_cross + 0.15
mech_gain = tpr_cross - add_cross
shuffle_drop = tpr_cross - tpr_shuf
transfer_earning = (mech_gain >= 0.15) and (shuffle_drop >= 0.15)
verdict = ("INCONCLUSIVE-task-artifact" if not anchor_ok
           else ("TRANSFER-EARNING" if transfer_earning else "NO-TRANSFER"))

res = {
    "mechanism": "tensor_product",
    "spec": "Smolensky TPR (E4): r = flatten(role_enc(a) x filler_enc(b)); learned encoders 32->16, linear head, end-to-end Adam",
    "task": "CORRECTED binding-dominant non-commutative pure-bilinear tanh(a^T T b); concepts 256x32, target on first 16 dims; T=RandomState(1).randn(16,16,16)",
    "epochs": EPOCHS, "lr": LR,
    "additive": {"train_r2": add_tr, "cross_r2": add_cross, "shuffle_r2": add_shuf},
    "tensor_product": {"train_r2": tpr_tr, "cross_r2": tpr_cross, "shuffle_r2": tpr_shuf},
    "slot_anchor": {"train_r2": slot_tr, "cross_r2": slot_cross, "shuffle_r2": slot_shuf},
    "anchor_ok": bool(anchor_ok),
    "mech_gain_vs_additive": mech_gain,
    "shuffle_drop": shuffle_drop,
    "criteria": "TRANSFER-EARNING iff (crossR2_mech - crossR2_additive) >= 0.15 AND shuffle_drop >= 0.15; anchor slot must clear additive+0.15 else INCONCLUSIVE",
    "verdict": verdict,
}
print(json.dumps(res, indent=2, default=float))
with open("/Users/mini/dancinlab/anima/state/transfer_mechanism_sweep/tensor_product/RESULT.json", "w") as fh:
    json.dump(res, fh, indent=2, default=float)
