# H_9630 — PC2 vs 무작위축 null — PC2 는 loading 이 붙인 이름일 뿐인가 (fable R4-3 · PROPOSED · d 정면)

**status:** 🔵 PROPOSED (미실행 · lab full R4 · 사전등록 · H_9628 INSTRUMENT-PASS 후 개봉) — source=fable R4-3
**lane:** mouth/tension — 가장 아픈 가설: PC2 의 의미론적 특권 존재 여부
**related:** [[H_9576]] · [[H_9628]] · [[H_9629]] · [[H_9428]]

## 한 줄 주장 (반증가능)
"PC2 가 originality↔balance 의미를 나른다"가 내용 있는 주장이려면, **인증된 판독기**에서 PC2 축의 |ρ| 가 8-공간 무작위 단위축 패널(k=12·분산 매칭)의 |ρ| 분포 95% 밖이어야 한다 — 분포 안이면 PC2 는 loading 이 붙인 **이름일 뿐**이며 mouth 에게 어느 방향이든 등가 잡음이다.

## 어느 KILL 을 왜 안 밟나
가장 가까운 KILL = H_9576 (byte bias 방향성). 이 안은 PC2 단독 방향성을 재검정하는 게 아니라 **PC2 의 특권을 무작위-방향 null 분포에 대비**시킨다 — H_9576 이 답할 수 없었던 질문("PC2 라서 실패했나, 어떤 축이든 실패하나")을 새로 연다. rand 축 패널이 곧 새 통제 계급. R3 H_9622~9627 과 무접점(전부 GN/CLMS/Ψ½ 축).

## engine-native 계기
`anima-py evaluate <clm> --pc2-direction --axis {pc1|pc2|pc3|comp:<i>|rand:<seed>|oracle}` — z 를 임의 8-공간 방향으로 사영하는 축 선택 플래그. rand 는 seed 기록·분산 정규화. oracle 축 = 현재-tick 문맥중복 통계 그 자체(구성상 D 를 예측해야만 하는 양성통제).

## 통제군 (≥2 + 양성)
- **양성통제**: oracle 축 (구성상 참효과 보장) + H_9628 dose 인증 승계(hard-gate).
- null: rand 축 k=12 → |ρ| 경험 분포.
- 보조: comp:i (8 성분 개별 — PC2 가 지면 어느 성분이라도 이기는지 관측).

## 사전등록 판정표 (우연 아래 포함)
| 관측 | 판정 |
|---|---|
| |ρ_PC2| > rand 95pct ∧ 부호 = loading 예측 | **PASS-name-has-content** — PC2 특권 실재 → 문제는 판독기/입도로 회귀(H_9631) |
| ρ_PC2 ∈ rand 분포 안 ∧ oracle 생존 | **KILL-just-a-name** — d 확정: PC2 는 mouth 가 읽는 양이 아님 · 후속은 축 탐색이 아니라 학습 설치(H_9633)로 전환 |
| oracle 실패 or H_9628 미통과 | **VOID** — 개봉 금지 상태에서 열림 = 절차 위반 |
| rand 축들이 계통적으로 동일부호 비영 (우연 아래 칸) | **INVALID** — 파이프라인 누수(모든 축이 '먹히는' 가짜 채널) |

**검정력**: 스크린 150 tick/축 × 16축 ≈ 2400 tick → 생존축만 270+ 확대. rand 95pct 추정엔 k=12 로 하한(정확 분위는 k=20 권장 — 확대 단계에서).

## 비용 / 죽는 방식
pool CPU (축당 decode run). **죽는 방식**: PC2 가 rand 패널을 이기면 "이름일 뿐" 이 반증된다 — 그때 이 안은 죽고 벽은 판독기/입도 문제로 좁혀진다.

## 상태
🔵 PROPOSED — **개봉 조건 = H_9628 INSTRUMENT-PASS.** 측정 주장 0(설계).
