#!/usr/bin/env python3
"""qentropy_benchmark.py — per-path QUANTUM-vs-DETERMINISTIC A/B benchmark harness.

H_924 M6. One-command, Mac-runnable ($0, no device, no torch) A/B runner over every
SW-reachable anima entropy seed/sample path. For each path it runs N trials in BOTH
entropy modes and records a ledger row.

────────────────────────────────────────────────────────────────────────────────
WHAT THIS IS — and what it deliberately is NOT
────────────────────────────────────────────────────────────────────────────────
This is a STATISTICAL-PARITY SANITY check + a PROVENANCE DIFFERENTIATOR surface.
It is *not* a superiority test. The honest non-claim (#123-A, NIST SP 800-22 7/7)
is that ANU vacuum-fluctuation entropy is statistically EQUAL to a chacha20/numpy
PRNG (JSD 0.000433, 23x under threshold). So we EXPECT the two modes to come out
statistically indistinguishable at the application level — and that expectation IS
the test: if the application-level distributions diverged wildly, *that* would be a
red flag (a coupling bug), not a win.

The difference that actually matters — and the reason both modes exist — is
PROVENANCE / auditability:

    quantum       -> tier=anu_committed, sha256 of the real ANU vacuum-fluctuation
                     buffer (a physical, auditable origin you can pin to a draw).
    deterministic -> tier=numpy_prng(seed=187), reproducible, no physical origin.

So the ledger surfaces, per path: (a) each mode's metric mean/std over N trials,
(b) a PROPER two-sample statistical test confirming parity, and (c) each mode's
provenance (mode / tier / sha256). The headline is NOT a delta in the metric — it is
the provenance column.

────────────────────────────────────────────────────────────────────────────────
THE STATISTICAL TEST (C7 upgrade)
────────────────────────────────────────────────────────────────────────────────
The original ledger used a COARSE closeness statistic |Δmean| / pooled_std. C7
upgrades this to a PROPER two-sample test so the parity claim is rigorous:

  * continuous metric (weight_l1, token_hist_entropy_bits)
        -> two-sample Kolmogorov–Smirnov (KS): compares the full empirical CDFs of
           the two modes' per-trial samples, not just their means. Reports the KS D
           statistic + a two-sided p-value.
  * sampler token distribution (decoder_qsample pooled histogram)
        -> chi-square contingency test (chi2_contingency) on the 2×K table of
           per-mode token counts. Reports chi2, dof, and a p-value.

How to read the p-value (this is the WHOLE point — read carefully):
  H0 (null) = "both modes' samples come from the SAME distribution."
  p > 0.05  = FAIL TO REJECT H0 = statistical PARITY = the EXPECTED, DESIRED result.
              This reproduces #123-A (ANU quantum ≡ PRNG) with a real test — it is
              NOT a null finding to bury; it is the claim confirmed rigorously.
  p < 0.05  = REJECT H0 = a distributional difference. On these modes that would be
              a surprise — likely a small-sample artifact or a real implementation
              asymmetry worth noting. The harness reports it HONESTLY, un-massaged.

  `parity_at_alpha_0.05` = (p_value > 0.05) = the parity verdict per path.

scipy is OPTIONAL. If `scipy.stats` imports, it is used (the fast-path). If scipy is
ABSENT, a self-contained pure-python two-sample KS (D statistic + asymptotic
Kolmogorov p-value via the Q_ks series) and a pure-python chi-square (with a
Wilson–Hilferty / series gamma-tail) are used instead — ZERO hard deps, same output
schema. Which engine ran is recorded per test as `engine: scipy | pure-python`.

────────────────────────────────────────────────────────────────────────────────
WHY A SUBPROCESS PER ARM
────────────────────────────────────────────────────────────────────────────────
qentropy.py reads ANIMA_ENTROPY_MODE *at import time* (module-global `_MODE`). Once
imported in this process, flipping os.environ would NOT change its behavior. So each
(path, mode) arm runs in a FRESH `python3 -c ...` subprocess with ANIMA_ENTROPY_MODE
set in its environment. That guarantees the mode is honestly fresh per arm and that
this harness's own import of qentropy can never contaminate an arm.

────────────────────────────────────────────────────────────────────────────────
PATHS
────────────────────────────────────────────────────────────────────────────────
SW-runnable now (benchmarked here):
  * plasticity_sw_approx  — SW learning. Metric = weight_l1 (a scalar summarizing
                            the learned weight matrix) per trial, over N trials.
  * decoder_qsample       — DECODER sampling. Metric = Shannon entropy (bits) of the
                            sampled-token histogram per trial, over N trials; we also
                            aggregate the pooled token histogram per mode.

device/torch-pending (recorded as rows so the surface is complete + extensible):
  * akida_r2_noise        — AKIDA spontaneous R2 noise (pi5-akida AKD1000). Same A/B
                            by flipping ANIMA_ENTROPY_MODE on the pi5 host.
  * akida_edge_learn      — AKIDA on-chip edge-learn input (pi5-akida). Same A/B.
  * torch_lane_p          — torch Lane-P CLM seed (GPU host). Same A/B; needs torch.

See BENCHMARK.md for how to flip those on once the device/torch host is available.

────────────────────────────────────────────────────────────────────────────────
USAGE
────────────────────────────────────────────────────────────────────────────────
    python3 qentropy_benchmark.py                 # default N=64, JSON ledger to stdout
    python3 qentropy_benchmark.py --n 128         # more trials per arm
    python3 qentropy_benchmark.py --out ledger.json
    python3 qentropy_benchmark.py --json | jq .   # pipe-friendly

The per-arm env (ANIMA_ENTROPY_MODE) is set by the harness internally; you do NOT
set it yourself when running the full A/B. (You CAN set it for a single manual run
of a path module — see BENCHMARK.md.)
"""
from __future__ import annotations

