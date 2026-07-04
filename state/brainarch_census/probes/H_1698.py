#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
H_1698 — Prefrontal-BG Gated Slot Register (PBWM) — variable binding by gated WM
================================================================================
cheap_test ($0, numpy toy, mini-safe, CPU ~minutes) — DIRECTIONAL ONLY.

  ⚠️ MEASUREMENT PATH: numpy toy = DIRECTIONAL (NOT engine-native,
     a_engine_native_learning). No cli/anima.hexa, no core/g_gates. The toy
     decides the DIRECTION of the architecture, NOT a terminal G0/G1/G2 verdict.
     Engine-native (single dispatch → generator L3 → g_gates/g6) + 303M GPU is
     cost-gated PRE-REGISTER ONLY (NOT fired). numpy cannot stamp 🟢/🧱.

MECHANISM UNDER TEST (card H_1698):
  O'Reilly-Frank PBWM: basal ganglia gate WHAT enters role-slot registers
  S1..Sk (input-gate per slot); once distinct fillers are gated into distinct
  role slots, a NON-SEPARABLE cross-slot CONJUNCTION operator over the bound
  (role,filler) tuples produces the emitted structured frame. The LOAD-BEARING
  claim is: the cross-slot conjunction (the bind) is what lets composed frames
  exceed any single slot — remove it (separable / additive readout) and you
  collapse to the max-single floor (= Fodor-Pylyshyn systematicity, not scale).

  The lever is therefore the CONJUNCTION OPERATOR, isolated here from:
    - whether the slots are filled (gating policy — kept ON for all arms)
    - parameter count / depth (arch FIXED across arms; only the readout differs)

TOY TASK (binding-required by construction; ambiguous-pair separation):
  Two role-slots: ROLE-A filler a ∈ Z_7* = {1..6}, ROLE-B filler b ∈ Z_7* = {1..6}.
  36 (a,b) "bound frames". Frame label = the conjunction target:
      y = (a * b) mod 7   (multiplicative ⇒ NON-separable / requires the joint)
  MARGINALS CARRY ~ZERO INFO: a is invertible in Z_7*, so for fixed a the product
  (a*b)%7 ranges over ALL of {1..6} as b varies ⇒ P(y|a) and P(y|b) are UNIFORM.
  The WHOLE set is the AMBIGUOUS subset: there is NO marginal shortcut — a model
  that only reads ROLE-A or ROLE-B (no cross-slot bind) is structurally pinned at
  chance. Productivity test = generalize to (a,b) combos never co-presented.

SPLIT: hold out 25% of 36 frames (9) as NOVEL role×filler combinations.

ARMS (SAME gated slot encoder; ONLY the cross-slot READOUT differs — isolate the
      CONJUNCTION OPERATOR as lever, arch otherwise fixed, a_no_llm_frame_trap):
  PBWM-bind  : slot embeddings ea=Ea[a], eb=Eb[b]; cross-slot CONJUNCTION via a
               bilinear/Hadamard bind  z = (ea ⊙ eb)  → readout = the proposed op.
               (Hadamard of two role-slot vectors = the literal non-separable bind.)
  ABLATE-add : INERT ablation — cross-weight OFF: product→add. z = (ea + eb).
               Same params, same slots, ONLY the bind operator removed → if this
               collapses to max_single = the conjunction is LOAD-BEARING; if it
               stays = INERT (the bind contributes 0).
  max-single : read ONLY ROLE-A slot (single filled slot, no second-slot bind) =
               the max_single floor a bound frame must beat.
  scramble   : G0 control — shuffle the (slot→evidence) map; bind op intact but
               wiring destroyed → must collapse to chance (sanity the bind isn't
               trivially solvable).

GROK POSITIVE CONTROL (under-power guard, REQUIRED):
  A canonical grokkable composable task — modular ADDITION (a+b)%P with a SHARED
  embedding head — trained at the SAME rung. If held-out ≫ chance ⇒ this $0 toy
  HAS the resolution to detect composition. If grok ctrl ≈ chance ⇒ the toy is
  UNDER-POWERED and the verdict is UNDER-POWER (NOT a science ceiling; a_break_
  the_wall type-a measurement limit) — the mechanism is not blamed.

