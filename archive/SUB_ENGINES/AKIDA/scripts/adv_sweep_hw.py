"""adv_sweep_hw.py — parameterized AKD1000 adversarial sweep companion.

Runs ONE regime on real silicon with caller-supplied seed/threshold/window and
emits the FULL per-step raster + a sha256 raster hash so HW vs SW can be diffed
bit-for-bit (Hamming distance) across the sweep envelope. Mirrors
spontaneous_emission.py regime semantics EXACTLY (same model, same all-ones
weights, same noise draw rng.integers(0,4), same recurrent feedback) but with
the operating point parameterized rather than hardcoded.

Usage:
  python adv_sweep_hw.py --regime R2 --seed 42 --threshold 24 --window 200 --repeat 3
Regimes: R0 R1 R2 R3 R4 (R2 is the only stochastic one — strongest jitter probe).
--repeat N runs the SAME config N times to expose run-to-run analog jitter.
Output: one JSON line per repeat to stdout (raster_sha256 + spike_counts + stats).
"""
import argparse
import hashlib
import json
import sys
import time

import numpy as np
import akida

N = 16
IN = 16


def build_model():
    dev = akida.devices()[0]
    model = akida.Model()
    model.add(akida.InputData(input_shape=(1, 1, IN), input_bits=4, name="in"))
    model.add(akida.FullyConnected(units=N, weights_bits=4, activation=True,
                                   act_bits=1, name="lif"))
    model.map(dev)
    lif = model.get_layer("lif")
    W = lif.get_variable("weights")
    lif.set_variable("weights", np.ones_like(W))
    backend = str(model.sequences[0].backend)
    return model, lif, backend


def spike_decision(model, lif, input_vec, threshold_vec):
    lif.set_variable("threshold", threshold_vec.astype(np.int32))
    x = np.clip(input_vec, 0, 15).astype(np.uint8).reshape(1, 1, 1, IN)
    y = model.forward(x)
    return (y.reshape(-1) > 0).astype(np.int8)[:N]


def isi_stats(spike_counts):
    fire = [i for i, c in enumerate(spike_counts) if c > 0]
    isis = [fire[i + 1] - fire[i] for i in range(len(fire) - 1)]
    if not isis:
        return {"n_fire_steps": len(fire), "isi_mean": None,
                "isi_min": None, "isi_max": None}
    return {"n_fire_steps": len(fire),
            "isi_mean": round(float(np.mean(isis)), 3),
            "isi_min": int(min(isis)), "isi_max": int(max(isis))}


def run_one(model, lif, regime, seed, threshold, window):
    """One full window for a regime. rng is RE-SEEDED per run (matches SW)."""
    rng = np.random.default_rng(seed)
    thr_het = np.where(np.arange(N) % 2 == 0, -1, 8).astype(np.int32)
    spike_counts = []
    last = np.zeros(N, dtype=np.int8)
    t0 = time.perf_counter()
    for step in range(window):
        if regime == "R0":
            thr = np.full(N, threshold, dtype=np.int32)
            inp = np.full(IN, 15.0)
        elif regime == "R1":
            thr = np.full(N, threshold, dtype=np.int32)
            inp = np.full(IN, 1.0)
        elif regime == "R2":
            thr = np.full(N, threshold, dtype=np.int32)
            inp = rng.integers(0, 4, size=IN).astype(np.float32)
        elif regime == "R3":
            thr = thr_het
            inp = np.zeros(IN, dtype=np.float32)
        elif regime == "R4":
            thr = thr_het
            fb = last.astype(np.float32)
            base = np.zeros(IN, dtype=np.float32)
            k = min(N, IN)
            base[:k] = fb[:k] * 3.0
            if step < 2:
                base[:k] += 6.0
            inp = base
        else:
            raise ValueError(regime)
        sp = spike_decision(model, lif, inp, thr)
        spike_counts.append(int(sp.sum()))
        last = sp
    t1 = time.perf_counter()
    raster = ",".join(str(c) for c in spike_counts)
    h = hashlib.sha256(raster.encode()).hexdigest()[:16]
    total = int(sum(spike_counts))
    return {
        "regime": regime, "seed": seed, "threshold": threshold,
        "window": window, "side": "HW",
        "raster_sha256": h,
        "total_spikes": total,
        "rate": round(total / float(N * window), 5),
        "std": round(float(np.std(spike_counts)), 4),
        "min": int(min(spike_counts)), "max": int(max(spike_counts)),
        "step_varies": bool(np.std(spike_counts) > 1e-9),
        "isi": isi_stats(spike_counts),
        "first10": spike_counts[:10], "last10": spike_counts[-10:],
        "wall_ms_per_step": round((t1 - t0) / window * 1000.0, 4),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--regime", required=True, choices=["R0", "R1", "R2", "R3", "R4"])
    ap.add_argument("--seed", type=int, default=187)
    ap.add_argument("--threshold", type=int, default=24)
    ap.add_argument("--window", type=int, default=200)
    ap.add_argument("--repeat", type=int, default=1)
    a = ap.parse_args()
    model, lif, backend = build_model()
    on_hw = "Hardware" in backend
    for r in range(a.repeat):
        rec = run_one(model, lif, a.regime, a.seed, a.threshold, a.window)
        rec["backend"] = backend
        rec["on_hardware"] = on_hw
        rec["repeat_idx"] = r
        print(json.dumps(rec))
        sys.stdout.flush()


if __name__ == "__main__":
    main()
