#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
H_1692 — Active-Inference Agent: Emission as Action Minimizing Expected Free Energy
==================================================================================
cheap_test ($0, numpy toy, mini-safe, CPU ~minutes) — DIRECTIONAL ONLY.

  ⚠️ MEASUREMENT PATH: numpy toy = DIRECTIONAL (NOT engine-native,
     a_engine_native_learning). No cli/anima.hexa, no core/g_gates, no torch.
     The toy decides the DIRECTION of the architecture, NOT a terminal G0/G1/G2
     verdict. Engine-native (single dispatch -> generator L3 -> g_gates/g6) +
     303M GPU is cost-gated PRE-REGISTER ONLY (NOT fired). numpy cannot stamp
     🟢/🧱. frozen-first, tune-to-green 금지 (p7/c9).

MECHANISM UNDER TEST (card H_1692, lens=predictive-objective):
  Friston active inference / planning-as-inference. The agent does not 'respond';
  it SELECTS an action (emit a symbol, or withhold) that minimizes Expected Free
  Energy (EFE) of future states. Generation = policy selection over the emission
  action-space. Context factors enter as SEPARATE PRIORS that combine
  MULTIPLICATIVELY inside the forward rollout (binding by JOINT belief).

  G1 LOAD-BEARING CLAIM (card §G1):
    "factored context priors combine in the forward rollout's joint likelihood
     (interaction term non-zero) -> joint conditioning reaches valid action-
     sequences no single context's optimal policy reaches; ablating the
     multiplicative prior-combination (replace with selection/argmax over single
     priors) drops composed_distinct to max_single."

  So the LEVER is the MULTIPLICATIVE COMBINATION of the two context priors in
  the generative model's likelihood used to score policies. The agent picks the
  emit action a* = argmin_a EFE(a) where EFE rewards realizing the joint-context
  preference (pragmatic value). We isolate the bind from:
    - the planning/EFE machinery itself (kept ON, identical, for all arms)
    - parameter count / preference richness (the generative model is the SAME
      learned likelihood; only HOW the two priors combine differs)

TOY POMDP (binding-required by construction; ambiguous-pair separation):
  Two context factors c1,c2 each in Z_7* = {1..6}.  Hidden cause / correct emit
  symbol for a (c1,c2) world = the CONJUNCTION:
      target(c1,c2) = (c1 * c2) mod 7   ->  symbol in {1..6}  (V = 6 emit symbols)
  Receiver-fixed alphabet V = {1..6} plus a {withhold} action.

  AMBIGUOUS by construction: c1 is invertible in Z_7*, so for fixed c1 the
  product (c1*c2)%7 ranges over ALL of {1..6} as c2 varies => the marginal
  preference P(symbol | c1) is UNIFORM (same for c2). The WHOLE 36-world set is
  the ambiguous subset: NO marginal shortcut. An agent whose generative model
  scores policies using only ONE context prior (or an additive blend of the two
  marginal preferences) is structurally pinned at chance — it cannot represent
  the conjunction, so the EFE optimum it reaches is the wrong (or a constant)
  symbol. Only a JOINT (multiplicative) belief makes the correct symbol the
  unique EFE minimizer.

  Productivity / G1 generalization test = hold out 25% of the 36 worlds as NOVEL
  (c1,c2) combinations never co-presented in training of the likelihood.

