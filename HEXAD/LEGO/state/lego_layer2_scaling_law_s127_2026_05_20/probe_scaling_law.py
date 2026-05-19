"""
§127 LEGO LAYER-2 SCALING-LAW PROBE
====================================

§126 measured η²(1024) / η²(256) = 1.189× — one scale-point comparison.
§127 fits a 4-point power-law scaling: N ∈ {256, 512, 1024, 2048} with same protocol.

Hypothesis form:  log η² = log a + k · log N
  k > +0.10  → ROBUST-POWER-LAW-GROWS-WITH-N
  |k| ≤ 0.10  → APPROXIMATELY-N-INVARIANT
  k < -0.10  → DEGRADES-WITH-N (small-N artifact)

Discipline
----------
- $0, NO GPU, NO runpod, NO fire, NO model.forward, NO corpus, NO dispatch.
- Import §117 lego_sim.py BYTE-IDENTICAL via importlib (no fork, no constructor edit).
- Same §125/§126 protocol: M=5 replicates × 12 stim × 80 steps × window=40, seeds {1337..1341}.
- Sole override: n_a/n_g/n_rec sized so n_a + n_g + n_rec = N for each N point.
- Network composition: n_a = n_g = 3N/8, n_rec = N/4 (preserves §117's 96/96/64 = 0.375/0.375/0.25 ratio).
"""

import importlib.util
import json
import math
import sys
import time
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
ANIMA = HERE.parent.parent
S117_LEGO_SIM = ANIMA / "state" / "lego_assembly_run_s117_2026_05_19" / "lego_sim.py"


def import_s117_lego_sim():
    spec = importlib.util.spec_from_file_location("s117_lego_sim", S117_LEGO_SIM)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["s117_lego_sim"] = mod
    spec.loader.exec_module(mod)
    return mod


