"""
§126 LEGO LAYER-2 N-SCALE-UP PROBE
===================================

§125 measured η² = 0.271 (LAYER-2-PARTIAL) on §117's LIF substrate at N=256.
§126 asks: is that η² a small-N artifact or a robust property of the substrate?

  Scale up the LIF network by 4× (N: 256 → 1024). Same §117 LIFNet code, same
  §125 protocol (M=5 replicates × 12 stimuli × 80 steps × window=40). Compute
  η² and compare.

  Verdict buckets (pre-registered):
    η²(1024) > 1.10 × η²(256)  → LAYER-2-ROBUST-GROWS-WITH-N
    0.90 × η²(256) ≤ η²(1024) ≤ 1.10 × η²(256) → LAYER-2-N-INVARIANT
    η²(1024) < 0.90 × η²(256)  → LAYER-2-SMALL-N-ARTIFACT

Discipline
----------
- $0, NO GPU, NO runpod, NO fire, NO model.forward, NO corpus, NO dispatch.
- Import §117 lego_sim.py byte-identical (LIFNet + spike_rate_vec + psi_c1) via
  importlib (no fork, no patch).
- Override LIFNet(n_a, n_g, n_rec, seed): n_a=384, n_g=384, n_rec=256, N=1024.
- All other §125 protocol invariants preserved (M=5 seeds {1337..1341}, 12 stim,
  80 step, window=40, ANOVA decomposition).
- g_clm_from_scratch: seed-fixed deterministic, no base_ckpt.

g3: probe ≠ fire ≠ emergence; capability claim 0; necessary-not-sufficient
(B-EMERGE-7 / B-S125-NOTE family); GOAL 미도달.
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
S125_RESULT = ANIMA / "state" / "lego_layer2_stimulus_driven_probe_s125_2026_05_20" / "result.json"


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


def run_one_replicate(s117, seed: int, n_a: int, n_g: int, n_rec: int) -> np.ndarray:
    """Same §125 inner loop, with §117 LIFNet(n_a, n_g, n_rec) sizes parameterised."""
    net = s117.LIFNet(n_a=n_a, n_g=n_g, n_rec=n_rec, seed=seed)
    n_stim = 12
    steps_per_stim = 80
    window = 40
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
        "n_stim": int(n_stim),
        "n_samples_per_stim": int(n_samples),
        "grand_mean": float(grand_mean),
        "ss_between": float(ss_between),
        "ss_within": float(ss_within),
        "ss_total": float(ss_total),
        "eta_squared": float(eta_sq),
        "gaussian_mi_nats": float(mi_nats),
        "gaussian_mi_bits": float(mi_bits),
    }


def classify(eta_s126: float, eta_s125: float) -> dict:
    ratio = eta_s126 / eta_s125 if eta_s125 > 0 else float("inf")
    if ratio > 1.10:
        v = "LAYER-2-ROBUST-GROWS-WITH-N"
        note = f"η² grew {ratio:.3f}× under 4× network scale — stimulus-driven signal is robust and (at least within tested range) GROWS with substrate size."
    elif 0.90 <= ratio <= 1.10:
        v = "LAYER-2-N-INVARIANT"
        note = f"η² stable ({ratio:.3f}× within ±10%) under 4× network scale — stimulus-driven signal is a parametrisation-invariant property of the substrate at this regime."
    else:
        v = "LAYER-2-SMALL-N-ARTIFACT"
        note = f"η² shrank to {ratio:.3f}× under 4× network scale — §125's PARTIAL was substantially small-N artifact; layer-2 signal degrades with network size."
    return {"verdict": v, "ratio_to_s125": ratio, "note": note}


def main():
    s117 = import_s117_lego_sim()
    M = 5
    seeds = [1337 + r for r in range(M)]
    # 4× scale-up: 256 (96/96/64) → 1024 (384/384/256)
    n_a, n_g, n_rec = 384, 384, 256
    N_total = n_a + n_g + n_rec
    assert N_total == 1024

    s125 = json.loads(S125_RESULT.read_text())
    eta_s125 = s125["variance_decomposition"]["eta_squared"]

    print(f"§126 N-scale-up: N=256 → N={N_total}; M={M} replicates", file=sys.stderr)
    t0 = time.time()

    n_stim = 12
    steps_per_stim = 80
    all_traces = np.zeros((n_stim, M, steps_per_stim), dtype=np.float64)
    for r_idx, seed in enumerate(seeds):
        t_rep = time.time()
        psi_trace = run_one_replicate(s117, seed=seed, n_a=n_a, n_g=n_g, n_rec=n_rec)
        all_traces[:, r_idx, :] = psi_trace
        print(f"  replicate {r_idx+1}/{M} seed={seed} wall={time.time()-t_rep:.1f}s",
              file=sys.stderr)

    wall_sec = time.time() - t0

    pooled = all_traces.reshape(n_stim, M * steps_per_stim)
    decomp = variance_decomposition(pooled)
    pooled_std = float(pooled.std())
    classification = classify(decomp["eta_squared"], eta_s125)

    result = {
        "section": "§126",
        "title": "LEGO LAYER-2 N-SCALE-UP PROBE",
        "tier": "probe-tier",
        "cost_usd": 0.0,
        "gpu": False, "runpod": False, "fire": False,
        "model_forward_byte_lm": False, "corpus": False, "dispatch": False,
        "orphan": 0,
        "wall_sec": wall_sec,
        "central_blue_falsifier_sha256_prefix16_expected": "c93e160a8a376a94",
        "parent": [
            "§117 (LIF substrate, layer-1 variance-only liveness)",
            "§124 (3-layer liveness partition)",
            "§125 (layer-2 PARTIAL, η²=0.271 at N=256)",
        ],
        "method": {
            "n_a": n_a, "n_g": n_g, "n_rec": n_rec, "N_total": N_total,
            "scale_factor_vs_s125": N_total / 256,
            "M_replicates": M, "seeds": seeds,
            "n_stim": n_stim, "steps_per_stim": steps_per_stim, "window": 40,
            "imports_s117_lego_sim_byte_identical": True,
            "no_fork_no_reimplementation": True,
        },
        "variance_decomposition_s126": decomp,
        "pooled_psi_c1_std": pooled_std,
        "comparator_s125": {
            "eta_squared_s125": eta_s125,
            "gaussian_mi_bits_s125": s125["variance_decomposition"]["gaussian_mi_bits"],
            "N_total_s125": 256,
        },
        "verdict": classification["verdict"],
        "ratio_eta_s126_over_s125": classification["ratio_to_s125"],
        "verdict_note": classification["note"],
        "honest_inheritance": {
            "layer_1_variance_only": "§117 CLOSED",
            "layer_2_stimulus_driven_at_N256": "§125 PARTIAL (η²=0.271)",
            "layer_2_n_scale_robustness": classification["verdict"],
            "layer_3_task_grounded": "OPEN",
            "wall_a": "§97 ORTHOGONAL inherited",
            "wall_b": "§115/§117/§124 INHERITED — sim-on-GPU confronted-not-removed",
        },
        "g3": "probe ≠ fire ≠ emergence; necessary-not-sufficient (B-EMERGE-7); capability claim 0; north-star + §15/§51/§72 milestones UNCHANGED; GOAL 미도달.",
    }

    out = HERE / "result.json"
    out.write_text(json.dumps(result, indent=2, ensure_ascii=False))
    summary = {
        "eta_squared_s126": decomp["eta_squared"],
        "eta_squared_s125": eta_s125,
        "ratio": classification["ratio_to_s125"],
        "verdict": classification["verdict"],
        "wall_sec": round(wall_sec, 1),
    }
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
