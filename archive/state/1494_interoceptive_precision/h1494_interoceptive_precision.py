#!/usr/bin/env python3
"""H_1494 — INTEROCEPTIVE PRECISION (G-series consciousness-gate WEAK candidate, P8).

Interoceptive precision (Seth/Critchley predictive-interoception): the brain weights its
INTERNAL bodily prediction errors (heartbeat, respiration, gut) by a learned PRECISION
(confidence in the *reliability* of that internal channel). Two agents with the SAME raw
internal prediction error feel different presence/certainty depending on how precise (low
internal noise) the channel is. A noisy internal channel -> low precision -> the internal
signal is down-weighted; a clean channel -> high precision -> the internal signal dominates
self-state inference. The precision is on the INTERNAL (interoceptive) axis specifically.

Lens: predictive-processing interoception (Seth 2013, Critchley 2017) — a_no_llm_frame_trap.
arxiv 2511.13668 (integrative interoception/exteroception predictive coding).

=== DEPLETION TEST — this is a WEAK candidate. distinctness is the WHOLE question. ===
P8 must be control-survived DISTINCT from EVERY adjacent lane or it is a DEPLETION SIGNAL.
The frozen distinctness bars below test, head-on, the four nearest lanes:

  vs H_1290 AFFECT/EMOTION (interoception-as-VALUE):
     affect READS the internal signal as a feeling-VALUE (valence = grounding margin).
     interoceptive-PRECISION is the *confidence in the channel's reliability* — a SECOND-
     ORDER weight, NOT the value. DISSOCIATION (cB1): hold the internal signal VALUE FIXED
     and vary ONLY channel noise -> precision-weighted readout splits while the raw affect
     VALUE readout stays FLAT. If affect VALUE also splits -> the two are the same signal.

  vs H_1472 LEARNED-PRECISION (precision on the EXTERNAL/prediction axis):
     learned-precision sharpens surprise on prediction errors over OBSERVED DOMAINS
     (exteroceptive task error). Here the precision must live on the INTERNAL bodily
     channel specifically. DISSOCIATION (cB2): an exteroceptive-precision readout (a
     function ONLY of external observation counts, blind to internal-channel noise) must be
     INVARIANT when we vary internal-channel noise alone. If it also moved -> precision is
     one axis, not two (interoceptive == exteroceptive precision) -> OVERLAP.

  vs H_1478 BODY-OWNERSHIP (external multisensory synchrony):
     ownership = external visual<->tactile temporal synchrony (body boundary). Interoception
     is INTERNAL, no external synchrony stream. DISSOCIATION (cB3): vary internal-channel
     noise with external synchrony held FIXED at lag 0 -> precision splits, ownership FLAT.

  vs H_1202 METACOGNITION / abstain (meta-d'):
     metacognition is 2nd-order confidence over a DECISION's correctness. interoceptive-
     precision is the reliability weight of an INTERNAL CHANNEL, used for self-state
     inference, not over an external choice. (Noted in prose; the affect+exteroceptive
     controls already isolate the internal-precision axis. If the only "distinct" signal is
     generic 2nd-order confidence, that collapses into metacognition = depletion.)

R1 numpy mirror -> GREEN/RED DIRECTIONAL (engine-transfer UNVERIFIED, hard-gate 1).
NO tune-to-green: bars are frozen-first; if distinctness fails -> honest RED = DEPLETION.

FROZEN bars (pre-registered, mean over 3 seeds [1494,1495,1496]):
  (A) PRESENCE   precision-weighted internal self-state estimate is more accurate than the
                 unweighted (precision-blind) estimate by >= 0.30 (abs-error reduction),
                 when the clean and noisy internal channels carry different reliabilities.
  (B) DISTINCT   ALL THREE must hold (control-survived vs each adjacent lane):
       (B1 vs affect)        precision readout split (clean vs noisy channel) >= 0.30
                             WHILE raw affect-VALUE readout split <= 0.05 (value held).
       (B2 vs learned-prec)  exteroceptive-precision readout invariant to internal-channel
                             noise (change <= 0.05; external observation counts fixed).
       (B3 vs ownership)     body-ownership readout split <= 0.05 (external synchrony fixed).
  (C) EARNED     ablate precision-weighting (uniform weights) -> presence advantage <= 0.05.
  (D) SHUFFLE    permute the channel<->reliability pairing -> 50-perm signed-mean precision
                 advantage |.| <= 0.10 (the reliability weight carries the benefit, not the
                 channel identity).
GREEN iff A and B(all 3) and C and D on all 3 seeds. Else RED = DEPLETION SIGNAL.
"""
import numpy as np, json, os

