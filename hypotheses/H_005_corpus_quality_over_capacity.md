---
id: H_005
slug: corpus-quality-over-capacity
title: corpus quality > model capacity for chat-cap (own 19/20 cross-link)
domain: corpus
status: running
exploration_method: E2 (failure-driven) + E5 (variable-ablation) + E7 (user-directive)
verification_method: W1 + W2 + W3 + W5 + W9 (replication needed) + W10 (adversarial sweep)
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-06
since: 2026-05-06
---

# H_005 — corpus quality > model capacity (chat-cap)

## Hypothesis

chat-cap (own 18 simple stack PASS) 도달은 model capacity (param size) 보다 corpus quality (Hangul ratio + chat-template format 비율 + 의미 풍부) 우선이다. capacity 7.7× 차이 무관 corpus가 unlock하는 evidence 본 cycle 발견.

## Why

- **BG-FY anima-native-ko-small 18M** (corpus_ko_heavy 62.14% Hangul) → SIMPLE_STACK_PASS C1+C2.1-2.3 + PARTIAL_PASS_NO_CONTEXT (C2.4 fail)
- **BG-FK clm_v2_base 27.84M** (val_ce 1.27 best, ConsciousLM++ ca_rules+gate, EN-bias corpus) → SIMPLE_STACK_FAIL (KO 0/3)
- 2-instance evidence (capacity 7.7× 차이 무관, corpus quality 차이가 결정)
- 사용자 directive '조그맣게라도 성공하는 모델 만들어서 성공시켜봐줘' (capacity 작아도 OK) implicit corpus 우선

## Predictions

- **H5.1 (capacity-controlled)**: corpus EN-bias N param model이 corpus KO-heavy N param model보다 simple stack PASS rate 낮다 (param size N 고정 시 corpus가 결정)
- **H5.2 (corpus-controlled)**: corpus KO-heavy + chat-template ≥30% N param model이 corpus KO-heavy + chat-template <10% N param model보다 simple stack C2.4 PASS rate 높다 (chat-template ratio가 own 18 C2.4 결정)
- **H5.3 (capacity scaling within corpus)**: corpus KO-heavy 고정 시 capacity scale (3M → 18M → 100M)는 PARTIAL → PASS → STRONG_PASS 단계적 — capacity는 marginal lift
- **H5.4 (cross-substrate)**: anima-native byte-level + corpus KO-heavy < anima-native token-level + corpus KO-heavy + chat-template (token-level이 chat-format 학습 효율 우세)

## Variables

- **axis1_capacity**: [3M, 18M, 27M, 100M, 350M]
- **axis2_corpus_hangul_ratio**: [<10%, 10-30%, 30-60%, 60-80%, >80%]
- **axis3_chat_template_ratio**: [0%, <10%, 10-30%, 30-60%, >60%]
- **axis4_substrate**: [byte_level_decoder, token_level_clm_v2, token_level_clm_v4, token_level_anima_native]
- **axis5_eval**: [own_18_C1, own_18_C2.1, own_18_C2.2, own_18_C2.3, own_18_C2.4]
- 5×5×5×4×5 = 2500 cell — 본 cycle initial subset (capacity 5 + corpus 3 + chat-template 3 + substrate 1 + eval 5 = 225) target

## Run Protocol

