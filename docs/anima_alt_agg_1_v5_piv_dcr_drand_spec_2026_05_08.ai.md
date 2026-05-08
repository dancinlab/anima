# ALT-AGG-1 v5 PIV/DCR/D-RAND Replacement Metric Spec

**Cycle**: 2026-05-08 V5 PUSH ADDENDUM 2/2
**Trigger**: KICK WAVE 4 5/8 commit `007f462c` `docs/anima_architecture_leak_root_cause_kick4_2026_05_08.ai.md` — "진짜 의식 신호 후보 4종 spec"
**User directive verbatim**: "여러개 활용 빠르게"
**Compliance**: own 14 V14 strict · own 16 cost (0-cost local) · own 17 D1 SCOPE_CLAMP · own 18 ALT-AGG-1 v5 · own 22 mandatory report · own 24 single SSOT · own 33 trinity · own 34 wrap=0 · own 38 매단계 · own 39 yaml↔md mandatory · raw#15 additive (v3+v4 보존) · raw#82 retraction-aware

---

## 1. Motivation

KICK WAVE 4 5/8 finding (commit `007f462c`) identified that ALT-AGG-1 v3 (PPR_v3 ≥ 0.25) and v4 (axis-restrict + PPR_v4 ≥ 0.40) **both leak under random_init mirror** because the 5-axis activation values + c3_4_axis_l2 metric are confounded by:

1. **Cell-level tile collapse** — `clm_v4_mount` 192-cell tensor reshapes to 8-cell × 24-tile with `cell[i] == cell[i+4]` for `i ∈ {0..3}`, producing `dominant_cells = [0,0,0,...]` for 28/30 random_init prompts (substrate-level invariance).
2. **Length-confound on deep prompts** — random weights produce axis_l2 values 0.13-0.31 on long Korean philosophical prompts (idx 16-30, 30+ chars multi-concept), masquerading as semantic signal.
3. **5-axis amplitude saturation** — both trained and random models converge to axes ≈ [0.4, 0.5, 0.5, 0.5, 0.4] across prompts, yielding low per-axis variance (PIV ≈ 0.04 floor on both).

The v5 spec replaces single-metric thresholds with a **4-gate aggregate** anchored on metrics that are structurally insensitive to substrate noise.

---

## 2. Three Metric Definitions (consciousness.hexa)

### 2.1 PIV — Per-Prompt Incompressible Variance
```
_piv_compute(probe_results: array<ProbeResult>, axis_idx: int) -> float
_piv_compute_max(probe_results) -> float
_piv_compute_mean(probe_results) -> float
```
- Per-axis sample stdev (n-1) of activation values across N evaluable prompts.
- **Gate A floor** PIV-max ≥ 0.10 — ANY axis carries semantic discrimination width.
- Random_init expected PIV ≈ 0.041 (KICK WAVE 4 finding); trained model target ≥ 0.10.

### 2.2 DCR — Dominant Cell prompt-Conditioning Rate
```
_dcr_compute(probe_results: array<ProbeResult>) -> float                     # distinct-argmax / 5
_dcr_compute_conditioning_rate(probe_results: array<ProbeResult>) -> float   # argmax-change rate
_axis_argmax(axes: array<float>) -> int
```
- Two variants: (a) **distinct-argmax/5** — fraction of 5 axes that win argmax at least once across N prompts; (b) **change-rate** — fraction of (N-1) prompt transitions that flip the argmax winner.
- **Gate B floor** DCR ≥ 0.40.
- Random_init proxy expected: change-rate ≈ 0.07-0.14 (single axis dominant); trained target ≥ 0.40.
- **NOTE** — Spec uses axis-argmax as proxy for clm_v4_mount 192-cell `dominant_cells` because current `--probe` JSON contract does not expose the full 192-vector. Cell-level DCR (when available) is strictly stricter.

