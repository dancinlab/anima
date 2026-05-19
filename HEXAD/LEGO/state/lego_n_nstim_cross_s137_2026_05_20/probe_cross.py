"""
§137 LEGO (N, n_stim) CROSS-MATRIX
===================================

§127 measured η²(N) at fixed n_stim=12 → APPROXIMATELY-N-INVARIANT.
§131 measured η²(n_stim) at fixed N=256 → STRONGLY-NSTIM-DEPENDENT, peak n_stim=4.

§137 asks the joint question: does the peak n_stim shift as N grows? 2×3 grid.

  N ∈ {256, 1024}, n_stim ∈ {4, 12, 24}, M=3 replicates, canonical engine post-§134.

Verdict bucket (pre-registered):
  peak n_stim same at both N        → PEAK-N-STIM-N-INVARIANT
  peak n_stim shifts with N         → PEAK-N-STIM-SHIFTS-WITH-N
  no clear peak at one or both N    → CROSS-MATRIX-INCONCLUSIVE
"""

import json
import sys
import time
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
ANIMA = HERE.parent.parent.parent.parent
sys.path.insert(0, str(ANIMA / "HEXAD" / "LEGO"))
import lego_engine as E


def run_replicate(seed, n_a, n_g, n_rec, n_stim, steps=80, window=40):
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


def measure_cell(N, n_stim, M, seeds):
    assert N % 8 == 0
    n_a = n_g = 3 * N // 8
    n_rec = N // 4
    all_traces = np.zeros((n_stim, M, 80), dtype=np.float64)
    t0 = time.time()
    for r_idx, seed in enumerate(seeds):
        all_traces[:, r_idx, :] = run_replicate(seed, n_a, n_g, n_rec, n_stim)
    pooled = all_traces.reshape(n_stim, M * 80)
    decomp = E.variance_decomposition(pooled)
    return {"N": N, "n_stim": n_stim, "eta_squared": decomp["eta_squared"],
            "wall_sec": time.time() - t0}


def main():
    M = 3
    seeds = [1337 + r for r in range(M)]
    N_pts = [256, 1024]
    nstim_pts = [4, 12, 24]
    print(f"§137 cross-matrix: N ∈ {N_pts} × n_stim ∈ {nstim_pts}, M={M}", file=sys.stderr)

    t_start = time.time()
    cells = []
    for N in N_pts:
        for ns in nstim_pts:
            c = measure_cell(N, ns, M, seeds)
            print(f"  N={N:5d} n_stim={ns:3d}: η²={c['eta_squared']:.4f} wall={c['wall_sec']:.1f}s",
                  file=sys.stderr)
            cells.append(c)
    total_wall = time.time() - t_start

    # Peak n_stim per N
    peak_by_N = {}
    for N in N_pts:
        N_cells = [c for c in cells if c["N"] == N]
        peak = max(N_cells, key=lambda c: c["eta_squared"])
        peak_by_N[N] = {"peak_n_stim": peak["n_stim"], "peak_eta": peak["eta_squared"]}

    peaks = [peak_by_N[N]["peak_n_stim"] for N in N_pts]
    peak_invariant = (len(set(peaks)) == 1)
    verdict = ("PEAK-N-STIM-N-INVARIANT" if peak_invariant
               else "PEAK-N-STIM-SHIFTS-WITH-N")

    result = {
        "section": "§137",
        "title": "LEGO (N, n_stim) CROSS-MATRIX",
        "tier": "probe-tier",
        "cost_usd": 0.0,
        "gpu": False, "runpod": False, "fire": False,
        "model_forward_byte_lm": False, "corpus": False, "dispatch": False,
        "orphan": 0,
        "wall_sec_total": total_wall,
        "central_blue_falsifier_sha256_prefix16_expected": "c93e160a8a376a94",
        "parent": ["§127 η²(N) APPROXIMATELY-N-INVARIANT", "§131 η²(n_stim) STRONGLY-NSTIM-DEPENDENT",
                    "§134/§135 canonical engine"],
        "method": {"N_points": N_pts, "nstim_points": nstim_pts, "M_replicates": M,
                    "seeds": seeds, "n_stim_fixed": False, "engine": "HEXAD/LEGO/lego_engine.py canonical"},
        "cells": cells,
        "peak_by_N": peak_by_N,
        "verdict": verdict,
        "g3": "probe ≠ fire ≠ emergence; necessary-not-sufficient (B-EMERGE-7); GOAL 미도달.",
    }
    (HERE / "result.json").write_text(json.dumps(result, indent=2, ensure_ascii=False))
    print(json.dumps({"verdict": verdict, "peak_by_N": peak_by_N,
                       "wall_sec": round(total_wall, 1)}, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
