"""
Transfer-mechanism sweep — MECHANISM = multiplicative_film (E5).

SHARED SYNTHETIC TASK (reference-match, binding-dominant non-commutative bilinear):
  - K=256 concepts, vec = RandomState(0).randn(256,32).  DISJOINT split:
      TRAIN concepts 0-191, TEST concepts 192-255 (overlap 0).
  - TARGET t(a,b) = tanh(einsum("kij,i,j->k", T, va, vb)), pure bilinear form,
      T = RandomState(1).randn(16,16,16), operating on the first 16 dims of each
      concept vector (T is 16x16x16, d=out=16). No linear a/b term -> additive
      (Wa@a+Wb@b) is structurally unable to represent it. T asymmetric -> t(a,b)!=t(b,a).
  - TRAIN pairs: 3000 ordered pairs among TRAIN concepts (seed 2).
  - TEST  pairs: 3000 ordered pairs among TEST concepts (seed 3) = CROSS-DISTRIBUTION.
  - Each mechanism: (vec[a],vec[b]) -> rep r -> LINEAR head -> predict t(a,b).
    End-to-end Adam MSE on TRAIN, ~4000 steps.
  - Report TEST cross R². Controls: (a) ADDITIVE baseline (same training),
    (b) ORDER-SHUFFLE (swap test a,b -> R² must collapse).
  - ANCHOR: slot_gated_write (E1, known escape) must clear additive+0.15 or task INVALID.

  Verdict TRANSFER-EARNING iff  cross_R2(mech) - R2(additive) >= 0.15
                          AND  order-shuffle drops R² by >= 0.15.

$0 numpy only. Mechanism input = full 32-dim concept vectors (all mechs identical,
fair); target defined on first 16 dims. Manual analytic backprop + Adam.
"""
import numpy as np
import json, os

OUTDIR = "/Users/mini/dancinlab/anima/state/transfer_mechanism_sweep/multiplicative_film"
os.makedirs(OUTDIR, exist_ok=True)

# ---------------- shared task ----------------
K, DIN, DT = 256, 32, 16
vec = np.random.RandomState(0).randn(K, DIN)          # concept table (input to mechs)
T   = np.random.RandomState(1).randn(DT, DT, DT)      # bilinear tensor (kij)

TRAIN_IDX = np.arange(0, 192)
TEST_IDX  = np.arange(192, 256)

def target(a_idx, b_idx):
    va = vec[a_idx][:, :DT]; vb = vec[b_idx][:, :DT]
    z = np.einsum("kij,ni,nj->nk", T, va, vb)         # (N,16)
    return np.tanh(z)

def make_pairs(idx_pool, n, seed):
    rng = np.random.RandomState(seed)
    a = idx_pool[rng.randint(0, len(idx_pool), size=n)]
    b = idx_pool[rng.randint(0, len(idx_pool), size=n)]
    return a, b

trA, trB = make_pairs(TRAIN_IDX, 3000, 2)
teA, teB = make_pairs(TEST_IDX,  3000, 3)

Xa_tr, Xb_tr = vec[trA], vec[trB]; Y_tr = target(trA, trB)
Xa_te, Xb_te = vec[teA], vec[teB]; Y_te = target(teA, teB)

def r2(pred, true):
    ss_res = np.sum((pred - true) ** 2)
    ss_tot = np.sum((true - true.mean(axis=0, keepdims=True)) ** 2)
    return 1.0 - ss_res / ss_tot

# ---------------- Adam optimizer over a param dict ----------------
class Adam:
    def __init__(self, params, lr=1e-2, b1=0.9, b2=0.999, eps=1e-8):
        self.p = params; self.lr = lr; self.b1 = b1; self.b2 = b2; self.eps = eps
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

def fit(init, fwd_back, steps=4000, lr=1e-2):
    params = {k: v.copy() for k, v in init.items()}
    opt = Adam(params, lr=lr)
    last = None
    for s in range(steps):
        loss, grads = fwd_back(params)
        opt.step(grads)
        last = loss
    return params, last

