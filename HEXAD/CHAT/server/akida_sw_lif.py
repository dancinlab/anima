#!/usr/bin/env python3
"""akida_sw_lif.py — numpy LIF simulator mirroring akida.FullyConnected.forward().

Software fallback for the AKIDA AKD1000 substrate when no BrainChip device is
reachable (no `akida` package OR empty `akida.devices()`). The interface and the
integer threshold-and-fire semantics match the on-chip FullyConnected layer used
by SUB_ENGINES/AKIDA/scripts/spontaneous_emission.py:

  - input  x : uint8[1, 1, 1, IN]  (values clipped to [0, 15], input_bits=4)
  - weights  : all-ones excitatory  -> potential(unit_j) = sum_i x_i  (IN-independent of j)
  - threshold: per-unit int32        -> spike iff potential > threshold  (act_bits=1)
  - output   : int8 spikes[:N]       (0/1 per neuron)

This is a deterministic replay of the same on-chip decision (potential > thr),
NOT a learned model — seed=187 fixes the noise regimes so SW results are
byte-stable and match the canonical HW raster regime structure (R0..R4).

CALIBRATION (HW-SW loop round 1, 2026-05-29): the per-regime record now reports
the SAME derived statistics the on-chip script emits (isi_min/isi_max +
first10/last10 step-count rasters + wall_ms_per_step), so HW-vs-SW can be diffed
on the FULL distribution surface (ISI tails + raster head/tail), not just the
summary rate/std. The added fields are computed by the SAME formula as
spontaneous_emission.py — derived measurements, NOT hardcoded HW numbers. A
step-by-step replay against live AKD1000 silicon (seed=187, n=16, 200 steps)
showed the SW R2 raster is BYTE-IDENTICAL to the HW raster (first10/last10/
fire-step count all exact), and the HW is fully deterministic across separate
invocations (no analog jitter at this seed) — so the model fidelity was already
complete; this round closes the REPORTING-surface gap that prevented the ISI-tail
and raster diffs from being computed at all.
"""
from __future__ import annotations

import time

import numpy as np

SEED = 187          # deterministic — matches spontaneous_emission.py SEED
N = 16              # neurons in the LIF pool (one NP)
IN = 16             # input lines
T = 200             # steps per regime window


def lif_forward(x, threshold_vec, n=N):
    """One forward pass, matching akida FullyConnected(units=n).forward(x).

    potential(unit_j) = sum_i clip(x_i, 0, 15)   (all-ones weights)
    spike(unit_j)     = 1 if potential > threshold_vec[j] else 0   (int compare)

    Returns int8 spikes[:n] — identical signature/semantics to the chip path's
    `(y.reshape(-1) > 0).astype(np.int8)[:N]`.
    """
    xv = np.clip(np.asarray(x).reshape(-1), 0, 15).astype(np.uint8)
    potential = int(xv.sum())                       # IN-independent of unit
    thr = np.asarray(threshold_vec, dtype=np.int32).reshape(-1)[:n]
    spikes = (potential > thr).astype(np.int8)
    return spikes[:n]


def _isi_stats(spike_counts):
    """Population inter-spike intervals — gaps between steps that had >=1 spike.

    Mirrors spontaneous_emission._isi_stats EXACTLY (same fire-step list, same
    consecutive-difference ISI, same min/mean/max) so HW and SW ISI distributions
    are diffable on the tails (isi_min / isi_max), not only the mean.
    """
    fire_steps = [i for i, c in enumerate(spike_counts) if c > 0]
    isis = [fire_steps[i + 1] - fire_steps[i] for i in range(len(fire_steps) - 1)]
    if not isis:
        return {"n_fire_steps": len(fire_steps), "isi_mean": None,
                "isi_min": None, "isi_max": None}
    return {"n_fire_steps": len(fire_steps),
            "isi_mean": round(float(np.mean(isis)), 3),
            "isi_min": int(min(isis)), "isi_max": int(max(isis))}


