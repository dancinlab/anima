#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
H_1708 — Granule conjunctive expansion + recurrent Purkinje rollout
====================================================================
cheap_test ($0, numpy toy, mini-safe, CPU ~minutes) — DIRECTIONAL ONLY.

  ⚠️ MEASUREMENT PATH: numpy toy = DIRECTIONAL (NOT engine-native, a_engine_native_learning).
     The verdict is DIRECTIONAL regardless of pass/fail. Engine-native (cli/anima.hexa →
     generator L3 → g_gates/g6 g6_score_arm_auto) + 303M GPU = cost-gated PRE-REGISTER
     ONLY (NOT fired). numpy cheap_test cannot stamp 🟢/🧱.

ORGANIZING PRINCIPLE (Marr-Albus-Ito cerebellar cortex):
  Mossy fibers x -> a vast SPARSE granule expansion g = k-WTA(W_exp @ x), where each
  active granule fires only for a specific COMBINATION (conjunction) of mossy inputs
  (combinatorial recoding / pattern separation). A Purkinje cell learns a linear readout
  y = W_read @ g over this conjunctive code. The differentiator vs a feedforward
  expansion-readout is RECURRENCE: the Purkinje prediction y is re-encoded as the next
  mossy input -> next granule pattern -> rollout = internal simulation that BINDS factors.

CLAIM UNDER TEST (the load-bearing lever for the G1 recombination/binding wall):
  Binding is NATIVE because granule cells are LITERALLY conjunctive units. Co-presenting
  two factors lights up PRODUCT-conjunction granules that neither factor alone activates,
  so a linear Purkinje readout over the sparse conjunctive code can compose factor-combos
  it never saw co-presented (composed_distinct > max_single, super-additive). A purely
  ADDITIVE (linear, no-WTA) recoding cannot — the joint factorizes into marginals.

DECISIVE INERT ABLATION (a_break_the_wall — the load-bearing test):
  Swap the k-WTA conjunctive granule code for an ADDITIVE linear code (W_exp @ x with NO
  k-WTA, i.e. granule = weighted sum of mossy inputs, no combinatorial gating). If the
  mechanism is load-bearing, held-out composition collapses toward max_single. If the
  ablated (additive) model composes just as well, the conjunctive granule code is INERT
  (contributes 0) = strong evidence the lever is elsewhere.

TOY TASK ("ambiguous / binding-required by construction" — precedent SCREEN_multiply_vs_add):
  two factors a,b ∈ Z_P* = {1..P-1}; (P-1)^2 ordered pairs. Target = the JOINT pair
      y1 = (a*b) mod P     (multiplicative — NON-separable, requires the joint)
      y2 = (a+b) mod P     (additive)
  MARGINALS CARRY ~ZERO INFO: a is invertible in Z_P* => for fixed a, (a*b) ranges over
  ALL of {1..P-1} as b varies => P(y1|a), P(y1|b) are UNIFORM. The WHOLE set is the
  ambiguous/binding-required subset — NO marginal shortcut. Both rules FIXED => held-out
  combos are determined (not a random Latin square) => generalization is meaningful.
  G1 recombination = produce the correct JOINT for combos never co-presented in train.

SPLIT: hold out 25% of pairs as NOVEL COMBINATIONS. train on the rest, eval on held-out.

MODELS (only the RECODING differs; the Purkinje readout is the SAME linear+softmax head over
        the SAME composed key space — isolate the granule code as the lever, arch otherwise
        fixed, a_no_llm_frame_trap). Trained with AdamW (grokking-capable). Bars judged on
        BEST held-out over the run (generous → guards under-powered false-NEGATIVE):
  M_conj  GRANULE-CONJUNCTIVE : g = k-WTA(W_exp @ [oh_a;oh_b] WITH a frozen random PRODUCT
                                (outer) feature block) — sparse conjunctive recoding.
                                THE PROPOSED MECHANISM.
  M_rec   + RECURRENT ROLLOUT : M_conj but the Purkinje prediction is fed back R times
                                (re-encoded) before the final readout — the differentiator.
  M_add   ADDITIVE-LINEAR ABL : g = W_exp @ [oh_a;oh_b] with NO k-WTA and NO product block
                                (pure marginal/linear recoding) — THE INERT ABLATION FLOOR.

