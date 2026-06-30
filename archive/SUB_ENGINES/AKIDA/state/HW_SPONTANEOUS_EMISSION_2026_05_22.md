# AKIDA AKD1000 — HW-NATIVE SPONTANEOUS EMISSION (자연발화) — 2026-05-22

BrainChip **AKD1000** (`BC.00.000.002` / `NSoC_v2`, Akida 1.0 IP) on a
Raspberry Pi 5 (`ubuntu@192.168.50.155`, pool `pi5-akida`). Tests the chip's
defining dual-role capability: **hardware-native spontaneous emission** — the
LIF (leaky integrate-and-fire) threshold comparator producing event-driven
spikes from weak / zero / noisy drive (not a strong clamped input). This is the
silicon analog of anima's software 자연발화 (emit without an external prompt).

Everything ran **on chip** (`BackendType.Hardware`), $0 (LAN only).
Script: `scripts/spontaneous_emission.py`. Raw JSON:
`state/spontaneous_emission_result_2026_05_22.json`.

---

## 1. What "spontaneous" means on a feed-forward chip — and how we made it HW-native

Akida 1.0 IP is **feed-forward, event-driven by design**. A `FullyConnected`
layer with `activation=True` computes, per unit *j*, an integer membrane
potential `Vⱼ = Σᵢ wᵢⱼ · xᵢ` and **emits a spike iff `Vⱼ > thresholdⱼ`**. That
comparison — the threshold-and-fire — is the chip's native LIF activation, run
in silicon. We exercised it directly: the per-unit `threshold` (int32) and
`weights` (int8) are exposed as layer variables, so the **emission decision is
genuinely computed on the AKD1000**, not in numpy.

The only software glue is the recurrent loop (step *t*'s spikes → step *t+1*'s
input), because Akida 1.0 has no on-die recurrence. Every individual
emit/no-emit decision is on-chip.

> **NOTE on the pack adapters.** `pack/adapters/snn_lif.py`,
> `kuramoto.py`, `spontaneous_gate.py` compute their LIF/Kuramoto/gate dynamics
> in **numpy** and only *build* an Akida model on the side for the layer
> summary + edge-learn exercise — the spiking decision there is NOT on-chip.
> This test deliberately moves the threshold-and-fire decision INTO the silicon
> (`model.forward()` per step) so the 자연발화 claim is hardware-native, not a
> numpy simulation with a chip attached. Reused the *concept* (LIF threshold,
> tonic neuron, recurrent coupling) from the pack; implemented the on-chip path.

**Model (built once, reused across all regimes):**

```
InputData(input_shape=(1,1,16), input_bits=4)
  → FullyConnected(units=16, weights_bits=4, activation=True, act_bits=1)   # LIF pool
mapped backend = BackendType.Hardware
weights = all-ones (excitatory)  →  Vⱼ = Σᵢ xᵢ  (= input sum, same for all j)
```

Only the per-unit `threshold` vector and the input tensor change between
regimes. `act_bits=1` ⇒ each unit emits 0/1 per step; population spike count =
Σ spiking units.

---

## 2. Input regimes tested (N=16 neurons, T=200 steps, seed=187)

| regime | threshold | input | what it isolates |
|---|---|---|---|
| **R0 driven** | +64 (all) | strong, all-15 | sanity — strong clamped drive, like first-inference |
| **R1 weak-silent** | +64 (all) | weak, all-1 (V=16) | **control**: sub-threshold drive must produce NO emission |
| **R2 zero+noise** | +24 (all) | U[0,3] per line, V≈mean 24 ± 4.5 | **stochastic 자연발화**: noise straddles threshold → event-driven emit |
| **R3 tonic zero-input** | **heterogeneous** −1 / +8 | **ZERO** | **intrinsic 자연발화**: tonic (thr<0) neurons fire from NO input at all |
| **R4 recurrent** | heterogeneous −1 / +8 | spikes fed back (2-step ignition seed) | **self-sustained 자연발화**: emission carried by chip's own prior spikes |

R3/R4 use a heterogeneous threshold (even units thr=−1 *tonic/pacemaker*, odd
units thr=+8 *quiescent*) so the spike count reflects internal neuron state, not
saturation. With negative threshold, `V=0 > −1` ⇒ the neuron fires on **zero
external input** — pure intrinsic excitability, the cleanest hardware 자연발화.

