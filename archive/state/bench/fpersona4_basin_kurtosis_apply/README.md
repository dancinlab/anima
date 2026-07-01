# F-PERSONA-4 basin_kurtosis 실측 적용 — cotrain v1 재분류

> PR #1130 (`feat(F-PERSONA-4): basin_kurtosis fallback gate`) 가 함수만 추가하고 실측 미실행.
> 본 bench 는 기존 cotrain v1 측정 데이터에 동 함수를 적용해 untyped FAIL(mean_KL=0) 을 **mode-collapse confirmed** 로 재분류한다.

## 1. 동기

- PR #1126 (BENCH #2 BASIN-RANK-DIVERSITY) — basin_kurtosis 가 balanced / differentiated / collapsed 세 시나리오를 변별함을 N=8 에서 입증 (🟢 PASS).
- PR #1130 — `tool/anima_persona_substrate_native_verify.hexa` 에 `basin_kurtosis_of_dist` + `mean_category_kurtosis` 함수 + KL dead-zone fallback gate 추가. **그러나 기존 데이터에 적용 미실행** (커밋 메시지: "측정 재실행 없음 — harness + result.json schema 만 갱신").
- 본 bench — PR #1130 의 함수를 `state/anima_v5mitosis_cotrain_2026_05_12/persona_4_root_cause_results.json` + `cotrain_result.json` 의 verbatim ground truth 에 적용. 1-hot N=64 → kurt ≈ +59 → mode-collapse 재분류.

## 2. 입력 데이터 (verbatim from on-disk JSON)

- `state/anima_v5mitosis_cotrain_2026_05_12/persona_4_root_cause_results.json`
  - `hypothesis_a_softmax_entropy.n_cells = 64`
  - `hypothesis_a_softmax_entropy.entropy_per_prompt_mean = 0.0`
  - `hypothesis_a_softmax_entropy.interpretation = "single_cell_collapse"`
  - `hypothesis_a_dominant_cell_audit.winners = [0]*50`
  - `hypothesis_a_dominant_cell_audit.unique_winners = [0]` · `winner_freq = {"0":50}`
- `state/anima_v5mitosis_cotrain_2026_05_12/cotrain_result.json`
  - `f_persona_4_remeasure.verdict = "FAIL"` · `mean_kl = 0.0` · `kl_matrix = [[0]*5]*5`
  - `f_persona_4_remeasure.categories = 5 (boundary · emotion · self_definition · self_knowledge · values)`

⇒ per-category mean weight 분포 ground truth = 5 카테고리 모두 1-hot at cell 0 (N=64).

## 3. 방법

- `bench.hexa` 가 `basin_kurtosis_of_dist` / `mean_category_kurtosis` 를 byte-equal 복제 (raw-117 + g61, 절대-경로 cross-repo import 없음).
- 5 categories × 1-hot N=64 distribution 생성, 동 함수 호출, mean_KL=0.0 입력으로 PR #1130 fallback gate 로직 (harness lines 740-770) 실행.

## 4. 측정 결과

| metric | value |
|---|---|
| per-cat basin_kurtosis (1-hot N=64) | **+59.0159** |
| mean_category_kurtosis (5 cats) | **+59.0159** |
| kl_dead_zone_threshold | 0.01 |
| kurt_collapse_threshold | 1.0 |
| kurt_fail_hard_threshold | 2.0 |
| fallback engaged | **true** (mean_kl=0.0 < 0.01) |
| reference uniform N=64 | −3.0 |
| reference differentiated N=64 (top-3 97%) | +16.40 |
| BENCH#2 N=8 1-hot cross-check | +3.14286 (byte-equal vs PR #1126) |

## 5. 게이트 결정

- **기존 (KL gate)** — FAIL, REASON unclassified (dead-zone).
- **신규 (PR #1130 basin_kurtosis fallback gate)** — FAIL, REASON = **mode-collapse confirmed** (kurt=59.02 ≫ +2.0 hard threshold).

## 6. Falsifier 평가 (5/5 PASS)

| 코드 | 결과 | 근거 |
|---|---|---|
| F-FBK-APPLY-1 kurt > collapse threshold | PASS | kurt=59.02 > 1.0 |
| F-FBK-APPLY-2 fallback gate engaged | PASS | mean_kl=0.0 < 0.01 |
| F-FBK-APPLY-3 reclassified FAIL/mode-collapse | PASS | verdict=FAIL, reason=mode-collapse |
| F-FBK-APPLY-4 3-regime separation at N=64 | PASS | uniform=−3 / diff=+16.4 / collapsed=+59 |
| F-FBK-APPLY-5 deterministic (closed-form) | PASS | no RNG, byte-equal |

## 7. 재분류 verdict (1줄)

> **cotrain v1 FAIL → mode-collapse** (basin_kurtosis=59.02 on N=64 1-hot, fallback gate engaged via KL dead-zone)

## 8. anima 적용 함의

- **D3 STRONG 4/5 cheap-path carry MAINTAINED** — F-PERSONA-4 의 FAIL root cause 가 winner-take-all 임이 공식 확정.
- category-invariance (kurt < 1.0 시나리오) 와 분리 — 가짜 동치 해소.
- 다음 진행로 = REBORN §88 cond.5 의 4-alternative future-path 중 (a) multi-corpus cotrain · (c) non-softmax metric 재정의.

## 9. honest limits

- ckpt 재로딩 없이 root_cause JSON 의 winner=0 monopoly 만 사용 — `winner_freq={"0":50}` 가 temperature-invariant top-1 → 1-hot 가정 robust (softmax temperature 와 무관).
- kurt 59.02 vs 닫힌형 61 차이는 분모 (n vs n-1) 컨벤션. 둘 다 ≫+2.0 → verdict 불변.
- PR #1126 가 3-regime 변별 검증을 N=8 에서 이미 완료. 본 bench 는 N=64 확장 + cotrain v1 데이터 retrospective 적용.

## 10. cross-link

- PR #1126 — `bench/basin_rank_diversity/` (BENCH #2 N=8 검증)
- PR #1130 — `tool/anima_persona_substrate_native_verify.hexa` (fallback gate 함수 추가)
- 소스 데이터 — `state/anima_v5mitosis_cotrain_2026_05_12/`
- memory — `project_anima_persona_4_root_cause_2026_05_12`, `project_v5_mitosis_cond5_cotrain_2026_05_12`