def make_stimuli(d, n_stim, seed):
    rng = np.random.default_rng(seed)
    pats = []
    for _ in range(n_stim):
        v = np.zeros(d, dtype=np.float32)
        idx = rng.choice(d, d // 2, replace=False)
        v[idx] = 1.0
        pats.append(v)
    return pats


def sizes_for_N(N: int):
    """Preserve §117 ratio: n_a = n_g = 3N/8, n_rec = N/4. N must be divisible by 8."""
    assert N % 8 == 0
    return 3 * N // 8, 3 * N // 8, N // 4


def run_one_replicate(s117, seed: int, n_a: int, n_g: int, n_rec: int) -> np.ndarray:
    net = s117.LIFNet(n_a=n_a, n_g=n_g, n_rec=n_rec, seed=seed)
    n_stim, steps_per_stim, window = 12, 80, 40
    d = net.n_a + net.n_g + net.n_rec
    stimuli = make_stimuli(d=d, n_stim=n_stim, seed=seed + 9999)
    psi_trace = np.zeros((n_stim, steps_per_stim), dtype=np.float64)
    s_prev = np.zeros(d, dtype=np.float32)
    for si, stim in enumerate(stimuli):
        stim_rasters = []
        for t in range(steps_per_stim):
            ext = stim + net.W @ s_prev
            spike = net.step(ext)
            stim_rasters.append(spike.copy())
            s_prev = spike.astype(np.float32)
            t0 = max(0, t - window + 1)
            r_window = np.array(stim_rasters[t0 : t + 1])
            r_a = s117.spike_rate_vec(r_window, np.arange(net.n_a))
            r_g = s117.spike_rate_vec(r_window, np.arange(net.n_a, net.n_a + net.n_g))
            psi_trace[si, t] = s117.psi_c1(r_a, r_g)[0]
    return psi_trace


def variance_decomposition(values: np.ndarray) -> dict:
    n_stim, n_samples = values.shape
    grand_mean = values.mean()
    stim_means = values.mean(axis=1)
    ss_between = n_samples * float(((stim_means - grand_mean) ** 2).sum())
    ss_within = float(((values - stim_means[:, None]) ** 2).sum())
    ss_total = ss_between + ss_within
    eta_sq = ss_between / ss_total if ss_total > 0 else 0.0
    mi_nats = -0.5 * math.log(max(1.0 - eta_sq, 1e-12))
    mi_bits = mi_nats / math.log(2.0)
    return {
        "eta_squared": float(eta_sq),
        "gaussian_mi_bits": float(mi_bits),
        "ss_between": float(ss_between),
        "ss_within": float(ss_within),
        "ss_total": float(ss_total),
    }


def measure_eta_at_N(s117, N: int, M: int, seeds: list) -> dict:
    n_a, n_g, n_rec = sizes_for_N(N)
    n_stim, steps_per_stim = 12, 80
    all_traces = np.zeros((n_stim, M, steps_per_stim), dtype=np.float64)
    t0 = time.time()
    for r_idx, seed in enumerate(seeds):
        psi_trace = run_one_replicate(s117, seed=seed, n_a=n_a, n_g=n_g, n_rec=n_rec)
        all_traces[:, r_idx, :] = psi_trace
    wall = time.time() - t0
    pooled = all_traces.reshape(n_stim, M * steps_per_stim)
    decomp = variance_decomposition(pooled)
    decomp["N_total"] = N
    decomp["n_a"], decomp["n_g"], decomp["n_rec"] = n_a, n_g, n_rec
    decomp["wall_sec"] = wall
    print(f"  N={N:5d}  η²={decomp['eta_squared']:.4f}  wall={wall:.1f}s", file=sys.stderr)
    return decomp


def fit_power_law(N_arr: np.ndarray, eta_arr: np.ndarray) -> dict:
    """Fit log η² = log a + k · log N via least squares.
    Returns slope k (scaling exponent), intercept log_a, R², residuals."""
    x = np.log(N_arr.astype(np.float64))
    y = np.log(eta_arr.astype(np.float64))
    # OLS slope/intercept
    x_mean = x.mean()
    y_mean = y.mean()
    Sxy = ((x - x_mean) * (y - y_mean)).sum()
    Sxx = ((x - x_mean) ** 2).sum()
    slope = Sxy / Sxx
    intercept = y_mean - slope * x_mean
    y_pred = intercept + slope * x
    ss_res = ((y - y_pred) ** 2).sum()
    ss_tot = ((y - y_mean) ** 2).sum()
    r_squared = 1.0 - ss_res / ss_tot if ss_tot > 0 else 1.0
    residuals = (y - y_pred).tolist()
    return {
        "k_scaling_exponent": float(slope),
        "log_a_intercept": float(intercept),
        "a_intercept": float(math.exp(intercept)),
        "r_squared": float(r_squared),
        "log_N_values": x.tolist(),
        "log_eta_values": y.tolist(),
        "log_eta_predicted": y_pred.tolist(),
        "log_residuals": residuals,
    }


def classify_scaling(k: float) -> dict:
    if k > 0.10:
        verdict = "ROBUST-POWER-LAW-GROWS-WITH-N"
        note = f"Scaling exponent k={k:.3f} > 0.10 — η² growth is a robust power-law in N over the 256→2048 range."
    elif abs(k) <= 0.10:
        verdict = "APPROXIMATELY-N-INVARIANT"
        note = f"Scaling exponent k={k:.3f} |k| ≤ 0.10 — η² is approximately N-invariant; §125→§126 1.189× was within natural variation."
    else:
        verdict = "DEGRADES-WITH-N-SMALL-N-ARTIFACT"
        note = f"Scaling exponent k={k:.3f} < -0.10 — η² degrades with N; small-N substrate had artificially high stim-discrimination."
    return {"verdict": verdict, "note": note}


def main():
    s117 = import_s117_lego_sim()
    M = 5
    seeds = [1337 + r for r in range(M)]
    N_points = [256, 512, 1024, 2048]

    print(f"§127 4-point scaling law: N ∈ {N_points}, M={M} replicates each", file=sys.stderr)
    t_start = time.time()

    measurements = []
    for N in N_points:
        m = measure_eta_at_N(s117, N=N, M=M, seeds=seeds)
        measurements.append(m)

    N_arr = np.array([m["N_total"] for m in measurements])
    eta_arr = np.array([m["eta_squared"] for m in measurements])
    fit = fit_power_law(N_arr, eta_arr)
    classification = classify_scaling(fit["k_scaling_exponent"])
    total_wall = time.time() - t_start

    result = {
        "section": "§127",
        "title": "LEGO LAYER-2 SCALING-LAW PROBE",
        "tier": "probe-tier",
        "cost_usd": 0.0,
        "gpu": False, "runpod": False, "fire": False,
        "model_forward_byte_lm": False, "corpus": False, "dispatch": False,
        "orphan": 0,
        "wall_sec_total": total_wall,
        "central_blue_falsifier_sha256_prefix16_expected": "c93e160a8a376a94",
        "parent": [
            "§117 LIF substrate (layer-1 variance-only liveness)",
            "§124 3-layer liveness partition",
            "§125 layer-2 PARTIAL (η²=0.271 at N=256)",
            "§126 N-scale-up single-point (η²=0.322 at N=1024, ratio 1.189×)",
        ],
        "method": {
            "N_points": N_points,
            "M_replicates": M,
            "seeds": seeds,
            "n_stim": 12, "steps_per_stim": 80, "window": 40,
            "ratio_preserved_n_a_n_g_n_rec": "3N/8 : 3N/8 : N/4",
            "imports_s117_lego_sim_byte_identical": True,
            "no_fork_no_reimplementation": True,
        },
        "per_N_measurements": measurements,
        "power_law_fit": fit,
        "verdict": classification["verdict"],
        "verdict_note": classification["note"],
        "honest_inheritance": {
            "layer_1_variance_only": "§117 CLOSED",
            "layer_2_partial_at_N256": "§125 CLOSED (η²=0.271)",
            "layer_2_n_scale_single_point": "§126 CLOSED (ROBUST-GROWS at one point)",
            "layer_2_scaling_law": classification["verdict"],
            "layer_3_task_grounded": "OPEN",
            "wall_a": "§97 ORTHOGONAL inherited",
            "wall_b": "§115/§117/§124 INHERITED — sim-on-GPU confronted-not-removed",
        },
        "g3": "probe ≠ fire ≠ emergence; necessary-not-sufficient (B-EMERGE-7); capability claim 0; GOAL 미도달.",
    }

    out = HERE / "result.json"
    out.write_text(json.dumps(result, indent=2, ensure_ascii=False))
    summary = {
        "N_points": N_points,
        "eta_values": [m["eta_squared"] for m in measurements],
        "k_scaling_exponent": fit["k_scaling_exponent"],
        "r_squared": fit["r_squared"],
        "verdict": classification["verdict"],
        "wall_sec_total": round(total_wall, 1),
    }
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
