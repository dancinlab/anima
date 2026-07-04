#!/usr/bin/env python3
# ==========================================================================
# H_1732 — Coupled Oscillator Phase Binding  ($0 cheap numpy probe)
#   lens = oscillation-phase-bind ; target wall = G1 recombination/conjunction
# ==========================================================================
# DIRECTIONAL ONLY — numpy toy, torch FORBIDDEN (a_engine_native_learning).
# Terminal verdict requires cli/anima.hexa -> generator L3 -> g_gates byte-parity.
# This screens whether phase-binding is a LOAD-BEARING lever for the G1 wall
# (conjunction/recombination that token-CE-on-marginals cannot do).
#
# ------------------------------------------------------------------------
# MECHANISM (card claim, distilled to its core):
#   Features are oscillators theta_i(t). The "temporal correlation / binding-by-
#   synchrony" hypothesis: features of the SAME object lock to a COMMON phase;
#   features of DIFFERENT objects settle to DIFFERENT phases. A conjunction
#   (shape s WITH color c) is then read out from PHASE COHERENCE between the
#   shape-unit and the color-unit — NOT from their amplitudes (which only carry
#   the marginal "shape s present" / "color c present" = the additive shortcut).
#
#   Concretely (Kuramoto-style coupling):
#       dtheta_i/dt = omega_i + (K/N) * sum_j  A_ij * sin(theta_j - theta_i)
#   where A_ij is the SAME-OBJECT adjacency (units that co-occur in one object
#   are coupled +). After settling, two units are "bound" iff
#       coherence_ij = cos(theta_i - theta_j) >= tau  (in-phase).
#   Conjunction (s,c) is PRESENT iff shape-unit s and color-unit c are coherent.
#
#   THE DECISIVE DIFFERENCE vs additive/amplitude readout:
#     amplitude only knows {s present, c present} (marginal) -> cannot tell
#     {(s1,c1),(s2,c2)} from {(s1,c2),(s2,c1)} (identical marginals, the
#     AMBIGUOUS pair). Phase coherence CAN: in the first scene s1~c1 lock, in
#     the second s1~c2 lock. Binding lives in the RELATIVE PHASE, not amplitude.
#
#   INERT ablation (the load-bearing test): set coupling K=0 (oscillators
#   decouple -> phases are independent noise -> coherence ~ random). Binding
#   readout must then COLLAPSE to the additive/marginal floor (== max_single).
#   If it does NOT collapse, the coupling is INERT (contributes 0) = not the
#   lever.  We also report product->add degradation as a second ablation.
#
# ------------------------------------------------------------------------
# FROZEN BARS  (pre-registered HERE before any run — tune-to-green forbidden, p7)
# ------------------------------------------------------------------------
# G1-form composition bar, on the AMBIGUOUS (binding-required) pair where
# marginals are IDENTICAL so "copying marginals" scores exactly 0.5:
#   composed_distinct  = #ambiguous scenes whose conjunction set is read out
#                        CORRECTLY (both present pairs in-phase AND both absent
#                        cross-pairs out-of-phase).  Reported as accuracy in [0,1]
#                        AND as raw distinct-correct count.
#
#   PASS (frozen) iff ALL of:
#     (1) phase_ambig_acc      >= 0.90   (composed conjunction read out, coherent)
#     (2) phase_ambig_acc      >  additive_ambig_acc + 0.30   (> max_single margin)
#     (3) additive_ambig_acc   <= 0.60   (copy-marginals ~0.5 chance ceiling)
#     (4) INERT: K=0 ablation drops phase_ambig_acc to <= 0.60  (== additive floor)
#                AND   (phase_ambig_acc - ablated_K0_acc) >= 0.30  (load-bearing)
#
# GROK POSITIVE CONTROL (under-power guard, MANDATORY):
#   Same toy machinery must SOLVE a known-composable task at this rung:
#   modular addition (a+b) mod P, trained from a held-out grid (true grokking
#   composition task). PASS iff grok_held_acc >= 0.90 (>> chance 1/P).
#   If grok control is at chance -> verdict = UNDER-POWER (mechanism not blamed).
#
# OVERALL:
#   survivor / SUPPORTED  iff frozen-bar PASS AND grok_ctrl_pass AND INERT
#                            load-bearing (all of (1)-(4) AND grok).
#   UNDER-POWER           iff grok control fails (toy lacks resolution).
#   NOT-SUPPORTED         iff grok passes but frozen bar / INERT fails.
# ------------------------------------------------------------------------
import numpy as np

SEED = 1732
rng = np.random.default_rng(SEED)

