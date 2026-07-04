#!/usr/bin/env python3
"""
STEP-0 DIRECTIONAL toy for trunk-objective candidate (3):
  mitosis structural curriculum (p8) -- growth <-> gradient develops composition.

CANDIDATE CLAIM: on a systematic-generalization split (train = primitives + some
combos, test = NOVEL combos), *weight-level* gradient training with *mitosis growth*
(Net2WiderNet = literal neuron division = p8 mitosis) + a staged curriculum carves
held-out recombination into the WEIGHTS -> reach(held-out) >> additive floor.

TASK (non-commutative -> DPI-escapable): permutation composition.
  input  = (f, g, x),  output = f(g(x)) = perm_f[perm_g[x]]   over S_K (non-abelian).
  A bag/additive readout CANNOT represent order (f o g != g o f) -> additive floor
  is bounded; if a model beats it on HELD-OUT combos it earned order-sensitive
  recombination (DPI escape). SHUFFLE control (swap f<->g at eval) must DROP acc.

SPLIT (memorization-free, by-construction guard):
  - singletons: (id,g,*) and (f,id,*) for every primitive -> teaches each action.
  - pairs (both non-id): hold out a fixed fraction as TEST. Every primitive appears
    in >=1 TRAIN pair (so no primitive is unseen-in-composition). TEST triples
    (f,g,x) NEVER appear in TRAIN -> reach cannot be leakage.

CONDITIONS
  A. additive-floor : logits = b + Wf[f] + Wg[g] + Wx[x]  (no interaction, trained)
  B. baseline       : fixed-width MLP, all curriculum at once
  C. (3) growth+curr: mitosis-grow width 16->32->64 (fn-preserving) + staged curr
  D. abl growth-OFF : fixed width 64 + staged curriculum   (isolates growth)
  E. abl curr-SHUF  : mitosis-grow but curriculum stages shuffled to a single flat mix
Metrics per condition: train_acc, heldout_reach_acc, shuffle_eval_acc, and the
earned-vs-additive gap.  chance = 1/K.
"""
import numpy as np

SEED = 0
K = 6          # permuted-set size; S_6 non-abelian -> order matters
N_PRIM = 8     # index 0 = identity, 1..7 = real primitives
IN = N_PRIM + N_PRIM + K
rng = np.random.default_rng(SEED)

# ---- primitives: identity + random permutations of {0..K-1} ----
perms = [np.arange(K)]  # identity
for _ in range(N_PRIM - 1):
    perms.append(rng.permutation(K))
perms = np.stack(perms)  # (N_PRIM, K)

def compose_out(f, g, x):
    return perms[f][perms[g][x]]  # f(g(x))

# ---- build datasets ----
def onehot(i, n):
    v = np.zeros(n); v[i] = 1.0; return v

def make_example(f, g, x):
    return np.concatenate([onehot(f, N_PRIM), onehot(g, N_PRIM), onehot(x, K)]), compose_out(f, g, x)

# singletons: one arg is identity (index 0)
singles = []
for g in range(1, N_PRIM):
    for x in range(K):
        singles.append((0, g, x))
for f in range(1, N_PRIM):
    for x in range(K):
        singles.append((f, 0, x))
for x in range(K):
    singles.append((0, 0, x))

# all non-identity pairs
all_pairs = [(f, g) for f in range(1, N_PRIM) for g in range(1, N_PRIM)]
rng.shuffle(all_pairs)
n_test_pairs = int(round(0.30 * len(all_pairs)))
test_pairs = set(all_pairs[:n_test_pairs])
train_pairs = [p for p in all_pairs if p not in test_pairs]

# guard: every primitive must appear in >=1 train pair (both slots)
def slot_cover(pairs):
    fs = set(f for f, g in pairs); gs = set(g for f, g in pairs)
    return fs, gs
fs, gs = slot_cover(train_pairs)
assert fs == set(range(1, N_PRIM)) and gs == set(range(1, N_PRIM)), "primitive uncovered in train pairs"

