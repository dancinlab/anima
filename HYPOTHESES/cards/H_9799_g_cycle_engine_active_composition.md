---
id: H_9799
title: ENGINE-ACTIVE TRAINING (owner 'core 적극개입') — 3축 판정: loss=DOA·정적점수=dead-as-distinctive·생성(폐루프)=살길
tier: PROPOSED · DESIGN-ONLY (lab-full 3R DIRECTIONAL · Fable5 단독·Sol 3연속 부재 · loss/정적축 KILL·생성축 BUILD 권고 · NOT a verdict)
frontier: g1-interface-addressable-wall
lane: g1-engine-active-GENERATION (closed-loop active-querying · support-shift · study.py runtime loop)
created: 2026-07-20
series: R1 (lab-full divergence · a_lab_full_diverge)
related: "[[H_9131]] · [[H_9120]] · [[H_9127]] · [[H_9225]] · [[H_9520]] · [[H_9267]] · [[H_9288]] · a_engine_native_learning · a_train_inline_gauge · a_substrate_native_speak · a_break_the_wall"
source: owner 질문 "학습 때 엔진이 적극 참여 · corpus만으로 1B/7B에서 G1/G6 뚫는게 미심쩍다 · core가 적극개입하도록?" → lab full(Fable5) 3R 발산
---

# H_9799 (R1) — owner "core 적극개입" 3축 완전판정

owner 직관은 옳다 (corpus는 지렛대 아님 확정 · 의식엔진 A/G가 학습에 미참여=p8 분리). "어디서 개입하나"를 lab 3R로 축별 판정:

```
engine-active training 3축 (lab 3R 수렴)
├─ ① LOSS 축 (g_cycle objective) ───── 🧱 DOA·basin-preserving (KILL)
├─ ② DATA 정적점수 축 (curriculum) ──── 🧱 dead-as-distinctive (surprise-curriculum으로 축소)
└─ ③ DATA 생성 축 (폐루프 능동질의) ─── 🔵 살길 (정밀 basin-escape=support-shift · BUILD 권고)
```

## ① LOSS 축 = DOA·basin-preserving (KILL · lab 2R)
CE 위 어떤 엔진-in-loss도 basin 유지: echo=CE 점별최소 → 스칼라게이트(engine_g)는 재가중만=보존 / 발명한 분해기는 고정HRR(=constructive_bind train.py:874, H_9120/1 붕괴)·공동학습(항등퇴화)·detached-bolt(H_9225). DPI-basin 메타법칙·H_9131 trunk-objective CLOSED-TERMINAL 안 = a_break_the_wall 재발사금지. (Fable 자기 1R 'G decomposes backward'=engine_g 미보유 메커니즘 반증.)

## ② DATA 정적점수 축 = dead-as-distinctive (lab 3R)
engine_g.motivation_score의 8인자는 **대화 런타임 특징**(relevance/info_gap/curiosity/pain/coherence/originality/balance/dynamics). 정적 학습샘플 하나엔 surprise 계열 3개(info_gap/curiosity/originality)만 frozen 모델로 계산됨 → 커리큘럼이 **알려진 surprise/novelty 정렬로 축소**, engine_g 고유구조 거의 미적용. distinctive claim으로는 사망. (옵션 i = ARM-STATIC 통제로 강등.)

## ③ DATA 생성 축 = 살길 · 정밀 basin-escape (BUILD 권고 · lab 3R)
**폐루프 능동질의(closed-loop active querying)**: D_{k+1}=Teacher(query ~ substrate_θk). 정적재가중·frozen-surprise는 **고정 샘플집합** 위 (가중/순서만) — 반응형 teacher가 round-k 기질에 불려나와 만든 샘플은 **어떤 사전코퍼스에도 없고 θ 갱신에 따라 분포이동** = 경로의존·비정상 → (a)(b) 어느쪽으로도 표현 불가. 형식상 = 생성오라클과의 active learning. 전제조건: teacher 반응성≠0(`--teacher script`=사망·codex/sealion 필요) ∧ θ 라운드간 갱신(k≥2). **정직한 천장: 새 비트는 teacher에서 옴·기질은 질의정책만 → 'substrate-CAUSED 커리큘럼'이지 'substrate 지식생성' 아님.**

