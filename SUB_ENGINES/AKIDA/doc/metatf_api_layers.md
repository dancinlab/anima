# MetaTF API — Akida V1 layers (AKD1000)

> SOURCE: https://doc.brainchipinc.com/api_reference/akida_apis.html#akida-v1-layers
> CACHED: 2026-05-21 UTC
> SCOPE: AKD1000 (Akida 1.0 V1 layers only — V2 layers excluded)

## Top-level imports

```python
from akida import (
    InputData,
    InputConvolutional,
    FullyConnected,
    Convolutional,
    SeparableConvolutional,
    Padding,
    PoolType,
    LayerType,
    ActivationType,
)
```

**NOTE — these are at the top of the `akida` package, NOT in `akida.layers`.**  Pack mock previously exposed `akida.layers.FullyConnected(...)` — this matches **Akida 2.0** convention. AKD1000 V1 uses bare `akida.FullyConnected(...)`. Mock now supports BOTH paths via:

```python
import akida
akida.FullyConnected(...)          # V1 path (canonical for AKD1000)
akida.layers.FullyConnected(...)   # V2 path (forward-compat alias)
```

## `InputData(input_shape, input_bits=4, name='')`

Input specification layer (declares model input contract).

| Param | Type | Default | Notes |
|---|---|---|---|
| `input_shape` | `tuple[int, int, int]` | required | `(H, W, C)` — channels-last |
| `input_bits` | `int` | `4` | 1, 2, 4, or 8 bit input |
| `name` | `str` | `''` | layer name |

```python
inp = InputData(input_shape=(28, 28, 1), input_bits=8, name='mnist_in')
```

## `InputConvolutional(...)`

First-layer convolution with 8-bit input + selectable weight bits.

```python
InputConvolutional(
    input_shape,                       # (H, W, C) — C ∈ {1, 3} only
    kernel_size,                       # int — 3, 5, or 7
    filters,                           # int — see AKD1000 max table
    name='',
    padding=Padding.Same,              # Padding.Same | Padding.Valid | Padding.SameUpper
    kernel_stride=(1, 1),              # (sh, sw) — sh, sw ∈ {1, 2, 3}
    weights_bits=1,                    # 1 | 2 | 4 | 8
    pool_size=(-1, -1),                # (-1, -1) = no pool; or (1,2)/(2,1)/(2,2)
    pool_type=PoolType.NoPooling,      # PoolType.{NoPooling, Max, Average}
    pool_stride=(-1, -1),
    activation=True,
    act_bits=1,                        # 1 | 2 | 4
    padding_value=0,
)
```

## `Convolutional(...)`