==============================================================================
FROZEN BARS  (pre-registered BEFORE running — frozen-first, tune-to-green 금지 p7/c9)
==============================================================================
  composed chance (1 of 6 classes) = 1/6 ≈ 0.1667

  Judge on the MEAN across 5 seeds, BEST held-out over the run (generous → guards
  against an under-powered FALSE-negative).

  BAR-1  binding/held-out   : PBWM-bind held-out acc >= 0.50  (≫ 1/6 chance)
  BAR-2  >max_single        : (PBWM held - max-single held) >= 0.20
                              AND PBWM held >= 0.50
  BAR-3  INERT ablation     : (PBWM held - ABLATE-add held) >= 0.30
                              (= the cross-slot conjunction is LOAD-BEARING;
                               if < 0.30 the bind is INERT)
  BAR-4  G0 scramble sanity : scramble held-out acc <= 0.35  (bind not trivial)
  AMBIG-PAIR separation     : composed_distinct(PBWM) >= 2 AND > composed_distinct(
                              max-single)   (real bind 1.0 vs copy 0.5 logic:
                              PBWM resolves ambiguous frames distinctly, the
                              single-slot floor cannot)

  GROK-CTRL (under-power guard) : grok modular-ADD held-out >= 0.50  (≫ 1/P)

  VERDICT (DIRECTIONAL):
    if NOT grok_ctrl_pass                       -> UNDER-POWER   (toy lacks resolution)
    elif BAR-1 & BAR-2 & BAR-3 & BAR-4 & AMBIG  -> SUPPORTED     (DIRECTIONAL)
    elif not BAR-3 (ablation INERT)             -> NOT-SUPPORTED (bind contributes 0)
    else                                        -> MIXED
  survivor = SUPPORTED AND grok_ctrl_pass AND BAR-3 load-bearing (very conservative).
