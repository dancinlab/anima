#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
H_1623 — Hypernetwork Multiplicative Binding (lens = binding-multiplicative)
============================================================================
cheap_test ($0, numpy toy, mini-safe, CPU ~minutes) — DIRECTIONAL ONLY.

  ⚠️ MEASUREMENT PATH: numpy toy = DIRECTIONAL (NOT engine-native, a_engine_native_learning).
     The verdict is DIRECTIONAL regardless of pass/fail. numpy cheap_test CANNOT stamp 🟢/🧱.
     Engine-native (cli/anima.hexa → generator L3 → g_gates/g6) + 303M GPU = cost-gated
     PRE-REGISTER ONLY (NOT fired). This screen only selects whether the mechanism is a
     load-bearing G1 lever worth that 303M spend.

CLAIM UNDER TEST (brainarch census candidate H_1623, lens binding-multiplicative):
  The recombination / G1 "conjunction" wall is broken by a HYPERNETWORK MULTIPLICATIVE
  bind: instead of composing two concepts ADDITIVELY (z = Wa@a + Wb@b, separable), one
  input GENERATES the weights that MULTIPLICATIVELY modulate the other input —
      z = ( Whyper(a) ⊙ proj(b) )        # a-conditioned multiplicative gate on b
  This is a true bilinear/conjunctive interaction (FiLM/hypernet family). The hypothesis:
  marginal additive models cannot represent (a*b)-type joints (a invertible ⇒ marginals
  uniform ⇒ no per-factor shortcut), but a multiplicative hypernet gate CAN, so it should
  generalize to NOVEL combinations (held-out (a,b) never co-presented) = G1 recombination.

TOY TASK (binding-required / whole set = "ambiguous subset" BY CONSTRUCTION):
  factored inputs a,b ∈ Z_7* = {1..6}; 36 (a,b) pairs.  future = factored pair (y1,y2):
      y1 = (a*b) mod 7   (multiplicative, NON-separable / requires JOINT)
      y2 = (a+b) mod 7   (additive)
  MARGINALS CARRY ~ZERO INFO: a invertible in Z_7* ⇒ for fixed a, (a*b) ranges over all of
  {1..6} as b varies ⇒ P(y1|a),P(y1|b) UNIFORM. The WHOLE set is the binding-required subset
  (no marginal shortcut, cannot be inflated by full-set stats). Both rules FIXED ⇒ held-out
  combos are DETERMINED ⇒ generalization is meaningful (not a random Latin square).
  G1 recombination = generalize to combos never co-presented.

SPLIT: hold out 25% of 36 pairs (9) as NOVEL COMBINATIONS. train 27, test 9 held-out.
  Output is the JOINT compositional class over K1*K2 = 42 combos (BOTH factors correct).

MODELS (ALL share: AdamW grok-capable optimizer, factored composed keys key[c]=Fa[c1]+Fb[c2],
        InfoNCE-style sampled-negative contrastive head; ONLY the binding/encoder differs so the
        MECHANISM is the isolated lever, a_no_llm_frame_trap). Bars on BEST held-out over the run
        (generous → guards under-powered false NEGATIVE):

  M_HYPER (the mechanism)  : hypernetwork MULTIPLICATIVE bind. a → MLP → gate vector g_a∈R^D ;
                            b → linear → h_b∈R^D ; z = g_a ⊙ h_b  (element-wise PRODUCT).
                            This is the candidate H_1623 conjunctive interaction.
  M_ADD (INERT ablation)   : SAME params/shapes but PRODUCT → SUM: z = g_a + h_b. The ONLY change
                            is ⊙ → +  (multiplicative interaction OFF). If held-out collapses to
                            ~M_MARGINAL ⇒ the product is LOAD-BEARING. If unchanged ⇒ INERT.
  M_MARGINAL (CE baseline) : two INDEPENDENT softmax heads predict y1,y2 separately on a plain
                            additive encoder = "predict the marginal next symbol" (DISCRIM control;
                            clears train likelihood yet should FAIL strict joint G1).

GROK POSITIVE CONTROL (under-power guard): a single-head modular-ADDITION run (the canonical
  grokkable composable task) under a SHARED-EMBEDDING encoder at the SAME rung. If held-out >>
  chance ⇒ this $0 toy HAS the resolution to detect held-out composition (the discriminator works).
  If grok ctrl ~ chance ⇒ verdict = UNDER-POWER (the toy lacks resolution; NOT the mechanism's fault,
  a_break_the_wall type-a measurement limit). TOP-3 lesson: $0 toys are usually under-power.

