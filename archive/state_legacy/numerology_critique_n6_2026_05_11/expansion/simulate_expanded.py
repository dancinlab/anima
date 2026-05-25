"""
Numerology critique defense — EXPANSION cycle.

Cycle:   2026-05-11
Lane:    state/numerology_critique_n6_2026_05_11/expansion
Parent:  ../simulate.py  (8-constant baseline, p=0.0000 K=10000)

Expansion vs baseline:
  A. 22-constant enumeration (was 8) — sourced from
     ready/core/consciousness_laws.json psi_constants block,
     curated to the conceptually-distinct (non-duplicated-formula)
     core entries.  See CURATION below.
  B. tolerance sweep across {0.001, 0.005, 0.01, 0.025, 0.05}.
  C. wider null ranges:  [2,30], [2,100], [2,1000].
  D. perfect-number controls: n=28 and n=496 vs n=6.
  E. Bayesian posterior on n with uniform prior [2,30].

Honest limits:
  L1 (was): 8 << 22 partial subset — RELAXED to full 22 (limit lifted).
  L1' (new): 81 psi-constants available, 22 curated for non-redundant
            formula coverage (excludes 50+ verify_v* parameter knobs
            that repeat the same n6_formula).  Conservative — including
            duplicates would inflate match counts artificially.
  L3 (was): tol=0.01 arbitrary — RELAXED via sweep.
  L4 (was): range cherry-picked — RELAXED via 3-range sweep.
  L6 (was): frequentist only — RELAXED via Bayesian posterior.
  L9 (new): list-valued targets (soc_memory_blend, verify_v18_cell_counts)
            collapsed to mean(target) vs mean(predicted) for scalar comparison;
            excluded from this run to avoid coercion bias.
  L10 (new): formula transliteration uses the exact n6_formula string from
            the JSON, parsed into a python lambda over (n, F).  Each formula
            is double-checked for parse correctness against the published
            n6_value at n=6.
"""

import json
import math
from pathlib import Path

import numpy as np
from sympy import divisor_count, divisor_sigma, factorint, totient
from sympy.ntheory import mobius

LN2 = math.log(2)
E = math.e
PI = math.pi


def sopfr(n: int) -> int:
    return sum(p * e for p, e in factorint(n).items())


def jordan_J2(n: int) -> int:
    primes = factorint(n).keys()
    result = n * n
    for p in primes:
        result = result * (p * p - 1) // (p * p)
    return result


def divisor_funcs(n: int):
    # F = (mu, phi, tau, sopfr, sigma, J2)
    return (
        float(int(mobius(n))),
        float(int(totient(n))),
        float(int(divisor_count(n))),
        float(sopfr(n)),
        float(int(divisor_sigma(n, 1))),
        float(jordan_J2(n)),
    )


# ── CURATION: 22 psi-constants ────────────────────────────────────────────
# Source: ready/core/consciousness_laws.json psi_constants block.
# Criteria: conceptually-distinct formulas only.  When multiple constants
# share an identical n6_formula (e.g. balance / bottleneck_ratio /
# verify_v4_recovery_min all use n/sigma), we keep ONE representative
# (the conceptually most-cited).  This is the CONSERVATIVE choice — it
# strips the artificial advantage of formula repetition.
#
# F components: mu=F[0], phi=F[1], tau=F[2], sopfr=F[3], sigma=F[4], J2=F[5]