# ================= MECHANISM: multiplicative FiLM (E5) =================
# r = gamma(a) * filler_enc(b) + beta(a)
H_FILM = 64
def film_init(seed=10):
    rng = np.random.RandomState(seed); sc = 0.1
    return {
        "Wg": rng.randn(DIN, H_FILM) * sc, "bg": np.zeros(H_FILM),
        "Wf": rng.randn(DIN, H_FILM) * sc, "bf": np.zeros(H_FILM),
        "Wbeta": rng.randn(DIN, H_FILM) * sc, "bbeta": np.zeros(H_FILM),
        "Wh": rng.randn(H_FILM, DT) * sc, "bh": np.zeros(DT),
    }
def film_forward(p, A, B):
    G = A @ p["Wg"] + p["bg"]
    F = B @ p["Wf"] + p["bf"]
    Bt = A @ p["Wbeta"] + p["bbeta"]
    R = G * F + Bt
    P = R @ p["Wh"] + p["bh"]
    return P, (G, F, Bt, R)
def film_fb(A, B, Y):
    N = A.shape[0]; scale = 1.0 / (N * DT)
    def fb(p):
        P, (G, F, Bt, R) = film_forward(p, A, B)
        diff = P - Y; loss = np.sum(diff * diff) * scale
        dP = 2 * diff * scale
        g = {}
        g["Wh"] = R.T @ dP; g["bh"] = dP.sum(0)
        dR = dP @ p["Wh"].T
        dG = dR * F; dF = dR * G; dBt = dR
        g["Wg"] = A.T @ dG; g["bg"] = dG.sum(0)
        g["Wf"] = B.T @ dF; g["bf"] = dF.sum(0)
        g["Wbeta"] = A.T @ dBt; g["bbeta"] = dBt.sum(0)
        return loss, g
    return fb

# ================= CONTROL: ADDITIVE baseline =================
H_ADD = 64
def add_init(seed=20):
    rng = np.random.RandomState(seed); sc = 0.1
    return {
        "Wa": rng.randn(DIN, H_ADD) * sc, "Wb": rng.randn(DIN, H_ADD) * sc,
        "b0": np.zeros(H_ADD), "Wh": rng.randn(H_ADD, DT) * sc, "bh": np.zeros(DT),
    }
def add_forward(p, A, B):
    R = A @ p["Wa"] + B @ p["Wb"] + p["b0"]
    P = R @ p["Wh"] + p["bh"]
    return P, R
def add_fb(A, B, Y):
    N = A.shape[0]; scale = 1.0 / (N * DT)
    def fb(p):
        P, R = add_forward(p, A, B)
        diff = P - Y; loss = np.sum(diff * diff) * scale
        dP = 2 * diff * scale
        g = {}
        g["Wh"] = R.T @ dP; g["bh"] = dP.sum(0)
        dR = dP @ p["Wh"].T
        g["Wa"] = A.T @ dR; g["Wb"] = B.T @ dR; g["b0"] = dR.sum(0)
        return loss, g
    return fb

# ================= ANCHOR: slot_gated_write (E1, known escape) =================
S_SLOT, V_SLOT = 16, 16
def slot_init(seed=30):
    rng = np.random.RandomState(seed); sc = 0.1
    return {
        "Wa": rng.randn(DIN, S_SLOT) * sc,          # address from role a
        "Wv": rng.randn(DIN, V_SLOT) * sc,          # value from filler b
        "Wh": rng.randn(S_SLOT * V_SLOT, DT) * sc, "bh": np.zeros(DT),
    }
def softmax(x):
    x = x - x.max(axis=1, keepdims=True); e = np.exp(x)
    return e / e.sum(axis=1, keepdims=True)
def slot_forward(p, A, B):
    logits = A @ p["Wa"]; addr = softmax(logits)     # (N,S)
    val = B @ p["Wv"]                                 # (N,V)
    R3 = addr[:, :, None] * val[:, None, :]           # (N,S,V) gated write
    R = R3.reshape(A.shape[0], -1)
    P = R @ p["Wh"] + p["bh"]
    return P, (addr, val, R)
