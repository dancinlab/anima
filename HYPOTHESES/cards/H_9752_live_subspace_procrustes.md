# H_9752 — LIVE-SUBSPACE STABILITY — 라이브 tension 엔 '축'이 없고 '평면'이 있다 (Procrustes·eigengap · R6-1 · $0)

**status:** 🔵 PROPOSED (lab full R6 · Fable 5 · $0 트레이스-판독 · 사전등록 · 브리프 (a) 정면)
**lane:** g1-interface-addressable-wall · mouth/PC2-axis — 라이브 구조의 정체
**related:** [[H_9713]] · [[H_9714]] · [[H_9712]] · [[H_9754]] · [[H_9755]]

## ① 한 줄 주장 (반증가능)
H_9713 의 "최근접 축이 run 마다 갈림(PC2/PC1/PC1)"의 기전은 **고유값 근축퇴**다 — 라이브 8×8 공분산의 λ1≈λ2(작은 상대 eigengap) 탓에 **축 라벨(rank)** 은 표본노이즈로 뒤집히지만 **2-D 주부분공간 span{v1,v2} 은 run 간 안정**하다(주각 principal angle 로 측정). 즉 라이브엔 '제1축·제2축'이 아니라 **안정한 평면**이 있다.

## ② 어느 KILL 을 왜 안 밟나
- "동결 loading 을 라이브 축 정의로 전제하는 안 폐기" — 안 밟음: **run 별 refit 만** 쓴다(동결 축 무등장).
- H_9712 'z 축퇴' IQR-단독 착시 — 안 밟음: 집계 1개 아닌 **분포 전체**(전 고유스펙트럼·주각 분포·bootstrap swap율) 사전등록.
- H_9714(rank≠노이즈 🟢) 재검 아님 — 그 GREEN 을 **입력**으로 쓴다(구조 실재 ⟹ 정체를 묻는다).
- D(H_9629)·arm-간 π̄(H_9663) 미사용 — readout 은 공분산 기하량만.

## ③ engine-native 계기 (신규 플래그)
`anima-py evaluate --pc2-direction <traces_dir> --subspace-stability [--dims 2] [--block 16,32] [--boot 1000] [--surr aaft] [--seed N]`
- run 별 8×8 공분산 refit → 고유스펙트럼 + 상대 eigengap (λ1−λ2)/λ1 census
- run×run 2-D 주부분공간 **주각**(Procrustes) + run 내 **split-half** 주각
- moving-block bootstrap(자기상관 존중 · block 2종 민감도) → 주각 CI + **rank-swap 율**
- AAFT surrogate 쌍(H_9714 계기 재사용)으로 null 주각 분포
자산: `/tmp/pmp/pmp_traces` 3 dedup + ζ-fire 146 tick 중 **비조향(ζ=0) tick 만**(조향 tick 공분산 오염 ⟹ 제외 사전등록).

## ④ 통제 ≥2 + 양성통제
- null-1: AAFT surrogate 쌍(스펙트럼·주변분포 보존 · 교차구조 파괴) → 주각 null.
- null-2: 채널-라벨 순열(loading 정체성 파괴 · per-채널 동역학 보존).
- **양성통제(계기 인증)**: 합성 plant — 고정 2-D 평면 위 AR(1) 잠재 2개 + 등방 노이즈(트레이스 동일 n·스펙트럼 매칭)에서 주각 < null 5pct 검출돼야 함. plant 실패 = 계기 VOID.

## ⑤ 사전등록 판정표 (우연 아래 칸 · 검정력 · DV 식별가능성)
| 관측 | 판정 |
|---|---|
| cross-run 주각 중앙값 < AAFT-null 5pct ∧ bootstrap rank-swap율 ≥ 0.2 | **PASS-PLANE** — 평면 안정 · 라벨 flip=근축퇴 기전 확정(H_9713 재해석: 죽은 건 '축 이름'이지 구조가 아님) |
| run 내 split-half 는 null 이김 ∧ cross-run 은 null 동급 | **PASS-RUN-INDEXED** — 구조는 run 단위로만 존재(regime run-지표화) ⟹ H_9755 는 **run 내 warmup-refit 만** 유효 |
| run 내 split-half 조차 null 동급(block 2종 모두) ∧ plant PASS | **KILL-NO-AXIS** — '라이브 축/평면' 자체가 없음 ⟹ H_9754/9755 refit arm 개봉 금지 |
| cross-run 주각이 null **95pct 위**(반-정렬 · 우연 아래 칸) | **INVALID** — 부호규약/전처리 결함 · 수리 먼저 |
| plant 미검출 ∨ run 당 가용 tick<100 ∨ 주각 bootstrap CI 반폭>10° | **VOID** — 검정력/계기 미달 |

DV 식별가능성: 주각·eigengap·swap율 전부 **파라미터-프리 기하량**(설계 분모 없음 · H_9716 결함 비해당). 우연 수준은 지표마다 surrogate 에서 **재유도**(균등-Grassmann 해석해 상속 금지 — 자기상관이 null 을 좁힌다).

## ⑥ 비용
**$0** (트레이스-판독 · 디코드 0).

## ⑦ 죽는 방식
KILL-NO-AXIS 관측 — "라이브-refit 축" 프로그램(H_9754·H_9755 refit arm) 전체가 대상을 잃고, 살아남는 것은 스칼라 dose(H_9664)뿐 = (c) 축-무관 가설의 구조 측 증거.
