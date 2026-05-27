# Option B — SW motivation → AKD1000 threshold modulation LANDED

> 2026-05-22. Second leg of the vP21 ⊥ AKD1000 bridge.
> Option A (HW spike → SW emit) landed in `INTEGRATED_LOOP_VP21_AKIDA_2026_05_22.md`
> (frac=1.0, 30/30). Option B drives the inverse direction: SW vP21 8-factor
> motivation_score rewrites the on-chip LIF threshold in real time, with a
> random-surrogate control to falsify "motivation → spike rate is the cause".

## Verdict: BIDIRECTIONAL_WORKS

Per the pre-registered criterion (`ρ_real > 0.3` AND `ρ_real − ρ_control > 0.2`):

| run | n_ticks | Spearman(drive, hw_rate) | Pearson(drive, hw_rate) | drive range | thr_offset range | hw_rate range |
|---|---|---|---|---|---|---|
| **option_b** (real motivation) | 45 | **+0.6947** | +0.9258 | [≈0.55, 0.76] | [-2, -1] | [0.825, 0.9375] |
| **option_b_random** (control)  | 45 | **−0.0313** | −0.0415 | [≈0, 1] | [-6, +6] | [0.500, 1.000] |

- ρ_real **0.6947** ≫ 0.3 threshold ✓
- ρ_real − ρ_control = **0.726** ≫ 0.2 threshold ✓
- Pearson on real run **+0.926** (linear coupling near-perfect inside the
  observed drive range)
- Pearson(thr_offset, hw_rate) = **−0.912** — confirms the physical mechanism:
  lowering the threshold raises the spike fraction monotonically.

Causal coupling is real: when motivation drives the on-chip threshold,
hw_rate tracks motivation. When the SAME mapping is fed a uniform-random
surrogate, the rank correlation collapses to noise (~0).

## Architecture (Option B)

```
ubu-2 (vP21)                                Pi 5 + AKD1000
============                                ==============
integrated_loop_vp21_akida_bc.py            spike_streamer.py
  AnimaState.tick() per 2.0s                  --regime M --allow-ctrl
    → 8-factor motivation_score s ∈ [0,1]    LIF.set_variable("threshold", arr)
  score_to_thr_vector(s):                    per-step on chip
    offset = round(12 × (0.5 - s))           V=N=16 weak-ones input
    thr[j] = baseline[j] + offset            on-chip threshold-and-fire decision
  ThresholdPublisher → TCP 9513   ─────→     ThresholdControlListener (port 9513)
                          JSON                set_threshold cmd applied at next step
  SpikeSubscriber  ←──── TCP 9512 ────       OUT broadcast spikes (port 9512)
                          JSONL              per-step records {n_spikes, thr, ...}
  window_rate() over 1.0s sliding
  → log (drive, hw_rate, thr_offset) per tick
  → Spearman/Pearson at end-of-run
```

Mapping `score ∈ [0,1] → offset ∈ [-6, +6]`: midpoint 0.5 = neutral
(offset=0); s=1 → -6 (low thr → MORE spikes); s=0 → +6 (high thr → FEWER
spikes). Amplitude 12 chosen so the offset sweep fully spans the
baseline `np.linspace(2, 18, 16)` regime.

## Window details

90s × 2 runs, 2.0s tick → 45 ticks each. Window after model warmup.

Pi: `spike_streamer.py --regime M --allow-ctrl --duration 360`, step 100ms.

Pi-side total `set_variable("threshold", ...)` overhead across **91 updates**
= **2.7 ms** = **~30 µs per update**. Negligible vs the 100ms step interval.
The chip is not the bottleneck.

The publisher sent 46 (option_b) + 91 cumulative (option_b_random) threshold
commands, 0 failures, persistent TCP connection.

## What this proves

1. **Threshold-rewrite mechanism works in real time**: a Python-emitted
   integer vector reaches the AKD1000 FullyConnected LIF and modifies its
   spike decision within ~100ms (one step). The chip stays on
   `BackendType.Hardware`; the only mutation is the int32 threshold
   variable.
2. **Motivation is the cause, not coincidence**: when the SAME mapping
   pipeline is fed a random surrogate, Spearman drops from 0.69 to
   −0.03. The SW 8-factor score is doing the work; the linkage is
   neither a TCP timing artifact nor a baseline drift.
3. **Together with Option A, both substrates can drive each other**:
   Option A (HW → SW, frac=1.0) shows the chip's spikes gate emission
   timing; Option B (SW → HW, ρ=0.69 vs control −0.03) shows the SW
   motivation modulates the chip's firing rate. Option C (run them
   simultaneously) is the next cycle — not in scope this run.

## Honest C3

1. **Real-motivation drive saturates** in `[0.55, 0.76]` → offset range
   only `[-2, -1]` (vs random's full `[-6, +6]`). Spearman is computed
   over the saturated drive range; if motivation were less saturated
   the linear regression slope would extend. The 0.69 correlation
   is genuine *inside* the observed range — extrapolating to the
   full motivation domain needs a different driver task.
2. **hw_rate ceiling at 1.0** (all 16 units fire). Once offset < -1,
   the chip is saturated and further reductions don't show. Future
   runs should raise the M baseline (e.g. linspace(8, 24)) to avoid
   the saturation cap.
3. **Single 90s window per run** (not multiple seeds, not multiple
   sessions). The Spearman estimate has ~45 paired samples — enough
   for a clear signal but not for tight CI.
4. **Mechanism is threshold-rewrite, not learning**. The chip
   doesn't adapt; the SW host is the only "learner". Closing the
   loop with on-chip STDP/edge-learn is a separate cycle.
5. **Mapping function `THR_AMPL=12, neutral=0.5` is hand-chosen**.
   No sweep over amplitude or neutral point. The motivation→threshold
   gain is a free parameter, not optimised.
6. **Pi-side `set_variable` overhead 30 µs** measured under one-update-per-tick
   load (2s cadence). Higher-frequency control (10 Hz or more) was
   not stressed; the chip might queue or coalesce updates at higher
   rates — this run doesn't constrain that path.
7. **Causal direction inside Option B alone**: motivation → threshold
   → hw_rate. The reverse (hw_rate → motivation) is what Option A
   tested; this run does NOT close the loop end-to-end. Option C
   does both directions simultaneously — separate cycle.

## Files

- ubu-2 client: `HEXAD/CHAT/integrated_loop_vp21_akida_bc.py`
  (extends Option A's `integrated_loop_vp21_akida.py` with publisher +
  `option_b` / `option_b_random` / `option_c` / `option_c_random` /
  `b_only` modes)
- Pi server: `SUB_ENGINES/AKIDA/scripts/spike_streamer.py`
  (already had `--regime M --allow-ctrl` from prior cycle; this run is the
  first end-to-end exercise of the control listener)
- Result: `vP21/integrated_opt_b_result_2026_05_22.json` (81 KB —
  per-tick (tick, t_rel, drive, score, thr_offset, hw_window_rate,
  hw_window_count, hw_total_spikes, pub_ok, factors{8}, …) for both runs +
  verdict)
- Client log: `vP21/opt_b_run.log`

## Related

- Option A: `INTEGRATED_LOOP_VP21_AKIDA_2026_05_22.md`
- vP21 SW spontaneous: `SPONTANEOUS_EMISSION_VP21.md`
- AKD1000 HW spontaneous: `SUB_ENGINES/AKIDA/state/HW_SPONTANEOUS_EMISSION_2026_05_22.md`
- Honest scope: `HELDOUT_VP21_2026_05_22.md`

## Cost

$0 — Pi 5 + AKD1000 + ubu-2 RTX 5070, all LAN.
