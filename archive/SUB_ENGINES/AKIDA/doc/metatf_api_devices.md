# MetaTF API — Device + NP

> SOURCE: https://doc.brainchipinc.com/api_reference/akida_apis.html#device
> SOURCE: https://doc.brainchipinc.com/api_reference/akida_apis.html#np
> SOURCE: https://doc.brainchipinc.com/user_guide/akida.html#devices
> CACHED: 2026-05-21 UTC
> SCOPE: AKD1000 (Akida 1.0 NSoC_v1)

## Device discovery

```python
import akida
devs = akida.devices()       # list of HwDevice
```

| Function | Returns | Notes |
|---|---|---|
| `akida.devices()` | `list[akida.HwDevice]` | empty list if no AKD1000 detected |
| `akida.AKD1000()` | `akida.Device` (virtual) | for host-only testing without silicon |
| `akida.AKD1500()` | `akida.Device` (virtual) | sibling chip — out-of-scope |
| `akida.TwoNodesIPv1()` | `akida.Device` (virtual) | small FPGA — out-of-scope |
| `akida.TwoNodesIPv2()` | `akida.Device` (virtual) | V2 FPGA — out-of-scope |
| `akida.SixNodesIPv2()` | `akida.Device` (virtual) | V2 FPGA — out-of-scope |

## `akida.Device` (base class)

| Property | Type | Notes |
|---|---|---|
| `version` | `akida.HwVersion` | enum value — for AKD1000: `HwVersion.NSoC_v1` |
| `ip_version` | tuple/str | IP revision identifier |
| `mesh` | `akida.NP.Mesh` | NP layout descriptor |
| `desc` | `str` | human-readable device description |

## `akida.HwDevice` (real silicon)

Inherits from `Device`, adds physical-IO surface:

| Property/Method | Notes |
|---|---|
| `soc` | `akida.SocDriver` — SoC-level control (clock, power) |
| `program(buffer)` | low-level program load (usually called via `model.map()`) |
| `power_meter` | `akida.PowerMeter` — energy measurement instance |

## `akida.HwVersion` (enum)

```python
class HwVersion(enum.Enum):
    NSoC_v1 = ...   # AKD1000 — current pack target
    NSoC_v2 = ...   # AKD2000 (future) — out-of-scope
```

Pack adapter should assert:

```python
dev = akida.devices()[0]
assert dev.version == akida.HwVersion.NSoC_v1, \
    f"expected AKD1000 (NSoC_v1), got {dev.version}"
```

## `akida.SocDriver`

| Property | Notes |
|---|---|
| `power_measurement_enabled` | bool — set True before forward() to record power |
| `clock_mode` | `akida.ClockMode` enum (`Performance`, `Economy`, `LowPower`) |

```python
dev.soc.power_measurement_enabled = True
dev.soc.clock_mode = akida.ClockMode.Economy
model.forward(x)
print(dev.power_meter.events)         # per-event readings
print(dev.power_meter.total_energy)   # joules
```

## `akida.ClockMode`

| Value | Meaning |
|---|---|
| `Performance` | max clock (300 MHz on AKD1000) |
| `Economy` | balanced |
| `LowPower` | minimum clock (event-driven idle) |

## `akida.NP.Mesh` (NPU layout descriptor)

For AKD1000:
- **20 NPUs** arranged in NoC mesh
- pack docs **NO LONGER** say "1024 NPU" — that was scaled-up FPGA marketing
- mesh layout: NoC topology, exact rows/cols accessible via `dev.mesh.nps`

```python
dev = akida.devices()[0]
mesh = dev.mesh                 # akida.NP.Mesh
for np_info in mesh.nps:        # iterate NP.Info
    print(np_info.ident, np_info.type, np_info.memory)
```

## `akida.NP.Component`

Returned by `model.map()` per layer — describes which NP a layer was mapped to.

```python
model.map(dev)
for seq in model.sequences:
    for comp in seq.components:
        print(comp.layer_name, comp.np_ident)
```

## `akida.NP.MemoryInfo` / `akida.NP.SramSize`

Per-NP memory stat for mapping feasibility checks.

| Field | Notes |
|---|---|
| `sram_size` | bytes — typically ~409 KB per NP on AKD1000 (8 MB / 20 NPUs) |
| `used` | bytes — populated after `model.map()` |

## `akida.MapMode` (enum)

| Value | Strategy |
|---|---|
| `AllNps` | default — distribute across all 20 NPUs (highest throughput) |
| `HwPr` | concurrent w/ partial reconfiguration (multi-model sharing) |
| `Minimal` | use fewest NPUs possible (lowest power) |

For anima Pack 8-neuron pools → `Minimal` mode wastes nothing (1 NP suffices).

```python
from akida import MapMode
model.map(dev, mode=MapMode.Minimal)
```

## `akida.MapConstraints`

Advanced NP allocation — pin specific layers to specific NPs. Not needed for anima 8-neuron pools.

## Pack mock vs HW device divergence

| Pack mock (before) | Real AKD1000 device | Fix |
|---|---|---|
| `MockDevice.name` | `Device.version` + `Device.desc` | mock now exposes `.version = HwVersion.NSoC_v1` (mock enum) + `.desc = "AKD1000_MOCK"` |
| `MockDevice.program(model) → bool` | not a public API — use `model.map(device)` | mock now exposes `model.map(device)`; `.program()` kept as deprecated alias returning `True` |
| no `mesh` | `Device.mesh` returns NP.Mesh | mock exposes mock mesh with `.nps = list of 20 mock NP.Info objects` |
| no `soc.power_measurement_enabled` | required for power tracking | mock exposes `.soc.power_measurement_enabled` (no-op bool) |
| no `MapMode` | enum required for `.map()` | mock exposes `MapMode.{AllNps, HwPr, Minimal}` enum |
| no `HwVersion` | required for assert | mock exposes `HwVersion.NSoC_v1` |
