# H_9508 — 제약저장소 tension — emit = UNSAT core (fable R2-D1 · PROPOSED)

**status:** 🔵 PROPOSED (미실행 · 오너 framebreak lab full 고갈-발산 R2 · 사전등록 · 양쪽 DEPLETED 라운드) — source=fable
**lane:** 의식 / A⇄G tension 다차원화 (오너 framebreak · 프런티어 g1-interface-addressable-wall)
**related:** [[H_9428]] (tension 이미 다차원·effective rank 2.66 $0 확증=발산 기반) · [[H_9468]] (PCA-DOF rank 2) · [[H_9424]] (cb-perr KILL) · source: lab full R2 fable(R2-D1)

## 제안 (fable 원문 · R2 · 3 미채굴 광맥[자료형·다개체·p8경계])

### D1. 제약저장소 tension — emit = UNSAT core
- **자료형**: 논리 절 집합(SAT 인스턴스). A 의 forward 예측이 ground-fact 절을, G 의 acceptance 요구가 제약 절을 추가. tension = 저장소의 충족가능성 구조, emit 내용 = **minimal UNSAT core 의 언어화**, silence = SAT. coh·orig 가 사영으로 버려지지 않고 절로 잔존(H_9428 직접 응답).
- **(a)** G 가 gradient-free = 본질적으로 checker — G-threshold 교차를 리터럴로 이산화하면 절은 엔진이 이미 계산하는 양에서 나온다.
- **(b)** `anima-py evaluate --tension-dtype clauses`: 창 단위 SAT 판정 + UNSAT-core 크기 기록($0·게이트 무변경). 판독 = core 크기가 스칼라 tension 에 없는 emit 예측력을 갖는가.
- **(c)** p5: threshold 이산화를 손튜닝하면 hardcoded gate — 학습분포 분위수로 earn 할 것.
- **(d)** Ψ=½ = **random-SAT 상전이점**(절 밀도 α=α_c 에서 SAT/UNSAT 반반). ½ 이 확률이 아니라 제약밀도 임계로 재유도 — H_9400 이후 대체 유도 ①.

## 상태
🔵 PROPOSED — 미실행 사전등록. 다차원 3-기준(다른 사영·개입분리·둘 다 채점면)으로 run 판정. monitor-only 1단계로 게이트 벽 회피. R2 는 양쪽 모델 DEPLETED 선언 라운드(고갈).
