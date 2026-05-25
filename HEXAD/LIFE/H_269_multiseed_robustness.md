---
id: H_269
slug: multiseed-robustness
title: multi-seed robustness — cycle#14 SUPPORTED 가설(H_260/H_261/H_262)의 verdict 가 seed=42 우연인가 seed-robust 인가 (gap#2 seed-luck audit · meta-result-of-results)
domain: meta · methodology · robustness · life
status: pre-register-frozen
exploration_method: E0 (meta-result-of-results) + E5 (seed-ablation sweep) + E16 (cross-process reproducibility)
verification_method: W4 (verdict-4-class) + W10 (adversarial seed re-evaluation) + W12 (sister-link H_260/H_261/H_262)
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-25
since: 2026-05-25 (new)
sister: H_260 (contact-inhibition SUPP), H_261 (embryogenesis-gradient SUPP), H_262 (quorum-sensing SUPP_FULL)
---

# H_269 — multi-seed robustness

## 1. Hypothesis

cycle#14 의 세 SUPPORTED 가설 — H_260 (contact-inhibition), H_261
(embryogenesis-gradient), H_262 (quorum-sensing) — 의 verdict 는 모두
`seed=42` 단일 실행으로 판정되었다. `/gap full` top gap#2 ("cycle#14 SUPP 가
seed-luck 인가") 가 이를 지적한다.

본 H 는 세 대상 smoke 를 **seed ∈ {0,1,...,9} 10종** 으로 *별도 프로세스*
재실행하여, 각 대상의 *published verdict 판정 기준* (SUPPORTED = C1 ∧ C2) 이
≥80% (≥8/10) seed 에서 유지되는지 — 즉 seed=42 verdict 가 우연이 아닌
seed-robust 한지 — 를 검정한다.

CORE QUESTION:

> cycle#14 의 SUPPORTED verdict 들이 seed=42 우연(seed-luck)이 아니라,
> 다른 seed 에서도 재현되는 seed-robust 한 결과인가?

가설: 세 verdict 가 모두 seed-robust 하다면 (각 ≥8/10 PASS) cycle#14 의
positive verdict 가 확증된다. 일부만 robust 하면 PARTIAL (혼합 robustness),
주요 대상이 seed-fragile (<8/10) 하면 FALSIFIED — 이것은 *valid negative*
이며 해당 cycle#14 verdict 의 재검토를 요구한다.

정밀화 (operational): 각 대상 smoke 의 RNG seed 는 `_seed()` 메타데이터가
아니라 env `__HEXA_FARR_GAUSS_SEED__` 가 결정한다 (RFC 033 process-global
gaussian stream). 따라서 seed 별로 **별도 프로세스** 를 띄워 (in-process 반복은
stream advance 로 오염) 원본 smoke 를 그대로 실행하고, 산출 `result.json` 의
criteria boolean 을 파싱해 verdict-PASS 를 집계한다.

