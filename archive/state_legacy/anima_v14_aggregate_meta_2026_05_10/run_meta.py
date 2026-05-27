#!/usr/bin/env python3
"""
V14 aggregate meta-analysis — local CPU, no external deps beyond stdlib + math.

Computes:
  - per-study trained-vs-mirror paired comparisons
  - aggregate paired comparisons (n>30)
  - Fisher's combined p-value
  - Bayesian beta-binomial posterior for "V14 passes within-arch"
  - Cochran's Q + I² heterogeneity
  - Sub-stratification by substrate / cap / paradigm / arch
  - Confounding factor decomposition

raw#15: only existing data; raw#9: local-only training (none here).
: $0 local CPU.
"""
import json
import math
from pathlib import Path

ROOT = Path("/Users/ghost/core/anima/state/anima_v14_aggregate_meta_2026_05_10")
ALL = json.loads((ROOT / "all_v14_results.json").read_text())

# ---------- helpers ----------
def sign_test_p_two_sided(k, n):
    """Exact two-sided sign test for k successes in n trials, H0: p=0.5."""
    # binomial pmf accumulator
    def pmf(i, n):
        # log-binomial
        from math import lgamma
        log_c = lgamma(n+1) - lgamma(i+1) - lgamma(n-i+1)
        return math.exp(log_c) * (0.5 ** n)
    if n == 0:
        return 1.0
    one_sided_extreme = min(k, n - k)
    p = sum(pmf(i, n) for i in range(0, one_sided_extreme + 1))
    p2 = min(1.0, 2 * p)
    return p2

def fisher_combine(p_list):
    """Fisher's method: -2 sum ln(p_i) ~ chi2(2k); return chi2 stat, df, p-value."""
    p_list = [max(p, 1e-300) for p in p_list]
    chi2 = -2.0 * sum(math.log(p) for p in p_list)
    df = 2 * len(p_list)
    # survival function of chi-square via regularized upper incomplete gamma
    # SF = Q(df/2, chi2/2). use math.gamma + series — for moderate chi2/df use numerical via scipy-like impl
    # Use a stable rational approximation: We'll use math.lgamma-based incomplete gamma series.
    p_combined = chi2_sf(chi2, df)
    return chi2, df, p_combined

def chi2_sf(x, k):
    """Survival function of chi-square distribution with k df."""
    if x <= 0:
        return 1.0
    a = k / 2.0
    z = x / 2.0
    # Use the regularized upper incomplete gamma: Q(a, z) = Gamma(a,z)/Gamma(a).
    # For large z relative to a, use continued fraction (Lentz's method); else series.
    if z < a + 1.0:
        # series for P(a,z), then Q = 1 - P
        return 1.0 - _gamma_series_P(a, z)
    else:
        return _gamma_cf_Q(a, z)

def _gamma_series_P(a, z, max_iter=400, eps=1e-12):
    if z == 0:
        return 0.0
    log_pref = -z + a * math.log(z) - math.lgamma(a)
    pref = math.exp(log_pref)
    term = 1.0 / a
    s = term
    for n in range(1, max_iter):
        term *= z / (a + n)
        s += term
        if abs(term) < abs(s) * eps:
            break
    return pref * s

def _gamma_cf_Q(a, z, max_iter=400, eps=1e-12):
    log_pref = -z + a * math.log(z) - math.lgamma(a)
    pref = math.exp(log_pref)
    # Lentz continued fraction
    b = z + 1.0 - a
    c = 1e30
    d = 1.0 / b
    h = d
    for i in range(1, max_iter):
        an = -i * (i - a)
        b += 2.0
        d = an * d + b
        if abs(d) < 1e-30:
            d = 1e-30
        c = b + an / c
        if abs(c) < 1e-30:
            c = 1e-30
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < eps:
            break
    return pref * h

def beta_quantile_approx(alpha, beta_p, q):
    """Approximate quantile of Beta(alpha,beta) via bisection on regularized incomplete beta."""
    # Use bisection
    lo, hi = 0.0, 1.0
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        # compute regularized incomplete beta I_mid(alpha,beta)
        if reg_incbeta(mid, alpha, beta_p) < q:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)

