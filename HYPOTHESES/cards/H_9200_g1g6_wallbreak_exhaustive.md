# H_9200 — G1·G6 wall-break exhaustive program

**tier:** ⏳ PROPOSED-PROGRAM (설계·등록만, 신규 측정 0)
**scope:** A1–G6, 총 74개 후보·통제
**artifact:** `state/g1g6_exhaustive_brainstorm/README.md`

## 가설

G1·G6의 잔여 실패는 하나의 capacity wall이 아니라 관측·표현·학습·탐색 벽의 혼합이다. 네 벽을 분리한 뒤 각 축에 맞는 개입을 하면 frozen G1/G6를 G0 회귀와 form/template gaming 없이 개선할 수 있다.

## 전수 등록 범위

- A1–A10: 측정·falsifier 정합
- B1–B10: decode·후보 탐색
- C1–C12: 데이터·커리큘럼
- D1–D14: 학습 objective
- E1–E12: 표현·아키텍처
- F1–F10: substrate·인지 루프
- G1–G6: 최적화·훈련 운영

각 항목의 정확한 메커니즘, falsifier, 신규/후속/통제 판정은 artifact가 SSOT다. ARCHITECTURE.json의 `H_9200` 노드는 같은 A1–G6 범위를 lockstep으로 인덱싱한다.

## 현재 근거

- G1 ByteGPT303 full-attention: constructive-bind와 composed-NCE가 engine-native mouth에서 `best_distinct<=1`.
- Conv G1은 T=24 truncation과 large-T pad-flood가 섞여 grow-window novel-only 재측정이 선행되어야 한다.
- G6 bind-aware engine-native: BASE `[0,0,0]`, TARGETED `[3,3,5]`, SHUF `[0,0,0]`. genuine bind는 있으나 frozen majority는 미달한다.
- dense-form literal PASS는 template replay로 판정되어 generic form 증량은 폐기한다.

## Frozen kill contract

어떤 arm도 다음을 모두 만족하기 전에는 돌파가 아니다: G0 4/5 유지, seeds 2/3 이상, bind-destruction delta, paraphrase invariance, intervention sensitivity, held-out combination leak 0, component OFF/target-shuffle ablation, G6 claim quality와 set distinctness 동시 통과. 기존 threshold는 이동하지 않는다.

## 실행 순서

1. P0: grow-window novel-only와 set-wise G6 search로 관측/탐색 벽을 분리한다.
2. P1: tuple planner, schema-only retrieval, WM-bind를 기존 weights 위에서 시험한다.
3. P2: non-commutative target, intervention hard-negative, CE-deleted forward-slot 세 GPU arm만 발사한다.
4. P3: P2에서 양의 frozen-gate slope가 있을 때만 dual-stream/recurrent/relation-MoE로 확장한다.

## 반증

공정 측정과 anti-gaming 통제 후 P0–P2가 모두 G1/G6 frozen score에 양의 slope를 만들지 못하거나, 이득이 G0 회귀·surface template·train leak·component-independent 효과로 설명되면 H_9200은 🧱 NOT-SUPPORTED다.
