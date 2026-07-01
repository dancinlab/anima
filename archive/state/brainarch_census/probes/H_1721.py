#!/usr/bin/env python3
# ==========================================================================
# H_1721 — Contrastive Equilibrium-Settling Energy Substrate ($0 cheap_test)
# ==========================================================================
# DIRECTIONAL ONLY — numpy toy, NOT engine-native (a_engine_native_learning).
# Terminal verdict requires cli/anima.hexa -> generator L3 -> g_gates byte-parity.
#
# Card claim (the differentiator): an EBM with a CONTRASTIVE energy objective
# (equilibrium-prop: free-settle vs weakly-nudged, local gradient-free rule)
# produces SYNTHESIS (compositional binding / recombination) because its energy
# carries CROSS-TERMS (the basins ARE conjunctions). Token-CE on marginals
# (the clm303 lossF~0-yet-recombine-fail pattern) cannot. The decisive INERT
# test: zero the cross-weights -> joint collapses to the separable additive
# floor. Plus double-well Psi=1/2 antagonistic attractor + residual-energy
# honesty (abstain on out-of-support).
#
# Cheap_test (card, verbatim intent):
#   (a) clamp 2 factors -> joint settle; zero cross-weights -> composed drops to
#       max_single (G1 INERT). [contrastive-EBM vs additive-CE baseline]
#   (b) settle on held-out NOVEL combo -> valid output (G2>=3); playback ctrl 0.
#   (c) double-well readout: perturb Psi -> return to 1/2 saddle w/ contraction;
#       remove one current -> migrates to a well (endogeneity).
#   (d) out-of-support query -> high residual energy -> abstain; AUROC~1 vs a
#       weight-shuffle surrogate at chance.
#
# Precedent (SCREEN_multiply_vs_add): additive can inflate FULL-SET acc via
# marginal shortcut -> MUST measure the ambiguous(binding-required) subset
# separately. Controls: cross-weight ablation, additive-CE baseline, playback,
# weight-shuffle surrogate.
#
# ------------------------------------------------------------------------
# FROZEN BARS  (pre-registered HERE, before any run — tune-to-green forbidden, p7)
# ------------------------------------------------------------------------
# (a) G1 composition + INERT decision (ambiguous/binding-required subset):
#       PASS iff  ebm_cross_ambig >= 0.95
#             AND additive_CE_ambig <= 0.60     (~chance 0.5; CE-on-marginals fails)
#             AND ablated_cross_ambig <= 0.60    (INERT: cross-weights causal locus)
#       (full-set acc REPORTED but NOT a bar — additive inflates it.)
# (b) G2 novelty:
#       PASS iff  ebm_cross novel-combo recall(F1) >= 0.80
#             AND  >=3 distinct novel conjunctions settled valid
#             AND  playback_control_F1 <= 0.10
# (c) double-well Psi:
#       PASS iff  |psi_balanced - 0.5| <= 0.05
#             AND  contraction (|after_perturb-0.5| < |perturb-0.5|, ratio<1)
#             AND  remove emit-current -> psi <= 0.20 (silence well)
#             AND  remove silence-current -> psi >= 0.80 (emit well)
# (d) honesty:
#       PASS iff  AUROC(residual energy: in-support vs out-of-support) >= 0.90
#             AND  weight-shuffle surrogate AUROC in [0.40, 0.60] (chance)
#
# OVERALL: SUPPORT(DIRECTIONAL) iff (a) AND >=2 of {(b),(c),(d)} pass.
#          MIXED if (a) passes but <2 others.  NOT if (a) fails.
# ------------------------------------------------------------------------
import numpy as np

SEED = 7
rng = np.random.default_rng(SEED)
S, C = 4, 4                      # shapes, colors -> 16 conjunctions
DA = S + C                       # additive (marginal) feature dim = 8
DB = S * C                       # bind/conjunction feature dim = 16

def conj_idx(s, c): return s * C + c

def scene_features(objs):
    """objs = list of (shape,color). x_add = marginal counts; x_bind = conj counts."""
    x_add = np.zeros(DA); x_bind = np.zeros(DB)
    for (s, c) in objs:
        x_add[s] += 1.0; x_add[S + c] += 1.0
        x_bind[conj_idx(s, c)] += 1.0
    t = (x_bind > 0).astype(float)          # presence target (16-dim)
    return x_add, x_bind, t

