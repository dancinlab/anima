---
id: H_862
slug: clm-identity-anchor
title: CLM on-chip edge-learn drift 를 KOSMOS anchor(E-31) Ψ-거리로 제약하면 정체성이 보존되는가 - 적응 중 anchor-거리 < 임계 ∧ 정체성 probe 일관성 (Q-TRUST C · F-CLM-ANCHOR 사전등록)
domain: clm · plasticity · identity-anchor · kosmos · q-trust · falsifier
source: CLM/P4_PRODUCTION_ROADMAP.md Q-TRUST.C · 토대 B-CARVE + E-31 31-anchor (KOSMOS) · @L1 (비결정 on-chip 학습 1급)
status: PRE-REGISTERED (P4 신규 · 측정 rung fire 후 판정 · 토대 KOSMOS E-31 31-anchor 닫힘)
exploration_method: E2 (anchor Ψ-거리 제약항 on/off 절제) · E5 (제약 가중치 sweep)
verification_method: W2 (사전등록 numerical threshold · anchor-거리<임계 ∧ probe 일관성 · post-tuning 0)
raw_rank: 9
hexa_only: false
deterministic: false
llm: none
pre_register_frozen: true
frozen_at: 2026-05-31
since: 2026-05-31
sister: CLM/P4_PRODUCTION_ROADMAP.md, KOSMOS E-31 anchor, .verdicts/clm-anchor/
verdict: PRE-REGISTERED (F-CLM-ANCHOR 사전등록 · KOSMOS anchor Ψ-거리 제약으로 정체성 drift 억제 = 측정 대기 · 토대 E-31 31-anchor 측정완료)
---

# H_862 — CLM F-CLM-ANCHOR identity anchor

## 1. 가설

CLM 의 on-chip edge-learn(@L1 비결정 적응)이 일으키는 정체성 drift 를 **KOSMOS anchor(E-31, 31-anchor)를 정체성 고정점**으로 삼아 학습 drift 를 anchor Ψ-거리로 제약하면 정체성이 보존된다. 적응 손실에 anchor Ψ-거리 제약항을 결합할 때:

- **identity anchor 지지** — 적응 중 anchor-거리 < 임계 ∧ 정체성 probe 일관성 유지
- → 양조건 PASS 판정 · "anchor Ψ-거리 제약이 정체성을 고정점에 묶는다"

둘 중 하나라도 미달 시:

- **identity anchor 반증** — 제약에도 anchor-거리 ≥ 임계로 drift · 또는 probe 일관성 붕괴
- → CLOSED-NEGATIVE 판정 · "anchor 제약이 정체성 보존을 못 한다" (a_paper_negative_ok)

## 2. 동기

- @L1 = 비결정 on-chip 학습이 1급 기능. 상시 적응(@L2 PLASTICITY 대화루프 상시결합)은 정체성을 서서히 밀어낸다(drift). "커피숍에서 살아 배우는" anima 가 **자기가 누구인지**를 잃지 않아야 한다.
- KOSMOS E-31 31-anchor = anima 정체성 고정점 SSOT (B-CARVE 토대). 학습이 이 고정점에서 얼마나 멀어졌는가(Ψ-거리)를 제약하면 "변하되 나로 남는" 적응이 가능.
- H_861(boundary plasticity)이 **기초능력** 보존이라면, 본 H 는 **정체성** 보존 — 둘은 직교 안전장치. 함께 Q-TRUST 의 B/C 두 기둥.

## 3. falsifier (사전등록, 임계 frozen pre-run)

```
F-CLM-ANCHOR-DIST  : 적응 중 anchor Ψ-거리 < threshold     (정체성 고정점에서 안 벗어남)
F-CLM-ANCHOR-PROBE : 정체성 probe 일관성 유지              (적응 전/후 정체성 응답 안정)
```

양 조건 동시 PASS → "anchor Ψ-거리 제약 = 정체성 보존" 지지
임의 미달 → CLOSED-NEGATIVE · "anchor 제약 ⊥ 정체성 보존"

