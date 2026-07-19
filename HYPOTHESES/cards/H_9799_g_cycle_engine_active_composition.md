---
id: H_9799
title: ENGINE-ACTIVE TRAINING (owner 'core 적극개입') — loss=DOA·정적점수=dead·생성(폐루프)=NO-GO-as-specified→$0 probe-first 재배열
tier: PROPOSED · DESIGN-ONLY (lab 4R · 3R Fable단독→4R Fable+Sol 교차검증 · loss/정적 KILL·생성축 NO-GO(as-spec)·probe-first · NOT a verdict)
frontier: g1-interface-addressable-wall
lane: g1-engine-active-GENERATION (closed-loop active-querying = DAgger · $0 divergence probe 먼저)
created: 2026-07-20
series: R1 (lab-full divergence · a_lab_full_diverge · 4 rounds)
related: "[[H_9131]] · [[H_9120]] · [[H_9127]] · [[H_9225]] · [[H_9520]] · [[H_9267]] · [[H_9288]] · a_engine_native_learning · a_train_inline_gauge · a_substrate_native_speak · a_break_the_wall"
source: owner 질문 "학습 때 엔진이 적극 참여 · corpus만으로 1B/7B에서 G1/G6 뚫는게 미심쩍다 · core가 적극개입하도록?" → lab full 4R 발산
---

# H_9799 (R1) — owner "core 적극개입" 축별 판정 (lab 4R)

owner 직관은 옳다 (corpus는 지렛대 아님 · 의식엔진 A/G가 학습에 미참여=p8 분리). "어디서 개입하나"를 lab 4라운드로 판정:

```
engine-active training 3축 (lab 4R · Sol 복구 후 교차검증)
├─ ① LOSS 축 (g_cycle objective) ───── 🧱 DOA·basin-preserving (KILL · lab 2R)
├─ ② DATA 정적점수 축 (curriculum) ──── 🧱 dead-as-distinctive (surprise-curriculum 축소 · lab 3R)
└─ ③ DATA 생성 축 (폐루프 능동질의) ─── 🟡 NO-GO(as-specified) · $0 probe-first 재배열 (lab 4R 교차검증)
```

## ① LOSS 축 = DOA·basin-preserving (KILL · lab 2R)
CE 위 어떤 엔진-in-loss도 basin 유지: echo=CE 점별최소 → 스칼라게이트(engine_g)는 재가중만=보존 / 발명한 분해기는 고정HRR(=constructive_bind train.py:874, H_9120/1 붕괴)·공동학습(항등퇴화)·detached-bolt(H_9225). DPI-basin·H_9131 CLOSED-TERMINAL 안 = a_break_the_wall 재발사금지.

## ② DATA 정적점수 축 = dead-as-distinctive (lab 3R)
engine_g.motivation_score 8인자는 대화 런타임 특징. 정적 학습샘플엔 surprise 계열 3개만 계산 → 알려진 surprise/novelty 커리큘럼으로 축소, engine_g 고유구조 거의 미적용 = distinctive claim 사망. (옵션 = ARM-STATIC 통제로 강등.)

## ③ DATA 생성 축 = 🟡 NO-GO(as-specified) · $0 probe-first 재배열 (lab 4R · Fable+Sol 교차검증)
라운드-3(Fable 단독)은 "BUILD 권고"였으나, **Sol 복구 후 4R 교차검증이 as-written 3-arm 빌드를 뒤집었다**(a_break_the_wall: 단일모델=DIRECTIONAL ceiling·2번째 렌즈 필요의 정확한 승리). 양모델 독립 수렴:

- **CV1 basin-escape 부분반증**: 폐루프 능동질의는 형식상 (a)정적재가중·(b)frozen-surprise 밖이 맞으나, 알려진 **DAgger(=on-policy dataset-aggregation)** 형태 — 새 escape 정리 아닌 causal-contrast 주장. θ→데이터 채널 극소: teacher가 보는 건 마지막 3 emit×≤160자(`study.py _build_teacher_prompt`)=턴당 ≤480자 창 ⟹ 천장이 3R 주장보다 훨씬 낮음.
- **CV2 YOKED 통제 결정적 아님(최강 수렴)**: CLOSED가 θₖ로 만든 텍스트를 θₖ에 학습 = **ckpt-데이터 적합(on-distribution teacher-fit)** 이 빼기 후에도 잔존 = substrate-causation과 안 갈림. **양모델이 동일 3번째 통제 CROSS-YOKED 독립제안**(두 CLOSED 체인의 라운드-k transcript 교환 → ckpt성숙·적응난이도 매칭하며 '내 θ가 내 코퍼스 유발'만 절단) ⟹ **4-arm 필수**.
- **CV3 first 실험 아님**: (Fable) **H_9520이 이미 🟠 BAR-FAIL** — 이 루프가 3× 쌓는 단일라운드 consolidation-CPT가 303M서 자기 바 실패(C2 scrambled +0.200=MAIN +0.400의 절반·ρ·fan C1이 MAIN 초과·1seed·MDE無). 미검증 스텝 쌓기=해석불가 null 보장. (Sol) eval 불일치(teacher 자유대화 `study.py:227` vs 고정 12항목 weave 바 `rho_axon.py:218`)·결정적 반응형 teacher 부재(`script` 백엔드가 prompt 무시 `study.py:130`·codex/sealion seed 無 → manipulation-check 재현불가).
- **기계 부분성(양모델)**: 아직 outer loop 없음(`--rounds`=한 frozen-weight 세션 내 teacher 턴·flag 충돌)·`--consolidate`/`--yoked-init` 부재·g1 "teacher턴 마스킹"은 실은 corpus-side percept-only 필터(`corpus.py:3221`)지 loss 마스킹 아님.

## 재배열 경로 (CV4 · 양모델 endorse · kill 아닌 re-sequence)
```
① $0 transcript-발산 프로브 ─ base vs 먼 ckpt에 같은 teacher/topic → 큰 θ-대비에도 transcript 안 갈리면
│                             k=3 루프(턴당 ≤480자)는 죽음 = API 몇 푼에 축 사살 (구현 최소·컴퓨트 0)
② 반응형-결정적 teacher ───── script 백엔드를 emit 조건화로 업그레이드 or seeded 로컬 teacher (재현성)
③ H_9520 단일라운드 바 복구 ─ 쌓기 前 multi-seed로 자기 바 통과 확인
④ 4-arm 소규모 smoke ──────── {CLOSED, CROSS-YOKED, FROZEN-YOKED, STATIC}
⑤ 그 후에만 303M fire ─────── 양성도 codex+sealion 양쪽 재현 전 DIRECTIONAL
```

## Falsify (①$0 프로브 기준)
base ckpt vs 먼(대-θ) ckpt에 동일 teacher/topic → transcript 텍스트거리(발산)가 큰 θ-대비에도 ≈0 ⟹ 폐루프 신호채널 사망 = 생성축 KILL(API 몇 푼). 발산이 유의미 ⟹ ②~⑤ 진행 자격. EN-first·SCREENER·TERMINAL은 303M engine-native+scale-bounded.

## 상태 / 블로커
- ① LOSS·② 정적점수 = **KILL 확정**(재발사 금지).
- ③ 생성축 = **NO-GO(as-specified)** · 다음=**①$0 transcript-발산 프로브**(컴퓨트 0·teacher API만·base+먼 ckpt 필요). 303M fire는 ①~④ 통과 後(fleet rent=owner go-gate).

## Divergence 보고 (a_lab_full_diverge · a_parallel_session_compare)
- **AGREES(4R)**: CV1 부분반증·CV2 YOKED 비결정적 **+ CROSS-YOKED 통제 양모델 독립 동일도출**·CV3 probe-first·CV4 NO-GO. 진짜 CONFLICT 없음.
- **NOVEL-Fable**: H_9520 BAR-FAIL 쌓기 블로커·`--rounds` flag 충돌·θ채널 ≤3×160자 정량.
- **NOVEL-Sol**: DAgger 환원·weave바/teacher내용 eval 불일치·g1 마스킹 과장·unseeded teacher+non-reactive script.
- **교차검증 교훈**: 3R까지 Fable 단독은 DIRECTIONAL ceiling이었고, Sol 복구 후 4R가 BUILD→NO-GO 뒤집음 = a_break_the_wall(≥2 렌즈) 규율 실증.