import argparse
import json
import math
import os
import subprocess
import sys
from datetime import datetime, timezone

_HERE = os.path.dirname(os.path.abspath(__file__))
# repo root = mirror/qmirror/seed -> up 3
_REPO = os.path.abspath(os.path.join(_HERE, os.pardir, os.pardir, os.pardir))

MODES = ("quantum", "deterministic")


# ────────────────────────────────────────────────────────────────────────────
# Arm runners. Each runs ONE mode in a fresh subprocess (so ANIMA_ENTROPY_MODE is
# honestly applied at qentropy import time) and returns a list of per-trial scalar
# metrics + the provenance dict of (the last) draw + optional path-specific extras.
# ────────────────────────────────────────────────────────────────────────────

def _run_arm(mode: str, snippet: str) -> dict:
    """Run `snippet` in a fresh python3 -c subprocess with ANIMA_ENTROPY_MODE=mode.

    The snippet MUST print exactly one line of JSON to stdout as its LAST stdout line:
        {"metrics": [float, ...], "provenance": {...}, "extra": {...}}
    `extra` is optional path-specific aggregate data (e.g. a pooled histogram).
    qentropy's committed-buffer resolution works offline, so no network is used.
    """
    env = dict(os.environ)
    env["ANIMA_ENTROPY_MODE"] = mode
    # Make sure the arm can import qentropy + the path modules regardless of cwd.
    preamble = (
        "import sys, os, json\n"
        f"sys.path.insert(0, {_HERE!r})\n"            # qentropy
        f"sys.path.insert(0, {os.path.join(_REPO, 'PLASTICITY')!r})\n"
        f"sys.path.insert(0, {os.path.join(_REPO, 'CORE', 'DECODER')!r})\n"
        "import numpy as np\n"
    )
    proc = subprocess.run(
        [sys.executable, "-c", preamble + snippet],
        capture_output=True, text=True, env=env, cwd=_REPO, timeout=300,
    )
    if proc.returncode != 0:
        return {"error": (proc.stderr.strip()[-800:] or "nonzero exit"),
                "metrics": [], "provenance": {}, "extra": {}}
    # The arm may emit a benign stderr WARN (e.g. fallback). Parse the LAST stdout line.
    lines = [ln for ln in proc.stdout.strip().splitlines() if ln.strip()]
    if not lines:
        return {"error": "no stdout", "metrics": [], "provenance": {}, "extra": {}}
    out = json.loads(lines[-1])
    out.setdefault("extra", {})
    return out