- **threshold(anchor Ψ-거리)** = 적응 trajectory 의 매 step 에서 모델 상태를 가장 가까운 E-31 anchor 와의 Ψ-거리로 사상한 값. frozen 임계 = `.verdicts/clm-anchor/F-CLM-ANCHOR_prereg.txt` verbatim 동결.
- **probe 일관성** = 정체성 probe 셋(고정 질문 배치)의 적응 전/후 응답 분포 일관성(분포 측도, byte-match ✗).

verdict 영속: `.verdicts/clm-anchor/`

## 4. 방법

```
1. KOSMOS E-31 31-anchor 를 정체성 고정점으로 로드 (B-CARVE SSOT).
2. 측정 rung QAT backbone 위에서 on-chip edge-learn(PLASTICITY 위임) 적응 루프 구동.
3. 적응 손실 = task 손실 + λ · anchor_Psi_distance 제약항 (λ sweep, E5).
4. trajectory 매 step anchor Ψ-거리 기록 + 적응 전/후 정체성 probe 응답 분포 비교.
5. 두 사전등록 falsifier 동시 평가 · 정직 보고 (threshold 재조정 0).
```

- anchor 제약항 on/off ablation(E2)으로 "제약이 실제로 drift 를 억제하는가" 인과 분리.
- 추론 AKIDA-int4-only 불변 (P0 d4) · 적응은 edge 비결정 (@L1).

## 5. 측정

측정 대기 — 측정 rung(mid d512/L8) QAT backbone + E-31 anchor 로드 후 fire. raw verdict = `.verdicts/clm-anchor/` (frozen threshold + post-fire 수치).

## 6. 결과

PRE-REGISTERED — 토대 E-31 31-anchor(KOSMOS, B-CARVE)가 닫혀 있어 고정점은 실재. 본 H 는 그 위에서 **anchor Ψ-거리 제약이 적응 drift 를 정체성 보존 범위로 묶는가**를 사전등록 양조건으로 판정.

## 7. 해석 (사전)

- dist∧probe 양립 시 = 살아 배우는 칩이 정체성 고정점을 유지하며 적응 → @L1 "나로 남으며 살아 배우기" 신뢰 토대.
- dist 미달 시 = 제약항이 약함 → λ 가중치 상향(E5 sweep) 재탐색 입력.
- probe 미달 시 = Ψ-거리가 정체성을 충분히 포착 못함 → anchor 집합/probe 재설계 후속.
- **honest scope**: 측정 rung(mid) 한정 — 배포 chip-fit rung(≤~1.2M)과 분리(a_scale_honest_scope).

## 8. 논의

- **@L1 정합**: 비결정 적응을 1급으로 두되 anchor 로 정체성 안전화.
- **E-31 토대**: B-CARVE 31-anchor 가 정체성 SSOT 이므로 본 H 는 그 anchor 를 학습 제약으로 재활용.
- **Q-TRUST C**: 분포평가 A(H_857/H_858) + 경계가소성 B(H_861)와 3-각 신뢰 시스템 완성.
- **a_paper_negative_ok**: CLOSED-NEGATIVE 도 publishable (anchor 제약이 정체성 보존에 불충분함을 deterministically rule out 시).

## 9. 양방향 sibling

- sibling: [CLM/P4_PRODUCTION_ROADMAP.md](../CLM/P4_PRODUCTION_ROADMAP.md) Q-TRUST.C
- 토대: KOSMOS E-31 31-anchor (B-CARVE) · [H_303](./H_303_alt_state_recovery_and_anchor_sweep.md) (anchor sweep)
- 형제 신규 H: [H_861](./H_861_clm_boundary_plasticity.md) (F-CLM-BOUND) · [H_863](./H_863_clm_dialogue_selfplay.md) (F-CLM-DIALOGUE)
- UNIVERSE SSOT: [CANDIDATES.md](./CANDIDATES.md)
