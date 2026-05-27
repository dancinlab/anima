"""
Numerology critique defense — FORMULA-SEARCH cycle (L12 neutralization).

Cycle:   2026-05-11
Lane:    state/numerology_critique_n6_2026_05_11/formula_search/
Parent:  ../expansion/simulate_expanded.py
Spec:    ./spec.md

L12 question:
  "Could a *different* formula from the same vocabulary fit each random n
   equally well as the published formula fits n=6?"

We DFS over formulas of depth ≤ d for each (n, T) pair and count how many
of the 22 targets admit ANY fitting formula at depth-2 and depth-3.

Seed: 0xF0EAFEA1
"""

import json
import math
import time
from pathlib import Path

import numpy as np
from sympy import divisor_count, divisor_sigma, factorint, totient
from sympy.ntheory import mobius

# ---------------------------------------------------------------------------
# Primitives — match the vocabulary used by the published n6_formula strings
# ---------------------------------------------------------------------------

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


def primitives(n: int) -> dict[str, float]:
    return {
        "1":     1.0,
        "n":     float(n),
        "mu":    float(int(mobius(n))),
        "phi":   float(int(totient(n))),
        "tau":   float(int(divisor_count(n))),
        "sigma": float(int(divisor_sigma(n, 1))),
        "sopfr": float(sopfr(n)) if n > 1 else 0.0,
        "J2":    float(jordan_J2(n)) if n > 1 else 1.0,
        "e":     E,
        "pi":    PI,
        "ln2":   LN2,
    }


# ---------------------------------------------------------------------------
# 22 targets (same as parent expansion lane)
# ---------------------------------------------------------------------------

TARGETS_22 = [
    ("alpha",               0.014),
    ("balance",             0.500),
    ("steps",               4.330),
    ("entropy",             0.998),
    ("F_c",                 0.100),
    ("gate_train",          1.000),
    ("gate_infer",          0.600),
    ("gate_micro",          0.001),
    ("narrative_min",       0.200),
    ("soc_ema_fast",        0.050),
    ("soc_ema_slow",        0.008),
    ("soc_ema_glacial",     0.002),
    ("soc_burst_denom",     7.000),
    ("soc_burst_cap",       0.300),
    ("soc_scale_ref_cells", 8.000),
    ("phi_hidden_inertia",  0.200),
    ("hivemind_phi_boost",  1.100),
    ("hivemind_phi_maint",  0.750),
    ("kuramoto_base_freq",  0.150),
    ("verify_diversity",    0.800),
    ("verify_v7_max_cells", 10.000),
    ("verify_mitosis",      3.000),
]


# ---------------------------------------------------------------------------
# Formula generation — enumerate value-sets up to a given depth
# ---------------------------------------------------------------------------

MAX_ABS = 1e8     # ignore intermediate values that explode
MIN_ABS = 1e-8    # treat near-zero values as zero (skip-divide)
EXP_LIMIT = 5     # |exponent| < 5 to prevent overflow / numerical garbage


def _safe_add(a, b):
    v = a + b
    return v if -MAX_ABS < v < MAX_ABS else None


def _safe_sub(a, b):
    v = a - b
    return v if -MAX_ABS < v < MAX_ABS else None


def _safe_mul(a, b):
    try:
        v = a * b
    except (OverflowError, ValueError):
        return None
    return v if -MAX_ABS < v < MAX_ABS else None


def _safe_div(a, b):
    if abs(b) < MIN_ABS:
        return None
    try:
        v = a / b
    except (OverflowError, ZeroDivisionError, ValueError):
        return None
    return v if -MAX_ABS < v < MAX_ABS else None


def _safe_pow(a, b):
    # restrict exponent magnitude
    if abs(b) >= EXP_LIMIT:
        return None
    # avoid 0^0 ambiguity and negative-base-fractional-exponent (complex)
    if a == 0 and b == 0:
        return None
    if a < 0 and not float(b).is_integer():
        return None
    try:
        v = a ** b
    except (OverflowError, ValueError, ZeroDivisionError):
        return None
    if isinstance(v, complex):
        return None
    if not (-MAX_ABS < v < MAX_ABS):
        return None
    if math.isnan(v) or math.isinf(v):
        return None
    return v


def _safe_log(a):
    if a is None or a <= 0:
        return None
    try:
        v = math.log(a)
    except (ValueError, OverflowError):
        return None
    return v if -MAX_ABS < v < MAX_ABS else None


def _safe_sqrt(a):
    if a is None or a < 0:
        return None
    try:
        v = math.sqrt(a)
    except (ValueError, OverflowError):
        return None
    return v if -MAX_ABS < v < MAX_ABS else None


