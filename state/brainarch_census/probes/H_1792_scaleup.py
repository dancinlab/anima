#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
H_1792 SCALE-UP — InfoNCE objective as G1 lever (mid-rung, resolution-gated)
============================================================================
DIRECTIONAL ONLY (numpy toy, NOT engine-native; a_engine_native_learning).
This mid-rung is the PREDICTION for the 303M objrun (H_1602) — terminal answer
is the engine-native 303M run, this只是 its miniature forecast.

WHY SCALE UP (a_break_the_wall type-a = measurement artifact):
  The $0 cheap_test was UNDER-POWERED — its grokkability control (single-head
  modular-addition MLP, no shared embedding) sat ≈ chance, i.e. the toy could
  not grok held-out generalization for ANY objective. A negative there measured
  the tool's resolution, not the science. This rung adds the missing inductive
  bias (shared per-symbol EMBEDDING table) + larger dim/width/steps so the grok
  control can actually grok → only THEN is the InfoNCE-vs-CE contrast meaningful.

RESOLUTION GATE (must pass before re-measuring the hypothesis):
  GROK-CTRL = single-head modular-ADDITION with a SHARED embedding table must
  reach held-out acc >> chance (bar: >= 0.80). If it fails, this rung is STILL
  under-powered → report "next rung needed", do NOT stamp the H_1792 bars.

ARCHITECTURE CHANGE vs cheap (isolate OBJECTIVE, a_no_llm_frame_trap):
  cheap used onehot->MLP (no symbol embedding). Mid-rung uses a SHARED EMBEDDING
  table E[symbol] (the grokking-capable inductive bias), then z = MLP([E[a],E[b]]).
  ALL models share this same encoder; ONLY the training objective differs.
  Bigger modulus P, bigger embed/hidden/latent dims, AdamW, more steps.

FROZEN BARS (identical thresholds to cheap — tune-to-green FORBIDDEN, p7/c9):
  chance(compositional) = 1/(K1*K2)
  BAR-1 binding/retrieval@1 : M3 InfoNCE held-out compositional acc >= 0.50
  BAR-2 objective is G1 lever: (M3 - M1 CE-marginal) >= 0.20 AND M3 >= 0.50
  BAR-3 interaction-ablation: (M3 - M4 additive-floor) >= 0.30
  BAR-4 verbatim control    : M3 prefers true future over verbatim distractor
                              on >= 0.80 of held-out pairs
  DISCRIM-CTRL sanity       : M1 train acc >= 0.95 AND M1 held < 0.50
  VERDICT(DIRECTIONAL): SUPPORT = all of BAR1..4 ; NOT = BAR-2 fails ; else MIXED
  Multi-seed mean across seeds.
