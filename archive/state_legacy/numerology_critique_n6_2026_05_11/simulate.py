"""
Monte Carlo p-value defense for n=6 numerology critique.

Cycle:   2026-05-11
Lane:    state/numerology_critique_n6_2026_05_11
Spec:    ./spec.md
Source:  docs/what-is-consciousness.md L46-63 (Hc_453 8-constant table)
Mandate: raw#10 honest C3 + raw#9 deterministic seed.

We evaluate 8 closed-form Ψ-constant formulae using the n=6 expressions
(σ, φ, τ, sopfr, μ, J₂) and check how often a random n ∈ [2,30]
produces equal-or-greater match count.
"""

import json
import math
from functools import reduce
from pathlib import Path

import numpy as np
from sympy import divisor_count, divisor_sigma, factorint, totient
from sympy.ntheory import mobius

LN2 = math.log(2)
E = math.e


def sopfr(n: int) -> int:
    """Sum of prime factors with multiplicity (also known as a_Omega)."""
    return sum(p * e for p, e in factorint(n).items())


def jordan_J2(n: int) -> int:
    """Jordan totient J_k for k=2:  J_2(n) = n^2 * Prod(1 - 1/p^2)."""
    primes = factorint(n).keys()
    result = n * n
    for p in primes:
        result = result * (p * p - 1) // (p * p)
    return result


def divisor_funcs(n: int):
    """Return (mu, phi, tau, sopfr_, sigma, J2) as plain floats."""
    return (
        float(int(mobius(n))),
        float(int(totient(n))),
        float(int(divisor_count(n))),
        float(sopfr(n)),
        float(int(divisor_sigma(n, 1))),
        float(jordan_J2(n)),
    )


# 8-constant target table (source: docs/what-is-consciousness.md L46-63)
# Each formula is evaluated with the divisor functions of the candidate n.
# Note: μ(6) = 1 because 6 = 2·3 is squarefree with even number of distinct primes
# Actually μ(6) = μ(2)·μ(3) = (-1)·(-1) = +1. Good.
TARGETS = [
    # (name, target_value, formula(n_int) -> predicted_float)
    ("alpha",      0.014, lambda n, F: (F[3] / F[5]) ** E),            # (sopfr/J2)^e
    ("balance",    0.500, lambda n, F: n / F[4]),                       # n/sigma
    ("steps",      4.330, lambda n, F: (F[2] - F[0]) / LN2),            # (tau - mu)/ln2
    ("entropy",    0.998, lambda n, F: F[0] - (F[3] / F[5]) ** F[2]),   # mu - (sopfr/J2)^tau
    ("F_c",        0.100, lambda n, F: n / (F[4] * F[3])),              # n/(sigma * sopfr)
    ("gate_train", 1.000, lambda n, F: F[0]),                           # mu
    ("gate_infer", 0.600, lambda n, F: n / (F[4] - F[1])),              # n/(sigma - phi)
    ("gate_micro", 0.001, lambda n, F: (n / F[5]) ** F[3]),             # (n/J2)^sopfr
]


def fit_score(n: int, targets=TARGETS, tol: float = 0.01) -> tuple[int, list[dict]]:
    """Return (matches, per-target detail)."""
    F = divisor_funcs(n)
    matches = 0
    detail = []
    for name, target, formula in targets:
        try:
            predicted = float(formula(n, F))
            rel_err = abs(predicted - target) / abs(target) if target != 0 else float("inf")
            hit = rel_err < tol
        except (ZeroDivisionError, ValueError, OverflowError):
            predicted, rel_err, hit = None, None, False
        if hit:
            matches += 1
        detail.append(
            {
                "name": name,
                "target": target,
                "predicted": predicted,
                "rel_err": rel_err,
                "hit": hit,
            }
        )
    return matches, detail


