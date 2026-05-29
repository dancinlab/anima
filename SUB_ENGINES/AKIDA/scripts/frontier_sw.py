"""frontier_sw.py -- SW model for the AKIDA frontier envelope (act_bits/weights/layers).

The act_bits=1 SW model (akida_sw_lif.lif_forward) collapses everything to a
1-bit threshold comparator: potential=sum(x); spike = potential>thr. That model
is INCOMPLETE for the frontier axes this script targets. Here we implement the
GENERAL akida FullyConnected forward as a quantized integer matmul + a graded
activation quantizer, parameterized by act_bits / weights / layer-count:

  potential_j = sum_i  x_i * W_ij                 (integer matmul, symmetric int4 W)
  y_j         = quantize_relu(potential_j, act_bits)

quantize_relu = ReLU then clamp to [0, 2^act_bits - 1] (the AKD1000 multi-bit
activation quantizer; act_bits=1 reduces to the old >0 comparator).

CALIBRATED HW constraints folded in (frontier round, 2026-05-29):
  - SYMMETRIC weights: int4 weights live in [-7,+7] (NOT [-8,+7]); the chip
    rejects the two's-complement min. rand_int_weights mirrors this.
  - akida weight LAYOUT is (1,1,IN,N); the rng draw uses that EXACT size+order
    so the SW weight tensor is byte-identical to the HW one for a given wseed.

Same probe_inputs + y_sha256 schema as frontier_hw.py for a bit-exact diff.

Usage (match the HW args exactly):
  python frontier_sw.py --axis actbits --act-bits 2
  python frontier_sw.py --axis weights --weights-bits 4 --wseed 7 --act-bits 2
  python frontier_sw.py --axis layers  --act-bits 4 --wseed 7
"""
import argparse
import hashlib
import json

import numpy as np

IN = 16
N = 16
WSHAPE = (1, 1, IN, N)   # akida FullyConnected weight layout


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


def rand_int_weights(rng, shape, weights_bits):
    """SYMMETRIC int weights [-(2^(b-1)-1), +(2^(b-1)-1)] -- mirrors AKD1000
    (rejects -2^(b-1)). Same draw size+order as the HW build for byte-match."""
    lim = (1 << (weights_bits - 1)) - 1
    return rng.integers(-lim, lim + 1, size=shape).astype(np.int64)


def quantize_relu(potential, act_bits, scale=1.0, input_bits=4):
    """AKD1000 graded activation quantizer -- CALIBRATED against AKD1000 silicon
    (frontier round, 2026-05-29).

    The chip does NOT clamp the raw integer potential to [0, 2^act_bits-1]
    (the naive act_bits=1 model). It quantizes the ReLU'd potential into
    2^act_bits levels with a STEP of 2^(input_bits - act_bits):

        step = 2^(input_bits - act_bits)
        act  = clip( ceil(potential / step), 0, 2^act_bits - 1 )

    Recovered step function (single-FC unit, weight*x0 sweep on AKD1000):
      act_bits=4 -> step 1  : pot 1->1, 2->2, ... 15->15, >=16 saturate (= naive clip)
      act_bits=2 -> step 4  : pot 0->0, 1..4->1, 5..8->2, 9..->3
      act_bits=1 -> step 8  : pot>0 -> 1 (= the old threshold comparator)
    `scale` (optional) overrides step = round(step/scale) for non-default chips.
    """
    p = np.maximum(np.asarray(potential, dtype=np.int64), 0)
    hi = (1 << act_bits) - 1
    step = 1 << (input_bits - act_bits)
    if scale != 1.0:
        step = max(1, int(round(step / scale)))
    act = -(-p // step)            # ceil division for non-negative p
    return np.clip(act, 0, hi).astype(np.int64)


def fc_forward(x, W, act_bits, scale=1.0):
    """potential_j = sum_i x_i * W[0,0,i,j]; W given in (1,1,IN,N) akida layout."""
    Wm = np.asarray(W).reshape(IN, N).astype(np.int64)
    potential = np.asarray(x).reshape(1, -1).astype(np.int64) @ Wm
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
    act_bits = a.act_bits
    meta = {"axis": a.axis, "act_bits": act_bits,
            "weights_bits": a.weights_bits, "wseed": a.wseed,
            "scale": a.scale, "backend": "sw-numpy-frontier"}

    W2 = None
    if a.axis == "actbits":
        W = np.ones(WSHAPE, dtype=np.int64)
        ws_sha = None
    elif a.axis == "weights":
        rng = np.random.default_rng(a.wseed)
        W = rand_int_weights(rng, WSHAPE, a.weights_bits)
        ws_sha = sha(W)
    else:  # layers -- two FCs drawn from ONE rng stream (matches HW build order)
        rng = np.random.default_rng(a.wseed)
        W = rand_int_weights(rng, WSHAPE, a.weights_bits)
        W2 = rand_int_weights(rng, WSHAPE, a.weights_bits)
        ws_sha = sha(np.concatenate([W.ravel(), W2.ravel()]))
    meta["weights_sha256"] = ws_sha
    print(json.dumps({"meta": meta}))

    for idx, x in enumerate(probe_inputs(IN, 15)):
        if a.axis == "layers":
            h = fc_forward(x, W, act_bits, a.scale)
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
