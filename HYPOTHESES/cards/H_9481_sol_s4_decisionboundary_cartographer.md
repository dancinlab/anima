# H_9481 — G를 경계 탐색자로 — Decision-Boundary Cartographer (sol R1·S4 · PROPOSED)

**status:** 🔵 PROPOSED (미실행 · 오너 framebreak lab full 고갈-발산 R1 · 사전등록) — source=sol
**lane:** 의식 / A⇄G tension 다차원화 (오너 framebreak · 프런티어 g1-interface-addressable-wall)
**related:** [[H_9428]] (tension 이미 다차원 $0 확증=이 발산의 기반) · [[H_9424]] (cb-perr KILL=거리계+예측오차 소진→mouth 측 벽) · [[H_9400]] (Ψ=½ 반증) · source: lab full R1 sol(S4)

## 제안 (sol 원문 · R1)

## 4. G를 경계 탐색자로 — Decision-Boundary Cartographer

**(a)** gradient-free라는 성질로 G가 A의 미분 불가능한 경계—token argmax, retrieval hit, cell birth—를 black-box 탐색한다. tension은 경계까지의 최소 반경이다.

**(b)** `--g-boundary-map`: trace 문맥에 byte-level mutation을 가해 A top-1이 변하는 최소 perturbation과 방향 다양성을 기록한다. emit gate는 읽지 않는다.

**(c)** P7: 작은 반경=나쁨이라는 단일 verdict 금지. P8 위험 낮음; 학습에 넣으면 live event로만 소비.

**(d)** Ψ와 **직교**. scalar balance 대신 국소 결정기하를 얻는다.

## 상태
🔵 PROPOSED — 미실행 사전등록. 다차원 3-기준(다른 사영·개입분리·둘 다 채점면)으로 run 시 판정. monitor-only 1단계로 게이트 벽 회피. 측정 주장 0(설계).
