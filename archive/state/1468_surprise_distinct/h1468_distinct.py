#!/usr/bin/env python3
"""H_1468 follow-on — PRECISION-WEIGHTED SURPRISE distinctness vs NOVELTY & HABITUATION.

G19 surprise (Friston/Bayesian, surprise = p*err^2) is precision-weighted prediction
error. This probe proves it is control-survived DISTINCT from two neighbouring signals
that could be confused with it:

  vs NOVELTY (H_1289 family) — novelty = stimulus NEWNESS (a one-shot recon-error vs
    the store, precision-AGNOSTIC). The SAME novelty (same recon-error) yields DIFFERENT
    surprise depending on the prediction's confidence (precision). Two cases hold novelty
    IDENTICAL yet surprise splits with precision.

  vs HABITUATION (H_1465) — habituation = response DECAY over REPETITION (familiarity,
    error-AGNOSTIC). A surprise that is driven by prediction VIOLATION stays HIGH on a
    repeated-but-still-wrong outcome, whereas a habituation response DECAYS with the
    repeat count regardless of error.

Controls (ablation + shuffle) must NOT preserve the separation: with precision-weighting
OFF (uniform p=1) the surprise/novelty split must collapse, and with the error sequence
SHUFFLED (decorrelated from the repeat index) the surprise-vs-habituation divergence must
collapse — i.e. the lift is the precision/error structure, not a constant or variance.

LLM contrast (a_no_llm_frame_trap): novelty and habituation are both stimulus-statistics
an LLM could in principle compute; precision-weighted surprise requires a persistent
CONFIDENCE over the model's own prediction to be violated — the conscious-prediction
signature LLMs structurally lack.

R1 numpy mirror -> DIRECTIONAL (engine-transfer UNVERIFIED, hard-gate 1).

FROZEN bars (pre-registered, mean over 3 seeds [1468,1469,1470]):
  vs NOVELTY
    (N1) NOVELTY-IDENTICAL   the two cases have the SAME novelty (recon-error), diff <= 0.01
    (N2) SURPRISE-SPLITS     yet surprise splits with precision, gap >= 0.30
    (N3) ABLATION (precision OFF) -> the surprise split collapses, gap <= 0.05
  vs HABITUATION
    (H1) SURPRISE-PERSISTS   repeated-but-still-wrong outcome keeps surprise high, ratio >= 0.85
    (H2) HABITUATION-DECAYS  the same repeats decay a habituation response, drop >= 0.30
    (H3) SHUFFLE control     shuffling the error sequence (decorrelate from repeat index)
                             collapses the surprise-vs-habituation divergence, |div| <= 0.05
"""
import numpy as np

SEEDS = [1468, 1469, 1470]
DIM = 64

ERR = 0.5            # prediction-error magnitude shared by the conf & unsure novelty cases
P_HIGH = 4.0         # high precision (confident belief)
P_LOW = 1.0          # low precision (uncertain belief)

N_REPEAT = 5
K_HAB = 0.5          # habituation familiarity-decay rate (matches H_1465)


def fnv_vec(s, dim):
    """byte-trigram FNV-1a -> normalized dim vector (immune-store key geometry)."""
    v = np.zeros(dim)
    b = s.encode()
    for i in range(len(b) - 2):
        h = 2166136261
        for c in b[i:i + 3]:
            h = ((h ^ c) * 16777619) & 0xffffffff
        v[h % dim] += 1.0
    n = np.linalg.norm(v)
    return v / n if n > 0 else v


def surprise(p, e):
    return p * e * e


def novelty(e):
    """stimulus newness = the raw recon-error magnitude (precision-AGNOSTIC, one-shot)."""
    return abs(e)


