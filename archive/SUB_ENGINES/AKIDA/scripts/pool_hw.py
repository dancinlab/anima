"""pool_hw.py -- AKD1000 pooling-axis frontier probe (round-5).

AKD1000 fuses pooling INTO the Convolutional layer (pool_size/pool_type/
pool_stride params), there is no standalone Pool layer in akida 2.19.1.
PoolType in {NoPooling, Max, Average}. This builds a single InputConvolutional
with pooling enabled and emits the FULL output tensor + sha per probe input so
pool_sw.py can be byte-diffed -- and so we can EMPIRICALLY recover whether the
chip pools BEFORE or AFTER the activation quantizer.

Usage: python pool_hw.py --pool max --psize 2 --pstride 2 --act-bits 4 \
                         --f1 8 --k 3 --hw 8 --wseed 7
"""
import argparse, hashlib, json, sys
import numpy as np
import akida

def sh(a): return hashlib.sha256(np.asarray(a).astype(np.int64).tobytes()).hexdigest()[:16]

def rand_int_weights(rng, shape, wb, dtype):
    lim = (1 << (wb - 1)) - 1
    return rng.integers(-lim, lim + 1, size=shape).astype(dtype)

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
    ap.add_argument("--pool", default="max", choices=["max", "average"])
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
    dev = akida.devices()[0]
    m = akida.Model()
    if a.pool == "max":
        pt = akida.PoolType.Max
        psz = (a.psize, a.psize); pstr = (a.pstride, a.pstride)
    else:  # AKD1000 Average pooling is GLOBAL only (pool_size must be -1)
        pt = akida.PoolType.Average
        psz = (-1, -1); pstr = (-1, -1)
    m.add(akida.InputConvolutional(input_shape=(H, W, C), kernel_size=(a.k, a.k),
        filters=a.f1, padding=akida.Padding.Same,
        pool_size=psz, pool_type=pt, pool_stride=pstr,
        weights_bits=a.weights_bits, activation=True, act_bits=a.act_bits, name="c1"))
    m.map(dev)
    rng = np.random.default_rng(a.wseed)
    c1 = m.get_layer("c1")
    W1 = rand_int_weights(rng, c1.get_variable("weights").shape, a.weights_bits, c1.get_variable("weights").dtype)
    c1.set_variable("weights", W1)
    try: c1.set_variable("threshold", np.zeros(a.f1, dtype=np.int32))
    except Exception: pass
    backends = [str(s.backend) for s in m.sequences]
    meta = {"axis": "pool", "pool": a.pool, "psize": a.psize, "pstride": a.pstride,
            "act_bits": a.act_bits, "f1": a.f1, "k": a.k, "hw": a.hwsz, "wseed": a.wseed,
            "W1_sha": sh(W1), "W1_flat": W1.reshape(-1).astype(int).tolist(),
            "W1_shape": list(W1.shape),
            "backends": backends, "on_hardware": any("Hardware" in b for b in backends),
            "device": str(dev.version)}
    print(json.dumps({"meta": meta})); sys.stdout.flush()
    for idx, x in enumerate(probe_imgs(H, W, C)):
        y = np.asarray(m.forward(x)).reshape(-1).astype(np.int64)
        rec = {"side": "HW", "axis": "pool", "input_idx": idx, "input_sha": sh(x),
               "y": y.tolist(), "y_sha256": sh(y), "y_len": int(y.size),
               "y_max": int(y.max()), "y_min": int(y.min()),
               "n_levels": int(len(np.unique(y)))}
        print(json.dumps(rec)); sys.stdout.flush()

if __name__ == "__main__":
    main()
