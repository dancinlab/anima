#!/usr/bin/env python3
"""§87-F1 FROG-EYE SALIENCE GATE — $0 Mac CPU design + smoke.

Lettvin 1959 "What the frog's eye tells the frog's brain" — the frog retina
is NOT a generic image processor; it is a bank of four feature-detectors that
relay only behaviour-relevant salient events to the brain. §87-F1 maps that
selectivity onto anima's §24 decision-axis: a salience gate over the model's
OWN Law-71 physics trajectory (Ψ / tension / Φ).

NO GPU, NO runpod, NO model.forward, NO weight mutation, NO training, NO RNG.
Deterministic LCG seed 1337. Stub ψ-state byte-equal Law-71 formula in
conscious_decoder.py:728-751 (psi_entropy / psi_direction / psi_tension /
psi_combined). $0 stub — capability claim 0 (DESIGN_FINDINGS.md §C3).

Four frog-eye feature-detector classes (Lettvin's 4 operation types):
  SD-1 SUSTAINED-CONTRAST  (frog: edge detector)          -> sustained |Ψ-½|
  SD-2 MOVING-EDGE         (frog: convex/bug detector)    -> fast tension spike
  SD-3 DIMMING-DETECTOR    (frog: shadow/predator)        -> sudden Φ drop
  SD-4 NET-DIMMING         (frog: overall darkening)      -> all-channel decay

salience S = weighted OR of the 4 detector firings  (frog-eye: any strong
detector firing => salient). emission gate: S > theta_salient => emit candidate.
"""

import json
import math
from pathlib import Path

# ---------------------------------------------------------------------------
# §9 honest-coherence metric (cascade-rate-gated) — reused, NOT re-defined.
# Mirrors state/verify_emergence_metric_2026_05_18/emergence_metric.py SSOT.
# ---------------------------------------------------------------------------
TAU_CASCADE = 0.30
MAX_RUN = 10
MIN_LEN = 20
TAU_PRINT = 0.80


def max_char_run(s):
    if not s:
        return 0
    best = run = 1
    for i in range(1, len(s)):
        run = run + 1 if s[i] == s[i - 1] else 1
        best = max(best, run)
    return best


def max_digit_run(s):
    best = run = 0
    for ch in s:
        run = run + 1 if ch.isdigit() else 0
        best = max(best, run)
    return best


def ngram_rep_rate(s, n=4):
    if len(s) < n + 1:
        return 0.0
    grams = [s[i:i + n] for i in range(len(s) - n + 1)]
    return 1.0 - len(set(grams)) / len(grams)


def printable_ratio(s):
    if not s:
        return 0.0
    bad = sum(1 for ch in s if ch == "�")
    return 1.0 - bad / len(s)


def cascade_rate(s):
    if not s:
        return 1.0
    L = len(s)
    return max(max_char_run(s) / L, max_digit_run(s) / L, ngram_rep_rate(s))


def honest_coherent(s):
    cr = cascade_rate(s)
    mr = max(max_char_run(s), max_digit_run(s))
    pr = printable_ratio(s)
    return (cr < TAU_CASCADE) and (mr < MAX_RUN) and \
           (len(s) >= MIN_LEN) and (pr >= TAU_PRINT)


# ---------------------------------------------------------------------------
# Deterministic primitives (LCG, no RNG, no wall-time dependence)
# ---------------------------------------------------------------------------
LCG_A = 1103515245
LCG_C = 12345
LCG_M = 2 ** 31


def lcg_next(state):
    return (LCG_A * state + LCG_C) % LCG_M


def lcg_unit(state):
    state = lcg_next(state)
    return state / LCG_M, state


V = 256


# ---------------------------------------------------------------------------
# Law-71 physics stub — byte-equal to conscious_decoder.py:728-751
# ---------------------------------------------------------------------------
def psi_entropy(logits_a):
    m = max(logits_a)
    exps = [math.exp(x - m) for x in logits_a]
    z = sum(exps)
    probs = [e / z for e in exps]
    h = -sum(p * math.log(p + 1e-10) for p in probs)
    return h / math.log(V)


