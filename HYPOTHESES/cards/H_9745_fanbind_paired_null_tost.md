# H_9745 — R2b fan-bind 계기 정렬: bind_delta paired 순열 null + prereg TOST

**status:** 🔵 PROPOSED (H_9694 reconcile 후속 · lab full Fable+Sol 수렴 · 계기 정렬결함) · not-terminal · 선행 [[H_9693]]·[[H_9694]]
**lane:** G6/ρ·fan · 계기 수리 **related:** [[H_9694]] · [[instrument-claim-alignment-before-reading-a-bar]] · [[chance-level-must-be-derived-per-metric]]

## 물음
H_9694 reconcile 가 드러낸 **계기 정렬결함**: `--fan-bind` 의 사전등록 절2(`composed J > mismatched-null p95`)는 **composition 이 아니라 emission** 을 잰다(짝 전파괴 shuf arm 이 composed J 최고값 0.0521 = kill#6 재발). composition 을 격리하는 유일 지표 **bind_delta = (Jc−Js)** 는 `eval_fan_bind` 에서 **자기 null pedestal 이 없다**(null 은 composed 방출을 다른 프레임 짝에 채점한 marginal J). ⟹ paired 차분을 marginal null 로 재판 = 범주오류 = KILL 제조.

## 조작 (engine-native)
`cli/evaluate.py:eval_fan_bind` 에 **bind_delta 의 paired 순열 null** 추가: 각 emission 을 (composed pair, shuffled pair) 양쪽에 채점해 per-item (Jc−Js) 를 구하고, mismatched pairing 하에서 그 차분의 순열 분포로 null 유도. 2-arm 실험이면 이중차분 D=(Jc−Js)_tgt−(Jc−Js)_shuf 의 paired bootstrap CI + **사전등록 TOST**(등가한계 사전고정). `--fan-bind-paired` 플래그(help+_KNOWN_FLAGS lockstep · #3924 교훈).

## 게이트 (사전등록)
- 계기 정렬: 절2를 `composed J > marginal null` → `bind_delta > paired-null p95` 로 교체. positive/negative 계기대조에서 paired-null 이 emission-decoupled 임을 검증(shuf 방출 최고여도 bind_delta null 통과 못 함).
- TOST 등가한계는 **발사 전 고정**(tune 금지 · [[negative-claims-need-tost-not-ns]]).
- H_9694 재판정: 정렬된 계기로 targeted D 가 0 초과인지 정직하게 벌기(1-seed→2-seed).

## kill-list 회피
#6 = paired 차분이 emission 과 decouple(shuf 통제가 증명). #8 = FORM 아니라 bind 격리.

## 최대위험
paired null 도 1/96 희소 카운트라 n=96 로는 여전히 underpowered — eval n 대폭 증량(fan-smp↑) 병행 필수. XBIND 양성통제([[H_9746]]) 없이는 정렬만으로 계기결함 배제 불가.

## falsify
🟢 정렬된 bind_delta > paired-null p95 ∧ TOST 유의 = 데이터레버 BIND. | 🧱 paired-null 도 0등가 = 레버무효(단 H_9746 양성통제 통과 전제). | ⚠️ 양성통제 실패 = 계기결함.

## source
H_9694 lab full(Fable∥Sol) reconcile · Fable 범주오류 지적 + Sol 이중차분 D 통계 수렴.