def reg_incbeta(x, a, b, max_iter=400, eps=1e-12):
    if x <= 0: return 0.0
    if x >= 1: return 1.0
    log_b = math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b) + a * math.log(x) + b * math.log(1.0 - x)
    bt = math.exp(log_b)
    if x < (a + 1.0) / (a + b + 2.0):
        return bt * _betacf(x, a, b) / a
    else:
        return 1.0 - bt * _betacf(1.0 - x, b, a) / b

def _betacf(x, a, b, max_iter=400, eps=1e-12):
    qab = a + b
    qap = a + 1.0
    qam = a - 1.0
    c = 1.0
    d = 1.0 - qab * x / qap
    if abs(d) < 1e-30: d = 1e-30
    d = 1.0 / d
    h = d
    for m in range(1, max_iter):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        if abs(d) < 1e-30: d = 1e-30
        c = 1.0 + aa / c
        if abs(c) < 1e-30: c = 1e-30
        d = 1.0 / d
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        if abs(d) < 1e-30: d = 1e-30
        c = 1.0 + aa / c
        if abs(c) < 1e-30: c = 1e-30
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < eps:
            break
    return h

# ---------- main analysis ----------
studies = ALL["studies"]

# Phase 0: build per-study paired-comparison records (only studies with quantitative trained_phi vs random_phi)
quant_studies = [s for s in studies if "trained_phi" in s and isinstance(s.get("random_phi"), list)]

# Aggregate paired comparison: for each study, count "trained beats mirror_i" trials.
# Each study contributes n_random_total Bernoulli trials.
total_trials = 0
total_beats = 0
study_recs = []
for s in quant_studies:
    n = s["n_random_total"]
    k = s["n_random_beats"]
    p2 = sign_test_p_two_sided(k, n)
    total_trials += n
    total_beats += k
    study_recs.append({
        "study_id": s["study_id"],
        "substrate": s["substrate"],
        "arch": s["arch"],
        "paradigm": s["paradigm"],
        "max_cells": s["max_cells"],
        "cap_binding": s["cap_binding"],
        "metric": s["metric"],
        "k": k,
        "n": n,
        "frac": k / n if n else 0.0,
        "p_two_sided": p2,
        "verdict": s["verdict"],
    })

aggregate_p_two_sided = sign_test_p_two_sided(total_beats, total_trials)

# Sub-stratification
def stratify(key_fn):
    out = {}
    for r in study_recs:
        k = key_fn(r)
        d = out.setdefault(k, {"k": 0, "n": 0, "studies": []})
        d["k"] += r["k"]
        d["n"] += r["n"]
        d["studies"].append(r["study_id"])
    for k, d in out.items():
        d["frac"] = d["k"] / d["n"] if d["n"] else 0.0
        d["p_two_sided"] = sign_test_p_two_sided(d["k"], d["n"])
    return out

by_substrate = stratify(lambda r: r["substrate"])
by_arch = stratify(lambda r: r["arch"])
by_paradigm = stratify(lambda r: r["paradigm"])
by_cap = stratify(lambda r: f"max_cells={r['max_cells']}")
by_cap_binding = stratify(lambda r: f"cap_binding={r['cap_binding']}")

# Fisher combined p-value (use one-sided p where applicable; here we use two-sided sign test p, conservative)
# Note: studies with k = n/2 will have p ~ 1, which makes Fisher conservative.
# For positive evidence we want one-sided in the direction of trained > random.
def sign_test_p_one_sided_upper(k, n):
    if n == 0: return 1.0
    from math import lgamma
    s = 0.0
    for i in range(k, n+1):
        log_c = lgamma(n+1) - lgamma(i+1) - lgamma(n-i+1)
        s += math.exp(log_c) * (0.5 ** n)
    return s

# One-sided p for "trained beats mirror more often than chance" per study
study_one_sided_p = []
for r in study_recs:
    p1 = sign_test_p_one_sided_upper(r["k"], r["n"])
    r["p_one_sided"] = p1
    study_one_sided_p.append(p1)

fisher_chi2_all, fisher_df_all, fisher_p_all = fisher_combine(study_one_sided_p)