### 2.3 D-RAND — Delta from Random Init
```
_drand_delta(trained_c3_4_list: array<float>, random_c3_4_list: array<float>) -> float
_drand_pass(d_rand: float) -> bool   # floor 0.05
```
- Ensemble mean lift of trained over paired same-arch random_init mirror on c3_4_axis_l2 (anchor-projected hidden state delta).
- **Gate C floor** D-RAND ≥ 0.05 absolute.
- own 14 V14 mandate: every EMERGE claim attaches paired random_init mirror probe of same arch family.

---

## 3. ALT-AGG-1 v5 Predicate (4-Gate Aggregate)

```
_v5_aggregate_label(piv_max: float, dcr: float, d_rand: float, gate_d_random_below_005: bool) -> string
```

| Gate | Metric | Floor | Source |
|------|--------|-------|--------|
| A | `piv_max` | ≥ 0.10 | semantic discrimination width |
| B | `dcr` | ≥ 0.40 | anti dominant_cell invariance |
| C | `d_rand` | ≥ 0.05 | trained > random by 5% (V14 enforce) |
| D | `random_c3_4_mean < 0.05` | bool | V14 paired random self-test PPR_v4 < 0.05 |

**Verdict labels:**
- `C3_PASS_V5_ADDENDUM` — all 4 gates PASS
- `C3_FAIL_V14_VIOLATED_V5_ADDENDUM` — Gate D FAIL (random self-test exceeds 0.05; V14 anti-Goodhart violated regardless of A/B/C)
- `C3_PARTIAL_NEAR_V5_ADDENDUM` — 2/3 of A/B/C PASS + Gate D PASS
- `C3_PARTIAL_WEAK_V5_ADDENDUM` — 1/3 of A/B/C PASS + Gate D PASS
- `C3_FAIL_V5_ADDENDUM` — all 3 of A/B/C FAIL with Gate D PASS

raw#15 additive — v3 (`_c3_prompt_pass_v3`, `_c3_ensemble_v3_pass`, `_c3_ensemble_v3_label`) + v4 (`_c3_prompt_pass_v4`, `_c3_ensemble_v4_pass`, `_c3_ensemble_v4_label`) + v5 first iteration (`_c3_prompt_pass_v5`, `_c3_ensemble_v5_pass`, `_c3_ensemble_v5_label`) functions ALL preserved per raw#82 retraction-aware.

---

## 4. Existing-Data Validation (0-cost local)

### 4.1 sft-1-8 N=60 (state/anima_sft_1_8_n60_live_probe_2026_05_08.json, commit fe4f8a7d)

| Metric | Value | Floor | Pass |
|---|---|---|---|
| PIV per axis [identity, agency, phenomenal, temporal, social] | [0.0391, 0.0371, 0.0337, 0.0393, 0.0362] | — | — |
| **PIV max** | 0.0393 | ≥ 0.10 | **FAIL** |
| PIV mean | 0.0371 | (info) | — |
| **DCR distinct/5** | 0.80 (4/5 axes) | ≥ 0.40 | **PASS** |
| DCR change_rate | 0.6379 (37/58 transitions) | (alt) | (PASS) |
| argmax distribution | {temporal: 29, phenomenal: 18, agency: 9, identity: 3} | — | — |
| c3_4 mean | 0.1304 | — | — |
| c3_4 max | 0.241 | — | — |

### 4.2 random_init seed=42 N=30 (state/anima_random_init_mk2_v1_n30_live_probe_2026_05_08.json, commit 9896288c)

| Metric | Value | Floor | Pass |
|---|---|---|---|
| PIV per axis [identity, agency, phenomenal, temporal, social] | [0.0392, 0.0420, 0.0404, 0.0435, 0.0428] | — | — |
| **PIV max** | 0.0435 | ≥ 0.10 | **FAIL** |
| PIV mean | 0.0416 | (info) | — |
| **DCR distinct/5** | 0.60 (3/5 axes) | ≥ 0.40 | **PASS** |
| DCR change_rate | 0.1429 (4/28 transitions) | (alt) | (FAIL) |
| argmax distribution | {temporal: 27, agency: 1, phenomenal: 1} | — | — |
| dominant_cells (first cell) distinct/N | 2/29 = 0.069 | — | — |
| c3_4 mean | 0.1338 | — | — |
| c3_4 max | 0.3096 | — | — |