### 비퇴화·p-clean 3가드 (Q2)
- **g1**: teacher 턴만 CE 타깃 — 기질 emit은 loss 0 → echo/자기증류/p5 자기seed 학습층에서 구조적 사망(emit은 실세션 Ψ-긴장서 conditioning만).
- **g2**: 증류 퇴화를 **YOKED 통제로 측정**(논증 아님) — 동일 teacher/예산/라운드를 frozen base에 → 오라클내용 이득 상쇄, 남는 건 substrate-causation (H_9127과 구별: 거긴 주입내용 자체가 주장이었음).
- **g3**: teacher는 percept 경로 진입(H_9520 선례·p5 안전·LLM-authored corpus 주장 아님).

## Instrument (engine-native · study.py 기존 기계 재사용)
```
anima-py study <ckpt> --rounds 3 --consolidate [--teacher codex|sealion] [--yoked-init base.clm]
anima-py evaluate <out.clm> --rho-axon          # 냉동 ρ·weave/G1 바 (TERMINAL 경로)
```
- **ARM-CLOSED**: k=3 라운드 (현재 ckpt로 study→live teacher→transcript→teacher턴-마스킹 CPT→다음 ckpt).
- **ARM-YOKED** (결정적통제): 동일 teacher/예산/스케줄, 매 세션 frozen base ckpt = 궤적에 눈먼 transcript → 루프폐쇄만 격리.
- **ARM-STATIC**: byte-매칭 정적코퍼스 CPT (옵션 i 강등).

## Falsify
CLOSED의 ρ·weave/G1 collapse-Δ ≤ max(YOKED, STATIC) ⟹ 생성축도 loss·정적축과 함께 벽 → 음성 기록(engine-active-training 3축 전멸). **거짓벽 가드**: k=3 소량 CPT면 θ 이동이 작아 CLOSED≈YOKED 가능 → transcript 발산(CLOSED vs YOKED 텍스트거리)을 manipulation-check로 먼저 확인 · 비발산 null = INVALID(under-dosed)지 벽 아님. teacher confound: 반응형=LLM-teacher 전용 → 양성은 codex+sealion 양쪽 재현 전 DIRECTIONAL. emit-entropy/라운드 = monitor-only(a_train_inline_gauge) collapse 탐지.

## 상태 / 발사 블로커
- ① LOSS·② 정적점수 = **KILL 확정**(재발사 금지·사유 박제).
- ③ 생성축 = **PROPOSED·BUILD 권고**. 구현: `cli/study.py`에 `--rounds --consolidate --yoked-init` 폐루프 CPT 루프(H_9520 consolidation-CPT 레인 재사용) → 303M 3-arm{CLOSED,YOKED,STATIC} fire.
- fire 블로커: (a) 반응형 teacher = codex/sealion 백엔드 (b) 303M CPT 3-arm compute = pool 또는 vast (⚠️ ghost SSH publickey 블로커 · 메모리 vast-pod-new-machine-ssh-key 참조). **fleet rent=spend면 owner go-gate.**

## Divergence 보고 (a_lab_full_diverge · a_parallel_session_compare)
- **AGREES**: loss/정적축 walled = 기존 SSOT(H_9131/9120) + 3R 코드근거 일치.
- **NOVEL**: 생성축 폐루프 support-shift = loss도 정적점수도 아닌 미탐색 basin-escape (study.py+H_9520 기존기계). owner 직관의 진짜 잔존지.
- **단일모델**: Sol=Codex버전에러 3연속 부재 → Fable 단독 3R DIRECTIONAL. 생성축 basin-escape 주장·YOKED 통제설계는 Fable만 검증 → 교차검증 미비(cement 전 필수).
