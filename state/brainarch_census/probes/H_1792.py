#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
H_1792 — Contrastive Predictive Future Latent (InfoNCE objective as G1 lever)
============================================================================
cheap_test ($0, numpy toy, mini-safe, CPU ~minutes) — DIRECTIONAL ONLY.

  ⚠️ MEASUREMENT PATH: numpy toy = DIRECTIONAL (NOT engine-native, a_engine_native_learning).
     The verdict is DIRECTIONAL regardless of pass/fail. Engine-native (cli/anima.hexa →
     generator L3 → g_gates/g6 g6_score_arm_auto) + 303M GPU = cost-gated PRE-REGISTER
     ONLY (NOT fired). numpy cheap_test cannot stamp 🟢/🧱.

CLAIM UNDER TEST (card + g1-lever-multilens-objective memory):
  The recombination/G1 lever is the TRUNK OBJECTIVE, not depth/data/scale.
  Plain next-byte CE rewards predicting the *marginal* next symbol and never the
  JOINT (conjunction) of two concepts. A contrastive predictive (InfoNCE) objective
  is "marginal-unsatisfiable" by construction: to score the true joint continuation
  above shuffled + verbatim distractors you MUST represent the conjunction → it
  should produce held-out composition where CE cannot. DISCRIMINATING CONTROL:
  a CE-marginal baseline clears likelihood (memorizes train) yet FAILS strict G1.

TOY TASK (binding-required / "ambiguous subset" BY CONSTRUCTION — precedent SCREEN_multiply_vs_add):
  factored inputs a,b ∈ Z_7* = {1..6}; 36 (a,b) pairs.  future = factored pair (y1,y2):
      y1 = (a*b) mod 7  (multiplicative, NON-separable / requires joint)
      y2 = (a+b) mod 7  (additive)
  MARGINALS CARRY ~ZERO INFO: a invertible in Z_7* ⇒ for fixed a, (a*b) ranges over all
  of {1..6} as b varies ⇒ P(y1|a),P(y1|b),P(y2|a),P(y2|b) all UNIFORM. The WHOLE set is
  the ambiguous/binding-required subset — there is NO marginal shortcut (cannot be inflated
  by full-set stats). Both rules FIXED ⇒ held-out combos are determined ⇒ generalization is
  meaningful (not a random Latin square). G1 recombination = generalize to combos never co-presented.

SPLIT: hold out 25% of 36 pairs (9) as NOVEL COMBINATIONS. train on 27, test on the 9 held-out.

MODELS (SAME context encoder z = MLP(onehot_a,onehot_b); ONLY the objective differs — isolate
        OBJECTIVE as lever, arch fixed, a_no_llm_frame_trap). Optimizer = AdamW (decoupled wd),
        the grokking-capable optimizer; evaluate bars on BEST held-out over the run (generous to
        the hypothesis → guards against an under-powered false NEGATIVE):
  M1 CE-marginal : two INDEPENDENT softmax heads predict y1,y2 separately = "predict the marginal
                   next symbol" CE baseline (DISCRIMINATING CONTROL).
  M2 CE-joint    : single softmax over K1*K2 composed combos (factored keys key[c]=Fa[c1]+Fb[c2]);
                   JOINT output, CE loss (isolates joint-output vs contrastive).
  M3 InfoNCE     : composed factor keys + CONTRASTIVE sampled negatives (shuffled futures) + a
                   VERBATIM hard negative (memorized recall combo). THE PROPOSED OBJECTIVE.
  M4 add-floor   : ADDITIVE (interaction-ablated) encoder z=Wa@oh_a+Wb@oh_b (no nonlinear joint),
                   InfoNCE objective → the SEPARABLE FLOOR (interaction-ablation control).

GROKKABILITY CONTROL: a single-head modular-ADDITION run (the canonical grokkable task) under the
  SAME toy → documents whether this $0 numpy MLP can grok held-out generalization AT ALL. If it
  cannot, the recombination axis of the cheap_test is UNDER-POWERED (scope caveat, a_break_the_wall
  type-a: measurement limit, NOT a science ceiling) and the negative is qualified accordingly.

