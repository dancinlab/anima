"""
Numerology critique — FORMULA-SEARCH depth-4 + Perfect-Number Control (L12 quantification).

Cycle:   2026-05-11 (cycle 5 #2)
Lane:    state/numerology_critique_n6_2026_05_11/formula_search/depth_4_perfect_control/
Parent:  ../simulate.py (depth-3 baseline; FORMULA_SEARCH_CRITICAL_BEATEN)
Spec:    ./spec.md

Variations:
  V1: depth=4, full vocab, tol=0.01, n ∈ [2,30]
  V2: depth=4, restricted-A (7 prims), tol=0.01, n ∈ [2,30]
  V3: depth=4, restricted-B (5 prims), tol=0.01, n ∈ [2,30]
  V4: depth=4, full vocab, tol=0.005, n ∈ [2,30]
  V5: depth=4, full vocab, tol=0.001, n ∈ [2,30]
  V6: depth=4, full vocab, tol=0.01, n ∈ {6, 28, 496, 8128}  (perfect-number control)
  V7: depth=4, restricted-A, tol=0.005, n ∈ {6, 28, 496, 8128}  (perfect tightened)

Each variation capped at 5 min wall-clock. On overrun we report partial coverage.

Seed: 0xF0EAFEA1 (same as parent for reproducibility)
"""

import json
import math
import random
import time
from pathlib import Path

import numpy as np
from sympy import divisor_count, divisor_sigma, factorint, totient
from sympy.ntheory import mobius


# ---------------------------------------------------------------------------
# Primitives & vocabulary subsets
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


def primitives_full(n: int) -> dict[str, float]:
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


VOCAB_SUBSETS = {
    "full":         ["1", "n", "mu", "phi", "tau", "sigma", "sopfr", "J2", "e", "pi", "ln2"],
    "restricted-A": ["1", "n", "mu", "phi", "tau", "sigma", "sopfr"],
    "restricted-B": ["n", "mu", "phi", "tau", "sigma"],
}


def primitives(n: int, subset: str) -> dict[str, float]:
    full = primitives_full(n)
    keys = VOCAB_SUBSETS[subset]
    return {k: full[k] for k in keys}


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
# Safe ops
# ---------------------------------------------------------------------------

MAX_ABS = 1e8
MIN_ABS = 1e-8
EXP_LIMIT = 5
L4_CAP = 200_000  # hard cap on |L4|


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
    if abs(b) >= EXP_LIMIT:
        return None
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


BIN_OPS = (_safe_add, _safe_sub, _safe_mul, _safe_div, _safe_pow)
UN_OPS = (_safe_log, _safe_sqrt, _safe_neg)


def hit(predicted, target, tol):
    if predicted is None:
        return False
    if math.isnan(predicted) or math.isinf(predicted):
        return False
    if target == 0:
        return abs(predicted) < tol
    return abs(predicted - target) / abs(target) < tol


# ---------------------------------------------------------------------------
# Layer generation
# ---------------------------------------------------------------------------

def generate_layer1(n: int, vocab_subset: str):
    P = primitives(n, vocab_subset)
    return set(P.values())


def generate_layer2(layer1):
    out = set()
    L1 = list(layer1)
    for a in L1:
        for fn in UN_OPS:
            v = fn(a)
            if v is not None and -MAX_ABS < v < MAX_ABS:
                out.add(v)
    for a in L1:
        for b in L1:
            for fn in BIN_OPS:
                v = fn(a, b)
                if v is not None:
                    out.add(v)
    return out


def generate_layer3(layer1, layer2):
    out = set()
    L1 = list(layer1)
    L2 = list(layer2)
    for a in L2:
        for fn in UN_OPS:
            v = fn(a)
            if v is not None:
                out.add(v)
    for a in L2:
        for b in L1:
            for fn in BIN_OPS:
                v = fn(a, b)
                if v is not None:
                    out.add(v)
    for a in L1:
        for b in L2:
            for fn in BIN_OPS:
                v = fn(a, b)
                if v is not None:
                    out.add(v)
    return out