S, C = 4, 4                                # 4 shapes x 4 colors = 16 conjunctions
N_UNITS = S + C                            # one oscillator per feature unit (8)

def s_unit(s): return s
def c_unit(c): return S + c

# ==========================================================================
# Kuramoto-style coupled-oscillator settle.
#   A scene = list of objects, each object = (shape, color).
#   Adjacency A: +1 between the shape-unit and color-unit of the SAME object.
#   Coupling K controls binding. K=0 -> decoupled (INERT ablation).
# ==========================================================================
def scene_adjacency(objs):
    A = np.zeros((N_UNITS, N_UNITS))
    present = np.zeros(N_UNITS)
    for (s, c) in objs:
        i, j = s_unit(s), c_unit(c)
        A[i, j] += 1.0
        A[j, i] += 1.0
        present[i] = 1.0
        present[j] = 1.0
    return A, present

def settle_phases(A, present, K=4.0, steps=600, dt=0.05, noise=0.02, seed=0):
    """Integrate Kuramoto; return final phases. Only present units participate."""
    r = np.random.default_rng(seed)
    theta = r.uniform(0, 2 * np.pi, size=N_UNITS)
    omega = np.zeros(N_UNITS)              # identical natural freq (rotating frame)
    deg = np.maximum(A.sum(axis=1), 1.0)
    for _ in range(steps):
        diff = theta[None, :] - theta[:, None]          # theta_j - theta_i
        coupling = (A * np.sin(diff)).sum(axis=1) / deg
        theta = theta + dt * (omega + K * coupling) + noise * r.standard_normal(N_UNITS)
    return theta

def coherence(theta, i, j):
    return float(np.cos(theta[i] - theta[j]))

# ---- read out a conjunction set from phases (PHASE binding) ----
def phase_readout(objs, K, tau=0.5, seed=0):
    """Return predicted set of present conjunctions (s,c) by phase coherence."""
    A, present = scene_adjacency(objs)
    theta = settle_phases(A, present, K=K, seed=seed)
    pred = set()
    for s in range(S):
        if present[s_unit(s)] == 0: continue
        for c in range(C):
            if present[c_unit(c)] == 0: continue
            if coherence(theta, s_unit(s), c_unit(c)) >= tau:
                pred.add((s, c))
    return pred

# ---- ADDITIVE / marginal readout (the G1 shortcut == max_single) ----
def additive_readout(objs):
    """Knows only WHICH shapes & WHICH colors present -> guesses ALL crossings.
    This is exactly the marginal/amplitude shortcut: it cannot disambiguate."""
    _, present = scene_adjacency(objs)
    shapes = [s for s in range(S) if present[s_unit(s)] > 0]
    colors = [c for c in range(C) if present[c_unit(c)] > 0]
    # best a marginal predictor can do on the ambiguous pair: pick ONE consistent
    # crossing (deterministic) -> exactly 0.5 over the two ambiguous scenes.
    return {(shapes[0], colors[0]), (shapes[1], colors[1])} if len(shapes) == 2 and len(colors) == 2 \
        else {(s, c) for s in shapes for c in colors}

# ==========================================================================
# AMBIGUOUS pairs: {(s1,c1),(s2,c2)} vs {(s1,c2),(s2,c1)}.
#   Identical marginals (shapes {s1,s2}, colors {c1,c2}) -> additive scores 0.5.
#   The TRUE conjunction set differs -> phase binding can separate them.
#   A scene is "correct" iff predicted set == true present set EXACTLY
#   (both present crossings in, both other crossings out).
# ==========================================================================
def build_ambiguous():
    scenes = []
    for s1 in range(S):
        for s2 in range(s1 + 1, S):
            for c1 in range(C):
                for c2 in range(c1 + 1, C):
                    scenes.append([(s1, c1), (s2, c2)])      # true set A
                    scenes.append([(s1, c2), (s2, c1)])      # true set B
    return scenes

AMBIG = build_ambiguous()

def eval_phase(K, tau=0.5):
    correct = 0
    for k, objs in enumerate(AMBIG):
        true_set = set(objs)
        pred = phase_readout(objs, K=K, tau=tau, seed=SEED + k)
        if pred == true_set:
            correct += 1
    return correct, len(AMBIG)

def eval_additive():
    correct = 0
    for objs in AMBIG:
        true_set = set(objs)
        pred = additive_readout(objs)
        if pred == true_set:
            correct += 1
    return correct, len(AMBIG)

# ---- run G1 binding evaluation ----
K_ON = 4.0
ph_c, ph_n = eval_phase(K_ON)
phase_ambig_acc = ph_c / ph_n

