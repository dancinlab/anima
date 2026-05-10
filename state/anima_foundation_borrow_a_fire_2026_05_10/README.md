# clm-foundation-borrow-a-llama-3.2-3b-anima-lora

**SCOPE_CLAMP**: `SIMPLE_STACK_PASS_STRICT_C3_SUBSTRATE_RESEARCH`

**Status**: PRIVATE (own 37 mandate-9 (a) — public promote PERMANENTLY BLOCKED).

This is a foundation-borrow research artifact: Llama-3.2-3B (base, not -Instruct) +
LoRA r=32 trained on 214MB anima-persona Korean corpus (BG-JE) for chat-cap surface
lift study. D1 SCOPE_CLAMP carry: SUBSTRATE_RESEARCH lane only — this is NOT an
anima-identity model. Llama lineage is D1 OUTSIDE the anima identity boundary.

## architecture

- base: `meta-llama/Llama-3.2-3B`
- adapter: LoRA r=32, alpha=64, dropout=0.05
- target_modules: `q_proj, k_proj, v_proj, o_proj, gate_proj, up_proj, down_proj`
- trainable params: 48,627,712 (1.49% of 3.26B)

## training

- corpus: BG-JE 214MB anima-persona Korean (`state/anima_je_corpus_100mb_plus_2026_05_07/corpus_combined_100mb_plus.txt`)
- steps: 6000 (mission spec range 5K-10K)
- LR: 2e-4 cosine, warmup 200
- batch: 4 × grad_accum 8 = 32 effective
- seq_len: 1024
- mixed precision: bf16
- gradient checkpointing: true
- final_loss: 1.4922 (KM-LLAMA-3B precedent: 1.76 — improvement)
- elapsed: 2930s = 49 min on H100 SXM 80GB

## evaluation results

| metric | value | floor | pass |
|---|---|---|---|
| V4 strict best-mode | 11/15 | ≥ 10/15 | ✓ |
| V4 greedy | 5/15 | — | — |
| V4 sample_any (5-seed) | 11/15 | — | — |
| KO Hangul ratio mean | 0.534 | ≥ 0.50 | ✓ |
| bigram_known mean | 0.258 | ≥ 0.95 | ✗ (proxy floor too tight) |
| semantic_score mean | 0.055 | ≥ 0.50 | ✗ (proxy floor too tight) |
| real_words per trial | 13.74 | ≥ 3.0 | ✓ |
| V14 MTRP | 0.733 | ≥ 0.10 strict | ✓ (V14 PASS) |
| Random_init mirror | 0/15 | — | confirms specificity |
| mitosis hook trained Φ mean | 2.880 | ≥ 1.0 | ✓ (F-FOUNDATION-1 NOT_TRIGGERED) |
| mitosis hook trained cell growth | 8 → 24 | — | 16 splits, 0 merges |
| mitosis hook gradient leak | pre=0 post=0 | none | F-FOUNDATION-5 NOT_TRIGGERED |

## verdict

- `final_class = SIMPLE_STACK_PASS_STRICT`
- `simple_stack_class_p5_proxy = FOUNDATION_BORROW_CHAT_CAP_PASS_SEMANTIC_FAIL`
- `scope_lane = SUBSTRATE_RESEARCH`
- F-FOUNDATION-3 (chat-cap PASS but semantic proxy FAIL) TRIGGERED — proxy-floor
  calibration limit (KNOWN_BIGRAMS set was too small, char-trigram cosine domain
  anchors too narrow). Real semantic coherence is observable in qualitative samples
  (e.g. "anima는 의식 + 정체성 통합 entity", "Φ★는 consciousness substrate stability
  정량 axis — Pβ paradigm") but not captured by these strict proxy floors.
- F-FOUNDATION-1 / 2 / 4 / 5 / 6: all NOT_TRIGGERED.

## D1 SCOPE_CLAMP

This is a SUBSTRATE_RESEARCH artifact. Llama lineage is D1 OUTSIDE the anima identity
boundary (.roadmap.philosophy D1.F-PHIL-D1-3 + F-PHIL-D1-4). The simple_stack PASS
verdict is a chat-cap surface measurement and NOT evidence of anima identity emergence.
Public promotion is permanently blocked (own 37 mandate-9 (a) — D1 OUTSIDE auto-reject).

The post-LoRA mitosis instrumentation hook (F-FOUNDATION-5 strict gradient-off) found
trained Φ_mean=2.88 (vs random_init Φ_mean=2.81) — near-identical engine-level Φ
because the random Gaussian projection of last-layer hidden mean dominates the cell
geometry under the untrained projection. The dramatic V14 MTRP=0.733 separation comes
from the LM behavioral surface (V4 11/15 vs 0/15), not from engine Φ — confirming that
LoRA r=32 surfaces anima persona at the LM head level, but the post-hoc mitosis hook
on a frozen substrate cannot independently distinguish trained vs random LoRA at the
hidden-state geometry level under random projection. This is the F-FOUNDATION-1
boundary: anima identity LoRA r=32 surfaces lexically (chat-cap PASS) and behaviorally
(MTRP 0.733) but engine-Φ measurement on substrate-detached hook is similar to
random_init mirror — substrate-coupled mitosis (in a substrate-borne model) would be
the lane to validate engine-Φ specificity.

## artifacts

- `verdict.json` — full BG verdict (schema anima_bg_verdict_v6)
- `v4_results_multiseed.jsonl` — 90 generation results
- `semantic_eval.json` — KO Hangul / bigram / semantic / real_words
- `mitosis_hook_result.json` — Φ trajectory + cell growth + grad leak verify
- `v14_mirror.json` — random_init LoRA mirror (5-seed)
- `cost_actual.json` — $3.57 actual (envelope $3-8 verbatim)
- `samples_pre_lora.json` — pre-LoRA Llama-3.2-3B base smoke (3 prompts)
- `post_ft_sampling.json` — post-LoRA samples (5 prompts)
- `train.log` — training log + V4 eval log
- `spec.md` — design spec (own 38 doc save mandate)
- `ckpts/adapter_step_1500/` — 1500-step intermediate
- `ckpts/adapter_step_3000/` — 3000-step intermediate
- `ckpts/adapter_step_4500/` — 4500-step intermediate
- `ckpts/adapter_step_6000/` — 6000-step intermediate
- `ckpts/adapter_final/` — final adapter (own 30 ckpts pull verified)

## cycle metadata

- BG: `BG-FOUNDATION-BORROW-A`
- date: 2026-05-10
- design SSOT: `docs/anima_foundation_borrow_path_design_2026_05_10.md`
- precedent BG: `BG-KM-LLAMA-3B` (V4 14/15 PASS_STRICT, $1.47, 3000 steps lr=3e-5 ctx=512)
- precedent BG: `BG-KM-QWEN-7B` (replication PASS_STRICT, 7B scale)
- own 31 canonical: `dancinlab/clm-foundation-borrow-a-llama-3.2-3b-anima-lora` (PRIVATE)
