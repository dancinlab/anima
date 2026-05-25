---
id: H_274
slug: quorum-cascade-seed-dependence
title: quorum-cascade seed-의존 메커니즘 — H_272 가 발견한 coop cascade under-drive(5/10) 의 성공/실패를 어느 초기 tension 분포통계가 예측하는가 (H_262/H_272 심층)
domain: life · collective · self-organization · seed-dependence · mechanism
status: pre-register-frozen
exploration_method: E0 (meta-result-of-results) + E5 (per-seed property sweep) + E11 (predictor-identification · 분포통계 → outcome 회귀)
verification_method: W4 (verdict-4-class) + W5 (numerical sim) + W12 (sister-link H_262/H_272/H_269)
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-25
since: 2026-05-25 (new)
sister: H_262 (quorum-sensing SUPPORTED_FULL→fragile · cascade 의 origin), H_272 (seed-robust recalibration PARTIAL · adaptive 5/10 under-drive 잔존 진단), H_269 (multiseed-robustness · fragility 진단)
---

# H_274 — quorum-cascade seed-의존 메커니즘

## 1. Hypothesis

H_272 (seed-robust re-calibration) 는 H_262 (quorum-sensing) 의 coop cascade 를
per-seed adaptive base_gain 으로 10 seed {0..9} 재측정하여 **비대칭 fragility**
를 발견했다: adaptive calibration 이 *over-drive* 절반 (control 이 majority 초과)
은 완전 제거 (ctrl_maxq 모든 seed < 0.5) 했으나, *under-drive* 절반 (coop cascade
실패) 은 잔존하여 cascade 가 **5/10 seed (0,1,2,4,6) 성공 · 5/10 (3,5,7,8,9) 실패**
로 갈렸다. H_272 §10 L3 은 이 잔존 fragility 가 substrate tension *구조* (분포
모양) 의 seed-의존이라 결론지었으나 — *어느* 구조 통계가 cascade 성공/실패를
좌우하는지는 미규명으로 남겼다.

본 H 는 그 미규명을 닫는다:

CORE QUESTION:

> H_272 가 발견한 coop cascade 의 seed-의존 성공/실패는 *초기 tension 분포의
> 어느 통계 (mean · var · std · max · min · range · 상위-tail mass · 임계초과
> 개수) 에 의해 예측되는가*? 즉 cascade 성공이 초기 분포로부터 예측 가능한
> 메커니즘인가, 아니면 예측 불가능한 chaotic 현상인가?

핵심 주장: coop cascade 의 성공은 *초기 per-cell tension 분포의 상위-tail mass*
(많은 cell 이 ON-latch 임계에 가까운가) 에 의해 예측되며 — 즉 H_272 의 under-drive
잔존은 *예측 가능한 메커니즘* 을 가진다.

## 2. Why (예측자가 초기 tension 분포인 사유 — PRE-REGISTERED)

- **quorum 동역학의 driver 가 per-cell tension**: H_262/H_272 의 activation 갱신은
  `a_i(t+1) = a_i(t) + (base + tcoef·tension_i) + boost − leak·a_i(t)`,
  `boost = (Q_prev > q_thr) ? coupling : 0`. per-cell intrinsic drive 가
  `base + tcoef·tension_i` 이므로, cell 별 tension 의 *분포 모양* 이 어느 cell 이
  먼저 ON-latch (up_thr=1.0) 에 도달하는가를 결정한다.

- **adaptive base_gain 이 *절대 level* 을 normalize-out → 남는 것은 *모양***:
  H_272 의 per-seed adaptive calibration 은 control max q_final 을 모든 seed 에서
  target window [0.20, 0.45] 에 고정한다 (mean 의 절대값을 pin). 따라서 cascade
  성공의 차이는 *mean 의 절대 level* 이 아니라 — 동일 control level 위에서 coupling
  boost 가 partial quorum 을 q_thr=0.3 위로 밀어 cascade 시킬 만큼 *충분한 cell 이
  ON 임계 근처에 있는가* (상위-tail mass / spread) 에 의존한다. 이것이 본 H 가
  *상위-tail 통계* 를 핵심 예측자 후보로 pre-register 하는 메커니즘적 사유.

- **예측자 식별 = robustness audit 의 다음 grain**: H_269 는 "verdict fragile"
  까지, H_272 는 "fragility 가 비대칭 (over-drive=criterion 결함, under-drive=진짜
  seed-의존)" 까지 보였다. 본 H 는 그 진짜 seed-의존을 *예측자* 로 분해 — "cascade
  실패는 어떤 초기 조건에서 일어나는가" 를 닫는다.

