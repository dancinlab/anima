# P9 P1.6 ablation_B 4-seed holdout-500 verdict — LANDED 2026-05-03

## TL;DR

**Verdict: SEED_LUCK_VARIANCE.** The s42 outlier (BLEU-1 0.0120, ROUGE-L 0.0118 — ~2x ablation_A floor) does **not** survive a 4-seed ensemble. Three additional seeds (s43, s44, s45) cluster at the noise floor (BLEU-1 0.0062–0.0075). 4-seed mean 0.0081 ± 0.0026 (cv 0.323) fails the cv < 0.30 "real lift" threshold on both BLEU-1 and ROUGE-L.

`b_s46` savepoint was never trained on ubu1 — per task spec we report 4-seed not 5-seed and do **not** retrain. (Marker: `state/markers/p9_p1_holdout500_5seed_landed.marker`.)

## Inputs

- Driver (ubu1): `/tmp/p9_p1_holdout500_reeval_v2.py`
  - Mirror in repo: `/Users/ghost/core/anima/state/p9_p1_holdout500_reeval_2026_05_03/p9_p1_holdout500_reeval_v2.py`
  - 9 ckpts × 6 metrics (BLEU-1/2/3, ROUGE-1/L, chrF), token persistence on, T=64, F1_GEN_LEN=32, greedy.
- Holdout: `/tmp/p9_p1_sft_data_holdout_500_augmented.jsonl` (n=499 after empty-completion drop)
- Llama-3.2-3B anchor: `/tmp/p9_p1_pre1_llama_gold.jsonl` (sentencepiece-tokenized, truncated to 32 tokens)
- Per-prompt outputs (mirrored to Mac): `/Users/ghost/core/anima/state/p9_p1_holdout500_reeval_2026_05_03/v2_per_prompt/`
- Consolidator: `/Users/ghost/core/anima/state/p9_p1_holdout500_reeval_2026_05_03/build_verdict_5seed.py`
- Final verdict JSON: `/Users/ghost/core/anima/state/p9_p1_holdout500_reeval_2026_05_03/verdict_5seed.json`

## Full 9-ckpt × 2-metric matrix (n=499)

| ckpt                | BLEU-1   | ROUGE-L  | chrF     | notes |
|---------------------|----------|----------|----------|-------|
| phase1_5            | 0.005636 | 0.005449 | 0.017652 | prior baseline |
| phase1_6            | 0.006388 | 0.006257 | 0.019475 | sentinel |
| phase1_8            | 0.006263 | 0.006045 | 0.023806 |  |
| ablation_A          | 0.006513 | 0.006533 | 0.021854 | non-B floor |
| **ablation_B (s42)**| **0.011961** | **0.011762** | **0.034110** | **outlier** |
| y1                  | 0.005949 | 0.005945 | 0.018449 |  |
| ablation_B_seed43   | 0.006764 | 0.006728 | 0.024605 |  |
| ablation_B_seed44   | 0.006200 | 0.006154 | 0.023492 |  |
| ablation_B_seed45   | 0.007515 | 0.007204 | 0.023027 |  |
| ablation_B_seed46   | —        | —        | —        | savepoint missing |
| Llama-3.2-3B anchor | 0.382160 | 0.321404 | 0.372875 | reference |

## 4-seed B ensemble stats (s42, s43, s44, s45)

| metric  | mean    | std     | min     | max     | cv    | cv<0.30? |
|---------|---------|---------|---------|---------|-------|----------|
| BLEU-1  | 0.008110 | 0.002624 | 0.006200 | 0.011961 | 0.323 | **fail** |
| ROUGE-L | 0.007962 | 0.002569 | 0.006154 | 0.011762 | 0.323 | **fail** |
| chrF    | 0.026309 | 0.005243 | 0.023027 | 0.034110 | 0.199 | pass     |

Spec required cv < 0.30 across both BLEU-1 and ROUGE-L → **SEED_LUCK_VARIANCE**.

## Lift vs ablation_A (non-B floor)

- BLEU-1: A=0.006513, B 4-seed mean=0.008110, delta=+0.001597 (ratio 1.245x)
- ROUGE-L: A=0.006533, B 4-seed mean=0.007962, delta=+0.001429 (ratio 1.219x)

Residual ~1.2x lift, but the spread (s42 ≈ 2x s44) dominates the signal — not stable enough to call a real axis effect by the spec's variance criterion.

## Lift vs phase1_5 prior

- BLEU-1: p1.5=0.005636, B 4-seed mean=0.008110, delta=+0.002474
- ROUGE-L: p1.5=0.005449, B 4-seed mean=0.007962, delta=+0.002513

Same story: small mean lift inside seed-noise envelope.

## Interpretation

1. **s42 was a lucky seed**, not evidence of an axis-B mechanism. The 4-seed cv 0.32 means one of every ~3 runs lands ~2x the others; this is consistent with Bernoulli-like reward sparsity at this BLEU-1 floor (frac_pos < 5% on holdout-500), where a handful of high-scoring prompts can swing the mean.
2. **chrF (cv 0.20) is the most stable metric** at this scale because it is character-level and captures fragmentary partial matches that token-level BLEU/ROUGE miss. If we were redesigning the verdict criterion at the noise floor we should weight chrF higher than BLEU-1.
3. **All non-Llama ckpts cluster in 0.005–0.012 BLEU-1** — vs Llama anchor 0.382 (~50–70x). This re-confirms the φ★ model is well below the noise threshold required to discriminate between training axes on holdout-500. The "real lift" question on this benchmark is unanswerable until the underlying generation quality clears ~0.05+ BLEU-1.
4. **No retrain.** Per task spec, b_s46 was not retrained; we report 4-seed and accept reduced statistical power.

## Constraints honoured

- raw#9 (.py only on ubu, hexa-style consolidation on Mac): driver lives at `/tmp/p9_p1_holdout500_reeval_v2.py` on ubu1; consolidator + verdict JSON on Mac.
- raw#10 (honest about noise floor): verdict explicitly returns SEED_LUCK_VARIANCE rather than over-claiming a 1.2x lift.
- raw#15 (no rewrite): used the existing v2 driver as-is; only added a verdict consolidator.
- $0 cost (ubu1 local, RTX 5070 sm_120, venv_orchestrator torch 2.11.0+cu128).

## Next options (not executed)

If 5-seed power is needed for a decisive verdict:
1. Train b_s46 on ubu1 (single LoRA, ~1h), re-eval, re-run consolidator → 5-seed cv (likely still > 0.30).
2. Switch verdict metric to chrF (cv 0.199) → would currently flip to "real lift" — but requires explicit spec change.
3. Move to a higher-signal benchmark (post-warmup MMLU subset or NB-style multi-step prompts) before claiming axis effects.

Recommendation by 완성도 lens: **(3) > (1) > (2)**. (3) addresses the root cause (BLEU-1 floor too low to discriminate); (1) is more data on the same too-noisy metric; (2) silently changes the rules.