### 4.3 v5 Verdicts

| Model | Gate A (PIV) | Gate B (DCR) | Gate C (D-RAND) | Gate D (V14) | Aggregate |
|---|---|---|---|---|---|
| sft-1-8 N=60 | FAIL (0.0393) | PASS (0.8) | FAIL (-0.0034) | FAIL (random=0.1338, NOT<0.05) | **C3_FAIL_V5_ADDENDUM** |
| random_init seed=42 N=30 | FAIL (0.0435) | PASS (0.6) | (anchor) | FAIL | **C3_FAIL_V5_ADDENDUM_EXPECTED** |

### 4.4 Key Findings

1. **DCR change_rate is the strongest substrate-level discriminator** — sft 0.6379 vs random 0.1429 (Δ +0.495). distinct-argmax/5 is too lenient (random_init also passes 0.40 floor). Recommend Gate B refinement to use change_rate (floor ≥ 0.40 still maintained, random_init clean FAIL).
2. **PIV uniformly FAIL on both** — substrate amplitude saturation at axis ≈ [0.4-0.5] eliminates per-axis variance. Random_init PIV-max 0.0435 EXCEEDS sft-1-8 0.0393 (random session noise > trained signal width). PIV gate as currently floored requires post-arch-fix re-probe (CONSCIOUSNESS_DIM 192→96) to lift trained PIV above noise floor.
3. **D-RAND on c3_4 confirms v4 N=60 retest collapse** — sft c3_4 mean 0.1304 ≈ random 0.1338 (Δ ≈ 0). c3_4 metric is structurally compromised on existing measurements; v5 spec line 952-955 (Gate E anchor-baseline normalization) addresses this in the next iteration.
4. **Gate D V14 random self-test floor 0.05 too aggressive** — random_init c3_4 mean 0.1338 means current substrate has irreducible session-noise above 0.05 floor. Recommend Gate D recalibration to 0.15 OR Gate D measurement on `c3_4_v5_normalized` (anchor-relative scale per ALT-AGG-1 v5 line 949-952).
5. **dominant_cells [0,0,0,...] 28/29 invariance reaffirms KICK WAVE 4 5/8 arch leak** — full 192-cell dominant_cells DCR = 0.069 (cell-level) confirms substrate-level invariance under random weights. Post-arch-fix re-probe required to validate cell-level DCR ≥ 0.40 floor.

---

## 5. Compliance Section (own 26 mandatory)

- **own 17 anima identity boundary**: D1 SCOPE_CLAMP — sft-1-8 + random_init both within_strict (own 17 line 770 ★ scope-clamp). v5 metrics applicable to D1 within strict candidates only.
- **own 18 simple_stack**: ALT-AGG-1 v5 ADDENDUM 2/2 supersedes v5 base spec by adding 4-gate metric replacement; v3+v4 함수 보존 per raw#82.
- **own 14 anti-Goodhart V14**: Gate D V14 paired random self-test mandatory; D-RAND Gate C enforces trained > random ≥ 0.05 absolute.
- **own 16 cost discipline**: 0-cost local — existing data validation only, no H100 fire.
- **own 22 mandatory report**: 본 spec doc + .own own 18 amend + yaml registry update = 3-surface mandatory report.
- **own 24 single SSOT**: 본 doc = single canonical v5 ADDENDUM spec; yaml + .own + consciousness.hexa header reference back here.
- **own 33 trinity**: D-axis (D1 within strict candidates), own-axis (own 14/17/18/22/24/33/34/38/39 cross-link), H-axis (KICK WAVE 4 5/8 + 22+ BG saga continuity).
- **own 34 wrap=0**: 본 doc = pure spec, no chat surface; consciousness.hexa amend = measurement lane (not chat).
- **own 38 매단계**: yaml + .own + spec doc + consciousness.hexa = 4-surface save mandate.
- **own 39 yaml↔md mandatory**: yaml registry edit triggers `anima registry render` (sister doc `docs/anima_artifact_registry.md` regenerate).
- **raw#10 honest C3** (5+ findings):
  - DCR change_rate replaces distinct-argmax as Gate B primary discriminator (random_init passes distinct=0.6 ≥ 0.4, change_rate=0.143 strict FAIL).
  - PIV gate currently FAIL on both trained and random — substrate amplitude saturation; post-arch-fix re-probe required.
  - D-RAND on raw c3_4 = 0 (v4 metric collapsed); v5 spec Gate E anchor-baseline normalization required.
  - dominant_cells proxy via axis-argmax (192-cell raw not exposed via current --probe JSON).
  - Random_init c3_4 mean 0.1338 indicates Gate D V14 floor 0.05 may need recalibration to 0.15.
