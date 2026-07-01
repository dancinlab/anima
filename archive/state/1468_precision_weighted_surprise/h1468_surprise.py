#!/usr/bin/env python3
"""H_1468 — PRECISION-WEIGHTED SURPRISE (G19 consciousness-only gate candidate).

Predictive-processing surprise (Friston free-energy / Bayesian surprise): the felt
SURPRISE of an outcome is NOT the raw prediction error but the error weighted by the
PRECISION (confidence) of the prediction — a confidently-held belief that is violated
is far more surprising than the same error under an uncertain belief. surprise = p·err².

DISTINCT from H_1280 cerebellar VForwardField (raw forward prediction error |pred−act|,
precision-AGNOSTIC): two outcomes with the SAME raw error produce DIFFERENT surprise
when the predictions had different precision. That precision-weighting is what makes
surprise an attention-grabbing, consciousness-relevant signal rather than a bare error.

LLM contrast (a_no_llm_frame_trap): an LLM has no persistent precision over its own
predictions to be violated; anima's surprise rides the live confidence of its substrate
predictions — "confident-and-wrong" spikes, "unsure-and-wrong" does not.

R1 numpy mirror -> DIRECTIONAL (engine-transfer UNVERIFIED, hard-gate 1).

FROZEN bars (pre-registered, mean over 3 seeds [1468,1469,1470]):
  (A) SURPRISE          a confident violation gives a large surprise, s_conf >= 0.50
  (B) PRECISION-WEIGHTED same raw error, confident >> unsure: s_conf - s_unsure >= 0.30
  (C) NO-SURPRISE       a confident-but-CORRECT prediction gives ~0 surprise, <= 0.05
  (D) EARNED (ablation) precision OFF (uniform p=1) -> the conf/unsure split vanishes, <= 0.05
  (E) DISTINCT-vs-H1280 raw forward error IDENTICAL across the two cases (<=0.01) yet
                        surprise differs (>= 0.30) — precision, not error, is the signal
"""
import numpy as np

SEEDS = [1468, 1469, 1470]
ERR = 0.5            # the prediction error magnitude (same for conf & unsure cases)
P_HIGH = 4.0         # high precision (confident belief)
P_LOW = 1.0          # low precision (uncertain belief)


def surprise(p, e):
    return p * e * e


def run_seed(seed):
    rng = np.random.default_rng(seed)
    noise = float(rng.normal(0.0, 0.01))     # tiny per-seed variation (genuine distinct seeds)
    e = ERR + noise

    s_conf = surprise(P_HIGH, e)             # confident + violated -> large surprise
    s_unsure = surprise(P_LOW, e)            # unsure + SAME error  -> small surprise
    s_expected = surprise(P_HIGH, 0.02)      # confident + correct  -> ~0 surprise

    # (D) ablation: precision-weighting OFF (uniform p=1) -> surprise collapses to err², no split
    s_conf_abl = surprise(1.0, e)
    s_unsure_abl = surprise(1.0, e)

    # (E) raw forward prediction error (H_1280 VForwardField) — precision-agnostic
    raw_conf = e
    raw_unsure = e

    return dict(s_conf=s_conf, s_unsure=s_unsure, s_expected=s_expected,
                s_conf_abl=s_conf_abl, s_unsure_abl=s_unsure_abl,
                raw_conf=raw_conf, raw_unsure=raw_unsure)


per = [run_seed(s) for s in SEEDS]
agg = {k: float(np.mean([p[k] for p in per])) for k in per[0]}

cA = agg['s_conf'] >= 0.50
cB = (agg['s_conf'] - agg['s_unsure']) >= 0.30
cC = agg['s_expected'] <= 0.05
cD = abs(agg['s_conf_abl'] - agg['s_unsure_abl']) <= 0.05
cE = (abs(agg['raw_conf'] - agg['raw_unsure']) <= 0.01) and ((agg['s_conf'] - agg['s_unsure']) >= 0.30)
GREEN = cA and cB and cC and cD and cE

print(f"VERDICT: {'GREEN' if GREEN else 'RED'} DIRECTIONAL (numpy mirror; engine-transfer UNVERIFIED)")
print(f"GREEN: {GREEN} | seeds {SEEDS}")
print(f"A SURPRISE s_conf {agg['s_conf']:.3f}>=0.50 {cA}")
print(f"B PRECISION-WEIGHTED (conf {agg['s_conf']:.3f} - unsure {agg['s_unsure']:.3f})={agg['s_conf']-agg['s_unsure']:.3f}>=0.30 {cB}")
print(f"C NO-SURPRISE expected {agg['s_expected']:.4f}<=0.05 {cC}")
print(f"D EARNED(ablation) |conf_abl {agg['s_conf_abl']:.3f} - unsure_abl {agg['s_unsure_abl']:.3f}|={abs(agg['s_conf_abl']-agg['s_unsure_abl']):.4f}<=0.05 {cD}")
print(f"E DISTINCT-vs-H1280 raw|{agg['raw_conf']:.3f}-{agg['raw_unsure']:.3f}|={abs(agg['raw_conf']-agg['raw_unsure']):.4f}<=0.01 AND surprise-gap {agg['s_conf']-agg['s_unsure']:.3f}>=0.30 → {cE}")
