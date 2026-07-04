#!/usr/bin/env python3
# ==========================================================================
# H_1717 — Apical-Basal Coincidence Ignition  ($0 cheap_test, numpy only)
# ==========================================================================
# DIRECTIONAL ONLY — numpy toy, NOT engine-native (a_engine_native_learning).
# Terminal verdict requires cli/anima.hexa -> generator L3 -> g_gates byte-parity.
#
# MECHANISM (the differentiator):
#   Cortical pyramidal neurons are two-compartment coincidence detectors. A BASAL
#   (bottom-up / feedforward) input and an APICAL (top-down / context) input that
#   arrive *coincidentally* trigger a dendritic Ca2+ plateau -> a high-gain burst
#   ("BAC firing" / apical amplification). Either input ALONE only weakly drives
#   the soma. The burst output is therefore (roughly) the PRODUCT basal*apical —
#   a hardware AND/conjunction gate. The G1 claim: this multiplicative coincidence
#   IGNITION can bind two factors into a conjunction (composed_distinct >= 2 AND
#   > max_single AND coherent), whereas a purely ADDITIVE soma (basal + apical,
#   the "CE-on-marginals" pattern that clm303 had at lossF~0 yet recombine-FAIL)
#   cannot represent the conjunction and collapses to the better single factor.
#
# DECISIVE INERT TEST (rule 3): take the SAME trained model and replace the
#   coincidence nonlinearity product(basal,apical) -> sum(basal,apical) (the only
#   mechanism turned OFF). If composed accuracy collapses to ~max_single, the
#   coincidence-ignition is LOAD-BEARING. If unchanged, it is INERT (contributes 0).
#
# BINDING SPLIT (rule 2): ambiguous-pair separation — measure on the binding-
#   required (ambiguous) subset where marginals P(y|basal), P(y|apical) are
#   UNIFORM so a copy/marginal shortcut scores 0.5 (chance) while true conjunction
#   scores 1.0. Full-set acc is REPORTED but is NOT a bar (additive inflates it).
#
# GROK POSITIVE CONTROL (rule 4, under-power guard): the SAME numpy toy is asked
#   to learn the canonical composable task (modular addition (a+b)%P with a
#   compositional held-out split). If it cannot beat chance there, the toy lacks
#   resolution -> verdict UNDER-POWER (NOT the mechanism's fault). grok_ctrl_pass
#   iff held-out >> chance.
#
# TOP-3 LESSON (rule 5): $0 toys are usually under-power; report honestly. The
#   INERT/load-bearing measurement is still worth capturing regardless.
#
# ------------------------------------------------------------------------
# FROZEN BARS  (pre-registered HERE, before any run — tune-to-green forbidden, p7)
# ------------------------------------------------------------------------
# (G1) composition + INERT, on the AMBIGUOUS (binding-required) subset:
#       composed_distinct (coincidence model held-out acc) >= 0.90
#       AND composed > max_single + 0.15   (a real binding gain, not marginal)
#       AND max_single <= 0.60             (copy/marginal ~chance 0.5)
#       AND ablate_INERT (product->sum, same weights) <= max_single + 0.10
#                                          (INERT collapse = mechanism load-bearing)
# (GROK CTRL) modular-addition held-out >> chance:
#       grok_held >= 0.50  (chance = 1/P = 1/7 ~ 0.143); PASS marks resolution.
#
# SURVIVOR (very conservative): G1 bar PASS  AND  grok_ctrl_pass  AND
#       ablation load-bearing (INERT collapse observed).
# ------------------------------------------------------------------------
import numpy as np

SEED = 7
rng = np.random.default_rng(SEED)

# ==========================================================================
# TASK: two factors (basal symbol b in [0,Kb), apical symbol a in [0,Ka)).
#   target y = bind(b,a) = a fixed pseudo-random conjunction code (b,a)->class.
#   Crucially y is NOT a function of b alone or a alone (true conjunction):
#   for every b, the map a->y is a different permutation, so P(y|b) and P(y|a)
#   are both UNIFORM => no marginal/copy shortcut on the binding-required subset.
# ==========================================================================
Kb, Ka = 6, 6
NCLASS = Kb * Ka
# conjunction code: y[b,a] = (b*Ka + a) but scrambled so neither margin leaks
perm = rng.permutation(NCLASS)
YMAP = perm.reshape(Kb, Ka)          # YMAP[b,a] -> class in [0,NCLASS)

def onehot(i, n):
    v = np.zeros(n); v[i] = 1.0; return v

