"""multinp_sw.py -- SW model for the multi-NP axis (placement-invariance check).

The on-chip multi-NP placement is just the SAME quantized FC cascade math spread
across >=2 neural processors. The SW model is therefore the SAME
akida_sw_lif.cascade_forward / fc_quantized_forward, with n=units (full-length
output, no truncation to 16). If HW (multi-NP) == SW (single numpy compute)
byte-for-byte, multi-NP placement is TRANSPARENT (placement-invariant).

ROUND-5 (>4-NP, 2026-05-30): verified at 6 NP and 8 NP -- all NONZERO-input
probes are byte-identical to this single SW cascade (placement transparent for
real inputs). The ONLY boundary is the ALL-ZERO input (idx0): on a deep (>=6-NP)
hardware cascade with no signal, the chip emits NON-DETERMINISTIC spurious
activity (floating NP / inter-NP DMA state with nothing to overwrite it; HW
y_max=3 vs SW 0, and two identical runs differ only at idx0). Not SW-modelable
(non-deterministic) -> CLOSED-NEGATIVE, scoped to the degenerate empty input
only -- see HW_SW_CALIBRATION_LOOP_2026_05_29.md 5차 axis 4.

Mirrors multinp_hw.py exactly. Usage:
  python multinp_sw.py --layers 4 --units 512 --wseed 7 --act-bits 4
"""
import argparse, hashlib, json, os, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "..", "HEXAD", "CHAT", "server"))
import akida_sw_lif

IN = 16
def sh(a): return hashlib.sha256(np.asarray(a).astype(np.int64).tobytes()).hexdigest()[:16]
def rand_int_weights(rng, shape, wb):
    lim = (1 << (wb - 1)) - 1
    return rng.integers(-lim, lim + 1, size=shape).astype(np.int64)
def probe_inputs(in_dim, mx):
    rng = np.random.default_rng(2026); xs = []
    xs.append(np.zeros(in_dim, dtype=np.uint8))
    xs.append(np.full(in_dim, mx, dtype=np.uint8))
    xs.append((np.arange(in_dim) % (mx + 1)).astype(np.uint8))
    for _ in range(7): xs.append(rng.integers(0, mx + 1, size=in_dim).astype(np.uint8))
    return xs

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--layers", type=int, default=4)
    ap.add_argument("--units", type=int, default=512)
    ap.add_argument("--wseed", type=int, default=7)
    ap.add_argument("--act-bits", type=int, default=4)
    ap.add_argument("--weights-bits", type=int, default=4)
    a = ap.parse_args()
    rng = np.random.default_rng(a.wseed)
    # akida FC weight layout (1,1,IN_l,units); first layer IN=16, rest IN=units.
    Wlist = []
    in_dim = IN
    for _ in range(a.layers):
        Wlist.append(rand_int_weights(rng, (1, 1, in_dim, a.units), a.weights_bits))
        in_dim = a.units
    meta = {"axis": "multinp", "layers": a.layers, "units": a.units, "wseed": a.wseed,
            "act_bits": a.act_bits, "weights_bits": a.weights_bits,
            "weights_sha256": sh(np.concatenate([w.ravel() for w in Wlist])),
            "backend": "sw-numpy-multinp"}
    print(json.dumps({"meta": meta}))
    for idx, x in enumerate(probe_inputs(IN, 15)):
        h = x.astype(np.int64)
        for Wl in Wlist:
            n_out = Wl.shape[3]
            h = akida_sw_lif.fc_quantized_forward(h, Wl, a.act_bits, n=n_out)
        y = h.reshape(-1).astype(np.int64)
        rec = {"side": "SW", "axis": "multinp", "input_idx": idx, "input_sha": sh(x),
               "y_sha256": sh(y), "y_len": int(y.size), "y_max": int(y.max()),
               "y_min": int(y.min()), "n_levels": int(len(np.unique(y)))}
        print(json.dumps(rec))

if __name__ == "__main__":
    main()
