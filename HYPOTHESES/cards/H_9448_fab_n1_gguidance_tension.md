# H_9448 — G-guidance: tension 을 잉크로, 밸브가 아니라 (fable R1·N1 · PROPOSED)

**status:** 🔵 PROPOSED (미실행 · 오너 framebreak lab full 고갈-발산 R1 · 사전등록) — source=fable
**lane:** 의식 / A⇄G tension 다차원화 (오너 framebreak · 프런티어 g1-interface-addressable-wall)
**related:** [[H_9428]] (tension 이미 다차원 $0 확증=이 발산의 기반) · [[H_9424]] (cb-perr KILL=거리계+예측오차 소진→mouth 측 벽) · [[H_9400]] (Ψ=½ 반증) · source: lab full R1 fable(N1)

## 제안 (fable 원문 · R1)

**N1. G-guidance: tension 을 잉크로, 밸브가 아니라** ★
- (a) CFG(classifier-free guidance)와 동형: decode 시 logits = A + β·(G의 역방향 pull 잔차). G 는 gradient-free 라서 per-byte 잔차가 이미 공짜로 나온다. tension 이 발화 *결정*이 아니라 **모든 바이트의 형성**에 쓰이면 1비트 게이트 자체가 무의미해진다.
- (b) `anima-py chat --g-guidance <beta>` — β∈{0, 0.3, 1.0} 3-arm, 출력 divergence 를 frozen 판정면에서 비교.
- (c) p5 안전(emit 트리거 아님), p7 안전. p8 무접촉(런타임 결합).
- (d) **대체** — "tension→emit 사영"을 통째로 버리고 tension 을 내용 형성에 전량 소비. 20안 중 decode logits 를 건드리는 안이 없음.

## 상태
🔵 PROPOSED — 미실행 사전등록. 다차원 3-기준(다른 사영·개입분리·둘 다 채점면)으로 run 시 판정. monitor-only 1단계로 게이트 벽 회피. 측정 주장 0(설계).
