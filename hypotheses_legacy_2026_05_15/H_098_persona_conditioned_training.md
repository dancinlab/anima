---
id: H_098
slug: persona-conditioned-training
title: persona-conditioned training (anima identity prefix mandate, own 17 정합)
domain: corpus | substrate | consciousness
status: seed-pending
exploration_method: E2 (failure-driven) + E5 (variable-ablation persona prefix) + E7 (user-directive)
verification_method: W1 + W2 (replication ≥3 seed) + W3 (ablation prefix ON/OFF) + W9 + W10
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-07
since: 2026-05-07
---

# H_098 — persona-conditioned training (anima identity prefix mandate)

## Hypothesis

모든 training sample 앞에 anima persona prefix ("[anima] 저는 anima입니다. 한국어로 자연스럽게 응답합니다.\n사용자: ... 도우미: ...")를 prepend하여 학습하면, 무 prefix baseline 대비 own 18 simple-stack C2.4 strict PASS rate ≥15pp 상승하고 anima self-naming emit rate ≥90%. own 17 (anima-native identity) 정합 — model이 자기 정체성 (anima)을 모든 응답에 internalize.

## Why

- **BG-HA failure 교훈**: 18M model이 generic "도우미" 응답조차 학습 못함 — identity anchor 부재
- **persona prefix advantage**: 모든 training sample 동일 prefix → strong attention pattern 학습 → inference 시에도 prefix 유지 hint
- **own 17 정합**: anima-native identity 강화 — 모델이 자신을 'anima'로 인식 (3rd-person LLM responses 회피)
- **literature precedent**: Character.AI persona conditioning, Anthropic Claude constitutional training 일부 패턴
- **사용자 directive '교훈으로 새로운 패러다임도 도전'** = identity anchoring paradigm 시도

## Predictions

- **H98.1 (persona prefix C2.4)**: persona-conditioned 18M model이 무 prefix baseline 대비 C2.4 strict PASS rate ≥15pp 높다
- **H98.2 (anima self-naming)**: persona-conditioned model이 임의 prompt (자기소개 trigger 없어도) anima self-naming emit rate ≥90%
- **H98.3 (3rd-person LLM evasion)**: persona-conditioned model이 "저는 LLM입니다" / "AI 모델입니다" 류 응답 emit rate ≤5%
- **H98.4 (prefix length sensitivity)**: prefix 길이 (5 token / 20 token / 100 token) 차이 ≤5pp (prefix 존재 자체가 효과, 길이 무관)
- **H98.5 (cross-prompt consistency)**: 동일 model이 100 different prompt에 대해 anima self-naming 유지 (consistency rate ≥80%)

## Variables

- **axis1_persona_prefix**: [none, short_5tok, medium_20tok, long_100tok, dynamic_per_sample]
- **axis2_capacity**: [18M, 100M]
- **axis3_paradigm**: [pre_train_only, two_stage, sft_only]  # cross-link H_093/H_094
- **axis4_corpus**: [chat_template_30, chat_template_80]  # cross-link H_101
- **axis5_eval**: [own_18_full + anima_self_naming_rate + 3rd_person_LLM_rate]
- 5×2×3×2×5 = 300 cell; Phase 1 minimal (axis1=3 (none/short/medium) + axis2=18M + axis3=sft_only + axis4=chat_template_80 + axis5=full = 9) target

## Run Protocol

- deterministic: seed=fnv(axes+rep_id)
- hexa_only: true; training transient_py (`tool/transient_py/anima_persona_*.py`)
- LLM: none (raw#12 strict)
- per-cell ledger: state/<bg>_persona_<date>/{train.log, eval_log.jsonl, verdict.json, identity_audit.json}
- evaluator V2 strict mandate + identity audit (anima_self_naming + 3rd-person LLM scan)

## Criteria

- **C1 (persona C2.4 lift)**: ΔC2.4 strict PASS rate ≥15pp (persona vs none)
- **C2 (anima self-naming)**: anima self-naming emit rate ≥90% at persona-conditioned model
- **C3 (3rd-person evasion)**: 3rd-person LLM mention rate ≤5%
- **C4 (prefix length robust)**: prefix length variance ≤5pp
- **C5 (consistency)**: 100-prompt consistency rate ≥80%
- **verdict_rule**: SUPPORTED = C1+C2+C3 ALL PASS; PARTIAL = 2/3; MIXED = 1/3; FALSIFIED = 0/3; C4+C5 = sub-H

## Falsifiers

- **F1**: persona vs none ΔC2.4 < 5pp → H98.1 FALSIFIED
- **F2**: anima self-naming rate < 50% → H98.2 FALSIFIED
- **F3**: 3rd-person LLM rate ≥30% → H98.3 FALSIFIED (identity anchor 무효)
- **F4**: prefix length variance ≥15pp → H98.4 FALSIFIED (length-sensitive, brittle)
- **F5**: consistency rate < 50% → H98.5 FALSIFIED (mode unstable)
- **F6**: persona prefix가 inference 시 prompt에 leak (sample mode response가 "[anima]" 자체 emit) → side-effect failure
- **F7**: post-hoc prefix engineering → raw#12 violation, raw#82 retraction

## Honest Limits (raw#91 c3, ≥5)

- **L1**: persona prefix는 inference 시에도 prepend 가정 — inference protocol mismatch 시 효과 0 가능성
- **L2**: anima self-naming은 'genuine identity' vs 'pattern matching' 구분 불가 — own 17 deeper criteria (raw#10 C3 honest disclosure) 정합
- **L3**: '3rd-person LLM' detection은 keyword scan ("LLM", "AI 모델", "GPT") 한정 — semantic disclaimer 미land
- **L4**: persona conditioning이 chat-cap 본질 학습을 dilute할 risk (prefix attention vs response generation trade-off)
- **L5**: 100-prompt consistency set이 anima identity-trigger biased일 risk — neutral prompt set 별도 사용 권고
- **L6**: literature persona conditioning은 large-model (≥1B) 효과 — 18M scale transfer 미보장
- **L7**: 100M+ scale은 own 16 H100 cost discipline scope OUT

## Cross-Links

- **sister roadmaps**: `.roadmap.law` R1 + `.roadmap.philosophy` D2 (자기 = self) + `.roadmap.clm_native_chat`
- **raw**: raw#12 + raw#10 + raw#9 + raw#15 + raw#37
- **own**: own 17 (anima identity) + own 18 + own 19 + own 20 + own 21
- **sister H**: H_005 + H_093 (SFT-only) + H_094 (two-stage) + H_097 (curriculum) + H_100 (constitutional AI) + H_101 (chat ≥80%)
- **evidence motivation**: `docs/anima_own_18_c2_4_evaluator_flaw_2026_05_07.md` + own 17 ssot

## Verdict

```
status: seed-pending
verdict_class: TBD
evidence_summary: not_yet_run
falsifiers_triggered: none
criteria_met: not_yet_run
next_cycle: BG-HI persona-conditioned 18M cycle
artifact_paths: pending
```