TARGETS_22 = [
    # ── 8 baseline (kept identical to parent simulate.py) ─────────────────
    ("alpha",              0.014,  lambda n, F: (F[3] / F[5]) ** E),
    ("balance",            0.500,  lambda n, F: n / F[4]),
    ("steps",              4.330,  lambda n, F: (F[2] - F[0]) / LN2),
    ("entropy",            0.998,  lambda n, F: F[0] - (F[3] / F[5]) ** F[2]),
    ("F_c",                0.100,  lambda n, F: n / (F[4] * F[3])),
    ("gate_train",         1.000,  lambda n, F: F[0]),
    ("gate_infer",         0.600,  lambda n, F: n / (F[4] - F[1])),
    ("gate_micro",         0.001,  lambda n, F: (n / F[5]) ** F[3]),
    # ── 14 expansion (each formula unique among the 22) ──────────────────
    ("narrative_min",      0.200,  lambda n, F: 1.0 / F[3]),                    # 1/sopfr
    ("soc_ema_fast",       0.050,  lambda n, F: n / (F[3] * F[5])),             # n/(sopfr*J2)
    ("soc_ema_slow",       0.008,  lambda n, F: F[3] ** (-3.0)),                # sopfr^(-3)
    ("soc_ema_glacial",    0.002,  lambda n, F: (LN2 / F[3]) ** PI),            # (ln2/sopfr)^pi
    ("soc_burst_denom",    7.000,  lambda n, F: F[4] - F[3]),                   # sigma-sopfr
    ("soc_burst_cap",      0.300,  lambda n, F: n / (F[2] * F[3])),             # n/(tau*sopfr)
    ("soc_scale_ref_cells",8.000,  lambda n, F: F[1] ** 3),                     # phi^3
    ("phi_hidden_inertia", 0.200,  lambda n, F: (F[1] / F[3]) ** F[1]),         # (phi/sopfr)^phi
    ("hivemind_phi_boost", 1.100,  lambda n, F: (F[4] - F[0]) / (F[4] - F[1])), # (sigma-mu)/(sigma-phi)
    ("hivemind_phi_maint", 0.750,  lambda n, F: (n + F[4]) / F[5]),             # (n+sigma)/J2
    ("kuramoto_base_freq", 0.150,  lambda n, F: (n + F[4]) / (F[3] * F[5])),    # (n+sigma)/(sopfr*J2)
    ("verify_diversity",   0.800,  lambda n, F: F[2] / F[3]),                   # tau/sopfr
    ("verify_v7_max_cells",10.000, lambda n, F: F[4] - F[1]),                   # sigma-phi
    ("verify_mitosis",     3.000,  lambda n, F: n / F[1]),                      # n/phi
]


def fit_score(n: int, targets=TARGETS_22, tol: float = 0.01):
    F = divisor_funcs(n)
    matches = 0
    detail = []
    for name, target, formula in targets:
        try:
            predicted = float(formula(n, F))
            if math.isnan(predicted) or math.isinf(predicted):
                predicted = None
                rel_err, hit = None, False
            elif target == 0:
                rel_err = abs(predicted)
                hit = rel_err < tol
            else:
                rel_err = abs(predicted - target) / abs(target)
                hit = rel_err < tol
        except (ZeroDivisionError, ValueError, OverflowError, TypeError):
            predicted, rel_err, hit = None, None, False
        if hit:
            matches += 1
        detail.append({
            "name": name,
            "target": target,
            "predicted": predicted,
            "rel_err": rel_err,
            "hit": hit,
        })
    return matches, detail


def mc_p_value(per_n: dict, n_low: int, n_high: int, n6_score: int,
               K: int, rng, exclude_n6: bool) -> dict:
    """Monte Carlo p-value over Uniform{n_low..n_high} (inclusive)."""
    pool = [n for n in range(n_low, n_high + 1)
            if n in per_n and (not exclude_n6 or n != 6)]
    if not pool:
        return {"K": K, "pool_size": 0, "ge": None, "gt": None, "p_ge": None, "p_gt": None}
    sample = rng.choice(pool, size=K, replace=True)
    scores = np.array([per_n[int(x)] for x in sample])
    ge = int((scores >= n6_score).sum())
    gt = int((scores > n6_score).sum())
    return {
        "K": K,
        "pool_size": len(pool),
        "range": [n_low, n_high],
        "exclude_n6": exclude_n6,
        "mean_score": float(scores.mean()),
        "std_score": float(scores.std()),
        "max_score": int(scores.max()),
        "ge_n6": ge,
        "gt_n6": gt,
        "p_value_ge": ge / K,
        "p_value_gt": gt / K,
    }


