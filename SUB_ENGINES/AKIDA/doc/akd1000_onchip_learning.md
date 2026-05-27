# AKD1000 on-chip (edge) learning

> SOURCE: https://doc.brainchipinc.com/user_guide/akida.html#using-akida-edge-learning
> SOURCE: https://doc.brainchipinc.com/examples/edge/plot_1_edge_learning_kws.html
> SOURCE: https://doc.brainchipinc.com/examples/edge/plot_2_edge_learning_parameters.html
> CACHED: 2026-05-21 UTC
> SCOPE: AKD1000 (Akida 1.0 — edge learning is 1.0-ONLY)

## Headline

**On-chip / edge learning is supported ONLY on AKD1000 (Akida 1.0).**  Akida 2.0 dropped this in favor of off-chip TENNs training.  This is one of the key reasons anima Pack targets AKD1000 specifically — Hebbian / 1-shot / Tension-link learning **needs** on-chip update silicon.

## Hard constraints

Per `user_guide/akida.html#learning-constraints`:

1. **Only the last layer** can be trained on-chip
2. The trainable layer **must be `FullyConnected`**
3. The trainable layer **must have binary weights** (`weights_bits=1`)
4. The trainable layer **must have binary inputs** (i.e., previous layer's `act_bits=1`)
5. The optimizer must be `akida.AkidaUnsupervised`

Pack adapter implication: every adapter that uses `.fit()` on AKD1000 must compile its trainable head as:

```python
FullyConnected(units=N, weights_bits=1, act_bits=1, name='trainable_head')
```

## API: `akida.AkidaUnsupervised`

```python
from akida import AkidaUnsupervised

optimizer = AkidaUnsupervised(
    num_weights,                # int — MANDATORY — active connections per neuron
    num_classes=1,              # int — divides neurons into class groups (enables supervised)
    initial_plasticity=1.0,     # float ∈ [0, 1] — high = freely modifiable
    learning_competition=0.0,   # float ∈ [0, 0.5] — competitive inhibition
    min_plasticity=0.1,         # float ∈ [0, 1] — floor for plasticity decay
    plasticity_decay=0.25,      # float ∈ [0, 1] — how fast plasticity drops per learn
)
```

| Param | Meaning | Pack default |
|---|---|---|
| `num_weights` | active connections per neuron (sparse — should be ≤ 50% of input fan-in; rule of thumb `1.2 × median_spikes`) | 4 (for 8-neuron pool) |
| `num_classes` | when > 1, neurons are grouped into per-class clusters | depends on adapter |
| `initial_plasticity` | "learning rate" analog at first step | 1.0 (full plasticity) |
| `learning_competition` | bigger → more neuron specialisation | 0.1 (Akida tutorial KWS) |
| `min_plasticity` | plasticity never drops below this | 0.1 |
| `plasticity_decay` | per-fit plasticity reduction | 0.25 |

## Usage pattern

```python
from akida import Model, InputData, FullyConnected, AkidaUnsupervised

# 1. build / load model with binary FC head
m = Model()
m.add(InputData(input_shape=(8, 1, 1), input_bits=1))
m.add(FullyConnected(units=8, weights_bits=1, act_bits=1, name='snn_pool'))

# 2. compile with edge-learning optimizer
m.compile(optimizer=AkidaUnsupervised(
    num_weights=4,
    num_classes=8,
    learning_competition=0.1,
))

# 3. (optional) map to AKD1000 — fit() runs on-chip
m.map(akida.devices()[0])

# 4. one-shot / few-shot learning
import numpy as np
x = np.array([[[[1]],[[0]],[[1]],[[0]],[[1]],[[0]],[[1]],[[0]]]], dtype=np.uint8).reshape(1,8,1,1)
y_labels = np.array([3], dtype=np.int32)  # NOT one-hot!

m.fit(x, y_labels)              # single-shot Hebbian on AKD1000

# 5. add new classes incrementally (anima Tension Link 5-ch use case)
m.add_classes(2)                # now 10 classes
m.fit(x_new, y_new_labels.astype(np.int32))
```

## num_weights / num_neurons estimation (per `plot_2_edge_learning_parameters.html`)

```python
# 1. forward training samples to count spike density
spikes = model_feature_extractor.forward(x_train[:1000])   # uint8 → int spikes
median_spikes = np.median(spikes.sum(axis=(1, 2, 3)))

# 2. set num_weights = 1.2 × median active spikes
num_weights = int(1.2 * median_spikes)

# 3. neurons-per-class: sweep, pick inflection point of accuracy
for k in (1, 4, 16, 64, 256):
    test_model.compile(optimizer=AkidaUnsupervised(num_weights=num_weights,
                                                   num_classes=N_CLASSES * k))
    # train, measure, pick k at accuracy plateau
```

Pack adapter shortcut: for 8-neuron pools, `num_weights = 4` (50% sparsity) is a safe default.

## Constraint: samples per class > neurons per class

You can't have more class-neurons than training samples for that class (would leave neurons un-bound). For 1-shot Tension-link learning, this means **neurons_per_class = 1** strictly.

## `add_classes(n)` — incremental learning

Allows adding new classes WITHOUT retraining existing weights:

```python
m = Model("base.fbz")           # 33 trained classes
m.add_classes(3)                # now 36
m.fit(x_new_samples, y_new_labels.astype(np.int32))
# original 33 classes still classify correctly (87.67% retained per KWS demo)
```

Pack `MemristorHybridAdapter` + `MotivationGateAdapter` use this to grow concept-vocabulary on the fly.

## Pack mock vs HW edge learning divergence

| Pack mock (before) | Real AKD1000 | Fix |
|---|---|---|
| `MockModel.fit(x, target)` — Hebbian outer-product on float | `.fit(uint8, int32_labels)` — opaque AkidaUnsupervised | mock now: `.fit(inputs, input_labels)` where `input_labels` is `int32` |
| no `.compile()` | `.compile(optimizer)` mandatory before `.fit()` | mock now raises if `.fit()` called without prior `.compile()` |
| no `AkidaUnsupervised` | mandatory optimizer class | mock now exposes `MockAkidaUnsupervised` with full signature |
| no `add_classes(n)` | required for incremental | mock now exposes `.add_classes(n)` (grows weight matrix) |
| lr=0.01 hardcoded | `initial_plasticity` / `plasticity_decay` parameterised | mock now uses optimizer params to compute effective lr |

## Honest C3

1. The actual on-chip learning algorithm is **not Hebbian** — it's an opaque BrainChip "competitive winner-takes-all" + plasticity decay. Mock's Hebbian outer-product is a **sw approximation** — byte-parity with real AKD1000 is NOT expected (F-AKIDA-*-5-PARITY tests will need calibration on real silicon).
2. Edge learning runs in fractions of a millisecond per sample — the 0.18 s for 480 samples (KWS example) includes I/O. Pack falsifier timing budgets should NOT assert "≤ X ms on AKD1000" until real-HW baseline measured.
3. `num_neurons_per_class` of 15 (KWS) is for 33 classes with ~100 samples/class. For anima 8-neuron pool with single-class, use 1 (1-shot per Tension Link 5-ch).
4. `add_classes()` may have a max-classes ceiling per AKD1000 (1024 hard limit on output neurons of any FC layer per § FullyConnected constraints — 57334 / weights_bits=1 / sparsity factor → ~ 1024 effective class slots).
5. Edge learning quality depends entirely on the **frozen feature extractor** preceding the FC head — toy 8-pool adapters won't show meaningful cross-sample generalization (which is fine for substrate validation).
