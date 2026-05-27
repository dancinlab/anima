"""
§133 LEGO LAYER-2 PER-N STANDARD ERROR — re-run §127 protocol with per-replicate η² capture

§127 saved pooled η² per N only. §133 captures per-replicate η² so that within-N
standard error of η² can be measured. Same protocol byte-identical: N ∈ {256, 512,
1024, 2048}, M=5 replicate seeds, 12 stim × 80 steps × window=40, 3:3:2 ratio.

Method (per N):
  - Run M=5 replicates as in §127.
  - For each replicate independently, compute per-replicate η² over its 12 stim
    × 80 samples = 960 samples (12 stim, n_samples_per_stim=80).
  - Report:
      η²_per_rep ∈ ℝ^5
      mean(η²) — should ≈ §127's pooled η² (NOT exactly equal — pooling concentrates)
      std(η²) — within-N standard error of η²
      jackknife SE = sqrt((M-1)/M · Σ (η²_(-i) - mean η²_(-i))²)
  - Closed-form: jackknife identity holds; SE bounded by total η² spread.
"""

import json
import math
import sys
import time
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
ANIMA = HERE.parent.parent
sys.path.insert(0, str(ANIMA / "HEXAD" / "LEGO"))
import lego_engine as E  # canonical SSOT post-§129


def run_one_replicate(seed, n_a, n_g, n_rec, n_stim=12, steps=80, window=40):
    net = E.LIFNet(n_a=n_a, n_g=n_g, n_rec=n_rec, seed=seed)
    d = net.n_a + net.n_g + net.n_rec
    stimuli = E.make_stimuli(d=d, n_stim=n_stim, seed=seed + 9999)
    psi_trace = np.zeros((n_stim, steps), dtype=np.float64)
    s_prev = np.zeros(d, dtype=np.float32)
    for si, stim in enumerate(stimuli):
        stim_rasters = []
        for t in range(steps):
            ext = stim + net.W @ s_prev
            spike = net.step(ext)
            stim_rasters.append(spike.copy())
            s_prev = spike.astype(np.float32)
            t0 = max(0, t - window + 1)
            r_win = np.array(stim_rasters[t0 : t + 1])
            r_a = E.spike_rate_vec(r_win, np.arange(net.n_a))
            r_g = E.spike_rate_vec(r_win, np.arange(net.n_a, net.n_a + net.n_g))
            psi_trace[si, t] = E.psi_c1(r_a, r_g)[0]
    return psi_trace


def measure_at_N(N, M, seeds):
    assert N % 8 == 0
    n_a = n_g = 3 * N // 8
    n_rec = N // 4
    per_replicate_eta = []
    pooled_traces = []
    t0 = time.time()
    for seed in seeds:
        trace = run_one_replicate(seed, n_a, n_g, n_rec)
        # Per-replicate η²: ANOVA over this single replicate's (12 stim × 80 steps)
        decomp = E.variance_decomposition(trace)  # shape (12, 80) → η² over 12 stim
        per_replicate_eta.append(decomp["eta_squared"])
        pooled_traces.append(trace)
    wall = time.time() - t0
    # Pooled η² (for byte-equal check vs §127)
    pooled = np.array(pooled_traces).transpose(1, 0, 2).reshape(12, M * 80)
    pooled_decomp = E.variance_decomposition(pooled)
    return {
        "N_total": N, "n_a": n_a, "n_g": n_g, "n_rec": n_rec,
        "M_replicates": M,
        "per_replicate_eta_squared": per_replicate_eta,
        "pooled_eta_squared": pooled_decomp["eta_squared"],
        "wall_sec": wall,
    }


def jackknife_se(values):
    """Leave-one-out jackknife SE: sqrt((n-1)/n * Σ (v_(-i) - mean v_(-i))²)."""
    n = len(values)
    arr = np.array(values, dtype=np.float64)
    pseudovals = np.array([np.delete(arr, i).mean() for i in range(n)])
    mean_pseudo = pseudovals.mean()
    se = math.sqrt(((n - 1) / n) * float(((pseudovals - mean_pseudo) ** 2).sum()))
    return se