def arm_plasticity(mode: str, n: int) -> dict:
    """SW learning path: run sw_approx_fit N times, collect weight_l1 per trial.

    Each trial draws a fresh weight-init from qentropy (the SW learning lever), so
    across N trials the weight_l1 spread reflects the entropy policy's variation.
    The input spike pattern is held FIXED across trials (a fixed deterministic numpy
    seed inside the arm) so the ONLY varying factor is the qentropy-sourced init —
    isolating the entropy path under test."""
    snippet = f"""
import plasticity_sw_approx as P
metrics = []
prov = {{}}
fixed = np.random.default_rng(20260606).integers(0, 2, size=(8, P.IN_DIM), dtype=np.uint8)
for _ in range({n}):
    r = P.sw_approx_fit(fixed)
    metrics.append(float(r["weight_l1"]))
    prov = r["entropy_provenance"]
print(json.dumps({{"metrics": metrics, "provenance": prov, "extra": {{}}}}))
"""
    return _run_arm(mode, snippet)


def arm_decoder(mode: str, n: int) -> dict:
    """DECODER sampling path: for each of N trials draw a block of tokens from a
    FIXED logits vector and record the Shannon entropy (bits) of that trial's token
    histogram. Also aggregate a pooled token histogram across all draws per mode. The
    forward logits are identical in both modes (only the draw differs)."""
    snippet = f"""
import decoder_qsample as D
logits = np.array([2.0, 1.0, 0.5, 3.0, 0.2, 1.5], dtype=np.float64)
block = 16
metrics = []
pooled = {{}}
prov = {{}}
for _ in range({n}):
    res = D.sample_n(logits, n=block, temperature=1.0)
    draws = res["draws"]
    vals, cnts = np.unique(draws, return_counts=True)
    p = cnts / cnts.sum()
    ent = float(-(p * np.log2(p)).sum())   # Shannon entropy (bits) of this trial
    metrics.append(ent)
    for v, c in zip(vals.tolist(), cnts.tolist()):
        pooled[str(int(v))] = pooled.get(str(int(v)), 0) + int(c)
    prov = res["provenance"]
print(json.dumps({{"metrics": metrics, "provenance": prov,
                   "extra": {{"pooled_histogram": pooled,
                              "argmax_forward": int(np.argmax(logits))}}}}))
"""
    return _run_arm(mode, snippet)


# ────────────────────────────────────────────────────────────────────────────
# Stats helpers (stdlib only — the harness top-level needs nothing exotic)
# ────────────────────────────────────────────────────────────────────────────

def _mean(xs):
    return sum(xs) / len(xs) if xs else None


def _std(xs):
    if not xs or len(xs) < 2:
        return 0.0
    m = sum(xs) / len(xs)
    return math.sqrt(sum((x - m) ** 2 for x in xs) / (len(xs) - 1))


# scipy is OPTIONAL. Probe ONCE at import; both a fast-path (scipy) and a fully
# self-contained pure-python fallback exist so the harness has ZERO hard deps.
try:
    from scipy import stats as _scipy_stats  # type: ignore
    _HAVE_SCIPY = True
except Exception:  # pragma: no cover - exercised only on a scipy-less host
    _scipy_stats = None
    _HAVE_SCIPY = False


