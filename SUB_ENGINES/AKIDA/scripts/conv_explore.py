"""conv_explore.py -- learn AKD1000 InputConvolutional semantics (round-4 conv axis).

Builds a tiny InputConvolutional on the chip, inspects weight shape/layout/dtype,
runs deterministic graded inputs, dumps full output tensor + sha to reverse-engineer
the conv quantizer (same method as the FC quantizer recovery).
"""
import json, hashlib
import numpy as np
import akida

def sh(a): return hashlib.sha256(np.asarray(a).astype(np.int64).tobytes()).hexdigest()[:16]

out = {}
dev = akida.devices()[0]
out["device"] = str(dev.version)
H = W = 6; C = 1; F = 4; K = 3
out["input_hwc"] = [H, W, C]; out["filters"] = F; out["kernel"] = K

m = akida.Model()
m.add(akida.InputConvolutional(
    input_shape=(H, W, C), kernel_size=(K, K), filters=F,
    padding=akida.Padding.Same, kernel_stride=(1, 1),
    weights_bits=4, activation=True, act_bits=4, name="conv"))
m.map(dev)
out["mapped_backend"] = str(m.sequences[0].backend)
out["on_hardware"] = "Hardware" in out["mapped_backend"]
out["model_input_shape"] = list(m.input_shape)
out["model_output_shape"] = list(m.output_shape)

conv = m.get_layer("conv")
Wv = conv.get_variable("weights")
out["weights_shape"] = list(Wv.shape)
out["weights_dtype"] = str(Wv.dtype)
rng = np.random.default_rng(7); lim = 7
Wr = rng.integers(-lim, lim+1, size=Wv.shape).astype(Wv.dtype)
try:
    conv.set_variable("weights", Wr); out["weights_set"] = True
except Exception as e: out["weights_set_err"] = repr(e)
for tname in ("threshold",):
    try:
        tv = conv.get_variable(tname)
        conv.set_variable(tname, np.zeros_like(tv)); out[tname+"_set"] = True
        out[tname+"_shape"] = list(tv.shape)
    except Exception as e: out[tname+"_note"] = repr(e)
out["var_names"] = [v for v in conv.variables.names] if hasattr(conv,"variables") else "n/a"
out["weights_sha"] = sh(Wr)
out["weights_flat_first27"] = Wr.reshape(-1)[:27].astype(int).tolist()

for idx in range(3):
    if idx == 0: x = np.zeros((1,H,W,C), dtype=np.uint8)
    elif idx == 1: x = np.full((1,H,W,C), 15, dtype=np.uint8)
    else: x = (np.arange(H*W*C).reshape(1,H,W,C) % 16).astype(np.uint8)
    y = np.asarray(m.forward(x)).reshape(-1).astype(np.int64)
    out[f"probe{idx}"] = {"input_sha": sh(x), "out_shape": list(np.asarray(m.forward(x)).shape),
                          "out_sha": sh(y), "out_max": int(y.max()), "out_min": int(y.min()),
                          "out_n_levels": int(len(np.unique(y))), "out_first40": y[:40].tolist()}
print(json.dumps(out, indent=2))