# ---- novelty holdout: a set of conjunctions NEVER present in TRAIN scenes ----
ALL_CONJ = [(s, c) for s in range(S) for c in range(C)]
NOVEL = [(0, 0), (1, 2), (3, 3)]            # 3 held-out conjunctions (G2 test)
NOVEL_IDX = sorted(conj_idx(s, c) for (s, c) in NOVEL)
TRAIN_CONJ = [sc for sc in ALL_CONJ if sc not in NOVEL]

def sample_scene(pool):
    return [pool[rng.integers(len(pool))] for _ in range(2)]

def make_set(n, pool, require_novel=False):
    XA, XB, T = [], [], []
    for _ in range(n):
        if require_novel:
            nv = NOVEL[rng.integers(len(NOVEL))]
            objs = [nv, ALL_CONJ[rng.integers(len(ALL_CONJ))]]
        else:
            objs = sample_scene(pool)
        a, b, t = scene_features(objs)
        XA.append(a); XB.append(b); T.append(t)
    return np.array(XA), np.array(XB), np.array(T)

# ==========================================================================
# EBM with CONTRASTIVE (equilibrium-prop) learning.
#   drive  z = W_add @ x_add + W_cross @ x_bind   (h settles to z; readout=identity)
#   free phase:  h_free = z          (min of E = 0.5||h-z||^2)
#   nudged:      h_beta = (z + beta*t)/(1+beta)   (min of E + beta/2||h-t||^2)
#   EqProp local rule:  dW ~ (1/beta)(h_beta - h_free) x^T  =  (t - z) x^T /(1+beta)
#   -> a local, gradient-free contrastive delta rule.  ADDITIVE-CE baseline uses
#      ONLY x_add (no cross pathway) = CE-on-marginals analogue.
# ==========================================================================
def train_eqprop(XA, XB, T, use_cross=True, epochs=400, beta=0.5, lr=0.05):
    H = DB
    W_add = np.zeros((H, DA))
    W_cross = np.zeros((H, DB))
    n = len(XA)
    for _ in range(epochs):
        z = XA @ W_add.T + (XB @ W_cross.T if use_cross else 0.0)
        h_free = z
        h_beta = (z + beta * T) / (1 + beta)
        delta = (h_beta - h_free) / beta            # = (T - z)/(1+beta)
        W_add += lr * (delta.T @ XA) / n
        if use_cross:
            W_cross += lr * (delta.T @ XB) / n
    return W_add, W_cross

def predict(W_add, W_cross, XA, XB, use_cross=True):
    return XA @ W_add.T + (XB @ W_cross.T if use_cross else 0.0)

# ---- data ----
XA_tr, XB_tr, T_tr = make_set(6000, TRAIN_CONJ)          # train: no novel conj
XA_te, XB_te, T_te = make_set(2000, ALL_CONJ)            # test: all conj (full-set)

# train: contrastive EBM (cross) + additive-CE baseline (marginals only)
Wa_x, Wc_x = train_eqprop(XA_tr, XB_tr, T_tr, use_cross=True)
Wa_a, _    = train_eqprop(XA_tr, XB_tr, T_tr, use_cross=False)

def bit_acc(pred, T, mask=None):
    p = (pred > 0.5).astype(float)
    if mask is None:
        return float((p == T).mean())
    m = mask.astype(bool)
    return float((p[m] == T[m]).mean())

# ---- full-set acc (REPORTED, not a bar) ----
full_cross = bit_acc(predict(Wa_x, Wc_x, XA_te, XB_te, True), T_te)
full_add   = bit_acc(predict(Wa_a, None,  XA_te, XB_te, False), T_te)

# ==========================================================================
# (a) AMBIGUOUS / binding-required subset (precedent: separate measurement).
#   pairs {(s1,c1),(s2,c2)} vs {(s1,c2),(s2,c1)}: identical x_add, different t.
#   measure acc ONLY on the 4 conjunction bits that VARY across the pair
#   (no inflation from shared absent bits).
# ==========================================================================
amb_XA, amb_XB, amb_T, amb_mask = [], [], [], []
for s1 in range(S):
    for s2 in range(s1 + 1, S):
        for c1 in range(C):
            for c2 in range(c1 + 1, C):
                for objs in ([(s1, c1), (s2, c2)], [(s1, c2), (s2, c1)]):
                    a, b, t = scene_features(objs)
                    amb_XA.append(a); amb_XB.append(b); amb_T.append(t)
                    m = np.zeros(DB)
                    for (s, c) in [(s1, c1), (s2, c2), (s1, c2), (s2, c1)]:
                        m[conj_idx(s, c)] = 1.0     # the 4 discriminating bits
                    amb_mask.append(m)
