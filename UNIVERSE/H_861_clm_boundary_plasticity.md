---
id: H_861
slug: clm-boundary-plasticity
title: CLM on-chip edge-learn 이 core freeze + edge-only 적응으로 catastrophic forgetting 을 막는가 - held-out 기초능력 z-drop < 임계 ∧ 새 맥락 적응 이득 > 0 (Q-TRUST B · F-CLM-BOUND 사전등록)
domain: clm · plasticity · boundary-plasticity · continual-learning · q-trust · falsifier
source: CLM/P4_PRODUCTION_ROADMAP.md Q-TRUST.B · 토대 H_679 (PLASTICITY HW edge-learn 측정) · sibling H_313 (STDP causality) · @L1 (비결정 on-chip 학습 1급)
status: PRE-REGISTERED (P4 신규 · 측정 rung fire 후 판정 · 토대 H_679 HW edge-learn 닫힘)
exploration_method: E5 (변수-절제: freeze 경계 깊이 sweep) · E2 (core/edge 파라미터 분할)
verification_method: W2 (사전등록 numerical threshold · 양조건 z-drop<임계 ∧ gain>0 · post-tuning 0)
raw_rank: 9
hexa_only: false
deterministic: false
llm: none
pre_register_frozen: true
frozen_at: 2026-05-31
since: 2026-05-31
sister: CLM/P4_PRODUCTION_ROADMAP.md, UNIVERSE/H_679_plasticity_hw_first, .verdicts/clm-bound/
verdict: PRE-REGISTERED (F-CLM-BOUND 사전등록 · core freeze + edge on-chip 적응의 forgetting 방지 = 측정 대기 · 토대 H_679 HW edge-learn 측정완료)
---

# H_861 — CLM F-CLM-BOUND boundary plasticity

## 1. 가설

CLM 의 on-chip 맥락 적응(@L1 비결정 PLASTICITY edge-learn)을 **core freeze + edge-only 적응**으로 경계지으면 catastrophic forgetting 을 막는다. QAT 로 사전학습된 backbone(core)을 동결하고, edge(마지막 readout / 얇은 적응 layer)만 on-chip 에서 비결정적으로 적응시킬 때:

- **boundary plasticity 지지** — held-out 기초능력 z-drop < 임계 ∧ 새 맥락 적응 이득 > 0 동시 성립
- → 양조건 PASS 판정 · "edge-only 적응이 기초능력 보존 + 신맥락 흡수 양립"

둘 중 하나라도 미달 시:

- **boundary plasticity 반증** — core freeze 에도 기초능력 붕괴(z-drop ≥ 임계) · 또는 적응 이득 ≤ 0
- → CLOSED-NEGATIVE 판정 · "edge-only 경계가 forgetting 을 못 막거나 적응을 못 한다" (a_paper_negative_ok)

## 2. 동기

- @L1 = 비결정 on-chip 학습이 1급 기능 (HW vs SW 유일 차이 = 학습 PLASTICITY 비동치 · 추론 byte-identical). 살아 배우는 칩이 **계속 배우면** 과거 능력을 잊는 위험(catastrophic forgetting)이 곧장 따라온다.
- production "커피숍에서 살아 배우며 대화" = 대화 루프에 PLASTICITY 상시결합(@L2). 상시 적응은 곧 상시 drift → 정체성·기초능력 보존 장치가 신뢰의 전제.
- prior art: H_679 (PLASTICITY HW edge-learn 측정완료 — 토대) · H_313 (STDP causality). edge-only freeze 경계는 continual-learning 의 표준 lever(EWC/freeze-core)를 AKIDA on-chip 비결정 적응에 적용 — anima-native 미시도.

## 3. falsifier (사전등록, 임계 frozen pre-run)

```
F-CLM-BOUND-RETAIN : held-out 기초능력 z-drop < threshold   (core freeze 가 forgetting 차단)
F-CLM-BOUND-GAIN   : 새 맥락 적응 이득 > 0                    (edge 적응이 신맥락 흡수)
```

