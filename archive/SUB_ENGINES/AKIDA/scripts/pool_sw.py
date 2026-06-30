"""pool_sw.py -- SW model for the AKIDA pooling axis (round-5, max only).

Mirrors pool_hw.py for pool_type=max: conv2d_quantized_forward (InputConv,
flip=False, SAME, stride1) then pool2d_quantized_forward (windowed max). Because
the activation quantizer is monotone, max-pool-after-activation == the chip's
fused Conv+MaxPool. Average (global) pooling is CLOSED-NEGATIVE (opaque akida-SW
internal rescale) and is intentionally NOT modeled here -- pass --pool max only.

Usage: python pool_sw.py --pool max --psize 2 --pstride 2 --act-bits 4 \
                         --f1 8 --k 3 --hw 8 --wseed 7
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
    ap.add_argument("--pool", default="max", choices=["max"])
    ap.add_argument("--psize", type=int, default=2)
    ap.add_argument("--pstride", type=int, default=2)
    ap.add_argument("--act-bits", type=int, default=4)
    ap.add_argument("--weights-bits", type=int, default=4)
    ap.add_argument("--f1", type=int, default=8)
    ap.add_argument("--k", type=int, default=3)
    ap.add_argument("--hw", dest="hwsz", type=int, default=8)
    ap.add_argument("--wseed", type=int, default=7)
    a = ap.parse_args()
    H = W = a.hwsz; C = 1
    rng = np.random.default_rng(a.wseed)
    W1 = rand_int_weights(rng, (a.k, a.k, C, a.f1), a.weights_bits)
    meta = {"axis": "pool", "pool": a.pool, "psize": a.psize, "pstride": a.pstride,
            "act_bits": a.act_bits, "f1": a.f1, "k": a.k, "hw": a.hwsz, "wseed": a.wseed,
            "W1_sha": sh(W1), "backend": "sw-numpy-pool"}
    print(json.dumps({"meta": meta}))
    for idx, ximg in enumerate(probe_imgs(H, W, C)):
        x = ximg[0].astype(np.int64)
        conv = akida_sw_lif.conv2d_quantized_forward(x, W1, a.act_bits, flip=False,
                                                     padding="same", stride=1)
        y = akida_sw_lif.pool2d_quantized_forward(conv, pool_size=a.psize,
                                                  pool_stride=a.pstride, pool_type="max")
        yf = y.reshape(-1).astype(np.int64)
        rec = {"side": "SW", "axis": "pool", "input_idx": idx, "input_sha": sh(ximg),
               "y": yf.tolist(), "y_sha256": sh(yf), "y_len": int(yf.size),
               "y_max": int(yf.max()), "y_min": int(yf.min()),
               "n_levels": int(len(np.unique(yf)))}
        print(json.dumps(rec))

if __name__ == "__main__":
    main()
