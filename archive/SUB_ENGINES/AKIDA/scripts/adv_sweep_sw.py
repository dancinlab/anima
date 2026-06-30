"""adv_sweep_sw.py — parameterized SW numpy-LIF adversarial sweep companion.

The exact SW counterpart of adv_sweep_hw.py: same regime semantics, same
default_rng(seed) noise stream, same all-ones-weights integer threshold
comparator (potential = Σ clip(x,0,15); spike iff potential > threshold), same
recurrent feedback. Emits the SAME JSON-line schema + raster_sha256 so the diff
tool can compute HW-vs-SW raster Hamming distance per operating point.

This is a generalizing parameterization of AGENT/CHAT/akida_sw_lif.py's
lif_forward + run_regime — NOT a per-point hardcode. Run with identical
--regime/--seed/--threshold/--window args as the HW side.
"""
import argparse
import hashlib
import json
import time

import numpy as np

N = 16
IN = 16


def lif_forward(x, threshold_vec):
    xv = np.clip(np.asarray(x).reshape(-1), 0, 15).astype(np.uint8)
    potential = int(xv.sum())
    thr = np.asarray(threshold_vec, dtype=np.int32).reshape(-1)[:N]
    return (potential > thr).astype(np.int8)[:N]


def isi_stats(spike_counts):
    fire = [i for i, c in enumerate(spike_counts) if c > 0]
    isis = [fire[i + 1] - fire[i] for i in range(len(fire) - 1)]
    if not isis:
        return {"n_fire_steps": len(fire), "isi_mean": None,
                "isi_min": None, "isi_max": None}
    return {"n_fire_steps": len(fire),
            "isi_mean": round(float(np.mean(isis)), 3),
            "isi_min": int(min(isis)), "isi_max": int(max(isis))}


def run_one(regime, seed, threshold, window):
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
        sp = lif_forward(inp, thr)
        spike_counts.append(int(sp.sum()))
        last = sp
    t1 = time.perf_counter()
    raster = ",".join(str(c) for c in spike_counts)
    h = hashlib.sha256(raster.encode()).hexdigest()[:16]
    total = int(sum(spike_counts))
    return {
        "regime": regime, "seed": seed, "threshold": threshold,
        "window": window, "side": "SW",
        "raster_sha256": h,
        "total_spikes": total,
        "rate": round(total / float(N * window), 5),
        "std": round(float(np.std(spike_counts)), 4),
        "min": int(min(spike_counts)), "max": int(max(spike_counts)),
        "step_varies": bool(np.std(spike_counts) > 1e-9),
        "isi": isi_stats(spike_counts),
        "first10": spike_counts[:10], "last10": spike_counts[-10:],
        "wall_ms_per_step": round((t1 - t0) / window * 1000.0, 4),
        "backend": "sw-numpy-lif", "on_hardware": False,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--regime", required=True, choices=["R0", "R1", "R2", "R3", "R4"])
    ap.add_argument("--seed", type=int, default=187)
    ap.add_argument("--threshold", type=int, default=24)
    ap.add_argument("--window", type=int, default=200)
    ap.add_argument("--repeat", type=int, default=1)
    a = ap.parse_args()
    for r in range(a.repeat):
        rec = run_one(a.regime, a.seed, a.threshold, a.window)
        rec["repeat_idx"] = r
        print(json.dumps(rec))


if __name__ == "__main__":
    main()
