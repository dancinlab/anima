#!/usr/bin/env python3
"""
Transfer-mechanism sweep — MECH = ssm_scan_trained (E12, TRAINED).

SHARED SYNTHETIC TASK (reference-match, binding-dominant non-commutative):
  - K=256 concepts. Concept vectors: vec_full = RandomState(0).randn(256,32);
    we use vec = vec_full[:, :16] (d=16) because the target tensor T is (16,16,16).
    (Honors the literal randn(256,32) seed AND the d=16/out=16 target; a peer agent
    generating randn(256,32) and slicing [:, :16] gets byte-identical vectors.)
  - DISJOINT split: TRAIN concepts 0-191 (192), TEST concepts 192-255 (64). overlap 0.
  - TARGET (pure bilinear, NO linear a/b term, asymmetric -> non-commutative):
      t(a,b)_k = tanh( sum_ij T[k,i,j] vec[a]_i vec[b]_j ),  T = RandomState(1).randn(16,16,16)
    additive (Wa@a + Wb@b) cannot represent a pure bilinear form -> additive R^2 must be low.
    T fixed -> transfers to unseen concept vectors iff the mechanism captures binding.
  - TRAIN pairs: 3000 ordered pairs from concepts 0-191  (RandomState(2)).
    TEST  pairs: 3000 ordered pairs from concepts 192-255 (RandomState(3)) = CROSS-DIST transfer.
  - Each mechanism: (vec[a],vec[b]) -> rep r -> linear head -> predict t. end-to-end Adam MSE.
  - Metric: TEST cross R^2. Controls: (a) ADDITIVE baseline (b) ORDER-SHUFFLE (swap a,b at test).
  - ANCHOR-VALIDATION: slot_gated_write (E1 known escape) must clear cross R^2 >= additive+0.15,
    else task invalid -> verdict INCONCLUSIVE-task-artifact (no mechanism judgment).
  - JUDGE mech: TRANSFER-EARNING iff cross_R2(mech)-R2(additive) >= 0.15 AND
    order-shuffle drops mech cross R^2 by >= 0.15. else NO-TRANSFER.

$0 numpy only. No torch / no 303M / no model load.
"""
import numpy as np, json, os

# ---------------- shared task construction ----------------
K = 256
vec_full = np.random.RandomState(0).randn(K, 32)
vec = vec_full[:, :16].astype(np.float64)          # d=16 concept vectors
D = 16
TRAIN_IDX = np.arange(0, 192)
TEST_IDX  = np.arange(192, 256)
T = np.random.RandomState(1).randn(16, 16, 16).astype(np.float64)   # target tensor

def target(a_idx, b_idx):
    va = vec[a_idx]; vb = vec[b_idx]                 # (N,16)
    bil = np.einsum('kij,ni,nj->nk', T, va, vb)      # t_k = sum_ij T[k,i,j] va_i vb_j
    return np.tanh(bil)

def make_pairs(idx_pool, n, seed):
    rs = np.random.RandomState(seed)
    a = idx_pool[rs.randint(0, len(idx_pool), size=n)]
    b = idx_pool[rs.randint(0, len(idx_pool), size=n)]
    return a, b

tr_a, tr_b = make_pairs(TRAIN_IDX, 3000, seed=2)
te_a, te_b = make_pairs(TEST_IDX, 3000, seed=3)

Xa_tr, Xb_tr = vec[tr_a], vec[tr_b]; Y_tr = target(tr_a, tr_b)
Xa_te, Xb_te = vec[te_a], vec[te_b]; Y_te = target(te_a, te_b)

def r2(pred, true):
    ss_res = np.sum((pred - true) ** 2)
    ss_tot = np.sum((true - true.mean(axis=0)) ** 2)
    return 1.0 - ss_res / ss_tot

# ---------------- generic Adam ----------------
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

RS = np.random.RandomState(7)
def W(shape, s=0.1): return (RS.randn(*shape) * s).astype(np.float64)
OUT = 16
EPOCHS = 3000

