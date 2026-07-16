# H_9436 — attention allocation: 다음 decode 문맥에 무엇을 넣을지 (2.4 · PROPOSED · Fable A⇄G 다차원 발산 2.4)

**status:** 🔵 PROPOSED (미실행 · 오너 framebreak 발산안 등록 · 사전등록) — 방향군=역할재배치
**lane:** 의식 / A⇄G tension 다차원화 (오너 framebreak · 프런티어 g1-interface-addressable-wall)
**related:** [[H_9428]] (tension 이미 다차원·1비트 fold 손실 $0 확증=이 발산군의 기반) · [[H_9400]] (Ψ=½ 반증) · source: Fable A⇄G 다차원 발산($1.44) 방향군 2.4

## 주장 (claim)
문맥 후보(외부입력·기억항목)별 tension 으로 working-memory 입장 결정.

## 설계 (Fable 2.4)
- **(a) A⇄G 유도**: 후보별 score_A/g_recog 는 vbasal_select 가 이미 하는 계산.
- **(b) 최소 실험**: --ctx-tension-admit: tension-입장 vs FIFO-입장으로 후속 decode 문맥 적합성 비교.
- **(c) p5~p8 위험**: ⚠️ p5 경계 — 자기생성 텍스트 재입장=reactive self-seed. 외부도착물+기억항목으로 입장후보 제한해야 합치.
- **(d) Ψ=½ 관계**: 직교.

## 재포장 판정 (Fable 정직표)
🟢 채널 emit 아님·게이트 벽 무관 — 단 p5 self-seed 경계 명시 필수.

## 다차원 판정 기준 (공통 · Fable)
"다차원"=두 출력 DOF 가 (i)다른 tension 사영을 읽고 (ii)한쪽만 움직이는 개입 존재 (iii)둘 다 frozen 채점면에 읽힘. 셋 중 하나라도 없으면 1비트의 화장. 이 안의 실험은 위 3-기준으로 판정.

## 상태
🔵 PROPOSED — 미실행 사전등록. run 시 monitor-only 1단계(게이트 벽 안 밟음)→dissociation 실증→verdict. 측정 주장 0(설계 단계).