amb_XA = np.array(amb_XA); amb_XB = np.array(amb_XB)
amb_T = np.array(amb_T);   amb_mask = np.array(amb_mask)

amb_cross   = bit_acc(predict(Wa_x, Wc_x, amb_XA, amb_XB, True),  amb_T, amb_mask)
amb_add     = bit_acc(predict(Wa_a, None,  amb_XA, amb_XB, False), amb_T, amb_mask)
# INERT control: take trained EBM, ZERO the cross-weights -> additive floor
amb_ablate  = bit_acc(predict(Wa_x, np.zeros_like(Wc_x), amb_XA, amb_XB, True),
                      amb_T, amb_mask)

pass_a = (amb_cross >= 0.95) and (amb_add <= 0.60) and (amb_ablate <= 0.60)

# ==========================================================================
# (b) G2 novelty: scenes containing held-out conjunctions; recall on novel idx.
# ==========================================================================
XA_nv, XB_nv, T_nv = make_set(2000, ALL_CONJ, require_novel=True)
pred_nv = predict(Wa_x, Wc_x, XA_nv, XB_nv, True)
p_nv = (pred_nv > 0.5).astype(float)

def f1_on(idx, P, T):
    Pm = P[:, idx]; Tm = T[:, idx]
    tp = ((Pm == 1) & (Tm == 1)).sum()
    fp = ((Pm == 1) & (Tm == 0)).sum()
    fn = ((Pm == 0) & (Tm == 1)).sum()
    prec = tp / (tp + fp + 1e-9); rec = tp / (tp + fn + 1e-9)
    return float(2 * prec * rec / (prec + rec + 1e-9))

novel_f1 = f1_on(NOVEL_IDX, p_nv, T_nv)
# count distinct novel conjunctions settled valid (recall>=0.5 each)
distinct_novel = 0
for ix in NOVEL_IDX:
    Pm = p_nv[:, ix]; Tm = T_nv[:, ix]
    rec = ((Pm == 1) & (Tm == 1)).sum() / max(1, (Tm == 1).sum())
    if rec >= 0.5: distinct_novel += 1
# playback control: NO relaxation — settle replaced by frozen random state
rng_pb = np.random.default_rng(99)
pb_pred = rng_pb.normal(size=pred_nv.shape)         # readout of a non-settled state
pb_f1 = f1_on(NOVEL_IDX, (pb_pred > 0.5).astype(float), T_nv)

pass_b = (novel_f1 >= 0.80) and (distinct_novel >= 3) and (pb_f1 <= 0.10)

# ==========================================================================
# (c) double-well Psi=1/2 antagonistic attractor.
#   dpsi/dt = I_emit*(1-psi) - I_silence*psi  (over-damped). Two opposing currents.
#   fixed point psi* = I_emit/(I_emit+I_silence); balanced -> 1/2, contraction
#   rate (I_emit+I_silence). Remove a current -> migrates to the opposite well.
# ==========================================================================
def settle_psi(I_emit, I_silence, psi0=0.5, steps=400, dt=0.05):
    psi = psi0
    for _ in range(steps):
        psi = psi + dt * (I_emit * (1 - psi) - I_silence * psi)
    return psi

I_e, I_s = 1.0, 1.0                                   # balanced (resolved == residual)
psi_bal = settle_psi(I_e, I_s)
# perturb away from saddle, let it relax back -> contraction
psi_perturb = 0.80
psi_back = settle_psi(I_e, I_s, psi0=psi_perturb, steps=200)
contraction = abs(psi_back - 0.5) / abs(psi_perturb - 0.5)
psi_no_emit = settle_psi(0.0, I_s, psi0=0.5)          # -> silence well (0)
psi_no_sil  = settle_psi(I_e, 0.0, psi0=0.5)          # -> emit well (1)

pass_c = (abs(psi_bal - 0.5) <= 0.05) and (contraction < 1.0) \
         and (psi_no_emit <= 0.20) and (psi_no_sil >= 0.80)

# ==========================================================================
# (d) residual-energy honesty.  residual = distance of settled presence vector
#   to nearest VALID near-binary pattern (in-support manifold). Real scenes ->
#   low residual; random/out-of-support inputs -> high residual -> abstain.
#   AUROC vs weight-shuffle surrogate (shuffled cross-weights = no real landscape).
# ==========================================================================
def residual_energy(pred):
    # distance to {0,1}^DB rounded pattern, penalized so confident valid=low
    r = np.minimum(np.abs(pred - 0.0), np.abs(pred - 1.0))   # per-bit ambiguity
    return r.sum(axis=1)