def _safe_neg(a):
    if a is None:
        return None
    return -a


def hit(predicted, target, tol=0.01):
    if predicted is None:
        return False
    if math.isnan(predicted) or math.isinf(predicted):
        return False
    if target == 0:
        return abs(predicted) < tol
    return abs(predicted - target) / abs(target) < tol


def generate_layer1(n: int) -> set[float]:
    """Depth-1 values: just the primitives."""
    P = primitives(n)
    return set(P.values())


def generate_layer2(n: int, layer1: set[float]) -> set[float]:
    """Depth-2 values: unary(layer1) ∪ (layer1 BIN layer1)."""
    out = set()
    L1 = list(layer1)
    # unary
    for a in L1:
        for fn in (_safe_log, _safe_sqrt, _safe_neg):
            v = fn(a)
            if v is not None and -MAX_ABS < v < MAX_ABS:
                out.add(v)
    # binary on L1×L1
    for a in L1:
        for b in L1:
            for fn in (_safe_add, _safe_sub, _safe_mul, _safe_div, _safe_pow):
                v = fn(a, b)
                if v is not None:
                    out.add(v)
    return out


def generate_layer3(n: int, layer1: set[float], layer2: set[float]) -> set[float]:
    """Depth-3 values: unary(layer2) ∪ (layer2 BIN layer1) ∪ (layer1 BIN layer2).

    To keep depth-3 tractable we limit BIN to layer2 × layer1 (one side at most
    depth-2). This still covers expressions like  (φ/sopfr)^φ  or
    (sigma - mu)/(sigma - phi) when the inner pieces have appeared at depth-2.
    """
    out = set()
    L1 = list(layer1)
    L2 = list(layer2)

    # unary on layer2
    for a in L2:
        for fn in (_safe_log, _safe_sqrt, _safe_neg):
            v = fn(a)
            if v is not None:
                out.add(v)

    # binary: L2 × L1 and L1 × L2
    for a in L2:
        for b in L1:
            for fn in (_safe_add, _safe_sub, _safe_mul, _safe_div, _safe_pow):
                v = fn(a, b)
                if v is not None:
                    out.add(v)
    for a in L1:
        for b in L2:
            for fn in (_safe_add, _safe_sub, _safe_mul, _safe_div, _safe_pow):
                v = fn(a, b)
                if v is not None:
                    out.add(v)
    return out


def search_fit(target: float, n: int, max_depth: int = 3, tol: float = 0.01):
    """Return ('depth', value) for first depth at which ANY formula fits."""
    L1 = generate_layer1(n)
    for v in L1:
        if hit(v, target, tol):
            return 1, v
    if max_depth < 2:
        return None
    L2 = generate_layer2(n, L1)
    for v in L2:
        if hit(v, target, tol):
            return 2, v
    if max_depth < 3:
        return None
    L3 = generate_layer3(n, L1, L2)
    for v in L3:
        if hit(v, target, tol):
            return 3, v
    return None


def score_search(n: int, max_depth: int = 3, tol: float = 0.01):
    """Count # targets that admit ANY formula at depth ≤ max_depth."""
    matches = 0
    detail = []
    # Cache layer sets per n (computed once)
    L1 = generate_layer1(n)
    L2 = generate_layer2(n, L1) if max_depth >= 2 else set()
    L3 = generate_layer3(n, L1, L2) if max_depth >= 3 else set()

    for name, target in TARGETS_22:
        found_depth = None
        found_value = None
        for v in L1:
            if hit(v, target, tol):
                found_depth, found_value = 1, v
                break
        if found_depth is None and max_depth >= 2:
            for v in L2:
                if hit(v, target, tol):
                    found_depth, found_value = 2, v
                    break
        if found_depth is None and max_depth >= 3:
            for v in L3:
                if hit(v, target, tol):
                    found_depth, found_value = 3, v
                    break
        if found_depth is not None:
            matches += 1
        detail.append({
            "name": name,
            "target": target,
            "found_depth": found_depth,
            "found_value": found_value,
        })
    return matches, detail


# ---------------------------------------------------------------------------
# Main driver
# ---------------------------------------------------------------------------

