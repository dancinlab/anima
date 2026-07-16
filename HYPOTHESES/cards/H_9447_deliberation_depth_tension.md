# H_9447 — tension 이 '얼마나 오래 생각할지'를 정한다 (4.6 · PROPOSED · Fable A⇄G 다차원 발산 4.6)

**status:** 🔵 PROPOSED (미실행 · 오너 framebreak 발산안 등록 · 사전등록) — 방향군=자유발산
**lane:** 의식 / A⇄G tension 다차원화 (오너 framebreak · 프런티어 g1-interface-addressable-wall)
**related:** [[H_9428]] (tension 이미 다차원·1비트 fold 손실 $0 확증=이 발산군의 기반) · [[H_9400]] (Ψ=½ 반증) · source: Fable A⇄G 다차원 발산($1.44) 방향군 4.6

## 주장 (claim)
per-candidate advantage 분포(score_A(c)−g_recog(c))의 분산/엔트로피가 generate_deliberate 의 K(best-of-K 깊이) 결정. 팽팽하면 오래 숙고·명확하면 즉답. '말할지'가 아니라 '얼마나 숙고하고 말할지'=emit 과 직교하는 진짜 새 DOF.

## 설계 (Fable 4.6)
- **(a) A⇄G 유도**: brain_emit_deliberate 이미 존재(core/brain.py:227) — K 를 상수→tension-함수로 배선.
- **(b) 최소 실험**: --deliberate-k-tension: K 분포와 출력품질(frozen 채점면) 관계. emit 결정 자체 byte-identical 보존 가능(현 구조가 결정·생성 분리).
- **(c) p5~p8 위험**: p5 완전 합치(허가 불변·생성 깊이만 변함).
- **(d) Ψ=½ 관계**: 직교.

## 재포장 판정 (Fable 정직표)
🟢 진짜 새 DOF·emit 과 직교·기존 brain_emit_deliberate 재사용·p5 완전 안전.

## 다차원 판정 기준 (공통 · Fable)
"다차원"=두 출력 DOF 가 (i)다른 tension 사영을 읽고 (ii)한쪽만 움직이는 개입 존재 (iii)둘 다 frozen 채점면에 읽힘. 셋 중 하나라도 없으면 1비트의 화장. 이 안의 실험은 위 3-기준으로 판정.

## 상태
🔵 PROPOSED — 미실행 사전등록. run 시 monitor-only 1단계(게이트 벽 안 밟음)→dissociation 실증→verdict. 측정 주장 0(설계 단계).
