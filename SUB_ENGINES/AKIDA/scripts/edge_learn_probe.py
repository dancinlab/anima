"""Probe: does BC.00.000.002 (NSoC_v2 / AKD1000) support on-chip edge learning?

On-chip Akida unsupervised learning requires the trainable layer to receive
BINARY inputs. We feed a 1-bit InputData so the FullyConnected gets binary
spikes, then compile AkidaUnsupervised + fit() ON CHIP.
"""
import hashlib
import json
import os

import numpy as np
import akida

# ── learning-input entropy source (H_923 M7 — production HW learning path) ──
# The few-shot on-chip AkidaUnsupervised input is host-side. When env
# ANIMA_QRNG_LEARN_BIN points at an ANU vacuum-fluctuation buffer (anu_pull.py),
# the production edge-learn draws its training samples from AUDITED quantum
# entropy instead of the numpy PRNG — wiring the PLASTICITY learning lane (not
# just the H_923 probe) to substrate-native quantum. Statistical quality is
# identical (chacha20==ANU, #123-A); value = provenance. DECODER inference is
# untouched (deterministic, separate lane).
_QRNG_BIN = os.environ.get("ANIMA_QRNG_LEARN_BIN", "")
_qrng_sha = None


def _learn_input(shape):
    """Binary {0,1} learning samples from ANU quantum bytes, or numpy PRNG."""
    global _qrng_sha
    n = int(np.prod(shape))
    if _QRNG_BIN and os.path.exists(_QRNG_BIN):
        raw = open(_QRNG_BIN, "rb").read()
        _qrng_sha = hashlib.sha256(raw).hexdigest()
        bits = np.unpackbits(np.frombuffer(raw, dtype=np.uint8))
        if bits.size < n:
            bits = np.resize(bits, n)          # cycle if buffer short
        return bits[:n].astype(np.uint8).reshape(shape)
    return np.random.default_rng(42).integers(0, 2, size=shape, dtype=np.uint8)


out = {}
dev = akida.devices()[0]
out["device_version"] = str(dev.version)
out["ip_version"] = str(dev.ip_version)

model = akida.Model()
# input_bits=1 => binary spikes feeding the trainable layer
model.add(akida.InputData(input_shape=(1, 1, 16), input_bits=1, name="in"))
model.add(akida.FullyConnected(units=10, name="fc", weights_bits=1,
                               activation=True))
model.map(dev)
out["mapped_backend"] = str(model.sequences[0].backend)

learn_ok = fit_ok = False
try:
    model.compile(optimizer=akida.AkidaUnsupervised(num_weights=2,
                                                    learning_competition=0.1))
    learn_ok = True
    out["compile_AkidaUnsupervised"] = "ok"
    out["device_learn_enabled_after_compile"] = bool(dev.learn_enabled)
except Exception as e:  # noqa: BLE001
    out["compile_err"] = repr(e)

if learn_ok:
    x = _learn_input((8, 1, 1, 16))  # binary — ANU quantum if armed, else numpy PRNG
    out["learn_input_source"] = "anu_quantum" if _qrng_sha else "numpy_prng"
    out["learn_input_provenance"] = {"bin": _QRNG_BIN, "sha256": _qrng_sha} if _qrng_sha else None
    try:
        model.fit(x)  # on-chip Hebbian learning
        fit_ok = True
        out["fit_on_chip"] = "ok"
        out["device_learn_enabled_after_fit"] = bool(dev.learn_enabled)
    except Exception as e:  # noqa: BLE001
        out["fit_err"] = repr(e)

out["edge_learning_supported"] = bool(learn_ok and fit_ok)
print(json.dumps(out, indent=2))
