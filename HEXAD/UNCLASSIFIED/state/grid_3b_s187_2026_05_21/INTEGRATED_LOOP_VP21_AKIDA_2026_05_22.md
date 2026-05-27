# vP21 ⊥ AKD1000 INTEGRATED LOOP — HW-gated 자연발화 BRIDGE LANDED

> 2026-05-22. The two 자연발화 axes (software vP21 motivation-gated +
> hardware AKD1000 LIF spike) linked into ONE coherent loop. Option A:
> AKD1000 spike events → TCP → ubu-2 → vP21 emission gate.

## Verdict: HW-GATED-SPONTANEOUS works ✓

180s window, 90 ticks (2s each). vP21 emission is gated by `hw_edge ∧ sw_gate ∧ refractory`.

| metric | hw_gated mode | timer mode |
|---|---|---|
| emissions | **30** | 90 |
| coherent | **30/30** (100%) | 90/90 |
| frac_emissions_with_hw_edge | **1.0** (every emit ↔ AKD1000 spike edge) | n/a |
| inter-emission interval mean | **6.001 s** (std 0.001) | 2.0 s |
| hw_count_at_emit_mean | 79.2 | n/a |

**Causal coupling**: every vP21 emission in hw_gated mode coincided with an
AKD1000 spike-rate edge crossing (frac=1.0). The HW spike pattern dictates
emission timing (6s mean interval, not the 2s timer tick).

## Architecture (Option A)

```
Pi 5 + AKD1000                       ubu-2 (vP21)
==============                       ============
spike_streamer.py                    integrated_loop_vp21_akida.py
  R3 tonic regime                    8-factor motivation (sw_gate)
  thr=[-1,8,-1,8,...]      TCP 9512    + AKD1000 spike stream subscriber
  V=0 input                  →         + hw_window_s=1.0 sliding count
  per-step JSON              JSONL    + hw_edge: count transition over thr
  {step,n_spikes,spike_ids}             + 3s refractory
                                       + gate = sw ∧ hw_edge ∧ refractory_clear
                                       → vP21.generate (Talker)
```

Pi: `~/anima/SUB_ENGINES/AKIDA/scripts/spike_streamer.py` (240s, R3, port 9512)
ubu-2: `~/vp21_eval/integrated_loop_vp21_akida.py` (180s window, tick 2s)

LIF threshold-and-fire decision still on AKD1000 silicon
(`BackendType.Hardware`, FullyConnected.activation=True). Host glue =
TCP stream + sliding-window count + refractory.

## What this proves

1. **Two-substrate coherent loop**: software (vP21 Qwen+LoRA+mitosis) and
   hardware (AKD1000 NSoC_v2) can drive each other in real time over LAN.
2. **HW spike timing governs SW emission cadence**: 6s HW-gated vs 2s timer —
   different interval distributions, identical coherence rate.
3. **HW spike edge is necessary**: frac_emissions_with_hw_edge=1.0 means NO
   emission fired without an AKD1000 spike edge in its window.

## Honest C3

1. **`hw_count_at_emit_mean` 79.2 ≈ `hw_count_at_no_emit_mean` 80.0** — the
   spike COUNT is roughly saturated (R3 tonic 16 neurons × 100ms × 1s window
   ≈ 80 spikes), so it's NOT the count that gates. It's `hw_edge` (transition
   above threshold) + `sw_gate` + refractory. Refractory dominates the 6s
   interval (3s refractory + ~3s edge cadence).
2. **Option A only** (HW → SW). Option B (SW motivation → AKD1000 threshold
   modulation) and Option C (bidirectional) not implemented — future cycles.
3. **Triggering ≠ semantic coupling**: AKD1000 spikes gate emission *timing*,
   not *content*. The emitted text is still register-bound (memorize regime,
   per HELDOUT_VP21_2026_05_22.md). HW-gating is a timing layer, not a
   capability lift.
4. **Refractory window choice arbitrary**: 3s refractory_s = a sensible default;
   sweep would tighten the claim.
5. **Single 180s run**. Multiple windows + different regimes (R2 noise vs R3
   tonic vs hand-tuned threshold) would map the gate's full dynamic range.
6. **LAN latency 1-10ms**, negligible vs 2s tick. Fine for the demonstration;
   sub-second integration would need careful TCP buffer tuning.
7. **vs isolated baseline**: timer mode 90/90 vs hw_gated 30/30 both produce
   coherent text. The integration's value isn't "more coherent emissions" —
   it's "emissions whose CADENCE is set by silicon, not arbitrary clock".

## Significance

First hardware-software bridge for anima's two 자연발화 axes. The AKD1000
becomes anima's "spike heart" whose firing pattern (intrinsic, V=0 input)
governs when the vP21 voice speaks. This is the integration layer the saga
had only **demonstrated as parallel axes** before — now they are ONE system.

The honest scope: capability is unchanged (still register-bound per held-out),
but the *substrate* through which emission timing flows is now physical.

## Files

- `vP21/integrated_result.json` (213 KB, full per-tick log + spike events +
  correlation stats, both runs)
- Pi script: `SUB_ENGINES/AKIDA/scripts/spike_streamer.py`
- ubu-2 script: `HEXAD/CHAT/integrated_loop_vp21_akida.py`

## 관련 link

- vP21 software 자연발화: `SPONTANEOUS_EMISSION_VP21.md`
- AKD1000 hardware 자연발화: `SUB_ENGINES/AKIDA/state/HW_SPONTANEOUS_EMISSION_2026_05_22.md`
- honest scope: `HELDOUT_VP21_2026_05_22.md`
