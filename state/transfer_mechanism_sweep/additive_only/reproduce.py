#!/usr/bin/env python3
"""
Transfer-mechanism sweep cell = additive_only (baseline anchor).

SHARED SYNTHETIC TASK (binding-dominant, non-commutative — corrected 2nd run):
  K=256 concepts, vec = RandomState(0).randn(256,32); use first 16 dims (V16)
  because the bilinear tensor T is (16,16,16) (einsum "kij,i,j->k").
  DISJOINT split: TRAIN concept idx 0..191, TEST idx 192..255 (overlap 0).
  TARGET t(a,b) = tanh( einsum("kij,i,j->k", T, V16[a], V16[b]) )
    T = RandomState(1).randn(16,16,16). PURE bilinear form: no linear a/b term
    -> additive(Wa@a+Wb@b) structurally cannot represent it (R^2 low, expect <~0.3).
    T asymmetric in (i,j) -> t(a,b) != t(b,a) (non-commutative).
    T fixed -> transfers to unseen concept vectors (cross-distribution).
  TRAIN pairs: 3000 ordered (a,b), both sampled iid from 0..191, seed 2.
  TEST  pairs: 3000 ordered (a,b), both sampled iid from 192..255, seed 3
               = CROSS-DISTRIBUTION (concepts never seen in training).

  MECHANISM (this cell) = additive_only:
      r = Wa @ V16[a] + Wb @ V16[b]   (order-blind sum; H=64)
      pred = Wh @ r + b0              (linear head, out=16)
  Composes to a purely LINEAR map of (a,b) -> cannot express bilinear T.
  Trained end-to-end (Adam, full-batch, 3000 epoch) it converges to the least
  -squares linear fit; its cross R^2 is the additive floor.

  Controls:
    (a) ADDITIVE baseline == this mechanism (so cross_r2_mech == cross_r2_additive
        by construction; delta=0). This cell IS the baseline anchor.
    (b) ORDER-SHUFFLE: swap test (a,b) -> R^2 must collapse if any order signal.
    ANCHOR-VALIDATION: also train slot_gated_write (multiplicative bind, the known
        E1 escape). If it does NOT clear cross_r2 >= additive + 0.15, the task is a
        still-broken artifact -> verdict INCONCLUSIVE-task-artifact.

  Verdict (mech=additive): TRANSFER-EARNING iff
      cross_r2_mech - cross_r2_additive >= 0.15  AND  shuffle_drop >= 0.15.
  For additive_only the first term is 0 by construction -> expected NO-TRANSFER.
"""
import json, os
import numpy as np

OUTDIR = os.environ.get("OUTDIR", os.path.dirname(os.path.abspath(__file__)))

# ---------------- shared task ----------------
K, D_FULL, D = 256, 32, 16
vec = np.random.RandomState(0).randn(K, D_FULL)
V16 = vec[:, :D]                                   # (256,16)
T = np.random.RandomState(1).randn(D, D, D)        # (16,16,16) k,i,j

N_PAIRS = 3000

def sample_pairs(lo, hi, n, seed):
    r = np.random.RandomState(seed)
    return r.randint(lo, hi, n), r.randint(lo, hi, n)

a_tr, b_tr = sample_pairs(0, 192, N_PAIRS, 2)
a_te, b_te = sample_pairs(192, 256, N_PAIRS, 3)

def target(a_idx, b_idx):
    A = V16[a_idx]; B = V16[b_idx]                 # (N,16)
    z = np.einsum("kij,ni,nj->nk", T, A, B)        # (N,16)
    return np.tanh(z)

A_tr, B_tr, Y_tr = V16[a_tr], V16[b_tr], target(a_tr, b_tr)
A_te, B_te, Y_te = V16[a_te], V16[b_te], target(a_te, b_te)
# order-shuffle test = feed swapped inputs, keep the true (a,b) target
A_sh, B_sh, Y_sh = V16[b_te], V16[a_te], Y_te

def r2(pred, y):
    ss_res = np.sum((pred - y) ** 2)
    ss_tot = np.sum((y - y.mean(axis=0)) ** 2)
    return 1.0 - ss_res / ss_tot

# ---------------- Adam ----------------
class Adam:
    def __init__(self, params, lr=0.01, b1=0.9, b2=0.999, eps=1e-8):
        self.p = params; self.lr = lr; self.b1 = b1; self.b2 = b2; self.eps = eps
        self.m = [np.zeros_like(x) for x in params]
        self.v = [np.zeros_like(x) for x in params]
        self.t = 0
    def step(self, grads):
        self.t += 1
        for i, g in enumerate(grads):
            self.m[i] = self.b1 * self.m[i] + (1 - self.b1) * g
            self.v[i] = self.b2 * self.v[i] + (1 - self.b2) * g * g
            mh = self.m[i] / (1 - self.b1 ** self.t)
            vh = self.v[i] / (1 - self.b2 ** self.t)
            self.p[i] -= self.lr * mh / (np.sqrt(vh) + self.eps)

H, OUT = 64, D

