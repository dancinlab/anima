#!/usr/bin/env python3
"""
Transfer-mechanism sweep — MECHANISM = multiplicative_film (FiLM gating, E5).

SHARED SYNTHETIC TASK (reference-match, identical across all agents):
  K=256 concepts, d=32 vectors: vec = RandomState(0).randn(256,32).
  DISJOINT split: TRAIN concepts 0-191, TEST concepts 192-255 (overlap 0).
  Non-commutative binding target:
     t(a,b) = tanh(Wr@vec[a] + Wf@vec[b] + vec[a]*roll(vec[b], roll))
     Wr,Wf,roll fixed by seed1  -> order-dependent: t(a,b) != t(b,a).
  Each mechanism maps (vec[a],vec[b]) -> rep r; a linear head regresses t;
  mechanism params + head trained END-TO-END (Adam, numpy).
  TRAIN pairs: 3000 ordered pairs within TRAIN concepts (seed2).
  TEST  pairs: 3000 ordered pairs within TEST concepts (unseen concepts)
               = CROSS-DISTRIBUTION transfer.
  Controls:
    (a) ADDITIVE baseline r = Wa@a + Wb@b (order-blind interaction), trained too.
    (b) ORDER-SHUFFLE: at test, randomly swap (a,b) -> destroy order info.
  Verdict: TRANSFER-EARNING iff
     cross_R2(mech) - cross_R2(additive) >= 0.15  AND
     order-shuffle drops mech cross_R2 by >= 0.15.
  else NO-TRANSFER.

MECHANISM (multiplicative_film / E5):
   gamma(a) = Ga@a ; beta(a) = Ba@a ; filler_enc(b) = Fb@b
   r = gamma(a) * filler_enc(b) + beta(a)      # role a modulates filler b
$0 numpy only. No torch / no 303M.
"""
import json, os, numpy as np

D = 32
M = 32          # target dim
H = 32          # rep dim
N_TRAIN = 3000
N_TEST = 3000
EPOCHS = 2000
LR = 3e-3

# ---- fixed concept vectors + disjoint split ----------------------------------
vec = np.random.RandomState(0).randn(256, D)
TRAIN_IDX = np.arange(0, 192)
TEST_IDX = np.arange(192, 256)

# ---- fixed non-commutative target ------------------------------------------
rs1 = np.random.RandomState(1)
Wr = rs1.randn(M, D) / np.sqrt(D)
Wf = rs1.randn(M, D) / np.sqrt(D)
ROLL = int(rs1.randint(1, D))       # nonzero shift -> multiplicative term non-commutative

def target(a, b):
    br = np.roll(b, ROLL, axis=1)
    return np.tanh(a @ Wr.T + b @ Wf.T + a * br)

# ---- sample ordered pairs (a != b) within a concept pool -------------------
def sample_pairs(pool, n, seed):
    rs = np.random.RandomState(seed)
    A = rs.choice(pool, size=n)
    B = rs.choice(pool, size=n)
    bad = A == B
    while bad.any():
        B[bad] = rs.choice(pool, size=int(bad.sum()))
        bad = A == B
    return A, B

trA_i, trB_i = sample_pairs(TRAIN_IDX, N_TRAIN, seed=2)
teA_i, teB_i = sample_pairs(TEST_IDX, N_TEST, seed=2)

Atr, Btr = vec[trA_i], vec[trB_i]
Ate, Bte = vec[teA_i], vec[teB_i]
Ttr = target(Atr, Btr)
Tte = target(Ate, Bte)

def r2(pred, true):
    ss_res = np.sum((pred - true) ** 2)
    ss_tot = np.sum((true - true.mean(0)) ** 2)
    return 1.0 - ss_res / ss_tot

# ---- generic Adam over a param dict ----------------------------------------
class Adam:
    def __init__(self, params, lr):
        self.lr = lr
        self.m = {k: np.zeros_like(v) for k, v in params.items()}
        self.v = {k: np.zeros_like(v) for k, v in params.items()}
        self.t = 0
    def step(self, params, grads, b1=0.9, b2=0.999, eps=1e-8):
        self.t += 1
        for k in params:
            self.m[k] = b1 * self.m[k] + (1 - b1) * grads[k]
            self.v[k] = b2 * self.v[k] + (1 - b2) * grads[k] ** 2
            mh = self.m[k] / (1 - b1 ** self.t)
            vh = self.v[k] / (1 - b2 ** self.t)
            params[k] -= self.lr * mh / (np.sqrt(vh) + eps)

# ============================================================================
# MECHANISM: multiplicative FiLM
# ============================================================================
def film_init(seed=7):
    rs = np.random.RandomState(seed)
    s = 1.0 / np.sqrt(D)
    return {
        "Ga": rs.randn(H, D) * s,   # gamma(a)
        "Fb": rs.randn(H, D) * s,   # filler_enc(b)
        "Ba": rs.randn(H, D) * s,   # beta(a)
        "Wh": rs.randn(M, H) * (1.0 / np.sqrt(H)),
        "bh": np.zeros(M),
    }