def expand(pairs):
    out = []
    for (f, g) in pairs:
        for x in range(K):
            out.append((f, g, x))
    return out

train_pair_triples = expand(train_pairs)
test_triples = expand(list(test_pairs))

# by-construction leakage guard: no test triple in train
train_all_triples = set(singles) | set(train_pair_triples)
assert not (set(test_triples) & train_all_triples), "LEAKAGE: test triple in train"

def to_matrix(triples):
    X = np.stack([make_example(*t)[0] for t in triples])
    Y = np.array([make_example(*t)[1] for t in triples])
    return X, Y

Xs, Ys = to_matrix(singles)
Xtp, Ytp = to_matrix(train_pair_triples)
Xte, Yte = to_matrix(test_triples)

# split train pairs into two curriculum halves (for staged growth)
half = len(train_pairs) // 2
tp_early = expand(train_pairs[:half])
tp_late = expand(train_pairs[half:])
Xtpe, Ytpe = to_matrix(tp_early)
Xtpl, Ytpl = to_matrix(tp_late)

# full train (singles + all train pairs)
Xtr = np.concatenate([Xs, Xtp]); Ytr = np.concatenate([Ys, Ytp])

print(f"K={K} N_PRIM={N_PRIM} | singles={len(singles)} train_pair_triples={len(train_pair_triples)} "
      f"test_triples={len(test_triples)} | test_pairs={len(test_pairs)}/{len(all_pairs)}")

# ---------------- Adam MLP (1 hidden, ReLU) ----------------
def init_mlp(H, seed):
    r = np.random.default_rng(seed)
    W1 = r.normal(0, np.sqrt(2.0 / IN), (IN, H))
    b1 = np.zeros(H)
    W2 = r.normal(0, np.sqrt(2.0 / H), (H, K))
    b2 = np.zeros(K)
    return dict(W1=W1, b1=b1, W2=W2, b2=b2)

def forward(p, X):
    z1 = X @ p['W1'] + p['b1']
    a1 = np.maximum(z1, 0)
    z2 = a1 @ p['W2'] + p['b2']
    return z1, a1, z2

def softmax_ce(z2, Y):
    z = z2 - z2.max(1, keepdims=True)
    e = np.exp(z); sm = e / e.sum(1, keepdims=True)
    n = len(Y)
    loss = -np.log(sm[np.arange(n), Y] + 1e-12).mean()
    dz2 = sm.copy(); dz2[np.arange(n), Y] -= 1; dz2 /= n
    return loss, dz2, sm

class Adam:
    def __init__(self, params, lr=3e-3):
        self.lr = lr; self.m = {k: np.zeros_like(v) for k, v in params.items()}
        self.v = {k: np.zeros_like(v) for k, v in params.items()}; self.t = 0
    def step(self, params, grads):
        self.t += 1; b1, b2, eps = 0.9, 0.999, 1e-8
        for k in params:
            self.m[k] = b1 * self.m[k] + (1 - b1) * grads[k]
            self.v[k] = b2 * self.v[k] + (1 - b2) * grads[k] ** 2
            mh = self.m[k] / (1 - b1 ** self.t); vh = self.v[k] / (1 - b2 ** self.t)
            params[k] -= self.lr * mh / (np.sqrt(vh) + eps)

def train_steps(p, opt, X, Y, steps, bs=64, seed=1):
    r = np.random.default_rng(seed); n = len(Y)
    for s in range(steps):
        idx = r.integers(0, n, size=min(bs, n))
        xb, yb = X[idx], Y[idx]
        z1, a1, z2 = forward(p, xb)
        loss, dz2, _ = softmax_ce(z2, yb)
        dW2 = a1.T @ dz2; db2 = dz2.sum(0)
        da1 = dz2 @ p['W2'].T; dz1 = da1 * (z1 > 0)
        dW1 = xb.T @ dz1; db1 = dz1.sum(0)
        opt.step(p, dict(W1=dW1, b1=db1, W2=dW2, b2=db2))
    return p

