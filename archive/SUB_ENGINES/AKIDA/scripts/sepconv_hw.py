"""sepconv_hw.py -- AKD1000 SeparableConvolutional frontier probe (round-5).

SeparableConvolutional = depthwise (per-channel KxK) then pointwise (1x1 conv
mixing channels). Variables: weights (K,K,Cin,1) depthwise + weights_pw
(1,1,Cin,F) pointwise. Maps to the akida SW backend on AKD1000 IP v1 (like
InputConvolutional). This builds InputConv(F1) -> SeparableConv(F2) (need >1
channel for depthwise to matter), fixes both kernel sets to symmetric int4, and
emits the FULL output + sha per probe so sepconv_sw.py can byte-diff.

Usage: python sepconv_hw.py --wseed 7 --act-bits 4 --f1 4 --f2 8 --k 3 --hw 8
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
    ap.add_argument("--wseed", type=int, default=7)
    ap.add_argument("--act-bits", type=int, default=4)
    ap.add_argument("--weights-bits", type=int, default=4)
    ap.add_argument("--f1", type=int, default=4)
    ap.add_argument("--f2", type=int, default=8)
    ap.add_argument("--k", type=int, default=3)
    ap.add_argument("--hw", dest="hwsz", type=int, default=8)
    a = ap.parse_args()
    H = W = a.hwsz; C = 1
    dev = akida.devices()[0]
    m = akida.Model()
    m.add(akida.InputConvolutional(input_shape=(H, W, C), kernel_size=(a.k, a.k),
        filters=a.f1, padding=akida.Padding.Same, weights_bits=a.weights_bits,
        activation=True, act_bits=a.act_bits, name="c1"))
    m.add(akida.SeparableConvolutional(kernel_size=(a.k, a.k), filters=a.f2,
        padding=akida.Padding.Same, weights_bits=a.weights_bits,
        activation=True, act_bits=a.act_bits, name="sc"))
    m.map(dev)
    rng = np.random.default_rng(a.wseed)
    c1 = m.get_layer("c1"); sc = m.get_layer("sc")
    W1 = rand_int_weights(rng, c1.get_variable("weights").shape, a.weights_bits, c1.get_variable("weights").dtype)
    c1.set_variable("weights", W1)
    Wdw = rand_int_weights(rng, sc.get_variable("weights").shape, a.weights_bits, sc.get_variable("weights").dtype)
    sc.set_variable("weights", Wdw)
    Wpw = rand_int_weights(rng, sc.get_variable("weights_pw").shape, a.weights_bits, sc.get_variable("weights_pw").dtype)
    sc.set_variable("weights_pw", Wpw)
    for c, f in ((c1, a.f1), (sc, a.f2)):
        try: c.set_variable("threshold", np.zeros(f, dtype=np.int32))
        except Exception: pass
    backends = [str(s.backend) for s in m.sequences]
    meta = {"axis": "sepconv", "wseed": a.wseed, "act_bits": a.act_bits,
            "f1": a.f1, "f2": a.f2, "k": a.k, "hw": a.hwsz,
            "W1_sha": sh(W1), "Wdw_sha": sh(Wdw), "Wpw_sha": sh(Wpw),
            "W1_flat": W1.reshape(-1).astype(int).tolist(),
            "Wdw_flat": Wdw.reshape(-1).astype(int).tolist(),
            "Wpw_flat": Wpw.reshape(-1).astype(int).tolist(),
            "W1_shape": list(W1.shape), "Wdw_shape": list(Wdw.shape),
            "Wpw_shape": list(Wpw.shape),
            "backends": backends, "on_hardware": any("Hardware" in b for b in backends),
            "device": str(dev.version)}
    print(json.dumps({"meta": meta})); sys.stdout.flush()
    for idx, x in enumerate(probe_imgs(H, W, C)):
        y = np.asarray(m.forward(x)).reshape(-1).astype(np.int64)
        rec = {"side": "HW", "axis": "sepconv", "input_idx": idx, "input_sha": sh(x),
               "y": y.tolist(), "y_sha256": sh(y), "y_len": int(y.size),
               "y_max": int(y.max()), "y_min": int(y.min()),
               "n_levels": int(len(np.unique(y)))}
        print(json.dumps(rec)); sys.stdout.flush()

if __name__ == "__main__":
    main()
