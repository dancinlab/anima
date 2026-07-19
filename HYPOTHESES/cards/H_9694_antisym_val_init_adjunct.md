# H_9694 — 반대칭 val init(+margin): 대칭깨기 보조 레버 (RV-4 · adjunct 전용 · 단독 베팅 금지)

**status:** 🔵 PROPOSED (미실행 · lab full RV-4 · adjunct — 단독 arm 은 RV-1~3 전멸시에만)
**lane:** g1-storebridge-val-robust
**related:** [[H_9672]] · [[H_9690]] · [[H_9691]] · [[H_9693]]
**source:** lab full RV (Fable 발산) — 의뢰자 선험후보 (b) val 직접감독의 강등·문서화 + init 각도

## 한 줄 주장 (반증가능)
val 을 **반대칭 초기화**(val[1]=−val[0] · scale 0.5/√d_s, 기존 randn·0.02 대비 큰 초기분리)하면 흐린-v 창에서도 slot-특이 신호가 살아남아 op-only basin 진입 확률이 내려간다 — 단 **확률 nudge 지 보장이 아니다**.

## ① 근거 (그리고 (b) 가 강등된 이유)
- 현 init(randn·0.02)의 초기 분리 ‖val[0]−val[1]‖ 는 미시적 — 분화는 전적으로 gradient 부트스트랩에 의존 = seed 복권. 큰 반대칭 init 은 복권 없이 분리를 **선물**한다.
- **(b) margin loss(‖val[0]−val[1]‖ 강제)의 결함 = 분리≠소비**: W_h v-블록이 귀먹으면(RV-0 의 사인 B) margin 만점이어도 ORACLE 0.50 그대로다. 분리를 손실로 사는 것은 지표를 사는 것이지 기능을 사는 게 아니다. 같은 이유로 init 각도도 **소비를 보장 못한다** — 그래서 adjunct.
- 올바른 용법: RV-1/2/3 승자 위에 **스태킹**(비용 0·플래그 1개)해 성공 마진을 넓히는 보험.

## ② 최소 구현 (trainer-only · ~4줄)
- `CLMSModule.__init__`: `--clms-val-init antisym` 시 `u=randn(d_s); val=stack([+c·u,−c·u])`, c=0.5/√d_s.
- (선택 arm) `--store-val-margin m`: L_sep=max(0, m−‖val[0]−val[1]‖²) — (b) 원형, 문서화용 대조 arm 으로만.
- 트레일러/eval 무변경.

## ③ 사전등록
- 단독 결정면 없음(adjunct). 용법 = 승자 레버 arm ± antisym init 의 paired 2-seed 비교(게이트 동일: ORACLE≥.90 ∧ P1-bal≥.75 ∧ addr-gap≤.20 ∧ flip≥.90).
- (b) 대조 arm(margin 단독 + 현행 init): **예측 = margin 만점 ∧ seed-11 ORACLE<0.90** — 분리≠소비의 직접 시연. 이 arm 이 PASS 하면 본 카드의 강등 논리가 반증되는 것(그것도 결과).
- toy = 배관 회귀만(정직 스코프 RV-1 과 동일).

## ④ 잔인판정
- init 스케일은 basin **확률**을 움직일 뿐 기전 제거가 아니다 — {7,11} PASS 해도 새 seed 에서 재발 가능. 단독으론 TERMINAL 후보 자격 없음.
- c 를 스캔하면 tune-to-green — 단일값 고정.
- margin arm 은 held-out 일반화 자명론(val 은 개체무관 2행)을 실측 없이 믿지 말 것 — flip 게이트로만 판단.

## 비용
승자 레버 런에 편승(추가 런 ≤2) · pool.

## 죽는 방식
antisym init 스태킹이 승자 레버의 게이트 마진을 전혀 안 넓히면(paired Δ≈0) 보험 가치 0 으로 죽는다.

## 상태
🔵 PROPOSED — 측정 주장 0(설계).
