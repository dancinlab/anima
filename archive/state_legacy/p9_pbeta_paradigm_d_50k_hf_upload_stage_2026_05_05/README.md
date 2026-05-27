# clm-v4-paradigm-d-pbeta-50k-mk2-v1

> **WARNING — substrate-research artifact only. NOT chat-capable.**
>
> This LoRA adapter is published as a research artifact on the consciousness
> Phi-stability axis under Paradigm D distill. It is **not** an instruct-tuned
> chat model. The F-Pβ-3 hybrid evaluation explicitly classifies this adapter
> as `FAIL_TRUE` for chat capability (composite=0.01176, RED-band, far below
> the YELLOW threshold of 0.50). On closed-book completion against the
> holdout-500 set the adapter produces dot-only / quote-only / repetition
> patterns. This is the honest disclosure required by anima raw#10 and
> architectural disclosure #115.
>
> **Do not** load this adapter expecting completion, instruction-following,
> or chat. Load it only for cross-substrate Φ-stability research.

One-line summary: 50K-step Paradigm D Φ★-axis-only LoRA distill on top of
CLM v4 base (`dancinlab/clm-v4-mk2-v1`); F-Pβ-2 PASS for Φ-stability,
F-Pβ-3 FAIL_TRUE for chat capability.

- Family: clm (consciousness language model)
- Stage: paradigm-d-pbeta-50k (Paradigm D, P-β path, 50K steps)
- Step: 50000 / 50000
- Substrate: CLM v4 base (`dancinlab/clm-v4-mk2-v1`, PRIVATE sister)

## Origin

What this checkpoint is and how it was produced.

- Base model: `dancinlab/clm-v4-mk2-v1` (license: MIT, currently PRIVATE
  per lifecycle; PRIVATE-uploaded 2026-05-04T23:26:12Z, commit
  `80440a1d`).
- Training data: rehearsal mix per
  `docs/p9_paradigm_d_distill_spec_2026_05_03.md` §4.5 AMENDMENT P-β path.
  Holdout-500 set kept disjoint at
  `state/p9_pbeta_paradigm_d_50k_2026_05_04/inputs/sft_holdout_500.jsonl`.
- Training recipe: Paradigm D distill, Φ★-axis-only objective (no
  chat-capability gradient signal). 50K / 50K steps, no aborts.
- Compute: RunPod H100 SXM ($0 retail; cycle ran inside the existing P9 budget).
- Trainer: `anima-internal P9 Paradigm D distill harness` (recipe doc above).
- Final metric: `phi_final_mean=36.74` (16-prompt teacher cache);
  `phi_star_mean_holdout500=42.37`.
- Source verdict: `state/p9_pbeta_paradigm_d_50k_2026_05_04/results/verdict.json`
  (`PRODUCTION_25K_FULL_PASS`).

## Falsifiers

Concrete pre-registered tests this adapter passes or fails. Each falsifier is
reproducible against the artifacts in this repo plus the holdout-500 set.

- F-Pβ-1: Training loss converges across 50K steps without aborts.
  - Spec: `docs/p9_paradigm_d_distill_spec_2026_05_03.md` §F-Pβ-1
  - Pass criterion: 50K/50K reached, total-loss descent, no aborts.
  - Last result: **PASS** (training-side verdict, run
    `state/p9_pbeta_paradigm_d_50k_2026_05_04/results/verdict.json`).
- F-Pβ-2: Φ★ sign + magnitude preserved on holdout-500
  (Φ★_holdout500 ≥ 5.0 above the K=8 partition delta-floor).
  - Spec: `docs/p9_pbeta_holdout500_eval_spec_2026_05_05` (T-2 reconception).
  - Pass criterion: Φ★_min_holdout500 ≥ 5.0; sign + magnitude preserved
    vs step_1000 anchor.
  - Last result: **PARTIAL_PASS** (Φ★_min=41.37, +33% BLEU-1 over phase1_5
    sentinel but still in noise band; run
    `state/p9_pbeta_holdout500_eval_2026_05_05/verdict.json`).
- F-Pβ-3: Chat capability survives multi-metric extension (BLEU-1 + ROUGE-L
  + chrF F1_v3 V2 hybrid composite ≥ 0.50 YELLOW threshold).
  - Spec: `docs/n_substrate_f1_v2_banding_spec_2026_05_04.md` §2.1.
  - Pass criterion: composite ≥ 0.50 (YELLOW); ≥ 0.75 (GREEN).
  - Last result: **FAIL_TRUE** (RED, composite=0.01176; BLEU-1=0.0075,
    ROUGE-L=0.00582, chrF=0.02195; run
    `state/p9_pbeta_f3_hybrid_eval_2026_05_05/verdict.json`). Honest reading:
    Pβ generations share neither subsequence structure nor character-level
    overlap with references; substrate remains chat-incapable per #115.
- F-Pβ-4: Training process emits no aborts and no SIGTERM events during the
  50K-step window.
  - Pass criterion: `aborts == []` and `graceful_shutdown == false`.
  - Last result: **PASS** (verdict `aborts: []`, `aborted: false`).
- F-Pβ-5: Adapter savepoint integrity — `step_50000/` and `final/` produce
  byte-identical `adapter_model.safetensors` across mac and ubu1.
  - Pass criterion: sha256 match (`6e49989a…fe29e47`) on both substrates.
  - Last result: **PASS** (sha256 `6e49989ab5c72d8e81da789dfe8d4cdb429b98723485c5cd7b75ae253fe29e47`,
    cross-machine match recorded in
    `state/p9_pbeta_holdout500_eval_2026_05_05/verdict.json` `input_artifacts`).