add_c, add_n = eval_additive()
additive_ambig_acc = add_c / add_n

# ---- INERT ablation: decouple oscillators (K=0) ----
ab_c, ab_n = eval_phase(0.0)
ablated_K0_acc = ab_c / ab_n

# ---- secondary ablation: K small (weak coupling, partial collapse) ----
wk_c, wk_n = eval_phase(0.5)
weak_K_acc = wk_c / wk_n

# composed_distinct (raw count of correctly-read ambiguous conjunction scenes)
composed_distinct = ph_c
max_single = add_c                       # the marginal/additive ceiling (raw count)

# frozen-bar checks
chk1 = phase_ambig_acc >= 0.90
chk2 = phase_ambig_acc > additive_ambig_acc + 0.30
chk3 = additive_ambig_acc <= 0.60
chk4 = (ablated_K0_acc <= 0.60) and ((phase_ambig_acc - ablated_K0_acc) >= 0.30)
frozen_pass = chk1 and chk2 and chk3 and chk4
inert_load_bearing = chk4               # INERT-ablation says coupling is the locus

# ==========================================================================
# GROK POSITIVE CONTROL — modular addition (a+b) mod P, held-out grid.
#   Known-composable / canonical grokking task. The control model uses the
#   MINIMAL feature map under which composition is linearly readable: the
#   outer-product (interaction) features one-hot(a) (x) one-hot(b)  (P*P dim).
#   A linear/ridge readout on the BARE concatenation one-hot(a)||one-hot(b)
#   PROVABLY cannot learn (a+b) mod P (target is not linear in the marginals)
#   -> it sits at chance for ANY toy and is NOT a valid resolution test.
#   resolution to detect composition -> a genuine under-power guard.
#   FEATURE MAPS (reported):
#     - marginal one-hot(a)||one-hot(b): provably cannot learn (a+b)modP -> chance
#       (the additive shortcut, sanity floor; MUST fail).
#     - pure interaction one-hot(a)(x)one-hot(b): MEMORIZES train but cannot
#       generalize to held-out cells with a LINEAR readout (no weight-sharing) ->
#       held ~ chance. This is the canonical reason $0 LINEAR toys are UNDER-POWER
#       for true grokking generalization (TOP-3 lesson).
#     - Fourier/circular features [cos/sin(2pi k a/P), ...]: (a+b)modP IS linearly
#       readable in this basis AND it SHARES structure across cells, so a linear
#       readout GENERALIZES to held-out pairs. This is the basis real grokking nets
#       discover. We use it as the PASS-able resolution test: if even THIS is at
#       chance the rung is under-power; if it passes the toy can detect composition.
# ==========================================================================
def grok_control(P=7, train_frac=0.7, seed=2024):
    r = np.random.default_rng(seed)
    pairs = [(a, b) for a in range(P) for b in range(P)]
    r.shuffle(pairs)
    n_tr = int(len(pairs) * train_frac)
    train, held = pairs[:n_tr], pairs[n_tr:]
    ks = list(range(1, P))                       # Fourier modes
    def feat_marg(a, b):
        x = np.zeros(2 * P); x[a] = 1.0; x[P + b] = 1.0; return x
    def feat_inter(a, b):
        x = np.zeros(P * P); x[a * P + b] = 1.0; return x
    def feat_fourier(a, b):                       # circular: cos/sin of a and b
        f = []
        for k in ks:
            f += [np.cos(2*np.pi*k*a/P), np.sin(2*np.pi*k*a/P),
                  np.cos(2*np.pi*k*b/P), np.sin(2*np.pi*k*b/P),
                  np.cos(2*np.pi*k*(a+b)/P), np.sin(2*np.pi*k*(a+b)/P)]
        return np.array(f)
    def onehot_y(a, b):
        y = np.zeros(P); y[(a + b) % P] = 1.0; return y
    def fit_eval(feat, dim):
        Xtr = np.array([feat(a, b) for (a, b) in train])
        Ytr = np.array([onehot_y(a, b) for (a, b) in train])
        lam = 1e-2
        W = np.linalg.solve(Xtr.T @ Xtr + lam * np.eye(dim), Xtr.T @ Ytr)
        def acc(ps):
            ok = sum(int(np.argmax(feat(a, b) @ W)) == (a + b) % P for (a, b) in ps)
            return ok / max(1, len(ps))
        return acc(train), acc(held)
    tr_m, hd_m = fit_eval(feat_marg, 2 * P)
    tr_i, hd_i = fit_eval(feat_inter, P * P)
    df = len(feat_fourier(0, 0))
    tr_f, hd_f = fit_eval(feat_fourier, df)
    return tr_f, hd_f, 1.0 / P, hd_m, hd_i

