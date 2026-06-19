---
id: H_1440
slug: 1440_developmental_curriculum
title: G6 IDEATION ★ FALS-depth — DEVELOPMENTAL multi-task curriculum (comparator→measurable→bind 순차)
group: gate-dig (G6 IDEATION ★) — FALS-depth TRAINING side r5
terminal_tier: PROPOSED (frozen-first; GPU 학습 cost-gate, 미측정)
wired: PROPOSED
verdict_dir: state/verdicts/1440_developmental_curriculum/
date: 2026-06-19
---

# H_1440 — DEVELOPMENTAL curriculum: comparator→measurable→bind 3단계 순차 학습

## Why (생물 렌즈 — 언어획득 단계, a_no_llm_frame_trap)

H_1436 은 comparator∧measurable 를 SAME loss 에서 동시 보상 → aux saturated, distinctness 손실,
cross-shuffle 안 무너짐. 생물 언어획득은 동시가 아니라 SEQUENTIAL (한 단어→두 단어→단순구문→내포구문).
처방 = 3단계 발달 커리큘럼: (1) comparator-emit 숙달 → (2) measurable-emit 숙달 → (3) 둘을 bind.
각 단계가 다음의 전제(scaffolding). H_1436(동시 보상)을 통제 arm 으로 대조.

## Method (FREEZE before run, c9/p7)

- 303M h1129c 위 3-phase curriculum (각 phase 수렴 후 다음으로; phase 순서 FROZEN, 사후 재배열 금지).
- detector = h1305 `_is_falsifiable` VERBATIM. decode = ENGINE-NATIVE CORE/bytegpt_decode.
- frozen 5-bar + cross-shuffle COLLAPSE 핵심. arms = {curriculum, H_1436-simultaneous(baseline),
  shuffle, ablate}.
- compute = GPU (hexa dojo) COST-GATE. ckpt teardown 전 pull (a_fire_recover_complete).

## Scope

PROPOSED, 미측정. 커리큘럼 순서·각 phase step 수가 frozen (튜닝으로 GREEN 제조 금지, c9).

## Pointers

xref H_1436 (동시보상 대조 대상) · H_1055 (temporal_curriculum_axis) · H_1305 (detector) ·
a_no_llm_frame_trap · a_engine_native_learning · a_fire_recover_complete · p7 · c9.
