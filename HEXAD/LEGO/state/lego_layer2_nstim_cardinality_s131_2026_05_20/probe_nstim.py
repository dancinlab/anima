"""
§131 LEGO LAYER-2 STIMULUS-CARDINALITY PROBE
=============================================

§127 measured η²(N) across 4 N points at fixed n_stim=12 → APPROXIMATELY-N-INVARIANT.
§131 asks the orthogonal question: at fixed N=256, how does η² depend on n_stim?

  n_stim ∈ {4, 12, 24, 48} (geometric step ×~2), N=256 fixed, M=5 replicates each.
  Imports HEXAD/LEGO/lego_engine.py canonical lib (post-§129 promote — NOT importlib
  from state/s117 anymore; this is the first probe written against the canonical
  engine SSOT).

Hypothesis form (pre-registered):
  ratio(η²_max / η²_min) > 1.50  → STRONGLY-NSTIM-DEPENDENT
  1.10 ≤ ratio ≤ 1.50            → MILDLY-NSTIM-DEPENDENT
  ratio < 1.10                    → NSTIM-INVARIANT

g3 (honest prior): n_stim → 1 forces all between-stim variance to 0 ⇒ η²=0; large
n_stim drowns the between-stim signal in within-stim noise; an intermediate n_stim
should peak. Whether anima's substrate is sensitive to this geometry at the §117
parametrisation is unknown.
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


def run_one_replicate(seed: int, n_a: int, n_g: int, n_rec: int,
                       n_stim: int, steps_per_stim: int = 80,
                       window: int = 40) -> np.ndarray:
    net = E.LIFNet(n_a=n_a, n_g=n_g, n_rec=n_rec, seed=seed)
    d = net.n_a + net.n_g + net.n_rec
    stimuli = E.make_stimuli(d=d, n_stim=n_stim, seed=seed + 9999)
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
            r_a = E.spike_rate_vec(r_window, np.arange(net.n_a))
            r_g = E.spike_rate_vec(r_window, np.arange(net.n_a, net.n_a + net.n_g))
            psi_trace[si, t] = E.psi_c1(r_a, r_g)[0]
    return psi_trace


def measure_eta_at_nstim(nstim: int, M: int, seeds: list,
                          n_a: int = 96, n_g: int = 96, n_rec: int = 64) -> dict:
    steps_per_stim = 80
    all_traces = np.zeros((nstim, M, steps_per_stim), dtype=np.float64)
    t0 = time.time()
    for r_idx, seed in enumerate(seeds):
        psi_trace = run_one_replicate(seed=seed, n_a=n_a, n_g=n_g, n_rec=n_rec,
                                        n_stim=nstim)
        all_traces[:, r_idx, :] = psi_trace
    wall = time.time() - t0
    pooled = all_traces.reshape(nstim, M * steps_per_stim)
    decomp = E.variance_decomposition(pooled)
    decomp["n_stim"] = nstim
    decomp["wall_sec"] = wall
    print(f"  n_stim={nstim:3d}  η²={decomp['eta_squared']:.4f}  "
          f"MI={decomp['gaussian_mi_bits']:.4f} bits  wall={wall:.1f}s",
          file=sys.stderr)
    return decomp


def classify(eta_ratio: float) -> dict:
    if eta_ratio > 1.50:
        v = "STRONGLY-NSTIM-DEPENDENT"
        n = f"η² range ratio {eta_ratio:.3f}× > 1.50 — n_stim is a strong modulator."
    elif 1.10 <= eta_ratio <= 1.50:
        v = "MILDLY-NSTIM-DEPENDENT"
        n = f"η² range ratio {eta_ratio:.3f}× — moderate n_stim sensitivity."
    else:
        v = "NSTIM-INVARIANT"
        n = f"η² range ratio {eta_ratio:.3f}× < 1.10 — η² approximately invariant under n_stim."
    return {"verdict": v, "note": n}


def main():
    M = 5
    seeds = [1337 + r for r in range(M)]
    nstim_points = [4, 12, 24, 48]

    print(f"§131 n_stim cardinality probe: nstim ∈ {nstim_points}, N=256, M={M}",
          file=sys.stderr)
    t_start = time.time()

    measurements = []
    for nstim in nstim_points:
        m = measure_eta_at_nstim(nstim=nstim, M=M, seeds=seeds)
        measurements.append(m)

    etas = [m["eta_squared"] for m in measurements]
    eta_max, eta_min = max(etas), min(etas)
    eta_ratio = eta_max / eta_min if eta_min > 0 else float("inf")
    cls = classify(eta_ratio)
    total_wall = time.time() - t_start

    # Locate peak n_stim
    peak_idx = etas.index(eta_max)
    peak_nstim = nstim_points[peak_idx]

    result = {
        "section": "§131",
        "title": "LEGO LAYER-2 STIMULUS-CARDINALITY PROBE",
        "tier": "probe-tier",
        "cost_usd": 0.0,
        "gpu": False, "runpod": False, "fire": False,
        "model_forward_byte_lm": False, "corpus": False, "dispatch": False,
        "orphan": 0,
        "wall_sec_total": total_wall,
        "central_blue_falsifier_sha256_prefix16_expected": "c93e160a8a376a94",
        "parent": [
            "§125/§126/§127 LEGO arc layer-2 axis on N (network size)",
            "§129 HEXAD/LEGO/lego_engine.py canonical engine SSOT",
        ],
        "method": {
            "nstim_points": nstim_points,
            "M_replicates": M,
            "seeds": seeds,
            "N_total_fixed": 256, "n_a": 96, "n_g": 96, "n_rec": 64,
            "steps_per_stim": 80, "window": 40,
            "engine_canonical_lib": "HEXAD/LEGO/lego_engine.py (post-§129)",
        },
        "per_nstim_measurements": measurements,
        "eta_squared_values": etas,
        "eta_max": eta_max, "eta_min": eta_min, "eta_range_ratio": eta_ratio,
        "peak_n_stim": peak_nstim,
        "verdict": cls["verdict"],
        "verdict_note": cls["note"],
        "g3": "probe ≠ fire ≠ emergence; necessary-not-sufficient (B-EMERGE-7); GOAL 미도달.",
    }
    out = HERE / "result.json"
    out.write_text(json.dumps(result, indent=2, ensure_ascii=False))

    summary = {
        "nstim_points": nstim_points,
        "eta_values": etas,
        "eta_range_ratio": round(eta_ratio, 3),
        "peak_n_stim": peak_nstim,
        "verdict": cls["verdict"],
        "wall_sec_total": round(total_wall, 1),
    }
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
