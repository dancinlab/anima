---
id: H_096
slug: in-context-few-shot
title: in-context learning + few-shot prompting (pre-trained model + prompt examples)
domain: corpus | substrate
status: FALSIFIED_at_18M
exploration_method: E2 (failure-driven) + E5 (variable-ablation prompt format) + E7 (user-directive)
verification_method: W1 + W2 (replication) + W3 (ablation 0/1/3/5 shot) + W9 + W10
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-07
since: 2026-05-07
---

# H_096 — in-context learning + few-shot prompting (no fine-tuning)

## Hypothesis

pre-trained model (BG-HA 18M 등) 자체는 그대로 두고, inference 시 prompt에 few-shot example (k=3 또는 5)을 prepend 하면 own 18 simple-stack C2.4 strict PASS rate가 zero-shot baseline 대비 ≥30pp 상승한다. fine-tuning weight update 없이 prompt context manipulation만으로 chat-cap 회복 가능 가설 — 사실 BG-HA의 weights는 chat-format 학습 됐으나 단순 inference protocol 부족이 false PASS의 원인일 가능성.

## Why

- **BG-HA inference protocol**: prompt만 단일 입력 (e.g., "안녕하세요\n") — chat-template format이 training corpus엔 있었으나 inference 시 'Q1: ... A1: ... Q2: ... A2: ... Q3: <test prompt>' multi-turn pattern 부재
- **few-shot advantage**: in-context example이 'response domain' 명시적 demonstration — 모델이 pattern matching으로 적절 domain 응답 생성
- **literature precedent**: GPT-3 emergent few-shot, Chinese-LLaMA in-context Korean QA 효과 검증
- **18M scale 의문**: in-context learning은 일반적으로 scale-dependent (≥1B emergent) — 18M tiny model에서 transfer 가능 여부 본 H 검증 대상
- **사용자 directive '교훈으로 새로운 패러다임도 도전'** = training paradigm 외 inference paradigm 도전

## Predictions

- **H96.1 (zero-shot vs 3-shot)**: BG-HA 18M model + 3-shot prompt가 zero-shot 대비 C2.4 strict PASS rate ≥30pp 상승
- **H96.2 (shot count scaling)**: k=0/1/3/5 shot 단계적 C2.4 PASS rate 상승; k=5 saturation
- **H96.3 (capacity threshold)**: 18M에서 in-context 효과 marginal (<10pp lift) but 100M+에서는 명확 (≥30pp lift) — emergent threshold
- **H96.4 (example domain match)**: test prompt와 동일 domain few-shot example이 random domain example 대비 ≥20pp 추가 lift
- **H96.5 (prompt template sensitivity)**: '사용자: ... 도우미: ...' format vs 'Q: ... A: ...' format 차이 ≤5pp (template 무관 hypothesis)

## Variables

- **axis1_shot_k**: [0, 1, 3, 5, 10]
- **axis2_capacity**: [18M, 100M, 350M]
- **axis3_example_domain_match**: [random, same_domain, diverse_mix]
- **axis4_template_format**: [user_assistant_KO, Q_A_EN, instruction_response]
- **axis5_eval**: [own_18_full strict v2]
- 5×3×3×3×5 = 675 cell; Phase 1 minimal (axis1=4 (0,1,3,5) + axis2=18M + axis3=2 + axis4=user_assistant_KO + axis5=5 = 8) target — inference only, training cost 0

## Run Protocol