# Within-arch Fisher combination
fisher_within = {}
for arch_name in set(r["arch"] for r in study_recs):
    pl = [r["p_one_sided"] for r in study_recs if r["arch"] == arch_name]
    chi2, df, p = fisher_combine(pl)
    fisher_within[arch_name] = {"chi2": chi2, "df": df, "p_combined": p, "n_studies": len(pl)}

# Bayesian beta-binomial posterior on the aggregate "P(trained beats random)"
# Prior: Beta(1,1) uniform.
alpha_post = 1 + total_beats
beta_post = 1 + (total_trials - total_beats)
post_mean = alpha_post / (alpha_post + beta_post)
post_var = alpha_post * beta_post / ((alpha_post + beta_post) ** 2 * (alpha_post + beta_post + 1))
post_lo = beta_quantile_approx(alpha_post, beta_post, 0.025)
post_hi = beta_quantile_approx(alpha_post, beta_post, 0.975)
post_p_gt_half = 1.0 - reg_incbeta(0.5, alpha_post, beta_post)

# Within-arch posterior
within_arch_post = {}
for arch_name in set(r["arch"] for r in study_recs):
    k_a = sum(r["k"] for r in study_recs if r["arch"] == arch_name)
    n_a = sum(r["n"] for r in study_recs if r["arch"] == arch_name)
    a_p = 1 + k_a
    b_p = 1 + (n_a - k_a)
    within_arch_post[arch_name] = {
        "k": k_a,
        "n": n_a,
        "frac": k_a / n_a if n_a else 0.0,
        "post_mean": a_p / (a_p + b_p),
        "ci95": [beta_quantile_approx(a_p, b_p, 0.025), beta_quantile_approx(a_p, b_p, 0.975)],
        "p_gt_half": 1.0 - reg_incbeta(0.5, a_p, b_p),
    }

# Cochran's Q heterogeneity test on per-study pass-rates
# Treat each study as binomial with effect = log-odds; Q = sum_i w_i (theta_i - theta_bar)^2
# Use log-odds-ratio of trained beats vs 0.5. With 0/n or n/n use Haldane correction.
def haldane_logit(k, n):
    p_hat = (k + 0.5) / (n + 1.0)
    return math.log(p_hat / (1.0 - p_hat))

def haldane_var(k, n):
    p_hat = (k + 0.5) / (n + 1.0)
    return 1.0 / ((n + 1.0) * p_hat * (1.0 - p_hat))

theta = []
weights = []
for r in study_recs:
    theta.append(haldane_logit(r["k"], r["n"]))
    weights.append(1.0 / haldane_var(r["k"], r["n"]))

w_sum = sum(weights)
theta_bar = sum(w * t for w, t in zip(weights, theta)) / w_sum
Q = sum(w * (t - theta_bar) ** 2 for w, t in zip(weights, theta))
df_Q = len(theta) - 1
Q_p = chi2_sf(Q, df_Q) if df_Q > 0 else 1.0
I2 = max(0.0, (Q - df_Q) / Q) * 100.0 if Q > 0 else 0.0

# Within-arch heterogeneity: engine_ag and v2_d384
def hetero_subset(subset_recs):
    if len(subset_recs) < 2:
        return None
    th = [haldane_logit(r["k"], r["n"]) for r in subset_recs]
    wt = [1.0 / haldane_var(r["k"], r["n"]) for r in subset_recs]
    ws = sum(wt)
    tb = sum(w * t for w, t in zip(wt, th)) / ws
    Q_s = sum(w * (t - tb) ** 2 for w, t in zip(wt, th))
    df_s = len(th) - 1
    p = chi2_sf(Q_s, df_s) if df_s > 0 else 1.0
    I = max(0.0, (Q_s - df_s) / Q_s) * 100.0 if Q_s > 0 else 0.0
    return {"Q": Q_s, "df": df_s, "p": p, "I2_pct": I}

hetero_engine_ag = hetero_subset([r for r in study_recs if r["arch"] == "engine_ag"])
hetero_v2 = hetero_subset([r for r in study_recs if r["arch"] == "v2_d384"])

