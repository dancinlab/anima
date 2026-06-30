"""H_927 — stochastic resonance sweep on the live AKD1000 (pi5-akida, $0).

QUESTION
--------
H_677 D1 found an edge-of-chaos Φ inverse-U ACROSS regimes (R1=0.000 silent,
R2=0.297 PEAK noise-straddle, R3=0.250 tonic, R4=0.000 saturated). H_927 asks
the sharper WITHIN-R2 question: holding everything else fixed, sweep the R2
NOISE AMPLITUDE and measure the same Φ-proxy at each level. Stochastic
resonance predicts a NON-MONOTONIC (inverse-U) response to noise amplitude:
  - too little noise  → mean potential << threshold → never crosses → silent → low Φ
  - too much noise    → mean potential >> threshold → always crosses → saturates → low Φ
  - a middle sweet spot (mean ≈ threshold) → ~half the steps cross → high Φ.

SWEEP AXIS (honest disclosure)
------------------------------
The R2 noise in spontaneous_emission.py is `rng.integers(0, 4)` per input line
(values 0..3, mean 1.5) over IN=16 lines, with threshold_const=24. We sweep the
upper bound K of `rng.integers(0, K)` (values 0..K-1, mean (K-1)/2). The mean
on-chip integrated potential is POT(K) = IN * (K-1)/2 = 16 * (K-1)/2 = 8*(K-1).
Threshold is held FIXED at 24. So:
  K=2  -> POT=8   (deep sub-threshold, silent floor)
  K=3  -> POT=16  (below threshold)
  K=4  -> POT=24  (== threshold, the canonical R2 straddle)  <- H_677 baseline
  K=6  -> POT=40  (above threshold)
  K=8  -> POT=56  (well above)
  K=12 -> POT=88  (saturating)
  K=16 -> POT=120 (input clipped to 15 -> heavy saturation)
This sweeps the mean-vs-threshold GAP from -16 (K=2) through 0 (K=4) to +96 (K=16),
crossing the straddle point exactly at K=4. Resonance peak (if any) is expected
near K=4 where POT==threshold.

Φ-PROXY (honest: NOT full IIT4 big_phi)
---------------------------------------
We reuse the repo's `phi_silicon_proxy` (AKIDA/akida_edge_of_chaos_phi.hexa),
mirrored byte-for-byte in Python here so the swept Φ is directly comparable to
the H_677 R2=0.2974 baseline. It is:
  phi = activity_gate * (integration * differentiation) * (0.5 + 0.5*H_entropy)
where entropy/integration use the first10+last10 step-count surrogate (20
samples) and differentiation uses spike_count_std + spike_count_max, exactly as
the .hexa harness consumes from spontaneous_emission.py. This is an INTEGRATION-
aware proxy (not just spike count): a saturated regime (all neurons fire every
step) has differentiation->0 hence Φ->0 despite max spike count.

HONEST SCOPE (a_scale_honest_scope): 1 AKD1000, N=16 neuron toy pool, T=200
steps, byte-quantised R2 noise, Φ-PROXY not full IIT Φ. Toy probe. deterministic:
false (R2 noise stochastic; numpy PRNG seed fixed per level for reproducibility).
"""
import json
import math
import sys
import time

import numpy as np
import akida

SEED = 187
N = 16          # neurons in the LIF pool (one NP) -- matches spontaneous_emission.py
IN = 16         # input lines
T = 200         # steps per level window
THRESHOLD = 24  # FIXED R2 threshold_const (held constant across the sweep)

# noise upper bound K sweep -- rng.integers(0, K) per line. ~7 levels.
K_LEVELS = [2, 3, 4, 6, 8, 12, 16]


# ── Φ-proxy: byte-for-byte mirror of akida_edge_of_chaos_phi.hexa ────────────
def _log2_safe(x):
    if x <= 0.0:
        return 0.0
    return math.log(x) / math.log(2.0)


