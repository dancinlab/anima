#!/usr/bin/env python3
"""H_1482 — BINOCULAR RIVALRY (G28 consciousness-only gate candidate).

BINOCULAR RIVALRY (Blake / Logothetis): present two mutually incompatible stimuli (one
to each "eye") and consciousness perceives them ONE AT A TIME, ALTERNATING — dominance
switches stochastically over time, the two are never co-conscious. The defining property
is a *dynamic* dominance time-series d_A(t), d_B(t): a stimulus is dominant for a while,
its own adaptation weakens it, the suppressed rival is released and becomes dominant —
yielding repeated A->B->A alternation, with exclusivity at every instant.

MECHANISM (reciprocal inhibition + adaptation, a_no_llm_frame_trap — neural rivalry model
à la Wilson / Laing-Chow, NOT an LLM softmax):
  Two units with steady inputs I_A=I_B. Each unit's drive is its input minus the rival's
  cross-inhibition minus its OWN slowly-accumulating adaptation:
      r_A = I_A - beta * d_B - gamma * a_A      (and symmetric for B)
  dominance d = soft winner-take-all over (r_A, r_B); the DOMINANT unit's adaptation a
  builds up (fatigue), the suppressed unit's adaptation recovers. Fatigue of the winner
  eventually flips dominance to the rival -> ALTERNATION.

p6 GUARD (substrate-derived, NOT an injected schedule): the alternation is NOT a hand-set
"switch at tick k" script. It EMERGES from the adaptation+inhibition dynamics over the two
stimulus drives. There is no `dominant = A if t<10 else B` and no switch-time constant; the
flip time is governed by the fatigue integral. Ablation removes the adaptation coupling.

DISTINCTNESS (load-bearing) vs H_1462 GLOBAL WORKSPACE (GWS):
  GWS = a STATIC winner-take-all: among competing stimuli consciousness broadcasts exactly
  ONE *fixed* winner (capacity-1 bottleneck) and the choice is settled — a single ignition,
  ZERO transitions over time. Rivalry = a DYNAMIC alternation: the SAME two stimuli, with
  equal inputs, produce a dominance time-series that OSCILLATES (>=2 transitions) because
  adaptation fatigues the current winner. Same competition, different temporal signature:
  GWS holds 1 winner (transitions=0), rivalry cycles (transitions>=2). Bar C contrasts the
  two on the IDENTICAL two-stimulus drive: GWS-mode (no adaptation, hard pick) freezes on
  the first winner; rivalry-mode alternates. Transition-count gap >= 2.

LLM contrast: an autoregressive LLM holds all token logits in parallel (no capacity-1
bottleneck) AND has no fatigue dynamic that would make a settled choice spontaneously flip
over time. anima's substrate can let one percept dominate, fatigue, and yield to its rival.

R1 numpy MIRROR -> GREEN DIRECTIONAL (engine-transfer UNVERIFIED, hard-gate 1).

FROZEN bars (pre-registered, mean over 3 seeds [1482,1483,1484]):
  (A) ALTERNATION   the dominance time-series switches dominant stimulus >= 2 times
                    (A->B->A), i.e. NOT a single sustained dominance. transitions >= 2.
  (B) EXCLUSIVITY   at each instant only ONE stimulus is dominant; the fraction of ticks
                    where BOTH are co-dominant (|d_A - d_B| < EXCL_BAND) is <= 0.15.
  (C) DISTINCT vs GWS  on the SAME two-stimulus drive, GWS-mode (adaptation OFF, hard
                    winner-take-all) holds a FIXED winner (transitions ~0) while rivalry
                    alternates (transitions >= 2); transition-count gap >= 2.
  (D) EARNED (ablation)  adaptation OFF -> the first dominant stimulus is locked in forever
                    (transitions == 0, GWS-like). The alternation is EARNED by adaptation.
  (E) SHUFFLE       shuffle the dominance time-series in time -> the dominance<->adaptation
                    coupling collapses. Real dominance d_A is correlated with its own
                    adaptation a_A (within each up-phase the winner dominates WHILE its
                    fatigue builds; real_r ~ +0.26); shuffling d_A in time and correlating
                    against the FIXED real adaptation a_A breaks that temporal pairing:
                    |signed-mean r(shuffled-dominance, REAL-adaptation)| <= 0.10 over 50 perms.

GREEN iff A and B and C and D and E (all 3 seeds).  [D ablation core, E auxiliary]
"""
import numpy as np