==============================================================================
FROZEN BARS  (pre-registered BEFORE running — frozen-first, tune-to-green FORBIDDEN p7/c9)
==============================================================================
  chance (compositional, both factors correct) = 1 / (K1*K2) = 1/42 ~= 0.0238

  BAR-1  binding / retrieval@1 : M3 held-out compositional acc (retrieval@1 over 42 combos) >= 0.50
  BAR-2  objective is G1 lever : (M3 held-out acc - M1 CE-marginal held-out acc) >= 0.20
                                 AND M3 held-out acc >= 0.50
  BAR-3  interaction-ablation : (M3 held-out acc - M4 additive-floor held-out acc) >= 0.30
  BAR-4  verbatim control     : M3 prefers TRUE compositional future over the verbatim-recall
                                 distractor on >= 0.80 of held-out pairs
  DISCRIM-CONTROL sanity      : M1 CE-marginal TRAIN acc >= 0.95 ("clears likelihood")
                                 AND M1 held-out acc < 0.50 (CE memorizes yet FAILS G1)

  VERDICT (DIRECTIONAL):
    SUPPORT  = BAR-1 & BAR-2 & BAR-3 & BAR-4 all pass
    NOT      = BAR-2 fails (InfoNCE not a meaningful lever over CE-marginal)
    MIXED    = otherwise (some pass, some fail)
  Multi-seed (5 seeds); judge on the MEAN across seeds (multi-seed lesson, anti sampler-artifact).