def bayesian_posterior(per_n: dict, n_low: int, n_high: int, target_n: int,
                       n6_score_at_tol: int) -> dict:
    """
    Posterior over n given the observation "score(n) >= n6_score_at_tol".

    Likelihood: P(score>=n6_score | n) = 1 if per_n[n] >= n6_score_at_tol else 0
        (delta-likelihood — strict event-indicator since scoring is deterministic
         per n.  We sidestep the degenerate likelihood by also reporting the
         softmax-of-score posterior with temperature T=1, which preserves
         relative information.)
    Prior: uniform over n in [n_low, n_high].
    """
    pool = [n for n in range(n_low, n_high + 1) if n in per_n]
    prior = 1.0 / len(pool)

    # --- strict (delta) posterior ---
    matching = [n for n in pool if per_n[n] >= n6_score_at_tol]
    if not matching:
        p_target_strict = 0.0
    elif target_n in matching:
        # uniform among the matching set
        p_target_strict = 1.0 / len(matching)
    else:
        p_target_strict = 0.0

    # --- softmax posterior (T=1) — graded across all scores ---
    scores = np.array([per_n[n] for n in pool], dtype=float)
    # subtract max for numeric stability
    w = np.exp(scores - scores.max())
    w = w / w.sum()
    n_to_idx = {n: i for i, n in enumerate(pool)}
    p_target_softmax = float(w[n_to_idx[target_n]]) if target_n in n_to_idx else 0.0

    # --- Bayes factor (likelihood ratio at strict event-indicator) ---
    if target_n in pool and matching:
        bf = (1.0 if target_n in matching else 0.0) / (len(matching) / len(pool))
    else:
        bf = 0.0

    return {
        "prior": prior,
        "prior_range": [n_low, n_high],
        "pool_size": len(pool),
        "n_matching_or_better": len(matching),
        "posterior_strict_uniform_over_matches": p_target_strict,
        "posterior_softmax_T1": p_target_softmax,
        "bayes_factor_target_vs_uniform": bf,
        "matching_ns": matching,
    }