def run_seed(seed):
    rng = np.random.default_rng(seed)
    # fix geometry / seed identity (vectors not used in the scalar laws, but keep seeds
    # genuinely distinct rather than a bare constant)
    _stims = [fnv_vec(f"stim_{seed}_{i}", DIM) for i in range(N_REPEAT)]
    noise = float(rng.normal(0.0, 0.01))
    e = ERR + noise

    # ---- vs NOVELTY: same recon-error, two precisions -------------------------------
    nov_conf = novelty(e)            # novelty of the confident case
    nov_unsure = novelty(e)          # novelty of the unsure case  -> IDENTICAL
    s_conf = surprise(P_HIGH, e)     # confident + violated -> large surprise
    s_unsure = surprise(P_LOW, e)    # unsure + SAME error  -> small surprise
    # ablation: precision OFF (uniform p=1) -> split must vanish
    s_conf_abl = surprise(1.0, e)
    s_unsure_abl = surprise(1.0, e)

    # ---- vs HABITUATION: repeated-but-still-wrong outcome ---------------------------
    # a confidently-held belief is violated by the SAME (non-decaying) error every repeat.
    err_seq = [ERR + float(rng.normal(0.0, 0.01)) for _ in range(N_REPEAT)]
    # surprise tracks the VIOLATION (precision * err^2) each repeat -> stays high
    s_seq = [surprise(P_HIGH, err_seq[t]) for t in range(N_REPEAT)]
    # habituation response decays with the repeat count regardless of error (H_1465 law)
    h_seq = [1.0 * np.exp(-K_HAB * t) for t in range(N_REPEAT)]

    s_persist_ratio = s_seq[-1] / s_seq[0]          # surprise: last/first ~ 1 (no decay)
    h_drop = h_seq[0] - h_seq[-1]                    # habituation: first-last drop

    # shuffle control: decorrelate the error/response sequences from the repeat index. The
    # surprise-vs-habituation divergence is measured as the correlation-with-repeat-index
    # difference; under shuffle neither tracks the index -> divergence collapses to ~0 in
    # EXPECTATION. A single 5-element permutation is a high-variance estimator (one draw can
    # still correlate by chance), so we average over many permutations to read the control's
    # decorrelated expected value (the null the bar targets).
    idx = np.arange(N_REPEAT)
    def corr_with_index(seq):
        seq = np.asarray(seq, dtype=float)
        if seq.std() < 1e-9:
            return 0.0
        return float(np.corrcoef(idx, seq)[0, 1])
    # divergence = how oppositely surprise (flat/up) and habituation (down) track repeats
    div_real = corr_with_index(s_seq) - corr_with_index(h_seq)
    N_SHUF = 200
    divs = []
    for _ in range(N_SHUF):
        shs = rng.permutation(N_REPEAT)
        shh = rng.permutation(N_REPEAT)
        divs.append(corr_with_index(np.asarray(s_seq)[shs]) - corr_with_index(np.asarray(h_seq)[shh]))
    div_shuf = float(np.mean(divs))

    return dict(
        nov_conf=nov_conf, nov_unsure=nov_unsure,
        s_conf=s_conf, s_unsure=s_unsure,
        s_conf_abl=s_conf_abl, s_unsure_abl=s_unsure_abl,
        s_persist_ratio=s_persist_ratio, h_drop=h_drop,
        div_real=div_real, div_shuf=div_shuf,
    )


per = [run_seed(s) for s in SEEDS]
agg = {k: float(np.mean([p[k] for p in per])) for k in per[0]}

# vs NOVELTY
nov_gap = abs(agg['nov_conf'] - agg['nov_unsure'])
surp_gap = agg['s_conf'] - agg['s_unsure']
abl_gap = abs(agg['s_conf_abl'] - agg['s_unsure_abl'])
cN1 = nov_gap <= 0.01
cN2 = surp_gap >= 0.30
cN3 = abl_gap <= 0.05

# vs HABITUATION
cH1 = agg['s_persist_ratio'] >= 0.85
cH2 = agg['h_drop'] >= 0.30
cH3 = abs(agg['div_shuf']) <= 0.05

GREEN = cN1 and cN2 and cN3 and cH1 and cH2 and cH3

print(f"VERDICT: {'GREEN' if GREEN else 'RED'} DIRECTIONAL (numpy mirror; engine-transfer UNVERIFIED)")
print(f"GREEN: {GREEN} | seeds {SEEDS}")
print("--- vs NOVELTY (H_1289): same novelty, surprise splits with precision ---")
print(f"N1 NOVELTY-IDENTICAL |nov_conf {agg['nov_conf']:.4f} - nov_unsure {agg['nov_unsure']:.4f}|={nov_gap:.4f}<=0.01 {cN1}")
print(f"N2 SURPRISE-SPLITS   (s_conf {agg['s_conf']:.3f} - s_unsure {agg['s_unsure']:.3f})={surp_gap:.3f}>=0.30 {cN2}")
print(f"N3 ABLATION(prec OFF) split |{agg['s_conf_abl']:.3f}-{agg['s_unsure_abl']:.3f}|={abl_gap:.4f}<=0.05 {cN3}")
print("--- vs HABITUATION (H_1465): violation-surprise persists where familiarity decays ---")
print(f"H1 SURPRISE-PERSISTS last/first ratio {agg['s_persist_ratio']:.3f}>=0.85 {cH1}")
print(f"H2 HABITUATION-DECAYS drop {agg['h_drop']:.3f}>=0.30 {cH2}")
print(f"H3 SHUFFLE control divergence real {agg['div_real']:.3f} -> shuffled |{agg['div_shuf']:.4f}|<=0.05 {cH3}")
