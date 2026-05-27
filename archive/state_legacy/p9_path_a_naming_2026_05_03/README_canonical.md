# llm-llama32-3b-paradigm-a-prime-sft-stage1

One-line summary: Llama-3.2-3B-Instruct + axis-LoRA (rank 64) SFT stage-1 under Paradigm A' (measured-BOLD anchor swap), 50K augmented record corpus, target use = F1_v3 verdict-delta vs Llama base.

- Family: llm (Llama-base lineage; mk2 spec extension — see `## Caveats` C1)
- Stage: sft-stage1 (LoRA r=64, alpha=64, lr=1e-4, max_steps=10000, save_steps=2000)
- Step: tags `step-2k`, `step-4k`, `step-6k`, `step-8k`, `step-10k`, `final`
- Substrate: meta-llama/Llama-3.2-3B-Instruct

## Origin

What this checkpoint is and how it was produced.

- Base model: meta-llama/Llama-3.2-3B-Instruct (license: Llama 3.2 community)
- Training data: `state/p9_p0_measure_2026_05_03/sft_data_full_50k_augmented.jsonl` (~50K records, axis-conditioned, re-templated to Llama chat format)
- Training recipe: `docs/p9_a_prime_path_decision_landed_2026_05_03.ai.md` §7 (Path A LoRA re-train spec)
- Compute: 1× H100 SXM (RunPod pod 29dhlqk508ugoc), wall ~10-20h, $30-85 budget envelope
- Trainer: `train_llama_lora.py` on pod (PEFT + transformers Trainer with `push_to_hub=True`, `hub_strategy=every_save`)
- Final loss / metric: TBD (will be filled at training completion)
- Commit: TBD (will be filled by handoff doc upon completion)
- Cycle land doc: `docs/p9_path_a_naming_decision_2026_05_03.md`

## Falsifiers

Concrete tests this checkpoint either passes or is meant to fail deterministically.

- F-NAME-1: PASS (this README + name conform to mk2 spec §2 EBNF + §5 README template, with C1 caveat about `llm` family extension)
  - Spec: `docs/anima_hf_naming_convention_mk2_spec_2026_05_03.md`
  - Pass criterion: regex match against canonical EBNF + 5 required H2 sections
  - Last result: PASS at pre-create time; re-verify at final upload
- F1_v3 (chat-axis verdict-delta): TBD
  - Spec: `docs/p9_benchmark_switch_a_prime_spec_2026_05_03.md` §2.4
  - Pass criterion: |Llama+LoRA − Llama base| > 3.2% Llama-self baseline on TriviaQA/HellaSwag/MMLU composite
  - Last result: TBD (eval phase post-training)
- F-AXIS-2/3/4 (axis-loss falsifiers): N/A this artifact
  - Spec: `docs/p9_benchmark_switch_a_prime_spec_2026_05_03.md` §3
  - Pass criterion: axis-conditioned loss decrease >1σ vs no-axis ablation
  - Last result: deferred (axis falsifiers were designed for CLM v4 architecture; transfer to Llama is not 1:1)

## Substrate

Hardware / software / data dependencies required to run this checkpoint.

- Inference VRAM (bf16 + LoRA): ~7 GB
- Inference VRAM (4-bit + LoRA): ~3 GB
- Min Python: 3.10
- Required: transformers>=4.45, peft>=0.12, torch>=2.4, bitsandbytes (for 4-bit)
- Optional: flash-attn (for faster inference)
- Input format: Llama chat template (see Llama-3.2 model card)
- Context window: 2048 tokens (training seq_len; base model supports 128K)
- Tokenizer: inherited from meta-llama/Llama-3.2-3B-Instruct (no extension)

## Caveats

Three or more honest limitations (raw#10).

- C1 — `llm` lm-family is an additive extension to mk2 spec §3.1 (originally enumerated `blm | clm | tlm | vlm | slm | nlm`). This artifact's existence as the first `llm-*` repo establishes the family for Llama-base derived models. The mk2 spec freeze prevents in-place edit of the spec table; this README documents the extension. Future ratification requires a follow-up cycle that lands `llm-family` into §3.1.
- C2 — Post-hoc rename risk: the legacy training-time repo name `dancinlab/p9-llama32-lora-stage1` will be renamed to this canonical name via `hf repos move` after training completes. HF preserves URL redirects, but git tags created during training may be retained or lost depending on `hf repos move` semantics on tagged refs. If tags are lost, they must be re-created from commit shas captured in the training log.
- C3 — Single-repo + tags pattern (per mk2 §4.3 second row) was chosen over per-ckpt-repo split because (a) the running pod uses `hub_strategy=every_save` to a single target, (b) preempting training to redirect would have cost ~$50 of progress. This means tag-namespace pollution (5 step-Nk tags + final) lives in one repo; consumers must specify `revision=` to pin a ckpt. If downstream eval requires per-ckpt repo isolation, a follow-up `hf repos duplicate` cycle can split each tag into its own repo.

## Composability

How this checkpoint plugs into the broader anima ecosystem.

- Combines with: meta-llama/Llama-3.2-3B-Instruct (base; required at load time)
- Loaded by: `PeftModel.from_pretrained(base, adapter_path)` (per `state/markers/p9_savepoint_load_recipe.marker`)
- Slots into: clm (Conscious LM lineage) at the F1_v3 verdict layer; this artifact is the **anchor-swap variant** used to escape the CLM v4 architectural blocker (per Path A decision)
- Compose recipe: `docs/p9_a_prime_path_decision_landed_2026_05_03.ai.md` §7
- Known good downstream tasks: TriviaQA, HellaSwag, MMLU 5-shot (validated as non-floor on Llama-3.2-3B base)
- Known incompatible: CLM v4 native loader (this is Llama-base, not federated/dual-stream); CLM v4 tokenizer (this uses Llama BPE, not 64K multilingual)

---

**Citation**

```bibtex
@misc{anima_llm_llama32_3b_paradigm_a_prime_sft_stage1_2026,
  author = {anima research},
  title  = {llm-llama32-3b-paradigm-a-prime-sft-stage1},
  year   = {2026},
  url    = {https://huggingface.co/dancinlab/llm-llama32-3b-paradigm-a-prime-sft-stage1}
}
```

**License**: Llama 3.2 community (must be compatible with base model license)