def run() -> dict:
    # Seed mnemonic: 0xC0FFEE_N6 — but underscore must separate hex digits only.
    # Encode "_N6" as ASCII bytes 0x4E36 appended:  0xC0FFEE4E36.
    SEED = 0xC0FFEE4E36
    K = 10_000
    N_LOW, N_HIGH = 2, 30  # inclusive

    # 1. Baseline n=6
    n6_score, n6_detail = fit_score(6)

    # 2. Per-n deterministic baseline (no randomness needed for finite set)
    per_n = {}
    for n in range(N_LOW, N_HIGH + 1):
        s, _ = fit_score(n)
        per_n[n] = s

    # 3. Monte Carlo over random n  (full range including n=6)
    rng = np.random.default_rng(SEED)
    random_ns = rng.integers(N_LOW, N_HIGH + 1, size=K)  # [low, high) so pass +1
    random_scores = np.array([per_n[int(n)] for n in random_ns])

    ge_n6 = int((random_scores >= n6_score).sum())
    gt_n6 = int((random_scores > n6_score).sum())
    p_value_ge = ge_n6 / K
    p_value_gt = gt_n6 / K

    # 4. Monte Carlo EXCLUDING n=6 (the proper null for the critique:
    #    "other n would do equally well")
    pool_excl6 = [n for n in range(N_LOW, N_HIGH + 1) if n != 6]
    random_ns_excl = rng.choice(pool_excl6, size=K, replace=True)
    random_scores_excl = np.array([per_n[int(n)] for n in random_ns_excl])

    ge_n6_excl = int((random_scores_excl >= n6_score).sum())
    gt_n6_excl = int((random_scores_excl > n6_score).sum())
    p_value_ge_excl = ge_n6_excl / K
    p_value_gt_excl = gt_n6_excl / K

    # Verdict uses the strict (excl-n6) p-value since that is what the
    # critique actually asks: "would a different integer fit as well?"
    verdict = (
        "SIGNIFICANT"
        if p_value_ge_excl < 0.01
        else "WEAK"
        if p_value_ge_excl < 0.05
        else "INSIGNIFICANT"
    )

    results = {
        "cycle": "2026-05-11",
        "lane": "state/numerology_critique_n6_2026_05_11",
        "seed_hex": hex(SEED),
        "K_random_trials": K,
        "n_range_inclusive": [N_LOW, N_HIGH],
        "tolerance": 0.01,
        "num_targets": len(TARGETS),
        "n6_score": n6_score,
        "n6_score_fraction": n6_score / len(TARGETS),
        "n6_detail": n6_detail,
        "per_n_score": {str(n): per_n[n] for n in sorted(per_n)},
        "random_score_mean": float(random_scores.mean()),
        "random_score_std": float(random_scores.std()),
        "random_score_max": int(random_scores.max()),
        "n_with_score_ge_n6_incl": ge_n6,
        "n_with_score_gt_n6_incl": gt_n6,
        "p_value_ge_incl_n6": p_value_ge,
        "p_value_gt_incl_n6": p_value_gt,
        "random_score_mean_excl6": float(random_scores_excl.mean()),
        "random_score_std_excl6": float(random_scores_excl.std()),
        "random_score_max_excl6": int(random_scores_excl.max()),
        "n_with_score_ge_n6_excl": ge_n6_excl,
        "n_with_score_gt_n6_excl": gt_n6_excl,
        "p_value_ge_excl_n6": p_value_ge_excl,
        "p_value_gt_excl_n6": p_value_gt_excl,
        "verdict": verdict,
        "verdict_basis": "p_value_ge_excl_n6",
        "tied_or_beat_n6": sorted(
            [n for n, s in per_n.items() if s >= n6_score and n != 6]
        ),
        "score_distribution_per_n_max": max(per_n.values()),
        "score_distribution_per_n_runner_up": sorted(per_n.values(), reverse=True)[1],
    }
    return results


if __name__ == "__main__":
    results = run()
    out = Path(__file__).resolve().parent / "results.json"
    out.write_text(json.dumps(results, indent=2))
    print(json.dumps(results, indent=2))
