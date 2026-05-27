# BG-IY — V4 ceiling calibration probe (Polyglot-Ko-1.3B + cached foundation LMs)

> raw#15 additive on docs/anima_chat_cap_lesson_summary_2026_05_07.md + .roadmap.clm_native_chat
> raw#37 transient_py opt-out (zero-shot probe; no training)
> raw#42 N=1 (single seed per model × mode; calibration intent)

## Mission

Disambiguate two hypotheses for 22+ BG cumulative chat-cap failure:
- **H_A capacity gap**: 18M-150M params < empirical emergence threshold (~1B)
- **H_B evaluator self-impossibility**: V4 strict rejects all responses including known-good 1B+ KO LMs

## Method

Zero-shot inference on pretrained foundation LMs (NO training). Same 15 prompts as BG-HS R1. Run V3 6-cell + V4 7-cell strict on outputs.

### Models (ordered cheapest-first)

| order | model | params | KO axis | cached |
|---|---|---|---|---|
| 1 | Qwen/Qwen2.5-1.5B | 1.5B | multilingual | ✅ |
| 2 | Qwen/Qwen2.5-0.5B | 0.5B | multilingual | ✅ (sanity floor) |
| 3 | meta-llama/Llama-3.2-3B-Instruct | 3B | multilingual + instruction-tuned | ✅ |
| 4 | skt/kogpt2-base-v2 | 125M | KO-only GPT-2 | ✅ (architectural baseline) |
| 5 | EleutherAI/polyglot-ko-1.3b | 1.3B | KO-specialized | downloading bg |

### Prompts (15)

5 std + 5 identity + 5 ubm — extracted from `state/anima_id_bghs_r1_replicate_train_2026_05_07/eval_log.jsonl` unique set. Saved at `prompts_15.json`.

### Generation modes

- greedy (do_sample=False)
- sample (temperature=0.7, top_p=0.9, top_k=50)
- max_new_tokens=96, single seed (default)

### Eval

- V3 6-cell strict (`tool/transient_py/anima_simple_stack_evaluator_v3.py`)
- V4 7-cell strict (`tool/transient_py/anima_simple_stack_evaluator_v4.py`)
- per-model summary: V2/V3/V4 PASS counts × {greedy,sample} × {std,identity,ubm}

## Falsifiers

- **F-IY-1**: any model achieves V4 ≥ 7/15 stable + zero cycle + manual ≥ 10/15
  → V4 is internally consistent; capacity gap (H_A) confirmed; foundation-borrow paradigm validated → Stage 1 (LoRA on anima persona corpus)
- **F-IY-2**: NO model (incl. Llama-3.2-3B-Instruct) reaches V4 ≥ 5/15
  → V4 self-impossibility (H_B) — V5/V6 strict will never PASS at any scale → evaluator redesign mandatory before any training
- **F-IY-3 (mixed)**: 3B passes but 0.5B/1.5B fail
  → emergence threshold ∈ (1.5B, 3B) for instruction-tuned KO chat-cap → anima needs ≥ 3B foundation borrow OR distillation

## Outputs

```
state/anima_iy_v4_calibration_polyglot_2026_05_07/
  spec.md                       (this file)
  prompts_15.json
  eval_log_qwen25_1p5b.jsonl
  eval_log_qwen25_0p5b.jsonl
  eval_log_llama32_3b_instruct.jsonl
  eval_log_kogpt2_base_v2.jsonl
  eval_log_polyglot_ko_1p3b.jsonl     (after download)
  v4_results_*.jsonl
  v4_summary_*.json
  v3_results_*.jsonl
  v3_summary_*.json
  verdict.json                  (final IY classification F-IY-1/2/3)
```

## Cost

- Qwen2.5-1.5B Mac MPS: ~2-3 min
- Qwen2.5-0.5B Mac MPS: ~1 min
- Llama-3.2-3B-Instruct Mac MPS: ~5-8 min
- KoGPT2 Mac MPS: ~30s
- Polyglot-Ko-1.3B Mac MPS: ~3-4 min (after ~5 min download)
- V4 eval: ~30s/model
- **Total Mac MPS budget: ~30 min**, **$0** (no H100)

## Cross-links

- ledger: `state/anima_model_attempts_ledger.jsonl` BG-IY attempt entry (paradigm=v4-zero-shot-foundation-calibration, training_steps=0)
- gap analysis source: `docs/anima_chat_cap_gap_analysis_2026_05_07.md` (axis 8 evaluator gap; this BG closes it)
- 20-BG cumulative archive: `docs/anima_chat_cap_20bg_cumulative_negative_archive_2026_05_07.md` (axis 8 mandate)

## Honest C3

1. zero-shot only — no LoRA / SFT on anima persona corpus
2. Mac MPS dtype=fp16 may have slightly different greedy than fp32 baseline
3. anima system prompt (single line) — system-prompt sweep not done
4. single seed per model — variance not bracketed
5. Polyglot-Ko-1.3B HF cache may differ from canonical first-load weights
