# Falsifier set — P9 Path A retrain v2 (LOCKED 2026-05-04, raw#71)

Schema: anima/state/p9_path_a_retrain_v2_spec/falsifier_set/1
Cycle: BG-Φ 2026-05-04
Driver: BG-Ρ Mode 1 eval `state/p9_lora_mode1_eval_2026_05_04/verdict.json`

LOCK statement: F-PA-RETRAIN-v2-1 through F-PA-RETRAIN-v2-4 metric definitions and pass thresholds are pre-registered AT THIS SPEC LANDING. Post-eval threshold tweaks are a verdict-invalidation under raw#71. Append-only audit trail required for any future amendment.

---

## F-PA-RETRAIN-v2-1 — Training loss converges (no diverge)

- **observable**: pod-side `trainer_state.json` log of `train_loss` per logging_step
- **metric**: max-window-increase across 500-step rolling windows after step 1000
- **PASS threshold**: max_window_increase < 0.1 absolute loss across last 4 windows; no NaN/Inf at any step
- **FAIL action**: ABORT pod immediately; cost-trap auto-kill; bug-fix LR or batch size; do NOT push partial ckpt

## F-PA-RETRAIN-v2-2 — Intermediate eval at step 2000: ≤ 5pp drop vs Llama base

- **observable**: intermediate eval JSON emitted at step 2000 (HellaSwag limit=200, lm-eval-harness 0.4.11)
- **metric**: HellaSwag-200 acc_norm at step 2000
- **PASS threshold**: acc_norm ≥ 0.604 (= Llama-3.2-3B non-Instruct base 0.654 − 5pp)
- **FAIL action**: EARLY-STOP retrain; treat as v2-FAIL_EARLY; do not proceed to step 6000; save adapter as `step-2000-aborted` for post-mortem; emit verdict v2-FAIL_EARLY

## F-PA-RETRAIN-v2-3 — Final V2 PASS criterion (Mode 1 eval)

- **observable**: post-train Mode 1 eval verdict.json (Llama-3.2-3B + LoRA-v2, limit=500, seed=42, bf16, lm-eval-harness 0.4.11; separate cycle ~$1.10)
- **metric (C-RV-1 parity floor)**:
  - HellaSwag acc_norm ≥ 0.644 (= base 0.654 − 1pp)
  - MMLU 5-shot acc ≥ 0.5696 (= base 0.5796 − 1pp)
  - TriviaQA EM ≥ 0.376 (= base 0.396 − 2pp)
- **metric (C-RV-2 improvement)**: at least 1 of the 3 benchmarks improves on base by ≥ 2pp:
  - HellaSwag ≥ 0.674 OR MMLU ≥ 0.5996 OR TriviaQA ≥ 0.416
- **PASS threshold**: C-RV-1 (all 3 within parity floor) AND C-RV-2 (≥1 improves by 2pp)
- **PARTIAL**: C-RV-1 PASS but C-RV-2 FAIL (forgetting fixed but no positive contribution)
- **FAIL**: C-RV-1 FAIL on any single benchmark (still degraded)
- **FAIL action**: v2-FAIL → escalate to S5 (paradigm D distillation) or S2 (replay buffer); do NOT post-eval relax thresholds

## F-PA-RETRAIN-v2-4 — Anima-axis preservation

- **observable**: post-train holdout BLEU-1 eval on axis-conditioned prompts (per `state/p9_p1_holdout500_reeval_2026_05_03/` framework; ~$1, separate cycle)
- **metric**: BLEU-1 (smoothed method1, lowercase whitespace tokenization) on holdout-500 axis-conditioned prompts
- **PASS threshold**: v2 BLEU-1 ≥ v1 step-8k LoRA BLEU-1 (anchor TBD by v1 measurement; preregistered as ratio ≥ 1.0)
- **FAIL action**: v2-PARTIAL_AXIS_LOST (forgetting fixed but axis lost); reduce academic % from 30→20 in v3 cycle

---

## Verdict logic table

| F-PA-RETRAIN-v2-1 | F-PA-RETRAIN-v2-2 | F-PA-RETRAIN-v2-3 | F-PA-RETRAIN-v2-4 | Overall verdict |
| --- | --- | --- | --- | --- | --- |
| FAIL | — | — | — | TRAIN_DIVERGE_ABORT |
| PASS | FAIL | — | — | EARLY_STOP_v2_FAIL |
| PASS | PASS | PASS (C-RV-1+C-RV-2) | PASS | **V2_PASS** |
| PASS | PASS | PARTIAL (C-RV-1 only) | PASS | V2_PARTIAL_NO_IMPROVEMENT |
| PASS | PASS | PASS | FAIL | V2_PARTIAL_AXIS_LOST |
| PASS | PASS | FAIL | * | V2_FAIL_FORGETTING_PERSISTS |

---

## Pre-registration anchor table

Source: `state/p9_base_validation_llama_anchor_2026_05_04/verdict.json` (BG-Ο, 93bef8c8)

| Benchmark | Llama base | F-PA-RETRAIN-v2-3 parity floor | F-PA-RETRAIN-v2-3 improvement bar |
| --- | --- | --- | --- |
| HellaSwag acc_norm (0-shot) | 0.654 | 0.644 (−1pp) | 0.674 (+2pp) |
| MMLU 5-shot acc | 0.5796 | 0.5696 (−1pp) | 0.5996 (+2pp) |
| TriviaQA EM (0-shot, remove_whitespace) | 0.396 | 0.376 (−2pp) | 0.416 (+2pp) |

Comparison anchor for F-PA-RETRAIN-v2-2: HellaSwag-200 (limit=200, faster proxy) vs same 0.654 base.

---

## Escalation chain

- v2-PASS → land verdict; advance F1_v3 V2 to SUCCESS_WITH_IMPROVEMENT; close .roadmap.p9_sft cond.path_a_retrain_v2
- v2-PARTIAL_NO_IMPROVEMENT → spec a v3 with S5 (distillation) or stronger rehearsal mix (50/40/10); cost $30-50
- v2-PARTIAL_AXIS_LOST → spec a v3 with reduced academic % (20% instead of 30%); cost band same $20-30
- v2-FAIL → escalate strategy entirely (S2 replay buffer or S5 distillation); evaluate against external r=16 result first
- TRAIN_DIVERGE_ABORT → pre-EXEC config error; fix and re-launch (no full v3 cycle)
- EARLY_STOP_v2_FAIL → step-2000 adapter saved for post-mortem; v3 must reduce academic % or LR further