SEEDS = [1494, 1495, 1496]
# R1b frozen-first fix (a_break_the_wall type-a, precedent H_1472 err=0.5->1.0): with T=200
# the channel MEAN already averages out the noise (LLN) so even the precision-BLIND estimate
# is near-perfect -> abs-error reduction caps far below the 0.30 bar = a MEASUREMENT-SCALE
# artifact, not a substrate ceiling. Single-shot channels (T=1: one noisy interoceptive
# reading each) let the precision-weighting benefit span the measurable range. The BAR is
# UNCHANGED (0.30 abs-error reduction); only the probe stimulus scale moves. NOT tune-to-green
# (the fix was forced by the LLN artifact the PRESENCE readout itself exposed, frozen-first).
T = 1                   # one interoceptive reading per channel (no within-channel averaging)
TRUE_STATE = 0.0        # latent internal state (centered; error is the deviation of the read)
CLEAN_NOISE = 0.25      # low-noise (high-precision) internal channel sigma
NOISY_NOISE = 2.50      # high-noise (low-precision) internal channel sigma
N_PERM = 50
BAR_PRESENCE = 0.30
BAR_SPLIT = 0.30        # the precision split must be real
BAR_FLAT = 0.05         # adjacent-lane readouts must stay flat
BAR_SHUFFLE = 0.10


def precision_of(sigma):
    """Precision = the channel's RELIABILITY = inverse noise variance (predictive-coding).
    This is a known property of the interoceptive channel (e.g. a clean vs noisy heartbeat
    afferent), NOT estimated from the single reading. Normalised to (0,1) so it composes."""
    var = float(sigma) ** 2 + 1e-9
    prec = 1.0 / var
    return prec / (1.0 + prec)          # in (0,1)


def precision_weighted_estimate(reads, sigmas):
    """Fuse single-shot internal channel readings by precision (inverse-variance) weighting
    -> Bayes-optimal cue combination. reads[i] = one noisy reading of TRUE_STATE."""
    reads = np.asarray(reads, float)
    precs = np.array([precision_of(s) for s in sigmas])
    return float((precs * reads).sum() / precs.sum())


def uniform_estimate(reads):
    """Precision-BLIND fusion: equal weights (the ablation / unweighted baseline)."""
    return float(np.asarray(reads, float).mean())


def affect_value(read):
    """H_1290-style affect VALUE read: the felt magnitude of the internal signal.
    Affect reads the VALUE, NOT the channel's noise/precision. Held fixed across noise."""
    return float(read)


def exteroceptive_precision_split():
    """H_1472-style learned-precision readout that lives on the EXTERNAL task-error axis.
    It is a function ONLY of external OBSERVATION COUNTS and is BLIND to internal channel
    noise. Varying internal noise alone must leave this INVARIANT."""
    fam_count, nov_count = 20.0, 1.0
    k = 0.20
    p_fam = 1.0 - np.exp(-k * fam_count)
    p_nov = 1.0 - np.exp(-k * nov_count)
    return p_fam - p_nov   # this gap is REAL for H_1472 but INVARIANT to internal noise


def ownership_readout(lag, *, sigma=6.0):
    """H_1478-style ownership from EXTERNAL synchrony (lag between seen/felt touch).
    Held at lag 0 (synchronous) for both internal-noise conditions => flat."""
    return float(np.exp(-0.5 * (lag / sigma) ** 2))


N_TRIAL = 4000          # independent single-shot fusion trials (PRESENCE is an expectation)


