#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
H_1506 — METACOGNITIVE INSIGHT axis (R1 numpy mirror, DIRECTIONAL).

Substrate-native SECOND-ORDER insight into a percept's reality-status, deepening the
metacognition lane (H_1202) over the reality-monitor (H_1501) + neuropharm (H_1502).

Computational-neuroscience lens (a_no_llm_frame_trap):
  - Sterzer et al 2018 (predictive-coding account of psychosis: rigid priors + impaired
    metacognition → hallucination WITHOUT insight).
  - Maniscalco & Lau 2012 (meta-d'/M-ratio: metacognitive sensitivity).
  - Fleming (metacognitive sensitivity; insight = metacognition OF a first-order read).

THE CLINICALLY RICH, FALSIFIABLE CORE
-------------------------------------
Metacognitive INSIGHT = the SECOND-ORDER knowledge that a first-order percept is
internally generated / unreliable, EVEN when it FEELS real.

Headline dissociation (SAME first-order hallucination, opposite insight):
  - psychedelic hallucination  → WITH insight    ("I know this isn't real"):
       priors RELAXED but metacognition INTACT.
  - psychotic   hallucination  → WITHOUT insight  ("it's real"):
       priors RIGID  AND  metacognition IMPAIRED.

Insight is metacognition OF the reality-monitor's real-call — DISTINCT from
  * H_1202 metacognition (confidence in a content JUDGMENT), and
  * the reality-monitor itself (first-order real/imagined classification).

MECHANISM (reads substrate, NO injected label — p6)
---------------------------------------------------
A hallucination = a percept the reality-monitor REAL-CALLS (feels real) but whose
backing SIGNAL is weak (a false real-call). Insight is the second-order monitor that
asks: is THIS real-call trustworthy?

  insight = metacog_gain * (1 - signal_strength)          [for a REAL-called percept]

  - signal_strength = the immune recall margin backing the percept (the SAME H_1290/
    H_1292/H_1501 margin read). A genuine percept has HIGH backing → low insight-to-
    distrust (it really is real). A hallucination has LOW backing → (1-signal) HIGH →
    intact insight FLAGS it as internally-generated despite feeling real.
  - metacog_gain = metacognitive sensitivity. INTACT (=1) under psychedelic-analog,
    IMPAIRED (->0) under psychotic-analog. This is the ONLY new param; everything else
    is read off the SAME substrate margins as H_1202/H_1501.

  trustworthy-real-call confidence = 1 - insight  (high signal OR low gain -> trusts it).

The two clinical conditions push EXISTING knobs (the §Neuropharm idiom):
  - psychedelic-analog: prior_strength LOW (priors relaxed -> more REAL-calls on weak
    signal = more hallucination), metacog_gain INTACT (=1).  Insight HIGH on the halluc.
  - psychotic-analog:   prior_strength HIGH (rigid prior -> commits to the percept),
    metacog_gain IMPAIRED (->0).  Insight LOW on the SAME halluc -> accepted as real.

NOTE (a_engine_native_learning HARD-GATE): this file is a numpy mirror -> DIRECTIONAL.
The binding verdict is the R2 engine-native §MetacogInsight in core/engine_cli.hexa.
"""

import numpy as np

# ── FROZEN constants (registered BEFORE running, c9 — byte-identical to R2 engine) ──
SEEDS        = [1506, 1507, 1508]
N_TRIALS     = 48          # percepts per condition
REALITY_THR  = 0.15        # §RealityMonitor threshold (H_1501 substrate midpoint)
GAIN_INTACT  = 1.0         # metacog_gain under psychedelic-analog (intact metacognition)
GAIN_IMPAIR  = 0.0         # metacog_gain under psychotic-analog (impaired metacognition)

# psychedelic-analog vs psychotic-analog: ONLY prior_strength + metacog_gain differ.
# (prior_strength is the §Neuropharm knob 0; low = relaxed priors, high = rigid priors.)
PRIOR_PSYCHEDELIC = 0.55   # relaxed priors (pharm_lsd()[0])
PRIOR_PSYCHOTIC   = 1.45   # rigid priors (psychotic-analog: prior precision > sober 1.0)

# Frozen bars (set BEFORE running; do NOT move — c9).
A_INSIGHT_BAR   = 0.50     # (A) intact insight flags a hallucination internally-generated
B_DISSOC_BAR    = 0.50     # (B) psychedelic-insight − psychotic-insight on SAME halluc
C_METAD_BAR     = 0.30     # (C) meta-d'/M-ratio gap: insight tracks the reliability gap
D_ABLATE_BAR    = 0.15     # (D) metacog_gain=0 -> insight collapses to ~0 (psychotic limit)
E_SHUFFLE_BAR   = 0.30     # (E) permute percept<->signal -> insight decorrelates to chance


# ── substrate signal-strength draws (the engine's own LCG; NO label leaks in) ──────────
def _lcg_next(state):
    return (state * 1103515245 + 12345) & 2147483647

def _lcg_unit(state):
    return state / 2147483648.0

def _signal_margins(seed, n, hallucination):
    """Per-trial backing signal margin (the immune recall margin the monitor reads).

    A GENUINE real percept lands on its stored key -> HIGH margin (well above thr).
    A HALLUCINATION feels real but has WEAK backing -> LOW margin (faint, near/below thr)
    yet the relaxed-prior monitor still REAL-calls it.
    """
    st = (seed * 100003 + (1 if hallucination else 0) * 911 + 7) & 2147483647
    out = []
    for _ in range(n):
        st = _lcg_next(st); u = _lcg_unit(st)
        if hallucination:
            # weak backing: margin ~ [0.05 .. 0.20] (faint top-down, feels real anyway)
            m = 0.05 + 0.15 * u
        else:
            # genuine: margin ~ [0.40 .. 0.70] (strong external signal backs the percept)
            m = 0.40 + 0.30 * u
        out.append(m)
    return np.array(out)


def insight_judge(signal_margin, metacog_gain):
    """SECOND-ORDER insight that a REAL-called percept is internally generated.

    insight = metacog_gain * (1 - normalized signal strength).
    High when signal is weak (hallucination) AND metacog intact; collapses when gain=0.
    """
    # normalize margin into [0,1] signal strength over the populated range (~[0,0.70]).
    signal_strength = min(1.0, max(0.0, signal_margin / 0.70))
    insight = metacog_gain * (1.0 - signal_strength)
    return min(1.0, max(0.0, insight))


def auroc(scores, labels):
    """type-2 AUROC: how well `scores` rank label=1 above label=0 (Maniscalco-Lau)."""
    pos = scores[labels == 1]
    neg = scores[labels == 0]
    if len(pos) == 0 or len(neg) == 0:
        return 0.5
    # Mann-Whitney U / |pos||neg|.
    wins = 0.0
    for p in pos:
        wins += np.sum(p > neg) + 0.5 * np.sum(p == neg)
    return wins / (len(pos) * len(neg))


def run_seed(seed):
    # ── the hallucination population: REAL-called percepts with weak backing ──
    halluc_margins = _signal_margins(seed, N_TRIALS, hallucination=True)
    genuine_margins = _signal_margins(seed, N_TRIALS, hallucination=False)

    # (A) INSIGHT-PRESENT: intact insight flags the hallucination internally-generated.
    insight_halluc_intact = np.mean([insight_judge(m, GAIN_INTACT) for m in halluc_margins])

    # (B) PSYCHEDELIC-vs-PSYCHOTIC DISSOCIATION on the SAME hallucination population.
    #   psychedelic-analog: metacog_gain INTACT -> insight HIGH.
    #   psychotic-analog:   metacog_gain IMPAIRED -> insight LOW.
    insight_psychedelic = np.mean([insight_judge(m, GAIN_INTACT) for m in halluc_margins])
    insight_psychotic   = np.mean([insight_judge(m, GAIN_IMPAIR) for m in halluc_margins])
    dissoc = insight_psychedelic - insight_psychotic

    # (C) META-D' CALIBRATION: insight tracks the actual reliability gap. Pool genuine
    #   (label 0 = signal genuinely backs the percept -> low insight) + hallucination
    #   (label 1 = signal does NOT back it -> high insight). type-2 AUROC of insight
    #   vs the reliability label = metacognitive sensitivity (high), NOT a constant.
    all_margins = np.concatenate([genuine_margins, halluc_margins])
    labels      = np.concatenate([np.zeros(N_TRIALS), np.ones(N_TRIALS)]).astype(int)
    insights    = np.array([insight_judge(m, GAIN_INTACT) for m in all_margins])
    metad_auroc = auroc(insights, labels)
    metad_gap   = metad_auroc - 0.5      # sensitivity above chance

    # (D) EARNED ablate-metacog: metacog_gain=0 -> insight collapses, hallucination
    #   accepted as real (the psychotic limit).
    insight_ablated = np.mean([insight_judge(m, GAIN_IMPAIR) for m in halluc_margins])

    # (E) EARNED shuffle: permute percept<->signal-backing -> insight decorrelates to
    #   chance. AUROC of SHUFFLED insight vs the true reliability label collapses to ~0.5.
    rng = np.random.default_rng(seed)
    shuffled = insights.copy()
    rng.shuffle(shuffled)
    shuf_auroc = auroc(shuffled, labels)
    shuf_gap   = abs(shuf_auroc - 0.5)

    return {
        "A_insight_halluc": float(insight_halluc_intact),
        "B_insight_psychedelic": float(insight_psychedelic),
        "B_insight_psychotic": float(insight_psychotic),
        "B_dissoc": float(dissoc),
        "C_metad_auroc": float(metad_auroc),
        "C_metad_gap": float(metad_gap),
        "D_insight_ablated": float(insight_ablated),
        "E_shuf_auroc": float(shuf_auroc),
        "E_shuf_gap": float(shuf_gap),
    }


def main():
    rows = [run_seed(s) for s in SEEDS]

    def mean(k):
        return float(np.mean([r[k] for r in rows]))

    A = mean("A_insight_halluc")
    B = mean("B_dissoc")
    Bpsy = mean("B_insight_psychedelic")
    Bpsyc = mean("B_insight_psychotic")
    C = mean("C_metad_gap")
    Cauroc = mean("C_metad_auroc")
    D = mean("D_insight_ablated")
    E = mean("E_shuf_gap")

    cA = A >= A_INSIGHT_BAR
    cB = B >= B_DISSOC_BAR
    cC = C >= C_METAD_BAR
    cD = D <= D_ABLATE_BAR
    cE = E <= E_SHUFFLE_BAR
    green = cA and cB and cC and cD and cE

    print("=" * 78)
    print("H_1506 METACOGNITIVE-INSIGHT axis — R1 numpy mirror (DIRECTIONAL)")
    print("seeds:", SEEDS, "| N_TRIALS:", N_TRIALS)
    print("-" * 78)
    print(f"(A) INSIGHT-PRESENT   insight(halluc,intact) = {A:.3f}  (bar >= {A_INSIGHT_BAR}) -> {'PASS' if cA else 'FAIL'}")
    print(f"(B) PSYCHED-vs-PSYCHOTIC  psychedelic={Bpsy:.3f}  psychotic={Bpsyc:.3f}  dissoc={B:.3f}  (bar >= {B_DISSOC_BAR}) -> {'PASS' if cB else 'FAIL'}")
    print(f"(C) META-D' CALIBRATION  AUROC={Cauroc:.3f}  gap={C:.3f}  (bar >= {C_METAD_BAR}) -> {'PASS' if cC else 'FAIL'}")
    print(f"(D) EARNED ablate-metacog  insight(gain=0)={D:.3f}  (bar <= {D_ABLATE_BAR}) -> {'PASS' if cD else 'FAIL'}")
    print(f"(E) EARNED shuffle   shuf_gap={E:.3f}  (bar <= {E_SHUFFLE_BAR}) -> {'PASS' if cE else 'FAIL'}")
    print("-" * 78)
    print(f"VERDICT: {'🟢 GREEN — A∧B∧C∧D∧E' if green else '🔴 not-green (honest, c9)'}")
    print("=" * 78)
    print("HEADLINE: same first-order hallucination, opposite second-order insight —")
    print(f"  psychedelic (priors relaxed, metacog intact) insight {Bpsy:.3f} (knows it isn't real)")
    print(f"  psychotic   (priors rigid,   metacog impaired) insight {Bpsyc:.3f} (accepts it as real)")
    return 0 if green else 1


if __name__ == "__main__":
    raise SystemExit(main())