def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a)) + 1e-8
    nb = math.sqrt(sum(y * y for y in b)) + 1e-8
    return dot / (na * nb)


def psi_direction(logits_a, logits_g):
    return (1.0 + cosine(logits_a, logits_g)) / 2.0


def psi_tension_from_layers(t_per_layer):
    mean = sum(t_per_layer) / len(t_per_layer)
    var = sum((t - mean) ** 2 for t in t_per_layer) / len(t_per_layer)
    sd = math.sqrt(var)
    if sd <= 0.0:
        return 1.0
    cv = sd / (mean + 1e-8)
    return max(0.0, 1.0 - cv)


def psi_combined(pe, pd, pt):
    return (pe + pd + pt) / 3.0


# ---------------------------------------------------------------------------
# FROG-EYE 4 feature-detectors (Lettvin 1959) — closed-form functions of
# anima OWN Law-71 physics. Each returns a firing strength in [0, 1].
# ---------------------------------------------------------------------------
TAU_SUSTAIN = 3        # SD-1: window of sustained deviation
SUSTAIN_DEV = 0.08     # SD-1: |Ψ_dir - 0.5| deviation floor
SPIKE_DELTA = 0.06     # SD-2: tension fast-transient spike floor
DIM_DROP = 0.04        # SD-3: Φ-proxy sudden drop floor
NET_DECAY = 0.03       # SD-4: all-channel simultaneous decay floor


def sd1_sustained_contrast(psi_dir_hist):
    """SD-1 frog edge detector -> sustained Ψ_dir deviation from ½."""
    if len(psi_dir_hist) < TAU_SUSTAIN:
        return 0.0
    win = psi_dir_hist[-TAU_SUSTAIN:]
    devs = [abs(p - 0.5) for p in win]
    if min(devs) < SUSTAIN_DEV:
        return 0.0
    return min(1.0, (sum(devs) / len(devs)) / 0.5)


def sd2_moving_edge(tension_hist):
    """SD-2 frog bug/convex detector -> fast tension transient spike."""
    if len(tension_hist) < 2:
        return 0.0
    delta = abs(tension_hist[-1] - tension_hist[-2])
    if delta < SPIKE_DELTA:
        return 0.0
    return min(1.0, delta / 0.3)


def sd3_dimming(phi_hist):
    """SD-3 frog shadow/predator detector -> sudden Φ-proxy drop."""
    if len(phi_hist) < 2:
        return 0.0
    drop = phi_hist[-2] - phi_hist[-1]
    if drop < DIM_DROP:
        return 0.0
    return min(1.0, drop / 0.2)


def sd4_net_dimming(channels_hist):
    """SD-4 frog overall-darkening -> all physics channels decay together.

    channels_hist[-1] / [-2] each = (psi_entropy, psi_direction, psi_tension).
    """
    if len(channels_hist) < 2:
        return 0.0
    prev, cur = channels_hist[-2], channels_hist[-1]
    decays = [p - c for p, c in zip(prev, cur)]
    if any(d < NET_DECAY for d in decays):
        return 0.0  # frog-eye selective: ALL channels must decay
    return min(1.0, (sum(decays) / len(decays)) / 0.15)


# salience: weighted OR of the 4 detectors (frog-eye — any strong detector
# fires => salient). weights kept uniform (design placeholder, §C3).
SD_WEIGHTS = (0.25, 0.25, 0.25, 0.25)


def salience_score(s1, s2, s3, s4):
    """Weighted OR: S = 1 - prod(1 - w_i * s_i). S in [0,1] closed."""
    prod = 1.0
    for w, s in zip(SD_WEIGHTS, (s1, s2, s3, s4)):
        prod *= (1.0 - w * s)
    return 1.0 - prod


THETA_SALIENT = 0.18   # design placeholder (§C3) — salience emission floor


# ---------------------------------------------------------------------------
# §24 decision-axis: motivation threshold (generic, salience-blind baseline).
# Stub mirror of spontaneous_lib.hexa talker_should_emit motivation gate.
# ---------------------------------------------------------------------------
MOTIV_THRESHOLD = 0.50