# ── pure-python two-sample Kolmogorov–Smirnov ───────────────────────────────
def _ks_2samp_pure(a: list, b: list) -> tuple:
    """Self-contained two-sample KS. Returns (D, p_value).

    D = sup_x |F_a(x) - F_b(x)| over the merged support (the classic two-sample KS
    statistic — trivial to compute by walking the sorted union of both samples).
    The p-value uses the asymptotic Kolmogorov distribution:
        p ≈ Q_ks( (sqrt(en) + 0.12 + 0.11/sqrt(en)) * D ),  en = na*nb/(na+nb)
    where Q_ks(t) = 2 * Σ_{k≥1} (-1)^{k-1} exp(-2 k² t²)  (Numerical Recipes form).
    This matches scipy.stats.ks_2samp(mode='asymp') closely for n≳40.
    """
    na, nb = len(a), len(b)
    if na == 0 or nb == 0:
        return (0.0, 1.0)
    sa, sb = sorted(a), sorted(b)
    ia = ib = 0
    fa = fb = 0.0
    d = 0.0
    # Walk the merged sorted support, advancing all ties together, tracking |Fa-Fb|.
    while ia < na and ib < nb:
        x = min(sa[ia], sb[ib])
        while ia < na and sa[ia] <= x:
            ia += 1
        while ib < nb and sb[ib] <= x:
            ib += 1
        fa = ia / na
        fb = ib / nb
        d = max(d, abs(fa - fb))
    en = math.sqrt(na * nb / (na + nb))
    t = (en + 0.12 + 0.11 / en) * d
    p = _q_ks(t)
    return (d, max(0.0, min(1.0, p)))


def _q_ks(t: float) -> float:
    """Q_ks(t) = 2 Σ_{k≥1} (-1)^{k-1} exp(-2 k² t²) — asymptotic Kolmogorov tail."""
    if t <= 0.0:
        return 1.0
    a2 = -2.0 * t * t
    total = 0.0
    sign = 1.0
    prev = 0.0
    for k in range(1, 101):
        term = sign * math.exp(a2 * k * k)
        total += term
        if abs(term) <= 1e-12 * (abs(prev) if prev else 1.0) or abs(term) < 1e-300:
            break
        prev = total
        sign = -sign
    return 2.0 * total


def _ks_2samp(a: list, b: list) -> dict:
    """Two-sample KS test on continuous samples. scipy fast-path, pure-python
    fallback. Reports the D statistic + a two-sided p-value + which engine ran."""
    if len(a) < 2 or len(b) < 2:
        return None
    if _HAVE_SCIPY:
        r = _scipy_stats.ks_2samp(a, b)          # default = auto/exact for small n
        return {"test": "ks_2samp", "engine": "scipy",
                "ks_D": float(r.statistic), "p_value": float(r.pvalue),
                "n_quantum": len(a), "n_deterministic": len(b),
                "parity_at_alpha_0.05": bool(r.pvalue > 0.05)}
    d, p = _ks_2samp_pure(a, b)
    return {"test": "ks_2samp", "engine": "pure-python",
            "ks_D": d, "p_value": p,
            "n_quantum": len(a), "n_deterministic": len(b),
            "parity_at_alpha_0.05": bool(p > 0.05)}


# ── pure-python chi-square contingency on a 2×K token-count table ────────────
def _gammq(s: float, x: float) -> float:
    """Regularized upper incomplete gamma Q(s,x) = Γ(s,x)/Γ(s). Series + continued
    fraction (Numerical Recipes §6.2) — used for the chi-square upper-tail p-value."""
    if x < 0.0 or s <= 0.0:
        return 1.0
    if x == 0.0:
        return 1.0
    gln = math.lgamma(s)
    if x < s + 1.0:                                 # series representation -> P
        ap = s
        summ = 1.0 / s
        delta = summ
        for _ in range(1000):
            ap += 1.0
            delta *= x / ap
            summ += delta
            if abs(delta) < abs(summ) * 1e-14:
                break
        return 1.0 - summ * math.exp(-x + s * math.log(x) - gln)
    # continued fraction representation -> Q directly
    b = x + 1.0 - s
    c = 1e300
    d = 1.0 / b
    h = d
    for i in range(1, 1000):
        an = -i * (i - s)
        b += 2.0
        d = an * d + b
        if abs(d) < 1e-300:
            d = 1e-300
        c = b + an / c
        if abs(c) < 1e-300:
            c = 1e-300
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < 1e-14:
            break
    return h * math.exp(-x + s * math.log(x) - gln)


