"""sepconv_sw.py -- SW model for the AKIDA SeparableConvolutional axis (round-5).

Mirrors sepconv_hw.py: InputConv (flip=False) -> SeparableConv (fused depthwise
+ pointwise). Uses akida_sw_lif.sepconv2d_quantized_forward with the recovered
FUSED semantics (depthwise true-conv raw potentials -> pointwise 1x1 -> single
activation quantize; NO mid-activation). Same probe images + y_sha256 schema.

Usage: python sepconv_sw.py --wseed 7 --act-bits 4 --f1 4 --f2 8 --k 3 --hw 8
"""
import argparse, hashlib, json, os, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "..", "HEXAD", "CHAT", "server"))
import akida_sw_lif

def sh(a): return hashlib.sha256(np.asarray(a).astype(np.int64).tobytes()).hexdigest()[:16]

def rand_int_weights(rng, shape, wb):
    lim = (1 << (wb - 1)) - 1
    return rng.integers(-lim, lim + 1, size=shape).astype(np.int64)

def probe_imgs(H, W, C):
    out = []
    out.append(np.zeros((1, H, W, C), dtype=np.uint8))
    out.append(np.full((1, H, W, C), 15, dtype=np.uint8))
    out.append((np.arange(H*W*C).reshape(1, H, W, C) % 16).astype(np.uint8))
    rng = np.random.default_rng(2026)
    for _ in range(7):
        out.append(rng.integers(0, 16, size=(1, H, W, C)).astype(np.uint8))
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--wseed", type=int, default=7)
    ap.add_argument("--act-bits", type=int, default=4)
    ap.add_argument("--weights-bits", type=int, default=4)
    ap.add_argument("--f1", type=int, default=4)
    ap.add_argument("--f2", type=int, default=8)
    ap.add_argument("--k", type=int, default=3)
    ap.add_argument("--hw", dest="hwsz", type=int, default=8)
    a = ap.parse_args()
    H = W = a.hwsz; C = 1
    rng = np.random.default_rng(a.wseed)
    W1 = rand_int_weights(rng, (a.k, a.k, C, a.f1), a.weights_bits)
    Wdw = rand_int_weights(rng, (a.k, a.k, a.f1, 1), a.weights_bits)
    Wpw = rand_int_weights(rng, (1, 1, a.f1, a.f2), a.weights_bits)
    meta = {"axis": "sepconv", "wseed": a.wseed, "act_bits": a.act_bits,
            "f1": a.f1, "f2": a.f2, "k": a.k, "hw": a.hwsz,
            "W1_sha": sh(W1), "Wdw_sha": sh(Wdw), "Wpw_sha": sh(Wpw),
            "backend": "sw-numpy-sepconv"}
    print(json.dumps({"meta": meta}))
    for idx, ximg in enumerate(probe_imgs(H, W, C)):
        x = ximg[0].astype(np.int64)
        h = akida_sw_lif.conv2d_quantized_forward(x, W1, a.act_bits, flip=False,
                                                  padding="same", stride=1)
        y = akida_sw_lif.sepconv2d_quantized_forward(h, Wdw, Wpw, a.act_bits,
                                                     flip=True, padding="same", stride=1)
        yf = y.reshape(-1).astype(np.int64)
        rec = {"side": "SW", "axis": "sepconv", "input_idx": idx, "input_sha": sh(ximg),
               "y": yf.tolist(), "y_sha256": sh(yf), "y_len": int(yf.size),
               "y_max": int(yf.max()), "y_min": int(yf.min()),
               "n_levels": int(len(np.unique(yf)))}
        print(json.dumps(rec))

if __name__ == "__main__":
    main()