def slot_fb(A, B, Y):
    N = A.shape[0]; scale = 1.0 / (N * DT)
    def fb(p):
        P, (addr, val, R) = slot_forward(p, A, B)
        diff = P - Y; loss = np.sum(diff * diff) * scale
        dP = 2 * diff * scale
        g = {}
        g["Wh"] = R.T @ dP; g["bh"] = dP.sum(0)
        dR = (dP @ p["Wh"].T).reshape(N, S_SLOT, V_SLOT)
        daddr = np.einsum("nsv,nv->ns", dR, val)
        dval = np.einsum("nsv,ns->nv", dR, addr)
        dlog = addr * (daddr - (daddr * addr).sum(axis=1, keepdims=True))
        g["Wa"] = A.T @ dlog; g["Wv"] = B.T @ dval
        return loss, g
    return fb

# ---------------- run all three ----------------
def evaluate(name, init_fn, fb_fn, fwd_fn, steps=4000, lr=1e-2):
    p, loss = fit(init_fn(), fb_fn(Xa_tr, Xb_tr, Y_tr), steps=steps, lr=lr)
    Ptr, _ = fwd_fn(p, Xa_tr, Xb_tr); tr = r2(Ptr, Y_tr)
    Pte, _ = fwd_fn(p, Xa_te, Xb_te); te = r2(Pte, Y_te)
    Psh, _ = fwd_fn(p, Xb_te, Xa_te); sh = r2(Psh, Y_te)   # order-shuffle
    print(f"{name:16s} train_loss={loss:.4f} train_R2={tr:.4f} "
          f"cross_R2={te:.4f} shuffle_R2={sh:.4f}")
    return {"train_loss": float(loss), "train_r2": float(tr),
            "cross_r2": float(te), "shuffle_r2": float(sh)}

print("=== transfer-mechanism sweep : multiplicative_film ===")
res_film = evaluate("film(mech)", film_init, film_fb, film_forward)
res_add  = evaluate("additive",   add_init,  add_fb,  add_forward)
res_slot = evaluate("slot(anchor)", slot_init, slot_fb, slot_forward)

# ---------------- verdict ----------------
mech_cross, add_cross = res_film["cross_r2"], res_add["cross_r2"]
mech_shuf = res_film["shuffle_r2"]
anchor_cross = res_slot["cross_r2"]

anchor_ok = (anchor_cross - add_cross) >= 0.15
delta_add = mech_cross - add_cross
shuffle_drop = mech_cross - mech_shuf

if not anchor_ok:
    verdict = "INCONCLUSIVE-task-artifact"
elif delta_add >= 0.15 and shuffle_drop >= 0.15:
    verdict = "TRANSFER-EARNING"
else:
    verdict = "NO-TRANSFER"

out = {
    "mechanism": "multiplicative_film",
    "spec": "r = gamma(a)*filler_enc(b) + beta(a) ; FiLM role->modulate filler",
    "task": "binding-dominant non-commutative bilinear tanh(einsum kij,i,j->k), "
            "concepts 0-191 train / 192-255 test cross-distribution",
    "film": res_film, "additive": res_add, "slot_anchor": res_slot,
    "anchor_validation": {
        "anchor_cross_r2": anchor_cross, "additive_cross_r2": add_cross,
        "anchor_minus_additive": float(anchor_cross - add_cross),
        "bar": 0.15, "anchor_ok": bool(anchor_ok),
    },
    "verdict_math": {
        "cross_r2_mech": mech_cross, "cross_r2_additive": add_cross,
        "delta_vs_additive": float(delta_add),
        "shuffle_r2": mech_shuf, "shuffle_drop": float(shuffle_drop),
        "bar": 0.15,
    },
    "verdict": verdict,
}
with open(os.path.join(OUTDIR, "RESULT.json"), "w") as f:
    json.dump(out, f, indent=2)
# preserve reproduce script alongside result
import shutil
shutil.copy(os.path.abspath(__file__), os.path.join(OUTDIR, "run.py"))
print("\nVERDICT:", verdict)
print(json.dumps(out["verdict_math"], indent=2))
print("anchor_ok:", anchor_ok, "anchor-additive=%.4f" % (anchor_cross - add_cross))