def _chi2_contingency_pure(table: list) -> tuple:
    """Pearson chi-square on an R×C contingency `table` (list of rows of counts).
    Returns (chi2, dof, p_value). p_value = Q(dof/2, chi2/2) (upper-tail)."""
    nrows = len(table)
    ncols = len(table[0]) if nrows else 0
    row_tot = [sum(r) for r in table]
    col_tot = [sum(table[i][j] for i in range(nrows)) for j in range(ncols)]
    grand = sum(row_tot)
    if grand == 0:
        return (0.0, 0, 1.0)
    chi2 = 0.0
    for i in range(nrows):
        for j in range(ncols):
            exp = row_tot[i] * col_tot[j] / grand
            if exp > 0.0:
                chi2 += (table[i][j] - exp) ** 2 / exp
    dof = (nrows - 1) * (ncols - 1)
    if dof <= 0:
        return (chi2, dof, 1.0)
    p = _gammq(dof / 2.0, chi2 / 2.0)
    return (chi2, dof, max(0.0, min(1.0, p)))


def _chi2_token_hist(q_hist: dict, d_hist: dict) -> dict:
    """Chi-square contingency on the pooled per-mode token histograms (2×K table).
    scipy fast-path, pure-python fallback. Tests whether the two modes' pooled token
    distributions differ. Drops zero-total columns (a token never drawn in either
    mode) to keep the expected counts well-defined."""
    keys = sorted(set(q_hist) | set(d_hist), key=lambda k: int(k))
    qrow = [int(q_hist.get(k, 0)) for k in keys]
    drow = [int(d_hist.get(k, 0)) for k in keys]
    # drop columns that are zero in BOTH modes (no information / undefined expected)
    cols = [(qc, dc) for qc, dc in zip(qrow, drow) if (qc + dc) > 0]
    if len(cols) < 2:
        return None
    qrow = [c[0] for c in cols]
    drow = [c[1] for c in cols]
    table = [qrow, drow]
    if _HAVE_SCIPY:
        chi2, p, dof, _ = _scipy_stats.chi2_contingency(table, correction=False)
        return {"test": "chi2_contingency", "engine": "scipy",
                "chi2": float(chi2), "dof": int(dof), "p_value": float(p),
                "n_quantum": sum(qrow), "n_deterministic": sum(drow),
                "k_tokens": len(qrow),
                "parity_at_alpha_0.05": bool(p > 0.05)}
    chi2, dof, p = _chi2_contingency_pure(table)
    return {"test": "chi2_contingency", "engine": "pure-python",
            "chi2": chi2, "dof": dof, "p_value": p,
            "n_quantum": sum(qrow), "n_deterministic": sum(drow),
            "k_tokens": len(qrow),
            "parity_at_alpha_0.05": bool(p > 0.05)}


def _coarse_separation(a: list, b: list) -> dict:
    """The ORIGINAL coarse closeness statistic |Δmean| / pooled_std — kept as a
    secondary, descriptive field (the rigorous verdict is now the KS p-value). Near
    0 = indistinguishable; this is a *parity* descriptor, NOT a win metric."""
    ma, mb = _mean(a), _mean(b)
    if ma is None or mb is None:
        return None
    sa, sb = _std(a), _std(b)
    pooled = math.sqrt((sa ** 2 + sb ** 2) / 2.0)
    if pooled == 0.0:
        sep = 0.0 if ma == mb else float("inf")
    else:
        sep = abs(ma - mb) / pooled
    return {
        "delta_mean": ma - mb,
        "abs_delta_mean": abs(ma - mb),
        "pooled_std": pooled,
        "standardized_separation": sep,            # ~0 = parity; >~1 = investigate
    }


