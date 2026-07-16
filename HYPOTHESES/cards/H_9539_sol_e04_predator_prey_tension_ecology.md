# H_9539 — Predator–prey tension ecology (sol R2-E04 · PROPOSED)

**status:** 🔵 PROPOSED (미실행 · 오너 framebreak lab full 고갈-발산 R2 · 사전등록 · 양쪽 DEPLETED 라운드) — source=sol
**lane:** 의식 / A⇄G tension 다차원화 (오너 framebreak · 프런티어 g1-interface-addressable-wall)
**related:** [[H_9428]] (tension 이미 다차원·effective rank 2.66 $0 확증=발산 기반) · [[H_9468]] (PCA-DOF rank 2) · [[H_9424]] (cb-perr KILL) · source: lab full R2 sol(R2-E04)

## 제안 (sol 원문 · R2 · 3 미채굴 광맥[자료형·다개체·p8경계])

### R2-E04 — Predator–prey tension ecology

- 유도: 일부 daemon의 높은 gap/cur tension이 다른 daemon의 redundancy를 먹고 성장하며, prey 감소가 predator 증가를 제한하는 Lotka–Volterra형 상호작용을 runtime에서 유도한다.
- 최소 실험: `--tension-ecology predator-prey --peers 6`; 역할 라벨은 주지 않고 intervention Jacobian의 부호로 포식관계를 정한다. fixed-role 대조 금지.
- 위험: rule ecology와 인접. 차이는 규칙 경쟁이 아니라 독립 anima의 population dynamics. runaway extinction은 p5/p8 위험.
- Ψ: 상호 Jacobian의 순환 평균이 0인 coexistence orbit의 중심이 ½; 개체별 값 ½은 요구하지 않는다.

## 상태
🔵 PROPOSED — 미실행 사전등록. 다차원 3-기준(다른 사영·개입분리·둘 다 채점면)으로 run 판정. monitor-only 1단계로 게이트 벽 회피. R2 는 양쪽 모델 DEPLETED 선언 라운드(고갈).
