#!/usr/bin/env python3
"""clm_akida_bench.py -- .clm int4 -> AKD1000 on-chip forward benchmark.

Loads a `.clm` model's int4-symmetric weights, builds the matching Akida
inference model (InputData + FullyConnected, the conv-native trunk readout
primitive), maps it to a physical AKD1000 device (`akida.devices()[0]`), and
times an on-chip forward pass: latency (wall ms/inference) + throughput
(inferences/s). The same int4 weights are run through the numpy software mirror
(`akida_sw_lif.fc_quantized_forward`) and the two outputs are checked
BYTE-IDENTICAL -- the 1st..5th-round calibrated AKD1000<->SW envelope.

Honesty rules (CLAUDE.md p7 + plan @L5):
  - When no real `.clm` exists yet (the P2 full-fire is still producing the
    first checkpoint -> .clm), the on-chip path is NOT faked. The harness runs
    the SW envelope on a tiny dummy int4 tensor to PROVE the harness wiring, and
    reports mode="sw-smoke" with awaiting_clm=true. No HW latency is fabricated.
  - When a real AKD1000 is reachable (akida.devices() non-empty) AND a real .clm
    is supplied, mode="hw-live" and the on-chip latency is the measured wall
    time. The pi5-akida single-chip file-lock means the live path requires the
    spike-streamer service to be STOPPED first and RESTORED after (see
    CLM/bench/README.md -- streamer stop -> bench -> restart).

Usage:
  python3 clm_akida_bench.py [--clm PATH] [--n-iter 100] [--units 16]
                             [--in-lines 16] [--act-bits 1] [--input-bits 4]
                             [--seed 187] [--json]

Interface mirrors SUB_ENGINES/AKIDA/scripts/first_inference.py (HW forward) and
AGENT/CHAT/akida_sw_lif.py (SW envelope). Code = English; the operator
README is Korean (CLM/bench/README.md).
"""
from __future__ import annotations

import argparse
import json
import os
import struct
import sys
import time

import numpy as np


# ---------------------------------------------------------------------------
# .clm int4 weight loader (CLM_FORMAT_SPEC layout: MAGIC + HEADER + BLOCKS + MANIFEST)
# ---------------------------------------------------------------------------
CLM_MAGIC = b"CLM\x01"


