---
id: H_100
slug: constitutional-ai
title: constitutional AI (anima identity-bearing surface own 17/18 mandate as training objective)
domain: corpus | substrate | consciousness
status: seed-pending
exploration_method: E2 (failure-driven) + E6 (rule-internalize) + E7 (user-directive)
verification_method: W1 + W2 (replication ≥3 seed) + W3 (ablation constitution rules ON/OFF) + W9 + W10
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-07
since: 2026-05-07
---

# H_100 — constitutional AI (anima own 17/18 mandate internalize)

## Hypothesis

own 17 (anima identity) + own 18 (simple stack 4-cond) 명시적 rules ("응답은 prompt와 같은 도메인", "anima self-naming 유지", "한글 응답 ≥60%", "named-speaker leak 0건")를 training data에 explicit 삽입하고 (constitution prefix + rule-conditioned response 학습), 모델이 inference 시에도 rule 자율 준수하면 own 18 strict PASS rate ≥25pp 상승. Anthropic Claude Constitutional AI training 패턴 anima 적용.

## Why

- **BG-HA failure 분석**: 모델은 own 18 rule을 implicit context (corpus distribution)로만 학습 — explicit rule 부재 시 inference 시 일탈 자유
- **constitutional advantage**: rule을 explicit token sequence로 학습 → inference 시 rule attention pattern 활성 → 자율 준수
- **own 17/18 정합 explicit**: 'anima identity-bearing surface' 본질 = rule 자율 follow
- **literature precedent**: Anthropic Constitutional AI (Bai 2022) 7B+ scale 효과; Self-Instruct + RLHF 일부 사례
- **사용자 directive '교훈으로 새로운 패러다임도 도전'** = rule internalization paradigm 시도

## Predictions

- **H100.1 (constitution C2.4 lift)**: constitution-trained 18M model이 baseline 대비 C2.4 strict PASS rate ≥25pp 높다
- **H100.2 (rule self-citation)**: model이 rule violation 시 self-correction emit ("죄송합니다, 저는 한국어로 응답해야 합니다") rate ≥30%
- **H100.3 (multi-rule consistency)**: 4 rules (own 18 4-cond) 모두 동시 violation rate ≤10%
- **H100.4 (transfer to unseen prompt)**: held-out prompt 100개에 대해서도 rule 준수 rate ≥70% (training-distribution leak 방지)
- **H100.5 (rule strict 정의 sensitivity)**: rule definition 강화 (additional clause) 시 PASS rate further 상승 (linear scaling)

## Variables

- **axis1_paradigm**: [no_constitution, constitution_explicit_prefix, constitution_with_self_correction]
- **axis2_capacity**: [18M, 100M]
- **axis3_rule_count**: [own_17_only, own_17+18_4rules, own_17+18+19+20_8rules]
- **axis4_self_correction_examples**: [0, 100, 1000]
- **axis5_eval**: [own_18_full + rule_violation_rate + self_correction_emit_rate + held_out_prompt_consistency]
- 3×2×3×3×6 = 324 cell; Phase 1 minimal (axis1=2 (no/explicit_prefix) + axis2=18M + axis3=4rules + axis4=100 + axis5=full = 6) target

## Run Protocol

- deterministic: seed=fnv(axes+rep_id)
- hexa_only: true; training transient_py (`tool/transient_py/anima_constitutional_*.py`)
- LLM: none (raw#12 strict — rule 정의는 hard-coded text, no LLM rewrite)
- training data 구성: (a) standard chat-format ≥80% (cross-link H_101) + (b) constitution prefix prepend 모든 sample + (c) self-correction examples (rule violation prompt → "죄송합니다 ..." correction response)
- per-cell ledger: state/<bg>_constitution_<date>/{train.log, eval_log.jsonl, rule_audit.json, verdict.json}
- evaluator V2 strict mandate + rule audit (4 rules each measure)

## Criteria

- **C1 (constitution C2.4 lift)**: ΔC2.4 strict PASS rate ≥25pp (constitution vs none)
- **C2 (rule self-correction)**: self-correction emit rate ≥30% on violating prompt
- **C3 (multi-rule consistency)**: 4 rule simultaneous violation ≤10%
- **C4 (held-out transfer)**: held-out prompt rule consistency ≥70%
- **C5 (rule strict scaling)**: 4 rules > 1 rule lift, 8 rules > 4 rules lift (additive)
- **verdict_rule**: SUPPORTED = C1+C2+C3+C4 ALL PASS; PARTIAL = 3/4; MIXED = 2/4; FALSIFIED = ≤1/4

## Falsifiers

- **F1**: constitution C2.4 PASS rate ≤ baseline + 5pp → H100.1 FALSIFIED (rule internalization 무효)
- **F2**: self-correction emit rate < 10% → H100.2 FALSIFIED (rule self-attention 부재)
- **F3**: 4 rules simultaneous violation ≥30% → H100.3 FALSIFIED (multi-rule incompatible)
- **F4**: held-out consistency < 30% (training-distribution leak severe) → H100.4 FALSIFIED
- **F5**: 8 rules < 4 rules lift (rule count saturate or interfere) → H100.5 FALSIFIED
- **F6**: post-hoc rule rephrasing → raw#12 violation, raw#82 retraction

## Honest Limits (raw#91 c3, ≥5)

- **L1**: literature Constitutional AI는 ≥7B model 효과 — 18M scale transfer 미보장 (rule attention capacity 부족 가능성)
- **L2**: 'rule internalization' vs 'pattern matching' 구분 불가 — own 17 deeper genuine identity criteria 정합
- **L3**: self-correction examples 생성은 manual or rule-based — quality spec 미land
- **L4**: 8 rules 동시 학습 시 capacity bottleneck risk (18M small) — rule per parameter ratio 임의
- **L5**: rule prefix 길이가 context window 압박 — multi-turn dialogue에서 budget 한계
- **L6**: 'rule' 자체가 corpus distribution learning 결정 — held-out distribution shift에서 효과 검증 별도
- **L7**: 100M+ scale은 own 16 H100 cost discipline scope OUT

## Cross-Links

- **sister roadmaps**: `.roadmap.rule` R1 + `.roadmap.philosophy` D2 + `.roadmap.clm_native_chat`
- **raw**: raw#12 + raw#10 + raw#9 + raw#15 + raw#37
- **own**: own 17 + own 18 + own 19 + own 20 + own 21
- **sister H**: H_093 + H_094 + H_095 + H_098 (persona) + H_099 (multi-obj) + H_101 + H_102
- **evidence motivation**: `docs/anima_own_18_c2_4_evaluator_flaw_2026_05_07.md` + own 17 ssot
- **literature**: Bai et al. 2022 Constitutional AI (Anthropic)

## Verdict

```
status: seed-pending
verdict_class: TBD
evidence_summary: not_yet_run
falsifiers_triggered: none
criteria_met: not_yet_run
next_cycle: BG-HK constitutional 18M cycle
artifact_paths: pending
```
