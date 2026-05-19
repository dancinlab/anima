#!/usr/bin/env python3
"""F-QBENCH-1 variance analyzer (Mac-side, $0).

Inputs:
  - subsamples.jsonl  (1000 records: 500 classical + 500 qmirror, each with 500 indices)
  - full_hellaswag_per_example.json  (10042-doc base eval, copied from ubu1)

For each sub-sample, compute mean(acc_norm) over the 500 selected docs.
Then:
  var(classical) vs var(qmirror)
  Levene test (median-centred, robust to non-normality)
  Bartlett test (parametric, sensitive to normality)
  F-test  (var classical / var qmirror) → two-sided p

F-QBENCH-1 PASS rule: var(qmirror) < var(classical) AND p < 0.05 on at
least one of {Levene, Bartlett, F}.
"""
import argparse
import json
import math
import statistics
import sys
from pathlib import Path

REPO = Path("/Users/ghost/core/anima")
DEFAULT_DIR = REPO / "state" / "p9_qbench_resample_2026_05_03"
ALPHA = 0.05


def read_jsonl(p):
    with open(p) as f:
        return [json.loads(line) for line in f if line.strip()]


def levene_median(a: list[float], b: list[float]):
    """Levene's test, Brown–Forsythe variant (median-centred)."""
    na, nb = len(a), len(b)
    ma, mb = statistics.median(a), statistics.median(b)
    da = [abs(x - ma) for x in a]
    db = [abs(x - mb) for x in b]
    mean_da = sum(da) / na
    mean_db = sum(db) / nb
    n = na + nb
    grand_mean = (sum(da) + sum(db)) / n
    num = (na * (mean_da - grand_mean) ** 2 + nb * (mean_db - grand_mean) ** 2)
    denom = (sum((x - mean_da) ** 2 for x in da) + sum((x - mean_db) ** 2 for x in db))
    if denom == 0:
        return None, None
    W = (n - 2) * num / (1 * denom)
    # F(1, n-2) → use scipy if available, else asymptotic chi-square approx
    try:
        from scipy import stats
        p = float(1 - stats.f.cdf(W, 1, n - 2))
    except Exception:
        # F(1, df) with df>>1 → chi^2(1) approximation
        p = math.erfc(math.sqrt(W / 2))
    return float(W), p


def bartlett(a: list[float], b: list[float]):
    """Bartlett's test for equal variances (2 groups)."""
    na, nb = len(a), len(b)
    va = statistics.variance(a)
    vb = statistics.variance(b)
    if va == 0 or vb == 0:
        return None, None
    pooled = ((na - 1) * va + (nb - 1) * vb) / (na + nb - 2)
    num = (na + nb - 2) * math.log(pooled) - ((na - 1) * math.log(va) + (nb - 1) * math.log(vb))
    c = 1 + (1 / (3 * 1)) * (1 / (na - 1) + 1 / (nb - 1) - 1 / (na + nb - 2))
    chi2 = num / c
    try:
        from scipy import stats
        p = float(1 - stats.chi2.cdf(chi2, 1))
    except Exception:
        p = math.erfc(math.sqrt(chi2 / 2))
    return float(chi2), p