def run_regime(name, threshold_const, input_fn,
               recurrent=False, threshold_vec=None,
               recur_gain=3.0, recur_seed_steps=2, t=T):
    """Run T steps of one regime — mirrors spontaneous_emission.run_regime().

    The returned record carries the SAME keys the on-chip script emits so a HW-vs-
    SW diff covers the full distribution surface:
      - first10_step_counts / last10_step_counts : raster head/tail (event-driven
        evidence; for R2 these are the stochastic 0/16 all-or-nothing steps).
      - wall_ms_per_step : SW pure-compute time (INFORMATIONAL — it will NOT match
        the HW ~13.7 ms/step which includes chip I/O; recorded for completeness,
        never a convergence target).
    """
    if threshold_vec is not None:
        thr = np.asarray(threshold_vec, dtype=np.int32)
    else:
        thr = np.full(N, threshold_const, dtype=np.int32)
    spike_counts = []
    last_spikes = np.zeros(N, dtype=np.int8)
    t0 = time.perf_counter()
    for step in range(t):
        if recurrent:
            fb = last_spikes.astype(np.float32)
            base = np.zeros(IN, dtype=np.float32)
            k = min(N, IN)
            base[:k] = fb[:k] * recur_gain
            if step < recur_seed_steps:
                base[:k] += 6.0
            inp = base
        else:
            inp = input_fn(step)
        sp = lif_forward(inp, thr)
        spike_counts.append(int(sp.sum()))
        last_spikes = sp
    t1 = time.perf_counter()
    total = int(sum(spike_counts))
    rate = total / float(N * t)
    return {
        "threshold_const": int(threshold_const),
        "recurrent": recurrent,
        "total_spikes": total,
        "mean_spike_rate_per_neuron_step": round(rate, 5),
        "spike_count_min": int(min(spike_counts)),
        "spike_count_max": int(max(spike_counts)),
        "spike_count_std": round(float(np.std(spike_counts)), 4),
        "step_varies": bool(np.std(spike_counts) > 1e-9),
        "first10_step_counts": spike_counts[:10],
        "last10_step_counts": spike_counts[-10:],
        "isi": _isi_stats(spike_counts),
        "wall_ms_per_step": round((t1 - t0) / t * 1000.0, 4),
    }


def simulate_regimes(seed=SEED):
    """Reproduce the R0..R4 regimes of spontaneous_emission.py in pure numpy.

    Deterministic (seed=187). Returns a dict mirroring the canonical raster:
    {"seed", "n_neurons", "n_inputs", "window_steps", "regimes": {R0..R4}, ...}.
    """
    rng = np.random.default_rng(seed)
    out = {"seed": seed, "n_neurons": N, "n_inputs": IN,
           "window_steps": T, "backend": "sw-numpy-lif", "regimes": {}}

    # R0 driven: strong input (all 15s), high threshold -> fires every step.
    out["regimes"]["R0_driven"] = run_regime(
        "R0_driven", 64, lambda s: np.full(IN, 15.0))
    # R1 weak: weak constant input (all 1s -> potential 16), thr 64 -> SILENT.
    out["regimes"]["R1_weak_silent"] = run_regime(
        "R1_weak_silent", 64, lambda s: np.full(IN, 1.0))
    # R2 zero+noise: U[0,4) noise per line, thr 24 at the mean -> ~half cross.
    out["regimes"]["R2_zero_noise"] = run_regime(
        "R2_zero_noise", 24, lambda s: rng.integers(0, 4, size=IN).astype(np.float32))
    # R3 tonic-zero: ZERO input + heterogeneous threshold (half -1 tonic, half +8).
    thr_het = np.where(np.arange(N) % 2 == 0, -1, 8).astype(np.int32)
    out["regimes"]["R3_tonic_zero_input"] = run_regime(
        "R3_tonic_zero_input", 0, lambda s: np.zeros(IN, dtype=np.float32),
        threshold_vec=thr_het)
    # R4 recurrent: heterogeneous tonic pool + spikes fed back as next input.
    out["regimes"]["R4_recurrent_selfsustained"] = run_regime(
        "R4_recurrent_selfsustained", 0, lambda s: np.zeros(IN),
        threshold_vec=thr_het, recurrent=True, recur_gain=3.0, recur_seed_steps=2)
    return out


if __name__ == "__main__":
    import json
    print(json.dumps(simulate_regimes(), indent=2))