- **cherry-pick 방지의 정직성**: 예측자 후보 8종 (mean · var · std · max · min ·
  range · topk_mass · n_above) 은 *결과를 보기 전에* 사전 고정했고, "성공군이 더
  높아야 메커니즘적으로 해석 가능" 한 방향 (C2) 도 사전 pre-register. ground-truth
  cascade outcome (5/10) 는 H_272 가 *독립적으로* 이미 산출한 것 — 본 H 가 만든 게
  아님 (F4 가 H_272 와의 byte-level 일치를 검정).

## 3. Predictions

| ID | 예측 | 근거 |
|----|------|------|
| H274.1 | ≥1 초기-tension 통계가 success 군 vs fail 군을 large effect (|d| ≥ 0.8) 로 분리 | quorum 동역학이 per-cell tension 의 함수 → 분포통계가 cascade 결과를 결정 |
| H274.2 | 분리 예측자는 상위-tail/spread 계열 (max · range · topk_mass · std · n_above) 이고 success 군이 *더 높음* | 많은 cell 이 ON-latch 근처 → coupling boost 가 cascade 충분 |
| H274.3 | mean 단독은 약한 예측자 (adaptive base_gain 이 control level 을 pin 하여 mean 의 절대값을 normalize-out) | adaptive calibration 이 mean 의 cross-seed 변동을 흡수 |
| H274.4 | cascade outcome (success bool) 이 H_272 와 byte-equal (5/10, 동일 seed) | H_261 leg 까지 replicate 하여 gauss stream 을 H_272 위치에 정렬 |
| H274.5 | 동일 seed cross-process snapshot byte-equal (결정론) | RFC 033 process-global gauss stream re-seed 결정론 |

## 4. Variables

- **axis1_seed** ∈ {0..9} — `__HEXA_FARR_GAUSS_SEED__` 별 *별도 프로세스*
- **axis2_predictor** ∈ {mean, var, std, max, min, range, topk_mass, n_above} —
  coop cascade pool 의 *초기* per-cell tension 분포통계
- **axis3_outcome** = cascade_success bool = `any_coop_switch && !any_ctrl_switch`
  (H_272 의 h262.gate 와 동일 정의)
- **예측자 측정원** = coop cascade pool (`_h262_up_capture(0.3, 0.20, base_cal)`)
  의 *초기* per-cell tension = `_cell_tension` (mean(|hidden|)) on 신선-init pool
  (boost 적용 전, cascade 가 실제로 진화하는 동일 stream-position pool)
- **H_262 substrate param (carried verbatim)**: d=8, N=16, max_steps=40,
  leak=0.05, tcoef=0.11, up=1.0, dn=0.4, coupling=0.20
- **H_272 adaptive param (carried verbatim)**: target [0.20, 0.45], bisection
  [0.0, 0.05] × 28 iter
- **H_261 leg param (stream-alignment only, NOT scored)**: d=8, N=12, steps=20,
  steepness {0.0 flat, 4.0 steep} — H_272 가 H_262 leg 전에 실행한 것을 replicate
- **predictor param (pre-register)**: topk=4 (상위-tail mass), large_d=0.8 (C1
  large-effect), above_thr=0.33 (n_above 의 상위-3분 경계)
- **측정량**: 예측자별 (succ_mean, fail_mean, Δ, pooled_std, |d|, rank_sep,
  higher_succ) · best 예측자 식별 (rank_sep 우선, 동률 시 |d| 최대)

## 5. Run Protocol

- **deterministic**: 각 seed `__HEXA_FARR_GAUSS_SEED__=<s>` (RFC 033) + 결정론적
  Lorenz. seed 별 *별도 프로세스* (in-process 반복은 stream advance 오염).
- **stream-position 정렬 (핵심)**: 각 seed run 은 H_272 의 per-seed sequence 를
  *그대로* 재현 — H_261 leg (flat → steep condition) → adaptive base 보정 →
  control sweep (q 0.3/0.5/0.7) → coop sweep — 하여, coop cascade 에 도달하는
  gauss stream 위치를 H_272 와 byte-identical 로 맞춘다. H_261 leg 은 *점수
  안 매김* (오직 stream advance 용). 정렬 검정 = F4 (base_cal · coop_maxq ·
  cascade_success 가 H_272 result.json 과 일치).
