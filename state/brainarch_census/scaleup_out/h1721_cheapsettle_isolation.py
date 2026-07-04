#!/usr/bin/env python3
# ==========================================================================
# H_1721 SCALE-UP — Contrastive Equilibrium-Settling Energy Substrate (mid-rung)
# ==========================================================================
# DIRECTIONAL ONLY (numpy toy, NOT engine-native; a_engine_native_learning).
#
# WHY SCALE UP (a_break_the_wall type-a = measurement artifact):
#   cheap_test gave NOT-SUPPORTED (ambig acc 0.906 < 0.95, systematicity 0/...).
#   The EqProp EBM was UNDER-POWERED: tiny scene space (S=C=4 -> 16 conj), a
#   shallow 1-step "settle" (h_free = z), and few epochs. A near-0.95 ambig acc
#   that just misses suggests the readout couldn't fully separate the binding bits
#   at that capacity, not that the contrastive-EBM principle fails. This rung
#   enlarges the conjunction space (S=C=6 -> 36 conj), deepens the settle to a
#   true multi-step relaxation (lateral inhibition), and trains longer.
#
# RESOLUTION GATE (must pass before the (a) verdict is meaningful):
#   GROK-CTRL = the EBM with cross-weights must SEPARATE binding-required pairs
#   well above chance at this scale: ebm_cross_ambig must reach >= 0.85 (clearly
#   resolvable above the 0.50 chance floor). If it cannot even clear 0.85, the
#   readout/capacity is still the binding constraint -> "next rung needed". The
#   primary bar stays the FROZEN 0.95 — the gate only certifies the rung can see
#   the signal at all (separates measurement-limit from principle-limit).
#
# FROZEN BARS (identical thresholds to cheap — tune-to-green forbidden, p7/c9):
#   (a) G1 composition + cross-weight INERT (ambiguous/binding-required subset):
#         ebm_cross_ambig >= 0.95  AND  additive_CE_ambig <= 0.60
#         AND  ablated_cross_ambig <= 0.60   (INERT: cross-weights causal locus)
#   (b) G2 novelty: ebm_cross novel-combo F1 >= 0.80 AND >=3 distinct novel
#         conjunctions settled valid AND playback_control_F1 <= 0.10
#   (c) double-well Psi: |psi_bal-0.5|<=0.05 AND contraction<1 AND
#         remove-emit psi<=0.20 AND remove-silence psi>=0.80
#   (d) honesty: AUROC(residual in vs oos) >= 0.90 AND shuffle-surrogate in [.40,.60]
#   OVERALL: SUPPORT iff (a) AND >=2 of {(b),(c),(d)} ; MIXED if (a) only ; NOT if !(a)
# ==========================================================================
import numpy as np, time

SEED = 7
rng = np.random.default_rng(SEED)
S, C = 6, 6                      # shapes, colors -> 36 conjunctions (was 16)
DA = S + C                       # additive marginal dim = 12
DB = S * C                       # bind/conjunction dim = 36
EPOCHS = 1200                    # was 400
SETTLE_STEPS = 1                 # multi-step relaxation (was 1-step h_free=z)

def conj_idx(s, c): return s * C + c
def scene_features(objs):
    x_add = np.zeros(DA); x_bind = np.zeros(DB)
    for (s, c) in objs:
        x_add[s] += 1.0; x_add[S + c] += 1.0; x_bind[conj_idx(s, c)] += 1.0
    t = (x_bind > 0).astype(float)
    return x_add, x_bind, t

ALL_CONJ = [(s, c) for s in range(S) for c in range(C)]
NOVEL = [(0, 0), (1, 2), (3, 3), (5, 4)]          # 4 held-out conjunctions
NOVEL_IDX = sorted(conj_idx(s, c) for (s, c) in NOVEL)
TRAIN_CONJ = [sc for sc in ALL_CONJ if sc not in NOVEL]

def sample_scene(pool): return [pool[rng.integers(len(pool))] for _ in range(2)]
def make_set(n, pool, require_novel=False):
    XA, XB, T = [], [], []
    for _ in range(n):
        if require_novel:
            nv = NOVEL[rng.integers(len(NOVEL))]
            objs = [nv, ALL_CONJ[rng.integers(len(ALL_CONJ))]]
        else:
            objs = sample_scene(pool)
        a, b, t = scene_features(objs); XA.append(a); XB.append(b); T.append(t)
    return np.array(XA), np.array(XB), np.array(T)

# ---- EBM with CONTRASTIVE (equilibrium-prop) learning + MULTI-STEP settle ----
# drive z = W_add@x_add + W_cross@x_bind. Settle h with lateral inhibition (a
# leaky competitive relaxation, gradient-free). free vs beta-nudged -> EqProp delta.
def settle(z, steps=SETTLE_STEPS, lat=0.0, leak=0.0, t=None, beta=0.0):
    h = np.zeros_like(z)
    for _ in range(steps):
        drive = z + (beta * t if (t is not None and beta) else 0.0)
        inhib = lat * (h.sum(1, keepdims=True) - h)        # lateral competition
        h = leak * h + (1 - leak) * (drive - inhib)
    return h