def main():
    M = 5
    seeds = [1337 + r for r in range(M)]
    N_points = [256, 512, 1024, 2048]
    print(f"§133 per-N SE: N ∈ {N_points}, M={M}", file=sys.stderr)
    t_start = time.time()
    measurements = []
    for N in N_points:
        m = measure_at_N(N, M, seeds)
        eta = np.array(m["per_replicate_eta_squared"])
        m["eta_mean"] = float(eta.mean())
        m["eta_std"] = float(eta.std(ddof=1))
        m["eta_min"] = float(eta.min())
        m["eta_max"] = float(eta.max())
        m["eta_jackknife_se"] = jackknife_se(m["per_replicate_eta_squared"])
        # 95% CI naive: mean ± 1.96·std/sqrt(M)
        m["eta_95ci_lo"] = m["eta_mean"] - 1.96 * m["eta_std"] / math.sqrt(M)
        m["eta_95ci_hi"] = m["eta_mean"] + 1.96 * m["eta_std"] / math.sqrt(M)
        print(f"  N={N:5d}  pooled_η²={m['pooled_eta_squared']:.4f}  "
              f"per-rep mean={m['eta_mean']:.4f} std={m['eta_std']:.4f}  "
              f"jackknife_SE={m['eta_jackknife_se']:.4f}  wall={m['wall_sec']:.1f}s",
              file=sys.stderr)
        measurements.append(m)
    total_wall = time.time() - t_start

    # CI overlap analysis: does §127's non-monotonic pattern survive when CIs are
    # taken into account? Specifically: does the N=2048 CI overlap with N=512 / N=1024?
    by_N = {m["N_total"]: m for m in measurements}
    overlaps = {}
    for i in range(len(N_points)):
        for j in range(i + 1, len(N_points)):
            ni, nj = N_points[i], N_points[j]
            mi, mj = by_N[ni], by_N[nj]
            # Two CIs overlap iff ci_lo_max ≤ ci_hi_min
            ci_lo_max = max(mi["eta_95ci_lo"], mj["eta_95ci_lo"])
            ci_hi_min = min(mi["eta_95ci_hi"], mj["eta_95ci_hi"])
            overlaps[f"{ni}_vs_{nj}"] = bool(ci_lo_max <= ci_hi_min)

    result = {
        "section": "§133",
        "title": "LEGO LAYER-2 PER-N STANDARD ERROR (bootstrap/jackknife)",
        "tier": "probe-tier (per-replicate η² capture, re-runs §127 protocol)",
        "cost_usd": 0.0,
        "gpu": False, "runpod": False, "fire": False,
        "model_forward_byte_lm": False, "corpus": False, "dispatch": False,
        "orphan": 0,
        "wall_sec_total": total_wall,
        "central_blue_falsifier_sha256_prefix16_expected": "c93e160a8a376a94",
        "parent": [
            "§127 4-point η²(N) fit (pooled η² only, per-replicate η² NOT saved)",
            "§127 honest residual: 'Per-N standard error (not computed; would tighten verdict)'",
            "§129 HEXAD/LEGO/lego_engine.py canonical engine SSOT",
        ],
        "method": {
            "N_points": N_points,
            "M_replicates": M, "seeds": seeds,
            "n_stim": 12, "steps_per_stim": 80, "window": 40,
            "ratio_n_a_n_g_n_rec": "3N/8 : 3N/8 : N/4",
            "engine_canonical_lib": "HEXAD/LEGO/lego_engine.py",
        },
        "per_N_measurements": measurements,
        "ci_overlap_pairs": overlaps,
        "g3": ("probe ≠ fire ≠ emergence; necessary-not-sufficient (B-EMERGE-7); "
                "GOAL 미도달; M=5 small for tight SE — wide CIs honest."),
    }
    out = HERE / "result.json"
    out.write_text(json.dumps(result, indent=2, ensure_ascii=False))

    summary = {
        "N_points": N_points,
        "per_N_pooled_eta": [m["pooled_eta_squared"] for m in measurements],
        "per_N_eta_mean_std": [(round(m["eta_mean"], 4), round(m["eta_std"], 4))
                                for m in measurements],
        "per_N_jackknife_SE": [round(m["eta_jackknife_se"], 4) for m in measurements],
        "ci_overlaps": overlaps,
        "wall_sec_total": round(total_wall, 1),
    }
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