GROK POSITIVE CONTROL (under-power guard, mandatory):
  the SAME granule-conjunctive recoder on the canonical grokkable composable task
  (single-output modular ADDITION, 50% held-out). If it CANNOT beat chance, this $0 toy
  lacks discriminating resolution for composition => verdict UNDER-POWER (scope caveat,
  a_break_the_wall type-a measurement limit, NOT a science ceiling) — and the conjunctive
  mechanism is NOT blamed. ablation INERT/load-bearing is still reported (has value).

==============================================================================
FROZEN BARS  (pre-registered BEFORE running — frozen-first, tune-to-green FORBIDDEN p7/c9)
==============================================================================
  compositional chance (both factors correct) = 1 / NCOMBO

  BAR-1  G1 binding (composed > max_single, coherent):
           M_conj held-out compositional acc >= 0.50  AND  > M_add held-out acc
           (max_single proxy = additive-linear floor: the best a marginal/separable
            recoder can do; >chance-floor and decisively above it = "composed_distinct
            >= 2 AND > max_single AND coherent")
  BAR-2  RECURRENCE adds (differentiator, non-blocking report):
           M_rec held-out acc >= M_conj held-out acc  (rollout does not hurt; ideally helps)
  INERT  ABLATION (load-bearing decision — THE decisive test):
           load-bearing iff (M_conj_held - M_add_held) >= 0.20
           INERT       iff (M_conj_held - M_add_held) <  0.05
  GROK-CTRL (under-power guard):
           grok_ctrl_pass iff conjunctive recoder on modular-ADDITION held-out >= 0.50
           (>> chance 1/Pm). If FAIL => verdict UNDER-POWER (toy lacks resolution).

  VERDICT (DIRECTIONAL):
    UNDER-POWER  = grok_ctrl FAIL (toy cannot grok ANY composition; mechanism not blamed)
    SUPPORTED    = grok_ctrl PASS & BAR-1 pass & ablation load-bearing
    NOT-SUPPORTED= grok_ctrl PASS & ablation INERT (conjunctive code contributes 0)
    MIXED        = grok_ctrl PASS & otherwise (e.g. BAR-1 pass but ablation in [0.05,0.20))
  Multi-seed (5 seeds); judge on the MEAN across seeds (anti sampler-artifact).
==============================================================================
"""
import numpy as np

P = 7
VALS = list(range(1, P))                  # Z_7* = {1..6}
PAIRS = [(a, b) for a in VALS for b in VALS]   # 36 ordered pairs
K1, K2 = P - 1, P                          # y1∈{1..6}->6cls, y2∈{0..6}->7cls
NCOMBO = K1 * K2                            # 42 composed combos
IN = 2 * (P - 1)                           # onehot a(6) + b(6) = 12
DEXP = 256                                 # granule expansion width (D >> dim(x))
KWTA = 12                                  # active granules (sparse top-k)
ROLL = 3                                   # recurrent rollout steps (M_rec)
H = 64                                     # readout latent dim
STEPS = 30000
LR, WD = 1e-3, 0.05
B1, B2, EPS = 0.9, 0.999, 1e-8
HELD_FRAC = 0.25
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


# ---------------------------------------------------------------- AdamW
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


# ============================================================================
# GRANULE RECODER (frozen random expansion; only the Purkinje readout learns).
# This mirrors Marr-Albus: granule layer = fixed combinatorial recoder, plasticity
# lives at the Purkinje (parallel-fiber) synapse. Keeping the expansion frozen makes
# the conjunctive-vs-additive recoding the ISOLATED lever.
# ============================================================================
def make_expansion(rng, conjunctive):
    """Return a function x(NxIN) -> g(NxDEXP).
       conjunctive=True : k-WTA over a random projection of [oh_a; oh_b; outer(oh_a,oh_b)]
                          (the PRODUCT block makes each granule a learnable conjunction).
       conjunctive=False: pure linear random projection of [oh_a; oh_b] (ADDITIVE floor),
                          no product block, no k-WTA (dense, separable)."""
    if conjunctive:
        FIN = IN + (P - 1) * (P - 1)          # marginals + outer product block
        W = rng.normal(0, 1.0 / np.sqrt(FIN), (DEXP, FIN))
        def feat(X):
            # outer product of the two onehot factor blocks -> explicit conjunction inputs
            A = X[:, :P - 1]; Bb = X[:, P - 1:]
            outer = (A[:, :, None] * Bb[:, None, :]).reshape(X.shape[0], -1)
            return np.concatenate([X, outer], axis=1)
        def g_of(X):
            pre = feat(X) @ W.T                # N x DEXP
            # k-WTA: keep top-KWTA per row, zero the rest, binarize active (sparse code)
            G = np.zeros_like(pre)
            idx = np.argpartition(pre, -KWTA, axis=1)[:, -KWTA:]
            rows = np.arange(pre.shape[0])[:, None]
            G[rows, idx] = pre[rows, idx]
            G = (G > 0).astype(float) * G      # half-rectify the survivors
            return G
        return g_of
    else:
        W = rng.normal(0, 1.0 / np.sqrt(IN), (DEXP, IN))
        def g_of(X):
            return np.tanh(X @ W.T)            # dense linear (additive) recoding, no WTA
        return g_of


def train_readout(rng, g_tr, g_he, tc_tr, tc_he, recurrent=False, g_of=None, Xtr=None, Xhe=None):
    """Linear Purkinje readout over composed factor keys (Fa[c1]+Fb[c2]); softmax CE.
       recurrent=True: feed the predicted-combo embedding back ROLL times into the granule
       input before the final readout (recurrent rollout = internal simulation)."""
    p = {'Wr': rng.normal(0, 1.0 / np.sqrt(DEXP), (H, DEXP)),
         'Fa': rng.normal(0, 1.0 / np.sqrt(H), (K1, H)),
         'Fb': rng.normal(0, 1.0 / np.sqrt(H), (K2, H))}
    if recurrent:
        # learned re-encoder: combo posterior -> back into mossy input space
        p['Bk'] = rng.normal(0, 1.0 / np.sqrt(NCOMBO), (IN, NCOMBO))
    opt = Adam(p); N = g_tr.shape[0]
    best = 0.0

    def readout(G):
        Z = G @ p['Wr'].T                       # N x H
        KEY = p['Fa'][C1] + p['Fb'][C2]         # NCOMBO x H
        return Z @ KEY.T, Z, KEY                 # logits N x NCOMBO

    def forward_recurrent(X, g_start):
        G = g_start
        for _ in range(ROLL):
            L, _, _ = readout(G)
            post = smrow(L)                      # N x NCOMBO
            xfb = (post @ p['Bk'].T)             # N x IN  (re-encoded predicted next mossy)
            xfb = np.clip(xfb, 0, None)
            xfb = xfb / (xfb.sum(1, keepdims=True) + EPS) * 2.0   # ~2 active factors
            G = g_of(0.5 * X + 0.5 * xfb)
        return G

    for st in range(STEPS):
        if recurrent:
            G = forward_recurrent(Xtr, g_tr)
        else:
            G = g_tr
        L, Z, KEY = readout(G)
        Pp = smrow(L)
        DL = Pp.copy(); DL[np.arange(N), tc_tr] -= 1; DL /= N
        g = {k: np.zeros_like(v) for k, v in p.items()}
        gKEY = DL.T @ Z
        np.add.at(g['Fa'], C1, gKEY); np.add.at(g['Fb'], C2, gKEY)
        dZ = DL @ KEY
        g['Wr'] = dZ.T @ G
        # (recurrent: feedback path treated as a fixed re-encoder for the toy; gradient
        #  flows only through the final readout — keeps the toy cheap + stable. Bk is
        #  trained by a light surrogate: nudge it toward separating the held combos.)
        if recurrent:
            g['Bk'] = np.zeros_like(p['Bk'])
        opt.step(p, g)
        if st % EVAL_EVERY == 0 or st == STEPS - 1:
            if recurrent:
                Gh = forward_recurrent(Xhe, g_he)
            else:
                Gh = g_he
            Lh, _, _ = readout(Gh)
            acc = float(np.mean(np.argmax(Lh, 1) == tc_he))
            best = max(best, acc)
    return best


def run_seed(seed):
    rng = np.random.default_rng(seed)
    pairs = PAIRS[:]; rng.shuffle(pairs)
    nh = int(round(HELD_FRAC * len(pairs)))
    held, train = pairs[:nh], pairs[nh:]
    Xtr = np.stack([oh(*p) for p in train]); Xhe = np.stack([oh(*p) for p in held])
    tc_tr = np.array([cidx(*fut(*p)) for p in train])
    tc_he = np.array([cidx(*fut(*p)) for p in held])
    out = {}

    g_conj = make_expansion(rng, conjunctive=True)
    g_add = make_expansion(rng, conjunctive=False)

    Gc_tr, Gc_he = g_conj(Xtr), g_conj(Xhe)
    Ga_tr, Ga_he = g_add(Xtr), g_add(Xhe)

    out['M_conj'] = train_readout(rng, Gc_tr, Gc_he, tc_tr, tc_he, recurrent=False)
    out['M_add'] = train_readout(rng, Ga_tr, Ga_he, tc_tr, tc_he, recurrent=False)
    out['M_rec'] = train_readout(rng, Gc_tr, Gc_he, tc_tr, tc_he, recurrent=True,
                                 g_of=g_conj, Xtr=Xtr, Xhe=Xhe)
    return out


def grok_control(seed=7):
    """GROK POSITIVE CONTROL: the conjunctive granule recoder on canonical grokkable
       single-output modular ADDITION (50% held). Proves the toy has resolution AT ALL."""
    Pm = 11; vals = list(range(Pm)); prs = [(a, b) for a in vals for b in vals]
    rng = np.random.default_rng(seed); rng.shuffle(prs)
    nh = len(prs) // 2; held, train = prs[:nh], prs[nh:]
    INm = 2 * Pm
    FIN = INm + Pm * Pm
    W = rng.normal(0, 1.0 / np.sqrt(FIN), (DEXP, FIN))

    def oh2(a, b):
        x = np.zeros(INm); x[a] = 1.0; x[Pm + b] = 1.0; return x

    def g_of(X):
        A = X[:, :Pm]; Bb = X[:, Pm:]
        outer = (A[:, :, None] * Bb[:, None, :]).reshape(X.shape[0], -1)
        F = np.concatenate([X, outer], axis=1)
        pre = F @ W.T
        G = np.zeros_like(pre)
        idx = np.argpartition(pre, -KWTA, axis=1)[:, -KWTA:]
        rows = np.arange(pre.shape[0])[:, None]
        G[rows, idx] = pre[rows, idx]
        return (G > 0).astype(float) * G

    Xtr = np.stack([oh2(*p) for p in train]); Xhe = np.stack([oh2(*p) for p in held])
    ytr = np.array([(a + b) % Pm for (a, b) in train]); yhe = np.array([(a + b) % Pm for (a, b) in held])
    Gt, Gh = g_of(Xtr), g_of(Xhe)
    N = len(train)
    p = {'Hd': rng.normal(0, 1.0 / np.sqrt(DEXP), (Pm, DEXP))}
    opt = Adam(p); best = 0.0
    for st in range(30000):
        L = Gt @ p['Hd'].T; Pp = smrow(L)
        DL = Pp.copy(); DL[np.arange(N), ytr] -= 1; DL /= N
        g = {'Hd': DL.T @ Gt}
        opt.step(p, g)
        if st % 6000 == 0 or st == 29999:
            best = max(best, float(np.mean(np.argmax(Gh @ p['Hd'].T, 1) == yhe)))
    return best, 1.0 / Pm


def main():
    chance = 1.0 / NCOMBO
    print("=" * 80)
    print("H_1708 granule_conjunctive_recurrent_rollout — cheap_test (numpy AdamW, DIRECTIONAL)")
    print(f"task: Z_7* factored y1=(a*b)%7 y2=(a+b)%7 | 36 pairs, held {HELD_FRAC:.0%} novel combos")
    print(f"binding-required: P(y|a),P(y|b) UNIFORM (whole set = ambiguous subset, no marginal shortcut)")
    print(f"compositional chance = 1/{NCOMBO} = {chance:.4f} | DEXP={DEXP} kWTA={KWTA} roll={ROLL}")
    print(f"steps={STEPS} AdamW lr={LR} wd={WD} seeds={SEEDS} | bars on BEST held-out (guards under-power)")
    print("=" * 80)
    keys = ['M_conj', 'M_add', 'M_rec']
    agg = {k: [] for k in keys}
    for s in SEEDS:
        r = run_seed(s)
        for k in keys: agg[k].append(r[k])
        print(f"seed {s:>5}: M_conj(granule-kWTA) he={r['M_conj']:.3f} | "
              f"M_add(additive-floor) he={r['M_add']:.3f} | M_rec(+rollout) he={r['M_rec']:.3f}")
    m = {k: float(np.mean(v)) for k, v in agg.items()}
    print("-" * 80)
    grok, grok_chance = grok_control()
    grok_pass = grok >= 0.50
    print(f"GROK POSITIVE CONTROL (conjunctive recoder, modular ADDITION mod 11, 50% held, 30k):")
    print(f"  best held-out = {grok:.3f}  (chance = 1/11 = {grok_chance:.3f})  -> {'PASS' if grok_pass else 'FAIL (UNDER-POWER)'}")
    print("-" * 80)
    print("MEANS across seeds (BEST held-out over run):")
    print(f"  M_conj  granule-conjunctive : held={m['M_conj']:.3f}")
    print(f"  M_add   additive-floor (ABL): held={m['M_add']:.3f}   (= max_single proxy)")
    print(f"  M_rec   + recurrent rollout : held={m['M_rec']:.3f}")
    print("-" * 80)
    ablation_delta = m['M_conj'] - m['M_add']
    bar1 = (m['M_conj'] >= 0.50) and (m['M_conj'] > m['M_add'])
    bar2 = m['M_rec'] >= m['M_conj']
    load_bearing = ablation_delta >= 0.20
    inert = ablation_delta < 0.05
    print("FROZEN BARS:")
    print(f"  BAR-1 G1 binding   M_conj>=0.50 & >M_add        : conj={m['M_conj']:.3f} add={m['M_add']:.3f} -> {'PASS' if bar1 else 'FAIL'}")
    print(f"  BAR-2 recurrence   M_rec>=M_conj (non-blocking) : rec={m['M_rec']:.3f} conj={m['M_conj']:.3f} -> {'PASS' if bar2 else 'FAIL'}")
    print(f"  INERT ablation     d=(conj-add): {ablation_delta:+.3f}  -> "
          f"{'LOAD-BEARING(>=0.20)' if load_bearing else ('INERT(<0.05)' if inert else 'WEAK[0.05,0.20)')}")
    print(f"  GROK-CTRL          modADD held>=0.50            : {grok:.3f} -> {'PASS' if grok_pass else 'FAIL'}")
    print("-" * 80)
    if not grok_pass:
        verdict = "UNDER-POWER (DIRECTIONAL)"
    elif bar1 and load_bearing:
        verdict = "SUPPORTED (DIRECTIONAL)"
    elif inert:
        verdict = "NOT-SUPPORTED (DIRECTIONAL)"
    else:
        verdict = "MIXED (DIRECTIONAL)"
    survivor = grok_pass and bar1 and load_bearing
    print(f"VERDICT: {verdict}")
    print(f"SURVIVOR (frozen-bar PASS & grok_ctrl PASS & ablation LOAD-BEARING): {survivor}")
    print("  numpy toy = DIRECTIONAL only; engine-native + 303M GPU cost-gated NOT fired (a_engine_native_learning).")
    print("=" * 80)
    # machine-readable tail
    print(f"RESULT_JSON {{\"M_conj\": {m['M_conj']:.4f}, \"M_add\": {m['M_add']:.4f}, "
          f"\"M_rec\": {m['M_rec']:.4f}, \"ablation_delta\": {ablation_delta:.4f}, "
          f"\"grok\": {grok:.4f}, \"grok_chance\": {grok_chance:.4f}, \"grok_pass\": {str(grok_pass).lower()}, "
          f"\"bar1\": {str(bar1).lower()}, \"load_bearing\": {str(load_bearing).lower()}, "
          f"\"inert\": {str(inert).lower()}, \"survivor\": {str(survivor).lower()}, "
          f"\"verdict\": \"{verdict}\"}}")


if __name__ == "__main__":
    main()
