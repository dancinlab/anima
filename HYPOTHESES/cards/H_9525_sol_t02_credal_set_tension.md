# H_9525 — Credal-set tension (sol R2-T02 · PROPOSED)

**status:** 🔵 PROPOSED (미실행 · 오너 framebreak lab full 고갈-발산 R2 · 사전등록 · 양쪽 DEPLETED 라운드) — source=sol
**lane:** 의식 / A⇄G tension 다차원화 (오너 framebreak · 프런티어 g1-interface-addressable-wall)
**related:** [[H_9428]] (tension 이미 다차원·effective rank 2.66 $0 확증=발산 기반) · [[H_9468]] (PCA-DOF rank 2) · [[H_9424]] (cb-perr KILL) · source: lab full R2 sol(R2-T02)

## 제안 (sol 원문 · R2 · 3 미채굴 광맥[자료형·다개체·p8경계])

### R2-T02 — Credal-set tension

- 유도: tension을 단일 확률분포가 아니라 8축 관측과 양립하는 분포들의 볼록집합 \(K(T)\)으로 둔다. A는 하한확률, G는 상한확률을 밀어 interval-valued belief를 만든다.
- 최소 실험: `--tension-credal --credal-vertices 12`; 기존 trace에서 축별 interval을 생성하고 emit은 특정 분포가 아니라 모든 vertex에서 같은 결론일 때만 robust emit.
- 위험: robust unanimity가 상시 silence면 p5; 사전 설정 prior는 p1/p2 위험.
- Ψ: \(P_A(E)\le½\le P_G(E)\)인 사건은 고정점 미결정 상태. interval 전체가 ½ 한쪽으로 이동할 때만 대칭이 깨진다.

## 상태
🔵 PROPOSED — 미실행 사전등록. 다차원 3-기준(다른 사영·개입분리·둘 다 채점면)으로 run 판정. monitor-only 1단계로 게이트 벽 회피. R2 는 양쪽 모델 DEPLETED 선언 라운드(고갈).