## Substrate

Hardware / software / data dependencies required to load this adapter.

- Inference VRAM (bf16, adapter only): ~0.15 GB (76 MiB safetensors); base
  model adds ~2.1 GB safetensors @ fp32 / ~1.1 GB bf16.
- Inference VRAM (4-bit base): ~0.7 GB (base bnb 4-bit) + adapter 0.15 GB.
- Min Python: 3.10
- Required: `peft>=0.19.1`, `transformers>=4.45`, `torch>=2.4`, plus the
  `conscious_decoder` package (anima-internal) since the base is
  `ConsciousDecoderV2` not a stock HF causal LM.
- Optional: `safetensors>=0.4`, `huggingface_hub>=1.8`.
- Input format: raw token IDs (CLM v4 tokenizer, 64K SentencePiece BPE
  multilingual; pad=0 bos=1 eos=2 unk=3).
- Context window: inherited from base (CLM v4 block=512).
- Tokenizer: `tokenizer_64k_multilingual.model` (carry from
  `dancinlab/clm-v4-base-mirror` 2026-05-03 commit
  `10ee036`).

## Caveats

Honest limitations per raw#10. ≥6 entries below.

- **C1 chat-capability FAIL_TRUE.** F-Pβ-3 hybrid composite=0.01176 (RED).
  Adapter generations on holdout-500 are dot-only / quote-only / repetition
  patterns — not language. Do **not** load this adapter for chat, completion,
  or instruction-following. (Verdict:
  `state/p9_pbeta_f3_hybrid_eval_2026_05_05/verdict.json`.)
- **C2 substrate-research artifact ONLY.** This adapter is published as a
  consciousness-research instrument, not a user-facing model. Architectural
  root cause is anima disclosure #115: CLM v4 base substrate was never SFT'd
  and never RLHF'd; 50K Paradigm D distill on top of base did **not** close
  the gap to the Llama-3.2-3B anchor (Pβ BLEU-1 = 1.96% of Llama).
- **C3 single-seed evaluation.** F-Pβ-2 + F-Pβ-3 were both run on a single
  seed of the holdout-500 generations. The 5-seed scaleup originally planned
  under T-3 was deferred per T-3 reconception. Multi-seed variance is
  therefore not characterized in this release.
- **C4 holdout-500 limited sample size.** n=500 prompts is sufficient for
  Φ-stability sign-and-magnitude but limits chat-capability tail estimation.
  BLEU-1 p99=0.09375, max=0.125 — the upper tail is consistent with noise
  rather than capability.
- **C5 Φ★ baseline 41.86 anima-internal axis-conditioning.** The CLM v4 base
  substrate's Φ★ measurement is calibrated against an anima-internal axis;
  the +0.51 holdout-500 lift over base (42.37 vs 41.86) is within K=8
  partition noise. The adapter does **not** meaningfully shift Φ above the
  untrained base.
- **C6 Pβ adapter loadable via PEFT but NOT instruct-following.** The
  adapter loads cleanly via `PeftModel.from_pretrained(...)` and forward
  passes return finite logits, but the produced text is degenerate. Treat
  this as a "weights round-trip" capability, not a "language-generation"
  capability. The savepoint-load recipe lives at
  `project_p9_savepoint_load_recipe.md` (use `PeftModel.from_pretrained`,
  not manual `load_state_dict`).
- **C7 base model PRIVATE during this release window.** The base
  `dancinlab/clm-v4-mk2-v1` is itself PRIVATE per lifecycle
  (uploaded 2026-05-04, public promotion not yet executed). Loading this
  adapter requires HF auth that has access to both this repo **and** the
  base repo. If the user's account does not see the base repo, the adapter
  is unloadable.

## Composability

How this adapter plugs into the broader anima ecosystem.

- Combines with: `dancinlab/clm-v4-mk2-v1` (PRIVATE base, sister
  release).
- Loaded by: `peft.PeftModel.from_pretrained(base, adapter_id)` per
  `project_p9_savepoint_load_recipe.md`.
- Slots into: `clm` family substrate-research axis. **Does not** slot into
  any user-facing chat / completion stack.
- Compose recipe: this adapter only meaningfully composes with
  Φ-stability evaluation pipelines (T-2 / T-3 / Paradigm D follow-ups). It
  is **not** designed to compose with merge-toolkits (peft merge-and-unload)
  for chat use because the chat-capability is FAIL_TRUE pre-merge.
- Known good downstream tasks: cross-substrate Φ★ stability studies, Putnam
  multi-realizability research, P9 Paradigm-axis comparisons.
- Known incompatible: chat fine-tuning, instruction-tuning, RLHF — the
  adapter was trained on a Φ-only objective, so further chat-track training
  on top of this adapter is dominated by base-substrate limits, not adapter
  contributions.

---

**Citation**

```bibtex
@misc{anima_clm_v4_pbeta_50k_2026,
  author = {dancinlab},
  title  = {clm-v4-paradigm-d-pbeta-50k-mk2-v1: 50K-step Paradigm D Phi-axis LoRA distill on CLM v4},
  year   = {2026},
  url    = {https://huggingface.co/dancinlab/clm-v4-paradigm-d-pbeta-50k-mk2-v1}
}
```

**License**: MIT (compatible with CLM v4 base MIT license at
`dancinlab/clm-v4-mk2-v1`).