def run() -> dict:
    SEED = 0xF0EAFEA1
    np.random.seed(SEED)

    TOL = 0.01
    N_RANGE = list(range(2, 31))
    MAX_DEPTH = 3

    out = {
        "cycle": "2026-05-11",
        "lane": "state/numerology_critique_n6_2026_05_11/formula_search",
        "seed_hex": hex(SEED),
        "tolerance": TOL,
        "num_targets": len(TARGETS_22),
        "n_range_inclusive": [N_RANGE[0], N_RANGE[-1]],
        "max_depth": MAX_DEPTH,
        "vocabulary": {
            "primitives": ["1", "n", "mu", "phi", "tau", "sigma", "sopfr",
                           "J2", "e", "pi", "ln2"],
            "binary_ops": ["+", "-", "*", "/", "**"],
            "unary_ops":  ["log", "sqrt", "neg"],
            "exp_limit_abs": EXP_LIMIT,
        },
    }

    # depth-2 + depth-3 scoring per n
    per_n_d2 = {}
    per_n_d3 = {}
    per_n_d3_detail_n6 = None
    t0 = time.time()
    for n in N_RANGE:
        s2, _ = score_search(n, max_depth=2, tol=TOL)
        s3, det3 = score_search(n, max_depth=3, tol=TOL)
        per_n_d2[n] = s2
        per_n_d3[n] = s3
        if n == 6:
            per_n_d3_detail_n6 = det3
    out["wall_clock_sec"] = round(time.time() - t0, 2)

    out["per_n_score_depth2"] = {str(n): per_n_d2[n] for n in N_RANGE}
    out["per_n_score_depth3"] = {str(n): per_n_d3[n] for n in N_RANGE}
    out["n6_score_depth2"] = per_n_d2[6]
    out["n6_score_depth3"] = per_n_d3[6]
    out["n6_detail_depth3"] = per_n_d3_detail_n6

    others_d2 = {n: s for n, s in per_n_d2.items() if n != 6}
    others_d3 = {n: s for n, s in per_n_d3.items() if n != 6}

    out["max_other_depth2"] = max(others_d2.values())
    out["max_other_depth3"] = max(others_d3.values())
    out["argmax_other_depth2"] = max(others_d2, key=others_d2.get)
    out["argmax_other_depth3"] = max(others_d3, key=others_d3.get)
    out["mean_other_depth2"] = float(np.mean(list(others_d2.values())))
    out["mean_other_depth3"] = float(np.mean(list(others_d3.values())))
    out["std_other_depth2"] = float(np.std(list(others_d2.values())))
    out["std_other_depth3"] = float(np.std(list(others_d3.values())))

    # Margin: how much does n=6 beat the runner-up under formula search?
    out["margin_depth2"] = per_n_d2[6] - max(others_d2.values())
    out["margin_depth3"] = per_n_d3[6] - max(others_d3.values())

    # Top-5 under depth-3 formula search
    top5_d3 = sorted(per_n_d3.items(), key=lambda kv: -kv[1])[:5]
    out["top5_depth3"] = [{"n": n, "score": s} for n, s in top5_d3]

    # Verdict
    s6 = per_n_d3[6]
    smax = max(others_d3.values())
    if s6 >= smax + 2 and s6 / len(TARGETS_22) >= 0.85:
        verdict = "N6_STILL_UNIQUE"
    elif s6 > smax:
        verdict = "N6_BARELY_UNIQUE"
    elif s6 == smax:
        verdict = "FORMULA_SEARCH_CRITICAL_TIED"
    else:
        verdict = "FORMULA_SEARCH_CRITICAL_BEATEN"
    out["verdict"] = verdict
    out["verdict_basis"] = {
        "n6_score_depth3": s6,
        "max_other_depth3": smax,
        "threshold_margin": 2,
        "threshold_fraction": 0.85,
        "n6_fraction": s6 / len(TARGETS_22),
    }

    return out


if __name__ == "__main__":
    results = run()
    out_path = Path(__file__).resolve().parent / "results.json"
    out_path.write_text(json.dumps(results, indent=2))
    # short summary
    print("=" * 64)
    print("Numerology critique — FORMULA-SEARCH defense (L12)")
    print("=" * 64)
    print(f"n=6 score under formula search:")
    print(f"  depth-2:  {results['n6_score_depth2']} / {results['num_targets']}")
    print(f"  depth-3:  {results['n6_score_depth3']} / {results['num_targets']}")
    print(f"max-other (n≠6):")
    print(f"  depth-2:  {results['max_other_depth2']}  (at n={results['argmax_other_depth2']})")
    print(f"  depth-3:  {results['max_other_depth3']}  (at n={results['argmax_other_depth3']})")
    print(f"margin (n6 − max_other):")
    print(f"  depth-2:  {results['margin_depth2']:+d}")
    print(f"  depth-3:  {results['margin_depth3']:+d}")
    print(f"top-5 under depth-3:")
    for row in results["top5_depth3"]:
        print(f"  n={row['n']:>3}  score={row['score']}")
    print(f"wall-clock: {results['wall_clock_sec']:.1f}s")
    print(f"VERDICT: {results['verdict']}")
    print(f"Wrote: {out_path}")