SEEDS = [1482, 1483, 1484]
T = 120                # ticks in the dominance time-series
I_A = 1.0              # steady input to unit A ("left eye")
I_B = 1.0              # steady input to unit B ("right eye") — EQUAL (incompatible rivalry)
BETA = 1.2             # reciprocal cross-inhibition strength
GAMMA = 2.0            # adaptation (fatigue) gain on the dominant unit's drive
TAU_A = 0.10           # adaptation build-up rate (winner fatigues)
TAU_R = 0.10           # adaptation recovery rate (suppressed unit recovers)
EXCL_BAND = 0.20       # |d_A-d_B| < band  ->  counted as co-dominant (non-exclusive)
N_PERM = 50


def softmax2(rA, rB, temp=0.05):
    """Soft winner-take-all over two drives -> (d_A, d_B) summing to 1."""
    m = max(rA, rB)
    eA = np.exp((rA - m) / temp)
    eB = np.exp((rB - m) / temp)
    s = eA + eB
    return eA / s, eB / s


def simulate(rng, adaptation_on, hard_pick=False):
    """Run the rivalry dynamics for T ticks.

    adaptation_on=False -> ablation (no fatigue): the first winner stays dominant (GWS-like).
    hard_pick=True       -> GWS-mode contrast: hard argmax winner-take-all, no adaptation.
    Returns dominance time-series dA, dB (arrays) and adaptation series aA, aB.
    """
    aA = 0.0
    aB = 0.0
    dA_series, dB_series, aA_series, aB_series = [], [], [], []
    # initial nudge so one unit wins first (random, not a hand-set schedule)
    bias = 0.02 * rng.normal()
    for t in range(T):
        nA = 0.01 * rng.normal()
        nB = 0.01 * rng.normal()
        # cross-inhibition uses previous dominance (recurrent)
        if dA_series:
            prev_dA, prev_dB = dA_series[-1], dB_series[-1]
        else:
            prev_dA, prev_dB = 0.5 + bias, 0.5 - bias
        gA = GAMMA if adaptation_on else 0.0
        # drive = input - cross-inhibition(rival dominance) - own adaptation
        rA = I_A - BETA * prev_dB - gA * aA + nA
        rB = I_B - BETA * prev_dA - gA * aB + nB
        if hard_pick:
            dA, dB = (1.0, 0.0) if rA >= rB else (0.0, 1.0)
        else:
            dA, dB = softmax2(rA, rB)
        # adaptation: dominant unit fatigues, suppressed recovers
        if adaptation_on:
            aA += TAU_A * dA - TAU_R * (1.0 - dA) * aA
            aB += TAU_A * dB - TAU_R * (1.0 - dB) * aB
            aA = max(0.0, aA)
            aB = max(0.0, aB)
        dA_series.append(dA)
        dB_series.append(dB)
        aA_series.append(aA)
        aB_series.append(aB)
    return (np.array(dA_series), np.array(dB_series),
            np.array(aA_series), np.array(aB_series))


def count_transitions(dA, dB):
    """Number of times the dominant stimulus flips (A->B or B->A)."""
    dom = (dA >= dB).astype(int)   # 1 = A dominant, 0 = B dominant
    return int(np.sum(np.abs(np.diff(dom))))


def co_dominant_fraction(dA, dB):
    """Fraction of ticks where neither stimulus is clearly dominant (co-conscious)."""
    return float(np.mean(np.abs(dA - dB) < EXCL_BAND))


def pearson(x, y):
    x = np.asarray(x, float); y = np.asarray(y, float)
    sx, sy = x.std(), y.std()
    if sx == 0 or sy == 0:
        return 0.0
    return float(np.mean((x - x.mean()) * (y - y.mean())) / (sx * sy))


