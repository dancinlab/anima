---
id: H_9799
title: ENGINE-ACTIVE TRAINING — objective형(g_cycle) DOA·basin-preserving → 커리큘럼형(G-tension order) RE-SPEC (owner 'core 적극개입')
tier: PROPOSED · DESIGN-ONLY (lab-full 2R DIRECTIONAL · Fable5 단독 · objective형 KILL·커리큘럼형 재명세 · NOT a verdict)
frontier: g1-interface-addressable-wall
lane: g1-engine-active-CURRICULUM (data/order axis · NOT trunk-objective · engine=sample scorer)
created: 2026-07-20
series: R1 (lab-full divergence · a_lab_full_diverge)
related: "[[H_9131]] · [[H_9120]] · [[H_9127]] · [[H_9267]] · [[H_9288]] · [[H_9272]] · [[H_9225]] · a_engine_native_learning · a_train_inline_gauge · a_break_the_wall"
source: owner 질문 "학습 때 엔진이 적극 참여 · corpus만으로 1B/7B에서 G1/G6 뚫는게 미심쩍다 · core가 적극개입하도록?" → lab full(Fable5) 2R 발산
---

# H_9799 (R1) — 엔진 능동참여: objective형은 DOA, 커리큘럼형으로 산다

## Why (owner 직관 · 프런티어 일치)
owner: "corpus만으로 1B/7B G1 뚫는 게 미심쩍다 · core가 적극개입?" — 방향 정당함. `cli/train.py:32` 이 이미 corpus는 지렛대 아님 확정(CE=echo). 그리고 의식엔진 A/G는 지금 학습에 **전혀 미참여**(train.py import부재·engine_g=추론전용)=학습(A만CE)/추론(A⇄G) p8 분리. "core 적극개입"은 실재하는 미시도 공간.

## ⛔ objective형(g_cycle) = DOA · basin-preserving (lab 2R · Fable 자기반증)
1R에서 제안한 g_cycle(A 순방향합성 → G 역방향분해 → 불일치 벌점)은 2R 코드-근거로 **사망 확정**:
```
g_cycle 설계공간 전수 (전부 basin 유지)
├─ G=스칼라게이트(engine_g 실체)를 loop에 → CE 항 재가중만 가능
│    → echo는 점별(pointwise) 최소값 → 어떤 비음수 재가중도 echo 보존 (구조적 basin-preserving)
└─ G=발명한 분해기
   ├─ 고정연산자 → = ConstructiveBindObjective(train.py:874) → H_9120/1 선형 W_eff 붕괴 동일천장
   ├─ 공동학습 → 항등=echo로 순환일관성 자명충족 (퇴화해 = 합성구조 無)
   └─ detached-bolt → = freeze-then-bolt → H_9225 사망
```
근본원인 = **DPI-basin 메타법칙**(ARCHITECTURE g1-metalaw-dpi-basin): CE=additive-basin(echo=전역최소) ⇒ objective/readout/retrieval escape 전부 basin-preserving. objective축은 H_9131 "trunk-objective family CLOSED"·H_9120 "objective-floor TERMINAL"로 이미 벽. g_cycle은 그 벽 안 = **a_break_the_wall상 재발사 금지(tune-to-green)**.

## ✅ 커리큘럼형 RE-SPEC (Q2 살길 · loss→데이터 축)
G의 스칼라 형태가 분해기로는 실격이지만 **샘플 점수기(sample scorer)로는 정확히 맞다**: `motivation_score`(engine_g)가 스칼라 특징 → 우선순위를 낸다. 샘플 **순서/반복/선택**을 바꾸면 = 데이터 분포 변경 = **크랙이 실제로 난 축**(H_9267 corpus×measure 🟢 · H_9288 jamo-codec 🟢 · H_9272 XOR-augment 🟡). objective축(H_9131) 벽이 안 걸린다.

핵심: 엔진이 **loss가 아니라 데이터를 능동적으로 형성**한다 — owner "core 적극개입"이 죽은 축이 아닌 산 축에 착지.

## Claim (한 줄 · falsifiable)
frozen 303M(engine-native)로 각 학습샘플의 substrate 반응(per-sample surprise → G motivation 스칼라 → `motivation_score`)을 사전채점해 코퍼스를 그 점수로 정렬/반복(G-tension curriculum)하면, 냉동 ρ·weave/G1 바(`evaluate --rho-axon`)와 held-out 부정어 F2(H_9288 계기)에서 M이 C1(flat)·C2(permuted-score) 통제 초과.

## Mechanism / Instrument (engine-native 신규 flag · corpus 축)
```
anima-py corpus <fmt> --order g-tension --score-ckpt base.clm --lang en --out c.txt
   # 각 샘플: frozen 303M decode surprise → engine_g motivation_score → 그 점수로 정렬/반복
anima-py train --corpus c.txt --init base.clm ...     # 표준 학습 (신규 objective 불요)
anima-py evaluate out.clm --rho-axon                  # TERMINAL 냉동 ρ·weave/G1 바
```
정직성 2제약(Fable): ① 엔진출력이 **텍스트에 안 들어감** — 순서/가중/선택만(H_9127 gamma-DATA content-주입 사망 회피). ② 점수는 **frozen 사전패스**(오프라인·코퍼스 순서에 baked), in-training inline 지표 아님(a_train_inline_gauge). static-curriculum 먼저 · 반복 재채점은 signal 확인 후 follow-on.

## Controls (≥2 · a_break_the_wall)
- **M** = g-tension curriculum.
- **C1** = flat/shuffled order (내용 byte-동일·동일 seed/budget floor).
- **C2** = permuted-score (동일 가중 multiset을 무작위 재배정 — "비균등 가중이면 아무거나 도움"을 kill).

## Falsify
M의 ρ·weave/G1 Δ ≤ max(C1,C2) OR held-out F2(M) ≤ F2(C1) ⟹ 커리큘럼형도 무신호 → engine-active 학습 계열 전체 종결(objective형 이미 DOA + 커리큘럼형 KILL). EN positive = SCREENER/DIRECTIONAL(형태소+base+carrier 동시이동) · TERMINAL은 303M engine-native + scale-bounded. 음성도 결과.

## 🧱 발사 블로커 / 상태
- objective형: **KILL 기록 완료**(위 basin-preserving 사유). 재발사 금지.
- 커리큘럼형: 구현 필요 — `cli/corpus.py`에 `--order g-tension --score-ckpt` 레버 추가(a_experiment_engine_native) → 303M 3-arm{M,C1,C2} fire(pool·EN-first). fire 인프라 = pool 또는 vast(과거 ghost SSH publickey 블로커 주의).

## Divergence 보고 (a_lab_full_diverge · a_parallel_session_compare)
- **AGREES**: objective축 walled(H_9131/9120)·크랙은 데이터축(H_9267/9288) = 기존 SSOT와 일치.
- **NOVEL**: engine_g의 스칼라 게이트를 "분해기 실격 → 샘플 점수기 적격"으로 재사용 = 미시도(loss가 아닌 curriculum에서 엔진 능동참여).
- **Fable 자기반증**: 1R "G decomposes backward"는 engine_g가 가진 적 없는 메커니즘 가정 → 2R가 반증, 방어 않고 뒤집음. Sol=Codex버전에러 부재 → Fable 단독 DIRECTIONAL(2R 일관).