- **two-mode harness** (`run_h274.hexa`):
  - mode `seed` (env `HEXA_H274_MODE=seed HEXA_H274_SEED=<s>`): 한 seed 에서
    sequence 재현 + coop cascade pool 의 초기 tension 분포 capture + 8 예측자
    통계 계산, `snapshots/seed<s>.json` write. driver 가 seed 0..9 별도 프로세스.
  - mode `agg` (env `HEXA_H274_MODE=agg`): 10 snapshot + `det_xproc.txt` 를
    `json_parse` 로 읽어 예측자별 group-separation 분석 + best 예측자 식별 + verdict.
- **group-separation 분석**: 각 예측자에서 success 군 / fail 군 mean 계산,
  normalized separation `|d| = |Δmean| / pooled_std` (Cohen-d style), 그리고
  *perfect rank-separation* (두 군이 단일 threshold 로 완전 분리 = 겹침 없음)
  여부.
- **C3 cross-process**: seed 0 (success) + seed 5 (fail) 를 각각 fresh process
  두 번 실행, snapshot sha256 비교, `det_xproc.txt` 에 `seed<s> PASS/FAIL <a> <b>`.
- **hexa 함정 우회**: `/Users/ghost/.hx/bin/hexa` 절대경로 + 스크립트 `/Users/`
  절대경로 (또는 cwd=worktree root 상대) + `__HEXA_FARR_GAUSS_SEED__` env-prefix.
  본 worktree 는 mac-local `hexa run` 성공 (pool-route 미차단).
- **runtime**: $0 mac local. d=8, no ckpt. `HEXA_MEM_UNLIMITED=1`.
- **artifacts**: `state/h274_cascade_seed_2026_05_25/{run_h274.hexa, result.json,
  det_xproc.txt, snapshots/seed{0..9}.json}`.
- **run cmd (verbatim — seed sweep, per seed s)**:
  `__HEXA_FARR_GAUSS_SEED__=<s> HEXA_H274_MODE=seed HEXA_H274_SEED=<s> HEXA_MEM_UNLIMITED=1 hexa run HEXAD/LIFE/state/h274_cascade_seed_2026_05_25/run_h274.hexa`
- **run cmd (verbatim — aggregation)**:
  `HEXA_H274_MODE=agg HEXA_MEM_UNLIMITED=1 hexa run HEXAD/LIFE/state/h274_cascade_seed_2026_05_25/run_h274.hexa`

## 6. Criteria

- **C1 (분리)**: H274.1 — ≥1 초기-tension 통계가 success vs fail 군을 large effect
  (|d| ≥ 0.8) 로 분리 *AND* perfect rank-separation (두 군이 단일 threshold 로 완전
  분리, 겹침 없음 = *결정론적* 예측자).
- **C2 (해석가능)**: H274.2 — best 예측자가 상위-tail/spread 계열이고 success 군이
  *더 높음* (메커니즘 방향 일치: 상위-tail mass ↑ → ON-latch 근처 cell ↑ → cascade).
- **C3 (결정론)**: H274.5 — 동일 seed cross-process snapshot byte-equal.
- **verdict_rule**:
  - `SUPPORTED` = C1 ∧ C2 (메커니즘적으로 해석 가능한 seed-property 가 cascade
    성공을 *결정론적으로* 예측 → seed-의존 메커니즘 완전 규명)
  - `PARTIAL` = C1 ∧ ¬C2 (통계가 군을 분리하나 방향이 메커니즘적으로 불명확 —
    예측적이나 opaque)
  - `FALSIFIED` = ¬C1 (어느 분포통계도 군을 *결정론적으로* 분리 못함 → cascade 가
    초기 분포로부터 결정론적 예측 불가)

## 7. Falsifiers (pre-registered ≥5, measurable)

- **F1 SEPARATES**: best 예측자가 large-effect (|d| ≥ 0.8) AND rank-sep 미달 →
  C1 FALSIFIED (측정: `best.d >= 0.8 && best.rank_sep`).
- **F2 INTERPRET**: best 예측자가 상위-tail/spread + higher-in-success 미달 →
  C2 FALSIFIED (측정: `is_uppertail(best) && best.higher_succ`).
- **F3 NONTRIVIAL**: success 군 또는 fail 군이 비어 분석 무의미 → degenerate
  (측정: `n_success >= 1 && n_fail >= 1`).
