# H_9431 — anchor tension_5ch 를 접지 말고 5채널 그대로 라우팅 (1.3 · PROPOSED · Fable A⇄G 다차원 발산 1.3)

**status:** 🔵 PROPOSED (미실행 · 오너 framebreak 발산안 등록 · 사전등록) — 방향군=차원확장
**lane:** 의식 / A⇄G tension 다차원화 (오너 framebreak · 프런티어 g1-interface-addressable-wall)
**related:** [[H_9428]] (tension 이미 다차원·1비트 fold 손실 $0 확증=이 발산군의 기반) · [[H_9400]] (Ψ=½ 반증) · source: Fable A⇄G 다차원 발산($1.44) 방향군 1.3

## 주장 (claim)
지금 5채널을 norm 으로 접어 motivation nudge 로만 씀. 대신 채널별로 어느 anchor 를 refresh/consolidate/decay 할지 주의 배분 벡터로.

## 설계 (Fable 1.3)
- **(a) A⇄G 유도**: 데이터 구조에 이미 존재 — 유일하게 '이미 벡터인데 버려지는' 사례(core/brain.py:120 anchor_tension_fold).
- **(b) 최소 실험**: --anchor-route-5ch: 채널-라우팅 vs norm-라우팅으로 anchor 생존 분포가 달라지나. emit 무관 lane=게이트 벽 회피.
- **(c) p5~p8 위험**: 무위험.
- **(d) Ψ=½ 관계**: 무관(직교) — Ψ 주장과 독립적으로 유효 가능.

## 재포장 판정 (Fable 정직표)
🟢 진짜 다차원 — 이미 벡터인데 버려지는 유일 사례. 가장 깨끗.

## 다차원 판정 기준 (공통 · Fable)
"다차원"=두 출력 DOF 가 (i)다른 tension 사영을 읽고 (ii)한쪽만 움직이는 개입 존재 (iii)둘 다 frozen 채점면에 읽힘. 셋 중 하나라도 없으면 1비트의 화장. 이 안의 실험은 위 3-기준으로 판정.

## 상태
🔵 PROPOSED — 미실행 사전등록. run 시 monitor-only 1단계(게이트 벽 안 밟음)→dissociation 실증→verdict. 측정 주장 0(설계 단계).