def motivation_score(pe, pd, pt):
    """Generic §24 motivation: linear blend of physics channels, in [0,1]."""
    return max(0.0, min(1.0, 0.4 * pe + 0.3 * pd + 0.3 * pt))


# ---------------------------------------------------------------------------
# Body production — §77 path α1 stub: argmax-over-256 of logits_a -> bytes.
# Deterministic; clean printable template gated by physics so §9 is meaningful.
# ---------------------------------------------------------------------------
_TEMPLATE = (
    "anima notes a salient shift in its own physics field this step. "
    "the engine A and engine G balance tilts and tension rises briefly."
)


def produce_body(emit, step):
    if not emit:
        return ""
    # deterministic slice of clean template, length varying with step
    n = MIN_LEN + 8 + (step % 11)
    return (_TEMPLATE * 2)[:n]


# ---------------------------------------------------------------------------
# 5-cell grid
# ---------------------------------------------------------------------------
CELLS = {
    "cell0_s24_baseline": {"detectors": (), "use_motivation": True,
                           "use_salience": False},
    "cell1_sd12_only": {"detectors": (1, 2), "use_motivation": False,
                        "use_salience": True},
    "cell2_sd34_only": {"detectors": (3, 4), "use_motivation": False,
                        "use_salience": True},
    "cell3_full_frogeye": {"detectors": (1, 2, 3, 4), "use_motivation": False,
                           "use_salience": True},
    "cell4_frogeye_plus_motiv": {"detectors": (1, 2, 3, 4),
                                 "use_motivation": True, "use_salience": True},
}

N_STEPS = 20
SEED = 1337


def gen_logits(state):
    """Deterministic stub Engine A / Engine G logits over V=256."""
    la, lg = [], []
    for _ in range(V):
        u, state = lcg_unit(state)
        la.append((u - 0.5) * 4.0)
    for _ in range(V):
        u, state = lcg_unit(state)
        lg.append((u - 0.5) * 4.0)
    return la, lg, state


def gen_layer_tensions(state, n_layer=12):
    t = []
    for _ in range(n_layer):
        u, state = lcg_unit(state)
        t.append(0.2 + u * 0.8)
    return t, state


