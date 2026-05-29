"""conv_map_diag.py -- WHY does InputConvolutional not map to AKD1000 NP?

Tries several conv configs + dumps model.summary() + per-sequence backend +
mapping incompatibility reasons, to determine if conv mapping is a config issue
or a genuine HW-placement limit (NSoC_v2 / AKD1000 1.0 IP).
"""
import json
import numpy as np
import akida

out = {"sdk": akida.__version__}
dev = akida.devices()[0]
out["device"] = str(dev.version); out["ip_version"] = str(dev.ip_version)

def try_cfg(name, builder):
    rec = {}
    try:
        m = builder()
        try:
            m.map(dev)
            rec["mapped"] = True
            rec["n_seq"] = len(m.sequences)
            rec["backends"] = [str(s.backend) for s in m.sequences]
            rec["on_hw"] = any("Hardware" in str(s.backend) for s in m.sequences)
            rec["out_shape"] = list(m.output_shape)
        except Exception as e:
            rec["map_err"] = repr(e)[:300]
        try:
            import io, contextlib
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                m.summary()
            rec["summary"] = buf.getvalue()[-1200:]
        except Exception as e:
            rec["summary_err"] = repr(e)[:200]
    except Exception as e:
        rec["build_err"] = repr(e)[:300]
    out[name] = rec

def b_inputconv_4f():
    m = akida.Model()
    m.add(akida.InputConvolutional(input_shape=(6,6,1), kernel_size=(3,3), filters=4,
        padding=akida.Padding.Same, weights_bits=4, activation=True, act_bits=4, name="c"))
    return m

def b_inputconv_wb1():
    m = akida.Model()
    m.add(akida.InputConvolutional(input_shape=(6,6,1), kernel_size=(3,3), filters=4,
        padding=akida.Padding.Same, weights_bits=1, activation=True, act_bits=1, name="c"))
    return m

def b_inputconv_3ch_valid():
    m = akida.Model()
    m.add(akida.InputConvolutional(input_shape=(8,8,3), kernel_size=(3,3), filters=8,
        padding=akida.Padding.Valid, weights_bits=2, activation=True, act_bits=4, name="c"))
    return m

def b_conv_then():
    m = akida.Model()
    m.add(akida.InputConvolutional(input_shape=(8,8,1), kernel_size=(3,3), filters=8,
        padding=akida.Padding.Same, weights_bits=4, activation=True, act_bits=4, name="c1"))
    m.add(akida.Convolutional(kernel_size=(3,3), filters=8, padding=akida.Padding.Same,
        weights_bits=4, activation=True, act_bits=4, name="c2"))
    return m

try_cfg("inputconv_4f_wb4", b_inputconv_4f)
try_cfg("inputconv_wb1_ab1", b_inputconv_wb1)
try_cfg("inputconv_3ch_valid", b_inputconv_3ch_valid)
try_cfg("inputconv_then_conv", b_conv_then)
print(json.dumps(out, indent=2))