def net2wider(p, newH, seed):
    """Function-preserving neuron division (Net2WiderNet = literal mitosis)."""
    r = np.random.default_rng(seed)
    H = p['W1'].shape[1]
    if newH <= H:
        return p
    # choose which existing units to clone (with replacement)
    clone_src = r.integers(0, H, size=newH - H)
    mapping = np.concatenate([np.arange(H), clone_src])  # newH -> src unit
    # count replications per src unit for outgoing split
    counts = np.bincount(mapping, minlength=H)
    W1n = p['W1'][:, mapping].copy()
    b1n = p['b1'][mapping].copy()
    # outgoing weights divided by replication count of the source unit -> fn preserved
    scale = 1.0 / counts[mapping]
    W2n = (p['W2'][mapping, :] * scale[:, None]).copy()
    return dict(W1=W1n, b1=b1n, W2=W2n, b2=p['b2'].copy())

def acc(p, X, Y):
    _, _, z2 = forward(p, X)
    return (z2.argmax(1) == Y).mean()

def acc_shuffle(p, triples, Y):
    """Swap f<->g at eval; if acc ~ unchanged the model is order-INERT (bag)."""
    swp = [(g, f, x) for (f, g, x) in triples]
    Xsw = np.stack([make_example(*t)[0] for t in swp])
    _, _, z2 = forward(p, Xsw)
    return (z2.argmax(1) == Y).mean()  # Y is still f(g(x)); order-sensitive model should DROP

# ---------------- additive floor (linear, no interaction) ----------------
def additive_floor(steps=4000):
    r = np.random.default_rng(SEED + 5)
    Wf = np.zeros((N_PRIM, K)); Wg = np.zeros((N_PRIM, K)); Wx = np.zeros((K, K)); b = np.zeros(K)
    params = dict(Wf=Wf, Wg=Wg, Wx=Wx, b=b)
    opt = Adam(params, lr=5e-3)
    def logits(P, F, G, Xi):
        return P['Wf'][F] + P['Wg'][G] + P['Wx'][Xi] + P['b']
    F = np.array([t[0] for t in singles + train_pair_triples])
    G = np.array([t[1] for t in singles + train_pair_triples])
    Xi = np.array([t[2] for t in singles + train_pair_triples])
    Yl = Ytr
    n = len(Yl)
    for s in range(steps):
        idx = r.integers(0, n, size=64)
        f, g, xi, y = F[idx], G[idx], Xi[idx], Yl[idx]
        z = logits(params, f, g, xi)
        z = z - z.max(1, keepdims=True); e = np.exp(z); sm = e / e.sum(1, keepdims=True)
        dz = sm.copy(); dz[np.arange(len(y)), y] -= 1; dz /= len(y)
        gWf = np.zeros_like(Wf); gWg = np.zeros_like(Wg); gWx = np.zeros_like(Wx)
        np.add.at(gWf, f, dz); np.add.at(gWg, g, dz); np.add.at(gWx, xi, dz)
        grads = dict(Wf=gWf, Wg=gWg, Wx=gWx, b=dz.sum(0))
        opt.step(params, grads)
    def a(triples, Y):
        F = np.array([t[0] for t in triples]); G = np.array([t[1] for t in triples]); Xi = np.array([t[2] for t in triples])
        z = logits(params, F, G, Xi)
        return (z.argmax(1) == Y).mean()
    return a(singles + train_pair_triples, Ytr), a(test_triples, Yte)

# ---------------- run conditions ----------------
STEPS = 9000
results = {}

# A. additive floor
add_tr, add_te = additive_floor()
results['A_additive_floor'] = dict(train=add_tr, heldout=add_te, shuffle=None)