- **F4 GROUNDTRUTH**: cascade outcome 이 H_272 와 불일치 (stream 정렬 실패) →
  분석 대상이 H_272 의 cascade 가 아님 (측정: success seed coop_maxq == 1.0 AND
  fail seed coop_maxq < 0.5 — H_272 의 [1.0,1.0,1.0,0.25,1.0,0.1875,1.0,0.3125,
  0.375,0.25] 과 일치).
- **F5 DETERMINISM**: 동일 seed cross-process snapshot byte-different → raw#9
  위반 (측정: `det_xproc 모든 줄 PASS`).

## 8. Honest Limits (raw#91 c3, ≥5)

- **L1 (10 seed = 작은 표본, 5/5 split)**: success 5 · fail 5 의 group mean 비교는
  각 군 n=5 의 작은 표본. 큰 effect size (topk_mass |d|=1.55, mean |d|=1.53) 는
  표본과 무관하게 robust 한 신호이나, rank-separation 의 정확한 충족/불충족은 더
  많은 seed 에서 안정화 필요. 핵심 finding (상위-tail mass 가 *aggregate* 예측자,
  단 *결정론적* 분리는 미달) 은 견고.

- **L2 (C1 의 perfect-rank-separation 이 strict bar)**: C1 은 large-effect 와
  *perfect rank-separation* 을 둘 다 요구한다 — 후자는 *결정론적* 예측자 (단일
  threshold 로 5 success 와 5 fail 을 완전 분리) 의 기준. 결과는 8 예측자 중 *어느
  것도* perfect rank-sep 미달 (모두 군이 겹침). 만약 C1 이 large-effect 단독이었다면
  4 예측자 (topk_mass · mean · n_above · max) 가 PASS 였을 것 — C1 의 verdict 는
  "결정론적 예측자 부재" 이지 "예측력 부재" 가 아님. raw#82 (post-hoc edit 금지)
  준수를 위해 사전 고정한 strict criterion 을 *유지* (느슨하게 바꾸지 않음).

- **L3 (overlap 의 구체적 원인 = 소수 예외 seed — 핵심 finding)**: best 예측자
  topk_mass 의 정렬은 하위 3 = 전부 FAIL (seed 5/3/8), 상위 3 = 전부 SUCCESS
  (seed 4/2/6) 로 *양 극단은 깨끗* 하다 — overlap 은 *중간대* 의 두 예외 (seed 7
  topk=0.381 FAIL · seed 9 topk=0.393 FAIL 가 success seed 0/1 topk=0.370 보다
  *높은데도* 실패) 가 일으킨다. mean 예측자는 더 깨끗 — 하위 6 중 seed 2 만 SUCCESS,
  상위 4 (0/1/4/6) 전부 SUCCESS, 즉 9/10 을 올바르게 정렬하고 seed 2 (낮은 mean
  인데 성공) 단 하나가 예외. 즉 cascade 성공은 초기 분포로부터 *대부분 예측 가능*
  하나, soft-threshold (boost trigger 의 q_prev>q_thr 비교) 의 *분포 모양 × cascade
  타이밍* 상호작용이 소수 seed 에서 leading 예측자를 뒤집는다.

- **L4 (예측자 다중공선성)**: mean · topk_mass · n_above · max 가 모두 |d| > 1.0
  으로 강하게 success 군이 높음 — 이들은 상호 상관 (분포가 전반적으로 위로 shift
  되면 mean·max·tail·n_above 가 함께 ↑). 따라서 "단일 *독립* 예측자" 라기보다
  "초기 tension 분포가 전반적으로 위쪽 (drive 충분)" 이라는 *하나의 잠재 인자* 의
  여러 관측. var · range · std (순수 spread, level-무관) 는 약함 (|d| 0.49~0.61) —
  즉 cascade 를 좌우하는 건 *순수 spread* 가 아니라 *전반적 상향 shift + 상위-tail*.

- **L5 (H274.3 부분 falsified — mean 도 강한 예측자)**: H274.3 은 adaptive base_gain
  이 mean 을 normalize-out 하여 mean 이 *약한* 예측자일 것으로 예측했다. 그러나
  mean |d|=1.53 으로 강함. 사유: adaptive base_gain 은 *control 의* max q_final 을
  pin 하나, 초기 tension *분포 자체의* mean 은 seed 간 자유롭게 변동 (calibration 은
  base_gain scalar 만 조정, tension 분포는 substrate 가 생성). 즉 control level
  pinning ≠ tension mean pinning — H274.3 의 전제가 부정확. 정직하게 기록.