==============================================================================
"""
import numpy as np, time

# ---- mid-rung scale (vs cheap: P 7->13, embed/H/D up, steps up) ----
P = 13                                  # modulus (Z_P*): 12 nonzero residues
VALS = list(range(1, P))
PAIRS = [(a, b) for a in VALS for b in VALS]    # 144 pairs
K1, K2 = P - 1, P                       # y1∈{1..P-1}->P-1 cls, y2∈{0..P-1}->P cls
NCOMBO = K1 * K2
EMB = 32                                 # shared per-symbol embedding dim (NEW)
H, D = 256, 96                           # hidden / latent (up from 128/48)
STEPS = 60000
LR, WD = 1e-3, 0.05
B1, B2, EPS = 0.9, 0.999, 1e-8
HELD_FRAC = 0.25
NEG_K = 40
EVAL_EVERY = 3000
SEEDS = [7, 4302, 4303, 11, 23]

COMBOS = [(c1, c2) for c1 in range(K1) for c2 in range(K2)]
C1 = np.array([c[0] for c in COMBOS]); C2 = np.array([c[1] for c in COMBOS])

def fut(a, b): return ((a * b) % P - 1, (a + b) % P)
def cidx(c1, c2): return c1 * K2 + c2
def smrow(L):
    L = L - L.max(1, keepdims=True); e = np.exp(L); return e / e.sum(1, keepdims=True)

class Adam:
    def __init__(self, params):
        self.m = {k: np.zeros_like(v) for k, v in params.items()}
        self.v = {k: np.zeros_like(v) for k, v in params.items()}; self.t = 0
    def step(self, params, grads):
        self.t += 1
        for k in params:
            g = grads[k]
            self.m[k] = B1 * self.m[k] + (1 - B1) * g
            self.v[k] = B2 * self.v[k] + (1 - B2) * g * g
            mh = self.m[k] / (1 - B1 ** self.t); vh = self.v[k] / (1 - B2 ** self.t)
            params[k] -= LR * (mh / (np.sqrt(vh) + EPS) + WD * params[k])

# ---- shared-embedding encoder: z = MLP([E[a-1], E[b-1]]) ----
def enc_init(rng):
    return {'Ea': rng.normal(0, 1/np.sqrt(EMB), (P-1, EMB)),
            'Eb': rng.normal(0, 1/np.sqrt(EMB), (P-1, EMB)),
            'W1': rng.normal(0, 1/np.sqrt(2*EMB), (H, 2*EMB)), 'b1': np.zeros(H),
            'W2': rng.normal(0, 1/np.sqrt(H), (D, H)), 'b2': np.zeros(D)}

def enc_fwd(p, ai, bi):
    X = np.concatenate([p['Ea'][ai], p['Eb'][bi]], axis=1)   # N x 2EMB
    PRE = X @ p['W1'].T + p['b1']; Hh = np.tanh(PRE); Z = Hh @ p['W2'].T + p['b2']
    return Z, Hh, X

def enc_bwd(p, g, ai, bi, X, Hh, dZ):
    g['W2'] = dZ.T @ Hh; g['b2'] = dZ.sum(0)
    dHh = dZ @ p['W2']; dPRE = dHh * (1 - Hh * Hh)
    g['W1'] = dPRE.T @ X; g['b1'] = dPRE.sum(0)
    dX = dPRE @ p['W1']                                      # N x 2EMB
    g['Ea'] = np.zeros_like(p['Ea']); g['Eb'] = np.zeros_like(p['Eb'])
    np.add.at(g['Ea'], ai, dX[:, :EMB]); np.add.at(g['Eb'], bi, dX[:, EMB:])

def run_seed(seed):
    rng = np.random.default_rng(seed)
    pairs = PAIRS[:]; rng.shuffle(pairs)
    nh = int(round(HELD_FRAC * len(pairs)))
    held, train = pairs[:nh], pairs[nh:]
    ai = np.array([a-1 for (a,b) in train]); bi = np.array([b-1 for (a,b) in train])
    aih = np.array([a-1 for (a,b) in held]); bih = np.array([b-1 for (a,b) in held])
    Ytr = [fut(*p) for p in train]; Yhe = [fut(*p) for p in held]
    t1 = np.array([y[0] for y in Ytr]); t2 = np.array([y[1] for y in Ytr])
    tc_tr = np.array([cidx(*y) for y in Ytr]); tc_he = np.array([cidx(*y) for y in Yhe])
    he1 = np.array([y[0] for y in Yhe]); he2 = np.array([y[1] for y in Yhe])
    N = len(train)
    def recall(pb):
        a, b = pb; tr = fut(a, b)
        cands = [fut(a, bb) for (aa, bb) in train if aa == a and fut(a, bb) != tr]
        if not cands: cands = [fut(*q) for q in train if fut(*q) != tr]
        return cidx(*cands[0])
    rec_he = np.array([recall(pb) for pb in held])
    out = {}

    # ---- M1 CE-marginal (two independent heads) ----
    p = enc_init(rng); p['Hy1'] = rng.normal(0, 1/np.sqrt(D), (K1, D)); p['Hy2'] = rng.normal(0, 1/np.sqrt(D), (K2, D))
    opt = Adam(p); best = 0.0; tr_at_best = 0.0
    for st in range(STEPS):
        Z, Hh, X = enc_fwd(p, ai, bi)
        Pp1 = smrow(Z @ p['Hy1'].T); Pp2 = smrow(Z @ p['Hy2'].T)
        DA = Pp1.copy(); DA[np.arange(N), t1] -= 1; DA /= N
        DB = Pp2.copy(); DB[np.arange(N), t2] -= 1; DB /= N
        g = {}; g['Hy1'] = DA.T @ Z; g['Hy2'] = DB.T @ Z
        dZ = DA @ p['Hy1'] + DB @ p['Hy2']; enc_bwd(p, g, ai, bi, X, Hh, dZ)
        opt.step(p, g)
        if st % EVAL_EVERY == 0 or st == STEPS - 1:
            Zh, _, _ = enc_fwd(p, aih, bih)
            acc = np.mean((np.argmax(Zh @ p['Hy1'].T, 1) == he1) & (np.argmax(Zh @ p['Hy2'].T, 1) == he2))
            Zt, _, _ = enc_fwd(p, ai, bi)
            tacc = np.mean((np.argmax(Zt @ p['Hy1'].T, 1) == t1) & (np.argmax(Zt @ p['Hy2'].T, 1) == t2))
            if acc >= best: best = acc; tr_at_best = tacc
    out['M1_held'] = best; out['M1_train'] = tr_at_best

    # ---- joint trainer (M2 CE-joint / M3 InfoNCE) ----
    def joint(infonce):
        p = enc_init(rng); p['Fa'] = rng.normal(0, 1/np.sqrt(D), (K1, D)); p['Fb'] = rng.normal(0, 1/np.sqrt(D), (K2, D))
        opt = Adam(p); best = 0.0; best_vb = 0.0
        for st in range(STEPS):
            Z, Hh, X = enc_fwd(p, ai, bi)
            KEY = p['Fa'][C1] + p['Fb'][C2]; L = Z @ KEY.T
            if infonce:
                mask = np.zeros((N, NCOMBO), bool); mask[np.arange(N), tc_tr] = True
                for i in range(N):
                    mask[i, rng.choice(NCOMBO, NEG_K, replace=False)] = True
                for i in range(N):
                    a, b = train[i]; tr = fut(a, b)
                    cs = [fut(a, bb) for (aa, bb) in train if aa == a and fut(a, bb) != tr]
                    if cs: mask[i, cidx(*cs[0])] = True
                Lm = np.where(mask, L, -1e9); Pp = smrow(Lm)
            else:
                Pp = smrow(L)
            DL = Pp.copy(); DL[np.arange(N), tc_tr] -= 1; DL /= N
            g = {}; g['Fa'] = np.zeros_like(p['Fa']); g['Fb'] = np.zeros_like(p['Fb'])
            gKEY = DL.T @ Z; np.add.at(g['Fa'], C1, gKEY); np.add.at(g['Fb'], C2, gKEY)
            dZ = DL @ KEY; enc_bwd(p, g, ai, bi, X, Hh, dZ)
            opt.step(p, g)
            if st % EVAL_EVERY == 0 or st == STEPS - 1:
                Zh, _, _ = enc_fwd(p, aih, bih)
                KEYe = p['Fa'][C1] + p['Fb'][C2]; sc = Zh @ KEYe.T
                acc = np.mean(np.argmax(sc, 1) == tc_he)
                s_true = sc[np.arange(len(held)), tc_he]; s_vb = sc[np.arange(len(held)), rec_he]
                vb = float(np.mean(s_true > s_vb))
                if acc >= best: best = acc; best_vb = vb
        return best, best_vb
    out['M2_held'], _ = joint(False)
    out['M3_held'], out['M3_verbatim_win'] = joint(True)

    # ---- M4 additive-floor (no nonlinear joint) + InfoNCE ----
    p = {'Ea': rng.normal(0, 1/np.sqrt(EMB), (P-1, EMB)), 'Eb': rng.normal(0, 1/np.sqrt(EMB), (P-1, EMB)),
         'Wa': rng.normal(0, 1/np.sqrt(EMB), (D, EMB)), 'Wb': rng.normal(0, 1/np.sqrt(EMB), (D, EMB)),
         'Fa': rng.normal(0, 1/np.sqrt(D), (K1, D)), 'Fb': rng.normal(0, 1/np.sqrt(D), (K2, D))}
    opt = Adam(p); best = 0.0
    for st in range(STEPS):
        Z = p['Ea'][ai] @ p['Wa'].T + p['Eb'][bi] @ p['Wb'].T    # NxD purely additive
        KEY = p['Fa'][C1] + p['Fb'][C2]; L = Z @ KEY.T
        mask = np.zeros((N, NCOMBO), bool); mask[np.arange(N), tc_tr] = True
        for i in range(N): mask[i, rng.choice(NCOMBO, NEG_K, replace=False)] = True
        Lm = np.where(mask, L, -1e9); Pp = smrow(Lm)
        DL = Pp.copy(); DL[np.arange(N), tc_tr] -= 1; DL /= N
        g = {k: np.zeros_like(v) for k, v in p.items()}
        gKEY = DL.T @ Z; np.add.at(g['Fa'], C1, gKEY); np.add.at(g['Fb'], C2, gKEY)
        dZ = DL @ KEY
        g['Wa'] = dZ.T @ p['Ea'][ai]; g['Wb'] = dZ.T @ p['Eb'][bi]
        np.add.at(g['Ea'], ai, dZ @ p['Wa']); np.add.at(g['Eb'], bi, dZ @ p['Wb'])
        opt.step(p, g)
        if st % EVAL_EVERY == 0 or st == STEPS - 1:
            Zh = p['Ea'][aih] @ p['Wa'].T + p['Eb'][bih] @ p['Wb'].T
            KEYe = p['Fa'][C1] + p['Fb'][C2]
            acc = np.mean(np.argmax(Zh @ KEYe.T, 1) == tc_he); best = max(best, acc)
    out['M4_held'] = best
    return out

def grokkability_control(seed=7):
    """single-head modular ADDITION WITH A SHARED EMBEDDING table (grokking inductive bias)."""
    Pm = 23; vals = list(range(Pm)); prs = [(a, b) for a in vals for b in vals]
    Em, Hm, Dm = 32, 256, 96
    rng = np.random.default_rng(seed); rng.shuffle(prs)
    nh = len(prs) // 2; held, train = prs[:nh], prs[nh:]
    ai = np.array([a for (a,b) in train]); bi = np.array([b for (a,b) in train])
    aih = np.array([a for (a,b) in held]); bih = np.array([b for (a,b) in held])
    ytr = np.array([(a+b) % Pm for (a,b) in train]); yhe = np.array([(a+b) % Pm for (a,b) in held])
    N = len(train)
    p = {'E': rng.normal(0, 1/np.sqrt(Em), (Pm, Em)),
         'W1': rng.normal(0, 1/np.sqrt(2*Em), (Hm, 2*Em)), 'b1': np.zeros(Hm),
         'W2': rng.normal(0, 1/np.sqrt(Hm), (Dm, Hm)), 'b2': np.zeros(Dm),
         'Hd': rng.normal(0, 1/np.sqrt(Dm), (Pm, Dm))}
    opt = Adam(p); best = 0.0
    for st in range(60000):
        X = np.concatenate([p['E'][ai], p['E'][bi]], axis=1)
        PRE = X @ p['W1'].T + p['b1']; Hh = np.tanh(PRE); Z = Hh @ p['W2'].T + p['b2']
        Pp = smrow(Z @ p['Hd'].T); DL = Pp.copy(); DL[np.arange(N), ytr] -= 1; DL /= N
        g = {}; g['Hd'] = DL.T @ Z; dZ = DL @ p['Hd']
        g['W2'] = dZ.T @ Hh; g['b2'] = dZ.sum(0); dHh = dZ @ p['W2']; dPRE = dHh * (1 - Hh*Hh)
        g['W1'] = dPRE.T @ X; g['b1'] = dPRE.sum(0); dX = dPRE @ p['W1']
        g['E'] = np.zeros_like(p['E']); np.add.at(g['E'], ai, dX[:, :Em]); np.add.at(g['E'], bi, dX[:, Em:])
        opt.step(p, g)
        if st % 6000 == 0 or st == 59999:
            Xh = np.concatenate([p['E'][aih], p['E'][bih]], axis=1)
            Zh = np.tanh(Xh @ p['W1'].T + p['b1']) @ p['W2'].T + p['b2']
            best = max(best, np.mean(np.argmax(Zh @ p['Hd'].T, 1) == yhe))
    return float(best), 1.0/Pm

def main():
    t0 = time.time()
    chance = 1.0 / NCOMBO
    print("=" * 84)
    print("H_1792 SCALE-UP — InfoNCE objective as G1 lever (mid-rung, numpy AdamW, DIRECTIONAL)")
    print(f"task: Z_{P}* factored y1=(a*b)%{P} y2=(a+b)%{P} | {len(PAIRS)} pairs, held {HELD_FRAC:.0%}")
    print(f"ARCH: shared per-symbol EMBEDDING(dim={EMB}) -> MLP(H={H},D={D}); ONLY objective differs")
    print(f"compositional chance = 1/{NCOMBO} = {chance:.4f} | steps={STEPS} AdamW lr={LR} wd={WD} seeds={SEEDS}")
    print("=" * 84)
    # ---- RESOLUTION GATE FIRST ----
    grok, gch = grokkability_control()
    grok_pass = grok >= 0.80
    print(f"[RESOLUTION GATE] grok-ctrl modular-ADD (shared embedding, mod 23, 50% held): held={grok:.3f} (chance={gch:.3f})")
    print(f"  -> grok PASS (>=0.80)? {grok_pass}  {'[resolution acquired]' if grok_pass else '[STILL under-powered -> next rung]'}")
    print("-" * 84)
    keys = ['M1_train','M1_held','M2_held','M3_held','M3_verbatim_win','M4_held']
    agg = {k: [] for k in keys}
    for s in SEEDS:
        r = run_seed(s)
        for k in keys: agg[k].append(r[k])
        print(f"seed {s:>5}: M1(CEmarg) tr={r['M1_train']:.2f} he={r['M1_held']:.2f} | "
              f"M2(CEjoint) he={r['M2_held']:.2f} | M3(InfoNCE) he={r['M3_held']:.2f} vb={r['M3_verbatim_win']:.2f} | "
              f"M4(addfloor) he={r['M4_held']:.2f}")
    m = {k: float(np.mean(v)) for k, v in agg.items()}
    print("-" * 84)
    print("MEANS across seeds (BEST held-out over run):")
    print(f"  M1 CE-marginal : train={m['M1_train']:.3f}  held={m['M1_held']:.3f}")
    print(f"  M2 CE-joint    : held={m['M2_held']:.3f}")
    print(f"  M3 InfoNCE     : held={m['M3_held']:.3f}  verbatim_win={m['M3_verbatim_win']:.3f}")
    print(f"  M4 add-floor   : held={m['M4_held']:.3f}")
    print("-" * 84)
    bar1 = m['M3_held'] >= 0.50
    bar2 = (m['M3_held'] - m['M1_held'] >= 0.20) and (m['M3_held'] >= 0.50)
    bar3 = (m['M3_held'] - m['M4_held'] >= 0.30)
    bar4 = m['M3_verbatim_win'] >= 0.80
    discrim = (m['M1_train'] >= 0.95) and (m['M1_held'] < 0.50)
    print("FROZEN BARS (identical to cheap):")
    print(f"  BAR-1 binding/retrieval@1  M3_held>=0.50            : {m['M3_held']:.3f}  -> {'PASS' if bar1 else 'FAIL'}")
    print(f"  BAR-2 objective=G1 lever   (M3-M1)>=0.20 & M3>=0.50 : d={m['M3_held']-m['M1_held']:+.3f} -> {'PASS' if bar2 else 'FAIL'}")
    print(f"  BAR-3 interaction-ablation (M3-M4floor)>=0.30       : d={m['M3_held']-m['M4_held']:+.3f} -> {'PASS' if bar3 else 'FAIL'}")
    print(f"  BAR-4 verbatim control     M3 vb_win>=0.80          : {m['M3_verbatim_win']:.3f}  -> {'PASS' if bar4 else 'FAIL'}")
    print(f"  DISCRIM-CTRL  M1 tr>=0.95 & M1 held<0.50            : tr={m['M1_train']:.2f} he={m['M1_held']:.2f} -> {'PASS' if discrim else 'FAIL'}")
    print("-" * 84)
    if not grok_pass:
        verdict = "UNDER-POWERED (resolution gate FAIL — next rung needed, bars NOT binding)"
    elif bar1 and bar2 and bar3 and bar4:
        verdict = "SUPPORT (DIRECTIONAL)"
    elif not bar2:
        verdict = "NOT (DIRECTIONAL)"
    else:
        verdict = "MIXED (DIRECTIONAL)"
    print(f"VERDICT: {verdict}")
    print(f"  [this mid-rung = PREDICTION for 303M objrun H_1602; terminal = engine-native 303M]")
    print(f"  numpy toy = DIRECTIONAL only (a_engine_native_learning). elapsed={time.time()-t0:.0f}s")
    print("=" * 84)

if __name__ == "__main__":
    main()