==============================================================================
FROZEN BARS  (pre-registered BEFORE running — frozen-first, tune-to-green FORBIDDEN p7/c9)
==============================================================================
  chance (compositional, BOTH factors correct) = 1 / (K1*K2) = 1/42 ~= 0.0238

  BAR-1  composed binding   : M_HYPER held-out compositional acc >= 0.50  (>> chance)
  BAR-2  > max single       : M_HYPER held-out acc > max(M_ADD held, M_MARGINAL held)
                              AND M_HYPER held >= 2x chance (composed_distinct>=2 spirit)
  BAR-3  INERT ablation     : product is LOAD-BEARING — (M_HYPER held - M_ADD held) >= 0.20
                              (turning ⊙→+ collapses generalization). If ~0 ⇒ INERT (mechanism free).
  BAR-4  ambiguous-pair     : on held pairs, M_HYPER prefers the TRUE joint future over a VERBATIM
                              same-a recall distractor (the "copying 0.5" trap) on >= 0.80 of pairs.
  GROK-CTRL  under-power     : modular-addition shared-embed held-out >> chance(=1/11) ⇒ toy has resolution.

  VERDICT (DIRECTIONAL):
    SUPPORTED   = grok_ctrl PASS & BAR-1 & BAR-2 & BAR-3 & BAR-4 all pass
    UNDER-POWER = grok_ctrl FAIL (toy lacks resolution; mechanism not blamed)
    NOT-SUPPORTED = grok_ctrl PASS but BAR-3 INERT (product contributes ~0) OR BAR-1 fails badly
    MIXED       = grok_ctrl PASS, some bars pass some fail
  Multi-seed (5 seeds); judge on the MEAN across seeds (anti sampler-artifact).
  survivor = SUPPORTED only (BARS frozen AND grok PASS AND ablation load-bearing). VERY conservative.