- **L6 (cascade 의 boost-trigger 가 soft-threshold)**: cascade 는 q_prev>q_thr 의
  *연속* 비교에 의한 boost on/off 의 positive-feedback. 초기 분포가 동일 방향으로
  강해도, cascade 진입 *타이밍* (어느 step 에서 q 가 q_thr 를 처음 넘는가) 의
  미세 차이가 latch hysteresis 와 결합해 비선형 결과를 낳음 — L3 의 예외 seed 들이
  이 타이밍 민감성의 증거. 초기 *분포통계* 단독으로는 이 동역학적 타이밍을 완전
  포착 못함 (rank-sep 미달의 근본 원인).

- **L7 (단일 d=8, single coupling=0.20, single q_thr=0.3 cascade)**: cascade
  성공은 q_thr=0.3 coop 조건에서만 발생 (H_262 L4: partial quorum ~0.44 가
  0.3 위 / 0.5·0.7 아래). 예측자 분석은 이 단일 cascade 조건 한정 —
  dimension/coupling/q_thr scaling 의 예측자 robustness 미검증 (H_262/H_272 carry).

## 9. Cross-Links

- **target H (필수, 심층 대상)**:
  - **H_272** (`H_272_seed_robust_recalibration.md`): 직접 모태 — H_272 가 발견한
    under-drive 잔존 (coop cascade 5/10) 의 *예측자 규명*. H_272 의 L3 ("cascade
    성공이 substrate tension 구조의 seed-의존") 이 본 H 의 pre-register 근거. 본 H
    는 그 "구조" 를 8 예측자로 분해 — 상위-tail/mean 이 aggregate 예측자이나
    결정론적 분리는 미달 (소수 예외 seed).
  - **H_262** (`H_262_quorum_sensing.md`): cascade 의 origin — quorum-gate +
    bistable switch 의 substrate 정의. 본 H 의 coop cascade 동역학 (`_h262_up`) 은
    H_262 의 byte-level 재현.
  - **H_269** (`H_269_multiseed_robustness.md`): fragility 진단의 출발점 (verdict
    fragile → H_272 비대칭 분해 → H_274 예측자 규명).
- **방법론 sister**:
  - **H_238** (`H_238_verdict_landscape_meta_map.md`): verdict-of-verdicts — 본 H
    는 그 축에 *outcome-predictor* (분포통계 → cascade) 를 추가.
  - **H_239** (`H_239_alternative_phi_metric_cross_validation.md`): criterion-
    robustness sister.
- **mitosis machinery**: `tool/hexa_native/mitosis_hook_lib.hexa`
  (`cell_pool_init` · `mitosis_forward_tail`) — 초기 per-cell tension = mean(|hidden|)
  의 원천. `HEXAD/LIFE/lib/phi_native.hexa` 는 Φ proxy sister (본 cycle 미사용).
- **raw**: raw#12 (deterministic + ≥5 falsifier + ≥5 honest limit) · raw#9/10
  (honest impl) · raw#15 (no-hardcode) · raw#82 (post-hoc edit 금지 — strict
  criterion 유지, 결과 본 뒤 느슨화 안 함).
- **philosophy (CLAUDE.md)**: p7 NO PERPLEXITY VERDICT (단일 통계를 truth 로 취급
  안 함 — 8 예측자 + rank-sep 교차검정, Goodhart guard) · a_autonomy_over_hardcode
  (cascade 성공이 외부 강제 아닌 substrate 초기 분포에서 emerge).
- **lesson pointer**: PSCC §45/§49 (F-PERSONA-4 seed-fragile, §A2-trap noise-floor)
  — single-seed 신호의 cross-seed 무너짐 lesson 의 LIFE 적용 + *예측자 식별로
  fragility 분해* 의 확장.
- **state**: `HEXAD/LIFE/state/h274_cascade_seed_2026_05_25/{run_h274.hexa,
  result.json, det_xproc.txt, snapshots/}`.

## 10. Verdict

본 cycle (2026-05-25) — pre-register-frozen (예측자 후보 8종 + C1/C2/C3 사전 확정)
+ runnable harness 실행 (10 seed 별도-프로세스 sweep + H_261-leg stream 정렬 +
cross-process determinism + aggregation), $0 mac local hexa-only deterministic.

