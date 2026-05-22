"""Probe: does BC.00.000.002 (NSoC_v2 / AKD1000) support on-chip edge learning?

On-chip Akida unsupervised learning requires the trainable layer to receive
BINARY inputs. We feed a 1-bit InputData so the FullyConnected gets binary
spikes, then compile AkidaUnsupervised + fit() ON CHIP.
"""
import json
import numpy as np
import akida

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
    rng = np.random.default_rng(42)
    x = rng.integers(0, 2, size=(8, 1, 1, 16), dtype=np.uint8)  # binary
    try:
        model.fit(x)  # on-chip Hebbian learning
        fit_ok = True
        out["fit_on_chip"] = "ok"
        out["device_learn_enabled_after_fit"] = bool(dev.learn_enabled)
    except Exception as e:  # noqa: BLE001
        out["fit_err"] = repr(e)

out["edge_learning_supported"] = bool(learn_ok and fit_ok)
print(json.dumps(out, indent=2))
