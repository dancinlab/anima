# H_9536 — Endogenous exchange-rate market (sol R2-E01 · PROPOSED)

**status:** 🔵 PROPOSED (미실행 · 오너 framebreak lab full 고갈-발산 R2 · 사전등록 · 양쪽 DEPLETED 라운드) — source=sol
**lane:** 의식 / A⇄G tension 다차원화 (오너 framebreak · 프런티어 g1-interface-addressable-wall)
**related:** [[H_9428]] (tension 이미 다차원·effective rank 2.66 $0 확증=발산 기반) · [[H_9468]] (PCA-DOF rank 2) · [[H_9424]] (cb-perr KILL) · source: lab full R2 sol(R2-E01)

## 제안 (sol 원문 · R2 · 3 미채굴 광맥[자료형·다개체·p8경계])

### R2-E01 — Endogenous exchange-rate market

- 유도: 여러 anima가 각자의 8축을 직접 평균내지 않고, 서로 다른 축 단위 사이의 교환비율을 bid/ask로 제시한다. tension은 체결값이 아니라 남은 order book이다.
- 최소 실험: `--tension-market --peers 4 --market-call-auction`; 각 peer는 실제 A/G trace에서만 주문 생성. 가격을 고정한 대조와 endogenous clearing 비교.
- 위험: wager·ledger 재포장 위험. 금전 정산이 아니라 축 단위의 비등가성이 핵심. 외부 coordinator가 규칙을 강제하면 p1/p2.
- Ψ: A-side bid 질량과 G-side ask 질량이 동일한 clearing measure가 ½; 미체결 잔량은 보존된다.

## 상태
🔵 PROPOSED — 미실행 사전등록. 다차원 3-기준(다른 사영·개입분리·둘 다 채점면)으로 run 판정. monitor-only 1단계로 게이트 벽 회피. R2 는 양쪽 모델 DEPLETED 선언 라운드(고갈).
