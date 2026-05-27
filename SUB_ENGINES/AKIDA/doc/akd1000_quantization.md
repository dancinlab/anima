# AKD1000 quantization (QuantizeML + CNN2SNN)

> SOURCE: https://doc.brainchipinc.com/user_guide/quantizeml.html
> SOURCE: https://doc.brainchipinc.com/user_guide/cnn2snn.html
> SOURCE: https://doc.brainchipinc.com/api_reference/cnn2snn_apis.html
> CACHED: 2026-05-21 UTC
> SCOPE: AKD1000 (target v1 — Akida 1.0)

## Two-stage pipeline (host-only)

```
Keras/ONNX float model
        ▼
  [QuantizeML]    → quantized Keras/ONNX (per-tensor, 1/2/4/8-bit)
        ▼
  [CNN2SNN convert + AkidaVersion.v1]
        ▼
  akida.Model (in-memory)
        ▼
  model.save("foo.fbz")     → ship .fbz to Pi 5
        ▼
  [Pi 5] akida.Model("foo.fbz") → model.map(device) → model.forward(x)
```

**All stages except the last run on host (Mac/x86 Linux) with full TF stack.**  Pi 5 only needs `akida` (2.4 MB wheel) — no TF.

## QuantizeML — params for AKD1000

```python
from quantizeml.models import QuantizationParams, quantize

qparams = QuantizationParams(
    input_weight_bits=8,        # first layer weights — 8-bit mandatory
    weight_bits=4,              # inner weights — 1, 2, or 4
    activation_bits=4,          # activations — 1, 2, or 4
    per_tensor_activations=True,  # MANDATORY for Akida 1.0/AKD1000
                                  # (per-axis is V2 only)
)

q_model = quantize(keras_model, qparams=qparams)
```

| Param | AKD1000 valid values | Notes |
|---|---|---|
| `input_weight_bits` | 8 | first layer ALWAYS 8-bit |
| `weight_bits` | 1, 2, 4 | edge-learnable layer **must be 1** |
| `activation_bits` | 1, 2, 4 | 1 = pure spike |
| `per_tensor_activations` | **True** | required for V1 conversion |

## CLI

```bash
# 4-bit weight + activation, 8-bit input
quantizeml quantize \
    -m model_keras.h5 \
    -i 8 -w 4 -a 4 \
    --per_tensor_activations

# with calibration (better quantization quality)
quantizeml quantize \
    -m model.h5 \
    -i 8 -w 4 -a 4 \
    -sa calibration_samples.npz \
    -bs 128 \
    --per_tensor_activations
```

## CNN2SNN convert (host)

```python
from cnn2snn import convert, set_akida_version, AkidaVersion

with set_akida_version(AkidaVersion.v1):     # CRITICAL for AKD1000
    akida_model = convert(quantized_keras_model)

akida_model.save("anima_kuramoto_8c.fbz")
```

**Default is `AkidaVersion.v2`** — if you forget `set_akida_version`, the `.fbz` won't map to AKD1000. Pack INSTALL.sh should always set:

```bash
export CNN2SNN_TARGET_AKIDA_VERSION=v1
```

before any `cnn2snn` invocation.

## CNN2SNN API

```python
cnn2snn.convert(
    model,
    file_path: str = None,
    input_scaling: tuple = None,
) → akida.Model
```

```python
cnn2snn.check_model_compatibility(
    model,
    device: akida.HwDevice = None,
    input_dtype: str = 'uint8',
) → None  # raises on first incompatibility
```

```python
cnn2snn.AkidaVersion           # enum: v1 (AKD1000), v2 (AKD2000)
cnn2snn.get_akida_version()    # current target
cnn2snn.set_akida_version(v)   # context manager
```

## QuantizeML CLI surface

```bash
quantizeml quantize ...        # main entry — full pipeline
quantizeml config ...          # generate config from model
quantizeml check ...           # compatibility pre-check (don't quantize)
quantizeml insert_rescaling ... # add Rescaling layer if missing
```

## FixedPoint representation (V1 + V2)

QuantizeML stores quantized tensors as `quantizeml.tensors.FixedPoint`:

```
FixedPoint = signed integer × 2^(-frac_bits)
```

- Integer-only operations throughout the network
- No float multiplication on the chip
- Bit-precision exactly matches `weight_bits` / `activation_bits` declared

This is why AKD1000 inference is mW-class: no FP unit, no IEEE rounding.

## Pack adapter quantization strategy

Most anima Pack adapters are **toy 8-neuron pools**. Conversion plan per adapter:

| Adapter | Built in | Pre-quant model | Conversion command (host) |
|---|---|---|---|
| `SnnLifAdapter` | numpy sw | binary FC → `FullyConnected(units=8, weights_bits=1, act_bits=1)` | `cnn2snn convert -m snn_lif.h5 --target v1 → snn_lif.fbz` |
| `KuramotoAdapter` | numpy sw | phase-encoded → `FullyConnected(units=8, weights_bits=4, act_bits=4)` | `cnn2snn convert -m kuramoto.h5 --target v1 → kuramoto.fbz` |
| `MemristorHybridAdapter` | numpy sw | binary FC + edge learn compile | `cnn2snn convert -m mem.h5 --target v1 → mem.fbz` |
| ... others ... | numpy sw | similar 8-unit binary FC | similar |

**Honest C3**: real Pi 5 conversion path requires (1) writing the Keras source model that mirrors the adapter's sw behavior, (2) calibrating with anima-realistic input samples, (3) verifying byte-parity hexa-sw vs AKD1000. This is **Phase 5 work** (post-Pi 5 arrival). Mock fallback path validates the API contract today.

## Pack mock quantization stubs

Mock doesn't actually quantize (it's a numpy fallback). New mock additions:

```python
# pack/mocks/metatf_mock.py
class MockAkidaUnsupervised:
    def __init__(self, num_weights, num_classes=1, initial_plasticity=1.0,
                 learning_competition=0.0, min_plasticity=0.1, plasticity_decay=0.25):
        self.num_weights = num_weights
        self.num_classes = num_classes
        self.initial_plasticity = initial_plasticity
        self.learning_competition = learning_competition
        self.min_plasticity = min_plasticity
        self.plasticity_decay = plasticity_decay

# adapter calls:
mock.AkidaUnsupervised(num_weights=4, num_classes=8)  # signature match w/ real SDK
```
