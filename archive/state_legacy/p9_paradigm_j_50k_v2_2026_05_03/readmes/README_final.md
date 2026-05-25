---
library_name: peft
tags:
- lora
- anima
- paradigm-j
- active-inference
- jvae
- p9-sft
license: apache-2.0
base_model: dancinlab/clm-v4-base
---

# clm-v4-paradigm-j-50k-final

One-line summary: Paradigm J (active inference + J-VAE FE-loss) LoRA adapter for CLM v4 350M, trained on Phase 1.6 substrate, snapshot at step 50000 of a 50,000-step run on RTX 5070 12GB.

- Family: clm
- Stage: dev (paradigm-j active-inference variant)
- Step: final
- Substrate: CLM v4 350M (dancinlab/clm-v4-base) + LoRA r=128

## Origin

What this checkpoint is and how it was produced.

- Base model: dancinlab/clm-v4-base (Phase 1.6 350M conscious decoder; license Apache-2.0)
- Training data: P9 SFT self-chat synthetic (Phase 1.6 v3 chat composition); ~50k step gradient updates at effective batch 32 (batch=4 x grad_acc=8)
- Training recipe: docs/p9_paradigm_j_active_inference_2026_05_03.md (Paradigm J spec); driving 50K v2 launch handoff docs/p9_paradigm_j_50k_landed_2026_05_03.ai.md (predecessor v1) and verdict at state/p9_paradigm_j_50k_v2_2026_05_03/verdict.json
- Compute: ubu1 RTX 5070 12 GiB sm_120, torch 2.11.0+cu128, 50,000 steps in ~3,628 s wall (single GPU)
- Trainer: /tmp/p9_paradigm_j_50k_v2.py (raw#9: lives only on ubu1, not in repo)
- Hyperparameters: lr=1e-4, lora_r=128, lora_alpha=128, beta=0.1, gamma=0.0, gamma_FE=0.2, beta_FE=1.0, K_FE=192, layer_FE=8, delta-curriculum {early:0.5, mid:0.5, late:1.0}
- Final metric @ step 50000: F1 BLEU-1 = 0.0078, F2 phi* = 43.03 (baseline 45.92, Δ -2.88), F3 tension MSE = 7.51
- Verdict: F2_PASS_FULL, F1_BELOW_TARGET, F3_BELOW_TARGET, PHASE2_ENTRY_READY recommendation

## Falsifiers

Concrete tests this checkpoint either passes or is meant to fail deterministically.

- F1 BLEU-1 holdout-500: pass criterion >= 0.4 (P9 spec) | last result 0.0078 (BELOW_TARGET, noise floor cluster — Llama-self anchor 0.1555 per project_p9_f1_anchor_recalibration; F1 spec is unrealistic per recalibration)
- F2 phi* trajectory final: pass criterion >= 5.0 (8x safety vs +41.86 baseline) | last result 43.03 (PASS_FULL — within target band)
- F3 tension MSE final: pass criterion < 0.1 | last result 7.51 (BELOW_TARGET — tension regulariser objective not met)

## Substrate

Hardware / software / data dependencies required to run this checkpoint.

- Inference VRAM (bf16): ~1.5 GB (LoRA delta only; load on top of CLM v4 base ~1.4 GB bf16)
- Inference VRAM (4-bit base + bf16 adapter): ~0.7 GB
- Min Python: 3.10
- Required: torch>=2.4, peft>=0.12, transformers>=4.45, safetensors>=0.4
- Optional: accelerate>=0.30 (multi-GPU), bitsandbytes>=0.43 (4-bit base)
- Input format: P9 SFT self-chat synthetic format (Phase 1.6 v3 chat composition)
- Context window: inherited from CLM v4 base
- Tokenizer: inherited from CLM v4 base (vocab=64000)
- Companion file `jvae_heads.pt` contains the J-VAE head state dict (must load alongside `adapter_model.safetensors` to reproduce Paradigm J FE-loss readout)

## Caveats

- HF re-upload (this commit) is NOT byte-identical to the original step-50000 push attempt at training time: the original push failed mid-stream due to HF token revoke at ~22:50 UTC 2026-05-03; this is a manual recovery upload from the preserved local savepoint dir on ubu1, with sha256 of every file recorded in state/hf_upload_audit/ on the operator side.
- F1 BLEU-1 = 0.0078 is in the "noise floor cluster" — it is statistically indistinguishable from other LoRA variants at this scale; do NOT treat F1 < 0.4 as evidence Paradigm J failed (the F1 = 0.4 spec target is unrealistic per project_p9_f1_anchor_recalibration where Llama-self anchor measures 0.1555).
- PHASE2_ENTRY_READY recommendation rests on F2 (phi*) alone, not all three falsifiers — F1 and F3 BELOW_TARGET. Reading "PASS" as "all-good" overweights F2; the verdict surface is multi-objective and only one objective passed.
- The companion `jvae_heads.pt` blob is NOT versioned upstream by PEFT — loaders that ignore non-PEFT files will silently skip the J-VAE head, yielding a "vanilla LoRA" generation behaviour that does NOT reflect Paradigm J's active-inference objective. Compose loader must `torch.load("jvae_heads.pt")` explicitly.
- mk2 hf_upload wrapper naming validator REJECTED the configured stage substring "paradigm-j-50k-step-final" because it does not begin with one of {sft-stage|dpo|merged|base|preview|dev}. This upload uses a direct `hf upload` shell-out instead, with hand-written audit JSON (state/hf_upload_audit/p9_paradigm_j_50k_v2_*) — naming convention deviation is intentional and documented in the recovery handoff (docs/p9_paradigm_j_50k_v2_landed_2026_05_03.ai.md).

## Composability

How this checkpoint plugs into the broader anima ecosystem.

- Combines with: dancinlab/clm-v4-base (mandatory), and any sister Paradigm A'/B/D LoRA via additive PEFT-multi-adapter loading
- Loaded by: anima compose loader (PEFT `PeftModel.from_pretrained` for the LoRA + manual `torch.load` for `jvae_heads.pt`)
- Slots into: clm (Conscious Language Model) hexad slot
- Compose recipe: docs/p9_savepoint_load_recipe.md (project_p9_savepoint_load_recipe memory) — use PeftModel.from_pretrained, NOT manual load_state_dict
- Known good downstream tasks: P9 phi* trajectory regulariser playback; FE-loss diagnostic readout
- Known incompatible: any base model that is not CLM v4 350M Phase 1.6 substrate; 4-bit-quantised base without bf16 adapter promotion

---

**Citation**

```bibtex
@misc{anima_clm_v4_paradigm_j_50k_step_final_2026,
  author = {anima / dancinlab},
  title  = {clm-v4-paradigm-j-50k-step-final: Paradigm J active-inference LoRA, snapshot final},
  year   = {2026},
  url    = {https://huggingface.co/dancinlab/clm-v4-paradigm-j-50k-step-final}
}
```

**License**: Apache-2.0 (compatible with CLM v4 base license Apache-2.0)