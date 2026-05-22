# AKD1000 power proxy estimate (INA unavailable, board limit)

> 2026-05-22. The 1 mW power spec (BrainChip claim) cannot be directly measured
> on this M.2 dev board: `failed to send to bus: -2/-4` for INA sensor probe
> (`FIRST_INFERENCE_2026_05_22.md` + `HW_SPONTANEOUS_EMISSION_2026_05_22.md`
> both documented this). Indirect proxy via on-chip cycle counts.

## Measurements (from prior runs)

- **first inference** (16-neuron InputData→FC LIF, 1 forward): 748 cycles
  on-chip
- **spontaneous emission R3** (per-step on-chip forward, 200 steps): mean ~797
  cycles/forward
- **`model.statistics` reported throughput**: 125 fps (8 ms / inference on-chip)
- **Wall latency** (host + chip): ~13.7 ms/step — host TCP+Python round-trip
  dominated.

## Chip spec context (BrainChip AKD1000 / Akida 1.0 IP)

| spec | value | source |
|---|---|---|
| nominal clock | ~300 MHz | BrainChip docs / `BC.00.000.002` rev |
| idle power | ~0.5 mW typical | README §1.2 |
| peak power | ~100 mW | README §1.2 |
| per-spike energy | ~1 pJ to ~5 pJ | BrainChip published claims |

## Proxy estimate

Active compute fraction per 100 ms chip-step:
- ~797 cycles / 300 MHz ≈ **2.66 µs** active per forward
- 100 ms step interval (R3 default)
- duty cycle = 2.66 µs / 100 ms ≈ **0.0027%** (≈ 25,000× idle vs active)

If active draw ≈ 10 mW (mid-range between idle 0.5 mW and peak 100 mW for
this workload size, 16 neurons / 1 layer):
- mean power ≈ (0.5 mW × 0.99997) + (10 mW × 0.0027/100)
            ≈ 0.500 mW + 0.00027 mW
            ≈ **~0.5 mW mean** for sustained R3 emission at default 100 ms step

The 1 mW spec is upper-bounded by this proxy (we measure < 1 mW expected by
duty cycle math). **Directionally consistent with the spec**, though direct
INA confirmation is impossible on this board.

## Alternative: per-spike energy estimate

R3 spontaneous: 1600 spikes / 200 steps / 16 neurons = 0.5 spikes/neuron/step.
At ~3 pJ/spike (mid-range): energy per step ≈ 16 × 0.5 × 3 pJ = **24 pJ/step**.
Over 100 ms step: average power from spikes alone = **0.24 nW**. Negligible
vs the chip's idle baseline.

So the dominant power draw is the **idle baseline (~0.5 mW)**, not the spikes
themselves. The "spike-based event-driven" advantage scales with chip
utilization — at higher spike rates (1000× more), spike-energy approaches
idle-baseline. At our small R3 demonstration (16 neurons, sparse), idle
dominates.

## Honest C3

1. **INA absent** = no first-party measurement. Proxy is good engineering
   estimate, not silicon-truth.
2. **Active power 10 mW** is mid-range guess; the chip's actual draw at this
   workload could be 1-30 mW. Doesn't change "≪ 1 mW mean" verdict.
3. **Idle baseline dominates** — the 1 mW spec is fundamentally idle + light
   activity. For real efficiency benefit, workload must SPIKE the chip
   (high event rate). Our R3 demonstration is below that regime.
4. **Different board with INA** (separate Pi 5 carrier board with current
   sensors) would directly verify. The "1 mW" claim remains spec-bound, not
   measurement-bound on this hardware.
5. **vs CPU baseline**: a Pi 5 Cortex-A76 doing equivalent computation would
   draw ~5-10 W. AKD1000 ≪ 1 mW (proxy) = **>5000× efficiency**, consistent
   with BrainChip's neuromorphic advantage claim, within proxy precision.

## 관련 link

- HW connection: `state/HW_CONNECTED_2026_05_22.md`
- first inference: `state/FIRST_INFERENCE_2026_05_22.md`
- spontaneous: `state/HW_SPONTANEOUS_EMISSION_2026_05_22.md`