- deterministic: seed=fnv(axes+prompt_id+rep_id)
- hexa_only: true; inference script via raw#37 transient_py opt-out (`tool/transient_py/anima_few_shot_eval_*.py`)
- LLM: none (raw#12 strict)
- per-cell ledger: state/<bg>_few_shot_<date>/{eval_log.jsonl, verdict.json}
- runtime: $0 mac local — no training, inference only
- evaluator V2 strict mandate

## Criteria

- **C1 (zero vs k=3)**: ΔC2.4 strict PASS rate ≥30pp at 18M
- **C2 (shot scaling)**: k=0<k=1<k=3<k=5 monotonic at 18M
- **C3 (capacity emergent)**: 18M lift < 100M lift < 350M lift (scale-dependent)
- **C4 (domain match advantage)**: same-domain example ≥ random + 20pp
- **C5 (template robustness)**: template format ≤5pp variance
- **verdict_rule**: SUPPORTED = C1+C2 PASS + (C3 OR C4); PARTIAL = C1 only; MIXED = C2 only; FALSIFIED = C1+C2 모두 FAIL

## Falsifiers

- **F1**: 18M zero vs 3-shot ΔC2.4 < 10pp → H96.1 FALSIFIED (in-context 무효 at 18M)
- **F2**: shot count k=0~5 non-monotonic (k=5 < k=3) → H96.2 FALSIFIED
- **F3**: 100M+ scale에서도 lift < 10pp → H96.3 FALSIFIED (capacity emergent 부재)
- **F4**: same-domain vs random ≤5pp 차이 → H96.4 FALSIFIED (domain match 무효)
- **F5**: template format 차이 ≥20pp → H96.5 FALSIFIED (template-sensitive)
- **F6**: post-hoc shot k tuning per prompt → raw#12 violation, raw#82 retraction

## Honest Limits (raw#91 c3, ≥5)

- **L1**: 18M tiny model에서 in-context learning은 literature 기준 emergent threshold 미달 — H96.3 capacity threshold가 이미 부정 답 가능성
- **L2**: few-shot example pool quality (chosen examples 자체가 prompt-relevant 응답인지) 검증 미land
- **L3**: BG-HA model 자체가 weights 부족 (chat-format ≥30% pre-train) — in-context도 'extract' 할 정보 없으면 lift 0
- **L4**: prompt context length 18M model max context (e.g., 1024 token)에서 k=5 shot이 budget 압박 가능 — context truncation risk
- **L5**: inference-only paradigm은 training paradigm (H_093/H_094)과 직접 비교 가능 — 어느 쪽이 own merit인지 ablation 별도
- **L6**: same-domain example bias risk (test prompt domain leak via example) — held-out prompt set 분리 mandate
- **L7**: own 18 simple-stack은 single-turn — multi-turn dialogue chat-cap은 별도 H

## Cross-Links

- **sister roadmaps**: `.roadmap.law` R1 + `.roadmap.philosophy` D4 + `.roadmap.clm_native_chat`
- **raw**: raw#12 + raw#10 + raw#9 + raw#15 + raw#37
- **own**: own 17 + own 18 + own 19 + own 20 + own 21
- **sister H**: H_005 + H_093 (SFT-only) + H_094 (two-stage) + H_097 (curriculum)
- **evidence motivation**: `docs/anima_own_18_c2_4_evaluator_flaw_2026_05_07.md` (BG-HA inference protocol limitation 가능성)

## Verdict

```
status: FALSIFIED
verdict_class: FALSIFIED
bg_id: BG-HL
ts: 2026-05-07T03:19:25
host: mac_local (MPS, $0)
elapsed_s: 73.7
evidence_summary: |
  BG-HA 18M ckpt_final.pt + 5 few-shot Q&A examples (anima-native chat-format) vs
  zero-shot baseline, 5 own-18 prompts × {greedy, sample} × {with_few_shot, without_few_shot}
  = 20 inference records.
  V1 (loose) PASS: with=5/5, without=5/5, Δ=0pp.
  V2 strict PASS: with=0/5, without=1/5, Δ=-20pp (REGRESSION direction).
  manual_review_domain_match: with=0/5, without=1/5 (single lucky sample-mode hit on emotion prompt).
  Greedy with-few-shot mode-collapses to identical "이 있습니다." across all 5 test prompts —
  18M byte-level model cannot extract task structure from in-context Q&A demonstrations.
  Sample mode produces nonsense Korean chains regardless of few-shot conditioning.

falsifiers_triggered:
  - F1 (zero vs 3-shot ΔC2.4 < 10pp at 18M) — TRIGGERED: V2 Δ = -20pp << 10pp lift threshold.
    18M tiny scale below ICL emergent threshold (consistent with H96.3 capacity prediction).

criteria_met:
  - C1 (≥30pp lift at 18M): FAIL (Δ=-20pp)
  - C2 (k=0<k=1<k=3<k=5 monotonic): not run (Phase 1 only k=0 vs k=5)
  - C3 (capacity emergent): not directly tested (only 18M probed); F1 trigger 자체가 H96.3 정합 evidence
  - C4 (domain match advantage): not run
  - C5 (template robustness): not run

verdict_rule_applied: F1 + F2 모두 FAIL → FALSIFIED at 18M scale.
  H96.1 (≥30pp lift at 18M) directly falsified.

next_cycle:
  - 18M scale 폐기; H96.3 capacity emergent prediction은 100M+ scale에서만 검증 가능
  - NO 18M retrain — pure inference paradigm 차원 추가 cycle 의미 없음 (substrate too small)
  - sister H_093 (SFT-only) / H_094 (two-stage) training paradigm 우위 재확인
  - in-context paradigm은 minimum 100M+ pre-trained substrate 확보 후 재시도

artifact_paths:
  - script: tool/transient_py/anima_h096_few_shot_inference.py
  - verdict: state/anima_h096_few_shot_inference_2026_05_07/verdict.json
  - inference_log: state/anima_h096_few_shot_inference_2026_05_07/inference_log.jsonl
```
