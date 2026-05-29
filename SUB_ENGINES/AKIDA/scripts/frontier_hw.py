"""frontier_hw.py — AKD1000 frontier-envelope probe (act_bits / weights / layers).

Round-3 FRONTIER of the HW<->SW calibration loop. The act_bits=1 envelope is
already proven byte-identical (adv_sweep). This script deliberately enters the
"NOT claimed" envelope where the SW model was INCOMPLETE:

  --axis actbits  : single FullyConnected with act_bits in {1,2,4}, all-ones
                    weights, GRADED integer inputs. Captures the RAW multi-level
                    activation y (NOT thresholded to 0/1) so the multi-bit
                    quantization behaviour is visible.
  --axis weights  : single FC, weights_bits=4, RANDOM int4 weight matrix
                    (seed-fixed), graded inputs -> quantized weighted sum.
  --axis layers   : 2 stacked FullyConnected, random int4 weights, act_bits=4
                    -> cascade quantization across layers.

Emits the FULL raw activation tensor per probe-input + a sha256 so HW vs SW can
be diffed exactly. Mirrors first_inference.py model-build style. One JSON line
per probe input to stdout.

Usage:
  python frontier_hw.py --axis actbits --act-bits 2
  python frontier_hw.py --axis weights --weights-bits 4 --wseed 7
  python frontier_hw.py --axis layers  --act-bits 4 --wseed 7
"""
import argparse
import hashlib
import json
import sys

import numpy as np
import akida

IN = 16
N = 16


def probe_inputs(in_dim, max_val):
    """Deterministic graded probe set spanning the input quantization range."""
    rng = np.random.default_rng(2026)
    xs = []
    xs.append(np.zeros(in_dim, dtype=np.uint8))
    xs.append(np.full(in_dim, max_val, dtype=np.uint8))
    xs.append((np.arange(in_dim) % (max_val + 1)).astype(np.uint8))
    for _ in range(7):
        xs.append(rng.integers(0, max_val + 1, size=in_dim).astype(np.uint8))
    return xs


def sha(arr):
    return hashlib.sha256(arr.astype(np.int64).tobytes()).hexdigest()[:16]


def build_actbits(dev, act_bits):
    m = akida.Model()
    m.add(akida.InputData(input_shape=(1, 1, IN), input_bits=4, name="in"))
    m.add(akida.FullyConnected(units=N, weights_bits=4, activation=True,
                               act_bits=act_bits, name="fc"))
    m.map(dev)
    fc = m.get_layer("fc")
    W = fc.get_variable("weights")
    fc.set_variable("weights", np.ones_like(W))
    # threshold low so graded potentials survive into the activation quantizer
    try:
        fc.set_variable("threshold", np.zeros(N, dtype=np.int32))
    except Exception:  # noqa: BLE001
        pass
    return m


def build_weights(dev, weights_bits, wseed, act_bits):
    m = akida.Model()
    m.add(akida.InputData(input_shape=(1, 1, IN), input_bits=4, name="in"))
    m.add(akida.FullyConnected(units=N, weights_bits=weights_bits,
                               activation=True, act_bits=act_bits, name="fc"))
    m.map(dev)
    fc = m.get_layer("fc")
    W = fc.get_variable("weights")
    rng = np.random.default_rng(wseed)
    lim = 2 ** (weights_bits - 1)
    Wr = rng.integers(-lim, lim, size=W.shape).astype(W.dtype)
    fc.set_variable("weights", Wr)
    try:
        fc.set_variable("threshold", np.zeros(N, dtype=np.int32))
    except Exception:  # noqa: BLE001
        pass
    return m, Wr


def build_layers(dev, weights_bits, wseed, act_bits):
    m = akida.Model()
    m.add(akida.InputData(input_shape=(1, 1, IN), input_bits=4, name="in"))
    m.add(akida.FullyConnected(units=N, weights_bits=weights_bits,
                               activation=True, act_bits=act_bits, name="fc1"))
    m.add(akida.FullyConnected(units=N, weights_bits=weights_bits,
                               activation=True, act_bits=act_bits, name="fc2"))
    m.map(dev)
    rng = np.random.default_rng(wseed)
    lim = 2 ** (weights_bits - 1)
    ws = {}
    for nm in ("fc1", "fc2"):
        fc = m.get_layer(nm)
        W = fc.get_variable("weights")
        Wr = rng.integers(-lim, lim, size=W.shape).astype(W.dtype)
        fc.set_variable("weights", Wr)
        ws[nm] = Wr
        try:
            fc.set_variable("threshold", np.zeros(N, dtype=np.int32))
        except Exception:  # noqa: BLE001
            pass
    return m, ws


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--axis", required=True, choices=["actbits", "weights", "layers"])
    ap.add_argument("--act-bits", type=int, default=2)
    ap.add_argument("--weights-bits", type=int, default=4)
    ap.add_argument("--wseed", type=int, default=7)
    a = ap.parse_args()
    dev = akida.devices()[0]
    meta = {"axis": a.axis, "act_bits": a.act_bits,
            "weights_bits": a.weights_bits, "wseed": a.wseed,
            "device": str(dev.version)}

    if a.axis == "actbits":
        m = build_actbits(dev, a.act_bits)
        ws_sha = None
    elif a.axis == "weights":
        m, Wr = build_weights(dev, a.weights_bits, a.wseed, a.act_bits)
        ws_sha = sha(Wr)
    else:
        m, ws = build_layers(dev, a.weights_bits, a.wseed, a.act_bits)
        ws_sha = sha(np.concatenate([ws["fc1"].ravel(), ws["fc2"].ravel()]))
    meta["weights_sha256"] = ws_sha
    meta["backend"] = str(m.sequences[0].backend)
    meta["on_hardware"] = "Hardware" in meta["backend"]
    print(json.dumps({"meta": meta}))
    sys.stdout.flush()

    for idx, x in enumerate(probe_inputs(IN, 15)):
        xin = x.reshape(1, 1, 1, IN).astype(np.uint8)
        y = m.forward(xin).reshape(-1)[:N].astype(np.int64)
        rec = {"side": "HW", "axis": a.axis, "input_idx": idx,
               "input_sha": sha(x), "y": y.tolist(),
               "y_sha256": sha(y), "y_max": int(y.max()), "y_min": int(y.min()),
               "n_levels": int(len(np.unique(y)))}
        print(json.dumps(rec))
        sys.stdout.flush()


if __name__ == "__main__":
    main()