def generate_layer4(layer1, layer2, layer3, rng: random.Random):
    """L4 = unary(L3) ∪ (L3 BIN L1) ∪ (L1 BIN L3) ∪ (L2 BIN L2).

    Hard cap |L4| ≤ L4_CAP by reservoir sampling of L3 if needed.
    """
    out = set()
    L1 = list(layer1)
    L2 = list(layer2)
    L3 = list(layer3)

    # If L3 is huge, sub-sample to keep wall-clock bounded
    if len(L3) > 3000:
        L3 = rng.sample(L3, 3000)
    L2_capped = L2 if len(L2) <= 400 else rng.sample(L2, 400)

    # unary(L3)
    for a in L3:
        for fn in UN_OPS:
            v = fn(a)
            if v is not None:
                out.add(v)
                if len(out) >= L4_CAP:
                    return out

    # L3 BIN L1
    for a in L3:
        for b in L1:
            for fn in BIN_OPS:
                v = fn(a, b)
                if v is not None:
                    out.add(v)
                    if len(out) >= L4_CAP:
                        return out
    # L1 BIN L3
    for a in L1:
        for b in L3:
            for fn in BIN_OPS:
                v = fn(a, b)
                if v is not None:
                    out.add(v)
                    if len(out) >= L4_CAP:
                        return out
    # L2 BIN L2 (capped)
    for a in L2_capped:
        for b in L2_capped:
            for fn in BIN_OPS:
                v = fn(a, b)
                if v is not None:
                    out.add(v)
                    if len(out) >= L4_CAP:
                        return out
    return out


# ---------------------------------------------------------------------------
# Scoring (with early-hit short-circuit)
# ---------------------------------------------------------------------------

def score_for_n(n: int, vocab_subset: str, max_depth: int, tol: float, rng: random.Random):
    """Return (matches, detail, l_sizes)."""
    L1 = generate_layer1(n, vocab_subset)
    L2 = generate_layer2(L1) if max_depth >= 2 else set()
    L3 = generate_layer3(L1, L2) if max_depth >= 3 else set()
    L4 = generate_layer4(L1, L2, L3, rng) if max_depth >= 4 else set()
    l_sizes = {"L1": len(L1), "L2": len(L2), "L3": len(L3), "L4": len(L4)}

    matches = 0
    detail = []
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
        if found_depth is None and max_depth >= 4:
            for v in L4:
                if hit(v, target, tol):
                    found_depth, found_value = 4, v
                    break
        if found_depth is not None:
            matches += 1
        detail.append({
            "name": name,
            "target": target,
            "found_depth": found_depth,
            "found_value": found_value,
        })
    return matches, detail, l_sizes


# ---------------------------------------------------------------------------
# Variations
# ---------------------------------------------------------------------------

PERFECT_NUMS = [6, 28, 496, 8128]

VARIATIONS = [
    {"id": "V1", "depth": 4, "vocab": "full",         "tol": 0.01,  "n_set": list(range(2, 31))},
    {"id": "V2", "depth": 4, "vocab": "restricted-A", "tol": 0.01,  "n_set": list(range(2, 31))},
    {"id": "V3", "depth": 4, "vocab": "restricted-B", "tol": 0.01,  "n_set": list(range(2, 31))},
    {"id": "V4", "depth": 4, "vocab": "full",         "tol": 0.005, "n_set": list(range(2, 31))},
    {"id": "V5", "depth": 4, "vocab": "full",         "tol": 0.001, "n_set": list(range(2, 31))},
    {"id": "V6", "depth": 4, "vocab": "full",         "tol": 0.01,  "n_set": PERFECT_NUMS},
    {"id": "V7", "depth": 4, "vocab": "restricted-A", "tol": 0.005, "n_set": PERFECT_NUMS},
]

TIME_CAP_PER_VARIATION = 300.0  # 5 min per spec