```
verdict_class: FALSIFIED  (1/3 criteria — ¬C1: large-effect 예측자 존재하나 perfect rank-separation 미달)
verdict_tier: 🟢 NUMERICAL  (10-seed cascade-outcome × 8 predictor group-separation, H_272 byte-aligned, separate processes, cross-process determinism)
evidence_summary:
  10-seed (0..9) cascade-success vs initial-tension-distribution predictor
  analysis (d=8, N=16 pool, H_272 adaptive base_gain, H_261-leg stream-aligned).
  cascade success: 5/10 [T,T,T,F,T,F,T,F,F,F]  (= H_272 byte-identical)
    predictor    succ-mean   fail-mean   |d|      rank-sep  higher-succ
    topk_mass    0.3948      0.3556      1.548    FALSE     TRUE
    mean         0.2936      0.2701      1.530    FALSE     TRUE
    n_above      5.000       3.200       1.480    FALSE     TRUE
    max          0.4545      0.4050      1.065    FALSE     TRUE
    std          0.0777      0.0686      0.610    FALSE     TRUE
    var          0.0063      0.0049      0.595    FALSE     TRUE
    range        0.3061      0.2713      0.488    FALSE     TRUE
    min          0.1484      0.1337      0.428    FALSE     TRUE
  BEST predictor: topk_mass (상위-4 tail mass) |d|=1.548, higher-in-success TRUE,
    perfect rank-sep FALSE (군 겹침)
criteria_met: 1/3 (C3 determinism ; ¬C1 결정론적 분리 미달 → ¬C2 cascade)
falsifiers: F1 SEPARATES FAIL · F2 INTERPRET FAIL · F3 NONTRIVIAL PASS
  · F4 GROUNDTRUTH PASS · F5 DETERMINISM PASS = 3/5
key_finding:
  cascade 성공은 초기 tension 분포로부터 *aggregate 로는 강하게 예측되나*,
  *결정론적으로는 분리 불가*. 4 예측자 (topk_mass |d|=1.55 · mean |d|=1.53 ·
  n_above |d|=1.48 · max |d|=1.07) 가 모두 large effect 로 success 군이 더 높음 —
  메커니즘 방향 정확히 일치 (상위-tail mass / 전반적 상향 shift ↑ → 많은 cell 이
  ON-latch 근처 → coupling boost 가 partial quorum 을 cascade). 즉 H_272 의
  under-drive 잔존은 "초기 분포가 충분히 위쪽으로 drive 되어 있는가" 라는 *해석
  가능한 메커니즘* 을 가진다. 그러나 *어느 통계도* perfect rank-separation 미달
  (군 겹침) — best 예측자 topk_mass 조차 양 극단 (하위 3 = 전부 fail seed 5/3/8,
  상위 3 = 전부 success seed 4/2/6) 은 깨끗하나 중간대 두 예외 (seed 7/9: 높은
  tail 인데 실패) 가 분리를 깬다. mean 예측자는 9/10 정렬 (seed 2 만 예외: 낮은
  mean 인데 성공). 사전 고정 C1 이 *결정론적* 예측자 (perfect rank-sep) 를 요구
  하므로 verdict 는 FALSIFIED — 단 이는 "예측력 부재" 가 아니라 "*결정론적*
  예측자 부재" 이며, cascade 가 초기 분포 + 동역학적 cascade-타이밍 (latch
  hysteresis × soft boost-trigger) 의 *상호작용* 임을 의미. 동일 seed cross-process
  byte-equal (C3 PASS, 5/5 falsifier 중 3 PASS).
honest_note:
  L2 carry — C1 의 perfect-rank-sep 이 strict bar; large-effect 단독이었다면 4
  예측자 PASS. raw#82 준수로 사전 criterion 유지 (느슨화 안 함). verdict 는
  "결정론적 예측자 부재" 이지 "예측력 부재" 아님.
  L3 carry critical — overlap 의 원인은 *중간대 소수 예외 seed* (topk: 7/9 高tail-fail;
  mean: 2 低mean-success); 양 극단은 깨끗. 즉 *대부분* 예측 가능 + soft-threshold
  cascade 타이밍이 소수 seed 에서 leading 예측자 뒤집음.
  L5 carry — H274.3 부분 falsified: adaptive base_gain 은 control level 만 pin,
  tension 분포 mean 자체는 seed 간 변동 → mean 도 강한 예측자 (|d|=1.53).
  L6 carry — rank-sep 미달의 근본 = boost-trigger 의 soft-threshold + latch
  hysteresis 가 초기 분포통계로 포착 안 되는 동역학적 타이밍 민감성 유발.
implication:
  H_272 의 under-drive 잔존 (coop cascade 5/10) 은 *예측 가능한 메커니즘* 을
  가진다 — 초기 tension 분포의 상위-tail mass / 전반적 상향 shift 가 success 군
  에서 일관 높음 (large effect, 메커니즘 방향 일치). 그러나 *결정론적* 단일-통계
  예측자는 부재 (모든 통계 군 겹침) — cascade 성공은 초기 분포의 *경향* 에 더해
  동역학적 cascade-타이밍 (latch hysteresis × soft boost-trigger) 의 상호작용
  이라, 초기 분포통계 단독으로는 소수 seed 에서 빗나간다. 다음 cycle 후보:
  (a) 초기 분포통계 + early-step q trajectory 의 *결합* 예측자 (동역학 타이밍
  포함), (b) boost-trigger 를 soft (sigmoid) 로 만들어 타이밍 민감성 완화 후
  rank-sep 회복 여부, (c) 더 많은 seed 로 중간대 예외 seed (7/9/2) 의 빈도 안정화.
  H_272 의 "substrate tension 구조 의존" 진단은 *방향* (상위-tail) 은 확정,
  *결정론* 은 부정으로 분해됨.
sibling: H_272 (seed-robust recalibration, under-drive 진단), H_262 (quorum-sensing,
         cascade origin), H_269 (multiseed-robustness, fragility 진단)
```

