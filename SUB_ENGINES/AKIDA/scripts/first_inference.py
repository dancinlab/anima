"""First inference on AKD1000 (NSoC_v2 / BC.00.000.002) — Pi 5 LAN, $0.

Builds a minimal Akida 1.0 model (InputData -> FullyConnected), maps it to the
physical hardware device, programs weights, and runs a forward pass ON the chip.
Captures device identity, mapping backend, latency (wall + on-chip clock),
output shape + non-trivial output, power telemetry availability.
"""
import json
import time

import numpy as np

import akida

out = {}

# --- 1. device identity -------------------------------------------------
dev = akida.devices()[0]
out["sdk_version"] = akida.__version__
out["device_version"] = str(dev.version)
out["device_desc"] = getattr(dev, "desc", "?")
out["device_is_AKD1000_factory_match"] = (dev.version == akida.AKD1000().version)
out["device_ip_version"] = str(dev.ip_version)
out["learn_enabled_default"] = bool(dev.learn_enabled)

# --- 2. build a minimal model (Akida 1.0 native quantized) --------------
model = akida.Model()
model.add(akida.InputData(input_shape=(1, 1, 16), input_bits=4, name="in"))
model.add(akida.FullyConnected(units=10, name="fc", weights_bits=1,
                               activation=False))
out["model_layer_count"] = model.layer_count
out["model_input_shape"] = list(model.input_shape)
out["model_output_shape"] = list(model.output_shape)

# --- 3. map to HARDWARE + set deterministic weights ---------------------
model.map(dev)
seqs = model.sequences
out["sequence_count"] = len(seqs)
out["mapped_backend"] = str(seqs[0].backend) if seqs else "none"

# deterministic 1-bit weights: identity-ish pattern so outputs are non-zero
fc = model.get_layer("fc")
try:
    w = fc.get_variable("weights")  # shape (1,1,16,10)
    w_new = np.ones_like(w)         # all +1 (binary => stored as needed)
    fc.set_variable("weights", w_new)
    out["weights_shape"] = list(w.shape)
    out["weights_set"] = True
except Exception as e:  # noqa: BLE001
    out["weights_set_err"] = repr(e)

# enable power measurement on the SoC if the board exposes an INA sensor
power_supported = False
try:
    dev.soc.power_measurement_enabled = True
    power_supported = True
except Exception as e:  # noqa: BLE001
    out["power_enable_note"] = repr(e)
out["power_measurement_supported"] = power_supported

# --- 4. forward pass ON CHIP --------------------------------------------
rng = np.random.default_rng(187)
x = rng.integers(0, 16, size=(1, 1, 1, 16), dtype=np.uint8)
out["input_sum"] = int(x.sum())

_ = model.forward(x)  # warm-up (lazy program upload)

N = 100
t0 = time.perf_counter()
for _ in range(N):
    y = model.forward(x)
t1 = time.perf_counter()

out["output_shape"] = list(y.shape)
out["output_dtype"] = str(y.dtype)
out["output_values"] = y.reshape(-1).tolist()
out["output_nonzero"] = bool(np.count_nonzero(y) > 0)
out["wall_latency_ms_per_inference"] = round((t1 - t0) / N * 1000.0, 4)
out["n_inferences_timed"] = N

# --- 5. on-chip clock + power -------------------------------------------
try:
    out["statistics"] = str(model.statistics)
except Exception as e:  # noqa: BLE001
    out["statistics_err"] = repr(e)

# inference_power_events is a property returning a list (not callable)
try:
    pe = dev.inference_power_events
    pe = list(pe) if pe is not None else []
    out["inference_power_events_count"] = len(pe)
    powers = [getattr(p, "power", None) for p in pe]
    powers = [p for p in powers if p is not None]
    if powers:
        out["avg_power_mW"] = round(sum(powers) / len(powers), 4)
except Exception as e:  # noqa: BLE001
    out["power_events_note"] = repr(e)

print(json.dumps(out, indent=2))