def run_variation(var: dict, seed: int) -> dict:
    """Run one variation; respects per-variation wall-clock cap."""
    rng = random.Random(seed)
    np.random.seed(seed & 0xFFFFFFFF)

    t0 = time.time()
    per_n_score = {}
    per_n_detail_n6 = None
    completed = []
    aborted = False
    for n in var["n_set"]:
        elapsed = time.time() - t0
        if elapsed >= TIME_CAP_PER_VARIATION:
            aborted = True
            break
        try:
            matches, detail, _l = score_for_n(
                n, var["vocab"], var["depth"], var["tol"], rng
            )
        except MemoryError:
            aborted = True
            break
        per_n_score[n] = matches
        if n == 6:
            per_n_detail_n6 = detail
        completed.append(n)

    wall = round(time.time() - t0, 2)
    coverage_pct = round(100 * len(completed) / len(var["n_set"]), 1)

    result = {
        "id":             var["id"],
        "depth":          var["depth"],
        "vocab":          var["vocab"],
        "vocab_size":     len(VOCAB_SUBSETS[var["vocab"]]),
        "tol":            var["tol"],
        "n_set":          var["n_set"],
        "completed_n":    completed,
        "coverage_pct":   coverage_pct,
        "aborted_at_cap": aborted,
        "wall_sec":       wall,
        "per_n_score":    {str(n): per_n_score[n] for n in completed},
        "n6_detail":      per_n_detail_n6,
    }

    # Headline summary numbers
    n6_score = per_n_score.get(6)
    perfect_scores = {n: per_n_score.get(n) for n in PERFECT_NUMS if n in per_n_score}
    others = {n: s for n, s in per_n_score.items() if n != 6}

    result["n6_score"] = n6_score
    result["perfect_scores"] = {str(n): s for n, s in perfect_scores.items()}

    if others:
        max_other = max(others.values())
        argmax_other = max(others, key=others.get)
        result["max_other"]    = max_other
        result["argmax_other"] = argmax_other
        result["mean_other"]   = float(np.mean(list(others.values())))
        result["std_other"]    = float(np.std(list(others.values())))
        result["margin"]       = (n6_score - max_other) if n6_score is not None else None
    else:
        result["max_other"]    = None
        result["argmax_other"] = None
        result["margin"]       = None

    # Verdict per variation
    result["verdict"] = compute_verdict(result, var)
    return result


def compute_verdict(r: dict, var: dict) -> str:
    n6 = r["n6_score"]
    if n6 is None:
        return "INCOMPLETE_NO_N6"

    is_perfect_control = (set(var["n_set"]) == set(PERFECT_NUMS))

    if is_perfect_control:
        # PERFECT_NUMBER_CLASS check
        ps = list(r["perfect_scores"].values())
        if len(ps) == 4:
            min_ps = min(ps)
            max_ps = max(ps)
            mean_ps = sum(ps) / 4
            if (max_ps - min_ps) <= 1 and mean_ps / len(TARGETS_22) >= 0.85:
                return "PERFECT_NUMBER_CLASS"
            # Differentiated?
            if n6 == max_ps and (max_ps - max(p for p in ps if p != n6 or len([x for x in ps if x == n6]) > 1)) >= 0:
                # n=6 is the top among perfect numbers
                return "PERFECT_N6_TOP" if n6 > max(p for n_, p in r["perfect_scores"].items() if int(n_) != 6) else "PERFECT_TIED"
            return "PERFECT_MIXED"
        return "PERFECT_PARTIAL"

    # Standard variations
    max_other = r["max_other"] or 0
    margin = (n6 - max_other) if max_other is not None else None
    if margin is not None and margin >= 2 and n6 / len(TARGETS_22) >= 0.85:
        return "N6_STILL_UNIQUE_d4"
    if margin is not None and margin > 0:
        return "N6_BARELY_UNIQUE_d4"
    if margin == 0:
        return "FORMULA_SEARCH_CRITICAL_TIED_d4"
    return "FORMULA_SEARCH_CRITICAL_BEATEN_d4"


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------