def film_forward(p, A, B):
    ga = A @ p["Ga"].T
    fb = B @ p["Fb"].T
    ba = A @ p["Ba"].T
    r = ga * fb + ba
    pred = r @ p["Wh"].T + p["bh"]
    cache = (A, B, ga, fb, ba, r)
    return pred, cache

def film_backward(p, cache, dpred):
    A, B, ga, fb, ba, r = cache
    g = {}
    g["Wh"] = dpred.T @ r
    g["bh"] = dpred.sum(0)
    dr = dpred @ p["Wh"]
    dga = dr * fb
    dfb = dr * ga
    dba = dr
    g["Ga"] = dga.T @ A
    g["Fb"] = dfb.T @ B
    g["Ba"] = dba.T @ A
    return g

# ============================================================================
# CONTROL: additive baseline
# ============================================================================
def add_init(seed=7):
    rs = np.random.RandomState(seed)
    s = 1.0 / np.sqrt(D)
    return {
        "Wa": rs.randn(H, D) * s,
        "Wb": rs.randn(H, D) * s,
        "Wh": rs.randn(M, H) * (1.0 / np.sqrt(H)),
        "bh": np.zeros(M),
    }

def add_forward(p, A, B):
    ga = A @ p["Wa"].T
    gb = B @ p["Wb"].T
    r = ga + gb
    pred = r @ p["Wh"].T + p["bh"]
    return pred, (A, B, r)

def add_backward(p, cache, dpred):
    A, B, r = cache
    g = {}
    g["Wh"] = dpred.T @ r
    g["bh"] = dpred.sum(0)
    dr = dpred @ p["Wh"]
    g["Wa"] = dr.T @ A
    g["Wb"] = dr.T @ B
    return g

# ---- training loop ----------------------------------------------------------
def train(init_fn, fwd, bwd, name):
    p = init_fn()
    opt = Adam(p, LR)
    scale = 1.0 / (Atr.shape[0] * M)
    for ep in range(EPOCHS):
        pred, cache = fwd(p, Atr, Btr)
        dpred = 2.0 * (pred - Ttr) * scale
        g = bwd(p, cache, dpred)
        opt.step(p, g)
    tr_pred, _ = fwd(p, Atr, Btr)
    te_pred, _ = fwd(p, Ate, Bte)
    tr_r2 = r2(tr_pred, Ttr)
    te_r2 = r2(te_pred, Tte)
    print(f"[{name}] train R2={tr_r2:.4f}  cross(test) R2={te_r2:.4f}")
    return p, te_r2

film_p, film_cross = train(film_init, film_forward, film_backward, "FiLM")
add_p, add_cross = train(add_init, add_forward, add_backward, "ADDITIVE")

# ---- ORDER-SHUFFLE control (FiLM) ------------------------------------------
rs_sh = np.random.RandomState(3)
swap = rs_sh.rand(N_TEST) < 0.5
As = Ate.copy(); Bs = Bte.copy()
As[swap], Bs[swap] = Bte[swap], Ate[swap]
sh_pred, _ = film_forward(film_p, As, Bs)
film_shuffle = r2(sh_pred, Tte)
print(f"[FiLM order-shuffle] cross R2={film_shuffle:.4f}")

# ---- verdict ----------------------------------------------------------------
gap = film_cross - add_cross
drop = film_cross - film_shuffle
transfer_earning = (gap >= 0.15) and (drop >= 0.15)
verdict = "TRANSFER-EARNING" if transfer_earning else "NO-TRANSFER"
print(f"\ngap(mech-additive)={gap:.4f}  shuffle_drop={drop:.4f}  -> {verdict}")

result = {
    "mechanism": "multiplicative_film",
    "spec": "r = gamma(a) * filler_enc(b) + beta(a)  (FiLM role modulation, E5)",
    "task": {
        "K": 256, "d": D, "target_dim": M, "rep_dim": H,
        "train_concepts": [0, 191], "test_concepts": [192, 255],
        "n_train_pairs": N_TRAIN, "n_test_pairs": N_TEST,
        "roll": ROLL, "epochs": EPOCHS, "lr": LR, "optimizer": "adam-numpy",
        "seeds": {"vec": 0, "target": 1, "pairs": 2, "shuffle": 3, "init": 7},
    },
    "cross_r2": float(film_cross),
    "additive_r2": float(add_cross),
    "shuffle_r2": float(film_shuffle),
    "gap_mech_minus_additive": float(gap),
    "shuffle_drop": float(drop),
    "thresholds": {"gap": 0.15, "shuffle_drop": 0.15},
    "verdict": verdict,
}
OUT = os.environ.get("OUTDIR", ".")
with open(os.path.join(OUT, "RESULT.json"), "w") as f:
    json.dump(result, f, indent=2)
print("wrote RESULT.json to", OUT)