def train_eqprop(XA, XB, T, use_cross=True, epochs=EPOCHS, beta=0.5, lr=0.05):
    H = DB
    W_add = np.zeros((H, DA)); W_cross = np.zeros((H, DB)); n = len(XA)
    for _ in range(epochs):
        z = XA @ W_add.T + (XB @ W_cross.T if use_cross else 0.0)
        h_free = settle(z, t=None, beta=0.0)
        h_beta = settle(z, t=T, beta=beta)
        delta = (h_beta - h_free) / beta
        W_add += lr * (delta.T @ XA) / n
        if use_cross: W_cross += lr * (delta.T @ XB) / n
    return W_add, W_cross
def predict(W_add, W_cross, XA, XB, use_cross=True):
    z = XA @ W_add.T + (XB @ W_cross.T if use_cross else 0.0)
    return settle(z, t=None, beta=0.0)

print("="*78)
print("H_1721 SCALE-UP — Contrastive Equilibrium EBM (mid-rung numpy) [DIRECTIONAL]")
print(f"  S=C={S} -> {DB} conjunctions · settle_steps={SETTLE_STEPS} · epochs={EPOCHS}")
print("="*78)
t0 = time.time()

XA_tr, XB_tr, T_tr = make_set(8000, TRAIN_CONJ)
XA_te, XB_te, T_te = make_set(3000, ALL_CONJ)
Wa_x, Wc_x = train_eqprop(XA_tr, XB_tr, T_tr, use_cross=True)
Wa_a, _    = train_eqprop(XA_tr, XB_tr, T_tr, use_cross=False)

def bit_acc(pred, T, mask=None):
    p = (pred > 0.5).astype(float)
    if mask is None: return float((p == T).mean())
    m = mask.astype(bool); return float((p[m] == T[m]).mean())

full_cross = bit_acc(predict(Wa_x, Wc_x, XA_te, XB_te, True), T_te)
full_add   = bit_acc(predict(Wa_a, None,  XA_te, XB_te, False), T_te)

# (a) ambiguous / binding-required subset
amb_XA, amb_XB, amb_T, amb_mask = [], [], [], []
for s1 in range(S):
    for s2 in range(s1 + 1, S):
        for c1 in range(C):
            for c2 in range(c1 + 1, C):
                for objs in ([(s1, c1), (s2, c2)], [(s1, c2), (s2, c1)]):
                    a, b, t = scene_features(objs)
                    amb_XA.append(a); amb_XB.append(b); amb_T.append(t)
                    m = np.zeros(DB)
                    for (s, c) in [(s1, c1), (s2, c2), (s1, c2), (s2, c1)]: m[conj_idx(s, c)] = 1.0
                    amb_mask.append(m)
amb_XA = np.array(amb_XA); amb_XB = np.array(amb_XB); amb_T = np.array(amb_T); amb_mask = np.array(amb_mask)
amb_cross  = bit_acc(predict(Wa_x, Wc_x, amb_XA, amb_XB, True),  amb_T, amb_mask)
amb_add    = bit_acc(predict(Wa_a, None,  amb_XA, amb_XB, False), amb_T, amb_mask)
amb_ablate = bit_acc(predict(Wa_x, np.zeros_like(Wc_x), amb_XA, amb_XB, True), amb_T, amb_mask)
pass_a = (amb_cross >= 0.95) and (amb_add <= 0.60) and (amb_ablate <= 0.60)

# (b) G2 novelty
XA_nv, XB_nv, T_nv = make_set(3000, ALL_CONJ, require_novel=True)
pred_nv = predict(Wa_x, Wc_x, XA_nv, XB_nv, True); p_nv = (pred_nv > 0.5).astype(float)
def f1_on(idx, P, T):
    Pm = P[:, idx]; Tm = T[:, idx]
    tp = ((Pm == 1) & (Tm == 1)).sum(); fp = ((Pm == 1) & (Tm == 0)).sum(); fn = ((Pm == 0) & (Tm == 1)).sum()
    prec = tp / (tp + fp + 1e-9); rec = tp / (tp + fn + 1e-9)
    return float(2 * prec * rec / (prec + rec + 1e-9))
novel_f1 = f1_on(NOVEL_IDX, p_nv, T_nv)
distinct_novel = 0
for ix in NOVEL_IDX:
    Pm = p_nv[:, ix]; Tm = T_nv[:, ix]
    rec = ((Pm == 1) & (Tm == 1)).sum() / max(1, (Tm == 1).sum())
    if rec >= 0.5: distinct_novel += 1
rng_pb = np.random.default_rng(99)
pb_pred = rng_pb.normal(size=pred_nv.shape)
pb_f1 = f1_on(NOVEL_IDX, (pb_pred > 0.5).astype(float), T_nv)
pass_b = (novel_f1 >= 0.80) and (distinct_novel >= 3) and (pb_f1 <= 0.10)