def make_pairs():
    return [(b, a) for b in range(Kb) for a in range(Ka)]

# compositional held-out: hold out a set of (b,a) combos NEVER seen in training,
# but every b and every a IS seen (in other combos) -> generalization by binding.
ALL = make_pairs()
rng.shuffle(ALL)
nh = NCLASS // 3
HELD = ALL[:nh]
TRAIN = ALL[nh:]
# ensure coverage: every b and a appears in TRAIN
seen_b = {b for (b, a) in TRAIN}; seen_a = {a for (b, a) in TRAIN}
assert seen_b == set(range(Kb)) and seen_a == set(range(Ka)), "coverage broken"

def encode(b, a):
    """basal channel = one-hot(b) padded; apical channel = one-hot(a) padded."""
    xb = onehot(b, Kb)
    xa = onehot(a, Ka)
    return xb, xa

def build(pairs, reps=200):
    XB, XA, Y = [], [], []
    for _ in range(reps):
        for (b, a) in pairs:
            xb, xa = encode(b, a)
            XB.append(xb); XA.append(xa); Y.append(YMAP[b, a])
    return np.array(XB), np.array(XA), np.array(Y)

XB_tr, XA_tr, Y_tr = build(TRAIN)
XB_he, XA_he, Y_he = build(HELD, reps=1)

# ==========================================================================
# COINCIDENCE-IGNITION MODEL (two-compartment pyramidal):
#   basal drive   gb = Wb @ xb        (per hidden unit)
#   apical drive  ga = Wa @ xa
#   ignition (BAC): burst = relu(gb) * relu(ga)   <-- multiplicative coincidence
#                   + small linear leak so single inputs weakly drive soma
#   logits = Wout @ burst
#   ABLATION (INERT): burst_add = relu(gb) + relu(ga)  (sum, mechanism OFF)
# Trained with plain SGD + softmax-CE (gradient through the product).
# ==========================================================================
H = 128

def init_params():
    return {
        'Wb': rng.normal(0, 1/np.sqrt(Kb), (H, Kb)),
        'Wa': rng.normal(0, 1/np.sqrt(Ka), (H, Ka)),
        'Wout': rng.normal(0, 1/np.sqrt(H), (NCLASS, H)),
        'bout': np.zeros(NCLASS),
    }

def relu(x): return np.maximum(x, 0.0)
def drelu(x): return (x > 0.0).astype(float)

def softmax(z):
    z = z - z.max(axis=1, keepdims=True)
    e = np.exp(z); return e / e.sum(axis=1, keepdims=True)

LEAK = 0.10   # small additive leak so isolated inputs weakly reach soma (biology)

def forward(p, XB, XA, mode='coincidence'):
    gb = XB @ p['Wb'].T            # (N,H)
    ga = XA @ p['Wa'].T
    rb, ra = relu(gb), relu(ga)
    if mode == 'coincidence':
        burst = rb * ra + LEAK * (rb + ra)
    elif mode == 'additive':       # INERT ablation: product -> sum
        burst = rb + ra
    else:
        raise ValueError(mode)
    logits = burst @ p['Wout'].T + p['bout']
    cache = (gb, ga, rb, ra, burst)
    return logits, cache

def train(p, XB, XA, Y, epochs=600, lr=0.3, mode='coincidence'):
    N = len(Y)
    for _ in range(epochs):
        logits, (gb, ga, rb, ra, burst) = forward(p, XB, XA, mode)
        P = softmax(logits)
        dlog = P.copy(); dlog[np.arange(N), Y] -= 1.0; dlog /= N
        gWout = dlog.T @ burst
        gbout = dlog.sum(0)
        dburst = dlog @ p['Wout']                       # (N,H)
        if mode == 'coincidence':
            drb = dburst * (ra + LEAK)
            dra = dburst * (rb + LEAK)
        else:
            drb = dburst.copy(); dra = dburst.copy()
        dgb = drb * drelu(gb)
        dga = dra * drelu(ga)
        gWb = dgb.T @ XB
        gWa = dga.T @ XA
        p['Wb']   -= lr * gWb
        p['Wa']   -= lr * gWa
        p['Wout'] -= lr * gWout
        p['bout'] -= lr * gbout
    return p

def acc(p, XB, XA, Y, mode='coincidence'):
    logits, _ = forward(p, XB, XA, mode)
    return float(np.mean(np.argmax(logits, axis=1) == Y))