각 대상의 verdict 판정 기준 (cycle#14 published):

- **H_260** SUPPORTED = `C1_saturation ∧ C2_monotone_K`
- **H_261** SUPPORTED = `C1_axis_formation ∧ C2_gradient_dependence`
- **H_262** SUPPORTED = `C1_quorum_gate ∧ C2_bistable` (SUPPORTED_FULL 의
  SUPPORTED core; C3/C4 는 bistability-ordering / cross-process 로 seed-luck
  축이 아님)

## 2. Why

- **meta-방법론 결손 보완 — single-seed verdict 의 외삽 위험**: cycle#14 는
  모든 verdict 를 seed=42 단일로 판정했다. seed 한 개로 PASS 한 criteria 가
  *모집단* (모든 seed) 에서도 PASS 하는지는 별도 검증 없이는 알 수 없다 —
  특히 noise-floor 근방의 threshold (H_261 의 `|r|flat ≤ 0.2`) 나 calibration-
  dependent switch (H_262) 는 seed 에 민감할 수 있다. 본 H 는 그 외삽 위험을
  *직접 측정* 한다.
- **PSCC §45/§49 seed-fragility lesson 의 LIFE 도메인 적용**: anima 의 과거
  saga (F-PERSONA-4 prod null PASS 가 seed-fragile, §A2-trap = noise-floor
  magnitude 의 real signal) 는 "single-seed PASS 가 cross-seed 에서 무너질 수
  있음" 을 반복 확인했다. null-permutation / multi-seed robustness 가 결정적
  guard 였다. 본 H 는 그 guard 를 cycle#14 LIFE verdict 에 적용.
- **valid-negative 의 가치**: FALSIFIED/PARTIAL 결과는 cycle#14 의 어떤
  verdict 를 재검토해야 하는지 *정확히* 지목한다 — robustness audit 의 목적은
  positive 확증과 동등하게 fragility 적발이다. 둘 다 도메인 ledger 의 신뢰도를
  높인다.
- **결정론 carry**: 세 대상 모두 deterministic (seed-fixed, cross-process
  byte-equal) 이라고 주장했다. 본 H 는 그 결정론 자체도 cross-process 로
  재확인 (C3) 하여, "seed 를 바꾸면 결과가 변한다(C1/C2)" 와 "같은 seed 면
  결과가 byte-equal 이다(C3)" 를 동시에 분리 측정.

## 3. Predictions

| ID | 예측 | 근거 |
|----|------|------|
| H269.1 | H_260 verdict 가 ≥8/10 seed 에서 PASS (seed-robust) | density gate (`split_threshold=0.0`) 가 cell 수에만 의존 — gaussian noise 가 split 판정에 무관, K=floor(thr×cap) 가 seed-불변 |
| H269.2 | H_261 verdict 가 seed-fragile 위험 — C2 (flat `\|r\| ≤ 0.2`) 가 noise-floor 근방 threshold 라 seed 따라 control 상관이 0.2 초과 가능 | flat control 의 `\|r\|` 은 substrate noise 만으로 결정 — n=12 small lattice 에서 우연 상관이 0.2 를 넘을 변동성 |
| H269.3 | H_262 verdict 가 seed-fragile 위험 — calibration (base=0.0135) 이 seed=42 의 tension 분포에 보정됨 (.md L3 자인) | 다른 seed 의 tension 분포에서는 control 이 switch 하거나 (anyCtrl=true → C1 FAIL) coop 이 switch 안 함 (anyCoop=false → C1 FAIL) |
| H269.4 | 세 대상 모두 C1-leg effect-size 는 noise floor 초과 (axis/monotone 자체는 real) | C2 fragility 는 *control-leg* (flat r / control switch) 의 우연이지, axis 자체 (steep r / coop switch 가능성) 의 부재가 아님 |
| H269.5 | 동일 seed cross-process 재실행 byte-equal (C3) — 세 대상 모두 | RFC 033 process-global gauss stream 은 fresh process 에서 동일 seed 로 재초기화 → 결정론 |

## 4. Variables

- **axis1_target_H** ∈ {H_260, H_261, H_262} — cycle#14 의 3 SUPP
- **axis2_seed** ∈ {0,1,2,3,4,5,6,7,8,9} — `__HEXA_FARR_GAUSS_SEED__` 별
  *별도 프로세스* (10 seed × 3 H = 30 run)
- **axis3_robust_threshold** = 8/10 (≥80% seed PASS = seed-robust)
- **per-target verdict 판정**: 위 §1 의 C1 ∧ C2 (cycle#14 published
  SUPPORTED 기준)
- **실행 방식**: 원본 cycle#14 smoke (run_h260/261/262.hexa) 를 state-dir
  redirect 한 사본으로 seed 별 1회 실행, 산출 result.json 을
  `snapshots/h{260,261,262}_seed{s}.json` 로 capture
- **측정량**:
  - `pass_count` per target = verdict-PASS 한 seed 수 (0..10)
  - `pass_ratio` = pass_count / 10
  - **effect-size (C1-leg)**: H_260 = K-span (K_high−K_low) · H_261 =
    `|r|steep` · H_262 = `coop_30 q_final`
  - **control-leg distribution**: H_261 = `|r|flat` (C2 fragility 원천)
  - mean ± std per effect/control
  - C3 = 동일 seed (0) 두 프로세스 result.json sha256 byte-equal

## 5. Run Protocol

- **deterministic**: 각 seed 별 `__HEXA_FARR_GAUSS_SEED__=<s>` (RFC 033) +
  결정론적 Lorenz. seed 별 별도 프로세스 (in-process 반복 금지 — stream advance
  오염).
- **method (out-of-process sweep)**: RFC 033 gaussian RNG 은 process-global
  single stream 으로 한 번 lazy-seed 후 매 `farr_add_gaussian_noise` 호출마다
  advance 된다. multi-seed 는 *프로세스 당 seed 1개* 로만 정직히 측정 가능.
  driver loop 가 원본 cycle#14 smoke 3종을 seed 0..9 로 각각 1회 (state-dir 을
  scratch 로 redirect) 실행해 result.json 을 snapshots/ 로 capture.