def _shannon_entropy_normalized(counts, n_steps):
    if n_steps <= 1:
        return 0.0
    n_bins = 5
    mx = 0
    for c in counts:
        if c > mx:
            mx = c
    if mx == 0:
        return 0.0
    hist = [0] * n_bins
    span = mx + 1
    for c in counts:
        bin_idx = (c * n_bins) // span
        if bin_idx >= n_bins:
            bin_idx = n_bins - 1
        hist[bin_idx] += 1
    total = float(len(counts))
    h = 0.0
    for b in range(n_bins):
        p = hist[b] / total
        if p > 0.0:
            h -= p * _log2_safe(p)
    return h / _log2_safe(n_bins + 0.0)


def _integration_proxy(first10, last10):
    m1 = sum(first10) / float(len(first10))
    m2 = sum(last10) / float(len(last10))
    denom = m1 if m1 > m2 else m2
    if denom <= 0.0:
        return 0.0
    absdiff = abs(m1 - m2)
    return 1.0 - (absdiff / (denom + 1e-9))


def _differentiation_proxy(spike_count_std, spike_count_max, n_neurons):
    if spike_count_max <= 0:
        return 0.0
    p = (spike_count_max + 0.0) / (n_neurons + 0.0)
    structural = 4.0 * p * (1.0 - p)
    temporal_raw = spike_count_std / ((n_neurons + 0.0) / 4.0)
    temporal = 1.0 if temporal_raw > 1.0 else temporal_raw
    return (structural + temporal) / 2.0


def phi_silicon_proxy(first10, last10, spike_count_std, spike_count_max,
                      n_neurons, n_steps, total_spikes):
    combined = list(first10) + list(last10)
    h = _shannon_entropy_normalized(combined, len(combined))
    intg = _integration_proxy(first10, last10)
    diff = _differentiation_proxy(spike_count_std, spike_count_max, n_neurons)
    act_raw = (total_spikes + 0.0) / ((n_neurons + 0.0) * (n_steps + 0.0) * 0.05)
    activity_gate = 1.0 if act_raw > 1.0 else act_raw
    core = intg * diff
    entropy_weight = 0.5 + 0.5 * h
    phi = activity_gate * core * entropy_weight
    order = (total_spikes + 0.0) / (n_neurons * n_steps + 0.0)
    return {
        "phi_silicon_proxy": phi,
        "axis_entropy": h,
        "axis_integration": intg,
        "axis_differentiation": diff,
        "activity_gate": activity_gate,
        "entropy_weight": entropy_weight,
        "core_int_x_diff": core,
        "order_param": order,
    }


# ── device + model (built ONCE, reused for every level) ──────────────────────
def build_model(dev):
    model = akida.Model()
    model.add(akida.InputData(input_shape=(1, 1, IN), input_bits=4, name="in"))
    model.add(akida.FullyConnected(units=N, weights_bits=4, activation=True,
                                   act_bits=1, name="lif"))
    model.map(dev)
    lif = model.get_layer("lif")
    W = lif.get_variable("weights")
    lif.set_variable("weights", np.ones_like(W))     # all-ones excitatory
    return model, lif


def spike_decision_on_chip(model, lif, input_vec, threshold_vec):
    lif.set_variable("threshold", threshold_vec.astype(np.int32))
    x = np.clip(input_vec, 0, 15).astype(np.uint8).reshape(1, 1, 1, IN)
    y = model.forward(x)
    return (y.reshape(-1) > 0).astype(np.int8)[:N]