# ---- train the coincidence-ignition model ----
p_coin = train(init_params(), XB_tr, XA_tr, Y_tr, mode='coincidence')
composed_train = acc(p_coin, XB_tr, XA_tr, Y_tr, 'coincidence')
composed_held  = acc(p_coin, XB_he, XA_he, Y_he, 'coincidence')

# ---- max_single: single-factor baselines (copy/marginal shortcut ceiling) ----
# basal-only model: predict y from b alone (ablate apical -> see only basal)
def single_factor_acc(use='basal'):
    pp = init_params()
    # zero the unused channel both in train and eval
    XBz = np.zeros_like(XB_tr); XAz = np.zeros_like(XA_tr)
    XBz_h = np.zeros_like(XB_he); XAz_h = np.zeros_like(XA_he)
    if use == 'basal':
        Tb, Ta, Tb_h, Ta_h = XB_tr, XAz, XB_he, XAz_h
    else:
        Tb, Ta, Tb_h, Ta_h = XBz, XA_tr, XBz_h, XA_he
    # train an additive model on the single visible factor (best a margin can do)
    pp = train(pp, Tb, Ta, Y_tr, mode='additive')
    return acc(pp, Tb_h, Ta_h, Y_he, 'additive')

acc_basal_only  = single_factor_acc('basal')
acc_apical_only = single_factor_acc('apical')
max_single = max(acc_basal_only, acc_apical_only)

# ---- INERT ablation: SAME trained coincidence weights, product -> sum ----
ablate_inert_held = acc(p_coin, XB_he, XA_he, Y_he, 'additive')

# ---- also: a from-scratch additive model (CE-on-marginals analogue) ----
p_add = train(init_params(), XB_tr, XA_tr, Y_tr, mode='additive')
additive_scratch_held = acc(p_add, XB_he, XA_he, Y_he, 'additive')

# ---- distinct composed classes correctly settled on held-out ----
logits_h, _ = forward(p_coin, XB_he, XA_he, 'coincidence')
pred_h = np.argmax(logits_h, axis=1)
correct_classes = sorted(set(int(c) for c, y in zip(pred_h, Y_he) if c == y))
composed_distinct = len(correct_classes)

chance = 1.0 / NCLASS

# ==========================================================================
# GROK POSITIVE CONTROL — modular addition (a+b)%P, compositional held split.
#   Same numpy two-compartment toy. If it cannot beat chance here, the toy is
#   UNDER-POWERED (not the mechanism). Uses Adam for a fair grok chance.
# ==========================================================================
class Adam:
    def __init__(self, params, lr=1e-2, b1=0.9, b2=0.999, eps=1e-8, wd=1e-2):
        self.lr, self.b1, self.b2, self.eps, self.wd = lr, b1, b2, eps, wd
        self.m = {k: np.zeros_like(v) for k, v in params.items()}
        self.v = {k: np.zeros_like(v) for k, v in params.items()}
        self.t = 0
    def step(self, params, grads):
        self.t += 1
        for k in params:
            g = grads[k] + self.wd * params[k]
            self.m[k] = self.b1*self.m[k] + (1-self.b1)*g
            self.v[k] = self.b2*self.v[k] + (1-self.b2)*(g*g)
            mh = self.m[k]/(1-self.b1**self.t); vh = self.v[k]/(1-self.b2**self.t)
            params[k] -= self.lr * mh/(np.sqrt(vh)+self.eps)