# in-support: real test scenes ; out-of-support: random dense feature vectors
in_pred  = predict(Wa_x, Wc_x, XA_te, XB_te, True)
oos_XA = rng.normal(1.0, 1.0, size=(len(XA_te), DA))
oos_XB = rng.normal(1.0, 1.0, size=(len(XB_te), DB))
oos_pred = predict(Wa_x, Wc_x, oos_XA, oos_XB, True)
r_in = residual_energy(in_pred); r_oos = residual_energy(oos_pred)

def auroc(neg, pos):  # pos = should-score-higher (out-of-support residual)
    s = np.concatenate([neg, pos]); y = np.concatenate([np.zeros(len(neg)), np.ones(len(pos))])
    order = np.argsort(s); ranks = np.empty(len(s)); ranks[order] = np.arange(1, len(s) + 1)
    npos = y.sum(); nneg = len(y) - npos
    return float((ranks[y == 1].sum() - npos * (npos + 1) / 2) / (npos * nneg))

auroc_real = auroc(r_in, r_oos)
# weight-shuffle surrogate: shuffle the cross-weight matrix entries
Wc_shuf = Wc_x.flatten(); rng.shuffle(Wc_shuf); Wc_shuf = Wc_shuf.reshape(Wc_x.shape)
in_s  = residual_energy(predict(Wa_x, Wc_shuf, XA_te, XB_te, True))
oos_s = residual_energy(predict(Wa_x, Wc_shuf, oos_XA, oos_XB, True))
auroc_shuf = auroc(in_s, oos_s)

pass_d = (auroc_real >= 0.90) and (0.40 <= auroc_shuf <= 0.60)

# ==========================================================================
# REPORT
# ==========================================================================
print("=" * 74)
print("H_1721 — Contrastive Equilibrium-Settling Energy Substrate  [DIRECTIONAL numpy toy]")
print("=" * 74)
print(f"[full-set REPORTED, not a bar]  ebm_cross={full_cross:.3f}  additive_CE={full_add:.3f}")
print()
print("(a) G1 composition + cross-weight INERT  (AMBIGUOUS/binding-required subset)")
print(f"    ebm_cross_ambig   = {amb_cross:.3f}   (bar >=0.95)")
print(f"    additive_CE_ambig = {amb_add:.3f}   (bar <=0.60  ~chance)")
print(f"    ablated_cross     = {amb_ablate:.3f}   (bar <=0.60  INERT: zero cross-weights)")
print(f"    -> (a) {'PASS' if pass_a else 'FAIL'}")
print()
print("(b) G2 novelty (held-out conjunctions)")
print(f"    novel_F1 = {novel_f1:.3f} (bar>=0.80)  distinct_novel={distinct_novel}/3 (bar>=3)"
      f"  playback_ctrl_F1={pb_f1:.3f} (bar<=0.10)")
print(f"    -> (b) {'PASS' if pass_b else 'FAIL'}")
print()
print("(c) double-well Psi=1/2 antagonistic attractor")
print(f"    psi_balanced={psi_bal:.4f} (bar |.-.5|<=.05)  contraction={contraction:.4f} (<1)")
print(f"    remove_emit->psi={psi_no_emit:.4f} (<=.20)  remove_silence->psi={psi_no_sil:.4f} (>=.80)")
print(f"    -> (c) {'PASS' if pass_c else 'FAIL'}")
print()
print("(d) residual-energy honesty (abstain on out-of-support)")
print(f"    AUROC_real={auroc_real:.3f} (bar>=0.90)   AUROC_weight_shuffle={auroc_shuf:.3f} (chance .40-.60)")
print(f"    -> (d) {'PASS' if pass_d else 'FAIL'}")
print()
core = pass_a
others = sum([pass_b, pass_c, pass_d])
if core and others >= 2:
    verdict = "SUPPORT (DIRECTIONAL)"
elif core:
    verdict = "MIXED (DIRECTIONAL)"
else:
    verdict = "NOT-SUPPORTED (DIRECTIONAL)"
print("=" * 74)
print(f"VERDICT: {verdict}   [(a)={'P' if pass_a else 'F'} (b)={'P' if pass_b else 'F'} "
      f"(c)={'P' if pass_c else 'F'} (d)={'P' if pass_d else 'F'}]")
print("numpy toy = DIRECTIONAL only; NOT engine-native (a_engine_native_learning).")
print("=" * 74)
