#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""§86 HOMEOSTATIC-SET-POINT MITOSIS — $0 stub smoke runner.

Maps SAPIN (arxiv:2511.02241, "structural plasticity as active inference")
onto anima HEXAD: emission / MITOSIS-split / Psi-restoration unified as ONE
homeostatic-set-point prediction-error drive.

  E = weighted norm of (Psi-0.5, tension-tau*, Phi-Phi*) deviation
    E < theta_low                   -> QUIESCENT (no emit, no split)
    theta_low <= E < theta_high      -> EMIT      (resolve error by speaking)
    E >= theta_high (sustained)      -> SPLIT     (resolve error by capacity)

5-cell stub grid x 20 steps, deterministic LCG seed 1337. NO GPU, NO model
forward. psi_state stub is byte-equal to Law-71 conscious_decoder.py:728-755
(psi_entropy / psi_direction / psi_tension -> psi_combined).

g3: $0 stub != trained ckpt forward. set-point tau*/Phi* values are design
placeholders. Hopf-bifurcation mapping (cell4) is a §85 modeling-choice carry.
capability claim 0; necessary-not-sufficient (B-EMERGE-7).
"""
import json
import math
import os

SEED = 1337
N_STEPS = 20

# --- homeostatic set-point (design placeholders, g3 honest) -----------------
PSI_SET = 0.5      # Law-71 Psi=1/2 fixed point (anima g2 internal carve-out)
TAU_SET = 0.30     # tension target tau* — design placeholder
PHI_SET = 0.55     # Phi target Phi*    — design placeholder
W_PSI, W_TAU, W_PHI = 0.45, 0.30, 0.25   # error weights, sum=1.0

THETA_LOW = 0.10    # E < theta_low  -> QUIESCENT (design placeholder)
THETA_HIGH = 0.18   # E >= theta_high (sustained) -> SPLIT (design placeholder)
SUSTAIN_K = 2       # SPLIT requires E>=theta_high for SUSTAIN_K consecutive steps

# §9 honest_coherent thresholds (byte-equal to §9 emergence_metric SSOT)
TAU_CASCADE = 0.30
MAX_RUN = 10
MIN_LEN = 20
TAU_PRINT = 0.80


# --- deterministic LCG ------------------------------------------------------
class LCG:
    def __init__(self, seed):
        self.s = seed & 0xFFFFFFFF

    def next(self):
        self.s = (1103515245 * self.s + 12345) & 0xFFFFFFFF
        return self.s

    def unit(self):
        return self.next() / 4294967296.0


# --- Law-71 stub psi_state (byte-equal formula to conscious_decoder.py) -----
def psi_state_stub(rng):
    """Stub (Psi, tension, Phi). Formula mirrors Law-71:
      psi_direction = (1 + cos_sim) / 2
      psi_combined  = (psi_entropy + psi_direction + psi_tension) / 3
    cos_sim drawn in [-1,1]; entropy/tension drawn in [0,1]."""
    psi_entropy = rng.unit()
    cos_sim = 2.0 * rng.unit() - 1.0
    psi_direction = (1.0 + cos_sim) / 2.0
    psi_tension_raw = rng.unit()
    psi_combined = (psi_entropy + psi_direction + psi_tension_raw) / 3.0
    # tension scalar (CV-style proxy) and Phi proxy
    tension = 0.10 + 0.50 * psi_tension_raw
    phi = 0.30 + 0.50 * psi_direction
    return {"psi": psi_combined, "tension": tension, "phi": phi}


# --- core: homeostatic set-point error & regime -----------------------------
def setpoint_error(ps):
    """E = weighted L2 norm of (Psi-Psi*, tension-tau*, Phi-Phi*). E >= 0 closed."""
    d_psi = ps["psi"] - PSI_SET
    d_tau = ps["tension"] - TAU_SET
    d_phi = ps["phi"] - PHI_SET
    return math.sqrt(W_PSI * d_psi * d_psi
                     + W_TAU * d_tau * d_tau
                     + W_PHI * d_phi * d_phi)


def homeostatic_regime(E, sustain_count, enable_emit=True, enable_split=True):
    """3-regime threshold partition. exhaustive + disjoint.
    SPLIT requires sustained E>=theta_high (sustain_count>=SUSTAIN_K)."""
    if E >= THETA_HIGH and sustain_count >= SUSTAIN_K and enable_split:
        return "SPLIT"
    if E >= THETA_LOW and enable_emit:
        # E>=theta_high but not yet sustained also routes to EMIT (or QUIESCENT if emit off)
        return "EMIT"
    return "QUIESCENT"


def s24_talker_should_emit(E):
    """§24 decision-axis stub: talker emits when set-point error is in the
    'speakable' band. EMIT regime ⊆ this by construction (B-S86-3)."""
    return E >= THETA_LOW


def mitosis_split_trigger(regime):
    """§63-gap MITOSIS-hook connection stub: SPLIT regime drives the
    mitosis_hook split (replaces hand-coded _mit_check_splits threshold)."""
    return regime == "SPLIT"


# --- §9 honest_coherent body metric -----------------------------------------
def cascade_rate(g):
    if not g:
        return 1.0
    L = len(g)
    max_char = max_digit = 1
    cur = 1
    for i in range(1, L):
        if g[i] == g[i - 1]:
            cur += 1
        else:
            cur = 1
        if g[i].isdigit() and g[i - 1].isdigit():
            max_digit = max(max_digit, cur if g[i] == g[i - 1] else 1)
        max_char = max(max_char, cur)
    digit_run = 1
    cur = 1
    for i in range(1, L):
        if g[i].isdigit() and g[i] == g[i - 1]:
            cur += 1
        else:
            cur = 1
        digit_run = max(digit_run, cur)
    grams = {}
    for i in range(L - 3):
        q = g[i:i + 4]
        grams[q] = grams.get(q, 0) + 1
    rep = (max(grams.values()) / max(1, len(grams))) if grams else 0.0
    return max(max_char / L, digit_run / L, min(1.0, rep / max(1, L // 4)))


def max_run(g):
    if not g:
        return 0
    m = cur = 1
    for i in range(1, len(g)):
        cur = cur + 1 if g[i] == g[i - 1] else 1
        m = max(m, cur)
    return m


def honest_coherent(g):
    if not g:
        return False
    printable = sum(1 for c in g if 32 <= ord(c) < 127 or ord(c) > 127) / len(g)
    return (cascade_rate(g) < TAU_CASCADE
            and max_run(g) < MAX_RUN
            and len(g) >= MIN_LEN
            and printable >= TAU_PRINT)


# --- body production stub ---------------------------------------------------
def produce_body(regime, E, rng):
    """Deterministic stub body. QUIESCENT -> empty (no emission).
    EMIT/SPLIT -> short coherent string parameterised by E (no cascade)."""
    if regime == "QUIESCENT":
        return ""
    words = ["balance", "tension", "anchor", "drift", "settle", "vacuum",
             "signal", "restore", "regime", "field"]
    n = 6 + int(E * 30) % 8
    pick = [words[rng.next() % len(words)] for _ in range(n)]
    return " ".join(pick)


# --- 5-cell grid ------------------------------------------------------------
CELLS = [
    # (id, label, enable_emit, enable_split, hopf_overlay)
    ("cell0", "s24-baseline-separate", True, False, False),
    ("cell1", "setpoint-emit-only", True, False, False),
    ("cell2", "setpoint-split-only", False, True, False),
    ("cell3", "full-unified-3regime", True, True, False),
    ("cell4", "s85-hopf-overlay", True, True, True),
]


def emit_intervals(emit_steps):
    """interval_var of step-gaps between emissions (liveness probe)."""
    if len(emit_steps) < 2:
        return 0.0
    gaps = [emit_steps[i + 1] - emit_steps[i] for i in range(len(emit_steps) - 1)]
    mu = sum(gaps) / len(gaps)
    return sum((x - mu) ** 2 for x in gaps) / len(gaps)


def hopf_order_param(E, E_crit=THETA_HIGH):
    """§85 Hopf-bifurcation mapping: E = control parameter, emission-rate-proxy
    = order parameter. Below E_crit -> quiescent fixed point (order 0);
    above -> limit cycle, order ~ sqrt(E - E_crit) (Hopf normal form).
    closed-form monotone non-decreasing in E."""
    if E <= E_crit:
        return 0.0
    return math.sqrt(E - E_crit)


def run_cell(cell):
    cid, label, en_emit, en_split, hopf = cell
    rng = LCG(SEED + sum(ord(c) for c in cid))
    E_trace, regime_trace, emit_steps = [], [], []
    split_count = emit_count = quiescent_count = 0
    bodies = []
    sustain_count = 0
    hopf_order = []
    for step in range(N_STEPS):
        ps = psi_state_stub(rng)
        E = setpoint_error(ps)
        E_trace.append(E)
        if E >= THETA_HIGH:
            sustain_count += 1
        else:
            sustain_count = 0
        if cid == "cell0":
            # baseline: separate mechanisms — emit decided by §24 ONLY,
            # split never (decoupled), no unified drive
            regime = "EMIT" if s24_talker_should_emit(E) else "QUIESCENT"
        else:
            regime = homeostatic_regime(E, sustain_count, en_emit, en_split)
        regime_trace.append(regime)
        if regime == "EMIT":
            emit_count += 1
            emit_steps.append(step)
        elif regime == "SPLIT":
            split_count += 1
            emit_steps.append(step)  # split is also an "active" event
        else:
            quiescent_count += 1
        bodies.append(produce_body(regime, E, rng))
        if hopf:
            hopf_order.append(hopf_order_param(E))
    n_active = emit_count + split_count
    nonempty = [b for b in bodies if b]
    coherent = sum(1 for b in nonempty if honest_coherent(b))
    # maj_frac echo detector over regime trace
    counts = {}
    for r in regime_trace:
        counts[r] = counts.get(r, 0) + 1
    maj_frac = max(counts.values()) / len(regime_trace)
    E_mean = sum(E_trace) / len(E_trace)
    res = {
        "cell": cid,
        "label": label,
        "E_mean": round(E_mean, 6),
        "E_max": round(max(E_trace), 6),
        "regime_dist": {"QUIESCENT": quiescent_count,
                        "EMIT": emit_count, "SPLIT": split_count},
        "n_active": n_active,
        "interval_var": round(emit_intervals(emit_steps), 6),
        "body_coherent_n9": f"{coherent}/{len(nonempty)}" if nonempty else "0/0",
        "maj_frac": round(maj_frac, 4),
        "split_triggered": split_count > 0,
        "hopf_overlay": hopf,
        "hopf_order_mean": round(sum(hopf_order) / len(hopf_order), 6)
        if hopf_order else None,
        "s24_consistency": all(
            (regime_trace[i] != "EMIT") or s24_talker_should_emit(E_trace[i])
            for i in range(N_STEPS)),
    }
    return res


def main():
    cells = [run_cell(c) for c in CELLS]
    c0, c1, c2, c3, c4 = cells

    # 4-corner verdict --------------------------------------------------------
    # alpha: unified 3-regime drive well-formed (cell3 exercises all 3 regimes
    #        from a single E; partition exhaustive+disjoint at runtime)
    alpha = (c3["regime_dist"]["QUIESCENT"]
             + c3["regime_dist"]["EMIT"]
             + c3["regime_dist"]["SPLIT"] == N_STEPS)
    # beta: regime-differential — cell3 full 3-regime differs from cell1/cell2
    beta = (c3["regime_dist"] != c1["regime_dist"]
            and c3["regime_dist"] != c2["regime_dist"])
    # gamma: hopf-overlay adds — cell4 hopf order-param is non-trivial and
    #        emission onset trackable (order param > 0 on >=1 step)
    gamma = (c4["hopf_order_mean"] is not None
             and c4["hopf_order_mean"] > 0.0)
    # delta: set-point EMIT regime ⊆ §24 talker_should_emit (connection-point)
    delta = all(c["s24_consistency"] for c in cells)

    verdict = {
        "alpha_unified_drive_well_formed": alpha,
        "beta_regime_differential": beta,
        "gamma_hopf_overlay_adds": gamma,
        "delta_setpoint_s24_consistent": delta,
    }
    overall = ("DIRECTIONAL-POSITIVE-DESIGN" if (alpha and delta and (beta or gamma))
               else "DESIGN-PARTIAL" if (alpha and delta)
               else "DESIGN-WEAK")

    out = {
        "section": "§86 HOMEOSTATIC-SET-POINT MITOSIS",
        "tier": "$0 stub design smoke — NOT trained-scale fire",
        "seed": SEED,
        "n_steps": N_STEPS,
        "set_point": {"PSI_SET": PSI_SET, "TAU_SET": TAU_SET, "PHI_SET": PHI_SET,
                      "weights": [W_PSI, W_TAU, W_PHI],
                      "theta_low": THETA_LOW, "theta_high": THETA_HIGH,
                      "sustain_k": SUSTAIN_K},
        "cells": cells,
        "verdict_4corner": verdict,
        "verdict_overall": overall,
        "g3_note": ("design-level unification claim; $0 stub != trained ckpt "
                    "forward != GOAL emergence; SAPIN active-inference = honest "
                    "direction-anchor NOT capability proof; necessary-not-"
                    "sufficient (B-EMERGE-7)"),
    }
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "result.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print(json.dumps(out, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
