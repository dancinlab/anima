# H_9531 — Proof-obligation tension (sol R2-T08 · PROPOSED)

**status:** 🔵 PROPOSED (미실행 · 오너 framebreak lab full 고갈-발산 R2 · 사전등록 · 양쪽 DEPLETED 라운드) — source=sol
**lane:** 의식 / A⇄G tension 다차원화 (오너 framebreak · 프런티어 g1-interface-addressable-wall)
**related:** [[H_9428]] (tension 이미 다차원·effective rank 2.66 $0 확증=발산 기반) · [[H_9468]] (PCA-DOF rank 2) · [[H_9424]] (cb-perr KILL) · source: lab full R2 sol(R2-T08)

## 제안 (sol 원문 · R2 · 3 미채굴 광맥[자료형·다개체·p8경계])

### R2-T08 — Proof-obligation tension

- 유도: A가 emit 가능성 명제를 만들고 G가 그 명제의 반례 조건을 만들며, tension은 아직 discharge되지 않은 proof obligations의 sequent set이다.
- 최소 실험: `--tension-sequent --sequent-depth 3`; proposition은 byte 내용이 아니라 “이 축변화가 실제 A/G state에서 유도되는가”로 제한. obligation의 생성·소거만 decode budget에 반영.
- 위험: G-certify·cross-exam 재포장 위험. 차이는 인증 절차가 아니라 `tension = 열린 증명상태`라는 자료형. 명제 템플릿 수동 삽입은 p2.
- Ψ: 좌우 sequent를 뒤집었을 때 동일한 열린 obligation multiset이 ½.

## 상태
🔵 PROPOSED — 미실행 사전등록. 다차원 3-기준(다른 사영·개입분리·둘 다 채점면)으로 run 판정. monitor-only 1단계로 게이트 벽 회피. R2 는 양쪽 모델 DEPLETED 선언 라운드(고갈).