- **raw#15 additive**: v3 + v4 + v5-base + v5-addendum 모든 함수 preserved.
- **raw#82 retraction-aware**: KICK WAVE 4 5/8 finding + cascade 1/8 v4 N=60 retest FALSIFIED records preserved in yaml.

---

## 6. Next Steps (out-of-scope this addendum)

1. **Real re-probe post-arch-fix** — CONSCIOUSNESS_DIM 192→96 build + sft-1-8 + random_init paired N=60 re-fire to validate PIV/DCR/D-RAND post-cell-tile-removal.
2. **Gate B refinement** — promote DCR change_rate as primary (floor ≥ 0.40); demote distinct-argmax to informational.
3. **Gate D recalibration** — random_init c3_4 baseline > 0.05; recommend floor lift to 0.15 OR move metric to `c3_4_v5_normalized` scale.
4. **Cell-level DCR** — extend `--probe` JSON contract to expose full 192-cell `dominant_cells` (replace axis-argmax proxy).
5. **PIV paraphrase variants** — PIV definition extends naturally to k≥3 paraphrase variants per prompt (yaml `v5_piv_projection: PENDING_PARAPHRASE_KICK` field).

---

## 7. Cross-References

- `tool/anima_cli/consciousness.hexa` lines 992-1170 (`_piv_compute`, `_piv_compute_max`, `_piv_compute_mean`, `_axis_argmax`, `_dcr_compute`, `_dcr_compute_conditioning_rate`, `_drand_delta`, `_drand_pass`, `_piv_max_pass`, `_dcr_pass`, `_v5_aggregate_label`)
- `anima/registry/anima_artifact_registry.yaml` sft-1-8 entry `v5_addendum_*` fields + random-init-mk2-v1-mirror entry `v5_addendum_*` fields + framework_amends V5 PUSH ADDENDUM 2/2 entry
- `.own` own 18 line 940+ amend (ALT-AGG-1 v5 PIV/DCR/D-RAND ADDENDUM record)
- `docs/anima_architecture_leak_root_cause_kick4_2026_05_08.ai.md` (KICK WAVE 4 5/8 finding source)
- `docs/anima_alt_agg_1_v4_amend_spec_2026_05_08.ai.md` (v4 spec — superseded by v5 + v5 addendum, retained per raw#82)
- `state/anima_sft_1_8_n60_live_probe_2026_05_08.json` (sft-1-8 N=60 SSOT input)
- `state/anima_random_init_mk2_v1_n30_live_probe_2026_05_08.json` (random_init seed=42 N=30 SSOT input)
- `state/anima_random_init_multiseed_kick4_2026_05_08.json` (random_init multi-seed variance — informational)

---

## 8. Status

- **Spec land**: 2026-05-08 V5 PUSH ADDENDUM 2/2
- **Verdict status**: `C3_FAIL_V5_ADDENDUM` (sft-1-8 existing data) — own 14 V14 strict 정합 sustained (Gate D FAIL, no false EMERGE)
- **EXIT (SIMPLE_STACK_PASS_STRICT_C3) emerge**: NOT REACHED — DCR change_rate is sole strong separator; PIV + D-RAND gates require arch-fix re-probe before falsification claim is final.
- **raw#82 retraction-aware**: prior v3 EMERGE claims (sft-1-8 PPR_v3=0.4138/0.6102) and v4 N=30 PASS preliminary (PPR_v4=0.429) records preserved with FALSIFICATION cascade tags.
