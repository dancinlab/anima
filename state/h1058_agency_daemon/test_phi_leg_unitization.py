#!/usr/bin/env python3
"""H_1058 · H_9269 Φ-leg redesign — SYNTHETIC-LATENT unit test (no .clm, mini-safe).

Verifies the FROZEN unitization + faithful-Φ path of phi_leg.py on synthetic latent (T x d)
arrays — the parts that do NOT need the real 303M trunk forward — plus that a constant-Φ series
trips the already-landed #3331 VOID guard in agency_T.shuffle_null.

Covered (frozen-instrument invariants):
  (i)   FROZEN units/thresholds are IDENTICAL across decisions when computed from the same
        calibration slice (calibration is per-session, NOT per-decision).
  (ii)  VARYING synthetic H  → VARYING Φ  (the instrument resolves signal).
  (iii) CONSTANT synthetic H → FLAT Φ, and that flat series hooks the #3331 VOID path
        (sd(Φ) < PHI_VAR_EPS ⇒ within_2sigma_null is None / void=True, NOT a false PASS).

Run: PYTHONPATH=cli:core python3 test_phi_leg_unitization.py   (numpy + stdlib only)
"""
import os
import statistics
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import phi_leg
import agency_T

PASS = 0
FAIL = 0


def check(name, cond):
    global PASS, FAIL
    if cond:
        PASS += 1
        print("  PASS  %s" % name)
    else:
        FAIL += 1
        print("  FAIL  %s" % name)


def synth_decision(rng, d, T, level, coupling=0.5):
    """A synthetic (T x d) latent window mimicking one decision's PRE-MoE trunk hidden.

    `level`    drives the per-dim time-MEAN (what calibration's cross-decision variance ranks).
    `coupling` drives how much a SHARED temporal factor (vs iid noise) governs each unit over
               the window → controls inter-unit mutual information → the faithful-Φ magnitude.
               Varying `coupling` across decisions is what makes Φ vary (integration, not level)."""
    base = rng.normal(0.0, 1.0, size=(d,)) * level           # per-dim level (selection signal)
    shared = rng.normal(0.0, 1.0, size=(T, 1))               # one shared temporal factor
    indep = rng.normal(0.0, 1.0, size=(T, d))                # per-unit independent variation
    return base[None, :] + coupling * shared + (1.0 - coupling) * indep


def main():
    rng = np.random.default_rng(1058)
    d, T = 64, phi_leg.T_WIN
    print("=== H_9269 Φ-leg synthetic-latent unit test (d=%d T=%d n_units=%d) ===" % (d, T, phi_leg.N_UNITS))

    # calibration slice: 16 synthetic decisions with varied per-decision levels + couplings
    calib = [synth_decision(rng, d, T, level=float(l), coupling=float(c))
             for l, c in zip(np.linspace(0.5, 2.0, 16), np.linspace(0.2, 0.9, 16))]

    # (i) FROZEN units/thresholds identical across decisions (same calibration slice → same maps)
    frozenA = phi_leg.calibrate_units(calib)
    frozenB = phi_leg.calibrate_units(calib)
    same = all(np.array_equal(frozenA[m]["idx"], frozenB[m]["idx"])
               and np.allclose(frozenA[m]["thr"], frozenB[m]["thr"])
               for m in phi_leg.MACRO_MAPS)
    check("(i) frozen units+thresholds identical across recomputation of same calib slice", same)
    # frozen maps are the SAME object applied to every scored decision (not per-decision reselected)
    n_top = len(frozenA["top_calib_variance"]["idx"])
    n_rnd = len(frozenA["random"]["idx"])
    check("(i) both macro-maps select exactly n_units=%d dims" % phi_leg.N_UNITS,
          n_top == phi_leg.N_UNITS and n_rnd == phi_leg.N_UNITS)

    # (ii) VARYING synthetic H → VARYING Φ (score 24 distinct decisions with the FROZEN top map)
    fm = frozenA["top_calib_variance"]
    scored = [synth_decision(rng, d, T, level=float(l), coupling=float(c))
              for l, c in zip(np.linspace(0.4, 2.5, 24), np.linspace(0.1, 0.95, 24))]
    phis_var = [phi_leg.faithful_phi_frozen(H, fm) for H in scored]
    sd_var = statistics.pstdev(phis_var)
    n_distinct_var = len(set(round(p, 4) for p in phis_var))
    check("(ii) varying H → sd(Φ) >= PHI_VAR_EPS (%.4g >= %.4g)" % (sd_var, agency_T.PHI_VAR_EPS),
          sd_var >= agency_T.PHI_VAR_EPS)
    check("(ii) varying H → multiple distinct Φ (@4sf) : %d distinct" % n_distinct_var,
          n_distinct_var >= 2)

    # (iii) CONSTANT synthetic H → FLAT Φ (identical window every decision → identical Φ)
    const_win = synth_decision(rng, d, T, level=1.0)   # one fixed window, reused verbatim
    phis_const = [phi_leg.faithful_phi_frozen(const_win.copy(), fm) for _ in range(24)]
    sd_const = statistics.pstdev(phis_const)
    check("(iii) constant H → FLAT Φ (sd=%.3g ~ 0)" % sd_const, sd_const <= 1e-12)

    # (iii) the flat Φ series HOOKS the #3331 VOID guard (must NOT be a false PASS)
    T_series = list(np.linspace(-1.0, 1.0, len(phis_const)))    # a real, varying T axis
    void_res = agency_T.shuffle_null(T_series, phis_const, min_other_sd=agency_T.PHI_VAR_EPS)
    check("(iii) flat Φ → agency_T VOID (within_2sigma_null is None, not a bool PASS)",
          void_res.get("void") is True and void_res.get("within_2sigma_null") is None)

    # sanity contrast: the VARYING Φ series is EVALUABLE (not void) under the same guard
    eval_res = agency_T.shuffle_null(T_series[:len(phis_var)], phis_var, min_other_sd=agency_T.PHI_VAR_EPS)
    check("(sanity) varying Φ → EVALUABLE (void=False, within_2sigma_null is a real bool)",
          eval_res.get("void") is False and isinstance(eval_res.get("within_2sigma_null"), bool))

    print("\n%d PASS / %d FAIL" % (PASS, FAIL))
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
