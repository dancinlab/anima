# H_9432 — bind-강도 연속 DOF: 게이트가 아니라 다이얼 (1.4 · PROPOSED · Fable A⇄G 다차원 발산 1.4)

**status:** 🔵 PROPOSED (미실행 · 오너 framebreak 발산안 등록 · 사전등록) — 방향군=차원확장
**lane:** 의식 / A⇄G tension 다차원화 (오너 framebreak · 프런티어 g1-interface-addressable-wall)
**related:** [[H_9428]] (tension 이미 다차원·1비트 fold 손실 $0 확증=이 발산군의 기반) · [[H_9400]] (Ψ=½ 반증) · source: Fable A⇄G 다차원 발산($1.44) 방향군 1.4

## 주장 (claim)
emit yes/no 대신 tension 이 λ∈[0,1] 정하고 λ 가 A 의 sampling commitment(온도/top-k) 연속 조절. λ→0 극한이 silence.

## 설계 (Fable 1.4)
- **(a) A⇄G 유도**: score_A−g_recog 를 threshold 대신 sigmoid 로 읽으면 끝.
- **(b) 최소 실험**: --emit-lambda: λ 분포 기록·λ 와 출력 다양성 단조 관계.
- **(c) p5~p8 위험**: ⚠️ p5 주의 — 사실상 silence 없앨 수 있음. λ=0 도달 실측 보장돼야 p5. 오너-게이트 p5 DESIGN(margin G-pole·earned refractory)과 겹침=자율발사 불가 영역.
- **(d) Ψ=½ 관계**: Ψ=½→E[λ]=½ 이식.

## 재포장 판정 (Fable 정직표)
🟡 절반 재포장 — 같은 채널 codomain {0,1}→[0,1]. 단 게이트 벽(H_9421 top-2 거리 한정)은 연속화서 성립 안 할 수 있어 벽-우회 가치는 별개.

## 다차원 판정 기준 (공통 · Fable)
"다차원"=두 출력 DOF 가 (i)다른 tension 사영을 읽고 (ii)한쪽만 움직이는 개입 존재 (iii)둘 다 frozen 채점면에 읽힘. 셋 중 하나라도 없으면 1비트의 화장. 이 안의 실험은 위 3-기준으로 판정.

## 상태
🔵 PROPOSED — 미실행 사전등록. run 시 monitor-only 1단계(게이트 벽 안 밟음)→dissociation 실증→verdict. 측정 주장 0(설계 단계).