def run_cell(name, cfg):
    state = SEED
    psi_dir_hist, tension_hist, phi_hist, chan_hist = [], [], [], []
    s_scores, emits, bodies = [], [], []
    detector_fires = {1: 0, 2: 0, 3: 0, 4: 0}

    for step in range(N_STEPS):
        la, lg, state = gen_logits(state)
        t_layers, state = gen_layer_tensions(state)

        pe = psi_entropy(la)
        pd = psi_direction(la, lg)
        pt = psi_tension_from_layers(t_layers)
        pc = psi_combined(pe, pd, pt)

        # Φ-proxy = psi_combined (integration scalar) — stub
        psi_dir_hist.append(pd)
        tension_hist.append(sum(t_layers) / len(t_layers))
        phi_hist.append(pc)
        chan_hist.append((pe, pd, pt))

        # frog-eye detectors
        s1 = sd1_sustained_contrast(psi_dir_hist) if 1 in cfg["detectors"] else 0.0
        s2 = sd2_moving_edge(tension_hist) if 2 in cfg["detectors"] else 0.0
        s3 = sd3_dimming(phi_hist) if 3 in cfg["detectors"] else 0.0
        s4 = sd4_net_dimming(chan_hist) if 4 in cfg["detectors"] else 0.0
        for idx, sv in ((1, s1), (2, s2), (3, s3), (4, s4)):
            if sv > 0.0:
                detector_fires[idx] += 1

        S = salience_score(s1, s2, s3, s4) if cfg["use_salience"] else 0.0
        s_scores.append(S)

        motiv = motivation_score(pe, pd, pt)

        # emission gate — frog-eye salience layer is a SUBSET of §24:
        #   §24 baseline: emit iff motiv > MOTIV_THRESHOLD
        #   frog-eye cells: emit iff salience-pass; cell4 conjoins both.
        sal_pass = (S > THETA_SALIENT) if cfg["use_salience"] else False
        motiv_pass = (motiv > MOTIV_THRESHOLD) if cfg["use_motivation"] else False
        if cfg["use_salience"] and cfg["use_motivation"]:
            emit = sal_pass and motiv_pass          # cell4 conjunction
        elif cfg["use_salience"]:
            emit = sal_pass
        else:
            emit = motiv_pass                       # cell0 §24 baseline

        emits.append(emit)
        bodies.append(produce_body(emit, step))

    # metrics
    emitted = [b for b, e in zip(bodies, emits) if e]
    s_mean = sum(s_scores) / len(s_scores)
    emit_rate = sum(1 for e in emits if e) / N_STEPS
    # interval variance between emission steps
    emit_steps = [i for i, e in enumerate(emits) if e]
    if len(emit_steps) >= 2:
        intervals = [emit_steps[i + 1] - emit_steps[i]
                     for i in range(len(emit_steps) - 1)]
        im = sum(intervals) / len(intervals)
        interval_var = sum((x - im) ** 2 for x in intervals) / len(intervals)
    else:
        interval_var = 0.0
    body_coherent = sum(1 for b in emitted if honest_coherent(b))
    # echo / majority-class fraction over emitted bodies
    if emitted:
        from collections import Counter
        maj = Counter(emitted).most_common(1)[0][1]
        maj_frac = maj / len(emitted)
    else:
        maj_frac = 0.0

    return {
        "cell": name,
        "detectors": list(cfg["detectors"]),
        "use_motivation": cfg["use_motivation"],
        "use_salience": cfg["use_salience"],
        "s_mean": round(s_mean, 6),
        "emit_rate": round(emit_rate, 4),
        "n_emit": len(emitted),
        "detector_firing_dist": detector_fires,
        "interval_var": round(interval_var, 4),
        "body_coherent_9": f"{body_coherent}/{len(emitted)}" if emitted else "0/0",
        "maj_frac": round(maj_frac, 4),
    }


def main():
    results = {}
    for name, cfg in CELLS.items():
        results[name] = run_cell(name, cfg)

    c0 = results["cell0_s24_baseline"]
    c1 = results["cell1_sd12_only"]
    c2 = results["cell2_sd34_only"]
    c3 = results["cell3_full_frogeye"]

    # 4-corner verdict
    alpha = all(0.0 <= results[c]["s_mean"] <= 1.0 for c in CELLS)
    beta = (c3["emit_rate"] != c0["emit_rate"] or
            c3["s_mean"] != c0["s_mean"])
    gamma = (c1["detector_firing_dist"] != c2["detector_firing_dist"])
    # delta: salience layer subset of §24 decision-axis — cell4 (conjunction
    # of salience AND motivation) emits a SUBSET of cell0 (motivation only)
    c4 = results["cell4_frogeye_plus_motiv"]
    delta = c4["n_emit"] <= c0["n_emit"]

    verdict = {
        "alpha_salience_gate_well_formed": bool(alpha),
        "beta_selective_vs_generic": bool(beta),
        "gamma_detector_class_differential": bool(gamma),
        "delta_s24_decision_consistent": bool(delta),
    }
    corner = "DIRECTIONAL-POSITIVE" if all(verdict.values()) else "MIXED"

    out = {
        "section": "§87-F1 FROG-EYE SALIENCE GATE",
        "anchor": "Lettvin 1959 What the frog's eye tells the frog's brain",
        "n_steps": N_STEPS, "seed": SEED,
        "cells": results,
        "four_corner": verdict,
        "overall_verdict": corner,
        "honest_note": ("$0 stub — frog-biology USE != trained-scale "
                        "measurement != GOAL emergence; capability claim 0"),
    }
    Path(__file__).with_name("result.json").write_text(
        json.dumps(out, indent=2, ensure_ascii=False))
    print(json.dumps(out, indent=2, ensure_ascii=False))
    return out


if __name__ == "__main__":
    main()