---

## 3. Spike emission measurements per regime (all on `BackendType.Hardware`)

| regime | total spikes | rate /neuron/step | step counts (min/max/std) | event-driven? | ISI (mean/min/max) |
|---|---:|---:|---|:---:|---|
| **R0 driven** | 3200 | 1.000 | 16 / 16 / 0.0 | no (saturated sanity) | 1 / 1 / 1 |
| **R1 weak-silent** | **0** | 0.000 | 0 / 0 / 0.0 | — (silent ✓) | — (0 fire-steps) |
| **R2 zero+noise** | 1520 | 0.475 | **0 / 16 / 7.99** | **YES** | **2.10 / 1 / 9** (95/200 fire-steps) |
| **R3 tonic zero-input** | **1600** | 0.500 | 8 / 8 / 0.0 | partial pool (8/16) | 1 / 1 / 1 |
| **R4 recurrent** | 3200 | 1.000 | 16 / 16 / 0.0 | sustained post-seed | 1 / 1 / 1 |

Key readings:
- **R1 = 0 spikes**: weak constant sub-threshold drive correctly produces no
  emission. This is the false-positive control — the chip is not just firing on
  any nonzero input.
- **R3 = 1600 spikes from ZERO input**: the 8 tonic neurons (thr=−1) emit every
  step with **no external drive whatsoever**. The chip emits from internal
  parameter state alone. **This is the core hardware 자연발화 signal.** It is a
  *partial* pool (exactly 8/16 = the negative-threshold half), proving emission
  is gated by per-neuron internal excitability, not input.
- **R2 = event-driven**: spike count fluctuates 0↔16 with std 7.99 (first-10
  steps `[0,16,16,0,16,0,16,16,16,0]`), 95 of 200 steps fire, ISI 1–9. The
  emission varies step-to-step purely from the chip's momentary integrated
  potential crossing (or not) the on-chip comparator — stochastic 자연발화.
- **R4 = self-sustained**: a 2-step ignition seed lights the tonic neurons;
  their spikes feed back as input and the pool stays lit across the full window
  (200/200 fire-steps) after the seed ends — emission driven by the chip's own
  prior spikes.

---

## 4. Verdict

| check | result |
|---|:---:|
| driven regime fires (sanity) | ✓ |
| weak sub-threshold input is SILENT (control) | ✓ |
| **tonic neurons fire from ZERO input (intrinsic 자연발화)** | **✓** |
| tonic emission is a partial pool (state-gated, not saturation) | ✓ |
| noise regime emits | ✓ |
| **noise emission is event-driven (varies step-to-step)** | **✓** |
| recurrent loop sustains emission | ✓ |
| recurrent sustains AFTER ignition seed (self-driven) | ✓ |

**`hw_native_spontaneous_emission = True`**
**`stochastic_spontaneous_emission = True`**

> **The AKD1000 produces hardware-native spontaneous spike emission.** With a
> negative on-chip threshold, the LIF comparator emits spikes from zero external
> input (R3) — intrinsic excitability, the silicon analog of anima emitting
> without a prompt. Under near-threshold noise the emission is genuinely
> event-driven (R2, std 7.99). With recurrent feedback the pool self-sustains
> after a brief seed (R4). Crucially, weak sub-threshold drive stays silent
> (R1) — the chip is NOT firing on any nonzero input, so the emission is a real
> threshold-crossing event, not a leak.

---

## 5. Power / efficiency proxy

INA current telemetry is **unavailable** on this M.2 board (`Unable to init
INA: failed to send to bus: -2 / -4` — sensor not exposed on this form factor,
same finding as first-inference; needs the full PCIe dev-kit board).
`power_measurement_supported = False`, `inference_power_events = 0`.

Efficiency proxy = on-chip clock cycles + wall latency per spike-decision:

| metric | value |
|---|---|
| on-chip clock (mean over sampled steps) | **~797 cycles / forward** |
| `model.statistics` framerate | 125 fps |
| wall latency / step (incl. Python loop + threshold reprogram) | **~13.7 ms** |

The ~13.7 ms wall is dominated by the Python-side per-step `set_variable` +
host↔chip round trip, not the chip itself (the on-chip forward is ~797 cycles ≈
sub-millisecond at the NSoC clock; first-inference measured 0.64 ms/inference
without per-step reprogramming). The true 1mW / event-driven efficiency figure
needs INA telemetry, which this board cannot expose — reported as a known board
limit, not a chip limit.