# ---------------- additive mechanism ----------------
def train_additive(epochs=3000, lr=0.01, seed=10):
    rs = np.random.RandomState(seed)
    Wa = rs.randn(H, D) * 0.1
    Wb = rs.randn(H, D) * 0.1
    Wh = rs.randn(OUT, H) * 0.1
    b0 = np.zeros(OUT)
    opt = Adam([Wa, Wb, Wh, b0], lr=lr)
    N = A_tr.shape[0]
    for _ in range(epochs):
        r = A_tr @ Wa.T + B_tr @ Wb.T
        pred = r @ Wh.T + b0
        d = 2.0 * (pred - Y_tr) / (N * OUT)
        dWh = d.T @ r
        db0 = d.sum(0)
        dr = d @ Wh
        dWa = dr.T @ A_tr
        dWb = dr.T @ B_tr
        opt.step([dWa, dWb, dWh, db0])
    return lambda A, B: (A @ Wa.T + B @ Wb.T) @ Wh.T + b0

# ---------------- slot gated-write anchor (E1 escape) ----------------
def train_slot(epochs=3000, lr=0.01, seed=11):
    # r = gate(a) * value(b): multiplicative gated write into a slot.
    # = sum of H rank-1 bilinear terms -> can represent fixed tensor T and
    #   transfer to unseen concepts (the known cross-distribution escape).
    rs = np.random.RandomState(seed)
    Wg = rs.randn(H, D) * 0.3
    Wv = rs.randn(H, D) * 0.3
    Wh = rs.randn(OUT, H) * 0.1
    b0 = np.zeros(OUT)
    opt = Adam([Wg, Wv, Wh, b0], lr=lr)
    N = A_tr.shape[0]
    for _ in range(epochs):
        g = A_tr @ Wg.T
        v = B_tr @ Wv.T
        r = g * v
        pred = r @ Wh.T + b0
        d = 2.0 * (pred - Y_tr) / (N * OUT)
        dWh = d.T @ r
        db0 = d.sum(0)
        dr = d @ Wh
        dWg = (dr * v).T @ A_tr
        dWv = (dr * g).T @ B_tr
        opt.step([dWg, dWv, dWh, db0])
    return lambda A, B: ((A @ Wg.T) * (B @ Wv.T)) @ Wh.T + b0

# ---------------- run ----------------
add_fwd = train_additive()
add_train_r2 = r2(add_fwd(A_tr, B_tr), Y_tr)
add_cross_r2 = r2(add_fwd(A_te, B_te), Y_te)
add_shuffle_r2 = r2(add_fwd(A_sh, B_sh), Y_sh)

slot_fwd = train_slot()
slot_train_r2 = r2(slot_fwd(A_tr, B_tr), Y_tr)
slot_cross_r2 = r2(slot_fwd(A_te, B_te), Y_te)
slot_shuffle_r2 = r2(slot_fwd(A_sh, B_sh), Y_sh)

cross_r2_mech = add_cross_r2
cross_r2_additive = add_cross_r2
delta_vs_additive = cross_r2_mech - cross_r2_additive          # 0 by construction
shuffle_drop = cross_r2_mech - add_shuffle_r2

anchor_delta = slot_cross_r2 - add_cross_r2
anchor_valid = anchor_delta >= 0.15

if not anchor_valid:
    verdict = "INCONCLUSIVE-task-artifact"
elif delta_vs_additive >= 0.15 and shuffle_drop >= 0.15:
    verdict = "TRANSFER-EARNING"
else:
    verdict = "NO-TRANSFER"

result = {
    "mechanism": "additive_only",
    "task": "binding-dominant non-commutative bilinear, cross-distribution (disjoint concept split)",
    "config": {
        "K": K, "d_full": D_FULL, "d_used": D, "out": OUT, "H": H,
        "train_concepts": [0, 191], "test_concepts": [192, 255],
        "n_train_pairs": N_PAIRS, "n_test_pairs": N_PAIRS,
        "target": "tanh(einsum(kij,i,j->k, T~RS(1), V16[a], V16[b])) PURE bilinear, no linear term",
        "opt": "adam", "lr": 0.01, "epochs": 3000,
    },
    "mechanism_forward": "r = Wa@a + Wb@b (order-blind sum); pred = Wh@r + b0",
    "train_r2_mech": round(float(add_train_r2), 4),
    "cross_r2_mech": round(float(cross_r2_mech), 4),
    "cross_r2_additive": round(float(cross_r2_additive), 4),
    "cross_r2_shuffle": round(float(add_shuffle_r2), 4),
    "delta_vs_additive": round(float(delta_vs_additive), 4),
    "shuffle_drop": round(float(shuffle_drop), 4),
    "anchor_slot_gated_write": {
        "note": "E1 known escape = multiplicative gated-write slot (bilinear-capable). Must clear additive+0.15 to validate the task harness.",
        "train_r2": round(float(slot_train_r2), 4),
        "cross_r2": round(float(slot_cross_r2), 4),
        "cross_r2_shuffle": round(float(slot_shuffle_r2), 4),
        "delta_vs_additive": round(float(anchor_delta), 4),
        "clears_bar": bool(anchor_valid),
    },
    "thresholds": {"delta_add>=": 0.15, "shuffle_drop>=": 0.15},
    "verdict": verdict,
    "interpretation": (
        "additive_only IS the baseline anchor: its cross R2 equals the additive floor by "
        "construction (delta=0). On the pure-bilinear (binding-dominant) target the "
        "order-blind additive sum cannot represent the non-commutative form, so cross R2 "
        "is low and it earns no transfer. The slot anchor clears +0.15, confirming a valid "
        "binding-dominant harness (not an additive-dominant artifact)."
        if anchor_valid else
        "Slot anchor failed to clear +0.15 -> task still artifact; mechanism judgment withheld."
    ),
}

with open(os.path.join(OUTDIR, "RESULT.json"), "w") as f:
    json.dump(result, f, indent=2)
print(json.dumps(result, indent=2))