def f_test(a: list[float], b: list[float]):
    """Two-sided F-test for ratio of variances. Returns (F, p_two_sided)."""
    na, nb = len(a), len(b)
    va = statistics.variance(a)
    vb = statistics.variance(b)
    if vb == 0:
        return None, None
    F = va / vb
    try:
        from scipy import stats
        # two-sided
        p = 2 * min(stats.f.cdf(F, na - 1, nb - 1),
                    1 - stats.f.cdf(F, na - 1, nb - 1))
        p = float(p)
    except Exception:
        p = None
    return float(F), p


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--subsamples", default=str(DEFAULT_DIR / "subsamples.jsonl"))
    ap.add_argument("--full-eval", default=str(DEFAULT_DIR / "full_hellaswag_per_example.json"))
    ap.add_argument("--metric", default="acc_norm", choices=["acc_norm", "acc"])
    ap.add_argument("--out-dir", default=str(DEFAULT_DIR))
    args = ap.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    subs = read_jsonl(args.subsamples)
    full = json.loads(Path(args.full_eval).read_text())
    pe = full["per_example_correctness"]
    by_doc = {r["doc_id"]: r for r in pe}
    n_full = len(by_doc)
    print(f"[load] full per-example: n={n_full}; n_subsamples={len(subs)}", flush=True)

    # Compute per-sub-sample mean
    per_sub = []
    miss = 0
    for rec in subs:
        idx = rec["indices"]
        vals = []
        for i in idx:
            r = by_doc.get(i)
            if r is None or r.get(args.metric) is None:
                miss += 1
                continue
            vals.append(r[args.metric])
        if not vals:
            continue
        m = sum(vals) / len(vals)
        per_sub.append({
            "source": rec["source"],
            "n": len(vals),
            "mean": m,
            "seed": rec.get("seed") or rec.get("seed_pers"),
        })

    if miss:
        print(f"[warn] {miss} (sub-sample, doc_id) misses (likely LIMIT smoke run)", flush=True)

    classical = [r["mean"] for r in per_sub if r["source"] == "classical_prng"]
    qmirror = [r["mean"] for r in per_sub if r["source"] == "qmirror_qrng"]
    print(f"[stats] classical n={len(classical)}  qmirror n={len(qmirror)}", flush=True)

    if len(classical) < 10 or len(qmirror) < 10:
        print("[FAIL] not enough sub-samples — likely full eval was a smoke run", flush=True)
        sys.exit(2)

    var_c = statistics.variance(classical)
    var_q = statistics.variance(qmirror)
    mean_c = statistics.fmean(classical)
    mean_q = statistics.fmean(qmirror)

    W_l, p_l = levene_median(classical, qmirror)
    chi2_b, p_b = bartlett(classical, qmirror)
    F, p_F = f_test(classical, qmirror)

    var_qmirror_lower = var_q < var_c
    any_significant = any(p is not None and p < ALPHA for p in [p_l, p_b, p_F])
    verdict = "PASS" if (var_qmirror_lower and any_significant) else "FAIL"

    comparison = {
        "schema": "anima/p9_qbench_resample/variance_comparison/1",
        "metric": args.metric,
        "n_subsamples_per_source": len(classical),
        "classical_prng": {
            "mean_of_means": mean_c,
            "var_of_means": var_c,
            "std_of_means": math.sqrt(var_c),
            "min": min(classical), "max": max(classical),
        },
        "qmirror_qrng": {
            "mean_of_means": mean_q,
            "var_of_means": var_q,
            "std_of_means": math.sqrt(var_q),
            "min": min(qmirror), "max": max(qmirror),
        },
        "delta_mean_q_minus_c": mean_q - mean_c,
        "ratio_var_q_over_c": var_q / var_c if var_c else None,
        "tests": {
            "levene_median": {"W": W_l, "p": p_l},
            "bartlett": {"chi2": chi2_b, "p": p_b},
            "f_test_two_sided": {"F": F, "p": p_F,
                                  "ratio_var_classical_over_qmirror": (var_c / var_q) if var_q else None},
        },
        "alpha": ALPHA,
    }

    verdict_doc = {
        "schema": "anima/p9_qbench_resample/verdict/1",
        "test": "F-QBENCH-1",
        "rule": "var(qmirror) < var(classical) AND p<0.05 on >=1 of {Levene,Bartlett,F-test}",
        "alpha": ALPHA,
        "var_classical": var_c,
        "var_qmirror": var_q,
        "var_qmirror_lower": var_qmirror_lower,
        "min_p_value": min([p for p in [p_l, p_b, p_F] if p is not None], default=None),
        "any_significant": any_significant,
        "verdict": verdict,
        "interpretation": {
            "PASS": "qmirror QRNG sub-sampling REDUCES eval-score variance vs classical PRNG (significant)",
            "FAIL": "no evidence qmirror QRNG reduces variance vs classical PRNG at alpha=0.05",
        }[verdict],
    }

    (out_dir / "variance_comparison.json").write_text(json.dumps(comparison, indent=2))
    (out_dir / "verdict.json").write_text(json.dumps(verdict_doc, indent=2))
    with (out_dir / "per_subsample_scores.jsonl").open("w") as f:
        for r in per_sub:
            f.write(json.dumps(r) + "\n")

    print(f"[done] verdict={verdict}", flush=True)
    print(f"  var_classical={var_c:.6e}  var_qmirror={var_q:.6e}  ratio={var_q/var_c:.4f}", flush=True)
    print(f"  p(Levene)={p_l}  p(Bartlett)={p_b}  p(F)={p_F}", flush=True)


if __name__ == "__main__":
    main()