==============================================================================
"""
import numpy as np

P = 7
VALS = list(range(1, P))
PAIRS = [(a, b) for a in VALS for b in VALS]            # 36
K1, K2 = P - 1, P                                       # y1∈{1..6}->6cls, y2∈{0..6}->7cls
NCOMBO = K1 * K2                                        # 42
NA = P - 1                                              # 6 distinct a / b values
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
def smrow(L):
    L = L - L.max(1, keepdims=True); e = np.exp(L); return e / e.sum(1, keepdims=True)

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
            params[k] -= LR * (mh / (np.sqrt(vh) + EPS) + WD * params[k])

# index arrays for a,b (0-based factor index) given a list of pairs
def ab_idx(pairs):
    return (np.array([a - 1 for (a, b) in pairs]),
            np.array([b - 1 for (a, b) in pairs]))

def run_seed(seed):
    rng = np.random.default_rng(seed)
    pairs = PAIRS[:]; rng.shuffle(pairs)
    nh = int(round(HELD_FRAC * len(pairs)))
    held, train = pairs[:nh], pairs[nh:]
    ai, bi = ab_idx(train); aih, bih = ab_idx(held)
    Ytr = [fut(*p) for p in train]; Yhe = [fut(*p) for p in held]
    t1 = np.array([y[0] for y in Ytr]); t2 = np.array([y[1] for y in Ytr])
    he1 = np.array([y[0] for y in Yhe]); he2 = np.array([y[1] for y in Yhe])
    tc_tr = np.array([cidx(*y) for y in Ytr]); tc_he = np.array([cidx(*y) for y in Yhe])
    N = len(train)
    # verbatim same-a recall distractor per held pair (the "copy 0.5" trap)
    def recall(pb):
        a, b = pb; tr = fut(a, b)
        cs = [fut(a, bb) for (aa, bb) in train if aa == a and fut(a, bb) != tr]
        if not cs: cs = [fut(*q) for q in train if fut(*q) != tr]
        return cidx(*cs[0])
    rec_he = np.array([recall(pb) for pb in held])
    out = {}

    # ---------- M_HYPER (multiplicative) / M_ADD (INERT ablation: product->sum) ----------
    # encoder: a -> MLP -> gate g_a (D) ; b -> linear -> h_b (D) ; z = g_a (*|+) h_b
    def bind_model(multiplicative):
        p = {
            # hypernet on a: onehot_a(NA) -> H -> D  (gate generator)
            'A1': rng.normal(0, 1/np.sqrt(NA), (H, NA)), 'ab1': np.zeros(H),
            'A2': rng.normal(0, 1/np.sqrt(H), (D, H)),   'ab2': np.zeros(D),
            # b projection: onehot_b(NA) -> D
            'Bp': rng.normal(0, 1/np.sqrt(NA), (D, NA)), 'bb': np.zeros(D),
            'Fa': rng.normal(0, 1/np.sqrt(D), (K1, D)),  'Fb': rng.normal(0, 1/np.sqrt(D), (K2, D)),
        }
        opt = Adam(p); best = 0.0; best_vb = 0.0
        OHa = np.eye(NA)[ai]; OHb = np.eye(NA)[bi]          # N x NA
        OHah = np.eye(NA)[aih]; OHbh = np.eye(NA)[bih]
        def fwd(OA, OB):
            PRE = OA @ p['A1'].T + p['ab1']; Hh = np.tanh(PRE)
            Ga = Hh @ p['A2'].T + p['ab2']                  # gate g_a  (n x D)
            Hb = OB @ p['Bp'].T + p['bb']                   # h_b       (n x D)
            Z = Ga * Hb if multiplicative else Ga + Hb
            return Z, Hh, Ga, Hb
        for st in range(STEPS):
            Z, Hh, Ga, Hb = fwd(OHa, OHb)
            KEY = p['Fa'][C1] + p['Fb'][C2]                 # 42 x D
            L = Z @ KEY.T                                   # N x 42
            # InfoNCE-style masked softmax: pos + NEG_K random negs + verbatim hard neg
            mask = np.zeros((N, NCOMBO), bool); mask[np.arange(N), tc_tr] = True
            for i in range(N):
                mask[i, rng.choice(NCOMBO, NEG_K, replace=False)] = True
                a, b = train[i]; tr = fut(a, b)
                cs = [fut(a, bb) for (aa, bb) in train if aa == a and fut(a, bb) != tr]
                if cs: mask[i, cidx(*cs[0])] = True
                mask[i, tc_tr[i]] = True
            Lm = np.where(mask, L, -1e9); Pp = smrow(Lm)
            DL = Pp.copy(); DL[np.arange(N), tc_tr] -= 1; DL /= N
            g = {k: np.zeros_like(v) for k, v in p.items()}
            gKEY = DL.T @ Z; np.add.at(g['Fa'], C1, gKEY); np.add.at(g['Fb'], C2, gKEY)
            dZ = DL @ KEY                                   # N x D
            if multiplicative:
                dGa = dZ * Hb; dHb = dZ * Ga
            else:
                dGa = dZ; dHb = dZ
            # b proj grads
            g['Bp'] = dHb.T @ OHb; g['bb'] = dHb.sum(0)
            # hypernet grads
            g['A2'] = dGa.T @ Hh; g['ab2'] = dGa.sum(0)
            dHh = dGa @ p['A2']; dPRE = dHh * (1 - Hh * Hh)
            g['A1'] = dPRE.T @ OHa; g['ab1'] = dPRE.sum(0)
            opt.step(p, g)
            if st % EVAL_EVERY == 0 or st == STEPS - 1:
                Zh, _, _, _ = fwd(OHah, OHbh)
                KEYe = p['Fa'][C1] + p['Fb'][C2]
                sc = Zh @ KEYe.T
                acc = np.mean(np.argmax(sc, 1) == tc_he)
                s_true = sc[np.arange(len(held)), tc_he]; s_vb = sc[np.arange(len(held)), rec_he]
                vb = float(np.mean(s_true > s_vb))
                if acc >= best: best = acc; best_vb = vb
        return float(best), best_vb

    out['HYPER_held'], out['HYPER_vb'] = bind_model(True)
    out['ADD_held'],   out['ADD_vb']   = bind_model(False)

    # ---------- M_MARGINAL (two independent CE heads, additive encoder) ----------
    p = {'Wa': rng.normal(0, 1/np.sqrt(NA), (D, NA)), 'Wb': rng.normal(0, 1/np.sqrt(NA), (D, NA)),
         'Hy1': rng.normal(0, 1/np.sqrt(D), (K1, D)), 'Hy2': rng.normal(0, 1/np.sqrt(D), (K2, D))}
    opt = Adam(p); best = 0.0; tr_at_best = 0.0
    for st in range(STEPS):
        Z = p['Wa'][:, ai].T + p['Wb'][:, bi].T            # N x D additive
        Pp1 = smrow(Z @ p['Hy1'].T); Pp2 = smrow(Z @ p['Hy2'].T)
        DA = Pp1.copy(); DA[np.arange(N), t1] -= 1; DA /= N
        DB = Pp2.copy(); DB[np.arange(N), t2] -= 1; DB /= N
        g = {k: np.zeros_like(v) for k, v in p.items()}
        g['Hy1'] = DA.T @ Z; g['Hy2'] = DB.T @ Z
        dZ = DA @ p['Hy1'] + DB @ p['Hy2']
        np.add.at(g['Wa'].T, ai, dZ); np.add.at(g['Wb'].T, bi, dZ)
        opt.step(p, g)
        if st % EVAL_EVERY == 0 or st == STEPS - 1:
            Zh = p['Wa'][:, aih].T + p['Wb'][:, bih].T
            acc = np.mean((np.argmax(Zh @ p['Hy1'].T, 1) == he1) & (np.argmax(Zh @ p['Hy2'].T, 1) == he2))
            Zt = p['Wa'][:, ai].T + p['Wb'][:, bi].T
            tacc = np.mean((np.argmax(Zt @ p['Hy1'].T, 1) == t1) & (np.argmax(Zt @ p['Hy2'].T, 1) == t2))
            if acc >= best: best = acc; tr_at_best = tacc
    out['MARG_held'] = float(best); out['MARG_train'] = float(tr_at_best)
    return out

def grok_control(seed=7):
    """canonical grokkable modular ADDITION with shared-embedding encoder — does the toy resolve composition AT ALL?"""
    Pm = 11; vals = list(range(Pm)); prs = [(a, b) for a in vals for b in vals]
    Hm, Dm = 256, 64
    rng = np.random.default_rng(seed); rng.shuffle(prs)
    nh = len(prs) // 2; held, train = prs[:nh], prs[nh:]
    ai = np.array([a for (a, b) in train]); bi = np.array([b for (a, b) in train])
    aih = np.array([a for (a, b) in held]); bih = np.array([b for (a, b) in held])
    ytr = np.array([(a + b) % Pm for (a, b) in train]); yhe = np.array([(a + b) % Pm for (a, b) in held])
    N = len(train)
    # shared embedding table E (Pm x Dm); encoder z = tanh([E[a];E[b]] @ W1) @ W2
    p = {'E': rng.normal(0, 1/np.sqrt(Dm), (Pm, Dm)),
         'W1': rng.normal(0, 1/np.sqrt(2*Dm), (Hm, 2*Dm)), 'b1': np.zeros(Hm),
         'W2': rng.normal(0, 1/np.sqrt(Hm), (Dm, Hm)), 'b2': np.zeros(Dm),
         'Hd': rng.normal(0, 1/np.sqrt(Dm), (Pm, Dm))}
    opt = Adam(p); best = 0.0
    def fwd(av, bv):
        X = np.concatenate([p['E'][av], p['E'][bv]], 1)    # n x 2Dm
        PRE = X @ p['W1'].T + p['b1']; Hh = np.tanh(PRE); Z = Hh @ p['W2'].T + p['b2']
        return Z, Hh, X
    for st in range(40000):
        Z, Hh, X = fwd(ai, bi)
        Pp = smrow(Z @ p['Hd'].T); DL = Pp.copy(); DL[np.arange(N), ytr] -= 1; DL /= N
        g = {k: np.zeros_like(v) for k, v in p.items()}
        g['Hd'] = DL.T @ Z; dZ = DL @ p['Hd']
        g['W2'] = dZ.T @ Hh; g['b2'] = dZ.sum(0)
        dHh = dZ @ p['W2']; dPRE = dHh * (1 - Hh * Hh)
        g['W1'] = dPRE.T @ X; g['b1'] = dPRE.sum(0)
        dX = dPRE @ p['W1']                                 # n x 2Dm
        np.add.at(g['E'], ai, dX[:, :Dm]); np.add.at(g['E'], bi, dX[:, Dm:])
        opt.step(p, g)
        if st % 8000 == 0 or st == 39999:
            Zh, _, _ = fwd(aih, bih)
            best = max(best, float(np.mean(np.argmax(Zh @ p['Hd'].T, 1) == yhe)))
    return best

def main():
    chance = 1.0 / NCOMBO
    print("=" * 80)
    print("H_1623 hypernet_multiplicative_bind — cheap_test (numpy AdamW, DIRECTIONAL)")
    print(f"task: Z_7* factored y1=(a*b)%7 y2=(a+b)%7 | 36 pairs, held {HELD_FRAC:.0%} novel combos")
    print(f"binding-required: P(y|a),P(y|b) UNIFORM (whole set = ambiguous subset, no marginal shortcut)")
    print(f"compositional chance = 1/{NCOMBO} = {chance:.4f} | steps={STEPS} AdamW lr={LR} wd={WD} seeds={SEEDS}")
    print("mechanism = z=g_a(b-gate) ⊙ h_b ; INERT ablation = ⊙→+ ; bars on BEST held over run")
    print("=" * 80)
    keys = ['HYPER_held','HYPER_vb','ADD_held','ADD_vb','MARG_held','MARG_train']
    agg = {k: [] for k in keys}
    for s in SEEDS:
        r = run_seed(s)
        for k in keys: agg[k].append(r[k])
        print(f"seed {s:>5}: HYPER he={r['HYPER_held']:.2f} vb={r['HYPER_vb']:.2f} | "
              f"ADD(inert) he={r['ADD_held']:.2f} vb={r['ADD_vb']:.2f} | "
              f"MARG tr={r['MARG_train']:.2f} he={r['MARG_held']:.2f}")
    m = {k: float(np.mean(v)) for k, v in agg.items()}
    print("-" * 80)
    grok = grok_control()
    print(f"GROK POSITIVE CONTROL (shared-embed modular ADDITION, AdamW 40k, 50% held): best held = {grok:.3f}")
    print(f"  chance=1/11={1/11:.3f}. grok>>chance ⇒ toy resolves held-out composition (discriminator works).")
    print(f"  grok~chance ⇒ UNDER-POWER (measurement limit, not the mechanism; a_break_the_wall type-a).")
    print("-" * 80)
    max_single = max(m['ADD_held'], m['MARG_held'])
    print("MEANS across seeds (BEST held over run):")
    print(f"  M_HYPER (mult)    : held={m['HYPER_held']:.3f}  vb_win={m['HYPER_vb']:.3f}")
    print(f"  M_ADD (INERT abl) : held={m['ADD_held']:.3f}  vb_win={m['ADD_vb']:.3f}")
    print(f"  M_MARGINAL (CE)   : train={m['MARG_train']:.3f}  held={m['MARG_held']:.3f}")
    print(f"  max_single        : {max_single:.3f}")
    print("-" * 80)
    grok_pass = grok >= 0.50          # >> chance(0.09); canonical grok clears easily if resolved
    bar1 = m['HYPER_held'] >= 0.50
    bar2 = (m['HYPER_held'] > max_single) and (m['HYPER_held'] >= 2 * chance)
    bar3 = (m['HYPER_held'] - m['ADD_held']) >= 0.20    # product LOAD-BEARING (else INERT)
    bar4 = m['HYPER_vb'] >= 0.80
    inert = (m['HYPER_held'] - m['ADD_held']) < 0.05    # explicit INERT flag
    print("FROZEN BARS:")
    print(f"  GROK-CTRL  modular-add held>=0.50                  : {grok:.3f}  -> {'PASS' if grok_pass else 'FAIL'}")
    print(f"  BAR-1 composed binding   HYPER_held>=0.50          : {m['HYPER_held']:.3f}  -> {'PASS' if bar1 else 'FAIL'}")
    print(f"  BAR-2 > max single       HYPER>max_single & >=2chance: {m['HYPER_held']:.3f} vs {max_single:.3f} -> {'PASS' if bar2 else 'FAIL'}")
    print(f"  BAR-3 INERT ablation     (HYPER-ADD)>=0.20         : d={m['HYPER_held']-m['ADD_held']:+.3f} -> {'PASS' if bar3 else 'FAIL'}")
    print(f"  BAR-4 ambiguous-pair     HYPER vb_win>=0.80        : {m['HYPER_vb']:.3f}  -> {'PASS' if bar4 else 'FAIL'}")
    print(f"  [INERT flag (HYPER-ADD)<0.05]                      : {'INERT' if inert else 'load-bearing'}")
    print("-" * 80)
    if not grok_pass:
        verdict = "UNDER-POWER (DIRECTIONAL)"
    elif bar1 and bar2 and bar3 and bar4:
        verdict = "SUPPORTED (DIRECTIONAL)"
    elif inert or not bar1:
        verdict = "NOT-SUPPORTED (DIRECTIONAL)"
    else:
        verdict = "MIXED (DIRECTIONAL)"
    survivor = grok_pass and bar1 and bar2 and bar3 and bar4
    print(f"VERDICT: {verdict}")
    print(f"SURVIVOR (worth 303M): {survivor}  (=grok PASS & all 4 bars & ablation load-bearing)")
    print("  numpy toy = DIRECTIONAL only; engine-native + 303M GPU cost-gated NOT fired (a_engine_native_learning).")
    print("=" * 80)
    return m, grok, verdict, survivor

if __name__ == "__main__":
    main()