def run() -> dict:
    SEED = 0xF0EAFEA1
    t_global = time.time()

    out = {
        "cycle":          "2026-05-11",
        "lane":           "state/numerology_critique_n6_2026_05_11/formula_search/depth_4_perfect_control",
        "parent_lane":    "state/numerology_critique_n6_2026_05_11/formula_search",
        "seed_hex":       hex(SEED),
        "num_targets":    len(TARGETS_22),
        "time_cap_per_variation_sec": TIME_CAP_PER_VARIATION,
        "L4_cap":         L4_CAP,
        "vocab_subsets":  {k: v for k, v in VOCAB_SUBSETS.items()},
        "variations":     [],
    }

    for var in VARIATIONS:
        print(f"--- {var['id']}: depth={var['depth']} vocab={var['vocab']} tol={var['tol']} "
              f"|n|={len(var['n_set'])} ---", flush=True)
        r = run_variation(var, SEED)
        print(f"  n6={r['n6_score']} max_other={r['max_other']} "
              f"margin={r['margin']} verdict={r['verdict']} "
              f"wall={r['wall_sec']}s coverage={r['coverage_pct']}%", flush=True)
        out["variations"].append(r)

    out["global_wall_sec"] = round(time.time() - t_global, 2)

    # Headline matrix
    headline = []
    for r in out["variations"]:
        ps = r.get("perfect_scores", {})
        # max(other n) for full-range; for perfect control, use max excluding 6
        if set(map(int, ps.keys())) == set(PERFECT_NUMS):
            non_n6 = {int(k): v for k, v in ps.items() if int(k) != 6}
            max_other_for_table = max(non_n6.values()) if non_n6 else None
            best_alt = max(non_n6, key=non_n6.get) if non_n6 else None
        else:
            max_other_for_table = r.get("max_other")
            best_alt = r.get("argmax_other")
        headline.append({
            "variation":   r["id"],
            "n6":          r["n6_score"],
            "n28":         ps.get("28"),
            "n496":        ps.get("496"),
            "n8128":       ps.get("8128"),
            "max_other_n": max_other_for_table,
            "best_alt_n":  best_alt,
            "verdict":     r["verdict"],
        })
    out["headline_table"] = headline

    return out


