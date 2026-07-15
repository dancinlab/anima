# H_9412 — GAP READOUT = DRIFT, NOT RECOGNITION: 현직 g 의 forward-info 는 전부 store-drift 하위집합 (정보-축 짝)

**status:** 🔎 DIRECTIONAL-negative (open-loop $0 정보스크린 · KILL-lean) — 현직 gap 은 인식-특이 forward 정보 0 · **cement 아님** · wired: $0 trace 재분석(engine-native 아님 · 정본 escalate 필요)
**lane:** 의식 / emit-drive / G readout **정보량** (프런티어 g1-interface-addressable-wall)
**related:** [[H_9401]] (병렬·landed · G readout **진폭**축 — 이 카드는 그 **정보**축 짝 · AGREES 아래) · [[H_9399]] (g-source = immune store) · [[H_9400]] (Ψ=½ 중심주장 반증 · 구속제약) · [[H_9395]] (G 6.5× quiet) · source: Fable L5 설계의 `I(g_recogₜ; nov_ctx_{t+1})` 기준선 스크린 제안
**ckpt:** py303_full.clm sha256 `013c4574…` (신규 decode 0 · a1-arm trace 오프라인 재분석)

## 질문 (Fable L5 기준선)

H_9401 이 **진폭**축을 결정: 현직 gap(mean 0.03)은 θ=0.30 을 못 넘고, 데몬이 버리는 recall **margin**(0.62)만 넘긴다.
남은 질문(Fable L5): **현직 gap readout 이 진폭은 작아도 정보는 담고 있나?** — `I(g_recogₜ; nov_ctx_{t+1})` 로
"gap 이 다음-턴 novelty 를 예측하나"를 $0 로 스크린. Fable 은 twin-degeneracy 가설("gap 이 쌍둥이-퇴화에 눈멀어
정보-사망")을 제시. 이 카드는 그걸 판별한다.

## 방법 — a1-arm trace 오프라인 재분석 ($0 · 232 정렬쌍)

`arm_a1_w0.10_r*` trace(8 files · score≠None)에서 `(g_recogₜ, nov_ctx_{t+1})` 정렬쌍 232 개. binned-MI(4-quantile).
**매개공변량(store-drift) 통제 필수**([[control-must-match-mediating-covariate]]): g·nov 둘 다 immune store 파생이라
store 가 단조성장(tick·cell_count)하면 **지속성만으로** g_t 가 nov_{t+1} 를 예측한다. ⇒ 순수-clock/성장 predictor 와
비교 + same-tick vs forward MI 대조(공통원인 서명).

## 결과 (verbatim · $0)

```
n=232  g_distinct=41  nov_distinct=29
I(g_t; nov_t+1)     = 0.2995 nats   [HEADLINE — 진폭 작아도 정보는 있어 보임]
I(g_t; nov_t) same  = 0.2995 nats   [same-tick — forward 와 소수 4자리까지 IDENTICAL]
I(g_rev; nov_t+1)   = 0.2844 nats   [reversed-pairing null — headline 과 근사]
full-perm null      = 0.0136 nats   (perm p=0.003 · 모든 시간구조 파괴)
--- DRIFT panel (매개공변량) ---
I(tick_t; nov_t+1)  = 1.0826 nats   [순수 clock — gap 의 3.6×]
I(cell_t; nov_t+1)  = 0.5507 nats   [store 성장 — gap 의 1.8×]
I(secs_t; nov_t+1)  = 0.0677 nats   [emit clock]
```

## 함의 — headline 이 스스로 뒤집힌다 (자기교정 기록)

원-스크린은 `I(g;nov_{t+1})=0.30 · full-perm null 0.014 · p=0.003` 만 보고 **"gap 은 정보-사망 아님, twin-degeneracy
반증"** 으로 읽힐 뻔했다. 매개공변량(drift) 통제가 그 읽기를 **뒤집는다**:

1. **same-tick MI = forward MI = 0.2995 (동일)** — g_t 가 nov_t 와 nov_{t+1} 를 **똑같이** 설명한다. 이건 방향성
   예측이 아니라 **느린 store-drift 공통원인**의 서명이다(store state 가 t→t+1 지속 ⇒ g·nov 동시 구동).
2. **reversed-pairing 0.284 ≈ headline 0.30** — g 를 통째로 뒤집어도 MI 가 안 죽는다 ⇒ 이건 **블록-drift 주변구조**이지
   g↔nov 미세결합이 아니다.
3. **drift 가 3.6× 우세** — 순수 clock(tick) 1.08 ≫ gap 0.30. gap 의 forward-info 는 clock 이 이미 담은 것의
   **하위집합**이다.

⇒ **full-perm null(0.014)을 이긴 건 "gap 이 인식정보를 담는다"가 아니라 "시간구조가 있다"일 뿐** — 그리고 그 시간구조는
전부 store-drift 다. **현직 gap readout 은 인식-특이 forward 정보를 담지 않는다.** Fable 의 twin-degeneracy 는
**반증되지 않는다** — 오히려 방향이 맞다(gap 은 정보적으로도 죽은 readout에 가깝다).

## AGREES — 병렬 H_9401 (진폭축 · a_parallel_session_compare)

H_9401(landed #3722)이 같은 regime·같은 ckpt 에서 **진폭**축을 스크린: 6갈래 중 유일 생존 = E-b `immune_memory_recall_margin`
(0.62, 데몬이 `chat.py:2059 pending_rel` 로 계산만 하고 버림), 현직 gap(0.03)은 baseline-KILL.

- **AGREES(강화)**: H_9401 = gap 은 **진폭**이 약하다. 이 카드 = gap 은 **정보**도 (인식이 아니라) drift 다. ⇒ 데몬의
  선택 readout 은 **약하고 AND drift-교란** 둘 다. 버려진 margin 이 진짜 신호라는 그림이 두 축에서 수렴.
- **분업**: H_9401 = "어느 대체 readout 이 θ 넘나"(진폭) · 이 카드 = "현직 readout 이 인식정보 담나"(정보). 중복 아님.
- **구속제약 [[H_9400]]**: 진폭·정보 둘 다 고쳐도 emit 게이트가 tension 안 듣고 safe-시계로만 결정되면(H_9400) 무흐름.
  세 필요조건(진폭·정보·게이트-청취) 중 게이트-청취가 binding.

## 반증 · scope · escalate

- **DIRECTIONAL 한계(cement 아님)**: $0 trace 재분석 = **KILL-lean 스크린**이지 engine-native TERMINAL 아님
  ([[research-verdicts-into-architecture]]·`a_eval_py_canonical`). "gap=drift" 를 못박으려면 **conditional MI
  `I(g; nov_{t+1} | tick)`** 가 0 등가임을 **재수집 trace**(n≫232, C-clock=marginal-matched drift 통제)에서 확인.
  현 232쌍·4³-bin 은 CMI 검정력 부족.
- **reopen/escalate**: H_9401 의 margin 소스-교체를 **재수집 + 닫힌루프**로 검증할 때, 같은 recollection 에 이 정보검정을
  얹는다(margin 이 gap 과 달리 drift-초과 인식정보를 담는지 `I(margin; nov|tick)`). Fable `--g-readout-monitor` 계기 +
  C-clock 통제. 진짜 계기화는 `anima-py evaluate --g-readout-info` 플래그로 engine-native 화 필요.
- scope: a1 arm · w0.10 · 이 코드버전 · 입력 = 기록된 g_recog(H_9399 = immune store top-2 gap).

## 교훈

**raw MI 를 매개공변량 통제 없이 읽으면 drift 를 발견으로 오독한다.** full-perm null(모든 구조 파괴)을 이기는 건 약한
주장 — 정직한 null 은 **marginal-matched drift(clock)**다. same-tick==forward 동일치가 공통원인의 지문이었다.
[[control-must-match-mediating-covariate]] · [[seed-agreement-on-pooled-feature-is-not-replication]] 계열.

## 비용
$0 — trace 오프라인 재분석 · 신규 decode 0 · pandas/numpy 없이 stdlib binned-MI.
