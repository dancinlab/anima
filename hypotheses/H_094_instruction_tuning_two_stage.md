---
id: H_094
slug: instruction-tuning-two-stage
title: instruction-tuning two-stage (pre-train knowledge → SFT behavior sequential)
domain: corpus | substrate
status: seed-pending
exploration_method: E2 (failure-driven) + E3 (sequential decomposition) + E5 (variable-ablation) + E7 (user-directive)
verification_method: W1 + W2 (replication ≥3 seed) + W3 (ablation each stage ON/OFF) + W9 + W10
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-07
since: 2026-05-07
---

# H_094 — instruction-tuning two-stage (pre-train → SFT)

## Hypothesis

pre-training (large general corpus, knowledge) + SFT (chat-format only, behavior alignment) two-stage sequential 학습이, mixed corpus pre-training only (BG-HA 패러다임)보다 own 18 simple-stack C2.4 strict PASS rate가 높다. pre-train 단계는 일반 지식 + 한국어 fluency, SFT 단계는 prompt-response mapping 학습 — 단계 분리가 학습 효율과 신호를 명확히 한다.

## Why

- **BG-HA failure 교훈**: mixed corpus (knowledge text + chat-template ≥30%) pre-train only → 두 신호 (LM + chat-format) 충돌, 어느 쪽도 충분히 학습 X
- **two-stage advantage**: stage1 pre-train (KO knowledge fluency) + stage2 SFT (prompt-response behavior) 신호 분리
- **literature precedent**: GPT-3 + InstructGPT, LLaMA + Alpaca/Vicuna, T5 + FLAN — large-model 표준 pipeline. small-model 18M scale에서 동일 효과 검증 미land
- **사용자 directive '교훈으로 새로운 패러다임도 도전'** = pre-train+SFT 분리 paradigm 시도

## Predictions

- **H94.1 (sequential vs mixed)**: pre-train(stage1) → SFT(stage2) 18M model이 mixed-corpus pre-train-only 18M (BG-HA baseline)보다 C2.4 strict PASS rate ≥20pp 높다
- **H94.2 (stage1 KO fluency)**: stage1 후 LM val_loss on KO Wikipedia eval이 baseline mixed보다 낮다 (knowledge fluency 분리 효과)
- **H94.3 (stage2 chat alignment)**: stage2 후 own 18 C2.2-C2.4 strict 모두 monotonic 상승 (stage2 epoch 0/1/2/3에서 PASS rate trajectory)
- **H94.4 (stage2 corpus quantity)**: stage2 SFT corpus ≥10MB chat-format 충분 (vs SFT-only H_093 25MB threshold) — stage1이 base fluency 제공
- **H94.5 (catastrophic forgetting)**: stage2 후 stage1 KO Wikipedia eval val_loss 증가 ≤10% (forgetting bound)

## Variables

- **axis1_paradigm**: [mixed_pre_train_only, two_stage_pre_then_sft, sft_only]
- **axis2_capacity**: [18M, 100M]
- **axis3_stage1_corpus_mb**: [50, 250, 1000]
- **axis4_stage2_sft_mb**: [5, 25, 100]
- **axis5_lr_ratio_stage2_to_stage1**: [0.1, 0.3, 1.0]
- **axis6_eval**: [own_18_full + KO_Wiki_val_loss + chat_format_val_loss]
- 3×2×3×3×3×6 = 972 cell; Phase 1 minimal (axis1=2 + axis2=18M + axis3=250MB + axis4=25MB + axis5=0.3 + axis6=full = 12) target

## Run Protocol

- deterministic seed=fnv(axes+rep_id)
- hexa_only: true; training transient_py opt-out (`tool/transient_py/anima_two_stage_*.py`)
- LLM: none (raw#12 strict)
- per-cell ledger: state/<bg>_two_stage_<date>/{stage1.log, stage2.log, verdict.json, eval_log.jsonl}
- 본 cycle 18M scope; 100M+은 별도 cycle (own 16 watchdog)
- evaluator V2 strict mandate

## Criteria

- **C1 (paradigm comparison strict)**: two-stage C2.4_strict_v2 PASS rate ≥ mixed-only PASS rate + 20pp at 18M (H94.1)
- **C2 (stage1 KO fluency)**: stage1-only KO Wiki val_loss < mixed-corpus pre-train val_loss (signal decoupling 증거)
- **C3 (stage2 trajectory)**: epoch 0/1/2/3 monotonic C2.4 PASS rate 상승
- **C4 (forgetting bound)**: stage2 후 KO Wiki val_loss 증가 ≤10%
- **C5 (own 19/20 정합)**: stage1 corpus_hangul_ratio ≥60% AND stage2 chat_format_ratio ≥80%
- **verdict_rule**: SUPPORTED = C1+C2+C3+C4 ALL PASS; PARTIAL = 3/4; MIXED = 2/4; FALSIFIED = ≤1/4

## Falsifiers

- **F1**: two-stage C2.4 strict PASS rate ≤ mixed-only baseline → H94.1 FALSIFIED
- **F2**: stage1 KO Wiki val_loss ≥ mixed-corpus baseline → H94.2 FALSIFIED (decoupling 무효)
- **F3**: stage2 trajectory non-monotonic (epoch 2 < epoch 1) → H94.3 FALSIFIED
- **F4**: stage2 후 KO Wiki val_loss 증가 >25% → H94.5 FALSIFIED (catastrophic forgetting 심각)
- **F5**: SFT-only (H_093 동급) PASS rate가 two-stage보다 같거나 높음 → H94 own merit 부재
- **F6**: post-hoc lr/epoch tuning → raw#12 violation, raw#82 retraction

## Honest Limits (raw#91 c3, ≥5)

- **L1**: 18M scale에서 large-model two-stage pipeline 효과 transfer 가정 (literature는 7B+) — small-scale validation 미land
- **L2**: catastrophic forgetting 측정은 single eval set (KO Wiki) 한정 — multi-domain forgetting bound 미land
- **L3**: stage2 lr ratio 0.3 임의 — sweep 미land
- **L4**: SFT corpus 'instruction quality' 측정 spec 미land (instruction diversity / verb coverage / domain breadth)
- **L5**: total compute = stage1 + stage2 합산이 mixed-only single-stage보다 ≥1.5× 큼 — 동일 budget 비교는 별도 control
- **L6**: 100M+ scale은 own 16 H100 cost discipline scope OUT
- **L7**: stage2 SFT data와 evaluator prompt domain 정합 risk (data leak) — held-out eval set 분리 mandate

## Cross-Links

- **sister roadmaps**: `.roadmap.law` R1 + `.roadmap.philosophy` D4 + `.roadmap.clm_native_chat`
- **raw**: raw#12 + raw#10 + raw#9 + raw#15 + raw#37
- **own**: own 17 + own 18 + own 19 + own 20 + own 21
- **sister H**: H_005 + H_093 (SFT-only) + H_095 (DPO/RLHF) + H_098 (persona) + H_101 (chat ≥80%)
- **evidence motivation**: `docs/anima_own_18_c2_4_evaluator_flaw_2026_05_07.md`

## Verdict

```
status: seed-pending
verdict_class: TBD
evidence_summary: not_yet_run
falsifiers_triggered: none
criteria_met: not_yet_run
next_cycle: BG-HF/HG/HH lane — two-stage 18M cycle
artifact_paths: pending
```
