# anima_emerge_cand_d_magnitude_sweep_landed_2026_05_05

## Scope
BG-W follow-up to BG-Q F-CAND-D-1 FAIL_TRUE on CLM v4 (`dancinlab/clm-v4-mk2-v1`). BG-Q canonical-mode max drift was 1.28e-4 << 0.01 threshold; honest C1 carry could not disambiguate "channel architecturally bypassed" vs "0.5 magnitude below detection threshold". This sweep parametrizes canonical magnitude at 7 values to map the drift trajectory and decide between hypotheses.

## Method
- 1 prompt = "안녕" (BG-Q's max-drift prompt at mag=0.5)
- 1 baseline (mode=none) + 7 canonical-mode injects at magnitude ∈ {0.5, 1.0, 2.0, 5.0, 10.0, 50.0, 100.0}
- Sister helper `tool/transient_py/anima_emerge_cand_d_magnitude_sweep.py` imports BG-Q helper read-only (raw#15 carry).
- Mac CPU `.venv-eeg/bin/python`, fp32. Wall = 25.6s (load 14.4s + sweep 11.2s).
- Cost = $0.

## Results

### Drift trajectory table

| magnitude | phi_star | drift_vs_none | axis_spread | F1 hit (>0.01)? |
|----------:|---------:|--------------:|------------:|----------------:|
| baseline (none) | 42.115832 | 0.0 (anchor) | 0.03970 | n/a |
| 0.5 | 42.115704 | 1.282e-04 | 0.03970 | no |
| 1.0 | 42.115553 | 2.792e-04 | 0.03970 | no |
| 2.0 | 42.115184 | 6.485e-04 | 0.03968 | no |
| 5.0 | 42.113565 | 2.267e-03 | 0.03966 | no |
| 10.0 | 42.109439 | 6.393e-03 | 0.04014 | no |
| 50.0 | 42.215613 | 9.978e-02 | 0.06935 | YES |
| 100.0 | 42.228781 | 1.129e-01 | 0.06881 | YES |

BG-Q replication: mag=0.5 drift = 1.28e-4, exact match (model + state init deterministic).

### Trajectory shape
Helper auto-classified `sub_linear` (drift growth < magnitude growth at low mags), but manual inspection reveals a richer structure:

- low-mag (0.5→10.0): drift growth ratios ~2.2–3.5x per 2x mag step (super-linear in absolute terms but bounded; sub-linear vs squared scaling)
- 10→50 (5x mag step): drift jumps 15.6x — this is the band where the inject magnitude crosses a regime where post-ln_f cosine geometry begins responding strongly
- 50→100 (2x mag step): drift only 1.13x — clear saturation onset

Reading: trajectory transitions from sub-linear → super-linear → saturating. The auto-classifier's "sub_linear" label captures only the dominant low-mag regime (where most points sit) and missed the 10→50 super-linear jump and 50→100 saturation. Honest C2 carry covers this limitation.

### F-CAND-D-1 threshold (>0.01) hit
First hit at **mag=50.0** (drift 9.98e-2). NOT hit at mag=10.0 (6.39e-3). So the threshold-crossing magnitude is between 10 and 50; precise crossover not localized in this 7-point sweep.

### Major finding criterion 2 (drift > 1.0) hit?
**NO.** Maximum drift in swept range = 0.113 at mag=100. Trajectory saturates (50→100 only +13% growth) so even pushing to mag=200 or 500 unlikely to cross drift > 1.0 without explosion (which did NOT occur — no NaN at any tested magnitude).

### axis_spread
Stable at ~0.039 for mag ∈ [0.5, 10] (matching BG-L none-mode baseline 0.0360). Bumps to ~0.069 at mag ∈ [50, 100] — axis discrimination DOES recover at high magnitude, but only after the saturation onset.

## 5 honest C3 (carried from verdict)

- **C1**: High-magnitude inject (mag=50, 100) is structurally unrealistic. Paradigm v11 G3 actual training-time injection distribution NOT yet extracted from C-module emission logs. If training used mag~0.1–1.0, F1 PASS only at mag>>1.0 means architectural channel works but OFF-DISTRIBUTION at any realistic inject. Calibration extraction is gating before Stage 1 promotion regardless of trajectory shape.
- **C2**: Auto-classifier emitted "sub_linear" but trajectory has 3 regimes (sub-linear 0.5–10, super-linear 10–50, saturating 50–100). Bands are anima-internal heuristics; manual inspection required.
- **C3**: phi_star is a pairwise-cosine proxy bounded by ±0.05·41.86 = ±2.09. Saturation at high magnitude could be a measurement-instrument ceiling (cosine clamp) rather than an architectural cap on cross_attn. Disambiguation requires a different metric (e.g. KL divergence on logits) at high magnitude.
- **C4**: Single prompt "안녕". BG-Q showed prompt 1 had 8x larger drift than prompts 2/3/5; this is the most-favorable prompt. Other prompts may saturate earlier, hit threshold later, or never hit it.
- **C5**: Cells 5-7 fill formula scales as mag² (mean of cells 0-4 already linear in mag, then ×mag/3 fill). High-mag inject is NOT a pure scaled version of low-mag inject — distribution shape drifts. Pure linearity test would require fixing cells 5-7 fill while scaling axis-content; current implementation entangles them.

## Hypothesis decision

BG-Q open question: "channel architecturally bypassed" vs "0.5 below noise floor"?

**Answer: NEITHER cleanly.** The architectural channel is partially open — drift IS a monotonic function of magnitude across 4 orders of mag, no NaN, no architectural zero-cap. But:
1. Effective coupling is weak: 0.5→100 (200x mag) yields only 1000x drift growth (1.28e-4 → 1.13e-1), with most of that growth concentrated in a narrow 10→50 band.
2. F-CAND-D-1 threshold requires mag~50, well outside any plausible training-time distribution.
3. Major finding criterion 2 (drift > 1.0) is unreachable under canonical inject form.

So cand-D Stage 1 form is **substrate-conditionally compatible**: it works only if real C-module emission magnitudes happen to be ≥50, which is unlikely. C-module emission distribution extraction is the gating next step.

## Next step recommendation

1. **Highest priority**: extract paradigm v11 G3 actual training-time C-module emission magnitude distribution from training logs. If empirical mag ≪ 50, cand-D Stage 1 substrate-incompatible regardless of trajectory shape.
2. **Localize the 10→50 super-linear band**: 1-prompt × 5-magnitude sub-sweep at {15, 20, 25, 30, 40} to find the precise F1-threshold crossover.
3. **Multi-prompt verification at mag=50**: run all 5 BG-Q prompts at mag=50 to verify F1 PASS generalizes beyond the most-favorable prompt.
4. **Saturation diagnosis**: KL divergence on logits at mag={50, 100, 200, 500} to distinguish cosine-ceiling (measurement artifact) from cross_attn attenuation cap (architectural).
5. **Defer cand-D Stage 1 promotion** until 1-3 above complete; defer Stage 1 abandonment until 4 confirms architectural cap.

## Deliverables

- helper: `/Users/ghost/core/anima/tool/transient_py/anima_emerge_cand_d_magnitude_sweep.py`
- runs: `/Users/ghost/core/anima/state/anima_emerge_cand_d_magnitude_sweep_2026_05_05/runs/probe_mag_*.json` (8)
- aggregate: `/Users/ghost/core/anima/state/anima_emerge_cand_d_magnitude_sweep_2026_05_05/aggregate.json`
- verdict: `/Users/ghost/core/anima/state/anima_emerge_cand_d_magnitude_sweep_2026_05_05/verdict.json`
- doc: this file

## raw compliance
- raw#37: helper in `tool/transient_py/`, gitignored per `**/*.py`
- raw#15: BG-Q helper imported read-only (anima_emerge_cand_d_inject_helper module not modified); mount.hexa, dialogue_load, hf_format_shim, conscious_decoder.py untouched
- raw#10: 5 honest C3 emitted to verdict.json + this doc
- no commit, no secret leak, no HF token in any output