def _prov_view(p: dict) -> dict:
    """The provenance columns that actually matter for the audit trail."""
    return {"mode": p.get("mode"), "tier": p.get("tier"), "sha256": p.get("sha256")}


# ────────────────────────────────────────────────────────────────────────────
# Ledger assembly
# ────────────────────────────────────────────────────────────────────────────

# device/torch-pending rows: the SAME A/B applies by flipping ANIMA_ENTROPY_MODE on
# the device/GPU host. Recorded so the benchmark surface is complete + obviously
# extensible (see BENCHMARK.md "Extending to device/torch paths").
PENDING_PATHS = [
    {
        "path": "akida_r2_noise",
        "status": "device-pending",
        "substrate": "pi5-akida (AKD1000)",
        "module": "SUB_ENGINES/AKIDA/scripts/spontaneous_emission.py",
        "metric": "R2 spontaneous-noise symbol histogram / spike rate",
        "how_to_run": ("on pi5-akida: ANIMA_ENTROPY_MODE={quantum,deterministic} "
                       "python3 spontaneous_emission.py  (qentropy_uniform 0..3)"),
    },
    {
        "path": "akida_edge_learn",
        "status": "device-pending",
        "substrate": "pi5-akida (AKD1000)",
        "module": "SUB_ENGINES/AKIDA/scripts/edge_learn_probe.py",
        "metric": "on-chip learned winner-unit distribution",
        "how_to_run": ("on pi5-akida: ANIMA_ENTROPY_MODE={quantum,deterministic} "
                       "python3 edge_learn_probe.py  (qentropy_bits learn-input)"),
    },
    {
        "path": "torch_lane_p",
        "status": "torch-pending",
        "substrate": "GPU host (Lane-P)",
        "module": "CLM/train/_qseed.py (resolve_seed) + _qseed_check.py",
        "metric": "torch.manual_seed -> torch.rand sample distribution",
        "how_to_run": ("on a torch host: ANIMA_ENTROPY_MODE={quantum,deterministic} "
                       "python3 CLM/train/_qseed_check.py"),
    },
]


