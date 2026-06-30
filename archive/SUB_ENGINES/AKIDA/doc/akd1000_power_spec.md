# AKD1000 power spec

> SOURCE: https://shop.brainchipinc.com/products/m-2-card-m-key (M.2 product page)
> SOURCE: https://doc.brainchipinc.com/api_reference/akida_apis.html#powermeter
> CACHED: 2026-05-21 UTC
> SCOPE: AKD1000 only

## Datasheet numbers

| Property | Value | Notes |
|---|---|---|
| Typical power (M.2 module, idle + light inference) | **1 W (1000 mW)** | NOT 1 mW — pack docs previously claimed "1 mW typical" — **WRONG** |
| Per-event power (event-driven inference) | sub-mW class | actual mW depends on input sparsity + clock mode |
| Peak power (sustained inference, 300 MHz, all 20 NPUs) | ~100 mW above idle (~1.1 W total) | inferred from "1 W typical" + headroom |
| Standby (clock gated) | sub-mW (NoC awake only) | event-driven re-wake on input |
| TDP envelope | 1 W total module incl. ARM M.4 + LPDDR4 PHY | passive cooling spec |
| Operating temp | 0 – 70 °C | commercial grade |
| Cooling | passive (no fan/heatsink) | true for 1 W envelope |

**Marketing claim "1 mW per inference"**: refers to ENERGY per inference event under sparse spike input (e.g. MNIST classify ≈ 1 mW × 1 ms = 1 μJ). The **chip itself** burns ~1 W on the M.2 module — the 1 mW is per-event-amortised, not chip TDP.

## `akida.PowerMeter` API

```python
dev = akida.devices()[0]
dev.soc.power_measurement_enabled = True

# run inference
out = model.forward(x)

# read
pm = dev.power_meter            # akida.PowerMeter
events = pm.events              # list[akida.PowerEvent]
total_j = pm.total_energy       # cumulative Joules since enabled
```

### `akida.PowerEvent`

| Field (inferred — exact schema TBD on real HW) | Type | Meaning |
|---|---|---|
| `inference_index` | int | which forward() call |
| `power_mw` | float | instantaneous mW during this event |
| `duration_us` | float | how long the event ran |
| `energy_uj` | float | event energy (mW × us / 1000) |

**Honest C3**: exact field names not in cached doc. Pack mock exposes a stub `MockPowerEvent` with these inferred fields — first action on real Pi 5 = `print(pm.events[0].__dict__)` to capture real schema and update mock.

## ClockMode → power tradeoff

```python
import akida

# fastest, highest power (~1.1 W peak)
dev.soc.clock_mode = akida.ClockMode.Performance

# balanced (~700 mW)
dev.soc.clock_mode = akida.ClockMode.Economy

# minimum (~200 mW, ~100 MHz effective)
dev.soc.clock_mode = akida.ClockMode.LowPower
```

For anima Pack 8-neuron pools running motivation-gate (sparse event emit ≤ 1/s), `LowPower` mode is the canonical choice.

## Pi 5 power envelope

| Component | Typical power |
|---|---|
| Pi 5 4 GB at idle | 2.5 W |
| Pi 5 with display + USB + Wi-Fi | 4 W |
| AKD1000 M.2 module typical | 1 W |
| AKD1000 peak | 1.1 W |
| **Total Pi 5 + AKD1000 worst case** | ~5.1 W |
| USB-C PD adapter required | 5V 3A (15 W) — Pi 5 stock 27W is overkill |

The AKD1000 is the **least power-hungry** component in the stack — fits within Pi 5's M.2 HAT 3.3 V rail budget without auxiliary power.

## Pack power-related falsifier strategy

Real per-event power numbers can only be measured on AKD1000 silicon. Mock fallback:

- F-AKIDA-*-4-POWER falsifier on mock: asserts `power_meter.events[-1].power_mw < 100.0` (mock returns synthetic ~5 mW per event)
- F-AKIDA-*-4-POWER on real AKD1000: replace mock value with real `pm.events[-1].power_mw`, calibration TBD post-arrival

Pack docs no longer claim "1 mW typical" — corrected to:
- typical inference event: sub-mW (event-amortised energy)
- chip TDP at idle: ~1 W (M.2 module)
- chip TDP at peak: ~1.1 W (300 MHz, all 20 NPUs active)