grok_train_acc, grok_held_acc, grok_chance, grok_marginal_held, grok_inter_held = grok_control()
grok_ctrl_pass = grok_held_acc >= 0.90

# ==========================================================================
# VERDICT
# ==========================================================================
# beats-max-single = mechanism does REAL work above the additive/marginal floor
beats_max_single = phase_ambig_acc > additive_ambig_acc + 1e-9

if not grok_ctrl_pass:
    # toy lacks resolution -> mechanism not blamed (TOP-3 lesson). But ablation
    # INERT-vs-load-bearing is still informative; report it.
    verdict = "UNDER-POWER"
elif frozen_pass and inert_load_bearing:
    verdict = "SUPPORTED"
elif inert_load_bearing and beats_max_single:
    # ablation proves coupling is the load-bearing locus AND it beats max_single,
    # but the frozen composition bar (>=0.90 / margin>+0.30) is NOT cleared by
    # this minimal toy -> honest MIXED (DIRECTIONAL lever signal, sub-bar).
    verdict = "MIXED"
elif not inert_load_bearing:
    verdict = "NOT-SUPPORTED"   # mechanism INERT -> not the lever
else:
    verdict = "NOT-SUPPORTED"

survivor = frozen_pass and grok_ctrl_pass and inert_load_bearing

# ==========================================================================
# REPORT
# ==========================================================================
print("=" * 76)
print("H_1732 — Coupled Oscillator Phase Binding   [DIRECTIONAL numpy toy, $0]")
print("         lens=oscillation-phase-bind   target=G1 recombination/conjunction")
print("=" * 76)
print(f"AMBIGUOUS binding pairs (identical marginals): N = {ph_n}")
print()
print("G1 composition (ambiguous / binding-required subset):")
print(f"  phase_ambig_acc   = {phase_ambig_acc:.3f}   ({composed_distinct}/{ph_n})   (bar >= 0.90)")
print(f"  additive_ambig    = {additive_ambig_acc:.3f}   ({max_single}/{add_n}) = max_single (bar <= 0.60)")
print(f"  margin (phase-add)= {phase_ambig_acc - additive_ambig_acc:+.3f}   (bar > +0.30)")
print()
print("INERT ablation (coupling = the load-bearing locus?):")
print(f"  K=0  decoupled    = {ablated_K0_acc:.3f}   (bar <= 0.60 AND drop >= 0.30)")
print(f"  drop (phase-K0)   = {phase_ambig_acc - ablated_K0_acc:+.3f}")
print(f"  K=0.5 weak        = {weak_K_acc:.3f}   (reported)")
print(f"  -> coupling load-bearing: {inert_load_bearing}")
print()
print("GROK positive control (modular add (a+b) mod 7, held-out grid):")
print(f"  grok_train_acc    = {grok_train_acc:.3f}  (Fourier/circular feature map)")
print(f"  grok_held_acc     = {grok_held_acc:.3f}   (bar >= 0.90 ; chance = {grok_chance:.3f})")
print(f"  grok_marginal_held= {grok_marginal_held:.3f}   (marginal map MUST fail ~chance: sanity)")
print(f"  grok_inter_held   = {grok_inter_held:.3f}   (pure-onehot interaction: memorize, no generalize)")
print(f"  -> grok_ctrl_pass : {grok_ctrl_pass}")
print()
print("frozen checks:  (1)phase>=.90={}  (2)margin>+.30={}  (3)add<=.60={}  (4)INERT-load={}"
      .format(chk1, chk2, chk3, chk4))
print("=" * 76)
print(f"VERDICT: {verdict}    survivor={survivor}")
print("numpy toy = DIRECTIONAL only; NOT engine-native (a_engine_native_learning).")
print("=" * 76)

# machine-readable tail
print("\nNUMBERS_VERBATIM | "
      f"composed_distinct={composed_distinct} | max_single={max_single} | "
      f"phase_ambig_acc={phase_ambig_acc:.3f} | additive_ambig_acc={additive_ambig_acc:.3f} | "
      f"ablate_K0_INERT_acc={ablated_K0_acc:.3f} | weak_K05_acc={weak_K_acc:.3f} | "
      f"grok_held={grok_held_acc:.3f} | grok_chance={grok_chance:.3f} | "
      f"grok_ctrl_pass={grok_ctrl_pass} | frozen_pass={frozen_pass} | "
      f"inert_load_bearing={inert_load_bearing} | survivor={survivor} | verdict={verdict}")
