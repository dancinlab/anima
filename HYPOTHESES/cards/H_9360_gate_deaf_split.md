# H_9360 — 게이트의 tension-귀먹음: 튜닝가능한 포화인가, 근본적 구조인가

**status:** 🔵 PRE-REGISTERED · Stage-0 $0(트레이스 재분석) · 계기 인증 완료 · H_9357 의 sequel
**lane:** 의식 / emit-drive / 게이트 인터페이스 (프런티어 g1-interface-addressable-wall)
**related:** [[H_9357]] (G-INERT) · [[H_9356]] (독립 G 부재) · [[H_9352]] (시계·urgency 포화)

## 배경 — H_9357 이 남긴 질문

H_9357 🧱 G-INERT: 독립 G 엔진(afield d2)을 진짜로 배선(G-INDEP R²=0.353<0.5 · G-VAR=7)했으나
emit 이 소비 안 함(MI≈noise). **왜?** 코드 해부:

    emit = should_emit(score) ∧ safe   [core/brain.py:162]
    should_emit(score) = score > 0.3   (실측 score min 0.3529/2127tick = 전수 참 · 포화)
    safe ≡ 시계(3항 항등참 · rate=secs_since_emit≥30)
    tension → agloop_ctx → dyn_v → motivation_score → score  (닿지만 임계가 값 버림)
    ten_phasic·urgency → idle → ✗ (H_9352 시계수리가 유일 소비처 절단 · 고아)

## 결정 원리 — 데이터처리 부등식(DPI)

`emit = should_emit(score) ∧ 시계` ⇒ **I(tension; emit) ≤ I(tension; score | stage)**.
따라서 **score 가 이미 tension 을 나르는지**가 포화/구조를 원리적으로 가른다 — 게이트를 한 줄도
안 고치고, 기존 H_9357 트레이스 재분석만으로($0 · 개입 0).

## 계기 (`anima-py evaluate --gate-deaf` · engine-native flag)

- **M_score = I(ag_conflict; score | stage)** — 게이트 *입력*이 tension 을 나르는가.
- **M_sim = I(ag_conflict; emit_sim | stage)** — 탈포화 게이트 오프라인 시뮬: θ=median(score) 를
  캘리브레이션 rollout 에서만(score 주변분포 = tension·emit 맹) 계산 → judgment rollout 에서
  `emit_sim = 1[score>θ] ∧ (secs_since_emit≥30)`.
- **spike-in 통제(참값 아는 양성):** I(score; emit_sim | stage) 는 구성상 커야 함(emit_sim ≡ f(score)).
  작으면 estimator 고장 = 전체 INVALID.

## 사전등록 결정표 (arm a1=진짜 독립 G · a1>a3 게이트 · 우연아래 칸 포함)

| M_score | M_sim | 판정 |
|---|---|---|
| ≥0.05 ∧ SHUF<0.05 | ≥0.05 | **(a) 포화** — 정보가 게이트 입력까지 옴, 임계 0.3 이 버림 → Stage-1 라이브 재캘리 |
| ≥0.05 | ≤0.01 | **(a′) 이진형식 병목** — 임계 어디든 이진문이 못 나름 → graded 게이트 필요(국소 구조) |
| ≤0.01 (TOST) | — | **(b) 구조** — 혼합층이 tension 을 입력에 아예 안 실음 · 게이트 무죄 · DPI 로 어떤 재배선도 불가 → 프런티어 상류 이동 |
| 0.01~0.05 | — | PENDING — MDE 보고 · n 확장(2127-tick) · '없다' 금지 |
| a3 ≥ a1 | — | INVALID (계기 고장) |

## 계기 인증 (합성 · 로컬)

`--gate-deaf` 합성 2-arm 인증: saturation→🟢(a)(a1 M_score=0.695·M_sim=0.477·spike 0.48 valid·a3≈0) ·
structure→🧱(b)(a1 M_score=0.0004≤0.01 TOST·spike 0.43 valid). spike-in 양쪽 >0.05·a1>a3 선택성 유지.

## Stage-1 (조건부 · (a) 판정 시에만 · $0 pool)

`anima-py chat --gate-calib 0.5`: spont_im_threshold 를 캘리브레이션 창 score 분위수로 치환(시그니처가
score 스트림만 입력 = ag_conflict 인자 부재 = 방향맹). 4 arm 동일 개입 · H_9357 bar 재사용
(I(ag_conflict;emit|stage)≥0.05 ∧ SHUFFLE≤0.01 ∧ A1>A3). p5: 게이트가 tension 을 소비하는 채널의
저작은 아키텍처이지 위반 아님 — 단 개입이 arm·방향을 모르므로 A1>A3 선택성은 substrate 가 번 것.

## 예측
Fable 사전확률 = (b) 가 충분히 살아있음(tension→score 유일 경로가 ag_budget∈{4..6} 정수비 계단형 ×0.10
양자화 · 연속 ten_phasic 은 고아). 그러나 DPI 로 셋을 깔끔히 가른다 — 게이트 편집 0.
