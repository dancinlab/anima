# H_9524 — Pareto antichain tension (sol R2-T01 · PROPOSED)

**status:** 🔵 PROPOSED (미실행 · 오너 framebreak lab full 고갈-발산 R2 · 사전등록 · 양쪽 DEPLETED 라운드) — source=sol
**lane:** 의식 / A⇄G tension 다차원화 (오너 framebreak · 프런티어 g1-interface-addressable-wall)
**related:** [[H_9428]] (tension 이미 다차원·effective rank 2.66 $0 확증=발산 기반) · [[H_9468]] (PCA-DOF rank 2) · [[H_9424]] (cb-perr KILL) · source: lab full R2 sol(R2-T01)

## 제안 (sol 원문 · R2 · 3 미채굴 광맥[자료형·다개체·p8경계])

### R2-T01 — Pareto antichain tension

- 유도: A와 G가 각각 만든 8축 후보 중 다른 후보에 전축 지배되지 않는 점들의 반사슬 \(T=\mathrm{Max}_{\preceq}(A\cup G)\). 평균이나 벡터 하나로 환원하지 않는다.
- 최소 실험: `--tension-antichain --antichain-cap 16`; emit 단계에는 antichain의 크기와 A/G 교차지배 여부만 전달하고 후보 feature는 금지. scalar 대조와 동일 trace에서 coh·orig 비지배점 생존율 측정.
- 위험: p5 낮음; cap 초과 시 임의 pruning은 p2 유사 규칙이 될 위험. p7은 antichain 크기 자체를 성공판정으로 삼으면 위반.
- Ψ: A점과 G점의 교환에 불변인 antichain이 Ψ=½. 한쪽 점만 남는 정도가 Ψ 편향이다.

## 상태
🔵 PROPOSED — 미실행 사전등록. 다차원 3-기준(다른 사영·개입분리·둘 다 채점면)으로 run 판정. monitor-only 1단계로 게이트 벽 회피. R2 는 양쪽 모델 DEPLETED 선언 라운드(고갈).