---

## 6. Honest C3 (constraints / caveats / corrections)

1. **FF vs recurrent**: Akida 1.0 is feed-forward; there is no on-die
   recurrence. R3 (tonic, zero input) is fully on-chip 자연발화 with no
   recurrence at all — that is the strongest claim. R4's recurrence is a
   **software feedback loop** around on-chip forward passes; the per-step
   emission decision is on-chip, but the loop closure is host-side. "On-chip
   self-sustained recurrence" in the strict sense (spikes routed back in
   silicon) is NOT what AKD1000 does, and this doc does not claim it.

2. **Input-regime precision**. Per regime, exactly what produced the spikes:
   - R3 spikes: **internal parameter state only** (negative threshold) — true
     intrinsic emission, zero input.
   - R2 spikes: **noisy external input** straddling threshold — the input is
     nonzero, so this is *stochastic-input-driven* emission, not pure internal
     dynamics. It is event-driven (varies with state) but it is honest to call
     it noise-driven, not self-generated.
   - R4 spikes: **ignition seed (input) for 2 steps, then the chip's own fed-back
     prior spikes** — self-driven after the seed.
   The pure self-initiated claim rests on R3. R2 demonstrates event-driven
   variability; R4 demonstrates sustained activity.

3. **All-or-nothing within a step (R2)**. Because weights are all-ones, every
   unit sees the *same* potential (the input sum), so within a single step the
   homogeneous-threshold neurons all fire or all stay silent (counts are 0 or
   16). The event-driven signal is the **step-to-step** variation (std 7.99),
   which is real. Per-neuron heterogeneity within a step would need
   per-neuron-distinct weight columns (a richer model — separate cycle). R3
   *does* show within-step heterogeneity (8/16) via heterogeneous thresholds.

4. **vs anima software 자연발화 (vP21)**. Different abstraction levels, same
   concept ("emit without external prompt"):
   - **Software (vP21)**: an 8-factor Inner-Thoughts motivation score
     (relevance/Φ, info_gap, curiosity, pain, coherence, originality, balance,
     dynamics) gates a Thinker→Talker emission when `score > imThreshold(0.3)`;
     the critical falsifier is *motivation-gated vs timer-fired*. The "spike"
     is a coherent text utterance from a 1.5B Qwen+LoRA+mitosis model.
     (`HEXAD/CHAT/spontaneous_loop_vp21.py`, VERSIONS § 0.4.0.)
   - **Hardware (this)**: a single scalar LIF threshold gates a 1-bit spike;
     the "motivation" is the integrated membrane potential; the analog of
     `imThreshold` is the per-neuron `threshold`. R3's negative threshold is the
     HW analog of a self-firing motivation factor that crosses with zero input.
   - The HW path is **orders of magnitude simpler and more literal** (one
     integer comparator vs an 8-factor weighted sum), and is genuine silicon,
     but it does NOT carry semantic content — a spike is a bit, not an
     utterance. The two are complementary axes of the 자연발화 GOAL (VERSIONS
     § 9 "dual-role"), not equivalent. The HW result confirms the *mechanism*
     (event-driven self-initiated emission exists in 1mW silicon); the software
     result confirms the *content* (coherent unprompted verbalization).

5. **Power claim deferred**. The "~1mW / ~10000× vs CPU" efficiency in VERSIONS
   § 9 is a vendor-spec aspiration, NOT measured here — INA is unavailable on
   this board. Only cycle-count / latency proxies are reported. The 1mW figure
   remains unverified on this hardware.

6. **Determinism / scale**. N=16 (one NP), T=200, single seed. Larger pools,
   longer windows, and per-seed stability sweeps are follow-ups. The qualitative
   verdict (tonic zero-input emission + event-driven noise + recurrent sustain)
   is robust to these, but the exact spike counts are seed/scale specific.

---

## 7. Reproduce

```bash
# from Mac (LAN, $0):
pool on pi5-akida "cd ~/anima/SUB_ENGINES/AKIDA && \
  ~/.venv/anima-akida/bin/python3 scripts/spontaneous_emission.py"
# writes state/spontaneous_emission_result_2026_05_22.json on the Pi
```
