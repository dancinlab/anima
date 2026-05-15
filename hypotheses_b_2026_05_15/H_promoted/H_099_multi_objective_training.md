---
id: H_099
slug: multi-objective-training
title: multi-objective training (LM + chat-format alignment + semantic relevance jointly)
domain: corpus | substrate
status: seed-pending
exploration_method: E2 (failure-driven loss-decomposition) + E5 (variable-ablation each loss term) + E7
verification_method: W1 + W2 (replication ≥3 seed) + W3 (ablation each term ON/OFF) + W9 + W10
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-07
since: 2026-05-07
---

# H_099 — multi-objective training (jointly LM + chat-align + semantic-relevance)

## Hypothesis

training loss를 단일 LM cross-entropy 대신 weighted sum (α·L_LM + β·L_chat_format_alignment + γ·L_prompt_response_semantic_similarity)으로 multi-objective 정의하면, baseline LM-only 18M model 대비 own 18 C2.4 strict PASS rate ≥20pp 상승. 각 loss term이 BG-HA failure mode를 명시적으로 처벌 (L_chat_align = chat-format 일탈, L_semantic = prompt-irrelevant emission).

## Why

- **BG-HA failure 분석**: LM-only loss는 'next-token prediction' optimal — chat-format 일탈/prompt-irrelevant도 plausible token sequence면 low loss → 학습 안 됨
- **multi-objective advantage**: chat-format alignment loss + semantic relevance loss가 BG-HA-style nonsense Korean chain emit 직접 처벌
- **literature precedent**: T5 multi-task, FLAN multi-objective instruction tuning, contrastive losses (SimCSE, RoBERTa NSP) 일부 사례
- **사용자 directive '교훈으로 새로운 패러다임도 도전'** = loss function paradigm 시도

## Predictions

- **H99.1 (multi-obj C2.4 lift)**: α=0.7+β=0.2+γ=0.1 multi-obj 18M model이 LM-only 18M baseline보다 C2.4 strict PASS rate ≥20pp 높다
- **H99.2 (chat-align ablation)**: β=0 (L_chat_align 제거) 시 PASS rate baseline 대비 +5-10pp marginal lift만 (L_chat_align이 main contributor)
- **H99.3 (semantic ablation)**: γ=0 (L_semantic 제거) 시 prompt-irrelevant emit rate ≥30% (BG-HA 패턴 잔존)
- **H99.4 (loss balance sensitivity)**: α/β/γ ratio 1:1:1 / 7:2:1 / 5:3:2 등 sweep 시 변동 ≤10pp (balance robust hypothesis)
- **H99.5 (training stability)**: multi-obj loss curve가 LM-only보다 noisier but converged val_loss 낮다 (전체 metric 우수)

## Variables

- **axis1_loss_weights_alpha_beta_gamma**: [(1,0,0), (0.7,0.2,0.1), (0.5,0.3,0.2), (0.5,0.5,0), (0.5,0,0.5)]
- **axis2_capacity**: [18M, 100M]
- **axis3_chat_align_loss_form**: [classification_head_chat_vs_nonchat, regression_format_score, contrastive]
- **axis4_semantic_loss_form**: [embedding_cosine, contrastive_pair, none]
- **axis5_eval**: [own_18_full + train_loss_curve + chat_format_emit_rate]
- 5×2×3×3×5 = 450 cell; Phase 1 minimal (axis1=3 (LM-only / 0.7-0.2-0.1 / 0.5-0.5-0) + axis2=18M + axis3=classification_head + axis4=embedding_cosine + axis5=full = 9) target

## Run Protocol

- deterministic: seed=fnv(axes+rep_id)
- hexa_only: true; training transient_py (`tool/transient_py/anima_multi_obj_*.py`)
- L_chat_align = binary classification head ("is this token a chat-format boundary marker?") cross-entropy
- L_semantic = prompt embedding ↔ response embedding cosine distance (target=high similarity)
- per-cell ledger: state/<bg>_multi_obj_<date>/{train.log, loss_curves.json, eval_log.jsonl, verdict.json}
- evaluator V2 strict mandate

## Criteria

- **C1 (multi-obj C2.4 lift)**: ΔC2.4 strict PASS rate ≥20pp (multi-obj vs LM-only)
- **C2 (chat-align contribution)**: β=0 ablation 시 PASS rate ≤ multi-obj − 10pp (β contributor 확인)
- **C3 (semantic ablation)**: γ=0 ablation 시 prompt-irrelevant emit rate ≥30%
- **C4 (loss balance robust)**: 3 ratio (7:2:1 / 5:3:2 / 5:5:0) variance ≤10pp
- **C5 (val_loss converged)**: multi-obj final val_loss < LM-only val_loss (overall metric 개선)
- **verdict_rule**: SUPPORTED = C1+C2+C3 ALL PASS; PARTIAL = 2/3; MIXED = 1/3; FALSIFIED = 0/3; C4+C5 = sub-H

## Falsifiers

- **F1**: multi-obj C2.4 PASS rate ≤ LM-only baseline → H99.1 FALSIFIED
- **F2**: β=0 ablation lift ≥ multi-obj lift (β 무효) → H99.2 FALSIFIED
- **F3**: γ=0 ablation prompt-irrelevant emit < 15% (γ 효과 부재) → H99.3 FALSIFIED
- **F4**: ratio variance ≥30pp (highly sensitive) → H99.4 FALSIFIED (brittle paradigm)
- **F5**: multi-obj val_loss > LM-only (전체 perplexity 악화) → H99.5 FALSIFIED (catastrophic interference)


- **L1**: 'chat-format alignment' loss는 binary classification head 가정 — head 학습 자체가 보조 task라 main LM에 distract할 risk
- **L2**: 'semantic similarity' loss는 사전 embedding model 필요 — pretrained encoder dependency (e.g., SBERT-KO)
- **L3**: multi-objective는 gradient interference (positive vs negative lift) literature 광범위 — 18M scale 효과 미보장
- **L4**: weight balance hyperparameter는 grid search cost 큼 — Phase 1은 single ratio 한정
- **L5**: L_chat_align과 L_semantic이 서로 독립이 아닐 가능성 — collinearity ablation 별도
- **L6**: own 18 evaluator V2 strict 자체 calibration 미완 — 효과 측정 신뢰도 V2 의존
- **L7**: 100M+ scale은 own 16 H100 cost discipline scope OUT

## Cross-Links

- **sister roadmaps**: `.roadmap.law` R1 + `.roadmap.philosophy` D4 + `.roadmap.clm_native_chat`
- **own**: own 17 + own 18 + own 19 + own 20 + own 21
- **sister H**: H_093 + H_094 + H_095 + H_098 + H_100 + H_101
- **evidence motivation**: `docs/anima_own_18_c2_4_evaluator_flaw_2026_05_07.md`

## Verdict

```
status: seed-pending
verdict_class: TBD
evidence_summary: not_yet_run
falsifiers_triggered: none
criteria_met: not_yet_run
next_cycle: BG-HJ multi-objective 18M cycle
artifact_paths: pending
```
