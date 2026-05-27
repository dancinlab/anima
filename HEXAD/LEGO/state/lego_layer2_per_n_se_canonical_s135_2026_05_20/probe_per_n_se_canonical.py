"""
§135 LEGO LAYER-2 PER-N STANDARD ERROR (CANONICAL ENGINE)
==========================================================

Closes §134's named open: §133's per-rep monotone-decrease finding
(0.382→0.258 across N=256→2048 on drifted engine) needs full 4-point
re-run on canonical engine post-§134 byte-equal restore.

Re-runs §133 protocol on canonical engine at all 4 N points:
  N ∈ {256, 512, 1024, 2048}, M=5 replicates, seeds {1337..1341},
  n_stim=12, steps=80, window=40, ratio 3:3:2.

Predictions (pre-registered, drift-aware):
  - Pooled η² at each N should match §127's published values byte-equal
    (extends §134's 2-point subset confirmation to all 4 points).
  - Per-rep mean η² is HIGHER than pooled η² (within-replicate stim
    discrimination is cleaner than pooled, by ANOVA arithmetic).
  - Per-rep monotone-decrease pattern from drifted §133 — does it survive
    on canonical?

Verdict bucket:
  - Per-rep mean: monotone-decreasing in N → MONOTONE-DECREASE-SURVIVES
  - Per-rep mean: non-monotonic (peak somewhere) → NON-MONOTONIC-ON-CANONICAL
  - Per-rep mean: flat → APPROXIMATELY-N-INVARIANT
"""

import json
import math
import sys
import time
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
ANIMA = HERE.parent.parent.parent.parent
sys.path.insert(0, str(ANIMA / "HEXAD" / "LEGO"))
import lego_engine as E

S127_RESULT = ANIMA / "state" / "lego_layer2_scaling_law_s127_2026_05_20" / "result.json"
S133_RESULT = ANIMA / "state" / "lego_layer2_per_n_se_s133_2026_05_20" / "result.json"


def run_replicate(seed, n_a, n_g, n_rec, n_stim=12, steps=80, window=40):
    net = E.LIFNet(n_a=n_a, n_g=n_g, n_rec=n_rec, seed=seed)
    d = net.n_a + net.n_g + net.n_rec
    stimuli = E.make_stimuli(d=d, n_stim=n_stim, seed=seed + 9999)
    psi_trace = np.zeros((n_stim, steps), dtype=np.float64)
    s_prev = np.zeros(d, dtype=np.float32)
    for si, stim in enumerate(stimuli):
        rasters = []
        for t in range(steps):
            ext = stim + net.W @ s_prev
            spike = net.step(ext)
            rasters.append(spike.copy())
            s_prev = spike.astype(np.float32)
            t0 = max(0, t - window + 1)
            r_win = np.array(rasters[t0 : t + 1])
            r_a = E.spike_rate_vec(r_win, np.arange(net.n_a))
            r_g = E.spike_rate_vec(r_win, np.arange(net.n_a, net.n_a + net.n_g))
            psi_trace[si, t] = E.psi_c1(r_a, r_g)[0]
    return psi_trace


def jackknife_se(values):
    n = len(values)
    arr = np.array(values, dtype=np.float64)
    pseudovals = np.array([np.delete(arr, i).mean() for i in range(n)])
    mean_pseudo = pseudovals.mean()
    return math.sqrt(((n - 1) / n) * float(((pseudovals - mean_pseudo) ** 2).sum()))


def measure_at_N(N, M, seeds):
    assert N % 8 == 0
    n_a = n_g = 3 * N // 8
    n_rec = N // 4
    per_rep = []
    pooled_traces = []
    t0 = time.time()
    for seed in seeds:
        trace = run_replicate(seed, n_a, n_g, n_rec)
        per_rep.append(E.variance_decomposition(trace)["eta_squared"])
        pooled_traces.append(trace)
    pooled = np.array(pooled_traces).transpose(1, 0, 2).reshape(12, M * 80)
    pooled_decomp = E.variance_decomposition(pooled)
    eta = np.array(per_rep)
    return {
        "N_total": N, "n_a": n_a, "n_g": n_g, "n_rec": n_rec,
        "M_replicates": M,
        "per_replicate_eta_squared": per_rep,
        "pooled_eta_squared": pooled_decomp["eta_squared"],
        "eta_mean": float(eta.mean()),
        "eta_std": float(eta.std(ddof=1)),
        "eta_min": float(eta.min()),
        "eta_max": float(eta.max()),
        "eta_jackknife_se": jackknife_se(per_rep),
        "eta_95ci_lo": float(eta.mean() - 1.96 * eta.std(ddof=1) / math.sqrt(M)),
        "eta_95ci_hi": float(eta.mean() + 1.96 * eta.std(ddof=1) / math.sqrt(M)),
        "wall_sec": time.time() - t0,
    }


def classify_monotonicity(per_rep_means):
    """Decide which bucket: monotone-decrease / non-monotonic / approximately-flat."""
    arr = np.array(per_rep_means)
    diffs = np.diff(arr)
    all_decreasing = bool(np.all(diffs < 0))
    all_increasing = bool(np.all(diffs > 0))
    spread = arr.max() - arr.min()
    range_ratio = arr.max() / arr.min() if arr.min() > 0 else float("inf")

    if all_decreasing:
        v = "MONOTONE-DECREASE-SURVIVES-CANONICAL"
        n = f"Per-rep mean monotonically decreases across all 4 N points (range ratio {range_ratio:.3f}×)."
    elif all_increasing:
        v = "MONOTONE-INCREASE-CANONICAL"
        n = f"Per-rep mean monotonically increases (unexpected; range ratio {range_ratio:.3f}×)."
    elif range_ratio < 1.10:
        v = "APPROXIMATELY-N-INVARIANT-CANONICAL"
        n = f"Per-rep mean approximately N-invariant (range ratio {range_ratio:.3f}× < 1.10)."
    else:
        v = "NON-MONOTONIC-ON-CANONICAL"
        # Find peak
        peak_idx = int(np.argmax(arr))
        v_peak = f"peak at index {peak_idx}"
        n = f"Per-rep mean is non-monotonic ({v_peak}); range ratio {range_ratio:.3f}×."
    return {"verdict": v, "note": n, "range_ratio": range_ratio,
            "all_decreasing": all_decreasing, "spread": float(spread)}