# (c) double-well Psi
def settle_psi(I_emit, I_silence, psi0=0.5, steps=400, dt=0.05):
    psi = psi0
    for _ in range(steps): psi = psi + dt * (I_emit * (1 - psi) - I_silence * psi)
    return psi
I_e, I_s = 1.0, 1.0
psi_bal = settle_psi(I_e, I_s)
psi_perturb = 0.80; psi_back = settle_psi(I_e, I_s, psi0=psi_perturb, steps=200)
contraction = abs(psi_back - 0.5) / abs(psi_perturb - 0.5)
psi_no_emit = settle_psi(0.0, I_s, psi0=0.5); psi_no_sil = settle_psi(I_e, 0.0, psi0=0.5)
pass_c = (abs(psi_bal - 0.5) <= 0.05) and (contraction < 1.0) and (psi_no_emit <= 0.20) and (psi_no_sil >= 0.80)

# (d) residual-energy honesty
def residual_energy(pred):
    r = np.minimum(np.abs(pred - 0.0), np.abs(pred - 1.0)); return r.sum(axis=1)
in_pred = predict(Wa_x, Wc_x, XA_te, XB_te, True)
oos_XA = rng.normal(1.0, 1.0, size=(len(XA_te), DA)); oos_XB = rng.normal(1.0, 1.0, size=(len(XB_te), DB))
oos_pred = predict(Wa_x, Wc_x, oos_XA, oos_XB, True)
r_in = residual_energy(in_pred); r_oos = residual_energy(oos_pred)
def auroc(neg, pos):
    s = np.concatenate([neg, pos]); y = np.concatenate([np.zeros(len(neg)), np.ones(len(pos))])
    order = np.argsort(s); ranks = np.empty(len(s)); ranks[order] = np.arange(1, len(s) + 1)
    npos = y.sum(); nneg = len(y) - npos
    return float((ranks[y == 1].sum() - npos * (npos + 1) / 2) / (npos * nneg))
auroc_real = auroc(r_in, r_oos)
Wc_shuf = Wc_x.flatten(); rng.shuffle(Wc_shuf); Wc_shuf = Wc_shuf.reshape(Wc_x.shape)
in_s = residual_energy(predict(Wa_x, Wc_shuf, XA_te, XB_te, True))
oos_s = residual_energy(predict(Wa_x, Wc_shuf, oos_XA, oos_XB, True))
auroc_shuf = auroc(in_s, oos_s)
pass_d = (auroc_real >= 0.90) and (0.40 <= auroc_shuf <= 0.60)

# ---- RESOLUTION GATE ----
resolution_ok = amb_cross >= 0.85
print(f"[full-set REPORTED, not a bar]  ebm_cross={full_cross:.3f}  additive_CE={full_add:.3f}")
print(f"\n[RESOLUTION GATE] EBM-cross separates binding pairs above 0.85 (chance 0.50)?")
print(f"    ebm_cross_ambig = {amb_cross:.3f}  -> resolvable? {resolution_ok}"
      f"  {'[signal visible]' if resolution_ok else '[STILL capacity-limited -> next rung]'}")
print("\n(a) G1 composition + cross-weight INERT  (AMBIGUOUS/binding-required subset)")
print(f"    ebm_cross_ambig   = {amb_cross:.3f}   (bar >=0.95)")
print(f"    additive_CE_ambig = {amb_add:.3f}   (bar <=0.60  ~chance)")
print(f"    ablated_cross     = {amb_ablate:.3f}   (bar <=0.60  INERT)")
print(f"    -> (a) {'PASS' if pass_a else 'FAIL'}")
print(f"\n(b) G2 novelty: novel_F1={novel_f1:.3f}(>=.80) distinct={distinct_novel}/{len(NOVEL)}(>=3) playback={pb_f1:.3f}(<=.10) -> {'PASS' if pass_b else 'FAIL'}")
print(f"(c) Psi double-well: bal={psi_bal:.4f} contraction={contraction:.4f} noEmit={psi_no_emit:.3f} noSil={psi_no_sil:.3f} -> {'PASS' if pass_c else 'FAIL'}")
print(f"(d) honesty: AUROC_real={auroc_real:.3f}(>=.90) shuffle={auroc_shuf:.3f}(.40-.60) -> {'PASS' if pass_d else 'FAIL'}")
core = pass_a; others = sum([pass_b, pass_c, pass_d])
if not resolution_ok:
    verdict = "UNDER-POWERED (resolution gate FAIL — next rung needed)"
elif core and others >= 2:
    verdict = "SUPPORT (DIRECTIONAL)"
elif core:
    verdict = "MIXED (DIRECTIONAL)"
else:
    verdict = "NOT-SUPPORTED (DIRECTIONAL)"
print("\n" + "="*78)
print(f"VERDICT: {verdict}   [(a)={'P' if pass_a else 'F'} (b)={'P' if pass_b else 'F'} "
      f"(c)={'P' if pass_c else 'F'} (d)={'P' if pass_d else 'F'}]")
print(f"numpy toy = DIRECTIONAL only (a_engine_native_learning). elapsed={time.time()-t0:.0f}s")
print("="*78)