# B. baseline fixed-width MLP, all-at-once
p = init_mlp(64, SEED + 10); opt = Adam(p, lr=3e-3)
train_steps(p, opt, Xtr, Ytr, STEPS, seed=SEED + 11)
results['B_baseline_fixed'] = dict(train=acc(p, Xtr, Ytr), heldout=acc(p, Xte, Yte),
                                   shuffle=acc_shuffle(p, test_triples, Yte))

# C. (3) mitosis growth + staged curriculum
p = init_mlp(16, SEED + 20); opt = Adam(p, lr=3e-3)
# stage 1: singletons only (learn each primitive's action)
train_steps(p, opt, Xs, Ys, STEPS // 3, seed=SEED + 21)
# mitosis: 16 -> 32, then singles + early train pairs
p = net2wider(p, 32, SEED + 22); opt = Adam(p, lr=3e-3)
Xce = np.concatenate([Xs, Xtpe]); Yce = np.concatenate([Ys, Ytpe])
train_steps(p, opt, Xce, Yce, STEPS // 3, seed=SEED + 23)
# mitosis: 32 -> 64, then all train data
p = net2wider(p, 64, SEED + 24); opt = Adam(p, lr=3e-3)
train_steps(p, opt, Xtr, Ytr, STEPS // 3, seed=SEED + 25)
results['C_growth_curriculum'] = dict(train=acc(p, Xtr, Ytr), heldout=acc(p, Xte, Yte),
                                      shuffle=acc_shuffle(p, test_triples, Yte))

# D. ablation growth-OFF + staged curriculum (fixed width 64)
p = init_mlp(64, SEED + 30); opt = Adam(p, lr=3e-3)
train_steps(p, opt, Xs, Ys, STEPS // 3, seed=SEED + 31)
opt = Adam(p, lr=3e-3); Xce = np.concatenate([Xs, Xtpe]); Yce = np.concatenate([Ys, Ytpe])
train_steps(p, opt, Xce, Yce, STEPS // 3, seed=SEED + 32)
opt = Adam(p, lr=3e-3)
train_steps(p, opt, Xtr, Ytr, STEPS // 3, seed=SEED + 33)
results['D_abl_growthOFF_curr'] = dict(train=acc(p, Xtr, Ytr), heldout=acc(p, Xte, Yte),
                                       shuffle=acc_shuffle(p, test_triples, Yte))

# E. ablation growth-ON + curriculum SHUFFLE (grow but flat mix, no staging)
p = init_mlp(16, SEED + 40); opt = Adam(p, lr=3e-3)
train_steps(p, opt, Xtr, Ytr, STEPS // 3, seed=SEED + 41)   # flat from start
p = net2wider(p, 32, SEED + 42); opt = Adam(p, lr=3e-3)
train_steps(p, opt, Xtr, Ytr, STEPS // 3, seed=SEED + 43)
p = net2wider(p, 64, SEED + 44); opt = Adam(p, lr=3e-3)
train_steps(p, opt, Xtr, Ytr, STEPS // 3, seed=SEED + 45)
results['E_abl_growth_currSHUF'] = dict(train=acc(p, Xtr, Ytr), heldout=acc(p, Xte, Yte),
                                        shuffle=acc_shuffle(p, test_triples, Yte))

# F. DIAGNOSTIC: explicit composition-operator model (bilinear) -- NOT the (3) lever.
#    per-primitive learned KxK matrix M_i; logits = M_f @ (M_g @ onehot(x)).
#    This has the RIGHT structure (a non-commutative combination operator). If it
#    generalizes to held-out pairs while B..E do not, the lever is the OPERATOR/
#    target-structure (DPI meta-law), NOT mitosis-growth or curriculum.
def comp_operator(steps=9000):
    r = np.random.default_rng(SEED + 50)
    M = r.normal(0, 0.3, (N_PRIM, K, K))
    M[0] = np.eye(K) * 3.0  # identity primitive warm-start toward I (still trained)
    opt_m = None
    m = np.zeros_like(M); v = np.zeros_like(M); t = 0
    lr = 5e-3
    F = np.array([tt[0] for tt in singles + train_pair_triples])
    G = np.array([tt[1] for tt in singles + train_pair_triples])
    Xi = np.array([tt[2] for tt in singles + train_pair_triples])
    Yl = Ytr; n = len(Yl)
    def fwd(Mp, f, g, xi):
        oh = np.eye(K)[xi]                    # (B,K)
        hg = np.einsum('bij,bj->bi', Mp[g], oh)   # M_g @ onehot(x)
        z = np.einsum('bij,bj->bi', Mp[f], hg)    # M_f @ hg
        return oh, hg, z
    for s in range(steps):
        idx = r.integers(0, n, size=64)
        f, g, xi, y = F[idx], G[idx], Xi[idx], Yl[idx]
        oh, hg, z = fwd(M, f, g, xi)
        zz = z - z.max(1, keepdims=True); e = np.exp(zz); sm = e / e.sum(1, keepdims=True)
        dz = sm.copy(); dz[np.arange(len(y)), y] -= 1; dz /= len(y)   # (B,K) dL/dz
        gM = np.zeros_like(M)
        # dz w.r.t M_f: z = M_f @ hg -> dM_f = dz outer hg
        np.add.at(gM, f, np.einsum('bi,bj->bij', dz, hg))
        # backprop to hg: dhg = M_f^T @ dz ; z=M_g@oh -> dM_g = dhg outer oh
        dhg = np.einsum('bij,bi->bj', M[f], dz)
        np.add.at(gM, g, np.einsum('bi,bj->bij', dhg, oh))
        t += 1; b1, b2, eps = 0.9, 0.999, 1e-8
        m = b1 * m + (1 - b1) * gM; v = b2 * v + (1 - b2) * gM ** 2
        mh = m / (1 - b1 ** t); vh = v / (1 - b2 ** t)
        M -= lr * mh / (np.sqrt(vh) + eps)
    def a(triples, Y):
        F = np.array([tt[0] for tt in triples]); G = np.array([tt[1] for tt in triples]); Xi = np.array([tt[2] for tt in triples])
        _, _, z = fwd(M, F, G, Xi)
        return (z.argmax(1) == Y).mean()
    def a_shuf(triples, Y):
        F = np.array([tt[1] for tt in triples]); G = np.array([tt[0] for tt in triples]); Xi = np.array([tt[2] for tt in triples])
        _, _, z = fwd(M, F, G, Xi)
        return (z.argmax(1) == Y).mean()
    return a(singles + train_pair_triples, Ytr), a(test_triples, Yte), a_shuf(test_triples, Yte)

comp_tr, comp_te, comp_sh = comp_operator()
results['F_diag_comp_operator'] = dict(train=comp_tr, heldout=comp_te, shuffle=comp_sh)

chance = 1.0 / K
print(f"\nchance = {chance:.4f}   additive_floor(heldout) = {add_te:.4f}\n")
print(f"{'condition':<26} {'train':>7} {'heldout':>8} {'shuffle':>8} {'earned-add':>11}")
for k, v in results.items():
    sh = f"{v['shuffle']:.4f}" if v['shuffle'] is not None else "  --  "
    gap = f"{v['heldout']-add_te:+.4f}"
    print(f"{k:<26} {v['train']:>7.4f} {v['heldout']:>8.4f} {sh:>8} {gap:>11}")

import json
with open('/Users/mini/dancinlab/anima/.claude/worktrees/wf_aa95feaf-90c-3/state/trunk_obj_step0/mitosis_curriculum/result.json', 'w') as fh:
    json.dump(dict(chance=chance, additive_floor_heldout=add_te, additive_floor_train=add_tr,
                   results={k: {kk: (None if vv is None else float(vv)) for kk, vv in v.items()} for k, v in results.items()},
                   config=dict(K=K, N_PRIM=N_PRIM, STEPS=STEPS, seed=SEED,
                               n_test_pairs=len(test_pairs), n_train_pairs=len(train_pairs))),
              fh, indent=2)
print("\nwrote result.json")