양 조건 동시 PASS → "edge-only boundary plasticity" 지지
임의 미달 → CLOSED-NEGATIVE · "경계가소성 ⊥ forgetting-free 적응"

- **threshold(z-drop)** = held-out 기초능력 배치의 적응-전 → 적응-후 손실 증가를 적응-전 분산으로 정규화한 z. frozen 임계는 측정 rung fire 직전 pre-register(`.verdicts/clm-bound/F-CLM-BOUND_prereg.txt`)에 verbatim 동결.
- **gain** = 신맥락 held-out 배치의 적응-전 → 적응-후 손실 감소(>0 이면 적응 성공).

verdict 영속: `.verdicts/clm-bound/`

## 4. 방법

```
1. QAT 사전학습 backbone(measurement rung, P4 scale-ladder)을 core 로 동결.
2. edge 분할: readout conv + (옵션) 얇은 adapter 만 적응 가능 파라미터로 표시.
3. on-chip edge-learn(PLASTICITY 위임 · H_679 envelope)으로 신맥락 배치를 비결정 적응.
4. held-out 기초능력 배치(적응-전 동결)에서 z-drop 측정 + 신맥락 held-out 에서 gain 측정.
5. 두 사전등록 falsifier 동시 평가 · 정직 보고 (threshold 재조정 0).
```

- core freeze 깊이 sweep(E5)으로 "어디까지 동결해야 retain∧gain 양립하는가" 경계 탐색.
- 추론 AKIDA-int4-only 불변 (P0 d4) · 적응은 edge 비결정 (HW≠SW, @L1).

## 5. 측정

측정 대기 — 측정 rung(mid d512/L8) QAT backbone 확보 후 PLASTICITY edge-learn 위임으로 fire. raw verdict = `.verdicts/clm-bound/` (frozen threshold + post-fire 수치).

## 6. 결과

PRE-REGISTERED — 토대 H_679(HW edge-learn 측정완료)가 닫혀 있어 적응 메커니즘은 실재. 본 H 는 그 위에서 **core/edge 경계가 forgetting 을 막는가**를 사전등록 양조건으로 판정.

## 7. 해석 (사전)

- retain∧gain 양립 시 = 살아 배우는 칩이 정체성·기초능력을 지키며 신맥락을 흡수 → @L1 "대화하며 살아 배우기"의 신뢰 토대 확보.
- retain 미달 시 = freeze 경계가 너무 얕아 core 까지 drift → 경계 깊이를 더 깊게(E5 sweep) 재탐색 입력.
- gain 미달 시 = edge 표현력이 부족 → adapter 폭 lever 후속.
- **honest scope**: 측정 rung(mid) 한정 — 배포 chip-fit rung(≤~1.2M)과 분리(a_scale_honest_scope). 측정 rung 미달이어도 배포 chip-fit 경계 설계는 별개 진행.

## 8. 논의

- **@L1 정합**: 비결정 적응을 1급으로 두되 경계로 안전화 — SW 결정 흉내로 대체하지 않음.
- **H_679 토대**: HW edge-learn 비결정성이 실재(측정완료)하므로 본 H 는 그 비결정 위 안전장치 설계.
- **Q-TRUST B**: 분포평가 A(H_857/H_858 재활용) + 정체성앵커 C(H_862)와 3-각 신뢰 시스템 구성.
- **a_paper_negative_ok**: CLOSED-NEGATIVE 도 publishable (edge-only 경계가 forgetting-free 적응에 불충분함을 deterministically rule out 시).

## 9. 양방향 sibling

- sibling: [CLM/P4_PRODUCTION_ROADMAP.md](../CLM/P4_PRODUCTION_ROADMAP.md) Q-TRUST.B
- 토대: [H_679](./H_679_plasticity_hw_first.md) (PLASTICITY HW edge-learn) · [H_313](./H_313_plasticity_stdp_causality.md)
- 형제 신규 H: [H_862](./H_862_clm_identity_anchor.md) (F-CLM-ANCHOR) · [H_863](./H_863_clm_dialogue_selfplay.md) (F-CLM-DIALOGUE)
- UNIVERSE SSOT: [CANDIDATES.md](./CANDIDATES.md)