def render_verdict_markdown(results: dict) -> str:
    lines = []
    lines.append("# Numerology Critique — FORMULA-SEARCH depth-4 + Perfect-Number Control")
    lines.append("")
    lines.append("**Cycle**: 2026-05-11 (cycle 5 #2)")
    lines.append(f"**Seed**: `{results['seed_hex']}`")
    lines.append(f"**Wall-clock (total)**: {results['global_wall_sec']:.1f} s")
    lines.append(f"**Time cap per variation**: {results['time_cap_per_variation_sec']:.0f} s")
    lines.append("")
    lines.append("Parent: `../verdict.md` (depth-3, `FORMULA_SEARCH_CRITICAL_BEATEN`).")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 1. Headline table")
    lines.append("")
    lines.append("| Variation | n=6 | n=28 | n=496 | n=8128 | max(other n) | best_alt_n | verdict |")
    lines.append("|---|---|---|---|---|---|---|---|")
    for row in results["headline_table"]:
        def cell(x):
            return "—" if x is None else str(x)
        lines.append(
            f"| {row['variation']} | {cell(row['n6'])} | {cell(row['n28'])} | "
            f"{cell(row['n496'])} | {cell(row['n8128'])} | {cell(row['max_other_n'])} | "
            f"{cell(row['best_alt_n'])} | `{row['verdict']}` |"
        )
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 2. Per-variation detail")
    lines.append("")
    for r in results["variations"]:
        lines.append(f"### {r['id']}  (depth={r['depth']}, vocab={r['vocab']} ({r['vocab_size']} prims), tol={r['tol']})")
        lines.append("")
        lines.append(f"- n-set: {r['n_set']}")
        lines.append(f"- wall: {r['wall_sec']} s — coverage {r['coverage_pct']}%"
                     + (" (aborted at 5-min cap)" if r['aborted_at_cap'] else ""))
        lines.append(f"- score(n=6) = {r['n6_score']} / 22")
        if r.get("max_other") is not None:
            lines.append(f"- max(other) = {r['max_other']} at n={r['argmax_other']}")
            lines.append(f"- mean(other) = {r['mean_other']:.2f}  std={r['std_other']:.2f}")
        if r["perfect_scores"]:
            lines.append(f"- perfect_scores = {r['perfect_scores']}")
        lines.append(f"- **verdict**: `{r['verdict']}`")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## 3. L12 BINDING quantification update")
    lines.append("")

    # Logic: find if any variation breaks back to N6_STILL_UNIQUE_d4 or PERFECT_NUMBER_CLASS.
    verdicts = [r["verdict"] for r in results["variations"]]
    n6_unique_cells = [r for r in results["variations"] if r["verdict"] == "N6_STILL_UNIQUE_d4"]
    perfect_class_cells = [r for r in results["variations"] if r["verdict"] == "PERFECT_NUMBER_CLASS"]
    beaten_cells = [r for r in results["variations"] if r["verdict"].startswith("FORMULA_SEARCH_CRITICAL_BEATEN")]

    if n6_unique_cells:
        lines.append("**L12 BINDING (revised)**: binding at depth-3 baseline but **lifted** under the following depth-4 cells:")
        for r in n6_unique_cells:
            lines.append(f"- {r['id']}: depth={r['depth']}, vocab={r['vocab']}, tol={r['tol']}, n_set={r['n_set']}")
        lines.append("")
        lines.append("Interpretation: tightening tolerance / restricting vocabulary at depth-4 can re-isolate n=6.")
    elif perfect_class_cells:
        lines.append("**L12 BINDING (refined)**: binding for 'n=6 individual uniqueness' but lifted for 'perfect-number-class uniqueness'.")
        for r in perfect_class_cells:
            lines.append(f"- {r['id']}: scores ≈ {r['perfect_scores']}")
        lines.append("")
        lines.append("Interpretation: σ(n)=2n class admits joint formula-search saturation; n=6 is one of four equally-special members.")
    else:
        lines.append("**L12 BINDING (unchanged)**: binding across all 7 depth-4 (vocab × tol × n-set) cells tested.")
        lines.append("")
        lines.append("Interpretation: depth-4 only amplifies the saturation observed at depth-3. Restricted vocab and "
                     "tightened tolerance do not re-isolate n=6. The published-formula uniqueness remains a narrow-formula "
                     "claim, not a vocabulary-level claim, and is not rescued by the perfect-number control either.")

    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 4. Honest findings")
    lines.append("")
    # Auto-derive findings from the variation matrix
    if all(v.startswith("FORMULA_SEARCH_CRITICAL_BEATEN") for v in verdicts):
        lines.append("1. depth-4 produces no qualitative shift from depth-3 — saturation is already a depth-3 phenomenon.")
        lines.append("2. restricting vocabulary (V2, V3) does not rescue n=6, indicating the saturation is not driven by transcendentals.")
        lines.append("3. tightening tolerance (V4, V5) does not rescue n=6 either, indicating the published Ψ-constants live too close to the dense arithmetic value-set for tolerance-based discrimination.")
        lines.append("4. perfect-number control (V6, V7) shows n=6 is not uniquely top within {6, 28, 496, 8128} — perfect-numerology, not n=6-specific.")
    else:
        lines.append("Findings vary across cells — see per-variation detail above and the headline table.")

    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 5. Cross-link decision")
    lines.append("")
    lines.append("- H_067 (perfect_number_architecture): update if PERFECT_NUMBER_CLASS observed OR if V6/V7 shows n=6 distinctly drops below {28,496,8128}.")
    lines.append("- H_153 (dimension_hierarchy_n6) C5/L7: update if any depth-4 cell returns `N6_STILL_UNIQUE_d4`.")
    lines.append("- H_124 (cross-link only if both above triggered).")
    lines.append("")
    lines.append("Triggered cross-links and rationale recorded in parent-process commit message.")
    return "\n".join(lines)


if __name__ == "__main__":
    res = run()
    out_dir = Path(__file__).resolve().parent
    (out_dir / "results.json").write_text(json.dumps(res, indent=2))
    (out_dir / "verdict.md").write_text(render_verdict_markdown(res))
    print()
    print("=" * 64)
    print("DEPTH-4 + PERFECT-NUMBER CONTROL — summary")
    print("=" * 64)
    print(f"global wall-clock: {res['global_wall_sec']:.1f} s")
    for row in res["headline_table"]:
        print(f"  {row['variation']}: n6={row['n6']} n28={row['n28']} "
              f"n496={row['n496']} n8128={row['n8128']} "
              f"max_other={row['max_other_n']} best_alt={row['best_alt_n']} -> {row['verdict']}")
    print(f"Wrote: {out_dir/'results.json'}")
    print(f"Wrote: {out_dir/'verdict.md'}")