def run_r2_level(model, lif, K, rng):
    """Run T steps of R2 with noise rng.integers(0, K), threshold fixed."""
    thr = np.full(N, THRESHOLD, dtype=np.int32)
    spike_counts = []
    for _ in range(T):
        inp = rng.integers(0, K, size=IN).astype(np.float32)
        sp = spike_decision_on_chip(model, lif, inp, thr)
        spike_counts.append(int(sp.sum()))
    total = int(sum(spike_counts))
    arr = np.array(spike_counts)
    return {
        "K": K,
        "pot_mean": 8.0 * (K - 1),                 # IN*(K-1)/2
        "threshold": THRESHOLD,
        "gap_pot_minus_thr": 8.0 * (K - 1) - THRESHOLD,
        "total_spikes": total,
        "mean_spike_rate_per_neuron_step": round(total / float(N * T), 5),
        "spike_count_min": int(arr.min()),
        "spike_count_max": int(arr.max()),
        "spike_count_std": round(float(arr.std()), 4),
        "first10_step_counts": spike_counts[:10],
        "last10_step_counts": spike_counts[-10:],
    }


def main():
    out = {
        "hypothesis": "H_927",
        "title": "R2 noise-amplitude stochastic-resonance Φ sweep",
        "seed": SEED, "n_neurons": N, "n_inputs": IN, "window_steps": T,
        "threshold_fixed": THRESHOLD,
        "phi_method": "phi_silicon_proxy (entropy x integration x differentiation; "
                      "honest proxy NOT full IIT4 big_phi; mirror of "
                      "AKIDA/akida_edge_of_chaos_phi.hexa)",
        "sweep_axis": "K = upper bound of rng.integers(0,K) per input line; "
                      "mean potential = IN*(K-1)/2 = 8*(K-1); threshold fixed at 24",
        "deterministic": False,
        "noise_source": "numpy_prng (seed 187, reseeded per level)",
        "k_levels": K_LEVELS,
        "levels": [],
    }
    dev = akida.devices()[0]
    out["device_version"] = str(dev.version)
    out["device_ip_version"] = str(dev.ip_version)
    model, lif = build_model(dev)
    out["mapped_backend"] = str(model.sequences[0].backend)
    out["mapped_on_hardware"] = ("Hardware" in out["mapped_backend"])

    for K in K_LEVELS:
        rng = np.random.default_rng(SEED)   # reseed per level => reproducible
        rec = run_r2_level(model, lif, K, rng)
        phi = phi_silicon_proxy(
            rec["first10_step_counts"], rec["last10_step_counts"],
            rec["spike_count_std"], rec["spike_count_max"],
            N, T, rec["total_spikes"])
        rec.update(phi)
        out["levels"].append(rec)
        print(f"K={K:2d} POT={rec['pot_mean']:5.1f} gap={rec['gap_pot_minus_thr']:+6.1f} "
              f"rate={rec['mean_spike_rate_per_neuron_step']:.4f} "
              f"std={rec['spike_count_std']:.3f} "
              f"phi={rec['phi_silicon_proxy']:.4f}", flush=True)

    # ── resonance verdict (pre-registered, no shaping) ──────────────────────
    phis = [lv["phi_silicon_proxy"] for lv in out["levels"]]
    peak_i = int(np.argmax(phis))
    peak_K = K_LEVELS[peak_i]
    n = len(phis)
    # inverse-U: peak strictly interior AND > first AND > last level.
    interior = 0 < peak_i < n - 1
    inverse_u = interior and (phis[peak_i] > phis[0]) and (phis[peak_i] > phis[-1])
    out["verdict"] = {
        "phi_by_level": {str(K_LEVELS[i]): phis[i] for i in range(n)},
        "peak_K": peak_K,
        "peak_phi": phis[peak_i],
        "peak_is_interior": interior,
        "phi_low": phis[0],
        "phi_high": phis[-1],
        "inverse_u_resonance": bool(inverse_u),
        "verdict": ("GREEN_RESONANCE_CONFIRMED" if inverse_u
                    else "RED_NO_RESONANCE_MONOTONIC_OR_FLAT"),
    }
    print("VERDICT:", json.dumps(out["verdict"]), flush=True)

    dst = sys.argv[1] if len(sys.argv) > 1 else "/tmp/h927_result.json"
    with open(dst, "w") as fh:
        json.dump(out, fh, indent=2)
    print("WROTE", dst, flush=True)


if __name__ == "__main__":
    main()