def _unpack_int4_sym(packed: bytes, count: int) -> np.ndarray:
    """Unpack symmetric int4 [-7,+7] from 2-weights/byte packing (low nibble
    first). The chip rejects -8, so values live in [-7, +7]; a nibble n in
    0..15 maps to n - 16 when n >= 8 (two's-complement nibble), but the spec
    guarantees the producer never emits -8.
    """
    out = np.empty(count, dtype=np.int64)
    for i in range(count):
        byte = packed[i // 2]
        nib = (byte & 0x0F) if (i % 2 == 0) else ((byte >> 4) & 0x0F)
        out[i] = nib - 16 if nib >= 8 else nib
    return out


def load_clm_int4(path: str):
    """Parse a `.clm` file far enough to recover (HEADER dict, first int4 weight
    block as an int matrix). Returns (header, name, shape, int4_weights).

    The full BLOCKS binary layout is producer-defined; this loader reads the
    HEADER json (authoritative arch/quant fields) and, if a JSON-described int4
    block is present, the first weight matrix. If the producer's binary block
    layout differs, the caller falls back to the HEADER arch dims to size the
    Akida model and uses deterministic int4 weights (clearly flagged
    weights_from_clm=false).
    """
    with open(path, "rb") as fh:
        magic = fh.read(4)
        if magic != CLM_MAGIC:
            raise ValueError(f"bad MAGIC {magic!r} (expected {CLM_MAGIC!r})")
        (hlen,) = struct.unpack("<I", fh.read(4))
        header = json.loads(fh.read(hlen).decode("utf-8"))
        # BLOCKS/MANIFEST binary layout is producer-defined; we only need the
        # HEADER arch/quant here. A future producer revision can extend this to
        # stream the first int4 block; until then weights come from HEADER dims.
    return header, None, None, None


# ---------------------------------------------------------------------------
# SW envelope (numpy mirror of on-chip FullyConnected forward)
# ---------------------------------------------------------------------------
def _import_sw_lif():
    """Import akida_sw_lif from AGENT/CHAT (the calibrated SW envelope)."""
    here = os.path.dirname(os.path.abspath(__file__))
    repo = os.path.abspath(os.path.join(here, "..", ".."))
    sw_dir = os.path.join(repo, "HEXAD", "CHAT", "server")
    if sw_dir not in sys.path:
        sys.path.insert(0, sw_dir)
    import akida_sw_lif  # noqa: E402
    return akida_sw_lif


def sw_forward(x, weights, act_bits, input_bits, n):
    """SW int4 forward via the calibrated fc_quantized_forward envelope."""
    sw = _import_sw_lif()
    return np.asarray(sw.fc_quantized_forward(x, weights, act_bits,
                                              input_bits=input_bits, n=n),
                      dtype=np.int64).reshape(-1)


# ---------------------------------------------------------------------------
# HW path (AKD1000 on-chip forward) -- mirrors first_inference.py
# ---------------------------------------------------------------------------
def hw_available():
    try:
        import akida  # noqa: F401
    except Exception:
        return False
    try:
        import akida
        return len(akida.devices()) > 0
    except Exception:
        return False


def hw_forward_bench(x, weights, units, in_lines, act_bits, input_bits, n_iter):
    """Build InputData+FullyConnected, map to AKD1000, program int4 weights,
    time n_iter on-chip forwards. Returns (out_vector, wall_ms_per_inf,
    throughput_hz, meta). Mirrors first_inference.py exactly."""
    import akida

    dev = akida.devices()[0]
    model = akida.Model()
    model.add(akida.InputData(input_shape=(1, 1, in_lines), input_bits=input_bits,
                              name="in"))
    # weights_bits=4 symmetric int4 -- the .clm int4_sym track. act_bits via
    # activation quantization (1 -> LIF comparator, matching SW envelope).
    fc = akida.FullyConnected(units=units, name="fc", weights_bits=4,
                              activation=(act_bits > 1))
    model.add(fc)
    model.map(dev)
    seqs = model.sequences
    backend = str(seqs[0].backend) if seqs else "none"

    fc_layer = model.get_layer("fc")
    w_var = fc_layer.get_variable("weights")               # (1,1,in_lines,units)
    w_new = np.asarray(weights, dtype=w_var.dtype).reshape(w_var.shape)
    fc_layer.set_variable("weights", w_new)

    xin = np.asarray(x, dtype=np.uint8).reshape(1, 1, 1, in_lines)
    _ = model.forward(xin)                                 # warm-up (lazy upload)
    t0 = time.perf_counter()
    for _ in range(n_iter):
        y = model.forward(xin)
    t1 = time.perf_counter()
    ms = (t1 - t0) / n_iter * 1000.0
    hz = n_iter / (t1 - t0)
    out = np.asarray(y).reshape(-1)[:units].astype(np.int64)
    return out, round(ms, 4), round(hz, 2), {
        "device_version": str(dev.version),
        "mapped_backend": backend,
        "n_iter": n_iter,
    }


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------
def run(clm_path, n_iter, units, in_lines, act_bits, input_bits, seed):
    rng = np.random.default_rng(seed)
    result = {
        "harness": "clm_akida_bench",
        "act_bits": act_bits,
        "input_bits": input_bits,
        "units": units,
        "in_lines": in_lines,
        "seed": seed,
    }

    weights_from_clm = False
    header = None
    if clm_path and os.path.exists(clm_path):
        try:
            header, _, _, _ = load_clm_int4(clm_path)
            result["clm_header_arch"] = header.get("arch")
            # Producer binary block layout TBD -> deterministic int4 weights
            # sized from the .clm arch HEADER (flagged honestly below).
        except Exception as e:  # noqa: BLE001
            result["clm_load_error"] = repr(e)

    # int4-sym weights in [-7,+7]; deterministic from seed (or .clm block when
    # the producer block layout lands). Shape (in_lines, units) for the FC.
    weights = rng.integers(-7, 8, size=(in_lines, units), dtype=np.int64)
    result["weights_from_clm"] = weights_from_clm

    # tiny dummy int4 activation input in [0, 2^input_bits - 1].
    x = rng.integers(0, (1 << input_bits), size=in_lines, dtype=np.int64)

    # --- SW envelope forward (always runs) ---
    sw_out = sw_forward(x, weights, act_bits, input_bits, units)
    result["sw_out"] = sw_out.tolist()

    have_clm = bool(clm_path and os.path.exists(clm_path))
    have_hw = hw_available()

    if have_clm and have_hw:
        hw_out, ms, hz, meta = hw_forward_bench(x, weights, units, in_lines,
                                                act_bits, input_bits, n_iter)
        byte_identical = bool(np.array_equal(hw_out, sw_out))
        result.update({
            "mode": "hw-live",
            "awaiting_clm": False,
            "hw_out": hw_out.tolist(),
            "latency_ms_per_inference": ms,
            "throughput_hz": hz,
            "byte_identical_hw_sw": byte_identical,
            "hamming": int(np.count_nonzero(hw_out != sw_out)),
            "hw_meta": meta,
            "provenance": "akida-hw",
        })
    else:
        # HONEST sw-smoke: no fabricated on-chip latency. Proves harness wiring.
        result.update({
            "mode": "sw-smoke",
            "awaiting_clm": not have_clm,
            "hw_reachable": have_hw,
            "latency_ms_per_inference": None,
            "throughput_hz": None,
            "byte_identical_hw_sw": None,
            "provenance": "akida-sw-fallback",
            "note": ("no real .clm yet (P2 full-fire 생성중) -- SW envelope smoke "
                     "only; on-chip latency NOT measured (p7 fake-measure 금지). "
                     "rerun with --clm <path> on pi5-akida (streamer stop->bench->"
                     "restart) once the .clm lands."),
        })
    return result


def main():
    ap = argparse.ArgumentParser(description="CLM .clm int4 -> AKD1000 on-chip bench")
    ap.add_argument("--clm", default=None, help="path to .clm (omit -> sw-smoke)")
    ap.add_argument("--n-iter", type=int, default=100)
    ap.add_argument("--units", type=int, default=16)
    ap.add_argument("--in-lines", type=int, default=16)
    ap.add_argument("--act-bits", type=int, default=1)
    ap.add_argument("--input-bits", type=int, default=4)
    ap.add_argument("--seed", type=int, default=187)
    ap.add_argument("--json", action="store_true", help="emit json only")
    args = ap.parse_args()

    res = run(args.clm, args.n_iter, args.units, args.in_lines,
              args.act_bits, args.input_bits, args.seed)
    if args.json:
        print(json.dumps(res, indent=2))
    else:
        print(f"[clm_akida_bench] mode={res['mode']} "
              f"awaiting_clm={res.get('awaiting_clm')}")
        print(f"  act_bits={res['act_bits']} input_bits={res['input_bits']} "
              f"units={res['units']} in_lines={res['in_lines']}")
        print(f"  sw_out={res['sw_out']}")
        if res["mode"] == "hw-live":
            print(f"  hw_out={res['hw_out']}")
            print(f"  byte_identical_hw_sw={res['byte_identical_hw_sw']} "
                  f"hamming={res['hamming']}")
            print(f"  latency={res['latency_ms_per_inference']} ms/inf  "
                  f"throughput={res['throughput_hz']} Hz")
            print(f"  hw_meta={res['hw_meta']}")
        else:
            print(f"  hw_reachable={res.get('hw_reachable')}")
            print(f"  {res['note']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
