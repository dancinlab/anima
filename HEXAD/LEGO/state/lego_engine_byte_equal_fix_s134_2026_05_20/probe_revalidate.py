"""
§134 ENGINE BYTE-EQUALITY RESTORE + RE-VALIDATE §131 + §133

§133 measurement detected pooled η² drift between §127 (which imported
state/lego_assembly_run_s117_2026_05_19/lego_sim.py via importlib) and
§131/§132/§133 (which imported HEXAD/LEGO/lego_engine.py post-§129 promote).
AST diff confirmed the §129 promote was NOT byte-equal: v init, dtypes, RNG
consumption order, bias term, STDP rates, w_max all differed.

§134 rewrote lego_engine.py to be byte-equal to §117 source. This probe
re-validates that fix by:
  (1) AST + numeric smoke: lego_engine matches §117 byte-equal post-§134.
  (2) Re-running §131 protocol (n_stim cardinality) on the canonical engine.
  (3) Re-running §133 protocol (per-N) on the canonical engine.
  (4) Reporting drift magnitude: |η²_canonical - η²_original| at every point.

Prediction (pre-registered before running):
  Post-§134 canonical-engine η² at N=256/n_stim=12 should ≈ 0.271 (matching
  §127's pooled value), NOT 0.218 (drifted §131/§133 value).
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
S127_RESULT = ANIMA / "state" / "lego_layer2_scaling_law_s127_2026_05_20" / "result.json"
S131_RESULT = ANIMA / "state" / "lego_layer2_nstim_cardinality_s131_2026_05_20" / "result.json"
S133_RESULT = ANIMA / "state" / "lego_layer2_per_n_se_s133_2026_05_20" / "result.json"
sys.path.insert(0, str(ANIMA / "HEXAD" / "LEGO"))
import lego_engine as E  # canonical post-§134 byte-equal restore


def import_s117():
    spec = importlib.util.spec_from_file_location("s117", S117_LEGO_SIM)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def byte_equal_smoke():
    """Verify lego_engine.LIFNet/spike_rate_vec/psi_c1 produce byte-equal output
    to §117 source after 80-step run with deterministic stim."""
    s117 = import_s117()
    net1 = s117.LIFNet(seed=1337)
    net2 = E.LIFNet(seed=1337)
    init_W_equal = bool(np.array_equal(net1.W, net2.W))
    init_v_equal = bool(np.array_equal(net1.v, net2.v))
    init_bias_equal = bool(np.array_equal(net1.bias, net2.bias))

    rng = np.random.default_rng(9999 + 1337)
    stim = np.zeros(net1.N); stim[rng.choice(net1.N, net1.N // 2, replace=False)] = 1.0
    s_prev1 = np.zeros(net1.N); s_prev2 = np.zeros(net2.N)
    for _ in range(80):
        s1 = net1.step(stim + net1.W @ s_prev1)
        s2 = net2.step(stim + net2.W @ s_prev2)
        s_prev1, s_prev2 = s1, s2
    final_spike_equal = bool(np.array_equal(s1, s2))
    final_W_equal = bool(np.array_equal(net1.W, net2.W))
    return {
        "init_W_byte_equal": init_W_equal,
        "init_v_byte_equal": init_v_equal,
        "init_bias_byte_equal": init_bias_equal,
        "post_80step_spike_byte_equal": final_spike_equal,
        "post_80step_W_byte_equal": final_W_equal,
        "all_byte_equal": (init_W_equal and init_v_equal and init_bias_equal
                            and final_spike_equal and final_W_equal),
    }


def run_replicate(seed, n_a, n_g, n_rec, n_stim, steps=80, window=40):
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


def revalidate_s131():
    """Re-run §131 n_stim cardinality at N=256."""
    M = 5
    seeds = [1337 + r for r in range(M)]
    nstim_pts = [4, 12, 24, 48]
    results = []
    t0 = time.time()
    for nstim in nstim_pts:
        all_traces = np.zeros((nstim, M, 80), dtype=np.float64)
        for r_idx, seed in enumerate(seeds):
            trace = run_replicate(seed, 96, 96, 64, nstim)
            all_traces[:, r_idx, :] = trace
        pooled = all_traces.reshape(nstim, M * 80)
        decomp = E.variance_decomposition(pooled)
        results.append({"n_stim": nstim, "eta_squared": decomp["eta_squared"]})
        print(f"  §131-revalidate n_stim={nstim}: η² = {decomp['eta_squared']:.4f}",
              file=sys.stderr)
    return {"per_nstim_canonical": results, "wall_sec": time.time() - t0}


def revalidate_s133_subset():
    """Re-run §133 per-N at a subset of N points for speed.
    Use N ∈ {256, 1024} (skip 512/2048 which add ~6 min for marginal info).
    Capture per-replicate η² for SE comparison."""
    M = 5
    seeds = [1337 + r for r in range(M)]
    N_pts = [256, 1024]  # subset for speed
    results = []
    t0 = time.time()
    for N in N_pts:
        assert N % 8 == 0
        n_a = n_g = 3 * N // 8
        n_rec = N // 4
        per_rep = []
        pooled_traces = []
        for seed in seeds:
            trace = run_replicate(seed, n_a, n_g, n_rec, n_stim=12)
            per_rep.append(E.variance_decomposition(trace)["eta_squared"])
            pooled_traces.append(trace)
        pooled = np.array(pooled_traces).transpose(1, 0, 2).reshape(12, M * 80)
        pooled_decomp = E.variance_decomposition(pooled)
        eta = np.array(per_rep)
        results.append({
            "N_total": N,
            "per_replicate_eta_squared": per_rep,
            "pooled_eta_squared": pooled_decomp["eta_squared"],
            "eta_mean": float(eta.mean()),
            "eta_std": float(eta.std(ddof=1)),
        })
        print(f"  §133-revalidate N={N}: pooled η²={pooled_decomp['eta_squared']:.4f} "
              f"per-rep mean={float(eta.mean()):.4f}", file=sys.stderr)
    return {"per_N_canonical": results, "wall_sec": time.time() - t0}


def main():
    t_start = time.time()
    smoke = byte_equal_smoke()
    print(f"§134 byte-equal smoke: {smoke['all_byte_equal']}", file=sys.stderr)
    print("§134 revalidating §131 (n_stim axis)...", file=sys.stderr)
    s131_revalidated = revalidate_s131()
    print("§134 revalidating §133 subset (N axis, 2 points)...", file=sys.stderr)
    s133_revalidated = revalidate_s133_subset()

    # Compare to originals
    s127 = json.loads(S127_RESULT.read_text())
    s131 = json.loads(S131_RESULT.read_text())
    s133 = json.loads(S133_RESULT.read_text())

    # §127 was on §117 source (correct engine). Predict re-§131 at n_stim=12, N=256
    # should match §127's η² at N=256.
    s127_eta_256 = next(m["eta_squared"] for m in s127["per_N_measurements"] if m["N_total"] == 256)

    s131_orig_eta_12 = next(m["eta_squared"] for m in s131["per_nstim_measurements"]
                              if m["n_stim"] == 12)
    s131_revalidated_eta_12 = next(m["eta_squared"]
                                     for m in s131_revalidated["per_nstim_canonical"]
                                     if m["n_stim"] == 12)

    s133_orig_eta_256_pooled = next(m["pooled_eta_squared"]
                                      for m in s133["per_N_measurements"]
                                      if m["N_total"] == 256)
    s133_revalidated_eta_256_pooled = next(m["pooled_eta_squared"]
                                             for m in s133_revalidated["per_N_canonical"]
                                             if m["N_total"] == 256)

    drift_diagnostics = {
        "s127_eta_at_N256_n_stim_12 (correct, source-engine)": s127_eta_256,
        "s131_original_eta_at_n_stim_12 (drifted engine)": s131_orig_eta_12,
        "s133_original_eta_at_N256_pooled (drifted engine)": s133_orig_eta_256_pooled,
        "s131_revalidated_eta_at_n_stim_12 (canonical engine post-§134)": s131_revalidated_eta_12,
        "s133_revalidated_eta_at_N256_pooled (canonical engine post-§134)": s133_revalidated_eta_256_pooled,
        "drift_s131_to_canonical": abs(s131_orig_eta_12 - s131_revalidated_eta_12),
        "drift_s133_to_canonical": abs(s133_orig_eta_256_pooled - s133_revalidated_eta_256_pooled),
        "canonical_matches_s127_at_N256_within_1e_6 (s131-revalidated)":
            abs(s131_revalidated_eta_12 - s127_eta_256) < 1e-6,
        "canonical_matches_s127_at_N256_within_1e_6 (s133-revalidated)":
            abs(s133_revalidated_eta_256_pooled - s127_eta_256) < 1e-6,
    }

    result = {
        "section": "§134",
        "title": "LEGO ENGINE BYTE-EQUALITY RESTORE + §131/§133 RE-VALIDATION",
        "tier": "fix-tier + probe-tier (drift detected + restored + revalidated)",
        "cost_usd": 0.0,
        "gpu": False, "runpod": False, "fire": False,
        "model_forward_byte_lm": False, "corpus": False, "dispatch": False,
        "orphan": 0,
        "wall_sec_total": time.time() - t_start,
        "central_blue_falsifier_sha256_prefix16_expected": "c93e160a8a376a94",
        "parent": [
            "§133 detected drift between §127 pooled η² (0.271 at N=256) and §131/§133 measurement (0.218 at N=256)",
            "AST diff confirmed §129 promote of LIFNet was NOT byte-equal to §117 source",
        ],
        "byte_equal_smoke": smoke,
        "s131_revalidated": s131_revalidated,
        "s133_revalidated_subset": s133_revalidated,
        "drift_diagnostics": drift_diagnostics,
        "verdict": ("ENGINE-BYTE-EQUALITY-RESTORED-AND-VALIDATED" if (smoke["all_byte_equal"]
                     and drift_diagnostics["canonical_matches_s127_at_N256_within_1e_6 (s131-revalidated)"]
                     and drift_diagnostics["canonical_matches_s127_at_N256_within_1e_6 (s133-revalidated)"])
                    else "REVALIDATION-INCOMPLETE"),
        "g3": ("fix ≠ measurement ≠ fire ≠ emergence; capability claim 0; §131/§133 "
                "ORIGINAL measurements remain valid for the *drifted-engine substrate* "
                "as historical evidence in their state-dirs; §134 establishes that the "
                "canonical engine produces §127-byte-equal η² values."),
    }
    out = HERE / "result.json"
    out.write_text(json.dumps(result, indent=2, ensure_ascii=False))
    print(json.dumps({"verdict": result["verdict"],
                       "drift_diagnostics": drift_diagnostics,
                       "wall_sec": round(result["wall_sec_total"], 1)},
                      indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