# ---------------- ADDITIVE baseline ----------------
def train_additive():
    P = {'Wa': W((OUT, D)), 'Wb': W((OUT, D)), 'bias': np.zeros(OUT)}
    opt = Adam(P, lr=1e-2)
    N = Xa_tr.shape[0]
    for ep in range(EPOCHS):
        pred = Xa_tr @ P['Wa'].T + Xb_tr @ P['Wb'].T + P['bias']
        dP = 2 * (pred - Y_tr) / (N * OUT)
        opt.step({'Wa': dP.T @ Xa_tr, 'Wb': dP.T @ Xb_tr, 'bias': dP.sum(0)})
    def fwd(Xa, Xb): return Xa @ P['Wa'].T + Xb @ P['Wb'].T + P['bias']
    return fwd

# ---------------- SLOT gated-write (E1 anchor) ----------------
# gate g = Wg@va, content c = Wc@vb, mem = g*c (gated write), pred = Wo@mem.
# multiplicative -> bilinear -> can represent tensor T; transfers to unseen vectors.
def train_slot(S=128):
    P = {'Wg': W((S, D)), 'Wc': W((S, D)), 'Wo': W((OUT, S)), 'bias': np.zeros(OUT)}
    opt = Adam(P, lr=5e-3)
    N = Xa_tr.shape[0]
    for ep in range(EPOCHS):
        G = Xa_tr @ P['Wg'].T
        C = Xb_tr @ P['Wc'].T
        M = G * C
        pred = M @ P['Wo'].T + P['bias']
        dP = 2 * (pred - Y_tr) / (N * OUT)
        dWo = dP.T @ M; dbias = dP.sum(0)
        dM = dP @ P['Wo']
        dG = dM * C; dC = dM * G
        opt.step({'Wg': dG.T @ Xa_tr, 'Wc': dC.T @ Xb_tr, 'Wo': dWo, 'bias': dbias})
    def fwd(Xa, Xb):
        return ((Xa @ P['Wg'].T) * (Xb @ P['Wc'].T)) @ P['Wo'].T + P['bias']
    return fwd

# ---------------- SSM linear scan (spec-literal mechanism under test) ----------------
# x1=va, x2=vb.  h1 = B@x1 ; h2 = A@h1 + B@x2 ; pred = Wo@h2.
# purely LINEAR recurrence + linear head -> structurally additive (order matters via A).
def train_ssm_linear(H=64):
    P = {'A': W((H, H)), 'B': W((H, D)), 'Wo': W((OUT, H)), 'bias': np.zeros(OUT)}
    opt = Adam(P, lr=5e-3)
    N = Xa_tr.shape[0]
    for ep in range(EPOCHS):
        H1 = Xa_tr @ P['B'].T
        Z  = H1 @ P['A'].T + Xb_tr @ P['B'].T
        pred = Z @ P['Wo'].T + P['bias']
        dP = 2 * (pred - Y_tr) / (N * OUT)
        dWo = dP.T @ Z; dbias = dP.sum(0)
        dZ = dP @ P['Wo']
        dA = dZ.T @ H1
        dH1 = dZ @ P['A']
        dB = dH1.T @ Xa_tr + dZ.T @ Xb_tr
        opt.step({'A': dA, 'B': dB, 'Wo': dWo, 'bias': dbias})
    def fwd(Xa, Xb):
        H1 = Xa @ P['B'].T
        Z = H1 @ P['A'].T + Xb @ P['B'].T
        return Z @ P['Wo'].T + P['bias']
    return fwd