### Run verdict (VERBATIM — `hexa run` stdout 2026-05-25, agg mode)

```
================================================================
H_274 quorum-cascade seed-dependence — which initial-tension
       statistic predicts coop cascade success?
  base: H_262 quorum-gate · H_272 adaptive base_gain (verbatim)
  predictor source: coop cascade pool INITIAL per-cell tensions
  seeds: 0..9 (one process per seed)
================================================================
cascade success: 5/10  fail: 5/10
  per-seed success: [true, true, true, false, true, false, true, false, false, false]

predictor    succ-mean    fail-mean    |d|        rank-sep  higher-succ
---------    ---------    ---------    ---        --------  -----------
  mean   sm=0.293575  fm=0.270117  d=1.52953  rsep=false  hi-succ=true
  var   sm=0.0062744  fm=0.00492229  d=0.595348  rsep=false  hi-succ=true
  std   sm=0.077741  fm=0.0685526  d=0.610149  rsep=false  hi-succ=true
  max   sm=0.454494  fm=0.405035  d=1.06464  rsep=false  hi-succ=true
  min   sm=0.148367  fm=0.133745  d=0.428527  rsep=false  hi-succ=true
  range   sm=0.306128  fm=0.27129  d=0.48807  rsep=false  hi-succ=true
  topk_mass   sm=0.394842  fm=0.355567  d=1.54816  rsep=false  hi-succ=true
  n_above   sm=5.0  fm=3.2  d=1.47959  rsep=false  hi-succ=true

BEST predictor: topk_mass  (|d|=1.54816, rank-sep=false, higher-in-success=true)
  success-group mean=0.394842  fail-group mean=0.355567  Δ=0.0392746

C1 SEPARATES   (best |d|>=0.8 AND rank-sep)      : false
C2 INTERPRET   (upper-tail/spread, higher-succ)  : false
C3 DETERMINISM (same-seed cross-process)         : true

F1 SEPARATES    FAIL
F2 INTERPRET    FAIL
F3 NONTRIVIAL   PASS
F4 GROUNDTRUTH  PASS
F5 DETERMINISM  PASS
================================================================
VERDICT: FALSIFIED  (1/3 criteria, 3/5 falsifiers PASS)
================================================================
ledger -> HEXAD/LIFE/state/h274_cascade_seed_2026_05_25/result.json
```

**State output**: `state/h274_cascade_seed_2026_05_25/result.json` +
`det_xproc.txt` (cross-process determinism) + `snapshots/seed{0..9}.json`
(per-seed initial-tension distribution statistics + cascade outcome)
**Harness**: `state/h274_cascade_seed_2026_05_25/run_h274.hexa` (two-mode
seed/agg, H_261-leg stream-aligned to H_272, hexa-only aggregation, LLM none)
