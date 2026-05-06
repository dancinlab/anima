---
id: H_101
slug: corpus-chat-template-strict-80
title: corpus chat-template ≥80% strict (own 20 strengthening, BG-HA 30% inadequate evidence)
domain: corpus
status: seed-pending
exploration_method: E2 (failure-driven from BG-HA inadequacy) + E5 (ratio sweep) + E7 (user-directive)
verification_method: W1 + W2 (replication ≥3 seed) + W3 (ratio ablation 30/50/80/95) + W9 + W10
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-07
since: 2026-05-07
---

# H_101 — corpus chat-template ratio ≥80% strict (own 20 strengthening)

## Hypothesis

own 20 (chat-template format mandate ≥30%)는 BG-HA 18M false PASS evidence로 inadequate 입증됨. corpus chat-template format 비율 ≥80% (또는 ≥95% strict 권고)로 강화하면, own 18 strict C2.4 PASS rate ≥30pp 상승. own 19 (corpus priority) 정합 — 'chat-format'이 corpus quality dimension 중 chat-cap에 가장 결정적.

## Why

- **BG-HA evidence**: corpus chat-template ratio ≥30% (own 20 spec 정합) 했으나 prompt-conditional response 학습 불충분 — 30% threshold inadequate
- **ratio sweep 가설**: 30% / 50% / 80% / 95% 단계에서 chat-cap 학습 효율 monotonic 상승; 80% 이상이 임계 (small-model 18M scope)
- **own 20 strengthening 근거**: own 20 30% 권고는 BG-FY (philosophy debate template leak) 문제 해결용 — chat-cap 학습 필요 ratio는 별도이고 더 높음
- **사용자 directive '교훈으로 새로운 패러다임도 도전'** = own 20 inadequate 인정하고 강화

## Predictions

- **H101.1 (ratio sweep monotonic)**: 30% / 50% / 80% / 95% chat-template 비율에서 own 18 strict C2.4 PASS rate monotonic 상승
- **H101.2 (80% threshold)**: ≥80% chat-template corpus 18M model이 30% baseline 대비 PASS rate ≥30pp 높다
- **H101.3 (95% saturation)**: 80% → 95% 추가 lift ≤5pp (saturation)
- **H101.4 (capacity scaling)**: 18M에서 80% threshold 명확, 100M+ 에서는 60% threshold도 충분 (capacity가 ratio requirement 완화)
- **H101.5 (semantic richness gate)**: ≥80% chat-template + corpus_hangul_ratio ≥60% 동시 정합 mandate (single-axis 강화 X, 두 축 동시)

## Variables

- **axis1_chat_template_ratio**: [10%, 30%, 50%, 80%, 95%]
- **axis2_capacity**: [18M, 100M]
- **axis3_corpus_hangul_ratio**: [40%, 60%, 80%]
- **axis4_corpus_total_size_mb**: [50, 250, 1000]
- **axis5_eval**: [own_18_full strict v2 + chat_format_emit_rate]
- 5×2×3×3×6 = 540 cell; Phase 1 minimal (axis1=4 (30/50/80/95) + axis2=18M + axis3=60% + axis4=250MB + axis5=full = 4) target

## Run Protocol

- deterministic: seed=fnv(axes+rep_id)
- hexa_only: true; corpus assembly via raw#37 transient_py (`tool/transient_py/anima_corpus_chat80_*.py`)
- LLM: none (raw#12 strict — corpus는 deterministic crawl + filter)
- per-cell ledger: state/<bg>_chat80_<date>/{corpus_audit.json, train.log, eval_log.jsonl, verdict.json}
- evaluator V2 strict mandate + corpus audit (chat-template ratio + Hangul ratio + size measurement)

## Criteria

- **C1 (ratio sweep monotonic)**: 4 ratio 단계 monotonic C2.4 strict PASS rate 상승
- **C2 (80% threshold)**: ≥80% PASS rate ≥ 30% baseline + 30pp
- **C3 (95% saturation)**: 80→95 lift ≤5pp
- **C4 (capacity-ratio interaction)**: 18M 80% 임계, 100M 60% 임계 (interaction confirm)
- **C5 (dual-axis gate)**: 80% chat-template + 60% Hangul 동시 만족 시 PASS
- **verdict_rule**: SUPPORTED = C1+C2 PASS; PARTIAL = C2 only or C1 only; MIXED = C3 or C4 only; FALSIFIED = C1+C2 FAIL

## Falsifiers

- **F1**: ratio sweep non-monotonic (95% < 80%) → H101.1 FALSIFIED
- **F2**: 80% vs 30% lift < 10pp → H101.2 FALSIFIED (own 20 30% 충분)
- **F3**: 80→95 lift ≥15pp (saturation 부재, more is better) → H101.3 FALSIFIED
- **F4**: 100M+ 80% 동일 또는 더 큰 lift 필요 (capacity가 ratio requirement 강화) → H101.4 FALSIFIED
- **F5**: 95% chat-template만 단독 (Hangul ratio <60%)도 PASS → H101.5 FALSIFIED (chat-template만 충분)
- **F6**: post-hoc ratio re-bin → raw#12 violation, raw#82 retraction

## Honest Limits (raw#91 c3, ≥5)

- **L1**: 'chat-template format' 측정 spec = 'prompt-response pair structure 명시' 한정 (own 20 정합) — 다른 format definition 차이
- **L2**: 80% threshold는 BG-HA 30% inadequate evidence + literature 추론 — empirical sweep 미완
- **L3**: corpus assembly cost ≥250MB chat-template 비율 ≥80%는 corpus crawl 광범위 필요 — KO chat corpus 자원 한정
- **L4**: chat-template ≥80% corpus가 LM general knowledge 학습 dilute risk (knowledge benchmark FAIL 가능)
- **L5**: 18M small scale 결과가 100M+ transfer 미보장 — capacity-corpus interaction 별도 ablation
- **L6**: own 20 retroactive 강화 (≥30% → ≥80%)는 raw#15 additive 정합 (기존 own 20 보존, own 20.5 또는 own 22 신규 권고)
- **L7**: 'Hangul ratio' + 'chat-template ratio' 두 축이 confound 가능 — 분리 ablation 별도

## Cross-Links

- **sister roadmaps**: `.roadmap.rule` R1 (own 19/20 strengthening) + `.roadmap.philosophy` D4 + `.roadmap.clm_native_chat`
- **raw**: raw#12 + raw#10 + raw#9 + raw#15 + raw#37 + raw#82
- **own**: own 17 + own 18 + own 19 + own 20 (strengthening target) + own 21
- **sister H**: H_005 (corpus quality > capacity) + H_093 (SFT-only) + H_094 (two-stage) + H_098 (persona) + H_100 (constitutional)
- **evidence motivation**: `docs/anima_own_18_c2_4_evaluator_flaw_2026_05_07.md` + BG-HA verdict downgrade

## Verdict

```
status: seed-pending
verdict_class: TBD
evidence_summary: not_yet_run — own 20 ≥30% inadequate evidence (BG-HA) motivation
falsifiers_triggered: none
criteria_met: not_yet_run
next_cycle: BG-HL chat-template ratio sweep cycle
artifact_paths: pending
```