Internal conv layer.  Note: **NOT named `Conv2D`** (that's Akida 2.0).

```python
Convolutional(
    kernel_size,                       # 1, 3, 5, or 7
    filters,
    name='',
    padding=Padding.Same,
    kernel_stride=(1, 1),              # 1 (any kernel) or 2 (3×3 only)
    weights_bits=1,                    # 1 | 2 | 4
    pool_size=(-1, -1),                # (-1, -1) or (2, 2)
    pool_type=PoolType.NoPooling,
    pool_stride=(-1, -1),
    activation=True,
    act_bits=1,
)
```

## `SeparableConvolutional(...)`

Depthwise-separable (point-wise + depth-wise).

```python
SeparableConvolutional(
    kernel_size,
    filters,
    name='',
    padding=Padding.Same,
    kernel_stride=(1, 1),
    weights_bits=2,                    # default differs from Convolutional (2 vs 1)
    pool_size=(-1, -1),
    pool_type=PoolType.NoPooling,
    pool_stride=(-1, -1),
    activation=True,
    act_bits=1,
)
```

## `FullyConnected(units, name='', weights_bits=1, activation=True, act_bits=1)`

Dense / classification layer. **Only V1 layer that supports edge learning** (last layer + binary weights/inputs).

| Param | Type | Default | Notes |
|---|---|---|---|
| `units` | `int` | required | output neuron count |
| `name` | `str` | `''` | |
| `weights_bits` | `int` | `1` | 1, 2, or 4 (must be **1** for edge learning) |
| `activation` | `bool` | `True` | False → linear output |
| `act_bits` | `int` | `1` | 1, 2, or 4 |

```python
# canonical anima pool
fc = FullyConnected(units=8, weights_bits=1, act_bits=1, name='snn_pool')
```

## Enums

### `akida.LayerType`
```
InputData, InputConvolutional, Convolutional, SeparableConvolutional, FullyConnected,
# V2 (excluded on AKD1000):
Conv2D, InputConv2D, DepthwiseConv2D, DepthwiseConv2DTranspose, Conv2DTranspose,
Dense1D, BufferTempConv, DepthwiseBufferTempConv, Add, Concatenate, Dequantizer,
```

### `akida.ActivationType`
```
NoActivation, ReLU, LUT
```
**AKD1000 supports `NoActivation` + bounded `ReLU` only** (no LUT — that's V2).

### `akida.Padding`
```
Valid, Same, SameUpper
```

### `akida.PoolType`
```
NoPooling, Max, Average
```

## Pack adapter layer mapping (revised)

| Adapter | n_neurons (max for AKD1000) | Layer stack (real V1) |
|---|---|---|
| `SnnLifAdapter` | 8 (≪ 57334 FC limit) | `InputData(shape=(8,1,1), input_bits=1)` → `FullyConnected(units=8, weights_bits=1, act_bits=1)` |
| `KuramotoAdapter` | 8 (oscillator pool, no SNN actually fires on AKD1000 — sw-only) | `InputData(shape=(8,1,1), input_bits=4)` → `FullyConnected(units=8, weights_bits=4, act_bits=4)` (phase encoded) |
| `MemristorHybridAdapter` | 8 (Hebbian on last FC) | `InputData(shape=(8,1,1), input_bits=1)` → `FullyConnected(units=8, weights_bits=1, act_bits=1)` + `compile(AkidaUnsupervised(num_weights=4))` |
| `IzhikevichAdapter` | 8 | `InputData` → `FullyConnected` (Izhikevich 2-var is sw-only; AKD1000 emits binary spike) |
| `ThetaGammaAdapter` | 8 | `InputData(shape=(8,1,1))` → `FullyConnected(units=8, weights_bits=2, act_bits=2)` (cross-freq via 2-bit phase) |
| `EegPatternAdapter` | 1×8×8 patch (sw-only mock) | host-only mock — no AKD1000 layer (would need full CNN) |
| `SparseAttentionAdapter` | 8 | `InputData` → `FullyConnected(weights_bits=1)` (sparsity emulated via binary weights) |
| `SpikeTierLmHeadAdapter` | 8 (toy vocab) | `InputData` → `FullyConnected(units=8)` (full LM head won't fit AKD1000 — toy only) |
| `MotivationGateAdapter` | 1 | `InputData(shape=(1,1,1))` → `FullyConnected(units=1, weights_bits=1, act_bits=1)` (threshold-fire = single binary FC) |
| `SpontaneousGateAdapter` | 1 | same as motivation gate |

**Note**: every anima adapter is **toy-scale on purpose** (8-neuron pool). This fits trivially in a single AKD1000 NP (each NP can hold ~1024 binary FC weights). The pack's value isn't compute — it's **substrate** (real spike on real silicon) for downstream demiurge gate verification.

## Pack mock vs HW layer divergence

| Pack mock (before) | Real V1 layer | Fix |
|---|---|---|
| `MockLayers.FullyConnected(**kw)` accepts anything | requires `units` positional | mock signature tightened |
| `MockLayers.Conv2D` | name doesn't exist in V1 | mock now exposes `Convolutional` (canonical) + `Conv2D` alias (V2 forward-compat) |
| `MockLayers.InputData(**kw)` | requires `input_shape` positional | mock signature tightened |
| no `Padding`/`PoolType`/`ActivationType` enums | required for layer params | mock now exposes these enums |