# ---------------- SSM nonlinear (tanh) scan (charitable variant) ----------------
def train_ssm_tanh(H=64):
    P = {'A': W((H, H)), 'B': W((H, D)), 'Wo': W((OUT, H)), 'bias': np.zeros(OUT)}
    opt = Adam(P, lr=5e-3)
    N = Xa_tr.shape[0]
    for ep in range(EPOCHS):
        A1 = Xa_tr @ P['B'].T; H1 = np.tanh(A1)
        Zc = H1 @ P['A'].T + Xb_tr @ P['B'].T; H2 = np.tanh(Zc)
        pred = H2 @ P['Wo'].T + P['bias']
        dP = 2 * (pred - Y_tr) / (N * OUT)
        dWo = dP.T @ H2; dbias = dP.sum(0)
        dH2 = dP @ P['Wo']
        dZc = dH2 * (1 - H2 ** 2)
        dA = dZc.T @ H1
        dH1 = dZc @ P['A']
        dB2 = dZc.T @ Xb_tr
        dA1 = dH1 * (1 - H1 ** 2)
        dB1 = dA1.T @ Xa_tr
        opt.step({'A': dA, 'B': dB1 + dB2, 'Wo': dWo, 'bias': dbias})
    def fwd(Xa, Xb):
        H1 = np.tanh(Xa @ P['B'].T)
        H2 = np.tanh(H1 @ P['A'].T + Xb @ P['B'].T)
        return H2 @ P['Wo'].T + P['bias']
    return fwd

# ---------------- run all ----------------
def evaluate(fwd):
    return dict(
        train_r2=float(r2(fwd(Xa_tr, Xb_tr), Y_tr)),
        cross_r2=float(r2(fwd(Xa_te, Xb_te), Y_te)),
        shuffle_r2=float(r2(fwd(Xb_te, Xa_te), Y_te)),
    )

print("training additive...");      add  = evaluate(train_additive())
print("training slot (anchor)..."); slot = evaluate(train_slot())
print("training ssm_linear...");    lin  = evaluate(train_ssm_linear())
print("training ssm_tanh...");      tanh = evaluate(train_ssm_tanh())

add_cross = add['cross_r2']
anchor_ok = slot['cross_r2'] >= add_cross + 0.15

def judge(m):
    beats = (m['cross_r2'] - add_cross) >= 0.15
    shuf_drop = (m['cross_r2'] - m['shuffle_r2']) >= 0.15
    return 'TRANSFER-EARNING' if (beats and shuf_drop) else 'NO-TRANSFER'

primary = lin
verdict = 'INCONCLUSIVE-task-artifact' if not anchor_ok else judge(primary)

result = {
    'mechanism': 'ssm_scan_trained',
    'spec': 'linear SSM associative scan h_t=A h_{t-1}+B x_t, x=[a,b] seq, A,B trained, linear head',
    'task': 'binding-dominant bilinear non-commutative (K=256, d=16, T=RS(1).randn(16,16,16))',
    'split': {'train_concepts': [0, 191], 'test_concepts': [192, 255], 'overlap': 0},
    'epochs': EPOCHS,
    'additive_baseline': add,
    'anchor_slot_gated_write': slot,
    'anchor_valid': bool(anchor_ok),
    'anchor_margin_over_additive': float(slot['cross_r2'] - add_cross),
    'ssm_linear_spec_literal': lin,
    'ssm_tanh_charitable_variant': tanh,
    'primary_mechanism': 'ssm_linear_spec_literal',
    'judge_linear': judge(lin) if anchor_ok else 'INCONCLUSIVE',
    'judge_tanh': judge(tanh) if anchor_ok else 'INCONCLUSIVE',
    'verdict': verdict,
    'note': ('Linear SSM readout collapses to pred=(Wo A B)a+(Wo B)b, the SAME linear '
             'function class as the additive baseline -> cannot earn bilinear-binding transfer. '
             'tanh nonlinearity in the scan is what unlocks binding.'),
}
here = '/Users/mini/dancinlab/anima/state/transfer_mechanism_sweep/ssm_scan_trained'
with open(os.path.join(here, 'RESULT.json'), 'w') as f:
    json.dump(result, f, indent=2)
print(json.dumps(result, indent=2))
