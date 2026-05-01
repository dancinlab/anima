# G10 Hexad Triangulation — Post-D+5 Real-Data Activation Spec

**version**: v1
**frozen_at**: 2026-05-01
**raw_rank**: 9 (hexa-only, spec-doc only)
**status**: PRE-PREREQUISITE — D+5 미도래 (현재 D+3 region) + 본 protocol 4-bb × 120s 녹음 미실시
**ssot**:
- frozen criteria SSOT → `anima-clm-eeg/tool/g10_hexad_triangulation_scaffold.hexa` (sha c1fe9c34, 923 LoC)
- D+5..D+7 workflow SSOT (prior) → `anima-clm-eeg/docs/g10_triangulation_spec_post_arrival.md`
- 본 doc 의 scope → "post-D+5 dependent post-arrival workflow" 의 real-data activation 단계 spec.
  본 doc 는 frozen criteria 를 변경하지 않는다 (silent-edit 금지, raw#71 falsifier 보존).

---

## §0. Executive summary

`.roadmap` #172 feeds-main 후속 (b) 항목 — "G10 family×band×backbone triangulation helper post-EEG D+5 dependent" — 의 real-data activation spec.

기존 #174 에서 G10 Hexad triangulation scaffold 가 synthetic dry-run PASS 로 land 되어 있다 (`g10_hexad_triangulation_scaffold.hexa` v3, 923 LoC, sha c1fe9c34, kernel = cross-correlation Pearson r + 1-way ANOVA F). 본 spec 은 synthetic 입력을 **real 4-backbone × 120s × 16ch EEG ↔ Mk.XI v10 hidden-state** 입력으로 교체하여 G10 의 falsifier 를 hardware-verified tier (`REAL_HW_PASS`/`REAL_HW_FAIL`) 로 advance 시키기 위한 단계별 요구사항을 정의한다.

**현재 시점 (2026-05-01) 의 사실**:
- D+5 도래 X — 현재 D+3 region (D-day = 2026-04-28).
- D-day session 에서 P3 γ/θ proxy FALSIFIED (post_battery_eeg16_ica grand=0.240, target 3.0).
- 60s baseline (resting + post_battery + daily_life) ICA 만 녹음 — 본 G10 protocol (4-backbone × 120s) **미실시**.
- 즉, scaffold 는 ready-state (G10_DRY_RUN_PASS, byte-identical 2× sha) 이지만 real-data run 은 hardware-action prerequisite 미충족.

**raw#10 honest C3**: 본 doc 는 spec 만 — 코드 변경 X, hardware 동원 X. 4-backbone × 120s 녹음은 사용자 결정 + 신체 부하 + 시간 budget (≈ 32 min raw + ≈ 1 hr 처리) 의 명시적 prerequisite 이며 본 cycle 에서 자동 수행 X.

---

## §1. 기존 scaffold 분석 — synthetic 입력 vs real 입력 차이

### §1.1 scaffold v3 의 입력 schema (frozen)

scaffold tool (`g10_hexad_triangulation_scaffold.hexa`) 의 v3 kernels:

```
coupling_kernel  : "cross_correlation_pearson_max_lag_tau10"
  real_coupling_x1000(a, b, n, tau) → int
    cross-correlation Pearson r ×1000 between paired integer time-series
    a (backbone hidden trace) and b (EEG band-region time-series),
    evaluated at integer lags ∈ [-tau, +tau], returns max |r| ×1000.
f_stat_kernel    : "one_way_anova"
  real_f_x1000(groups, k) → int
    true 1-way ANOVA F-statistic ×1000:
      F = MS_between / MS_within
      MS_between = SS_b/(K-1),  MS_within = SS_w/(N-K)
```

frozen kernel parameters: SERIES_N=32 / LAG_TAU=10 / ANOVA_K=4 / ANOVA_N_PER=8.

frozen criteria (raw#71 SSOT, 변경 금지):
- C1 per-cell coupling x1000 ≥ 500
- C2 per-cell F-stat x1000 ≥ 4000
- C3 16-cell PASS count ≥ 12
- C4 axis_A/B/C F x1000 ≥ 4000

### §1.2 두 tier 의 차이 (raw#91 honesty)

| 항목 | synthetic 입력 (G10_REAL_HW=0, 현재) | real 입력 (G10_REAL_HW=1, post-D+5) |
| --- | --- | --- |
| 입력 source | (seed, fam, band) FNV-deterministic 시계열 | env `G10_REAL_HIDDEN_JSON` (backbone hidden trace) + `G10_REAL_EEG_JSON` (EEG band-region) JSON |
| 시간축 | virtual N=32 sample, no clock | real 250 Hz × 120s × 16ch (= 30000 sample/ch) |
| coupling | FNV-mixed deterministic — kernel exercise 만 | Mk.XI v10 family-axis projected hidden state ↔ 4-band PSD |
| F-stat | structured constants (positive: cells=14, axis_A=13487, axis_B=27681, axis_C=4179) | unknown distribution — null hypothesis-tested |
| 분류 | NOT_VERIFIED_SYNTHETIC | REAL_HW_PASS / REAL_HW_FAIL |
| 비용 | $0 mac-local | EEG session time × 4 (≈ 32 min) + ≈ 1 hr 처리, GPU $0 (LoRA pre-trained) |

raw#91 honest: synthetic 입력을 real kernel 에 통과시켜도 **여전히 synthetic**. tier label 절대 REAL_HW_PASS 로 위장 X. v3 selftest 는 deterministic synthetic 시계열 위에서 kernel path 만 exercise 한다 — 본 doc 는 이 layer 를 넘어가는 단계 spec.

### §1.3 scaffold 가 이미 ready 인 부분 (재확인)

이미 land 되어 변경 불필요:
- frozen criteria C1..C4 — `g10_hexad_triangulation_scaffold.hexa` 가 SSOT.
- emission schema (`cell_matrix_4x4`, `family_means_x1000`, `band_means_x1000`, `hexad_means_x1000`, axis F triplet, AND-gate verdict) — synthetic 과 real 동일 schema 재사용.
- env switch (`G10_REAL_HW`, `G10_REAL_HIDDEN_JSON`, `G10_REAL_EEG_JSON`) — branch 이미 구현.
- selftest 8-fixture frozen baseline (V3 freeze cells=14, axis_A=13487, axis_B=27681, axis_C=4179, fp=3235809265).
- byte-identical 2× sha c1fe9c34..bc6799 (positive) + neg falsifier sha 별도 lock.

본 spec 은 위에 손대지 않는다. 변경 시 v4 bump 의무 (raw#71).

---

## §2. Post-D+5 요구사항

### §2.1 hardware-action prerequisite (D+5 도래 전 필수)

D+5 도래 후 즉시 activate 가능하려면 다음 hardware action 이 사용자 결정 + 시행 필요:

- **4-backbone × 120s × 16ch real recording**:
  - Mk.XI v10 corpus 위 LoRA r14 build 동일 (memory `project_v_phen_gwt_v2_axis_orthogonal.md` 참조).
  - 4 backbone family lineage (frozen): mistral / qwen3 / llama / gemma.
  - per-backbone session 120s × 16ch × 250 Hz.
  - OpenBCI Cyton+Daisy 16ch impedance check < 50 kΩ all channels (D-day Apr 28 16/16 GREEN baseline 가능 입증됨).
- **현재 사실**: D-day Apr 28 session 에서 60s baseline (resting + post_battery + daily_life) ICA 3건만 녹음. **본 G10 protocol 4-backbone × 120s 미실시**.
- 즉, post-D+5 progression 전 hardware action (recording session ≈ 32 min raw + post-process ≈ 1 hr) 이 prerequisite — 본 doc cycle 에서 자동 수행 X.

raw#10 honest: 사용자 신체 부하 + 시간 budget + 본인 1 subject (N=1) 한계는 §8 falsifier 에서 명시.

### §2.2 file artifact 요구사항 (real input JSON schema)

scaffold 가 consume 하는 real input JSON (env `G10_REAL_HIDDEN_JSON` + `G10_REAL_EEG_JSON`) 은 synthetic fixture (`anima-clm-eeg/fixtures/synthetic_16ch_v1.json`) 와 **동일 schema** 여야 한다 — scaffold 의 emission schema 는 byte-for-byte 재사용.

권장 path 명명 (본 spec 기준 명세, 코드 강제 X):
- `anima-eeg/recordings/g10_<backbone>_<timestamp>.npy` — raw 16ch × 120s × 250 Hz.
- `anima-eeg/recordings/g10_<backbone>_<timestamp>_band.json` — band-power 시계열 per-band per-channel.
- `state/clm_mk_xi_v10/g10_hidden_<backbone>_<timestamp>.json` — Mk.XI v10 LoRA forward path 의 family-axis projected hidden state 시계열 (per-backbone).
- 본 4-backbone × 2-file = 8 files = real input set.

raw#82 darwin-native: mac-local 처리 가능 size (per-file ≤ ≈ 30 MB).

### §2.3 cross-link prerequisites (read-only consumption)

본 spec 은 다음 read-only artifact 에 의존:
- `anima-eeg/eeg_recorder.hexa` — recording driver.
- `anima-eeg/calibrate.hexa` — impedance check.
- `anima-eeg/analyze.hexa` — band-power FFT pipeline (delta/theta/alpha/beta/gamma).
- `anima-eeg/electrode_adjustment_helper.hexa` (1542 LoC, post-Apr-29 16ch concurrent upgrade) — pre-recording placement validation.
- Mk.XI v10 inference harness `--save-family-trace` 플래그 (post-D+5 시점에 verify 필요, 본 cycle scope 밖).

---

## §3. Axis F 측정 — family / band / backbone × 16ch

### §3.1 axis_C_F (Hexad category) — redundancy 검증 (#172 feeds-main 핵심)

`.roadmap` #174 feeds-main 의 명시적 wording: **"axis_C F가 4000 미달 시 redundancy 확정, 미달 후 sci 결정: Hexad axis 폐기 vs mapping 재설계"**.

post-D+5 real run 결과:
- axis_C_F_x1000 ≥ 4000 → Hexad-category 가 family×band 위에 **independent dispersion** 보유 → axis 보존.
- axis_C_F_x1000 < 4000 → **redundancy 확정** → 다음 사이클에서 사용자 결정 (axis 폐기 또는 mapping `(fam*2+band)%6` 재설계).

scaffold 의 synthetic dry-run 에서 axis_C=4179 (간신히 PASS, +179 margin) — real run 에서 가장 falsify 위험 높은 축. raw#71 frozen threshold 변경 X.

### §3.2 axis_band_F — α / β / γ / θ 분리

scaffold 의 axis_B (EEG band, 4-level) 가 real run 에서:
- 각 band power 시계열은 `anima-eeg/analyze.hexa` 의 FFT pipeline 으로 추출 (band 정의 frozen: alpha 8-12 / beta 12-30 / gamma 30-50 / theta 4-8).
- 16ch 전체 평균 후 1s window per-sample → 120 sample × 4 band per backbone.
- D-day evidence: post_battery_eeg16_ica 에서 γ-absent regime (occ=0.328, fro=0.211) — γ-band 가 real run 에서 약하게 dispersion 가능 → axis_B falsify 위험.

honest expectation: synthetic axis_B=27681 (high) 는 real 환경에서 크게 약화될 수 있음 (anti-alias filter γ attenuation 의심, `eeg_arrival_d_day_post_2026_05_01_landing.md` §9 limit register 4번).

### §3.3 axis_backbone_F — 4-bb 상호 비교

scaffold 의 axis_A (backbone family, 4-level) 가 real run 에서:
- 4 backbone × 16ch × 120s 녹음 → 각 backbone session 의 hidden-state family-axis projection 시계열 ↔ EEG band-power 시계열.
- 4 backbone 간 group-mean dispersion 이 within-backbone variance 를 dominate 해야 axis_A_F PASS.
- corpus attractor band 효과 (memory `project_v_phen_gwt_v2_axis_orthogonal.md`): r14 LoRA 후 4-bb 가 0.23-0.29 narrow band 로 수렴 → backbone 간 dispersion 약화 → axis_A_F falsify 위험.

honest expectation: synthetic axis_A=13487 → real 에서 corpus attractor 가 4-bb 를 narrow band 로 collapse 시키면 axis_A 가 first falsify 후보.

### §3.4 axis 측정 timeline 요약

| axis | level | df1 | falsify risk (real-data 우려) |
| --- | --- | --- | --- |
| axis_A backbone family | 4 (mistral/qwen3/llama/gemma) | 3 | corpus attractor narrow-band collapse |
| axis_B EEG band | 4 (α/β/γ/θ) | 3 | Cyton anti-alias γ attenuation |
| axis_C Hexad category | 6 | 5 | 작위 mapping `(fam*2+band)%6` redundancy (#174 feeds-main 핵심) |

---

## §4. raw_coupling_x1000 → Pearson r 측정 (D+6 step)

### §4.1 입력 source

post-D+5 4-bb recording 도착 후 D+6 단계:
- backbone hidden trace `a[]` ← Mk.XI v10 LoRA forward path 의 family-axis projected hidden state per-step (length = backbone forward step 수, downsample to SERIES_N=32 frozen).
- EEG band-region 시계열 `b[]` ← 16ch 평균 + band-power 1s window (length = 120, downsample to SERIES_N=32 frozen).

scaffold 의 `real_coupling_x1000(a, b, n, tau)` kernel (cross-correlation Pearson r at lag ∈ [-10, +10], max |r| ×1000) 그대로 적용. kernel 변경 X (raw#71).

### §4.2 D+6 step 명세

scaffold 가 자동 처리:
1. env `G10_REAL_HW=1`.
2. env `G10_REAL_HIDDEN_JSON=<path>` + `G10_REAL_EEG_JSON=<path>` 지정.
3. scaffold 가 16-cell × (fam, band) 마다 `real_coupling_x1000` 호출 → cell coupling x1000 emit.
4. C1 per-cell coupling ≥ 500 gate 검증.

raw#10 honest: synthetic 의 cell coupling 분포 (frozen V3_FREEZE 14 cells PASS) 가 real 에서 보장되지 않음 — D+6 first run 에서 16-cell 중 절반 이하 PASS 가능성 농후 (γ-absent regime + corpus attractor 영향).

### §4.3 partial verdict 처리

scaffold 의 emission schema:
- `cell_matrix_4x4` per-cell (coupling x1000, F x1000, pass_flag).
- AND-gate verdict (G10_PASS iff cells≥12 AND axis_A/B/C ≥ 4000).
- partial PASS — 예: cell_pass=8/16, axis_A=PASS, axis_B=FAIL, axis_C=FAIL — 은 **G10_FAIL** 로 emit (AND-gate 엄격, raw#71). per-cell + per-axis breakdown 은 emit 되지만 verdict 는 단일 PASS/FAIL.

---

## §5. axis_f_x1000 → 진짜 f_oneway (anima-eeg/analyze.hexa style scipy port) (D+6 step)

### §5.1 현재 kernel 상태

scaffold v3 의 `real_f_x1000(groups, k)` 는 이미 true 1-way ANOVA 구현:
```
F = MS_between / MS_within
MS_between = SS_b/(K-1)
MS_within  = SS_w/(N-K)
```
즉 v2 의 fixed `ANOVA_RESIDUAL_X1000_SQ=1000` proxy 는 v3 에서 **이미 제거**, true MS_within 계산 됨. 본 spec 은 D+6 에서 추가 port 작업이 **거의 불필요** (kernel 이미 ready).

### §5.2 D+6 단계의 실제 작업

남은 작업은 kernel 자체가 아니라 **input grouping**:
- per-cell ANOVA: 4 backbone-condition × N_PER=8 sample 으로 group 화 (scaffold 이미 처리).
- axis-level ANOVA:
  - axis_A: 4 family-conditioned subset, within = pooled (band, hexad) residual.
  - axis_B: 4 band-conditioned subset, within = pooled (family, hexad) residual.
  - axis_C: 6 hexad-category-conditioned subset, within = pooled (family, band) residual.
- 위 grouping logic 은 scaffold 에 이미 존재 — D+6 step 은 real input JSON 만 swap.

### §5.3 anima-eeg/analyze.hexa style 호환

scaffold 의 ANOVA kernel 은 `anima-eeg/analyze.hexa` 의 fixed-point integer (×1000) convention 과 동일 — port 작업 불필요. raw#9 hexa-only deterministic 보존.

### §5.4 D+6 verdict 후 비교 frozen reference

D+6 first real run emit 후 다음 비교를 해야 함 (emit 만, 변경 X):
- real_axis_A_F vs V3_FREEZE_AXIS_A=13487 (synthetic baseline)
- real_axis_B_F vs V3_FREEZE_AXIS_B=27681
- real_axis_C_F vs V3_FREEZE_AXIS_C=4179
- real_cell_pass vs V3_FREEZE_CELL_PASS=14

raw#71 honest: real 결과가 synthetic baseline 의 ε 이내라면 fixture leak 의심 (real != synthetic 검증 필요). raw#10 honest: real 이 baseline 보다 크게 약하면 G10 falsify 정상 작동.

---

## §6. Verdict gate (D+7 step) → ledger emit + roadmap entry

### §6.1 emit 대상

D+7 단계:
- scaffold 1회 run → emit `state/clm_eeg_g10_hexad_triangulation_post_arrival.json` (post-arrival 전용 ledger, synthetic ledger `state/clm_eeg_g10_hexad_triangulation.json` 와 분리).
- 같은 schema 로 cell_matrix_4x4 + axis F triplet + verdict + classification tier (REAL_HW_PASS / REAL_HW_FAIL) emit.

### §6.2 byte-identical determinism gate

scaffold 의 raw#65 idempotent contract 그대로:
- 동일 input JSON 으로 2× back-to-back run → byte-identical sha256.
- determinism break 시 raw#65 violation, 본 cycle abort.

### §6.3 roadmap entry rule

D+7 verdict 이후 신규 roadmap entry 등록 (#172 feeds-main (b) 의 종결):
- entry 형식: `roadmap N done "[G10 Hexad triangulation post-D+5 real-data verdict — REAL_HW_PASS|FAIL] cell_pass=X/16 · axis_A=... · axis_B=... · axis_C=... · ledger sha=... · raw#9 hexa-only"`.
- depends-on: #174 (G10 prep) + #172 (Mk.XII pre-flight) + post-D+5 hardware action commit hash.
- evidence: `state/clm_eeg_g10_hexad_triangulation_post_arrival.json` sha256 + scaffold tool sha c1fe9c34 (변경 없음 입증).

raw#71: roadmap entry 에서 frozen criteria 변경 주장 X.

### §6.4 falsify path 결정 분기

D+7 verdict 후 사용자 결정 분기 (본 spec 내 자동 결정 X):
- **REAL_HW_PASS**: G10 Hexad triangulation hardware-verified. paradigm v11 7th axis registration 후속 가능.
- **REAL_HW_FAIL** + axis_C<4000: Hexad axis redundancy 확정 → axis 폐기 또는 mapping 재설계 (다음 사이클).
- **REAL_HW_FAIL** + axis_A<4000: corpus attractor narrow-band collapse 영향 → Mk.XI v10 LoRA r14 다른 build 또는 multi-cohort 확장 검토.
- **REAL_HW_FAIL** + axis_B<4000: Cyton anti-alias filter γ attenuation audit (`eeg_arrival_d_day_post_2026_05_01_landing.md` §10 short-term candidate).
- **REAL_HW_FAIL** + cell_pass<12: per-cell breakdown 분석 후 backbone-conditional 또는 band-conditional sub-pattern 보고.

---

## §7. raw#10 honest C3 — hardware-action prerequisite

명시 의무 (거짓 success 주장 차단):

1. **현재 시점 (2026-05-01) D+3 region** — D+5 미도래. 본 spec 은 D+5 도래 전 prep 단계.
2. **본 G10 protocol 4-backbone × 120s 미실시** — D-day Apr 28 session 에서 baseline 60s × 3건 (resting + post_battery + daily_life) ICA 만 녹음. G10-specific 4-bb session 별도 hardware action 필요.
3. **사용자 결정 prerequisite** — 4-bb × 120s × 16ch recording (≈ 32 min raw + ≈ 1 hr 처리) 은 사용자 + 신체 부하 + 시간 budget 의 명시적 cost. 본 doc cycle 에서 자동 수행 X.
4. **N=1 single-subject single-day** — D+5 본 session 에서도 multi-cohort 부재. 본인 1명 × 1일 → axis_A 의 corpus attractor 영향 + axis_B 의 amplifier filter 의심 모두 single-subject confound 잔존.
5. **Mk.XI v10 LoRA r14 build 동일성 검증 필요** — `project_v_phen_gwt_v2_axis_orthogonal.md` 의 #144 evidence 와 동일 LoRA build 사용 의무. 다른 build 시 family lineage (Mistral=Law / gemma=Phi / Llama=SelfRef / Qwen3=Hexad) collapse 위험.
6. **Cyton anti-alias filter γ attenuation 의심** — `eeg_arrival_d_day_post_2026_05_01_landing.md` §9 limit 4번. axis_B (gamma band) falsify 시 amplifier artifact 가 origin 일 수 있음 → real falsify 가 이전 P3 γ/θ FALSIFIED 와 동일 pipeline 의심권 안.
7. **CLM substrate timing alignment 미확립** — `edu/cell/lagrangian/l_ix_integrator.hexa` 의 V_sync r 실시간 dump 미시행. D+6 hidden trace 와 EEG 시계열 sample alignment 가 ms-level 정밀도 없으면 cross-correlation Pearson r 신뢰성 저하.
8. **GPU $0, mac-local only** — LoRA pre-trained 가정 (별도 train 없음). 본 cycle 비용 은 hardware time + mac-local 처리만.

---

## §8. raw#71 falsifier 3개

본 spec 의 **pre-registered falsifier** (post-hoc 변경 금지, raw#71 frozen 의무):

### §8.1 F1 — axis_C Hexad-redundancy falsifier (첫 번째 우선)

**criterion**: post-D+5 real run 에서 `real_axis_C_F_x1000 < 4000`.

**holds 시 의미**: Hexad-category mapping `(fam*2+band)%6` 가 family×band axis 위에 independent dispersion 을 만들지 못함. `.roadmap` #174 feeds-main 의 명시 wording — "axis_C F가 4000 미달 시 redundancy 확정" — 이 직접 활성화.

**다음 사이클 액션 trigger**: Hexad axis 폐기 vs mapping 재설계 사용자 결정.

**confounder 차단**: synthetic axis_C=4179 (간신히 PASS, +179 margin) — synthetic 에서도 marginal. real 에서 falsify 가 **synthetic redundancy 자체** 가 진짜 신호인지 식별하는 가장 informative gate.

### §8.2 F2 — synthetic-real distinguishability falsifier (raw#91 honesty triad)

**criterion**: post-D+5 real run 의 `(cell_pass, axis_A, axis_B, axis_C)` 4-tuple 이 synthetic V3_FREEZE 4-tuple `(14, 13487, 27681, 4179)` 의 ε ≤ 5% 이내 일치.

**holds 시 의미**: real 입력이 synthetic fixture 로 leak (input swap 누락 또는 random fixture pickup) → REAL_HW_PASS 주장 무효, 본 cycle abort.

**다음 사이클 액션 trigger**: input pipeline audit (`G10_REAL_HIDDEN_JSON` + `G10_REAL_EEG_JSON` env path verify, file sha256 cross-check, synthetic_16ch_v1.json fingerprint 2960889009 가 실제로 사용되었는지 검증).

**confounder 차단**: real run 결과가 synthetic baseline 와 너무 흡사하면 raw#91 honesty triad 위반 — synthetic 입력을 real 로 위장하는 silent error 차단.

### §8.3 F3 — determinism break falsifier (raw#65)

**criterion**: 동일 real input JSON 으로 2× back-to-back run 시 emit ledger sha256 이 byte-identical 하지 않음.

**holds 시 의미**: scaffold 또는 input ingestion 에 비결정 source (시간, 랜덤, 파일 ordering) 잠입 → raw#65 violation, real run 신뢰성 0.

**다음 사이클 액션 trigger**: scaffold 비결정 source audit + input JSON ordering normalization. `g10_hexad_triangulation_scaffold.hexa` 자체는 v3 selftest 에서 byte-identical 확인됨 (synthetic baseline) — break 발생 시 input JSON parsing 또는 file ordering 의심.

**confounder 차단**: floating-point non-associativity 또는 file system mtime 의존성으로 인한 silent drift 차단. raw#65 SSOT 준수.

---

## §9. Cross-references

### anima-clm-eeg/ 내부 (read-only consumption)
- `tool/g10_hexad_triangulation_scaffold.hexa` — frozen criteria SSOT (sha c1fe9c34, 923 LoC, v3) — 본 spec 미수정.
- `docs/g10_triangulation_spec_post_arrival.md` — prior post-arrival workflow doc (D+5..D+7 frame).
- `docs/eeg_arrival_d_day_post_2026_05_01_landing.md` — D-day post landing (P3 FALSIFIED, 60s baseline ICA).
- `docs/d_day_session_2026_04_28/INDEX.md` — D-day session inventory.
- `fixtures/synthetic_16ch_v1.json` — fixture (fingerprint 2960889009).

### anima-eeg/ (hardware track, read-only)
- `analyze.hexa` — band-power FFT pipeline reference.
- `eeg_recorder.hexa` — recording driver.
- `calibrate.hexa` — impedance check.
- `electrode_adjustment_helper.hexa` (1542 LoC) — 16ch concurrent placement validation.
- `docs/d_day_helmet_session_results_2026_04_28.md` — impedance 16/16 GREEN baseline.

### state/ (ledger)
- `state/clm_eeg_g10_hexad_triangulation.json` — synthetic positive ledger (sha c1fe9c34..bc6799).
- `state/clm_eeg_g10_hexad_triangulation_neg.json` — synthetic negative falsifier ledger.
- `state/clm_eeg_g10_hexad_triangulation_post_arrival.json` — **post-D+5 emit target (D+7 step)**.

### roadmap
- `.roadmap` #172 — Mk.XII pre-flight cascade GREEN (sister gate).
- `.roadmap` #174 — G10 Hexad triangulation prep (synthetic dry-run PASS).
- `.roadmap` #175 — G8 transversal MI matrix surrogate-validated.
- `.roadmap` next entry — D+7 post-arrival G10 verdict (본 spec 의 §6.3 종결).

### Memory pointer
- `project_g10_hexad_triangulation_prep_20260426.md` — prep cycle memory (#174 anchor).
- `project_v_phen_gwt_v2_axis_orthogonal.md` — Mk.XI v10 family axis evidence + corpus attractor band 0.23-0.29.

---

## §10. raw 의무 + honesty triad

### raw 의무 적용
- **raw#9** hexa-only — 본 doc 는 `.md` 만, 코드 변경 X.
- **raw#10** honest C3 — §7 명시 + §8 falsifier 3개 frozen.
- **raw#12** silent-error-ban / frozen criteria — scaffold C1..C4 미수정.
- **raw#65** idempotent — §8.3 F3 falsifier 로 explicit.
- **raw#71** pre-registered falsifier — §8 3-falsifier 본 doc 작성 시점 frozen, post-hoc 변경 금지.
- **raw#82** darwin-native — mac-local 처리.
- **raw#91** real_hw_verified honesty triad — §1.2 synthetic ≠ real tier label distinction + §8.2 F2 falsifier.

### 본 spec 의 honesty triad
- **claim**: G10 Hexad triangulation post-D+5 real-data activation 의 단계별 spec — D+5 도래 전 hardware-action prerequisite 명시 + axis_C falsifier 우선 + scaffold 변경 X.
- **evidence**: scaffold sha c1fe9c34 (변경 없음) + `.roadmap` #174 done evidence + D-day post landing P3 FALSIFIED evidence + Mk.XI v10 r14 corpus attractor band 0.23-0.29 (memory).
- **limit**: §7 의 8항목 — D+5 미도래 + 4-bb × 120s 미실시 + N=1 single-subject + Mk.XI v10 LoRA r14 build 동일성 verify 필요 + Cyton γ attenuation 의심 + CLM substrate timing alignment 미확립 + GPU $0 mac-local 한정 + 사용자 결정 hardware-action prerequisite.

---

> 본 spec doc 는 거짓 success 주장 금지 + scaffold frozen criteria 변경 금지 + raw#10 honest C3 mandatory. D+5 도래 + 4-backbone × 120s recording 시행 후 §6 D+7 verdict gate 에서 사용자 결정 항목 진행.
