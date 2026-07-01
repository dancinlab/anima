# composite-v1-lora-r6-multi

One-line summary: Round-6 multi-substrate LoRA adapter set (4 substrates) — φ★ 14-gate substrate study.

- Family: composite
- Stage: lora-r6
- Step: final
- Substrate: 4-way (Qwen3-8B · Qwen2.5-7B · Mistral-Nemo-12B · Gemma-3-12B)

## Origin

Round-6 of the multi-substrate LoRA training series (`trained_adapters_r4/r5/r6`). Four
sibling adapters, one per substrate: p1=Qwen3-8B (r64), p2=Qwen2.5-7B (r64),
p3=Mistral-Nemo-12B (r96), p4=Gemma-3-12B (r128). Part of the φ★ (phi-star) 14-gate
substrate study (`LORA.md`). r4/r5/r6 are distinct rounds (sha256-verified non-identical).

## Falsifiers

- Substrate-invariance claim FALSE if the 4 adapters' behaviors diverge beyond the study's
  tolerance on the shared evaluation (per the φ★ gate criteria).
- "round-6 improves on r5" FALSE if r6 does not beat r5 on the gate metrics.

## Substrate

Four base models adapted via LoRA (ranks 64/64/96/128). No merged weights — adapters only;
load atop the respective base. `training_args.bin` included per adapter.

## Caveats

- WIP / intermediate research adapters — PRIVATE, not released models.
- Adapter-only: requires the matching base model (not redistributed here).
- Verification per φ★ gates; loss/perplexity are not truth (p7). Local-only backup → HF.

## Composability

Series: `trained_adapters_r4` → `r5` → `r6` (this) → partial `r7` (p4 only). Each adapter
composes atop its base substrate. Part of the composite LM family.
