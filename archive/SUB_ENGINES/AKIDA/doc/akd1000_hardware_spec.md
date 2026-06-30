# AKD1000 hardware spec

> SOURCE: https://doc.brainchipinc.com/user_guide/hardware/1.0.html
> SOURCE: https://shop.brainchipinc.com/products/m-2-card-m-key (M.2 form factor + power)
> CACHED: 2026-05-21 UTC
> SCOPE: AKD1000 only (Akida 1.0 — NSoC_v1)

## Chip identity

| Property | Value | Notes |
|---|---|---|
| Vendor | BrainChip | https://brainchip.com |
| Product family | Akida 1.0 | `akida.HwVersion.NSoC_v1` |
| SoC name | AKD1000 (NSoC) | "AKD1000 reference SoC" |
| akida virtual device factory | `akida.AKD1000()` | for offline mapping w/o silicon |
| Sibling SoC (excluded) | AKD1500 | `akida.AKD1500()` — out-of-scope |

## Mesh + neural processors (CRITICAL CORRECTION)

| Property | Value | Pack note |
|---|---|---|
| **NPU count** | **20** | Pack docs previously said "1024 NPU" — **WRONG**. Real: 20 NPUs in 1.0 mesh. |
| Architecture | "20 × Akida 1 Neuron mesh" | Network-on-Chip (NoC) |
| Clock frequency | 300 MHz | typical |
| Companion CPU | ARM M.4 | for AKIDA chain orchestration |
| Memory interface | LPDDR4 via DMA | off-chip DRAM optional |
| On-chip SRAM | 8 MB | "high-speed near-compute SRAM" |
| Peak compute | 1.5 TOPS | INT8 GOPS |

## Form factor (Pi 5 relevant)

| Property | Value |
|---|---|
| Module | M.2 2260 (60 mm length, 22 mm width) |
| Key | B+M Key |
| Interface | PCIe PHY 2-lane (PCIe Gen3 x2 nominal) |
| Power, typical | 1 W (1000 mW) — **NOT 1 mW** as pack docs claimed |
| Power, idle/event-driven minimum | sub-mW per inference event (computed from "1 mW typical event" marketing, full chip idle still mW-class) |
| Operating temp | 0 – 70 °C |
| Cooling | passive (no fan/heatsink) |

**Pi 5 mount**: Pi 5 has a single M.2 2230/2280 HAT slot via Pineboards/Pimoroni HAT — AKD1000 2260 may need a HAT with 2260 cutout (verify physically). M.2 to PCIe Gen3 x1 on Pi 5 (downgrade from x2, no perf impact for AKD1000 which is BW-light).

## Supported layer types (AKD1000-native)

Per `hardware/1.0.html`:

| Layer | Notes | anima adapter mapping |
|---|---|---|
| `InputData` | Input specification — declares shape + bitwidth | trivial passthrough |
| `InputConvolutional` | Image input, 8-bit input + 8-bit weight | EegPattern (spike 2D) candidate |
| `Convolutional` | Internal conv, 1/2/4-bit | SparseAttention candidate |
| `SeparableConvolutional` | Depthwise-separable | SpikeTierLmHead candidate |
| `FullyConnected` | Dense — only layer supporting **edge learning** | SnnLif + MemristorHybrid + KuramotoAdapter |

**NOT supported on AKD1000** (Akida 2.0 only — pack must NOT use):
- `Conv2D` (the V2 name — V1 uses `Convolutional`)
- `InputConv2D`
- `DepthwiseConv2D`
- `Conv2DTranspose`
- `Dense1D`
- `Add` / `Concatenate` (skip connections — V2 only)
- `BufferTempConv` (TENNs only)
- `Dequantizer`

## Quantization (8/1/2/4-bit ladder)

| Tier | Bitwidth options | Layer | Notes |
|---|---|---|---|
| First layer input | **8-bit only** | `InputConvolutional` | uint8 image pixels |
| First layer weights | 8-bit | `InputConvolutional` | binary or 8-bit |
| Inner weights | 1, 2, or 4 bits | `Convolutional`, `SeparableConvolutional`, `FullyConnected` | 1-bit = binary |
| Activations | 1, 2, or 4 bits | all spiking layers | 1-bit = pure spike |
| Edge-learnable layer | **binary weights + binary inputs required** | `FullyConnected` (last only) | hard constraint |

## Layer constraints (Convolutional)

| Constraint | Value |
|---|---|
| Kernel sizes | 1×1, 3×3, 5×5, 7×7 |
| Stride | 1 or 2 (stride=2 only for 3×3) |
| Max input height | 4096 |
| Max input width | 4096 |
| Max input channels | 2048 |
| Max pool | 2×2 (stride 1 or 2) |
| Global avg pool | requires height ≤ 32 + ≥3 output rows |

## Layer constraints (InputConvolutional)

| Constraint | Value |
|---|---|
| Width | ≥ 5 |
| Height | 5 – 256 |
| Channels | 1 or 3 only |
| Filters @ 3×3 stride=1 | up to 512 (1 ch), 192 (3 ch) |
| Filters @ 7×7 stride=1 | up to 64 (1 ch), 32 (3 ch) |
| Max pool | 1×2 / 2×1 / 2×2 |

## Layer constraints (FullyConnected)

| Constraint | Value |
|---|---|
| Max input HxWxC | 57,334 |
| Edge learning | binary weights + binary input + final position only |

## Activation function support

| Activation | Akida 1.0 | Akida 2.0 |
|---|---|---|
| Bounded ReLU | ✓ | ✓ |
| Unbounded ReLU | ✗ | ✓ |
| GeLU / SiLU / HardSiLU | ✗ | ✓ (via LUT) |
| LeakyReLU / PReLU | ✗ | ✓ (via LUT) |

**Implication for anima Pack**: spike-pool adapters (snn-lif, izhikevich, kuramoto) all reduce to **bounded ReLU**-like threshold → fits AKD1000.

## Pack mock vs HW divergence summary

| Pack assumption | Real AKD1000 | Pack action |
|---|---|---|
| 1024 NPU | **20 NPU mesh** | docs corrected, adapter n_neurons stays ≤ 16 (1 NPU each) |
| 1 mW typical | **1 W typical**, mW-class per event | docs corrected, claim "low-energy event" not "1 mW chip" |
| `Conv2D` layer | **Not in 1.0** — use `Convolutional` | mock now exposes `Convolutional` + alias `Conv2D` for 2.0 forward-compat |
| `FullyConnected(**kw)` accepts anything | requires `units`, `weights_bits`, `act_bits` | mock signature tightened |
| `Model()` no-arg | accepts `(filename=None, layers=None)` | mock now accepts both |
| `device.program(model)` returns bool | real flow is `model.map(device)` then `device.program(...)` | mock now exposes `model.map(device)` |