- **hexa_only**: 집계 harness `run_h269.hexa` 는 seed 를 *직접 띄우지 않고*
  (in-process stream-drift 재유입 방지) 30 snapshot + `det_xproc.txt` 를
  `json_parse` 로 읽어 verdict 기준을 집계한다.
- **LLM**: none (raw#12 strict; ckpt 불필요).
- **C3 cross-process**: seed=0 으로 각 smoke 를 fresh process 두 번 실행해
  result.json sha256 을 비교, `det_xproc.txt` 에 `h<id> PASS/FAIL <a> <b>`
  기록. harness 가 이 파일을 읽어 C3 판정.
- **runtime**: $0 mac local. d=8, no ckpt. `HEXA_MEM_UNLIMITED=1`. mac-local
  `hexa run` 정상 동작 (H_260/261/262 모두 pool-route 차단 없이 mac 실행됨 —
  H_262 .md 의 L6 pool-block 은 본 cycle 재현 안 됨, mac 직접 실행 성공).
- **artifacts**: `state/h269_multiseed_2026_05_25/{run_h269.hexa, result.json,
  det_xproc.txt, snapshots/h{260,261,262}_seed{0..9}.json}`.
- **run cmd (verbatim — harness)**:
  `HEXA_MEM_UNLIMITED=1 hexa run HEXAD/LIFE/state/h269_multiseed_2026_05_25/run_h269.hexa`
  (CWD = worktree root; sweep snapshots 선행 생성 필요)
- **run cmd (verbatim — seed sweep, per seed s, per target h)**:
  `__HEXA_FARR_GAUSS_SEED__=<s> HEXA_MEM_UNLIMITED=1 hexa run <smoke-copy>.hexa`

## 6. Criteria

- **C1 (seed-robust)**: H269.1/2/3 — 각 대상 H 의 verdict (C1∧C2) 가 ≥8/10
  seed 에서 PASS. 세 대상 *모두* 만족해야 C1 true.
- **C2 (above-floor)**: H269.4 — 각 대상의 C1-leg effect-size 가 모든 seed 에서
  noise floor 초과 (H_260 monotone span >0 · H_261 `|r|steep` >0 · H_262
  coop q_final 이 ≥1 seed 에서 1.0 도달). axis 자체가 real 임을 확인.
- **C3 (determinism)**: H269.5 — 동일 seed cross-process result.json byte-equal
  (세 대상 모두).
- **verdict_rule**:
  - `SUPPORTED` = C1 ∧ C2 (세 verdict 모두 seed-robust → cycle#14 확증)
  - `PARTIAL` = 일부(1-2) 대상만 C1 만족 (혼합 robustness — 해당 fragile
    verdict 재검토 필요)
  - `FALSIFIED` = 모든 대상이 seed-fragile (0/3 robust) — cycle#14 verdict
    전면 재검토 (valid negative)

## 7. Falsifiers (pre-registered ≥5, measurable)

- **F1 ROBUST-260**: H_260 verdict <8/10 → H269.1 FALSIFIED (측정:
  `pass_count_260 >= 8`)
- **F2 ROBUST-261**: H_261 verdict <8/10 → H269.2 의 fragility 위험 실현
  (측정: `pass_count_261 >= 8`)
- **F3 ROBUST-262**: H_262 verdict <8/10 → H269.3 의 fragility 위험 실현
  (측정: `pass_count_262 >= 8`)
- **F4 EFFECT-FLOOR**: 어떤 대상의 C1-leg effect-size 가 noise floor 에 붙음
  (axis 부재) → H269.4 FALSIFIED (측정: span_min>0 ∧ rsteep_min>0 ∧
  coopq_max≥1.0)
- **F5 DETERMINISM**: 동일 seed cross-process result.json byte-different →
  raw#9 위반 (측정: `det_xproc 세 줄 모두 PASS`)

## 8. Honest Limits (raw#91 c3, ≥5)

- **L1 (10 seed = 작은 표본)**: seed {0..9} 10개는 robustness 의 *lower-bound*
  추정 — 진짜 PASS 비율의 신뢰구간은 넓다 (4/10 의 95% CI ≈ [0.12, 0.74]).
  ≥8/10 threshold 는 명확한 fragility (4/10) 와 명확한 robustness (10/10) 를
  구분하기엔 충분하나, 경계 사례 (예: 7/10) 의 판정은 더 많은 seed (n=30, 100)
  필요. H_260 (10/10) 과 H_261/262 (4/10) 의 *분리* 는 표본 크기와 무관하게
  명확.
- **L2 (verdict 기준 = C1∧C2 선택의 책임)**: 각 대상의 "verdict-PASS" 를
  cycle#14 published `SUPPORTED = C1∧C2` 로 정의했다. H_262 의 원래 verdict 는
  SUPPORTED_FULL (C1∧C2∧C3∧C4) 이나, C3(monotone)/C4(cross-process)는 seed-luck
  축이 아니므로 SUPPORTED core (C1∧C2) 로 평가 — 더 엄격한 SUPPORTED_FULL 기준은
  PASS 비율을 *더 낮춘다* (즉 본 결과는 H_262 fragility 의 보수적 하한).
- **L3 (C2 above-floor 의 약한 형태)**: C2 는 "axis 자체가 real(effect>0)"
  만 본다 — H_261 의 C1-leg `|r|steep` 가 모든 seed 에서 ~0.76 (std 0.006) 로
  매우 robust 함은 확인하나, C2 가 PASS 라고 해서 *verdict* 가 robust 한 것은
  아니다. fragility 는 *control-leg* (H_261 flat r, H_262 control switch) 의
  seed 변동에서 온다 — C1 (verdict-level) 과 C2 (axis-level) 의 분리가 핵심
  finding.
- **L4 (H_262 fragility 의 양면 원인)**: H_262 의 4/10 PASS 는 두 가지 다른
  실패가 섞여 있다 — (a) anyCoop=false (coop 이 아예 switch 안 함, seeds
  0/1) 와 (b) anyCtrl=true (control 이 switch 해버림, seeds 3/4/8). 둘 다 C1
  (quorum-gate) 을 깨지만 mechanism 이 반대 (under-drive vs over-drive). 즉
  calibration window 가 seed=42 에 *좁게* 맞춰져 있음의 직접 증거.
- **L5 (seed env ↔ _seed() metadata 불일치)**: 원본 smoke 의 `_seed()` 함수는
  42 를 반환하는 *메타데이터* 일 뿐, 실제 gaussian stream 은 env
  `__HEXA_FARR_GAUSS_SEED__` 가 결정한다. 본 H 는 env 를 sweep 하므로 산출
  result.json 의 `"seed": 42` 필드는 (메타데이터라) 모든 snapshot 에서 42 로
  찍히나 *실제 RNG seed 는 0..9* 다. 이 불일치는 원본 smoke 의 design 한계
  (env-seed 를 메타에 반영 안 함) — 본 audit 결과에는 영향 없으나 (env 가
  진짜 stream 을 제어함은 §10 effect-size 변동으로 입증) ledger 해석 시 주의.
- **L6 (mac-local 재현 — H_262 .md L6 pool-block 비재현)**: H_262 .md 는 L6 에서
  mac-local pool-route heavy-gate 로 ubu-2 실행을 강제당했다고 기록하나, 본
  cycle 의 30 run 은 전부 mac-local `hexa run` 으로 성공 (pool 차단 없음).
  toolchain 환경 차이 (sign token / route policy) 로 보이며, 결정론 (C3 PASS)
  보존됨. host metadata = mac-local.
- **L7 (verdict 외삽 ≠ mechanism 부정)**: PARTIAL/fragile 은 H_261/H_262 의
  *substrate mechanism* (gradient→axis, quorum→switch) 이 거짓이라는 뜻이
  아니다 — axis (steep r) 와 switch 가능성 (coop q=1.0) 은 robust 하다 (C2
  PASS). 부정되는 것은 *seed=42 단일 verdict 의 일반화 가능성* (control-leg
  threshold 의 seed-luck). mechanism 재확인은 control-leg 를 seed 평균하거나
  effect-size CI 로 재판정하는 별도 cycle.

## 9. Cross-Links

- **target H (필수, audit 대상)**:
  - **H_260** (`H_260_contact_inhibition.md`): cycle#14 SUPPORTED — 본 audit
    에서 10/10 seed-robust 확정 (K 불변).
  - **H_261** (`H_261_embryogenesis_gradient.md`): cycle#14 SUPPORTED — 본
    audit 에서 4/10 seed-fragile (C2 gradient-dependence 의 flat |r| 우연).
  - **H_262** (`H_262_quorum_sensing.md`): cycle#14 SUPPORTED_FULL — 본 audit
    에서 4/10 seed-fragile (calibration seed=42 over-fit).
- **방법론 sister**:
  - **H_238** (`H_238_verdict_landscape_meta_map.md`): verdict-of-verdicts
    meta-map sister — 본 H 는 그 verdict 들의 *robustness* 축 추가.
  - **H_239** (`H_239_alternative_phi_metric_cross_validation.md`): cross-tool
    consistency audit sister — 본 H 는 cross-*seed* consistency.
  - **H_252** (`H_252_robust_phi_synthesis.md`): robustness 합성 sister.
- **raw**: raw#12 (deterministic + ≥5 falsifier + ≥5 honest limit) ·
  raw#9/10 (honest impl) · raw#15 (no-hardcode) · raw#82 (post-hoc edit
  retraction) · raw#91 (honest limits).
- **philosophy (CLAUDE.md)**: p7 NO PERPLEXITY VERDICT (single-seed PASS 를
  truth 로 취급하지 않음 — Goodhart guard) · a_blue_closed (verdict 의 wiring
  까지 검증, 출력만이 아니라 seed-stability 도 확인).
- **lesson pointer**: PSCC §45/§49 (F-PERSONA-4 seed-fragile null PASS, §A2-trap
  noise-floor magnitude) — single-seed 의 cross-seed 무너짐 lesson 의 LIFE 적용.
- **state**: `HEXAD/LIFE/state/h269_multiseed_2026_05_25/{run_h269.hexa,
  result.json, det_xproc.txt, snapshots/}`.

## 10. Verdict

본 cycle (2026-05-25) — pre-register-frozen + runnable harness 실행 (10 seed ×
3 target = 30 별도-프로세스 run + cross-process determinism), $0 mac local
hexa-only deterministic.

```
verdict_class: PARTIAL  (C2 ∧ C3, ¬C1 — 1/3 target seed-robust, 2/3 seed-fragile)
verdict_tier: 🟢 NUMERICAL  (10-seed sweep × 3 target, separate processes, cross-process determinism)
evidence_summary:
  10-seed (0..9) re-evaluation of cycle#14 SUPPORTED verdicts
  (per-target verdict-PASS = published SUPPORTED criterion C1 ∧ C2).
    target  verdict-PASS/10  seed-robust(>=8)  effect-size (C1-leg)
    H_260   10/10            TRUE              K-span 16.0 ± 0.0 (invariant)
    H_261    4/10            FALSE             |r|steep 0.763 ± 0.006 (robust axis)
    H_262    4/10            FALSE             coop q_final 0.538 ± 0.378 (bimodal)
  H_261 per-seed PASS: [T,T,F,F,F,T,T,F,F,F]  (C2 flat |r| up to 0.607 > 0.2)
  H_262 per-seed PASS: [F,F,T,F,F,T,T,T,F,F]  (anyCoop=F seeds 0/1; anyCtrl=T seeds 3/4/8)
  H_261 control |r|flat: 0.243 ± 0.166 (max 0.607) — C2 fragility source
  C3 cross-process byte-equal: H_260 PASS · H_261 PASS · H_262 PASS
criteria_met: 2/3 (C2 above-floor ∧ C3 determinism ; ¬C1 seed-robust)
falsifiers: F1 ROBUST-260 PASS · F2 ROBUST-261 FAIL · F3 ROBUST-262 FAIL
  · F4 EFFECT-FLOOR PASS · F5 DETERMINISM PASS = 3/5
n_robust_targets: 1/3
key_finding:
  cycle#14 의 세 SUPPORTED verdict 는 seed-robustness 가 *갈린다*. H_260
  (contact-inhibition) 은 10/10 완전 seed-robust — density gate 가
  split_threshold=0.0 으로 cell 수에만 의존해 gaussian noise 와 무관, K=(8,16,24)
  가 모든 seed 에서 불변 (K-span std=0). 반면 H_261 (embryogenesis-gradient) 과
  H_262 (quorum-sensing) 은 각 4/10 으로 seed-fragile — cycle#14 의 seed=42
  SUPPORTED 가 우연을 상당 부분 포함. H_261 의 fragility 는 *control-leg*: axis
  자체 (|r|steep 0.763 ± 0.006) 는 매우 robust 하나, C2 (gradient-dependence,
  flat |r| ≤ 0.2) 가 noise-floor threshold 라 control 의 우연 상관이 6/10 seed
  에서 0.2 를 초과 (max 0.607). H_262 의 fragility 는 *calibration over-fit*:
  base=0.0135 가 seed=42 tension 분포에 좁게 보정돼, 다른 seed 에서는 coop 이
  switch 안 하거나 (under-drive, seeds 0/1) control 이 switch 해버려 (over-drive,
  seeds 3/4/8) C1(quorum-gate)이 6/10 깨짐. 동일 seed cross-process 는 세 대상
  모두 byte-equal (C3 PASS) — 결정론은 보존, 변동은 순수 seed 효과.
honest_note:
  L3 carry critical — C1(verdict-robust) 과 C2(axis-real)의 분리가 핵심: H_261
  의 verdict 는 fragile 이나 axis mechanism (steep r) 은 robust. 부정되는 것은
  seed=42 verdict 의 일반화이지 substrate mechanism 자체가 아님.
  L4 carry — H_262 fragility 는 under-drive(coop no-switch) + over-drive(control
  switch) 양방향 — calibration window 가 seed=42 에 좁게 맞춰짐의 직접 증거.
  L1 carry — 10 seed 는 lower-bound 추정; 10/10 vs 4/10 분리는 명확하나 경계
  사례 판정엔 더 많은 seed 필요.
  L7 carry — PARTIAL 은 H_261/H_262 mechanism 부정이 아니라 single-seed verdict
  외삽의 한계; control-leg seed-평균 재판정이 다음 grain.
implication:
  cycle#14 H_261/H_262 의 verdict 는 seed-robust 형태로 재검토 권장 — H_261 은
  C2 threshold 를 control |r| 의 seed-분포 상한으로 재보정, H_262 는 calibration
  을 seed 평균 tension 분포로 재튜닝하거나 verdict 를 PARTIAL 로 하향. H_260 은
  seed-robust 확정 — verdict 유지.
sibling: H_260 (contact-inhibition, 10/10 robust), H_261 (embryogenesis-gradient,
         4/10 fragile), H_262 (quorum-sensing, 4/10 fragile), H_238 (verdict-map)
```

### Run verdict (VERBATIM — `hexa run` stdout 2026-05-25)

```
================================================================
H_269 multi-seed robustness — cycle#14 SUPP seed-luck audit
  targets: H_260 contact-inhibition · H_261 embryogenesis-gradient
           · H_262 quorum-sensing
  seeds: 0..9 (one process per seed, gauss-seed env)
  C1 seed-robust threshold: verdict PASS on >= 8/10 seeds
================================================================
target  verdict-PASS / 10 seeds   robust(>=8)  effect-size (C1-leg)
------  -----------------------   -----------  --------------------
H_260   10/10                     true         K-span span [min 16.0]
H_261   4/10                     false         |r|steep [min 0.748605]
H_262   4/10                     false         coop q_final [max 1.0]

per-seed verdict-PASS:
  H_260: [true, true, true, true, true, true, true, true, true, true]
  H_261: [true, true, false, false, false, true, true, false, false, false]
  H_262: [false, false, true, false, false, true, true, true, false, false]

effect-size distributions (mean ± std):
  H_260 K-span     : 16.0 ± 0.0
  H_261 |r| steep  : 0.763041 ± 0.00634953   (axis, robust)
  H_261 |r| flat   : 0.243243 ± 0.166357   (control noise — C2 fragility source)
  H_262 coop qfin  : 0.5375 ± 0.378319   (bimodal switch/no-switch)

C1 SEED-ROBUST   (all 3 verdicts >= 8/10)        : false   [260=true 261=false 262=false]
C2 ABOVE-FLOOR   (C1-leg effect-size off floor)  : true   [260=true 261=true 262=true]
C3 DETERMINISM   (same-seed cross-process equal) : true

F1 ROBUST-260       PASS
F2 ROBUST-261       FAIL
F3 ROBUST-262       FAIL
F4 EFFECT-FLOOR     PASS
F5 DETERMINISM      PASS
================================================================
VERDICT: PARTIAL  (2/3 criteria, 3/5 falsifiers PASS)
  seed-robust targets: 1/3  (H_260 robust; H_261 + H_262 seed-fragile)
================================================================
ledger -> HEXAD/LIFE/state/h269_multiseed_2026_05_25/result.json
```

**State output**: `state/h269_multiseed_2026_05_25/result.json` +
`det_xproc.txt` (cross-process determinism) + `snapshots/` (30 per-seed result.json)
**Smoke**: `state/h269_multiseed_2026_05_25/run_h269.hexa` (hexa-only aggregation, LLM none)