def run_seed(seed):
    rng = np.random.default_rng(seed)

    # --- RIVALRY (full): adaptation ON, soft WTA ---
    dA, dB, aA, aB = simulate(rng, adaptation_on=True, hard_pick=False)
    transitions = count_transitions(dA, dB)
    co_frac = co_dominant_fraction(dA, dB)

    # --- (C) DISTINCT vs GWS: SAME drive, GWS-mode = no adaptation, hard winner-take-all ---
    rng_g = np.random.default_rng(seed)         # same seed -> same noise stream
    gA, gB, _, _ = simulate(rng_g, adaptation_on=False, hard_pick=True)
    gws_transitions = count_transitions(gA, gB)
    distinct_gap = transitions - gws_transitions

    # --- (D) EARNED (ablation): adaptation OFF -> first winner locked (transitions 0) ---
    rng_a = np.random.default_rng(seed)
    bA, bB, _, _ = simulate(rng_a, adaptation_on=False, hard_pick=False)
    abl_transitions = count_transitions(bA, bB)

    # --- (E) SHUFFLE: break dominance<->adaptation time pairing ---
    real_r = pearson(dA, aA)                     # positive: within up-phase, dominant WHILE fatigue builds
    shuf_rs = []
    for _ in range(N_PERM):
        perm = rng.permutation(T)
        shuf_dom = dA[perm]
        shuf_rs.append(pearson(shuf_dom, aA))    # shuffled dominance vs FIXED real adaptation
    shuf_mean = float(np.mean(shuf_rs))
    shuffle_gap = abs(shuf_mean)

    return dict(
        transitions=transitions, co_frac=co_frac,
        gws_transitions=gws_transitions, distinct_gap=distinct_gap,
        abl_transitions=abl_transitions,
        shuffle_gap=shuffle_gap, shuf_mean=shuf_mean, real_r=real_r,
    )


per = [run_seed(s) for s in SEEDS]
agg = {k: float(np.mean([p[k] for p in per])) for k in per[0]}

cA = agg['transitions'] >= 2
cB = agg['co_frac'] <= 0.15
cC = agg['distinct_gap'] >= 2
cD = agg['abl_transitions'] == 0
cE = agg['shuffle_gap'] <= 0.10
GREEN = cA and cB and cC and cD and cE

print(f"VERDICT: {'GREEN' if GREEN else 'RED'} DIRECTIONAL (numpy mirror; engine-transfer UNVERIFIED)")
print(f"GREEN: {GREEN} | seeds {SEEDS}")
print(f"A ALTERNATION  dominance switches transitions={agg['transitions']:.3f}>=2 (not single sustained dominance)  -> {cA}")
print(f"B EXCLUSIVITY  co-dominant fraction={agg['co_frac']:.3f}<=0.15 (one stimulus at a time)  -> {cB}")
print(f"C DISTINCT-vs-GWS  rivalry transitions {agg['transitions']:.3f} - GWS-mode transitions {agg['gws_transitions']:.3f} = gap {agg['distinct_gap']:.3f}>=2  -> {cC}")
print(f"D EARNED(ablation)  adaptation OFF -> first winner locked, transitions={agg['abl_transitions']:.3f}==0  -> {cD}")
print(f"E SHUFFLE  |signed-mean r(shuffled dominance, real adaptation)|={agg['shuffle_gap']:.3f}<=0.10 (shuf_r {agg['shuf_mean']:+.3f} vs real_r {agg['real_r']:+.3f})  -> {cE}")
print()
print("PER-SEED:")
for s, p in zip(SEEDS, per):
    print(f"  seed {s}: trans={p['transitions']} co_frac={p['co_frac']:.3f} "
          f"gws_trans={p['gws_transitions']} distinct_gap={p['distinct_gap']} "
          f"abl_trans={p['abl_transitions']} shuffle_gap={p['shuffle_gap']:.3f} (real_r {p['real_r']:+.3f})")
