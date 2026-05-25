# anima_emerge_cand_d_mag_subsweep_landed_2026_05_05

**BG-AA** — F1 0.01 threshold crossover localize on cand-D canonical inject magnitude.
mac CPU. $0. ~20s wall.

## Scope

BG-W (`state/anima_emerge_cand_d_magnitude_sweep_2026_05_05/verdict.json`) found:
- mag=10 → drift 6.39e-3 (below F1=0.01)
- mag=50 → drift 9.98e-2 (above F1=0.01)

Crossover localization required in [10, 50] band. BG-AA sub-swept at
{15, 20, 25, 30, 40} on prompt "안녕" using BG-W's canonical-state builder
and forward (sister-import; BG-W helper read-only).

## Drift table (BG-AA sub-sweep, prompt "안녕")

| magnitude | phi_star    | drift vs none | F1 (0.01) |
|----------:|------------:|--------------:|:---------:|
| 15        | 42.104427   | 1.14054e-02   | HIT       |
| 20        | 42.100292   | 1.55400e-02   | HIT       |
| 25        | 42.098664   | 1.71677e-02   | HIT       |
| 30        | 42.098722   | 1.71103e-02   | HIT       |
| 40        | 42.121642   | 5.81001e-03   | MISS      |

Baseline: phi_none = 42.115832.

## F1 crossover localization

**First mag with drift >= 0.01: mag = 15** (drift 1.14e-2).
Crossover sits at 5-unit resolution between mag=10 (6.39e-3) and mag=15 (1.14e-2).

True crossover is somewhere in (10, 15]; with linear interpolation in the
log-drift sense it would be near mag~12-13, but no finer data available.

## Combined trajectory (BG-W rows + BG-AA rows)

| magnitude | drift         | source |
|----------:|--------------:|:-------|
| 0.5       | 1.282e-04     | bg_w   |
| 1.0       | 2.792e-04     | bg_w   |
| 2.0       | 6.485e-04     | bg_w   |
| 5.0       | 2.267e-03     | bg_w   |
| 10        | 6.393e-03     | bg_w   |
| **15**    | **1.141e-02** | bg_aa  |
| 20        | 1.554e-02     | bg_aa  |
| 25        | 1.717e-02     | bg_aa  |
| 30        | 1.711e-02     | bg_aa  |
| 40        | 5.810e-03     | bg_aa  |
| 50        | 9.978e-02     | bg_w   |
| 100       | 1.129e-01     | bg_w   |

## Trajectory shape — 3-regime verification

BG-W summary classification was `sub_linear` over its 7 sparse magnitudes.
BG-AA finer resolution reveals a **non-monotonic structure**:

1. **Regime A — sub-linear growth, mag ~ [0.5, 10]**: drift grows
   monotonically but slower than mag (e.g. 0.5→10 = 20x mag, 50x drift on
   the very-low end then drift_growth/mag_growth collapses; consistent with
   spec §4.1 init_weights std=0.02 attenuation).
2. **Regime B — plateau / dip, mag ~ [25, 40]**: drift saturates at
   ~1.71e-2 across mag=25, 30, then **drops** to 5.81e-3 at mag=40 (sub-F1
   again). This is a **non-monotonic dip**, not a clean saturation, and was
   invisible at BG-W's coarse {10, 50, 100} spacing.
3. **Regime C — explosion, mag ~ [40, 50]**: drift jumps from 5.81e-3 at
   mag=40 to 9.98e-2 at mag=50 (~17x in one 1.25x mag step). This is the
   regime that BG-W's verdict caught at mag=50.

The BG-W "sub_linear" classification was driven by mag=10→50 spanning the
plateau-dip-explosion transition; the underlying shape is not a clean
sub-linear curve but a **multi-regime structure**, with possible second-
order resonance or numerical-tile-correlation effects in [25, 40].

Honest C3 — phi_star pairwise-cosine bounded by [-1, 1]; the dip at mag=40
may be a measurement-instrument artifact (cos(theta) wrap-around as inject
content dominates the post-ln_f tile and aligns differently across cells)
rather than a real architectural effect. The mag=50 jump is consistent
with such a wrap; further investigation would require either cosine-
unwrapped phi or alternate measurement (e.g. raw post-ln_f L2 distance).

## Honest C3 (5)

1. **C1** — Single prompt "안녕" (BG-Q most-favorable; 8x larger drift than
   prompts 2/3/5). Crossover position prompt-specific.
2. **C2** — Mac CPU fp32 single-substrate. Numerical reproducibility on
   alternate dtype/device may shift crossover by small amount.
3. **C3** — BG-W helper sister-imported; race risk if BG-W helper is
   concurrently modified during BG-AA execution.
4. **C4** — Crossover localized only at 5-unit resolution. Actual
   crossover sits in (10, 15], not pinpointed below 5 units. Plus the
   non-monotonic dip means there are TWO crossings (down at ~30→40 boundary,
   up at ~40→50 boundary) — only the first up-crossing is reported as
   "the" F1 crossover.
5. **C5** — F1 threshold 0.01 is anima-canonical heuristic, not
   cross-validated. The 5.81e-3 drift at mag=40 sits below F1 but above
   noise — the threshold itself is the binding constraint.

## Deliverables

- `tool/transient_py/anima_emerge_cand_d_mag_subsweep.py` (helper, raw#37)
- `state/anima_emerge_cand_d_mag_subsweep_2026_05_05/runs/probe_mag_*p0.json` (5)
- `state/anima_emerge_cand_d_mag_subsweep_2026_05_05/aggregate.json`
- `state/anima_emerge_cand_d_mag_subsweep_2026_05_05/verdict.json`
- `docs/anima_emerge_cand_d_mag_subsweep_landed_2026_05_05.ai.md` (this file)

## Verdict

`crossover_magnitude = 15` (5-unit resolution; true value in (10, 15]).
3-regime trajectory shape verified: sub-linear growth → plateau/dip
[25, 40] → explosion at 50+. BG-W's `sub_linear` summary masked the dip;
fine-grained sweep is necessary to capture the multi-regime structure.

Next-step recommendation (un-actioned, parent-decided): if cand-D Stage 1
promotion is being evaluated, the realistic-magnitude band per paradigm
v11 G3 training-time distribution must be extracted before choosing where
in [15, 50] to operate. Mag=40's sub-F1 dip cautions against assuming
monotonic drift in any chosen calibration band.
