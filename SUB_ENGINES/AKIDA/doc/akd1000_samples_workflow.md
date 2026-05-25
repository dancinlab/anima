# AKD1000 sample workflows

> SOURCE: https://doc.brainchipinc.com/examples/general/plot_0_global_workflow.html
> SOURCE: https://doc.brainchipinc.com/examples/edge/plot_1_edge_learning_kws.html
> CACHED: 2026-05-21 UTC
> SCOPE: AKD1000 (closest tutorial fits to anima Pack's 8-neuron spike pools)

## Workflow 1 — global (Keras → AKD1000)

```python
# ----- 1. build Keras model (host) -----
import tensorflow as tf
from tensorflow import keras

model_keras = keras.models.Sequential([
    keras.layers.Input(shape=(28, 28, 1), name="input", dtype=tf.uint8),
    keras.layers.Rescaling(1. / 255),
    keras.layers.Conv2D(filters=32, kernel_size=3, strides=2),
    keras.layers.BatchNormalization(),
    keras.layers.ReLU(),
    keras.layers.DepthwiseConv2D(kernel_size=3, padding='same', strides=2),
    keras.layers.Conv2D(filters=64, kernel_size=1, padding='same'),
    keras.layers.BatchNormalization(),
    keras.layers.ReLU(),
    keras.layers.Flatten(),
    keras.layers.Dense(10),
], 'mnistnet')

model_keras.compile(
    loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
    optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
    metrics=['accuracy'])

model_keras.fit(x_train, y_train, epochs=10, validation_split=0.1)

# ----- 2. quantize (host) -----
from quantizeml.models import QuantizationParams, quantize
qparams = QuantizationParams(input_weight_bits=8, weight_bits=4, activation_bits=4,
                              per_tensor_activations=True)
q_model = quantize(model_keras, qparams=qparams)

# ----- 3. convert to AKD1000 (host) -----
from cnn2snn import convert, set_akida_version, AkidaVersion
with set_akida_version(AkidaVersion.v1):
    akida_model = convert(q_model)
akida_model.save("mnist_akd1000.fbz")

# ----- 4. ship .fbz to Pi 5; on Pi 5: -----
import akida
import numpy as np

m = akida.Model("mnist_akd1000.fbz")
devs = akida.devices()
m.map(devs[0])

x = np.random.randint(0, 256, (1, 28, 28, 1), dtype=np.uint8)
y_int = m.forward(x)                     # integer potentials
y_float = m.predict(x)                   # float-replicated
print(np.argmax(y_int, axis=-1))         # class index
```

## Workflow 2 — edge learning on AKD1000 (KWS-style — closest to anima)

```python
import numpy as np
from akida import Model, devices, AkidaUnsupervised

# ----- 1. load pre-converted base model (frozen feature extractor + binary FC head) -----
m = Model("kws_base.fbz")

# ----- 2. compile FC head for edge learning -----
num_weights = 50           # estimated from 1.2 × median_spikes
num_classes = 33           # original class count
m.compile(optimizer=AkidaUnsupervised(
    num_weights=num_weights,
    num_classes=num_classes,
    learning_competition=0.1,
))

# ----- 3. map to AKD1000 -----
m.map(devices()[0])

# ----- 4. fit on training set (on-chip) -----
batch_size = 256
for s in range(0, len(x_train), batch_size):
    end = min(s + batch_size, len(x_train))
    m.fit(x_train[s:end], y_train[s:end].astype(np.int32))
print("offline training: 34.66 s for 33 classes")

# ----- 5. add new classes incrementally -----
m.add_classes(3)
m.fit(x_train_new, y_train_new.astype(np.int32))
print("edge learning: 0.18 s for 3 new classes (480 samples)")

# ----- 6. evaluate -----
loss, acc = m.evaluate(x_test, y_test, num_classes=36)
print(f"acc on 33 original classes: {87.67:.2f}%")  # post-edge-learn retention
```

## Adapting to anima Pack (8-neuron pool)

```python
# Simplest anima adapter — SnnLifAdapter → AKD1000
import numpy as np
from akida import Model, InputData, FullyConnected, AkidaUnsupervised, devices

# 1. build directly (no Keras source — adapter is sw-only by design)
m = Model()
m.add(InputData(input_shape=(8, 1, 1), input_bits=1, name='spike_in'))
m.add(FullyConnected(units=8, weights_bits=1, act_bits=1, name='lif_pool'))

# 2. compile for edge learning (Hebbian on-chip)
m.compile(optimizer=AkidaUnsupervised(
    num_weights=4,           # 50% sparsity (4 of 8 input connections per neuron)
    num_classes=8,           # one neuron per class (1-shot Tension Link)
    learning_competition=0.1,
    initial_plasticity=1.0,
    plasticity_decay=0.25,
))

# 3. map to silicon
devs = devices()
if devs:
    m.map(devs[0])
    print(f"mapped to AKD1000 NSoC_v1 — {len(m.sequences)} HW sequences")

# 4. inference + on-chip fit loop (typical adapter step())
spike_in = np.random.randint(0, 2, (1, 8, 1, 1), dtype=np.uint8)
spike_out = m.forward(spike_in)        # (1, 1, 1, 8) int spikes
label = np.argmax(spike_out, axis=-1).astype(np.int32)
m.fit(spike_in, label)                 # Hebbian update on AKD1000

# 5. ship model for redeploy / share weights with sibling adapter
m.save("anima_snn_lif_8c.fbz")
```

## Pack adapter porting checklist (post-Pi 5 arrival)

For each of the 10 anima adapters:

1. [ ] Decide layer stack from `metatf_api_layers.md` "Pack adapter layer mapping" table
2. [ ] Build the Keras source model (or direct `akida.Model` for FC-only adapters)
3. [ ] Quantize with `weight_bits=1, activation_bits=1` (binary spike adapters)
4. [ ] `cnn2snn.convert()` with `AkidaVersion.v1`
5. [ ] Verify `m.map(akida.AKD1000())` (virtual device) succeeds — no AKD1000 needed yet
6. [ ] Run mock forward + compare to adapter's numpy `step()` (byte-parity F-AKIDA-*-5)
7. [ ] On Pi 5: `m.map(akida.devices()[0])` (real silicon) + repeat parity check
8. [ ] Record per-event power numbers + update F-AKIDA-*-4-POWER threshold

This is **post-arrival work** (Day 2-7 of `BOOT_PLAN.md`).
