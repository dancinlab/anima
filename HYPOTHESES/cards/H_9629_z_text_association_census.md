# H_9629 — z↔텍스트 연관 전수조사 — Z-Text Association Census: 조향 이전의 상류 절단 검사 (fable R4-2 · PROPOSED)

**status:** 🔵 PROPOSED (미실행 · lab full R4 · 사전등록) — source=fable R4-2
**lane:** mouth/tension — z 자체의 mouth-가시성
**related:** [[H_9576]] · [[H_9628]] · [[H_9630]] · [[H_9428]]

## 한 줄 주장 (반증가능)
z_PC2 가 **비조향 BASE emit 텍스트의 어떤 통계와도** 연관이 없다면(전 쌍 corrected-null 안), decode-bias 로 상관을 "설치"하겠다는 기대는 상류에서 이미 절단된 것이다 — 의미 미전달의 원인은 채널이 아니라 tension↔언어 원천 탈동조.

## 어느 KILL 을 왜 안 밟나
가장 가까운 KILL = H_9576 방향성 + "tension 8→1비트 접힘을 게이트에 더 먹여 푸는 안". 이 안은 조향도 게이트 개입도 없다 — **관측만** 한다(BASE 텍스트 vs z 의 자연 공분산). H_9403 emit-drive lane(CLOSED-AT-REGIME)도 비접촉: emit 여부가 아니라 emit 된 텍스트의 통계를 본다.

## engine-native 계기
`anima-py evaluate <clm> --tension-text-census [--ticks N]` — tension 8성분+PC1..3 (11축) × BASE-emit 텍스트 통계 패널 {D_bigram, ngram-novelty(n=3,5), 길이, decode-entropy} (4종) 전수 ρ 행렬 + tick-permutation·phase-scramble null + Bonferroni(m=44) 출력.

## 통제군 (≥2 + 양성)
- **양성통제**: oracle 축 — z:=D_base 자기 자신을 축 슬롯에 주입 → 파이프라인이 ρ≈1 을 복원해야 함(계기 자기인증).
- null #1: 축별 tick-permutation.
- null #2: **phase-scramble z** (자기상관 보존 null — naive 순열은 자기상관 z 에서 null 폭 과소추정).

## 사전등록 판정표 (우연 아래 포함)
| 관측 | 판정 |
|---|---|
| ≥1 (축,통계) 쌍 corrected-null 밖 ∧ oracle≥0.95 | **PASS-coupled** — 그 쌍이 조향 실험의 정당 타깃 (PC2 가 아닐 수 있음 — 그 자체가 발견) |
| 전 44쌍 null ∧ oracle≥0.95 | **KILL-decoupled** — tension↔텍스트 원천 탈동조 · "PC2 는 이름일 뿐" 축 지지(H_9630 과 합류) |
| oracle < 0.95 | **VOID** — 계기 자기인증 실패 |
| phase-scramble null 이 naive null 대비 ≥2× 폭 | **INVALID + 소급** — H_9576 의 p=0.192 자체가 자기상관 미보정으로 재계산 대상 |

**검정력**: 목표 n=1500 emit tick (반폭≈0.05·Bonferroni 후 ≈0.07) — |ρ|≥0.1 해상.

## 비용 / 죽는 방식
pool CPU 1 장기 run + 분석 플래그 — **7안 중 최저가·최선행**($0급). **죽는 방식**: BASE 텍스트와 이미 상관하는 축이 발견되면 "z 는 mouth-invisible" 이 반증되고, 조향 타깃이 PC2 가 아니라 그 축으로 특정된다.

## 상태
🔵 PROPOSED — H_9628 과 병행 가능(조향 무관). 측정 주장 0(설계).