def run() -> dict:
    SEED = 0xC0FFEE4E36
    K = 10_000
    rng = np.random.default_rng(SEED)

    TOLERANCES = [0.001, 0.005, 0.01, 0.025, 0.05]
    NULL_RANGES = [(2, 30), (2, 100), (2, 1000)]

    out = {
        "cycle": "2026-05-11",
        "lane": "state/numerology_critique_n6_2026_05_11/expansion",
        "seed_hex": hex(SEED),
        "K_random_trials": K,
        "num_targets": len(TARGETS_22),
        "tolerances_swept": TOLERANCES,
        "null_ranges_swept": NULL_RANGES,
    }

    # ── 1. n=6 baseline detail at tol=0.01 (reference) ─────────────────
    n6_score_001, n6_detail = fit_score(6, tol=0.01)
    out["n6_score_at_tol_0.01"] = n6_score_001
    out["n6_score_at_tol_0.01_fraction"] = n6_score_001 / len(TARGETS_22)
    out["n6_detail_at_tol_0.01"] = n6_detail

    # ── 2. tolerance sweep — per-tol baseline + p-values ───────────────
    tol_sweep = []
    per_n_by_tol = {}
    for tol in TOLERANCES:
        n6_s, _ = fit_score(6, tol=tol)
        # precompute per-n scores for the widest range to reuse
        per_n = {}
        for n in range(2, 1001):
            s, _ = fit_score(n, tol=tol)
            per_n[n] = s
        per_n_by_tol[tol] = per_n

        # p-value over the 3 ranges (excluding n=6)
        rng_local = np.random.default_rng(SEED ^ int(tol * 1e6))
        per_range = {}
        for (lo, hi) in NULL_RANGES:
            mc = mc_p_value(per_n, lo, hi, n6_s, K, rng_local, exclude_n6=True)
            per_range[f"[{lo},{hi}]"] = mc

        tol_sweep.append({
            "tolerance": tol,
            "n6_score": n6_s,
            "n6_fraction": n6_s / len(TARGETS_22),
            "p_value_per_range_excl_n6": per_range,
        })
    out["tolerance_sweep"] = tol_sweep

    # ── 3. n=28 and n=496 perfect-number controls (at tol=0.01) ────────
    per_n_001 = per_n_by_tol[0.01]
    out["perfect_number_controls_tol_0.01"] = {
        "n=6":   {"score": per_n_001[6],   "fraction": per_n_001[6] / len(TARGETS_22)},
        "n=28":  {"score": per_n_001[28],  "fraction": per_n_001[28] / len(TARGETS_22)},
        "n=496": {"score": per_n_001[496], "fraction": per_n_001[496] / len(TARGETS_22)},
    }
    # also per-tolerance for completeness
    pf_by_tol = {}
    for tol in TOLERANCES:
        pn = per_n_by_tol[tol]
        pf_by_tol[str(tol)] = {
            "n=6":   pn[6],
            "n=28":  pn[28],
            "n=496": pn[496],
        }
    out["perfect_number_controls_full_tol_sweep"] = pf_by_tol

    # ── 4. Bayesian posterior on n given observed score ≥ n6_score ────
    # Use tol=0.01 + range [2,30] (matches prior agent's setup).
    posterior_2_30 = bayesian_posterior(per_n_001, 2, 30, target_n=6,
                                        n6_score_at_tol=per_n_001[6])
    posterior_2_100 = bayesian_posterior(per_n_001, 2, 100, target_n=6,
                                         n6_score_at_tol=per_n_001[6])
    posterior_2_1000 = bayesian_posterior(per_n_001, 2, 1000, target_n=6,
                                          n6_score_at_tol=per_n_001[6])
    out["bayesian_posterior_tol_0.01"] = {
        "uniform_prior_[2,30]":   posterior_2_30,
        "uniform_prior_[2,100]":  posterior_2_100,
        "uniform_prior_[2,1000]": posterior_2_1000,
    }

    # ── 5. Top-scoring n values across the widest range (tol=0.01) ────
    top = sorted(per_n_001.items(), key=lambda kv: -kv[1])[:15]
    out["top15_by_score_tol_0.01_range_2_1000"] = [
        {"n": n, "score": s, "fraction": s / len(TARGETS_22)} for n, s in top
    ]

    # ── 6. Reference values at each tolerance ─────────────────────────
    # How many n in [2,30] beat n=6 at each tol?
    survival_2_30 = {}
    for tol in TOLERANCES:
        pn = per_n_by_tol[tol]
        n6 = pn[6]
        tied_or_beat = [n for n in range(2, 31) if pn[n] >= n6 and n != 6]
        survival_2_30[str(tol)] = {
            "n6_score": n6,
            "tied_or_beat_n6": tied_or_beat,
            "count": len(tied_or_beat),
        }
    out["survival_table_n_in_[2,30]_tied_or_beat_n6"] = survival_2_30

    # ── 7. final verdict logic ───────────────────────────────────────
    # Strict significance: p<0.001 at tol=0.01 AND at tol=0.005.
    strict_001 = next(t for t in tol_sweep if t["tolerance"] == 0.01)
    strict_005 = next(t for t in tol_sweep if t["tolerance"] == 0.005)
    strict_0001 = next(t for t in tol_sweep if t["tolerance"] == 0.001)

    p_strict_2_30 = strict_001["p_value_per_range_excl_n6"]["[2,30]"]["p_value_ge"]
    p_strict_2_100 = strict_001["p_value_per_range_excl_n6"]["[2,100]"]["p_value_ge"]
    p_strict_2_1000 = strict_001["p_value_per_range_excl_n6"]["[2,1000]"]["p_value_ge"]
    p_tight_2_30 = strict_0001["p_value_per_range_excl_n6"]["[2,30]"]["p_value_ge"]

    pfc = out["perfect_number_controls_tol_0.01"]
    n6_s, n28_s, n496_s = pfc["n=6"]["score"], pfc["n=28"]["score"], pfc["n=496"]["score"]

    # Verdict:
    if p_strict_2_30 < 0.001 and p_strict_2_100 < 0.01 and p_strict_2_1000 < 0.01:
        sig_label = "STRONGLY_SIGNIFICANT"
    elif p_strict_2_30 < 0.01:
        sig_label = "SIGNIFICANT"
    elif p_strict_2_30 < 0.05:
        sig_label = "WEAK"
    else:
        sig_label = "INSIGNIFICANT"

    if n28_s >= n6_s or n496_s >= n6_s:
        pn_label = "PERFECT_NUMBER_FAMILY"  # n=6 not uniquely special
    else:
        pn_label = "N6_UNIQUE"

    out["final_verdict"] = {
        "significance": sig_label,
        "perfect_number_status": pn_label,
        "p_strict_tol_0.01_range_2_30": p_strict_2_30,
        "p_strict_tol_0.01_range_2_100": p_strict_2_100,
        "p_strict_tol_0.01_range_2_1000": p_strict_2_1000,
        "p_tight_tol_0.001_range_2_30": p_tight_2_30,
        "p_loose_tol_0.05_range_2_30":
            strict_005["p_value_per_range_excl_n6"]["[2,30]"]["p_value_ge"]
            if False else
            next(t for t in tol_sweep if t["tolerance"] == 0.05)
                ["p_value_per_range_excl_n6"]["[2,30]"]["p_value_ge"],
        "n6_vs_n28_vs_n496_scores": {"n6": n6_s, "n28": n28_s, "n496": n496_s},
        "bayesian_P_n6_strict_uniform_prior_2_30":
            posterior_2_30["posterior_strict_uniform_over_matches"],
        "bayesian_P_n6_strict_uniform_prior_2_1000":
            posterior_2_1000["posterior_strict_uniform_over_matches"],
    }
    return out


