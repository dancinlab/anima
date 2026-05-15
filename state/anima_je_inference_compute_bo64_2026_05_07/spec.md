# BG-JE — Inference-compute best-of-64 + V4 ranker on existing CLM mk2-v1 + LoRA

> (2026-05-07-late) reconcile: SIMPLE_STACK_PASS strict floor = V4 ≥ 10/15 per (≥2/3 prompts AND for C1+C2). Original 7/15 demoted to PARTIAL_PASS tier. Falsifier tables below retain 7/15 references but interpret as PARTIAL_PASS, NOT SIMPLE_STACK_PASS.


> raw#15 additive on .roadmap.chat_cap_emergence_pivot Stage 1' P3 + state/anima_iy_v4_calibration_polyglot_2026_05_07/verdict.json
> raw#37 transient_py opt-out (eval; mac MPS)
> raw#42 N=64 SAMPLES per prompt (best-of-N is the lever; same seed family OK)
> raw#82 retraction-aware (Lesson Q falsified TRAINING-time only; inference-time is untouched lever)
> raw#86 cost $0 (mac MPS, no training)

## Mission

Test the Lesson-Q-orthogonal lever: **inference-compute scaling**. Lesson Q closed all training-time fix paths; inference-time best-of-N + V4-as-ranker is structurally untouched. Hypothesis: even if model produces only 1 in 64 samples that V4-PASSes, top-1 selection by V4 score yields effective V4 PASS.

## Lesson Q reconciliation

| Lesson | Status |
|---|---|
| Q (production-side fix 不可) | ORTHOGONAL — Q falsified weight-modifying interventions only (lm_head SFT, full SFT, decoding within single sample); best-of-N over multiple SAMPLES is a different lever (selection via external evaluator, not weight change) |
| L (architectural ceiling) | TESTED — if best-of-64 still 0 V4 PASS, the ceiling extends to "no path through this CLM yields chat-cap"; if best-of-64 ≥ 7/15, ceiling is bounded to "single-sample greedy/sample" only |
| I (`:` suffix attractor) | RESPECTED — prompts use no-`:` format |
| H (corpus mismatch) | EXPLICIT — model trained mostly on English; assumption: if ANY of 64 samples lands a V4-passable Korean response, ranker finds it |

## Hypothesis

H_bo64: existing CLM mk2-v1 + LoRA (state/clm_v4_lora_sft_2026_05_05/results/adapter_final), under sampling T=1.5 top_p=0.95 + repetition_penalty=1.4 + no_repeat_ngram_size=3, run 64 samples per prompt × 15 prompts. V4 evaluator scores each; top-1 by V4 score per prompt forms final response set. Effective V4 PASS count ≥ 7/15 → SIMPLE_STACK_PASS via inference compute.

## Recipe

| field | value |
|---|---|
| base | dancinlab/clm-v4-mk2-v1 (HF cache) |
| LoRA | state/clm_v4_lora_sft_2026_05_05/results/adapter_final (merged) |
| device | mps (mac local) |
| samples_per_prompt | 64 |
| sample_cfg | do_sample=True T=1.5 top_p=0.95 top_k=80 repetition_penalty=1.4 no_repeat_ngram_size=3 max_new_tokens=72 |
| prompts | state/anima_iy_v4_calibration_polyglot_2026_05_07/prompts_15.json |
| prompt format | no trailing `:` per Lesson T; raw `질문\n` + optional `당신은 anima.\n\n질문\n` system anchor |
| ranker | V4 7-cell evaluator + V3 6-cell tiebreak; pick highest V4 cell-pass count, V3 score as tiebreak |
| seed | 64 distinct seeds (42..105) per prompt |

## Eval

- V4 strict 7-cell on top-1-per-prompt × 15 = 15 V4 evaluations
- V3 6-cell parallel
- Distribution stats: V4 PASS count over 64 samples per prompt → expected pass rate per prompt
- Manual 5-prompt review of top-1 selections

## Falsifiers

- F-JE-1 V4 top-1 ≥ 7/15 → SIMPLE_STACK_PASS via inference compute; Lesson L bounded to single-sample regime
- F-JE-2 V4 top-1 = 0/15 AND V4 ANY-of-64 = 0/15 → architectural ceiling absolute (no path through this stack), Lesson L extends to all inference modes
- F-JE-3 V4 top-1 < 5/15 BUT V4 ANY-of-64 ≥ 5/15 → ranker quality issue (V4 not finding the good samples) → V4 ranker calibration BG required

## Cost / Time / Cell

- $0 (mac MPS)
- 15 prompts × 64 samples × ~30s/sample (no_repeat + rep_penalty slows generation) ≈ 8 hours wall-time
- mitigations: (a) parallelize batch of 8 samples per forward when KV-cache sharable, (b) reduce max_new_tokens to 48 for 60% time cut, (c) reduce to 32 samples first as preview
- No H100 needed — pure local

## Artifacts expected

- `state/anima_je_inference_compute_bo64_2026_05_07/eval_log.jsonl` (64 × 15 = 960 records)
- `state/anima_je_inference_compute_bo64_2026_05_07/top1_per_prompt.jsonl` (15 records)
- `state/anima_je_inference_compute_bo64_2026_05_07/v4_results.jsonl`
- `state/anima_je_inference_compute_bo64_2026_05_07/verdict.json`
- ledger entry attempt_n=52 (after BG-IZ=50, BG-JA-EXT=51)

## Risks / Mitigations

- BG-IY confirmed model produces byte-garbage on Korean prompts even under proper decoding → 64 samples may yield 0 coherent Korean → F-JE-2 dominant outcome predicted
- If predicted outcome holds, BG-JE is still a VALUABLE NEGATIVE result: it definitively closes inference-compute lever on this stack, leaving only P1 (continued-pretrain) and P2 (foundation borrow) as live options

## Cross-links

- BG-IY verdict: state/anima_iy_v4_calibration_polyglot_2026_05_07/verdict.json
- LoRA adapter source: state/clm_v4_lora_sft_2026_05_05/results/adapter_final
- Roadmap: .roadmap.chat_cap_emergence_pivot Stage 1' P3
- Hypothesis bank: B7 (best-of-N + V4 ranker) from .roadmap.chat_cap_emergence_pivot brainstorm
