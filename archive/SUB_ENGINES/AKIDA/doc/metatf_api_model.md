# MetaTF API — akida.Model

> SOURCE: https://doc.brainchipinc.com/api_reference/akida_apis.html#model
> SOURCE: https://doc.brainchipinc.com/user_guide/akida.html#the-akida-model
> CACHED: 2026-05-21 UTC
> SCOPE: AKD1000 (Akida 1.0 V1 model)

## Constructor

```python
akida.Model(filename=None, layers=None)
```

| Param | Type | Default | Meaning |
|---|---|---|---|
| `filename` | `str | Path | None` | `None` | Path to `.fbz` Akida model file to load from disk |
| `layers` | `list[akida.Layer] | None` | `None` | List of pre-constructed layers to wrap |

**Both None** → empty model (call `.add()` per layer thereafter).
**`filename`** → loaded from `.fbz` (FlatBuffer) — common production path.
**`layers`** → in-memory build (programmatic path).

```python
# 1. empty + manual build
from akida import Model, InputData, FullyConnected
m = Model()
m.add(InputData(input_shape=(8, 1, 1), input_bits=1))
m.add(FullyConnected(units=4, weights_bits=1, act_bits=1))

# 2. load from file (production)
m = Model("my_model.fbz")

# 3. from layer list
m = Model(layers=[
    InputData(input_shape=(8, 1, 1), input_bits=1),
    FullyConnected(units=4, weights_bits=1, act_bits=1),
])
```

## Methods (verbatim from API reference)

### Layer assembly

```python
model.add(layer, inbound_layers=[])
```
Append a layer. `inbound_layers` lets you wire non-sequential branches (Akida 2.0 only — V1/AKD1000 is sequential).

```python
model.pop_layer()
```
Remove the last layer (used when swapping the trainable head for edge learning).

```python
model.get_layer(name_or_index)
```
Retrieve a specific layer by name (str) or integer index.

### Inference

```python
outputs = model.forward(inputs, batch_size=0)
```
- `inputs` : `np.ndarray` shape `(batch, H, W, C)` dtype `uint8`
- `batch_size` : 0 = use model default
- **Returns**: integer-valued `np.ndarray` (the raw potentials, **not** softmax probabilities)
- Output shape mirrors final layer's output specification

```python
float_outputs = model.predict(inputs, batch_size=0)
```
- Same input shape
- **Returns**: `float32` `np.ndarray` — replicates the converted CNN's float output (useful when comparing to source Keras model)

### Edge learning (AKD1000 only)

```python
model.compile(optimizer)
```
Bind an `AkidaUnsupervised` optimizer to the trainable final `FullyConnected` layer. Must be called **before** `.fit()`.

```python
model.fit(inputs, input_labels, batch_size=0)
```
- `inputs` : `uint8` `(batch, H, W, C)`
- `input_labels` : `np.int32` 1-D array of class labels (NOT one-hot)
- **Returns**: documented as no return value; modifies model weights in place
- Repeated calls accumulate (online learning)

```python
loss, accuracy = model.evaluate(inputs, labels, num_classes=0, batch_size=0)
```
Helper for measuring classifier performance.

```python
model.add_classes(n)
```
Append `n` new class slots to a compiled edge-learning model (Akida 1.0 edge-learning convention for adding categories incrementally).

### Hardware deployment

```python
model.map(device, hw_only=False, mode=MapMode.AllNps, constraints=None)
```
| Param | Default | Meaning |
|---|---|---|
| `device` | required | `akida.HwDevice` (real) or virtual (`akida.AKD1000()`) |
| `hw_only` | `False` | If True, raise if any layer can't fit HW (vs falling back to CPU) |
| `mode` | `MapMode.AllNps` | `AllNps`, `HwPr`, or `Minimal` (NP usage strategy) |
| `constraints` | `None` | `akida.MapConstraints` for advanced NP allocation |

After `.map()`, `forward()` runs on silicon.

### Persistence

```python
model.save(model_file)         # writes .fbz to disk
buf = model.to_buffer()        # serialize to bytes
m2 = Model.from_buffer(buf)    # round-trip
```

### Introspection

```python
model.summary()                # print layer table + NP allocation
model.input_shape              # (H, W, C) — channels-last
model.output_shape             # (H', W', C')
model.layer_count              # int
model.layers                   # list[akida.Layer]
model.device                   # bound device (or None)
model.macs                     # int — multiply-accumulate count
model.statistics               # dict — populated after forward() runs
model.sequences                # list — HW sequences after .map()
```

## End-to-end example (AKD1000)

```python
import numpy as np
from akida import Model, devices

# 1. load pre-converted .fbz (built on host with cnn2snn)
m = Model("anima_kuramoto_8c.fbz")

# 2. probe hardware
devs = devices()
if not devs:
    raise RuntimeError("no AKD1000 detected — check lspci + akida_pcie module")
dev = devs[0]
print(f"AKD1000 detected: version={dev.version}")  # NSoC_v1

# 3. map to silicon
m.map(dev)
print(m.summary())  # shows NP allocation per layer

# 4. inference
x = np.random.randint(0, 256, size=(1,) + tuple(m.input_shape), dtype=np.uint8)
y = m.forward(x)
print(f"output shape={y.shape}, dtype={y.dtype}")  # integer potentials

# 5. statistics after inference
print(m.statistics)  # spike counts, NP utilization, latency
```

## Pack adapter mock vs HW divergence

| Pack mock (before update) | Real `akida.Model` | Fix in pack |
|---|---|---|
| `Model()` no-arg only | `Model(filename=None, layers=None)` | mock now accepts both |
| `.forward(input)` returns binary mask via LCG | `.forward(uint8 nparray)` returns integer potentials | mock now returns `np.int32` array (still deterministic LCG-seeded) |
| `.fit(input, target)` Hebbian outer-product on float | `.fit(uint8, int32_labels)` opaque on-chip update | mock now accepts `(inputs, input_labels)` signature; internal Hebbian still computed for parity test, but signature matches |
| No `.compile()` | `.compile(optimizer)` mandatory before `.fit()` | mock now requires `.compile(AkidaUnsupervised(...))` before `.fit()` |
| No `.map()` | `.map(device)` is the binding call | mock now exposes `.map(device)` |
| No `.predict()` | `.predict()` returns float32 | mock now exposes `.predict()` = `.forward().astype(np.float32)` |
| No `.summary()` / `.save()` | both standard | mock stubs both |
