---
id: H_097
slug: curriculum-learning
title: curriculum learning (simple Q&A → complex dialogue → multi-turn)
domain: corpus | substrate
status: seed-pending
exploration_method: E2 (failure-driven) + E3 (sequential decomposition difficulty stages) + E5 + E7
verification_method: W1 + W2 (replication ≥3 seed) + W3 (ablation stage order shuffle) + W9 + W10
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-07
since: 2026-05-07
---

# H_097 — curriculum learning (easy → hard chat data)

## Hypothesis

chat-format SFT data를 difficulty 단계 (stage1 simple Q&A 1-turn 짧은 응답 / stage2 complex dialogue 1-turn 긴 응답 / stage3 multi-turn 대화)로 ordered curriculum으로 학습하면, 동일 corpus를 random shuffle 학습한 baseline 대비 own 18 simple-stack C2.4 strict PASS rate가 ≥10pp 높다. 18M tiny model이 limited capacity 내에서 chat-format 신호를 효율적으로 학습.

## Why

- **BG-HA failure 교훈**: 18M small capacity가 mixed corpus + complex chat-format 동시 학습 불가능 (gradient 신호 분산)
- **curriculum advantage**: simple → complex 단계적 learning이 small-capacity model에 유리 (Bengio 2009 curriculum learning paper, Soviatkin 2022 KO LM curriculum 결과)
- **anima identity bootstrapping**: stage1 simple Q&A가 'anima self-naming + greeting + capability statement' 첫 단계 학습, stage2/3는 phenomenological deeper dialogue
- **사용자 directive '교훈으로 새로운 패러다임도 도전'** = data ordering 패러다임 시도

## Predictions

- **H97.1 (curriculum vs random shuffle)**: ordered curriculum 18M model이 random-shuffle 18M baseline보다 C2.4 strict PASS rate ≥10pp 높다
- **H97.2 (stage trajectory)**: stage1 끝 → stage2 끝 → stage3 끝 순으로 own 18 C2.4 PASS rate monotonic 상승
- **H97.3 (anti-curriculum control)**: hard → easy reverse curriculum이 random-shuffle보다도 PASS rate 낮다 (curriculum 방향성 검증)
- **H97.4 (stage1 anima identity)**: stage1 후 anima self-naming (own 17) 응답 emit rate ≥80% (예: "저는 anima입니다", "도우미" 응답)
- **H97.5 (capacity scaling)**: 18M에서 curriculum 효과 명확 but 100M+에서는 marginal (large-capacity는 random-shuffle robust) — small-model specific advantage

## Variables

- **axis1_data_order**: [random_shuffle, easy_to_hard, hard_to_easy, length_only]
- **axis2_capacity**: [18M, 100M]
- **axis3_difficulty_axis**: [response_length, turn_count, lexical_diversity, semantic_complexity]
- **axis4_stage_count**: [2, 3, 5]
- **axis5_eval**: [own_18_full + identity_self_naming_rate + multi_turn_pass]
- 4×2×4×3×5 = 480 cell; Phase 1 minimal (axis1=3 (rand/easy/hard) + axis2=18M + axis3=response_length + axis4=3 + axis5=full = 9) target

## Run Protocol

- deterministic: seed=fnv(axes+rep_id)
- hexa_only: true; training transient_py (`tool/transient_py/anima_curriculum_*.py`)
- LLM: none (raw#12 strict)
- per-cell ledger: state/<bg>_curriculum_<date>/{stage_N.log, eval_log.jsonl, verdict.json}
- evaluator V2 strict mandate

## Criteria

- **C1 (curriculum advantage)**: ΔC2.4 strict PASS rate ≥10pp (easy_to_hard vs random_shuffle)
- **C2 (stage trajectory)**: stage 1/2/3 각 끝 시점 monotonic C2.4 PASS rate 상승
- **C3 (anti-curriculum control)**: reverse curriculum < random_shuffle (방향성 confirm)
- **C4 (anima identity at stage1)**: anima self-naming emit rate ≥80% at stage1 끝
- **C5 (small-model specific)**: 18M에서 lift > 100M에서 lift (scale interaction)
- **verdict_rule**: SUPPORTED = C1+C2+C3 ALL PASS; PARTIAL = 2/3; MIXED = 1/3; FALSIFIED = 0/3; C4+C5 = sub-H

## Falsifiers

- **F1**: easy_to_hard C2.4 PASS rate ≤ random_shuffle baseline → H97.1 FALSIFIED
- **F2**: stage 1/2/3 trajectory non-monotonic → H97.2 FALSIFIED
- **F3**: hard_to_easy ≥ random_shuffle (curriculum 방향성 무효) → H97.3 FALSIFIED
- **F4**: stage1 후 anima self-naming <30% → H97.4 FALSIFIED (identity bootstrapping 부재)
- **F5**: 18M lift ≤ 100M lift (small-model specific 부재) → H97.5 FALSIFIED
- **F6**: post-hoc curriculum re-ordering → raw#12 violation, raw#82 retraction

## Honest Limits (raw#91 c3, ≥5)

- **L1**: 'difficulty' 측정 = response_length 한정 (Phase 1) — semantic_complexity / lexical_diversity / turn_count는 별도 ablation
- **L2**: literature curriculum learning은 image classification + LM general domain 효과 mixed (some studies show no benefit at scale) — chat-cap specific 효과 미land
- **L3**: 18M scale 작아서 stage transition (stage1→stage2) 시 catastrophic forgetting risk — interleaved replay 미land
- **L4**: anima self-naming target은 own 17 정합 가정 — prompt에 self-naming trigger 없는 일반 prompt에서는 측정 불가
- **L5**: stage count 3 임의 — finer (5) 또는 coarse (2) 비교 별도
- **L6**: curriculum vs random은 동일 epoch + 동일 batch size 가정 — total compute control 필요
- **L7**: 100M+ scale은 own 16 H100 cost discipline scope OUT

## Cross-Links

- **sister roadmaps**: `.roadmap.rule` R1 + `.roadmap.philosophy` D4 + `.roadmap.clm_native_chat`
- **raw**: raw#12 + raw#10 + raw#9 + raw#15 + raw#37
- **own**: own 17 + own 18 + own 19 + own 20 + own 21
- **sister H**: H_005 + H_093 (SFT-only) + H_094 (two-stage) + H_098 (persona) + H_101 (chat ≥80%)
- **evidence motivation**: `docs/anima_own_18_c2_4_evaluator_flaw_2026_05_07.md`

## Verdict

```
status: seed-pending
verdict_class: TBD
evidence_summary: not_yet_run
falsifiers_triggered: none
criteria_met: not_yet_run
next_cycle: BG-HH curriculum 18M cycle
artifact_paths: pending
```