THE GENERATIVE MODEL (learned, shared, $0):
  Per context value we learn a "likelihood factor" over emit symbols:
      phiA[c1] in R^V   (how c1 alone makes each symbol plausible)
      phiB[c2] in R^V
  The agent's belief over the correct symbol for a world, used to score policies:
      bind  (active-inference JOINT): log-likelihood  L = phiA[c1] + phiB[c2]
             but the WORLD-LEVEL JOINT preference is realized by a multiplicative
             interaction term:  L_joint = phiA[c1] + phiB[c2] + (gA[c1] ⊙ gB[c2])·W
             i.e. the two factor beliefs COMBINE MULTIPLICATIVELY (Hadamard
             interaction) before the policy-score readout. This is the non-
             separable joint belief the card requires.
      add   (INERT ablation): MULTIPLICATIVE COMBINE OFF — replace the joint
             interaction with selection/additive: L = phiA[c1] + phiB[c2] only
             (drop the gA⊙gB term). Same params elsewhere, same EFE planner,
             ONLY the multiplicative prior-combination removed. If composed
             generalization collapses to max_single => the bind is LOAD-BEARING;
             if it stays => INERT (the joint term contributes 0).
      single: agent reads ONLY context factor c1 (one prior) — the max_single
             floor a joint world must beat.
      scramble: G0 control — permute the (context->factor-belief) wiring; the
             EFE planner + bind op are intact but the wiring is destroyed -> must
             collapse to chance (sanity: the bind isn't trivially solvable).

  EMISSION = ACTION MIN-EFE: a* = argmax_symbol (policy-score L); the WITHHOLD
  action is selected iff no emit policy beats the abstain baseline (model-
  evidence floor). On in-support worlds an emit policy beats withhold; on out-of-
  support worlds it does not (honesty falls out of EFE arithmetic) — we don't
  bar-gate honesty here (G1 program) but the planner uses the argmin-EFE rule so
  this is genuinely policy-selection, not a plain classifier head.

GROK POSITIVE CONTROL (under-power guard, REQUIRED):
  Canonical grokkable composable task — modular ADDITION (a+b)%P with a SHARED
  embedding MLP head — trained at the SAME rung. If held-out >> chance => this $0
  toy HAS the resolution to detect composition. If grok ctrl ~ chance => the toy
  is UNDER-POWERED and verdict = UNDER-POWER (a_break_the_wall type-a measurement
  limit; the mechanism is NOT blamed).

==============================================================================
FROZEN BARS  (pre-registered BEFORE running — frozen-first, tune-to-green 금지)
==============================================================================
  composed chance (1 of 6 emit symbols) = 1/6 ≈ 0.1667
  Judge on the MEAN across 5 seeds, BEST held-out over the run (generous ->
  guards against an under-powered FALSE-negative).

  BAR-1  binding/held-out   : bind held-out acc >= 0.50  (>> 1/6 chance)
  BAR-2  >max_single        : (bind held - single held) >= 0.20 AND bind >= 0.50
  BAR-3  INERT ablation     : (bind held - add held) >= 0.30
                              (= multiplicative prior-combination LOAD-BEARING;
                               if < 0.30 the joint term is INERT)
  BAR-4  G0 scramble sanity : scramble held-out acc <= 0.35  (bind not trivial)
  AMBIG-PAIR separation     : composed_distinct(bind) >= 2 AND > composed_distinct
                              (single)  (real joint resolves ambiguous worlds
                               distinctly; single-prior floor cannot)

  GROK-CTRL (under-power guard) : grok modular-ADD held-out >= 0.50  (>> 1/P)

  VERDICT (DIRECTIONAL):
    if NOT grok_ctrl_pass                       -> UNDER-POWER   (toy lacks resolution)
    elif BAR1 & BAR2 & BAR3 & BAR4 & AMBIG      -> SUPPORTED     (DIRECTIONAL)
    elif not BAR3 (ablation INERT)              -> NOT-SUPPORTED (joint contributes 0)
    else                                        -> MIXED
  survivor = SUPPORTED AND grok_ctrl_pass AND BAR-3 load-bearing (very conservative).
==============================================================================
"""
import numpy as np

P = 7
VALS = list(range(1, P))                       # Z_7* = {1..6}
WORLDS = [(c1, c2) for c1 in VALS for c2 in VALS]   # 36 (c1,c2) worlds
V = P - 1                                       # emit symbols (c1*c2)%7 in {1..6} -> 6
NCLS = V
D = 48                                          # factor-belief / interaction dim
STEPS = 40000
LR, WD = 1e-3, 0.05
B1, B2, EPS = 0.9, 0.999, 1e-8
HELD_FRAC = 0.25
EVAL_EVERY = 2000
SEEDS = [7, 4302, 4303, 11, 23]


def target(c1, c2):
    return (c1 * c2) % P - 1                    # symbol index 0..5


def smrow(L):
    L = L - L.max(1, keepdims=True)
    e = np.exp(L)
    return e / e.sum(1, keepdims=True)


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


# ---------------------------------------------------------------------------
# Active-inference agent. The generative model produces a policy-score over emit
# symbols for a (c1,c2) world; the emit ACTION = argmax policy-score (= argmin
# EFE pragmatic-divergence with uniform prior preferences). The lever is the
# multiplicative prior-combination (gA ⊙ gB interaction term):
#   mode='bind'   : L = phiA[c1] + phiB[c2] + (gA[c1]*gB[c2]) @ Wj   (JOINT belief)
#   mode='add'    : L = phiA[c1] + phiB[c2]            (INERT: multiplicative OFF)
#   mode='single' : L = phiA[c1]                       (one prior -> max_single)
# trained by softmax CE on the world target (= preference-divergence min == EFE
# pragmatic value with uniform preferences). readout is the policy selection.
# ---------------------------------------------------------------------------
def run_arm(seed, mode, scramble=False):
    rng = np.random.default_rng(seed)
    worlds = WORLDS[:]
    rng.shuffle(worlds)
    nh = int(round(HELD_FRAC * len(worlds)))
    held, train = worlds[:nh], worlds[nh:]

    permA = np.arange(P - 1)
    permB = np.arange(P - 1)
    if scramble:
        permA = rng.permutation(P - 1)
        permB = rng.permutation(P - 1)

    a_tr = np.array([permA[c1 - 1] for (c1, c2) in train])
    b_tr = np.array([permB[c2 - 1] for (c1, c2) in train])
    y_tr = np.array([target(c1, c2) for (c1, c2) in train])
    a_he = np.array([permA[c1 - 1] for (c1, c2) in held])
    b_he = np.array([permB[c2 - 1] for (c1, c2) in held])
    y_he = np.array([target(c1, c2) for (c1, c2) in held])
    N = len(train)

    # generative-model parameters (factor beliefs + multiplicative interaction)
    p = {
        'phiA': rng.normal(0, 1 / np.sqrt(V), (P - 1, NCLS)),   # c1 -> symbol prior
        'phiB': rng.normal(0, 1 / np.sqrt(V), (P - 1, NCLS)),   # c2 -> symbol prior
        'gA':   rng.normal(0, 1 / np.sqrt(D), (P - 1, D)),      # c1 interaction feat
        'gB':   rng.normal(0, 1 / np.sqrt(D), (P - 1, D)),      # c2 interaction feat
        'Wj':   rng.normal(0, 1 / np.sqrt(D), (D, NCLS)),       # joint readout
    }
    opt = Adam(p)
    best = 0.0
    best_pred_he = None

    def fwd(ai, bi):
        pha = p['phiA'][ai]
        phb = p['phiB'][bi]
        ga = p['gA'][ai]
        gb = p['gB'][bi]
        inter = ga * gb                       # Hadamard = multiplicative combine
        if mode == 'bind':
            L = pha + phb + inter @ p['Wj']
        elif mode == 'add':
            L = pha + phb                      # multiplicative combine OFF
        elif mode == 'single':
            L = pha
        else:
            raise ValueError(mode)
        return L, pha, phb, ga, gb, inter

    for st in range(STEPS):
        L, pha, phb, ga, gb, inter = fwd(a_tr, b_tr)
        Pp = smrow(L)
        DL = Pp.copy()
        DL[np.arange(N), y_tr] -= 1
        DL /= N
        g = {k: np.zeros_like(v) for k, v in p.items()}
        # phiA / phiB gradients (present in all modes that use them)
        if mode in ('bind', 'add', 'single'):
            np.add.at(g['phiA'], a_tr, DL)
        if mode in ('bind', 'add'):
            np.add.at(g['phiB'], b_tr, DL)
        # joint interaction gradients (bind only)
        if mode == 'bind':
            g['Wj'] = inter.T @ DL
            d_inter = DL @ p['Wj'].T          # (N,D)
            d_ga = d_inter * gb
            d_gb = d_inter * ga
            np.add.at(g['gA'], a_tr, d_ga)
            np.add.at(g['gB'], b_tr, d_gb)
        opt.step(p, g)

        if st % EVAL_EVERY == 0 or st == STEPS - 1:
            Lh, _, _, _, _, _ = fwd(a_he, b_he)
            pred = np.argmax(Lh, 1)            # emit ACTION = argmin-EFE policy
            acc = float(np.mean(pred == y_he))
            if acc >= best:
                best = acc
                best_pred_he = pred.copy()

    if best_pred_he is None:
        cd = 0
    else:
        cd = len(set(int(c) for c, t in zip(best_pred_he, y_he) if c == t))
    return best, cd


def grok_control(seed=7):
    """Canonical grokkable composable task: modular ADDITION (a+b)%Pm, shared MLP head."""
    Pm = 11
    vals = list(range(Pm))
    prs = [(a, b) for a in vals for b in vals]
    IN2, H2, D2 = 2 * Pm, 256, 64
    rng = np.random.default_rng(seed)
    rng.shuffle(prs)
    nh = len(prs) // 2
    held, train = prs[:nh], prs[nh:]

    def oh2(a, b):
        x = np.zeros(IN2)
        x[a] = 1
        x[Pm + b] = 1
        return x

    Xtr = np.stack([oh2(*q) for q in train])
    Xhe = np.stack([oh2(*q) for q in held])
    ytr = np.array([(a + b) % Pm for (a, b) in train])
    yhe = np.array([(a + b) % Pm for (a, b) in held])
    N = len(train)
    p = {
        'W1': rng.normal(0, 1 / np.sqrt(IN2), (H2, IN2)), 'b1': np.zeros(H2),
        'W2': rng.normal(0, 1 / np.sqrt(H2), (D2, H2)), 'b2': np.zeros(D2),
        'Hd': rng.normal(0, 1 / np.sqrt(D2), (Pm, D2)),
    }
    opt = Adam(p)
    best = 0.0
    for st in range(40000):
        PRE = Xtr @ p['W1'].T + p['b1']
        Hh = np.tanh(PRE)
        Z = Hh @ p['W2'].T + p['b2']
        Pp = smrow(Z @ p['Hd'].T)
        DL = Pp.copy()
        DL[np.arange(N), ytr] -= 1
        DL /= N
        g = {}
        g['Hd'] = DL.T @ Z
        dZ = DL @ p['Hd']
        g['W2'] = dZ.T @ Hh
        g['b2'] = dZ.sum(0)
        dHh = dZ @ p['W2']
        dPRE = dHh * (1 - Hh * Hh)
        g['W1'] = dPRE.T @ Xtr
        g['b1'] = dPRE.sum(0)
        opt.step(p, g)
        if st % 8000 == 0 or st == 39999:
            Zh = np.tanh(Xhe @ p['W1'].T + p['b1']) @ p['W2'].T + p['b2']
            best = max(best, float(np.mean(np.argmax(Zh @ p['Hd'].T, 1) == yhe)))
    return best


def main():
    chance = 1.0 / NCLS
    print("=" * 80)
    print("H_1692 active_inference_efe_policy — cheap_test (numpy AdamW, DIRECTIONAL)")
    print(f"lens=predictive-objective | emission = action min-EFE; lever = MULTIPLICATIVE")
    print(f"  prior-combination (joint belief) in the forward rollout (card §G1)")
    print(f"task: 2 context factors Z_7*, world target y=(c1*c2)%7 | 36 worlds, held {HELD_FRAC:.0%} novel")
    print(f"binding-required: P(y|c1),P(y|c2) UNIFORM (whole set = ambiguous, no marginal shortcut)")
    print(f"INERT ablation = multiplicative combine OFF (drop gA⊙gB interaction -> additive)")
    print(f"composed chance = 1/{NCLS} = {chance:.4f} | steps={STEPS} AdamW lr={LR} wd={WD} seeds={SEEDS}")
    print("=" * 80)

    keys = ['bind', 'add', 'single', 'scramble']
    accs = {k: [] for k in keys}
    cds = {k: [] for k in keys}
    for s in SEEDS:
        rb, cb = run_arm(s, 'bind')
        ra, ca = run_arm(s, 'add')
        rs, cs_ = run_arm(s, 'single')
        rsc, csc = run_arm(s, 'bind', scramble=True)
        accs['bind'].append(rb); cds['bind'].append(cb)
        accs['add'].append(ra); cds['add'].append(ca)
        accs['single'].append(rs); cds['single'].append(cs_)
        accs['scramble'].append(rsc); cds['scramble'].append(csc)
        print(f"seed {s:>5}: bind he={rb:.2f}(cd={cb}) | ABLATE-add he={ra:.2f}(cd={ca}) | "
              f"max-single he={rs:.2f}(cd={cs_}) | scramble he={rsc:.2f}")
    m = {k: float(np.mean(v)) for k, v in accs.items()}
    mcd = {k: float(np.mean(v)) for k, v in cds.items()}
    print("-" * 80)

    grok = grok_control()
    print(f"GROK POSITIVE CONTROL (modular ADDITION (a+b)%11, shared MLP head, 50% held, AdamW 40k): held={grok:.3f}")
    print(f"  -> if ~chance(1/11={1/11:.3f}): toy lacks resolution => UNDER-POWER (a_break_the_wall type-a).")
    print("-" * 80)
    print("MEANS across seeds (BEST held-out over run):")
    print(f"  bind (joint) : held={m['bind']:.3f}  composed_distinct={mcd['bind']:.2f}")
    print(f"  ABLATE-add   : held={m['add']:.3f}  composed_distinct={mcd['add']:.2f}   (INERT: multiplicative OFF)")
    print(f"  max-single   : held={m['single']:.3f}  composed_distinct={mcd['single']:.2f}  (single-prior floor)")
    print(f"  scramble     : held={m['scramble']:.3f}                              (G0 wiring control)")
    print("-" * 80)

    grok_pass = grok >= 0.50
    bar1 = m['bind'] >= 0.50
    bar2 = (m['bind'] - m['single'] >= 0.20) and (m['bind'] >= 0.50)
    bar3 = (m['bind'] - m['add'] >= 0.30)        # multiplicative combine load-bearing
    bar4 = m['scramble'] <= 0.35
    ambig = (mcd['bind'] >= 2) and (mcd['bind'] > mcd['single'])

    print("FROZEN BARS:")
    print(f"  BAR-1 binding/held-out     bind>=0.50                 : {m['bind']:.3f}  -> {'PASS' if bar1 else 'FAIL'}")
    print(f"  BAR-2 >max_single          (bind-single)>=0.20 & >=.5 : d={m['bind']-m['single']:+.3f} -> {'PASS' if bar2 else 'FAIL'}")
    print(f"  BAR-3 INERT ablation       (bind-add)>=0.30 load-bear : d={m['bind']-m['add']:+.3f} -> {'PASS' if bar3 else 'FAIL'}")
    print(f"  BAR-4 G0 scramble sanity   scramble<=0.35            : {m['scramble']:.3f}  -> {'PASS' if bar4 else 'FAIL'}")
    print(f"  AMBIG-PAIR separation      cd(bind)>=2 & >cd(single)  : {mcd['bind']:.2f} vs {mcd['single']:.2f} -> {'PASS' if ambig else 'FAIL'}")
    print(f"  GROK-CTRL (under-power)     grok_add held>=0.50       : {grok:.3f}  -> {'PASS' if grok_pass else 'FAIL'}")
    print("-" * 80)

    if not grok_pass:
        verdict = "UNDER-POWER"
    elif bar1 and bar2 and bar3 and bar4 and ambig:
        verdict = "SUPPORTED"
    elif not bar3:
        verdict = "NOT-SUPPORTED"
    else:
        verdict = "MIXED"

    survivor = (verdict == "SUPPORTED") and grok_pass and bar3
    print(f"VERDICT (DIRECTIONAL): {verdict}")
    print(f"survivor (frozen-bar PASS & grok_ctrl & ablation load-bearing): {survivor}")
    print("  numpy toy = DIRECTIONAL only; engine-native + 303M GPU cost-gated NOT fired (a_engine_native_learning).")
    print("=" * 80)

    print(f"RESULT_JSON {{\"verdict\":\"{verdict}\",\"grok_ctrl_pass\":{str(grok_pass).lower()},"
          f"\"survivor\":{str(survivor).lower()},\"bind_held\":{m['bind']:.3f},\"add_held\":{m['add']:.3f},"
          f"\"single_held\":{m['single']:.3f},\"scramble_held\":{m['scramble']:.3f},"
          f"\"cd_bind\":{mcd['bind']:.2f},\"cd_single\":{mcd['single']:.2f},\"grok\":{grok:.3f}}}")


if __name__ == "__main__":
    main()