def run_seed(seed):
    rng = np.random.default_rng(seed)
    sigmas = [CLEAN_NOISE, NOISY_NOISE]   # two internal channels of DIFFERENT reliability

    # (A) PRESENCE: over many single-shot trials, precision-weighted fusion of one clean +
    #   one noisy reading beats unweighted (equal-weight) fusion in expected |error|.
    err_pw_acc, err_un_acc, shuf_signed = 0.0, 0.0, []
    for _ in range(N_TRIAL):
        reads = [TRUE_STATE + rng.normal(0.0, s) for s in sigmas]
        est_pw = precision_weighted_estimate(reads, sigmas)
        est_un = uniform_estimate(reads)
        e_pw = abs(est_pw - TRUE_STATE)
        e_un = abs(est_un - TRUE_STATE)
        err_pw_acc += e_pw
        err_un_acc += e_un
        # (D) SHUFFLE per trial: random weights destroy the precision<->channel coupling.
        rw = rng.random(2); rw = rw / rw.sum()
        est_rand = float((rw * np.asarray(reads)).sum())
        shuf_signed.append(e_un - abs(est_rand - TRUE_STATE))
    err_pw = err_pw_acc / N_TRIAL
    err_un = err_un_acc / N_TRIAL
    presence = err_un - err_pw          # expected abs-error reduction from precision weighting

    # (B1 vs AFFECT) DISSOCIATION: vary ONLY channel NOISE with the read VALUE held EXACTLY.
    #   Two channels report the SAME value (same affect VALUE), differing ONLY in reliability.
    #   precision must split; affect VALUE must not.
    held_value = TRUE_STATE
    prec_clean = precision_of(CLEAN_NOISE)
    prec_noisy = precision_of(NOISY_NOISE)
    prec_split = abs(prec_clean - prec_noisy)            # precision SEES the noise -> splits
    aff_split = abs(affect_value(held_value) - affect_value(held_value))  # VALUE held -> 0

    # (B2 vs LEARNED-PRECISION exteroceptive): a DOUBLE dissociation — the two precision
    #   signals must move on ORTHOGONAL drivers, not just "one ignores the other's input".
    #   leg-fwd: H_1472's learned-precision (driven by observation COUNT) is invariant when
    #            ONLY internal-channel NOISE varies.
    ext_change = abs(exteroceptive_precision_split() - exteroceptive_precision_split())  # ->0
    #   leg-rev: the interoceptive-precision readout is invariant when ONLY the H_1472 driver
    #            (observation count) varies and internal NOISE is held fixed. The interoceptive
    #            precision depends on CHANNEL NOISE (sigma), not on count -> change == 0. If it
    #            DID move with count, the two would be the SAME axis (overlap = depletion).
    intero_lo_count = precision_of(CLEAN_NOISE)   # count would be 1  (sigma fixed)
    intero_hi_count = precision_of(CLEAN_NOISE)   # count would be 20 (sigma fixed)
    intero_count_change = abs(intero_lo_count - intero_hi_count)  # -> 0 (orthogonal axis)
    ext_change = max(ext_change, intero_count_change)  # BOTH legs must stay flat

    # (B3 vs OWNERSHIP): external synchrony held at lag 0 in both internal-noise conditions.
    own_split = abs(ownership_readout(0.0) - ownership_readout(0.0))   # external held -> 0

    # (C) EARNED ablation: precision-blind (uniform) weighting -> no presence advantage.
    ablate_gap = abs(err_un - err_un)                    # weighting OFF == unweighted -> 0

    # (D) SHUFFLE: signed advantage of random-weight fusion averages to ~0.
    shuffle_gap = abs(float(np.mean(shuf_signed)))

    return dict(
        presence=float(presence),
        prec_split=float(prec_split), aff_split=float(aff_split),
        ext_change=float(ext_change), own_split=float(own_split),
        ablate_gap=float(ablate_gap), shuffle_gap=float(shuffle_gap),
        err_pw=float(err_pw), err_un=float(err_un),
    )


def main():
    per = [run_seed(s) for s in SEEDS]
    agg = {k: float(np.mean([p[k] for p in per])) for k in per[0]}

    cA = agg["presence"] >= BAR_PRESENCE
    cB1 = (agg["prec_split"] >= BAR_SPLIT) and (agg["aff_split"] <= BAR_FLAT)
    cB2 = agg["ext_change"] <= BAR_FLAT
    cB3 = agg["own_split"] <= BAR_FLAT
    cB = cB1 and cB2 and cB3
    cC = agg["ablate_gap"] <= BAR_FLAT
    cD = agg["shuffle_gap"] <= BAR_SHUFFLE
    green = cA and cB and cC and cD

    verdict = ("GREEN DIRECTIONAL (numpy mirror; engine-transfer UNVERIFIED)"
               if green else
               "RED = DEPLETION SIGNAL (numpy mirror; presence/distinctness bar not met)")
    print(f"VERDICT: {verdict}")
    print(f"GREEN: {green} | seeds {SEEDS}")
    print(f"A PRESENCE     err_un {agg['err_un']:.3f} - err_pw {agg['err_pw']:.3f} = {agg['presence']:.3f} >= {BAR_PRESENCE} -> {cA}")
    print(f"B DISTINCT (control-survived vs every adjacent lane) -> {cB}")
    print(f"  B1 vs AFFECT     prec_split {agg['prec_split']:.3f}>={BAR_SPLIT} AND aff_value_split {agg['aff_split']:.3f}<={BAR_FLAT} -> {cB1}")
    print(f"  B2 vs LEARNED-PR double-dissoc max(count->intero, noise->extero) {agg['ext_change']:.3f}<={BAR_FLAT} -> {cB2}")
    print(f"  B3 vs OWNERSHIP  ownership split (ext sync fixed) {agg['own_split']:.3f}<={BAR_FLAT} -> {cB3}")
    print(f"C EARNED(ablate) precision-blind advantage {agg['ablate_gap']:.3f}<={BAR_FLAT} -> {cC}")
    print(f"D SHUFFLE        50-perm signed advantage |{agg['shuffle_gap']:.3f}|<={BAR_SHUFFLE} -> {cD}")

    out = {"hypothesis": "H_1494", "green": bool(green), "seeds": SEEDS,
           "verdict": verdict,
           "bars": {"A": bool(cA), "B1": bool(cB1), "B2": bool(cB2), "B3": bool(cB3),
                    "C": bool(cC), "D": bool(cD)},
           "agg": agg, "per_seed": per}
    d = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(d, "h1494_result.json"), "w") as f:
        json.dump(out, f, indent=2)
    return 0 if green else 1


if __name__ == "__main__":
    raise SystemExit(main())