def build_ledger(n: int) -> dict:
    runnable = [
        ("plasticity_sw_approx", arm_plasticity,
         "weight_l1", "L1 norm of SW-learned weight matrix (scalar per trial)"),
        ("decoder_qsample", arm_decoder,
         "token_hist_entropy_bits",
         "Shannon entropy (bits) of sampled-token histogram per trial"),
    ]
    rows = []
    for path, runner, metric_name, metric_desc in runnable:
        per_mode = {}
        arm_extra = {}
        raw_metrics = {}
        for mode in MODES:
            res = runner(mode, n)
            metrics = res.get("metrics", [])
            raw_metrics[mode] = metrics
            per_mode[mode] = {
                "n": len(metrics),
                "metric_mean": _mean(metrics),
                "metric_std": _std(metrics),
                "provenance": _prov_view(res.get("provenance", {})),
                "error": res.get("error"),
            }
            if res.get("extra"):
                arm_extra[mode] = res["extra"]
        qm = raw_metrics["quantum"]
        dm = raw_metrics["deterministic"]
        # PROPER two-sample test on the continuous per-trial metric (C7).
        ks = _ks_2samp(qm, dm)
        # Secondary descriptive coarse separation (kept for continuity with v1).
        coarse = _coarse_separation(qm, dm)
        # For the sampler path, ALSO run a chi-square on the pooled token histograms.
        chi2 = None
        if path == "decoder_qsample" and "quantum" in arm_extra and "deterministic" in arm_extra:
            qh = arm_extra["quantum"].get("pooled_histogram", {})
            dh = arm_extra["deterministic"].get("pooled_histogram", {})
            chi2 = _chi2_token_hist(qh, dh)
        formal_test = {"primary": ks, "coarse_separation": coarse}
        if chi2 is not None:
            formal_test["token_histogram_chi2"] = chi2
        # The path-level parity verdict = the primary KS test (continuous metric).
        parity = bool(ks["parity_at_alpha_0.05"]) if ks else None
        formal_test["parity_verdict"] = (
            "PARITY — fail to reject H0 (same distribution) at alpha=0.05; "
            "consistent with #123-A (expected)." if parity else
            "REJECT — p<0.05, distributional difference flagged (investigate: "
            "small-sample artifact or implementation asymmetry)." if parity is not None
            else "INDETERMINATE")
        qp = per_mode["quantum"]["provenance"]
        dp = per_mode["deterministic"]["provenance"]
        row = {
            "path": path,
            "status": "benchmarked",
            "substrate": "SW (Mac, $0, no device/torch)",
            "metric_name": metric_name,
            "metric_desc": metric_desc,
            "n_per_mode": n,
            "modes": per_mode,
            "formal_test": formal_test,
            "provenance_differs": (qp.get("tier") != dp.get("tier")),
        }
        if arm_extra:
            row["extra"] = arm_extra
        rows.append(row)
    return {
        "benchmark": "qentropy_quantum_vs_deterministic_AB",
        "milestone": "H_924 M6",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "host": "mac (SW-only, $0, no device, no torch)",
        "n_trials_per_arm": n,
        "modes": list(MODES),
        "stats_engine": ("scipy" if _HAVE_SCIPY else "pure-python"),
        "test_methodology": ("Two-sample Kolmogorov-Smirnov (ks_2samp) on the continuous "
                             "per-trial metric per path; PLUS a chi-square contingency "
                             "(chi2_contingency) on the decoder pooled token histograms. "
                             "H0 = both modes draw from the same distribution. p>0.05 = "
                             "FAIL TO REJECT = statistical PARITY = the EXPECTED, DESIRED "
                             "result (reproduces #123-A with a rigorous test). p<0.05 = "
                             "REJECT = reported honestly (small-sample artifact or real "
                             "asymmetry). scipy OPTIONAL — pure-python KS + chi-square "
                             "fallback gives identical schema (engine recorded per test)."),
        "framing": ("Statistical-parity SANITY + PROVENANCE differentiator, NOT a "
                    "superiority test. #123-A: ANU quantum == chacha20 PRNG statistically "
                    "(JSD 23x under NIST 7/7). Expectation: per-path metric distributions "
                    "are statistically indistinguishable across modes (parity holds at the "
                    "application level, p>0.05); the difference that matters is the provenance "
                    "column (quantum->anu_committed sha256 vs deterministic->numpy_prng seed)."),
        "rows": rows,
        "device_pending_rows": PENDING_PATHS,
        "honest_non_claim": ("This benchmark does NOT and cannot show quantum entropy is "
                             "'better'. The two modes are by design statistically equal. "
                             "The auditable PROVENANCE (physical ANU origin + sha256) is the "
                             "only real differentiator and is surfaced per path/mode."),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="qentropy quantum-vs-deterministic A/B benchmark")
    ap.add_argument("--n", type=int, default=128, help="trials per (path, mode) arm (>=128)")
    ap.add_argument("--out", type=str, default="", help="write ledger JSON to this path")
    ap.add_argument("--json", action="store_true", help="print ledger JSON to stdout (default)")
    args = ap.parse_args()
    n = max(args.n, 1)
    ledger = build_ledger(n)
    text = json.dumps(ledger, indent=2)
    if args.out:
        os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
        with open(args.out, "w") as f:
            f.write(text + "\n")
        sys.stderr.write(f"[qentropy_benchmark] ledger written: {args.out}\n")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
