"""stride_sw.py -- SW model for the AKIDA conv stride/VALID axis (round-5).

Mirrors stride_hw.py exactly. Uses akida_sw_lif.conv2d_quantized_forward with the
calibrated flip semantics AND the new stride/padding params:
  - stage 1 InputConvolutional : flip=False (cross-correlation, akida SW front-end)
  - stage 2 Convolutional      : flip=True  (true convolution = 180deg kernel, HW CNP)
Both stages use the same --stride / --padding. Note: with padding=valid the
stage-1 output H shrinks, so stage-2 sees a smaller map -- both modeled by the
same forward. Same probe images + y_sha256 schema as stride_hw.py.

Usage: python stride_sw.py --wseed 7 --act-bits 4 --f1 8 --f2 8 --k 3 --hw 8 \
                           --stride 2 --padding same
"""
import argparse, hashlib, json, os, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "..", "HEXAD", "CHAT", "server"))
import akida_sw_lif

def sh(a): return hashlib.sha256(np.asarray(a).astype(np.int64).tobytes()).hexdigest()[:16]

def rand_int_weights(rng, shape, weights_bits):
    lim = (1 << (weights_bits - 1)) - 1
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
    ap.add_argument("--f1", type=int, default=8)
    ap.add_argument("--f2", type=int, default=8)
    ap.add_argument("--k", type=int, default=3)
    ap.add_argument("--hw", dest="hwsz", type=int, default=8)
    ap.add_argument("--stride", type=int, default=2)
    ap.add_argument("--padding", default="same", choices=["same", "valid"])
    a = ap.parse_args()
    H = W = a.hwsz; C = 1
    rng = np.random.default_rng(a.wseed)
    W1 = rand_int_weights(rng, (a.k, a.k, C, a.f1), a.weights_bits)
    W2 = rand_int_weights(rng, (a.k, a.k, a.f1, a.f2), a.weights_bits)
    meta = {"axis": "stride", "wseed": a.wseed, "act_bits": a.act_bits,
            "f1": a.f1, "f2": a.f2, "k": a.k, "hw": a.hwsz,
            "stride": a.stride, "padding": a.padding,
            "W1_sha": sh(W1), "W2_sha": sh(W2), "backend": "sw-numpy-conv-stride"}
    print(json.dumps({"meta": meta}))
    for idx, ximg in enumerate(probe_imgs(H, W, C)):
        x = ximg[0].astype(np.int64)               # (H, W, C)
        h = akida_sw_lif.conv2d_quantized_forward(x, W1, a.act_bits, flip=False,
                                                  padding=a.padding, stride=a.stride)
        y = akida_sw_lif.conv2d_quantized_forward(h, W2, a.act_bits, flip=True,
                                                  padding=a.padding, stride=a.stride)
        yf = y.reshape(-1).astype(np.int64)
        rec = {"side": "SW", "axis": "stride", "input_idx": idx, "input_sha": sh(ximg),
               "y": yf.tolist(), "y_sha256": sh(yf), "y_len": int(yf.size),
               "y_max": int(yf.max()), "y_min": int(yf.min()),
               "n_levels": int(len(np.unique(yf)))}
        print(json.dumps(rec))

if __name__ == "__main__":
    main()
