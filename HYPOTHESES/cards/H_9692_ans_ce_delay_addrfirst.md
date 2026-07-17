# H_9692 — address-first 2-phase: ans-CE 지연으로 흐린-v 창 제거 (RV-2 · 최저가 대안)

**status:** 🔵 PROPOSED (미실행 · lab full RV-2 · 303M pool 2-seed · DESIGN-ONLY)
**lane:** g1-storebridge-val-robust
**related:** [[H_9672]] · [[H_9690]] · [[H_9691]] · [[H_9693]]
**source:** lab full RV (Fable 발산) — 의뢰자 선험후보 (c) 온도-annealing 의 재진단판

## 한 줄 주장 (반증가능)
phase-1 에서 **addr-loss 만**(ans-CE weight 0)으로 W_q 를 먼저 sharp 하게 만든 뒤 phase-2 에서 ans-CE 를 켜면, val 의 **첫 gradient 부터** Stage1.5-급 clean 신호가 되어 op-only 국소최적 진입 창이 사라진다.

## ① 근거
- 나쁜 basin 진입은 **초기 흐린-v 창**에서 일어난다(RV-0 공유 진단). 창을 시간축에서 제거하는 최소 수단 = 학습 순서 강제.
- 의뢰자 (c)(온도 annealing) 의 결함: 초기 sharp 는 **sharp-but-wrong** — 자신있는 오답 주소로 val gradient 를 오염시킬 수 있다. 올바른 형태는 "일찍 sharp"가 아니라 "**정확해진 다음에 값 학습**" = 본 카드.
- phase-2 시작 시 val/W_h/W_out 은 랜덤 init 이지만 주소는 이미 정확·sharp(addr-loss 는 H_9672 서 2-seed robust) — Stage1.5(주소 공짜 상태에서 val 1.00 분화)와 동일 레짐.

## ② 최소 구현 (trainer-only · ~5줄)
- 플래그 `--store-ans-delay N`: step<N 에서 store 손실 = w_addr·L_addr 만(ans-CE 항 0 · val/W_h/W_out 무grad), step≥N 부터 전체.
- **N 사전등록**: T3 로그에서 양 seed 의 addr-gap≤0.2 도달 step × 2 (단일값 · seed 별 스캔 금지).
- core/clms.py·트레일러·eval 무변경.

## ③ 사전등록
- toy = 배관 회귀만(RV-1 과 동일한 정직 스코프 — toy 는 fragility 미재현이라 반증력 0).
- 결정면 = 303M 2-seed {7,11} · T3 config + delay N · 총 step = T3 + N(연장분은 phase-1 몫 — kill-list 의 'step 증액'과 구분: 그건 동일기전 연장, 이건 스케줄 변경. 대조를 위해 등예산 arm 도 기록).
- 게이트: ORACLE≥.90 ∧ P1-balanced≥.75 ∧ addr-gap≤.20 ∧ flip≥.90 (양 seed · balanced). PASS 시 confirm seed 13.
- 통제군: ① delay=0 = T3 재현(양성대조) ② 등예산(T3 총 step 고정 · phase-1 이 잡아먹는) arm ③ λ=0 C2.

## ④ 잔인판정
- **잔존 blur**: phase-2 주소는 addr_mass≈0.95 sharp-but-soft — ~5% majority 누수가 원리적으로 남는다(RV-3 만 이걸 구조 봉쇄). 그 5% 로도 seed-11 이 또 죽으면 이 레버 한계.
- **trunk 드리프트**: phase-1 동안 main-corpus CE 로 trunk 이 움직여 yn_q 분포가 변함 → phase-2 초 주소 재열화 가능(addr-loss 상시 유지로 완화 — 그래도 열리는 창은 창이다).
- N 은 새 하이퍼 — N 스캔 = tune-to-green. 단일 N, 실패는 결과.
- 감독 tier 동일(addr 라벨) · 창발 주장 불가.

## 비용
303M 2런(+confirm 1런) · pool · RV-1 과 동일 자릿수(phase-1 은 lane 만이라 약간 쌈).

## 죽는 방식
sharp-correct 주소를 첫 step 부터 줬는데도 seed-11 val 이 미분화면 죽는다 — 그러면 흐린-v 창 가설 자체가 부정되고 사인은 값경로 구조(→ RV-3/RV-0 재부검).

## 상태
🔵 PROPOSED — 측정 주장 0(설계).