==============================================================================
"""
import numpy as np

P = 7
VALS = list(range(1, P))
PAIRS = [(a, b) for a in VALS for b in VALS]            # 36
K1, K2 = P - 1, P                                       # y1∈{1..6}->6cls, y2∈{0..6}->7cls
NCOMBO = K1 * K2                                        # 42
IN = 2 * (P - 1)                                        # onehot a(6)+b(6)=12
H, D = 128, 48
STEPS = 40000
LR, WD = 1e-3, 0.05
B1, B2, EPS = 0.9, 0.999, 1e-8
HELD_FRAC = 0.25
NEG_K = 20
EVAL_EVERY = 2000
SEEDS = [7, 4302, 4303, 11, 23]

COMBOS = [(c1, c2) for c1 in range(K1) for c2 in range(K2)]
C1 = np.array([c[0] for c in COMBOS])
C2 = np.array([c[1] for c in COMBOS])

def fut(a, b):
    return ((a * b) % P - 1, (a + b) % P)

def cidx(c1, c2):
    return c1 * K2 + c2

def oh(a, b):
    x = np.zeros(IN); x[a - 1] = 1.0; x[(P - 1) + (b - 1)] = 1.0; return x

def smrow(L):
    L = L - L.max(1, keepdims=True); e = np.exp(L); return e / e.sum(1, keepdims=True)

# ---------- AdamW ----------
class Adam:
    def __init__(self, params):
        self.m = {k: np.zeros_like(v) for k, v in params.items()}
        self.v = {k: np.zeros_like(v) for k, v in params.items()}
        self.t = 0
    def step(self, params, grads):
        self.t += 1
        for k in params:
            g = grads[k]
            self.m[k] = B1 * self.m[k] + (1 - B1) * g
            self.v[k] = B2 * self.v[k] + (1 - B2) * g * g
            mh = self.m[k] / (1 - B1 ** self.t)
            vh = self.v[k] / (1 - B2 ** self.t)
            params[k] -= LR * (mh / (np.sqrt(vh) + EPS) + WD * params[k])  # decoupled wd

def enc_init(rng):
    return {'W1': rng.normal(0, 1/np.sqrt(IN), (H, IN)), 'b1': np.zeros(H),
            'W2': rng.normal(0, 1/np.sqrt(H), (D, H)), 'b2': np.zeros(D)}

def enc_fwd(p, X):
    PRE = X @ p['W1'].T + p['b1']; Hh = np.tanh(PRE); Z = Hh @ p['W2'].T + p['b2']
    return Z, Hh

def enc_bwd(p, g, X, Hh, dZ):
    g['W2'] = dZ.T @ Hh; g['b2'] = dZ.sum(0)
    dHh = dZ @ p['W2']; dPRE = dHh * (1 - Hh * Hh)
    g['W1'] = dPRE.T @ X; g['b1'] = dPRE.sum(0)

def run_seed(seed):
    rng = np.random.default_rng(seed)
    pairs = PAIRS[:]; rng.shuffle(pairs)
    nh = int(round(HELD_FRAC * len(pairs)))
    held, train = pairs[:nh], pairs[nh:]
    Xtr = np.stack([oh(*p) for p in train]); Xhe = np.stack([oh(*p) for p in held])
    Ytr = [fut(*p) for p in train]; Yhe = [fut(*p) for p in held]
    t1 = np.array([y[0] for y in Ytr]); t2 = np.array([y[1] for y in Ytr])
    tc_tr = np.array([cidx(*y) for y in Ytr]); tc_he = np.array([cidx(*y) for y in Yhe])
    he1 = np.array([y[0] for y in Yhe]); he2 = np.array([y[1] for y in Yhe])
    N = len(train)
    # verbatim-recall combo per HELD pair: future of a train pair sharing factor a, != true
    def recall(pb):
        a, b = pb; tr = fut(a, b)
        cands = [fut(a, bb) for (aa, bb) in train if aa == a and fut(a, bb) != tr]
        if not cands: cands = [fut(*q) for q in train if fut(*q) != tr]
        return cidx(*cands[0])
    rec_he = np.array([recall(pb) for pb in held])
    out = {}

    # ---------- M1 CE-marginal ----------
    p = enc_init(rng); p['Hy1'] = rng.normal(0, 1/np.sqrt(D), (K1, D)); p['Hy2'] = rng.normal(0, 1/np.sqrt(D), (K2, D))
    opt = Adam(p); best = 0.0; tr_at_best = 0.0
    for st in range(STEPS):
        Z, Hh = enc_fwd(p, Xtr)
        Pp1 = smrow(Z @ p['Hy1'].T); Pp2 = smrow(Z @ p['Hy2'].T)
        DA = Pp1.copy(); DA[np.arange(N), t1] -= 1; DA /= N
        DB = Pp2.copy(); DB[np.arange(N), t2] -= 1; DB /= N
        g = {}; g['Hy1'] = DA.T @ Z; g['Hy2'] = DB.T @ Z
        dZ = DA @ p['Hy1'] + DB @ p['Hy2']; enc_bwd(p, g, Xtr, Hh, dZ)
        opt.step(p, g)
        if st % EVAL_EVERY == 0 or st == STEPS - 1:
            Zh, _ = enc_fwd(p, Xhe)
            acc = np.mean((np.argmax(Zh @ p['Hy1'].T, 1) == he1) & (np.argmax(Zh @ p['Hy2'].T, 1) == he2))
            Zt, _ = enc_fwd(p, Xtr)
            tacc = np.mean((np.argmax(Zt @ p['Hy1'].T, 1) == t1) & (np.argmax(Zt @ p['Hy2'].T, 1) == t2))
            if acc >= best: best = acc; tr_at_best = tacc
    out['M1_held'] = best; out['M1_train'] = tr_at_best

    # ---------- joint trainer (M2 CE-joint / M3 InfoNCE) ----------
    def joint(infonce):
        p = enc_init(rng); p['Fa'] = rng.normal(0, 1/np.sqrt(D), (K1, D)); p['Fb'] = rng.normal(0, 1/np.sqrt(D), (K2, D))
        opt = Adam(p); best = 0.0; best_vb = 0.0
        for st in range(STEPS):
            Z, Hh = enc_fwd(p, Xtr)
            KEY = p['Fa'][C1] + p['Fb'][C2]            # 42xD
            L = Z @ KEY.T                              # Nx42
            if infonce:
                mask = np.zeros((N, NCOMBO), bool); mask[np.arange(N), tc_tr] = True
                for i in range(N):
                    mask[i, rng.choice(NCOMBO, NEG_K, replace=False)] = True
                    mask[i, recall(train[i]) if False else tc_tr[i]] = True  # pos guaranteed
                # add a verbatim hard-neg per train example (recall of a same-a train pair)
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
            dZ = DL @ KEY; enc_bwd(p, g, Xtr, Hh, dZ)
            opt.step(p, g)
            if st % EVAL_EVERY == 0 or st == STEPS - 1:
                Zh, _ = enc_fwd(p, Xhe)
                KEYe = p['Fa'][C1] + p['Fb'][C2]
                sc = Zh @ KEYe.T
                acc = np.mean(np.argmax(sc, 1) == tc_he)
                # verbatim control on held: score(true) > score(recall)
                s_true = sc[np.arange(len(held)), tc_he]; s_vb = sc[np.arange(len(held)), rec_he]
                vb = float(np.mean(s_true > s_vb))
                if acc >= best: best = acc; best_vb = vb
        return best, best_vb

    out['M2_held'], _ = joint(False)
    out['M3_held'], out['M3_verbatim_win'] = joint(True)

    # ---------- M4 additive-floor + InfoNCE ----------
    p = {'Wa': rng.normal(0, 1/np.sqrt(P-1), (D, P-1)), 'Wb': rng.normal(0, 1/np.sqrt(P-1), (D, P-1)),
         'Fa': rng.normal(0, 1/np.sqrt(D), (K1, D)), 'Fb': rng.normal(0, 1/np.sqrt(D), (K2, D))}
    ai = np.array([a - 1 for (a, b) in train]); bi = np.array([b - 1 for (a, b) in train])
    aih = np.array([a - 1 for (a, b) in held]); bih = np.array([b - 1 for (a, b) in held])
    opt = Adam(p); best = 0.0
    for st in range(STEPS):
        Z = p['Wa'][:, ai].T + p['Wb'][:, bi].T        # NxD
        KEY = p['Fa'][C1] + p['Fb'][C2]; L = Z @ KEY.T
        mask = np.zeros((N, NCOMBO), bool); mask[np.arange(N), tc_tr] = True
        for i in range(N):
            mask[i, rng.choice(NCOMBO, NEG_K, replace=False)] = True
        Lm = np.where(mask, L, -1e9); Pp = smrow(Lm)
        DL = Pp.copy(); DL[np.arange(N), tc_tr] -= 1; DL /= N
        g = {k: np.zeros_like(v) for k, v in p.items()}
        gKEY = DL.T @ Z; np.add.at(g['Fa'], C1, gKEY); np.add.at(g['Fb'], C2, gKEY)
        dZ = DL @ KEY
        np.add.at(g['Wa'].T, ai, dZ); np.add.at(g['Wb'].T, bi, dZ)
        opt.step(p, g)
        if st % EVAL_EVERY == 0 or st == STEPS - 1:
            Zh = p['Wa'][:, aih].T + p['Wb'][:, bih].T
            KEYe = p['Fa'][C1] + p['Fb'][C2]
            acc = np.mean(np.argmax(Zh @ KEYe.T, 1) == tc_he)
            best = max(best, acc)
    out['M4_held'] = best
    return out

def grokkability_control(seed=7):
    """single-head modular ADDITION (canonical grokkable task), AdamW — can this toy grok AT ALL?"""
    Pm = 11; vals = list(range(Pm)); prs = [(a, b) for a in vals for b in vals]
    IN2 = 2 * Pm; H2, D2 = 256, 64
    rng = np.random.default_rng(seed); rng.shuffle(prs)
    nh = len(prs) // 2; held, train = prs[:nh], prs[nh:]
    def oh2(a, b):
        x = np.zeros(IN2); x[a] = 1; x[Pm + b] = 1; return x
    Xtr = np.stack([oh2(*p) for p in train]); Xhe = np.stack([oh2(*p) for p in held])
    ytr = np.array([(a + b) % Pm for (a, b) in train]); yhe = np.array([(a + b) % Pm for (a, b) in held])
    N = len(train)
    p = {'W1': rng.normal(0, 1/np.sqrt(IN2), (H2, IN2)), 'b1': np.zeros(H2),
         'W2': rng.normal(0, 1/np.sqrt(H2), (D2, H2)), 'b2': np.zeros(D2),
         'Hd': rng.normal(0, 1/np.sqrt(D2), (Pm, D2))}
    opt = Adam(p); best = 0.0
    for st in range(40000):
        PRE = Xtr @ p['W1'].T + p['b1']; Hh = np.tanh(PRE); Z = Hh @ p['W2'].T + p['b2']
        Pp = smrow(Z @ p['Hd'].T); DL = Pp.copy(); DL[np.arange(N), ytr] -= 1; DL /= N
        g = {}; g['Hd'] = DL.T @ Z; dZ = DL @ p['Hd']
        g['W2'] = dZ.T @ Hh; g['b2'] = dZ.sum(0); dHh = dZ @ p['W2']; dPRE = dHh * (1 - Hh * Hh)
        g['W1'] = dPRE.T @ Xtr; g['b1'] = dPRE.sum(0)
        opt.step(p, g)
        if st % 8000 == 0 or st == 39999:
            Zh = np.tanh(Xhe @ p['W1'].T + p['b1']) @ p['W2'].T + p['b2']
            best = max(best, np.mean(np.argmax(Zh @ p['Hd'].T, 1) == yhe))
    return float(best)

def main():
    chance = 1.0 / NCOMBO
    print("=" * 80)
    print("H_1792 contrastive_predictive_future_latent — cheap_test (numpy AdamW, DIRECTIONAL)")
    print(f"task: Z_7* factored y1=(a*b)%7 y2=(a+b)%7 | 36 pairs, held {HELD_FRAC:.0%} novel combos")
    print(f"binding-required: P(y|a),P(y|b) UNIFORM (whole set = ambiguous subset, no marginal shortcut)")
    print(f"compositional chance = 1/{NCOMBO} = {chance:.4f} | steps={STEPS} AdamW lr={LR} wd={WD} seeds={SEEDS}")
    print("bars judged on BEST held-out over run (generous → guards under-powered false-negative)")
    print("=" * 80)
    keys = ['M1_train','M1_held','M2_held','M3_held','M3_verbatim_win','M4_held']
    agg = {k: [] for k in keys}
    for s in SEEDS:
        r = run_seed(s)
        for k in keys: agg[k].append(r[k])
        print(f"seed {s:>5}: M1(CEmarg) tr={r['M1_train']:.2f} he={r['M1_held']:.2f} | "
              f"M2(CEjoint) he={r['M2_held']:.2f} | M3(InfoNCE) he={r['M3_held']:.2f} vb={r['M3_verbatim_win']:.2f} | "
              f"M4(addfloor) he={r['M4_held']:.2f}")
    m = {k: float(np.mean(v)) for k, v in agg.items()}
    print("-" * 80)
    grok = grokkability_control()
    print(f"GROKKABILITY CONTROL (single-head modular ADDITION, AdamW 40k, 50% held): best held-out = {grok:.3f}")
    print(f"  -> if ~chance(=1/11={1/11:.3f}): this $0 numpy MLP CANNOT grok held-out generalization for ANY")
    print(f"     objective (lacks shared-embedding inductive bias) => recombination axis UNDER-POWERED (scope).")
    print("-" * 80)
    print("MEANS across seeds (BEST held-out over run):")
    print(f"  M1 CE-marginal : train={m['M1_train']:.3f}  held={m['M1_held']:.3f}")
    print(f"  M2 CE-joint    : held={m['M2_held']:.3f}")
    print(f"  M3 InfoNCE     : held={m['M3_held']:.3f}  verbatim_win={m['M3_verbatim_win']:.3f}")
    print(f"  M4 add-floor   : held={m['M4_held']:.3f}")
    print("-" * 80)
    bar1 = m['M3_held'] >= 0.50
    bar2 = (m['M3_held'] - m['M1_held'] >= 0.20) and (m['M3_held'] >= 0.50)
    bar3 = (m['M3_held'] - m['M4_held'] >= 0.30)
    bar4 = m['M3_verbatim_win'] >= 0.80
    discrim = (m['M1_train'] >= 0.95) and (m['M1_held'] < 0.50)
    print("FROZEN BARS:")
    print(f"  BAR-1 binding/retrieval@1  M3_held>=0.50            : {m['M3_held']:.3f}  -> {'PASS' if bar1 else 'FAIL'}")
    print(f"  BAR-2 objective=G1 lever   (M3-M1)>=0.20 & M3>=0.50 : d={m['M3_held']-m['M1_held']:+.3f} -> {'PASS' if bar2 else 'FAIL'}")
    print(f"  BAR-3 interaction-ablation (M3-M4floor)>=0.30       : d={m['M3_held']-m['M4_held']:+.3f} -> {'PASS' if bar3 else 'FAIL'}")
    print(f"  BAR-4 verbatim control     M3 vb_win>=0.80          : {m['M3_verbatim_win']:.3f}  -> {'PASS' if bar4 else 'FAIL'}")
    print(f"  DISCRIM-CTRL  M1 tr>=0.95 & M1 held<0.50            : tr={m['M1_train']:.2f} he={m['M1_held']:.2f} -> {'PASS' if discrim else 'FAIL'}")
    print("-" * 80)
    if bar1 and bar2 and bar3 and bar4:
        verdict = "SUPPORT (DIRECTIONAL)"
    elif not bar2:
        verdict = "NOT (DIRECTIONAL)"
    else:
        verdict = "MIXED (DIRECTIONAL)"
    print(f"VERDICT: {verdict}")
    print("  numpy toy = DIRECTIONAL only; engine-native + 303M GPU cost-gated NOT fired (a_engine_native_learning).")
    print("=" * 80)

if __name__ == "__main__":
    main()