==============================================================================
"""
import numpy as np

P = 7
VALS = list(range(1, P))                       # Z_7* = {1..6}
PAIRS = [(a, b) for a in VALS for b in VALS]   # 36 bound frames
NCLS = P - 1                                    # product (a*b)%7 ∈ {1..6} -> 6 classes
IN = P - 1                                      # one-hot filler dim per slot (6)
D = 48                                          # slot-embedding dim
STEPS = 40000
LR, WD = 1e-3, 0.05
B1, B2, EPS = 0.9, 0.999, 1e-8
HELD_FRAC = 0.25
EVAL_EVERY = 2000
SEEDS = [7, 4302, 4303, 11, 23]


def prod_y(a, b):
    return (a * b) % P - 1                      # class index 0..5


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
# A gated-slot register model.  Each role-slot holds an embedding of its gated
# filler (ea=Ea[a], eb=Eb[b]).  The cross-slot bind is the lever:
#   mode='bind'    : z = ea * eb       (Hadamard conjunction = non-separable bind)
#   mode='add'     : z = ea + eb       (INERT ablation: cross-weight OFF)
#   mode='single'  : z = ea            (only ROLE-A slot read -> max_single floor)
# readout: linear head z -> NCLS classes (softmax CE).
# ---------------------------------------------------------------------------
def run_arm(seed, mode, scramble=False):
    rng = np.random.default_rng(seed)
    pairs = PAIRS[:]
    rng.shuffle(pairs)
    nh = int(round(HELD_FRAC * len(pairs)))
    held, train = pairs[:nh], pairs[nh:]

    # scramble control: permute the filler->evidence map (destroy slot wiring)
    permA = np.arange(P - 1)
    permB = np.arange(P - 1)
    if scramble:
        permA = rng.permutation(P - 1)
        permB = rng.permutation(P - 1)

    ai_tr = np.array([permA[a - 1] for (a, b) in train])
    bi_tr = np.array([permB[b - 1] for (a, b) in train])
    y_tr = np.array([prod_y(a, b) for (a, b) in train])
    ai_he = np.array([permA[a - 1] for (a, b) in held])
    bi_he = np.array([permB[b - 1] for (a, b) in held])
    y_he = np.array([prod_y(a, b) for (a, b) in held])
    N = len(train)

    p = {
        'Ea': rng.normal(0, 1 / np.sqrt(IN), (P - 1, D)),
        'Eb': rng.normal(0, 1 / np.sqrt(IN), (P - 1, D)),
        'Hd': rng.normal(0, 1 / np.sqrt(D), (NCLS, D)),
    }
    opt = Adam(p)
    best = 0.0
    best_pred_he = None

    def fwd(ai, bi):
        ea = p['Ea'][ai]
        eb = p['Eb'][bi]
        if mode == 'bind':
            z = ea * eb
        elif mode == 'add':
            z = ea + eb
        elif mode == 'single':
            z = ea
        else:
            raise ValueError(mode)
        return z, ea, eb

    for st in range(STEPS):
        z, ea, eb = fwd(ai_tr, bi_tr)
        L = z @ p['Hd'].T
        Pp = smrow(L)
        DL = Pp.copy()
        DL[np.arange(N), y_tr] -= 1
        DL /= N
        g = {k: np.zeros_like(v) for k, v in p.items()}
        g['Hd'] = DL.T @ z
        dz = DL @ p['Hd']
        if mode == 'bind':
            dEa = dz * eb
            dEb = dz * ea
            np.add.at(g['Ea'], ai_tr, dEa)
            np.add.at(g['Eb'], bi_tr, dEb)
        elif mode == 'add':
            np.add.at(g['Ea'], ai_tr, dz)
            np.add.at(g['Eb'], bi_tr, dz)
        elif mode == 'single':
            np.add.at(g['Ea'], ai_tr, dz)
        opt.step(p, g)

        if st % EVAL_EVERY == 0 or st == STEPS - 1:
            zh, _, _ = fwd(ai_he, bi_he)
            pred = np.argmax(zh @ p['Hd'].T, 1)
            acc = float(np.mean(pred == y_he))
            if acc >= best:
                best = acc
                best_pred_he = pred.copy()

    # composed_distinct = # of distinct correctly-predicted held-out classes
    if best_pred_he is None:
        cd = 0
    else:
        cd = len(set(int(c) for c, t in zip(best_pred_he, y_he) if c == t))
    return best, cd


def grok_control(seed=7):
    """Canonical grokkable composable task: modular ADDITION (a+b)%Pm, shared head."""
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
    print("H_1698 pbwm_gated_slot_register — cheap_test (numpy AdamW, DIRECTIONAL)")
    print(f"task: 2 role-slots Z_7* fillers, frame label y=(a*b)%7 | 36 frames, held {HELD_FRAC:.0%} novel")
    print(f"binding-required: P(y|a),P(y|b) UNIFORM (whole set = ambiguous subset, no marginal shortcut)")
    print(f"lever = cross-slot CONJUNCTION op (Hadamard bind); INERT ablation = product->add")
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
        print(f"seed {s:>5}: PBWM-bind he={rb:.2f}(cd={cb}) | ABLATE-add he={ra:.2f}(cd={ca}) | "
              f"max-single he={rs:.2f}(cd={cs_}) | scramble he={rsc:.2f}")
    m = {k: float(np.mean(v)) for k, v in accs.items()}
    mcd = {k: float(np.mean(v)) for k, v in cds.items()}
    print("-" * 80)

    grok = grok_control()
    print(f"GROK POSITIVE CONTROL (modular ADDITION (a+b)%11, shared head, 50% held, AdamW 40k): held={grok:.3f}")
    print(f"  -> if ~chance(1/11={1/11:.3f}): toy lacks resolution => UNDER-POWER (a_break_the_wall type-a).")
    print("-" * 80)
    print("MEANS across seeds (BEST held-out over run):")
    print(f"  PBWM-bind   : held={m['bind']:.3f}  composed_distinct={mcd['bind']:.2f}")
    print(f"  ABLATE-add  : held={m['add']:.3f}  composed_distinct={mcd['add']:.2f}   (INERT ablation: bind OFF)")
    print(f"  max-single  : held={m['single']:.3f}  composed_distinct={mcd['single']:.2f}  (single-slot floor)")
    print(f"  scramble    : held={m['scramble']:.3f}                              (G0 wiring control)")
    print("-" * 80)

    grok_pass = grok >= 0.50
    bar1 = m['bind'] >= 0.50
    bar2 = (m['bind'] - m['single'] >= 0.20) and (m['bind'] >= 0.50)
    bar3 = (m['bind'] - m['add'] >= 0.30)        # ablation load-bearing
    bar4 = m['scramble'] <= 0.35
    ambig = (mcd['bind'] >= 2) and (mcd['bind'] > mcd['single'])

    print("FROZEN BARS:")
    print(f"  BAR-1 binding/held-out     PBWM>=0.50                 : {m['bind']:.3f}  -> {'PASS' if bar1 else 'FAIL'}")
    print(f"  BAR-2 >max_single          (PBWM-single)>=0.20 & >=.5 : d={m['bind']-m['single']:+.3f} -> {'PASS' if bar2 else 'FAIL'}")
    print(f"  BAR-3 INERT ablation       (PBWM-add)>=0.30 load-bear : d={m['bind']-m['add']:+.3f} -> {'PASS' if bar3 else 'FAIL'}")
    print(f"  BAR-4 G0 scramble sanity   scramble<=0.35            : {m['scramble']:.3f}  -> {'PASS' if bar4 else 'FAIL'}")
    print(f"  AMBIG-PAIR separation      cd(PBWM)>=2 & >cd(single)  : {mcd['bind']:.2f} vs {mcd['single']:.2f} -> {'PASS' if ambig else 'FAIL'}")
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

    # machine-readable tail
    print(f"RESULT_JSON {{\"verdict\":\"{verdict}\",\"grok_ctrl_pass\":{str(grok_pass).lower()},"
          f"\"survivor\":{str(survivor).lower()},\"bind_held\":{m['bind']:.3f},\"add_held\":{m['add']:.3f},"
          f"\"single_held\":{m['single']:.3f},\"scramble_held\":{m['scramble']:.3f},"
          f"\"cd_bind\":{mcd['bind']:.2f},\"cd_single\":{mcd['single']:.2f},\"grok\":{grok:.3f}}}")


if __name__ == "__main__":
    main()