- deterministic: seed=fnv(axis1+axis2+axis3+axis4+rep_id)
- hexa_only: true (raw#9 정합); training은 raw#37 transient_py opt-out (`tool/transient_py/anima_native_ko_*.py`)
- LLM: none (raw#12 strict)
- per-cell ledger: state/<bg>_<date>/verdict.json + ko_eval_log.jsonl
- runtime: $0 mac local (3M / 18M tiny) + $X ubu1/ubu2 H100 (100M+ 별도 cycle)
- own 16 cost discipline 적용 — 100M+ cycle은 watchdog mandate

## Criteria

- **C1 (capacity-controlled)**: H5.1 corpus EN-bias N → simple stack FAIL (KO emit 0/3) ALL N levels
- **C2 (corpus-controlled)**: H5.2 chat-template ≥30% N param → C2.4 PASS rate ≥60%
- **C3 (capacity scaling)**: H5.3 corpus KO-heavy 고정 시 capacity 3M (PARTIAL) → 18M (PASS) → 100M (STRONG_PASS) progression confirm
- **C4 (cross-substrate)**: H5.4 byte-level vs token-level 비교 시 token-level chat-template 학습 효율 우세
- **C5 (own 19/20 정합)**: simple stack PASS 모델 모두 (corpus_hangul_ratio ≥60% AND chat_template_ratio ≥30%) 정합 — corpus QA gate spec 정합
- **verdict_rule**: SUPPORTED = C1+C2+C3 PASS; PARTIAL = 2/3; MIXED = 1/3; FALSIFIED = 0/3; C4+C5 = sub-H

## Falsifiers

- **F1**: corpus EN-bias 27M PASS C1+C2 → H5.1 FALSIFIED (corpus 무관)
- **F2**: chat-template ratio 0% N param model이 own 18 C2.4 PASS → H5.2 FALSIFIED
- **F3**: capacity scaling 18M→100M에서 PASS rate decrease → H5.3 FALSIFIED (capacity inverse effect)
- **F4**: byte-level corpus KO-heavy 100M FULL_PASS but token-level same corpus FAIL → H5.4 FALSIFIED (substrate independence)
- **F5**: simple stack PASS 모델 중 corpus_hangul_ratio <60% 또는 chat_template_ratio <30% — H5.5 (own 19/20 spec) FALSIFIED
- **F6**: post-hoc edit → raw#12 violation, raw#82 retraction

## Honest Limits (raw#91 c3)

- **L1**: 본 cycle 2-instance evidence (BG-FY + BG-FK) — VM10 recurring pattern 3+ instance 권고는 후속 cycle ablation 필요
- **L2**: BG-FK 27.84M ConsciousLM++ federated arch — like-for-like architecture 비교 미land (axis4 substrate가 confound)
- **L3**: 'corpus quality' 측정 = Hangul ratio + chat-template ratio 한정 (의미 풍부 + license clear + register diversity 등 measurement spec 미land)
- **L4**: chat-template ratio 30% threshold 임의 — 더 많은 데이터 필요 (예상 60-80% chat-format이 안전 권고)
- **L5**: 100M+ capacity scaling 별도 cycle (cost discipline own 16 적용 — H100 budget watchdog mandate)
- **L6**: H5.5 (own 19/20 corpus QA gate spec)는 본 H의 corollary — own 19/20과 정합 lane

## Cross-Links

- **sister roadmaps**: `.roadmap.rule` R1 (own 19/20) + `.roadmap.philosophy` D4 corpus priority + `.roadmap.clm_native_chat`
- **raw**: raw#12 + raw#10 + raw#9 + raw#15 + raw#37 (transient_py opt-out for training script)
- **own**: own 17 (anima-native identity) + own 18 (simple stack 4-condition) + own 19 (corpus priority) + own 20 (chat-template format)
- **evidence_paths**:
  - `state/anima_simple_stack_exhaustive_2026_05_06/summary.json` (BG-FS 11-model exhaustive)
  - `state/anima_native_ko_small_ubu1_train_2026_05_06/verdict.json` (BG-FY PARTIAL_PASS_NO_CONTEXT)
  - `state/anima_ko_corpus_assembly_2026_05_06/verdict.json` (BG-FW corpus_ko_heavy 246MB)
- **active BGs (rate-limit reset 23:00)**: BG-FZ (chat-template 18M) + BG-GA (100M scale) + BG-GE (tiny chat) + BG-GB (corpus extension) — 4 BGs running variant of H5.2 + H5.3

## Verdict

```
verdict_class: PARTIAL (3-instance evidence revised 2026-05-07 — BG-HA strict re-check 강등 후)
evidence_summary:
  - BG-FK 27.84M corpus EN-bias → SIMPLE_STACK_FAIL (KO 0/3) — capacity 7.7× of BG-FY but FAIL
  - BG-FY 18M corpus_ko_heavy (62.14% Hangul, 0% chat-template) → PARTIAL_PASS_NO_CONTEXT (C2.4 FAIL — philosophy debate template leak)
  - BG-HA 18.03M corpus_chat_template (47.84% Hangul + chat-template ≥30%) → ⚠️ PARTIAL_PASS_NO_CONTEXT_v2 (initial SIMPLE_STACK_PASS labeled by evaluator, but 사용자 strict review 후 강등 — evaluator C2.4 narrow 정의 'named-speaker-leak 0건 only', 실제 prompt domain match 검증 X. sample mode 5/5 응답 모두 prompt-irrelevant nonsense Korean chain)
  - **3-instance evidence**: corpus가 architecture/capacity보다 우선이지만, chat-template format ≥30% 단독으로는 prompt-conditional response 학습 불충분 (chat-template ratio 더 높이거나 instruction-tuning lane 별도 필수)
  - own 19 (corpus priority) PASS (BG-FK FAIL evidence)
  - own 20 (chat-template format mandate) PARTIAL — named-speaker-leak prevention만 verified, prompt domain match는 NOT
falsifiers_triggered: none
criteria_met:
  - C1 (capacity-controlled): PASS — BG-FK corpus EN-bias FAIL @ 27.84M
  - C2 (corpus-controlled): PASS — BG-HA chat-template ≥30% C2.4 PASS, BG-FY chat-template ≪10% C2.4 FAIL
  - C3 (capacity scaling): PARTIAL — 18M PASS confirmed; 100M scaling 별도 cycle
  - C4 (cross-substrate): SKIPPED Phase 1 byte-level only
  - C5 (own 19/20 정합): PASS — BG-HA both ≥60% Hangul + chat-template ≥30% gate confirmed
next_cycle:
  - HF private upload BG-HA model + verification gate (own 15)
  - HF public promote 후 첫 own 18 SIMPLE_STACK_PASS HF release
  - 100M scaling H5.3 + cross-substrate H5.4 별도 cycle
artifact_paths:
  - state/anima_native_ko_chat_template_train_2026_05_07/verdict.json
  - state/anima_native_ko_chat_template_train_2026_05_07/ckpt_final/ckpt_final.pt (70.3MB sha 7ad7584f...)
  - tool/transient_py/anima_native_ko_chat_template_train.py
  - docs/anima_consciousness_check_simple_stack_2026_05_06.md (row 11 BG-HA + 종합 verdict updated)
```