def main():
    M = 5
    seeds = [1337 + r for r in range(M)]
    N_pts = [256, 512, 1024, 2048]
    print(f"§135 canonical re-run: N ∈ {N_pts}, M={M}", file=sys.stderr)

    t_start = time.time()
    measurements = []
    for N in N_pts:
        m = measure_at_N(N, M, seeds)
        print(f"  N={N:5d}  pooled_η²={m['pooled_eta_squared']:.4f}  "
              f"per-rep mean={m['eta_mean']:.4f} std={m['eta_std']:.4f}  "
              f"jackknife_SE={m['eta_jackknife_se']:.4f}  wall={m['wall_sec']:.1f}s",
              file=sys.stderr)
        measurements.append(m)
    total_wall = time.time() - t_start

    per_rep_means = [m["eta_mean"] for m in measurements]
    pooled_etas = [m["pooled_eta_squared"] for m in measurements]
    cls = classify_monotonicity(per_rep_means)

    # CI overlap analysis
    overlaps = {}
    by_N = {m["N_total"]: m for m in measurements}
    for i in range(len(N_pts)):
        for j in range(i + 1, len(N_pts)):
            ni, nj = N_pts[i], N_pts[j]
            mi, mj = by_N[ni], by_N[nj]
            ci_lo_max = max(mi["eta_95ci_lo"], mj["eta_95ci_lo"])
            ci_hi_min = min(mi["eta_95ci_hi"], mj["eta_95ci_hi"])
            overlaps[f"{ni}_vs_{nj}"] = bool(ci_lo_max <= ci_hi_min)

    # Compare to §127's pooled values
    s127 = json.loads(S127_RESULT.read_text())
    s127_pooled = {m["N_total"]: m["eta_squared"] for m in s127["per_N_measurements"]}
    s127_match = {}
    for m in measurements:
        N = m["N_total"]
        s127_match[N] = {
            "s127_pooled": s127_pooled[N],
            "canonical_pooled": m["pooled_eta_squared"],
            "byte_equal": abs(s127_pooled[N] - m["pooled_eta_squared"]) < 1e-6,
        }

    # Compare to drifted §133
    s133 = json.loads(S133_RESULT.read_text())
    s133_per_rep_mean = {m["N_total"]: m["eta_mean"] for m in s133["per_N_measurements"]}
    drift_diagnostics = {}
    for m in measurements:
        N = m["N_total"]
        drift_diagnostics[N] = {
            "drifted_per_rep_mean": s133_per_rep_mean[N],
            "canonical_per_rep_mean": m["eta_mean"],
            "drift": abs(s133_per_rep_mean[N] - m["eta_mean"]),
        }

    result = {
        "section": "§135",
        "title": "LEGO LAYER-2 PER-N SE (canonical engine post-§134)",
        "tier": "probe-tier (canonical engine re-run of §133 protocol)",
        "cost_usd": 0.0,
        "gpu": False, "runpod": False, "fire": False,
        "model_forward_byte_lm": False, "corpus": False, "dispatch": False,
        "orphan": 0,
        "wall_sec_total": total_wall,
        "central_blue_falsifier_sha256_prefix16_expected": "c93e160a8a376a94",
        "parent": [
            "§133 drifted-engine per-N SE (monotone-decrease per-rep mean 0.382→0.258)",
            "§134 engine byte-equality restore (canonical = §117 source byte-equal)",
        ],
        "method": {
            "N_points": N_pts,
            "M_replicates": M, "seeds": seeds,
            "n_stim": 12, "steps_per_stim": 80, "window": 40,
            "ratio": "3N/8 : 3N/8 : N/4",
            "engine": "HEXAD/LEGO/lego_engine.py post-§134 byte-equal §117",
        },
        "per_N_measurements": measurements,
        "ci_overlap_pairs": overlaps,
        "s127_match_per_N": s127_match,
        "drift_vs_s133_per_N": drift_diagnostics,
        "per_rep_mean_classification": cls,
        "verdict": cls["verdict"],
        "verdict_note": cls["note"],
        "g3": ("probe ≠ fire ≠ emergence; necessary-not-sufficient (B-EMERGE-7); "
                "GOAL 미도달; M=5 small for tight SE."),
    }
    out = HERE / "result.json"
    out.write_text(json.dumps(result, indent=2, ensure_ascii=False))

    summary = {
        "N_pts": N_pts,
        "pooled_eta": [round(m["pooled_eta_squared"], 4) for m in measurements],
        "per_rep_mean": [round(m["eta_mean"], 4) for m in measurements],
        "per_rep_std": [round(m["eta_std"], 4) for m in measurements],
        "jackknife_SE": [round(m["eta_jackknife_se"], 4) for m in measurements],
        "ci_overlaps": overlaps,
        "all_4N_match_s127": all(s127_match[N]["byte_equal"] for N in N_pts),
        "verdict": cls["verdict"],
        "wall_sec_total": round(total_wall, 1),
    }
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
