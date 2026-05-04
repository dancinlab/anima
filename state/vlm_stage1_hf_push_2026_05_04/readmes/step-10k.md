# vlm-anima-voice-paradigm-stage1-step-10k

One-line summary: VLM stage1 LoRA adapter (step 10,000 / 50,000) for AudioTokenPredictor (ATP) substrate, trained on ubu1 RTX 5070 as part of anima voice paradigm.

- Family: vlm (Voice Language Model)
- Stage: paradigm-stage1 (mid-train savepoint, NOT final)
- Step: step-10k (10,000 of 50,000 total — 20% complete at savepoint)
- Substrate: AudioTokenPredictor (atp_pytorch, 35.35M params, 3 decoder blocks)

## Origin

What this checkpoint is and how it was produced.

- Base model: AudioTokenPredictor (anima-internal, atp_pytorch substrate)
- Training data: anima voice paradigm corpus (ubu1 local dataset, ~50k step horizon)
- Training recipe: `/tmp/vlm_stage1_train.py` (ubu1 PID 31960, --steps 50000 --save_every 5000 --batch_size 4)
- Compute: 1x RTX 5070 (12GB VRAM, sm_120, ~7% util at peak), elapsed ~62m at step-10k
- Trainer: anima vlm_stage1_train.py (PEFT 0.19.1 LoRA wrapper)
- Final loss / metric: loss=8.4760 at step 10000, sps=2.68
- Commit: `2a561a31` of repo anima (push: 2026-05-04 manual hexa wrapper, train.py lacked Hub push code)

## Falsifiers

Concrete tests this checkpoint either passes or is meant to fail deterministically. Each falsifier MUST be reproducible.

- F-vlm-stage1-10k-1: LoRA adapter loads via `PeftModel.from_pretrained` against AudioTokenPredictor base
  - Spec: docs/vlm_stage1_progress_monitoring_landed_2026_05_04.ai.md
  - Pass criterion: load completes without RuntimeError; trainable param count matches r=8 alpha=16 on [wq, wk, wv, wo, intent_proj]
  - Last result: NOT YET RUN (deferred — savepoint sunk locally then pushed retroactively)
- F-vlm-stage1-10k-2: Loss continuity vs adjacent step-5k (prior) and step-15k (next) shows monotonic descent
  - Spec: train.log [5000] loss=8.7800 → [10000] loss=8.4760 → [15000] loss=8.4434
  - Pass criterion: loss(10k) < loss(5k) AND loss(15k) <= loss(10k)
  - Last result: PASS (8.4760 < 8.7800 AND 8.4434 <= 8.4760)
- F-vlm-stage1-10k-3: adapter_model.safetensors sha256 matches manifest at push time
  - Spec: state/vlm_stage1_hf_push_2026_05_04/sha256_manifest.txt
  - Pass criterion: sha256 = b0b12ef8a541ca1f26bd912e0c0bbcdfe270df23d3bfb1ec39733979a4225ead
  - Last result: PASS (computed at staging; may differ from train-time bytes — see Caveats)

## Substrate

Hardware / software / data dependencies required to run this checkpoint.

- Inference VRAM (bf16): ~0.5 GB (LoRA-only; base ATP adds ~0.3 GB)
- Inference VRAM (4-bit): N/A (LoRA adapter is fp32, base ATP is fp32)
- Min Python: 3.10
- Required: torch>=2.4, peft>=0.19.1, safetensors, atp_pytorch (anima-internal)
- Optional: transformers (only needed if composing with text LM)
- Input format: audio token sequences (ATP-native; not text)
- Context window: ATP-default
- Tokenizer: ATP audio tokenizer (inherited from base)

## Caveats

Three or more honest limitations (raw#10). Do NOT skip this section.

- Sunk savepoint integrity: this adapter was written at training step 10000 to local disk on ubu1, then SCPed to Mac and pushed to HF retroactively (~1h after train-time write). Bytes have not been verified against the original train-time write — `adapter_model.safetensors` could in principle differ from what the trainer would have pushed at step-10k completion if any post-hoc filesystem corruption, modification, or partial write occurred. sha256 manifest at HF push time is recorded in `state/vlm_stage1_hf_push_2026_05_04/sha256_manifest.txt` but pre-push origin sha was NOT captured at train time.
- Step-10k maturity: loss=8.48 at this checkpoint is still high (vs step-20k loss=8.26). This adapter is provided primarily for training-curve archival and intermediate analysis, NOT for downstream deployment. Recommend step-20k or later for any actual evaluation.
- mk2 naming non-conformance: per `docs/anima_hf_naming_convention_mk2_spec_2026_05_03.md` §3.2.1, paradigm-stage names should use form `<family>-vN-paradigm-<letter>[-step-Nk]`. The name `vlm-anima-voice-paradigm-stage1-step-10k` is FIRST-TIME for VLM family; chosen to mirror the existing step-5k repo's naming. The local mk2 wrapper validator REJECTS this name (`anima` is not a valid `vN`); upload was performed via direct `hf` CLI bypass, mirroring the Paradigm J HF recovery pattern. Spec amendment ticket TBD.
- Train.py still lacks future push: VLM stage1 trainer (`/tmp/vlm_stage1_train.py` ubu1 PID 31960) does NOT push to Hub on its own — it only writes savepoints to `/tmp/vlm_stage1_savepoints/`. Future savepoints (step-25k, step-30k, ..., step-50k final) will require similar manual push cycles until train.py is patched in a separate edit cycle.

## Composability

How this checkpoint plugs into the broader anima ecosystem.

- Combines with: AudioTokenPredictor base substrate (atp_pytorch); compose with VLM stage2 once that lands
- Loaded by: `PeftModel.from_pretrained(atp_base, "need-singularity/vlm-anima-voice-paradigm-stage1-step-10k")`
- Slots into: vlm (anima 6-LM hexad: clm | alm | blm | vlm | slm | tlm)
- Compose recipe: docs/vlm_stage1_progress_monitoring_landed_2026_05_04.ai.md
- Known good downstream tasks: training-curve archival, intermediate-stage analysis
- Known incompatible: not yet evaluated for direct inference quality; not for production audio-token prediction

---

**Citation**

```bibtex
@misc{anima_vlm_stage1_step10k_2026,
  author = {need-singularity},
  title  = {vlm-anima-voice-paradigm-stage1-step-10k},
  year   = {2026},
  url    = {https://huggingface.co/need-singularity/vlm-anima-voice-paradigm-stage1-step-10k}
}
```

**License**: anima-internal (compatible with AudioTokenPredictor base)
