# Self-experiment longitudinal protocol — N=1 within-subject

**Date frozen**: 2026-04-28
**Linked SSOT files**:
- runner: `anima-eeg/tool/longitudinal_session_recorder.hexa`
- ledger: `state/longitudinal_audit/sessions.jsonl` (append-only)
- pre-reg: `state/longitudinal_pre_register.json`
- raw: 9, 10, 12, 37, 65, 82, 91, own5

---


Multi-subject N≥10 cross-sectional baseline collection requires recruitment, IRB,
for **fast within-subject baseline distribution formation**: each variable axis
filled to N≥10 sessions over ~14 days of self-discipline.

**Goal**: replace the operational placeholder `human_baseline_lz76_x1000 = 850`
**empirical (mean − 2·SD)** computed from N≥10 own-subject resting sessions per
condition. Threshold is *not* tuned post-hoc; it is *replaced* once a frozen
N is reached, and the new value is itself frozen at that point.

## 2. Variables (5 axes, frozen pre-registration)

| Axis | Levels | N target / level | Total |
|---|---|---|---|
| 1. Caffeine    | pre-09:00 / post-09:30 / +30min / +60min            | 10 | 40 |
| 2. Circadian   | 09:00 / 12:00 / 15:00 / 18:00 / 21:00               | 10 | 50 |
| 3. Post-meal   | imm / +1h / +2h                                     | 10 | 30 |
| 4. Post-exercise| imm / +30min                                       | 10 | 20 |
| 5. Sleep       | wake-imm / +30min / +60min                          | 10 | 30 |
| **Total**      |                                                     |    |**170 sessions** |

Per session = 60s eyes-closed + 5min eyes-open daily-life = ~7min wear time
+ ~3min setup/teardown ≈ **10min × 170 = 1700min = ~28.3h electrode-on time**.

## 3. Per-session protocol (frozen)

1. Mount Cyton+Daisy 16ch helmet (board_health_check passes)
2. Impedance check (`impedance_check.hexa --selftest` then real Z scan)
5. Compute per-session:
   - LZ76 (Kaspar-Schuster 1987) on resting segment
   - γ/θ ratio = bandpower(30-80) / bandpower(4-8)
   - engagement = β/α ratio
   - drowsy_idx = (θ+α)/(β+γ)
6. Append one JSONL row to `state/longitudinal_audit/sessions.jsonl`


- **H1**: caffeine elevates β/α engagement at +30/+60min vs pre baseline (paired t).
- **H2**: circadian effect on LZ76 — afternoon (15:00) ≥ morning (09:00) (Marzano 2010).
- **H3**: post-meal +0min lowers engagement vs +2h (postprandial dip).
- **H4**: post-exercise +0min elevates γ/θ vs +30min recovery.
- **H5**: wake-immediate elevates drowsy_idx vs +60min (sleep inertia).

## 5. Statistical protocol

- N≥10 sessions per condition → mean ± SD per metric per level
- Within-subject **paired t-test** (level vs level)
- Within-subject **repeated-measures ANOVA** for circadian 5-level
- All α = 0.05, **Bonferroni-corrected** for 5 axes × 4 metrics = 20 tests → α' = 0.0025
- Effect-size (Cohen's d) reported alongside p; underpowered tests flagged.


1. After 170 sessions accumulated, freeze ledger (`chflags uchg`).
2. Compute mean(LZ76) and SD(LZ76) on **resting eyes-closed × all conditions**.
3. New threshold = `round((mean - 2·SD) × 1000)`.
4. Bump `clm_eeg_p1_lz_pre_register.json` → v2, **diff-only commit**, no silent edit.


- **N=1**: results bind only to this single subject; no claim of generalisation.
- **Carryover**: caffeine half-life 5-6h → between-day washout required (no
  caffeine after 14:00 on session-days).
- **Adherence**: dependent on user willpower; missed sessions → reduced power,
  **no imputation**, ledger gaps reported as-is.
- **Order effects**: randomisation log per day; circadian axis is intrinsically
  ordered, others rotated.
- **Hardware drift**: per-session board_health_check + impedance Z logged.


F1-F5 in pre-registration card.

## 9. RAW compliance map

- own 5 (5-falsifier completeness): F1..F5 enumerated
