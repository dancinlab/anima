"""multinp_hw.py -- map a model across >=2 neural processors on AKD1000.

Round-4 multi-NP axis. A single small FC fits on one NP. To force a >=2-NP
placement we either widen the FC (large units) or stack several FC layers; akida's
mapper then distributes layers/units across multiple NPs (reported as NP count in
model.summary()). Question: does the on-chip multi-NP result still equal the
single-NP SW compute (same math, different placement)? Likely transparent.

Emits per-probe end-to-end y + sha (diffable by frontier_diff.py against the SAME
fc_quantized cascade SW), PLUS the mapping report: sequence count, per-seq backend,
NP/component count parsed from summary -- the evidence that >=2 NPs were used.

Usage: python multinp_hw.py --layers 4 --units 512 --wseed 7 --act-bits 4
"""
import argparse, hashlib, io, contextlib, json, re, sys
import numpy as np
import akida

IN = 16
def sh(a): return hashlib.sha256(np.asarray(a).astype(np.int64).tobytes()).hexdigest()[:16]
def rand_int_weights(rng, shape, wb, dtype):
    lim = (1 << (wb - 1)) - 1
    return rng.integers(-lim, lim + 1, size=shape).astype(dtype)
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
    dev = akida.devices()[0]
    m = akida.Model()
    m.add(akida.InputData(input_shape=(1, 1, IN), input_bits=4, name="in"))
    names = [f"fc{i+1}" for i in range(a.layers)]
    for nm in names:
        m.add(akida.FullyConnected(units=a.units, weights_bits=a.weights_bits,
            activation=True, act_bits=a.act_bits, name=nm))
    m.map(dev)
    rng = np.random.default_rng(a.wseed)
    ws = {}
    for nm in names:
        fc = m.get_layer(nm)
        Wr = rand_int_weights(rng, fc.get_variable("weights").shape, a.weights_bits,
                              fc.get_variable("weights").dtype)
        fc.set_variable("weights", Wr); ws[nm] = Wr
        try: fc.set_variable("threshold", np.zeros(a.units, dtype=np.int32))
        except Exception: pass
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        m.summary()
    summ = buf.getvalue()
    nps = re.findall(r"(\d+)\s+(?:CNP|FNP|HRC)\d*", summ)
    np_total = sum(int(x) for x in nps)
    backends = [str(s.backend) for s in m.sequences]
    meta = {"axis": "multinp", "layers": a.layers, "units": a.units, "wseed": a.wseed,
            "act_bits": a.act_bits, "weights_bits": a.weights_bits,
            "weights_sha256": sh(np.concatenate([ws[k].ravel() for k in sorted(ws)])),
            "n_sequences": len(m.sequences), "backends": backends,
            "on_hardware": any("Hardware" in b for b in backends),
            "np_component_counts": nps, "np_total": np_total,
            "multi_np": np_total >= 2, "device": str(dev.version),
            "summary_tail": summ[-700:]}
    print(json.dumps({"meta": meta})); sys.stdout.flush()
    for idx, x in enumerate(probe_inputs(IN, 15)):
        xin = x.reshape(1, 1, 1, IN).astype(np.uint8)
        y = np.asarray(m.forward(xin)).reshape(-1).astype(np.int64)
        rec = {"side": "HW", "axis": "multinp", "input_idx": idx, "input_sha": sh(x),
               "y_sha256": sh(y), "y_len": int(y.size), "y_max": int(y.max()),
               "y_min": int(y.min()), "n_levels": int(len(np.unique(y)))}
        print(json.dumps(rec)); sys.stdout.flush()

if __name__ == "__main__":
    main()