# Confounding decomposition: paradigm effect within engine_ag
# naive_cotrain (S1, S2, S3, S8, S12) vs naive_pretrain_no_cotrain (S4, S11) vs slab-swapped (S13-S15)
def subset_summary(recs, label):
    if not recs: return None
    k = sum(r["k"] for r in recs)
    n = sum(r["n"] for r in recs)
    return {"label": label, "k": k, "n": n, "frac": k/n if n else 0.0, "p_two_sided": sign_test_p_two_sided(k, n), "n_studies": len(recs)}

cotrain_engine = [r for r in study_recs if r["arch"] == "engine_ag" and "naive_cotrain" in r["paradigm"] and "swap" not in r["paradigm"]]
pretrain_no_cotrain = [r for r in study_recs if r["arch"] == "engine_ag" and "no_cotrain" in r["paradigm"]]
slab_swap = [r for r in study_recs if r["arch"] == "engine_ag" and "swap" in r["paradigm"]]

paradigm_decomp = {
    "engine_ag_cotrain": subset_summary(cotrain_engine, "engine_ag_cotrain"),
    "engine_ag_no_cotrain": subset_summary(pretrain_no_cotrain, "engine_ag_no_cotrain"),
    "engine_ag_slab_swapped": subset_summary(slab_swap, "engine_ag_slab_swapped"),
}

# v2 paradigm decomp
v2_aware = [r for r in study_recs if r["arch"] == "v2_d384" and "aware" in r["paradigm"]]
v2_naive_ft = [r for r in study_recs if r["arch"] == "v2_d384" and "naive_ft" in r["paradigm"]]
paradigm_decomp_v2 = {
    "v2_aware": subset_summary(v2_aware, "v2_aware"),
    "v2_naive_ft_no_mitosis": subset_summary(v2_naive_ft, "v2_naive_ft_no_mitosis"),
}

# Cap effect within engine_ag cotrain
cap_decomp_engine_cotrain = {}
for cap in [32, 128, 256]:
    recs = [r for r in cotrain_engine if r["max_cells"] == cap]
    if recs:
        cap_decomp_engine_cotrain[f"cap_{cap}"] = subset_summary(recs, f"engine_ag_cotrain_cap_{cap}")

cap_decomp_v2 = {}
for cap in [128, 256]:
    recs = [r for r in study_recs if r["arch"] == "v2_d384" and r["max_cells"] == cap]
    if recs:
        cap_decomp_v2[f"cap_{cap}"] = subset_summary(recs, f"v2_cap_{cap}")

# Output
out = {
    "ts": "2026-05-10",
    "n_studies_quant": len(study_recs),
    "aggregate": {
        "total_trials": total_trials,
        "total_beats": total_beats,
        "frac": total_beats / total_trials if total_trials else 0.0,
        "sign_test_p_two_sided": aggregate_p_two_sided,
        "fisher_chi2_one_sided": fisher_chi2_all,
        "fisher_df": fisher_df_all,
        "fisher_p_one_sided": fisher_p_all,
    },
    "bayesian_posterior_aggregate": {
        "alpha": alpha_post,
        "beta": beta_post,
        "post_mean": post_mean,
        "post_var": post_var,
        "ci95_pct": [post_lo, post_hi],
        "p_gt_half": post_p_gt_half,
    },
    "heterogeneity_all": {
        "Q": Q,
        "df": df_Q,
        "p": Q_p,
        "I2_pct": I2,
    },
    "heterogeneity_engine_ag": hetero_engine_ag,
    "heterogeneity_v2_d384": hetero_v2,
    "by_substrate": by_substrate,
    "by_arch": by_arch,
    "by_paradigm": by_paradigm,
    "by_cap": by_cap,
    "by_cap_binding": by_cap_binding,
    "fisher_within_arch": fisher_within,
    "within_arch_posterior": within_arch_post,
    "paradigm_decomposition_engine_ag": paradigm_decomp,
    "paradigm_decomposition_v2": paradigm_decomp_v2,
    "cap_decomposition_engine_ag_cotrain": cap_decomp_engine_cotrain,
    "cap_decomposition_v2": cap_decomp_v2,
    "per_study_records": study_recs,
}

(ROOT / "meta_analysis.json").write_text(json.dumps(out, indent=2))
print(json.dumps({k: v for k, v in out.items() if k not in ("per_study_records", "by_substrate", "by_paradigm", "by_cap", "by_cap_binding")}, indent=2))