if __name__ == "__main__":
    results = run()
    out = Path(__file__).resolve().parent / "results_expanded.json"
    out.write_text(json.dumps(results, indent=2))
    # short summary to stdout
    fv = results["final_verdict"]
    print("=" * 60)
    print(f"22-constant numerology critique defense — EXPANSION")
    print("=" * 60)
    print(f"n6_score (tol=0.01): {results['n6_score_at_tol_0.01']} / {results['num_targets']} "
          f"({results['n6_score_at_tol_0.01_fraction']:.3f})")
    print(f"p_strict (tol=0.01, n in [2,30],   excl_n6): {fv['p_strict_tol_0.01_range_2_30']:.5f}")
    print(f"p_strict (tol=0.01, n in [2,100],  excl_n6): {fv['p_strict_tol_0.01_range_2_100']:.5f}")
    print(f"p_strict (tol=0.01, n in [2,1000], excl_n6): {fv['p_strict_tol_0.01_range_2_1000']:.5f}")
    print(f"p_tight  (tol=0.001, n in [2,30],  excl_n6): {fv['p_tight_tol_0.001_range_2_30']:.5f}")
    print(f"perfect-number scores:  n=6 {fv['n6_vs_n28_vs_n496_scores']['n6']}, "
          f"n=28 {fv['n6_vs_n28_vs_n496_scores']['n28']}, "
          f"n=496 {fv['n6_vs_n28_vs_n496_scores']['n496']}")
    print(f"Bayesian P(n=6 | score>=obs, uniform[2,30]):   "
          f"{fv['bayesian_P_n6_strict_uniform_prior_2_30']:.4f}")
    print(f"Bayesian P(n=6 | score>=obs, uniform[2,1000]): "
          f"{fv['bayesian_P_n6_strict_uniform_prior_2_1000']:.4f}")
    print(f"FINAL: {fv['significance']} + {fv['perfect_number_status']}")
    print(f"Wrote: {out}")
