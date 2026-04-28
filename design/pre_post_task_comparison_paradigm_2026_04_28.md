# T16 — Pre/Post Task Comparison Paradigm (Within-Subject Baseline Shift)

**Date**: 2026-04-28
**Track**: anima β Learning-Free / EEG paradigms
**Frozen**: raw#12 (60s pre + 60s post window, 4 metrics, N>=10/task, d>=0.5)
**Companions**: T5 (longitudinal), T15 (frontal asymmetry), N=1 within-subject design
**API**: NONE — Claude CLI only / pure-hexa stdlib (raw#9)

---

## 1. Hypothesis

Within a single subject (N=1), goal-directed tasks (coding, meditation, exercise,
meal, caffeine) produce measurable **paired pre/post baseline shifts** in EEG
markers. We measure:

- **Coding** : sustained attention → expected post γ/θ ↑, engagement ↑
- **Meditation** : focused breath → expected post γ/θ ↓ (relaxed), alpha ↑
- **Exercise** : light walk/stretch → expected post engagement ↑, drowsy ↓
- **Meal** : carb load → expected post drowsy ↑ (postprandial dip @ 30/60min)
- **Caffeine** : 50–100 mg → expected post engagement ↑, alpha ↓ @ 30min peak

H0 per metric: **μ_post = μ_pre** (no shift). H1: **μ_post ≠ μ_pre**.

## 2. Per-Session Protocol (frozen raw#12)

```
[t=-60s]  60s pre   eyes-closed                   ──┐
[t=  0s]  60s pre   eyes-open                       ├─ pre window (120s total)
[t=+60s]  TASK begins (30 min coding / etc.)        │   metric extraction window = last 60s
[t=END]   TASK ends                                 │
[t=END+0]  60s post eyes-closed                   ──┐
[t=END+60] 60s post eyes-open                       └─ post window (120s total)
```

Pre window and post window are each **60s** for the metric of record (eyes-open
sub-window for engagement / γθ / asymmetry; eyes-closed for alpha attenuation
and drowsy index). T15 frontal asymmetry uses the eyes-closed sub-window.

## 3. Five Task Types (frozen)

| Task ID         | Pre-cond                | Task action                    | Post-cond            |
|-----------------|-------------------------|--------------------------------|----------------------|
| `coding`        | rested, no caffeine 2h  | 30 min focused coding          | immediate            |
| `meditation`    | quiet room              | 30 min breath-focus meditation | immediate            |
| `exercise`      | seated baseline         | 30 min walking / stretching    | 5 min cool-down then |
| `meal_30`       | 4h fasted               | normal meal (~600 kcal)        | 30 min post-meal     |
| `meal_60`       | (same session as above) | (no second meal)               | 60 min post-meal     |
| `caffeine_30`   | no caffeine 8h          | 80 mg coffee / espresso        | 30 min post-ingest   |
| `caffeine_60`   | (same session as above) | (no second dose)               | 60 min post-ingest   |

Note: `meal_30/60` and `caffeine_30/60` share a single pre but yield two paired
post rows (per-subject paired design preserved per timepoint).

## 4. Metrics (paired pre/post, x1000 integer)

1. **LZ76 b(n)** — Lempel-Ziv complexity (own 3 σ/τ=3 verify-pass channel mean)
2. **γ/θ ratio** — gamma (30–80 Hz) / theta (4–8 Hz) bandpower ratio
3. **Engagement** — β/(α+θ) per Pope-style index
4. **Frontal asymmetry** — log(α_F4) − log(α_F3) (T15 paired)

Optional: drowsy index, DMN coherence shift (deferred — needs ≥ 8-channel cap).

## 5. Statistical Design

- **Test**: paired two-tailed t-test on (post − pre) per task per metric
- **Effect size**: Cohen's d_z = mean(post − pre) / sd(post − pre)
- **Frozen N**: N >= 10 paired sessions per task type
  - Power 0.8, α 0.05, two-tailed → minimum d ≈ 0.92 detectable at N=10
  - Frozen criterion **d >= 0.5** is "minimum meaningful"; if d in [0.5, 0.92] at
    N=10 → declare *underpowered_suggestive*, queue more sessions
- **Multiple comparisons**: 4 metrics × 5 task types = 20 tests → Bonferroni
  α_corr = 0.0025, or FDR(BH) at q=0.10

## 6. raw#71 Falsifiers (5+)

- **F1**: pre window > 60s OR pre/task overlap (no clean inter-task gap) → ABORT
- **F2**: post window starts < 0s after task-end (no recovery time / motion
  contamination from chair-shift) → ABORT
- **F3**: head-movement artifact > 30% segments (per board_health_check) → ABORT
- **F4**: ICA decomposition fails (rank-deficient, non-convergent, or > 50 %
  components flagged as artifact) → ABORT
- **F5**: paired t-test p > 0.5 across N >= 10 sessions per task → declare
  **NULL** (task does not shift baseline) — honest C3 retraction (raw#91)
- **F6**: |d| < 0.2 at N >= 20 → small-or-no effect, deprioritize task
- **F7**: pre vs pre intra-day variance > post − pre delta → noise-dominant,
  lengthen pre window or stabilize protocol

## 7. Implementation

- `anima-eeg/tool/pre_post_task_recorder.hexa` (~150 LoC)
  - inputs: `--task <coding|meditation|exercise|meal_30|meal_60|caffeine_30|caffeine_60>`
  - outputs: one JSONL row per paired (pre,post) measurement with all 4 metrics
    pre and post side-by-side, plus delta and within-row Cohen-style |delta|/sd
    placeholder (sd accumulated cross-session by aggregator)
  - audit: `state/pre_post_audit/<YYYY-MM-DD>_<task>.jsonl`

## 8. Frozen criteria summary (raw#12)

```
window_pre_s         = 60
window_post_s        = 60
metrics              = [lz76_x1000, gamma_theta_x1000, engagement_x1000, frontal_asym_x1000]
task_types_frozen    = [coding, meditation, exercise, meal_30, meal_60, caffeine_30, caffeine_60]
N_min_per_task       = 10
effect_size_d_min    = 0.5
multiple_comparisons = bonferroni @ 0.0025  (or BH-FDR q=0.10)
falsifiers           = F1..F7  (raw#71)
```

## 9. raw compliance

raw#9 / 10 / 12 / 37 / 65 / 71 / 82 / 91 / own5 — covered.
T5 (longitudinal axes) is the cross-day baseline; T16 is the within-task pair.
T15 (asymmetry) shares the eyes-closed sub-window — paired analyzable.

## 10. First user session (operator action)

```
$HEXA_LANG/hexa.real run anima-eeg/tool/pre_post_task_recorder.hexa --selftest
$HEXA_LANG/hexa.real run anima-eeg/tool/pre_post_task_recorder.hexa \
    --task coding --timestamp $(date -u +%Y-%m-%dT%H:%M:%SZ) --append
```
