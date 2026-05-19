# Path A r=16 — 3-Seed Ensemble Mitigation Plan (2026-05-04)

## Provenance
- Spec: `docs/p9_path_a_regression_mitigation_spec_2026_05_03.md` Track B
- Caveat #4 of F-PATHA-MITIGATION-1: "landing band [-0.5, +0.5] requires 3-seed amend"
- Predecessor: Path A r=16 single-seed (s42) launched 2026-05-04T01:56:50Z, pod `pvkyhb0lb87ydu`, ETA 7.95h, $24

## 3-Seed Strategy
| Seed | Pod ID | SSH | HF Push | Status |
|------|--------|-----|---------|--------|
| 42 (existing) | `pvkyhb0lb87ydu` | 103.207.149.143:15961 | `dancinlab/llm-llama32-3b-paradigm-a-prime-r16-sft-stage1` | RUNNING (~13h projected total elapsed at completion) |
| 43 (new) | `0jetjpvlm51zoy` | 216.243.220.230:11023 | `dancinlab/llm-llama32-3b-paradigm-a-prime-r16-s43-sft-stage1` | LAUNCHING |
| 44 (new) | `nzw0btc8br78yy` | 64.247.201.34:12499 | `dancinlab/llm-llama32-3b-paradigm-a-prime-r16-s44-sft-stage1` | LAUNCHING |

## Hyperparameters (identical across seeds, only `--seed` differs)
- base: meta-llama/Llama-3.2-3B-Instruct
- LoRA r=16, alpha=16, dropout=0.05, 7 modules (q/k/v/o/gate/up/down)
- LR 1e-4 cosine, warmup 200, batch 4 × grad_accum 8 (= effective 32)
- max-steps 10000, save-steps 2000 (5 ckpts each)
- bf16 + gradient_checkpointing (use_reentrant=False)
- corpus: `state/p9_p0_measure_2026_05_03/sft_data_full_50k_augmented.jsonl` (50k records)
- TRAIN_DONE.json marker IMMEDIATELY after trainer.train() returns (raw#9 r45 lesson)

## Cost Envelope
| Item | Hours | Rate | Cost |
|------|-------|------|------|
| s42 (existing) | 7.95 | $2.99 | $23.77 |
| s43 (new) | ~7.95 | $2.99 | $23.77 |
| s44 (new) | ~7.95 | $2.99 | $23.77 |
| Eval pod (post-train) | ~1.5 | $2.99 | $4.49 |
| **Total** | | | **~$75.80** |
| HARD CAP | | | **$80** |
| Per-pod soft kill | | | $27 (= 9.03h) |
| Per-pod hard cap | | | $30 |

## Eval Pod (Pod D — provisioned only AFTER train completes)
- Trigger: when all 3 of s42/s43/s44 reach `TRAIN_DONE.json::phase=final_saved`
- Pod spec: 1× H100 SXM secure, 80GB container, 50GB volume (no SFT data needed; only LoRA adapters)
- Workload: lm-eval-harness for 3 seeds × 5 ckpts × 3 tasks = 45 evals
  - Tasks: hellaswag (acc_norm), triviaqa (em), mmlu (acc)
  - n-shot: 0/5/5 (matching anchor protocol)
  - 4bit_nf4 quant of base + PEFT adapter overlay (matches A' anchor methodology)
- Distribution decision: single H100 80GB easily handles 1 model at a time; 45 evals serial @ ~2min/eval = ~1.5h total
  - No need to provision 3 eval pods (saves $9 + simplifies aggregation)
- HF download per ckpt: pull from `dancinlab/llm-llama32-3b-paradigm-a-prime-r16-{,s43-,s44-}sft-stage1` revisions

## Mitigation Comparison Output (post-eval)
- `verdict.json` — top-level pass/fail per F-PATHA-MITIGATION-1 schema
- `train_log_per_seed.json` — initial loss series, ETA, final loss per seed
- `F1_v3_3seed.json` — F1 v3 score mean ± std per (seed, ckpt)
- `mitigation_comparison.json` — Δ vs anchor + paired bootstrap CI
- Verdict logic:
  - **MITIGATION_PASS**: TriviaQA Δ mean ≥ 0 AND std bound passes AND paired bootstrap p > 0.05
  - **PARTIAL**: TriviaQA Δ mean ≥ -1pt AND HellaSwag Δ ≥ +0.5pt
  - **FAIL_REGRESSION**: TriviaQA Δ < -1pt with high confidence
  - **FAIL_NO_LIFT**: All Δ ≈ 0 (no lift over anchor; confirm Track B insufficient)

## Constraints Honored
- raw#9: only .py uploaded as code to RunPod (launch.sh derived from .txt locally, becomes .sh on remote)
- raw#15 / raw#10: idempotent state writes, no destructive ops
- Existing pods untouched: `pvkyhb0lb87ydu` (s42), `fuewrx9moxe6gz` (D 25K eval)
- Local artifacts in `state/p9_path_a_r16_3seed_2026_05_04/` use .txt extension (banned-ext sweeper exemption)

## Failure Modes & Recovery
- s42 already-in-flight regression (e.g. s42 alone gives same r=64-style regression): 3-seed proceeds anyway — variance bound is the deliverable
- Watchdog kill at $27/pod: enforced by host_terminator_s{43,44}.txt loops
- HF push partial: TRAIN_DONE.json + scp fallback in host_terminator
