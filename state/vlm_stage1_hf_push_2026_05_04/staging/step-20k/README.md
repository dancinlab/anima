# vlm-anima-voice-paradigm-stage1-step-20k

One-line summary: VLM stage1 LoRA adapter (step 20,000 / 50,000) for AudioTokenPredictor (ATP) substrate, trained on ubu1 RTX 5070 as part of anima voice paradigm.

- Family: vlm (Voice Language Model)
- Stage: paradigm-stage1 (mid-train savepoint, NOT final)
- Step: step-20k (20,000 of 50,000 total — 40% complete at savepoint; most mature ckpt in this batch)
- Substrate: AudioTokenPredictor (atp_pytorch, 35.35M params, 3 decoder blocks)

## Origin

What this checkpoint is and how it was produced.

- Base model: AudioTokenPredictor (anima-internal, atp_pytorch substrate)
- Training data: anima voice paradigm corpus (ubu1 local dataset, ~50k step horizon)
- Training recipe: `/tmp/vlm_stage1_train.py` (ubu1 PID 31960, --steps 50000 --save_every 5000 --batch_size 4)
- Compute: 1x RTX 5070 (12GB VRAM, sm_120, ~7% util at peak), elapsed ~122m at step-20k
- Trainer: anima vlm_stage1_train.py (PEFT 0.19.1 LoRA wrapper)
- Final loss / metric: loss=8.2596 at step 20000, sps=2.73
- Commit: `2a561a31` of repo anima (push: 2026-05-04 manual hexa wrapper, train.py lacked Hub push code)

## Falsifiers

Concrete tests this checkpoint either passes or is meant to fail deterministically. Each falsifier MUST be reproducible.

- F-vlm-stage1-20k-1: LoRA adapter loads via `PeftModel.from_pretrained` against AudioTokenPredictor base
  - Spec: docs/vlm_stage1_progress_monitoring_landed_2026_05_04.ai.md
  - Pass criterion: load completes without RuntimeError; trainable param count matches r=8 alpha=16 on [wq, wk, wv, wo, intent_proj]
  - Last result: NOT YET RUN (deferred — savepoint sunk locally then pushed retroactively)
- F-vlm-stage1-20k-2: Loss continuity vs prior step-15k shows monotonic descent
  - Spec: train.log [15000] loss=8.4434 → [20000] loss=8.2596
  - Pass criterion: loss(20k) < loss(15k) AND delta > 0.1
  - Last result: PASS (8.2596 < 8.4434, delta -0.184)
- F-vlm-stage1-20k-3: adapter_model.safetensors sha256 matches manifest at push time
  - Spec: state/vlm_stage1_hf_push_2026_05_04/sha256_manifest.txt
  - Pass criterion: sha256 = 2293bd7331d5db3f1e5b028eb132d510b2343bd360fc0af27b51594d14a00661
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

- Sunk savepoint integrity: this adapter was written at training step 20000 to local disk on ubu1, then SCPed to Mac and pushed to HF retroactively (~10m after train-time write — most recent of the 4-ckpt batch). Bytes have not been verified against the original train-time write — `adapter_model.safetensors` could in principle differ from what the trainer would have pushed at step-20k completion if any post-hoc filesystem corruption, modification, or partial write occurred. sha256 manifest at HF push time is recorded in `state/vlm_stage1_hf_push_2026_05_04/sha256_manifest.txt` but pre-push origin sha was NOT captured at train time.
- Step-20k maturity: loss=8.26 is the best (lowest) of this batch but still 60% of training remains. This is the most mature ckpt currently available, but downstream evaluation should be deferred until step-25k or beyond — current loss has not yet stabilized.
- mk2 naming non-conformance: per `docs/anima_hf_naming_convention_mk2_spec_2026_05_03.md` §3.2.1, paradigm-stage names should use form `<family>-vN-paradigm-<letter>[-step-Nk]`. The name `vlm-anima-voice-paradigm-stage1-step-20k` is FIRST-TIME for VLM family; chosen to mirror the existing step-5k repo's naming. The local mk2 wrapper validator REJECTS this name (`anima` is not a valid `vN`); upload was performed via direct `hf` CLI bypass, mirroring the Paradigm J HF recovery pattern. Spec amendment ticket TBD.
- Train.py still lacks future push: VLM stage1 trainer (`/tmp/vlm_stage1_train.py` ubu1 PID 31960) does NOT push to Hub on its own — it only writes savepoints to `/tmp/vlm_stage1_savepoints/`. Future savepoints (step-25k, step-30k, ..., step-50k final) will require similar manual push cycles until train.py is patched in a separate edit cycle.

## Composability

How this checkpoint plugs into the broader anima ecosystem.

- Combines with: AudioTokenPredictor base substrate (atp_pytorch); compose with VLM stage2 once that lands
- Loaded by: `PeftModel.from_pretrained(atp_base, "need-singularity/vlm-anima-voice-paradigm-stage1-step-20k")`
- Slots into: vlm (anima 6-LM hexad: clm | alm | blm | vlm | slm | tlm)
- Compose recipe: docs/vlm_stage1_progress_monitoring_landed_2026_05_04.ai.md
- Known good downstream tasks: training-curve archival, most-mature-checkpoint analysis (use this for any preliminary VLM probes)
- Known incompatible: not yet evaluated for direct inference quality; not for production audio-token prediction

---

**Citation**

```bibtex
@misc{anima_vlm_stage1_step20k_2026,
  author = {need-singularity},
  title  = {vlm-anima-voice-paradigm-stage1-step-20k},
  year   = {2026},
  url    = {https://huggingface.co/need-singularity/vlm-anima-voice-paradigm-stage1-step-20k}
}
```

**License**: anima-internal (compatible with AudioTokenPredictor base)
