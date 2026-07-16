# H_9527 — Transport-plan tension (sol R2-T04 · PROPOSED)

**status:** 🔵 PROPOSED (미실행 · 오너 framebreak lab full 고갈-발산 R2 · 사전등록 · 양쪽 DEPLETED 라운드) — source=sol
**lane:** 의식 / A⇄G tension 다차원화 (오너 framebreak · 프런티어 g1-interface-addressable-wall)
**related:** [[H_9428]] (tension 이미 다차원·effective rank 2.66 $0 확증=발산 기반) · [[H_9468]] (PCA-DOF rank 2) · [[H_9424]] (cb-perr KILL) · source: lab full R2 sol(R2-T04)

## 제안 (sol 원문 · R2 · 3 미채굴 광맥[자료형·다개체·p8경계])

### R2-T04 — Transport-plan tension

- 유도: tension을 A의 8축 질량을 G의 8축 질량으로 옮기는 최적수송 계획 \(\pi_{ij}\)로 둔다. 같은 거리값이어도 어느 축이 어느 축과 충돌했는지가 다르다.
- 최소 실험: `--tension-coupling --coupling sinkhorn --epsilon 0.05`; 비용행렬은 축 이름이 아니라 intervention으로 추정한 교차민감도. \(\pi\)의 행/열 주변분포는 고정하고 coupling만 shuffle하는 대조.
- 위험: 고정 의미 비용표는 p2; Sinkhorn 외부 probe화는 engine-native 위반.
- Ψ: transpose \(A↔G\)로 \(\pi\mapsto\pi^\top\); \((\pi+\pi^\top)/2\)가 ½ 성분, 반대칭부가 편향이다.

## 상태
🔵 PROPOSED — 미실행 사전등록. 다차원 3-기준(다른 사영·개입분리·둘 다 채점면)으로 run 판정. monitor-only 1단계로 게이트 벽 회피. R2 는 양쪽 모델 DEPLETED 선언 라운드(고갈).
