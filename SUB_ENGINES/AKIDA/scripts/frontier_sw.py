"""frontier_sw.py — SW model for the AKIDA frontier envelope (act_bits/weights/layers).

The act_bits=1 SW model (akida_sw_lif.lif_forward) collapses everything to a
1-bit threshold comparator: potential=Σx; spike = potential>thr. That model is
INCOMPLETE for the frontier axes this script targets. Here we implement the
GENERAL akida FullyConnected forward as a quantized integer matmul + a graded
activation quantizer, parameterized by act_bits / weights / layer-count:

  potential_j = Σ_i  x_i * W_ij                 (integer matmul, signed int4 W)
  y_j         = quantize_relu(potential_j, act_bits)

where quantize_relu clamps to [0, 2^act_bits - 1] after ReLU (the AKD1000
multi-bit activation quantizer; act_bits=1 reduces to the old >0 comparator).
The exact integer scale factor the chip applies before clamping is the unknown
this script CALIBRATES against HW (frontier_hw.py) — see --scale.

Same probe_inputs + sha256 schema as frontier_hw.py for a bit-exact diff.

Usage (match the HW args exactly):
  python frontier_sw.py --axis actbits --act-bits 2
  python frontier_sw.py --axis weights --weights-bits 4 --wseed 7
  python frontier_sw.py --axis layers  --act-bits 4 --wseed 7
"""
import argparse
import hashlib
import json

import numpy as np

IN = 16
N = 16


def probe_inputs(in_dim, max_val):
    rng = np.random.default_rng(2026)
    xs = []
    xs.append(np.zeros(in_dim, dtype=np.uint8))
    xs.append(np.full(in_dim, max_val, dtype=np.uint8))
    xs.append((np.arange(in_dim) % (max_val + 1)).astype(np.uint8))
    for _ in range(7):
        xs.append(rng.integers(0, max_val + 1, size=in_dim).astype(np.uint8))
    return xs


def sha(arr):
    return hashlib.sha256(np.asarray(arr).astype(np.int64).tobytes()).hexdigest()[:16]


def quantize_relu(potential, act_bits, scale=1.0):
    """AKD1000 graded activation quantizer.

    ReLU then clamp to the act_bits range [0, 2^act_bits - 1]. `scale` is the
    per-step integer rescale the chip applies before clamping (calibrated vs HW).
    act_bits=1 => clamp to {0,1} == the old (potential>0) comparator.
    """
    p = np.maximum(potential, 0)
    if scale != 1.0:
        p = np.floor(p * scale).astype(np.int64)
    hi = (1 << act_bits) - 1
    return np.clip(p, 0, hi).astype(np.int64)


def random_weights(shape, weights_bits, wseed):
    rng = np.random.default_rng(wseed)
    lim = 2 ** (weights_bits - 1)
    return rng.integers(-lim, lim, size=shape).astype(np.int64)


def fc_forward(x, W, act_bits, scale=1.0):
    """W shape (1,1,IN,N) akida layout OR (IN,N). potential = x @ W."""
    Wm = np.asarray(W).reshape(IN, N) if np.asarray(W).size == IN * N else \
        np.asarray(W).reshape(-1, N)
    potential = np.asarray(x).reshape(1, -1).astype(np.int64) @ Wm.astype(np.int64)
    return quantize_relu(potential.reshape(-1), act_bits, scale)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--axis", required=True, choices=["actbits", "weights", "layers"])
    ap.add_argument("--act-bits", type=int, default=2)
    ap.add_argument("--weights-bits", type=int, default=4)
    ap.add_argument("--wseed", type=int, default=7)
    ap.add_argument("--scale", type=float, default=1.0,
                    help="activation pre-clamp rescale (calibrated vs HW)")
    a = ap.parse_args()
    meta = {"axis": a.axis, "act_bits": a.act_bits,
            "weights_bits": a.weights_bits, "wseed": a.wseed,
            "scale": a.scale, "backend": "sw-numpy-frontier"}

    if a.axis == "actbits":
        W = np.ones((IN, N), dtype=np.int64)
        ws_sha = None
        act_bits = a.act_bits
    elif a.axis == "weights":
        W = random_weights((IN, N), a.weights_bits, a.wseed)
        ws_sha = sha(W)
        act_bits = a.act_bits
    else:
        W1 = random_weights((IN, N), a.weights_bits, a.wseed * 1)
        # second draw continues the SAME rng stream as the HW layer build
        rng = np.random.default_rng(a.wseed)
        lim = 2 ** (a.weights_bits - 1)
        W1 = rng.integers(-lim, lim, size=(IN, N)).astype(np.int64)
        W2 = rng.integers(-lim, lim, size=(N, N)).astype(np.int64)
        ws_sha = sha(np.concatenate([W1.ravel(), W2.ravel()]))
        act_bits = a.act_bits
    meta["weights_sha256"] = ws_sha
    print(json.dumps({"meta": meta}))

    for idx, x in enumerate(probe_inputs(IN, 15)):
        if a.axis == "layers":
            h = fc_forward(x, W1, act_bits, a.scale)
            y = fc_forward(h, W2, act_bits, a.scale)
        else:
            y = fc_forward(x, W, act_bits, a.scale)
        rec = {"side": "SW", "axis": a.axis, "input_idx": idx,
               "input_sha": sha(x), "y": y.tolist(),
               "y_sha256": sha(y), "y_max": int(y.max()), "y_min": int(y.min()),
               "n_levels": int(len(np.unique(y)))}
        print(json.dumps(rec))


if __name__ == "__main__":
    main()