def grok_control(P=7, seed=11, steps=15000):
    rg = np.random.default_rng(seed)
    pairs = [(a, b) for a in range(P) for b in range(P)]
    rg.shuffle(pairs)
    nh = len(pairs)//2
    held, train_ = pairs[:nh], pairs[nh:]
    # cover all a and all b in train_
    def enc(a, b):
        xb = onehot(b, P); xa = onehot(a, P); return xb, xa
    XBt = np.stack([enc(a, b)[0] for (a, b) in train_])
    XAt = np.stack([enc(a, b)[1] for (a, b) in train_])
    Yt  = np.array([(a + b) % P for (a, b) in train_])
    XBh = np.stack([enc(a, b)[0] for (a, b) in held])
    XAh = np.stack([enc(a, b)[1] for (a, b) in held])
    Yh  = np.array([(a + b) % P for (a, b) in held])
    Hh = 128
    pr = {
        'Wb': rg.normal(0, 1/np.sqrt(P), (Hh, P)),
        'Wa': rg.normal(0, 1/np.sqrt(P), (Hh, P)),
        'Wout': rg.normal(0, 1/np.sqrt(Hh), (P, Hh)),
        'bout': np.zeros(P),
    }
    opt = Adam(pr, lr=5e-3, wd=1e-2)
    N = len(Yt); best = 0.0
    for st in range(steps):
        gb = XBt @ pr['Wb'].T; ga = XAt @ pr['Wa'].T
        rb, ra = relu(gb), relu(ga)
        burst = rb*ra + LEAK*(rb+ra)
        logits = burst @ pr['Wout'].T + pr['bout']
        Pp = softmax(logits)
        dlog = Pp.copy(); dlog[np.arange(N), Yt] -= 1.0; dlog /= N
        g = {}
        g['Wout'] = dlog.T @ burst; g['bout'] = dlog.sum(0)
        dburst = dlog @ pr['Wout']
        drb = dburst*(ra+LEAK); dra = dburst*(rb+LEAK)
        dgb = drb*drelu(gb); dga = dra*drelu(ga)
        g['Wb'] = dgb.T @ XBt; g['Wa'] = dga.T @ XAt
        opt.step(pr, g)
        if st % 2500 == 0 or st == steps-1:
            gbh = XBh @ pr['Wb'].T; gah = XAh @ pr['Wa'].T
            bh = relu(gbh)*relu(gah) + LEAK*(relu(gbh)+relu(gah))
            lh = bh @ pr['Wout'].T + pr['bout']
            best = max(best, float(np.mean(np.argmax(lh, 1) == Yh)))
    return best, 1.0/P

grok_held, grok_chance = grok_control()
grok_ctrl_pass = grok_held >= 0.50

# ==========================================================================
# VERDICT
# ==========================================================================
g1_pass = (composed_held >= 0.90
           and composed_held > max_single + 0.15
           and max_single <= 0.60
           and ablate_inert_held <= max_single + 0.10)
ablation_load_bearing = ablate_inert_held <= max_single + 0.10

survivor = bool(g1_pass and grok_ctrl_pass and ablation_load_bearing)

if not grok_ctrl_pass:
    verdict = "UNDER-POWER"
elif g1_pass and ablation_load_bearing:
    verdict = "SUPPORTED"
elif g1_pass or ablation_load_bearing:
    verdict = "MIXED"
else:
    verdict = "NOT-SUPPORTED"

print("=" * 78)
print("H_1717 — Apical-Basal Coincidence Ignition   [DIRECTIONAL numpy toy]")
print("=" * 78)
print(f"task: bind(b,a) scrambled conjunction | Kb={Kb} Ka={Ka} NCLASS={NCLASS} "
      f"chance={chance:.4f}")
print(f"      held-out = {nh} novel (b,a) combos; every b,a seen elsewhere (compositional)")
print("-" * 78)
print("(G1) composition + INERT ablation  [binding-required: margins uniform]")
print(f"    composed_train            = {composed_train:.3f}")
print(f"    composed_held (DISTINCT)  = {composed_held:.3f}   (bar >= 0.90)")
print(f"    composed_distinct classes = {composed_distinct} / {nh} held")
print(f"    max_single (basal {acc_basal_only:.3f} | apical {acc_apical_only:.3f}) = {max_single:.3f}   (bar <= 0.60)")
print(f"    composed - max_single     = {composed_held - max_single:+.3f}   (bar > +0.15)")
print(f"    ablate-INERT (prod->sum)  = {ablate_inert_held:.3f}   (bar <= max_single+0.10 = {max_single+0.10:.3f})")
print(f"    additive-from-scratch held= {additive_scratch_held:.3f}   (CE-on-marginals analogue, reported)")
print(f"    -> ablation load-bearing  = {ablation_load_bearing}")
print(f"    -> (G1) {'PASS' if g1_pass else 'FAIL'}")
print("-" * 78)
print("(GROK CTRL) modular addition (a+b)%7, compositional held  [under-power guard]")
print(f"    grok_held = {grok_held:.3f}   (chance = 1/7 = {grok_chance:.3f}; bar >= 0.50)")
print(f"    -> grok_ctrl_pass = {grok_ctrl_pass}")
print("=" * 78)
print(f"VERDICT: {verdict}    survivor={survivor}")
print(f"  [G1={'P' if g1_pass else 'F'}  grok={'P' if grok_ctrl_pass else 'F'}  "
      f"INERT-load-bearing={'Y' if ablation_load_bearing else 'N'}]")
print("numpy toy = DIRECTIONAL only; NOT engine-native (a_engine_native_learning).")
print("=" * 78)
