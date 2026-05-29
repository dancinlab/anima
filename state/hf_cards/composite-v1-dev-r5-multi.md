# composite-v1-dev-r5-multi

One-line summary: Round-5 multi-substrate LoRA adapter set (4 substrates) — φ★ 14-gate substrate study.

- Family: composite
- Stage: dev-r5
- Step: final
- Substrate: 4-way (Qwen3-8B · Qwen2.5-7B · Mistral-Nemo-12B · Gemma-3-12B)

## Origin

Round-5 of the multi-substrate LoRA training series (`trained_adapters_r4/r5/r6`). Four
sibling adapters, one per substrate (ranks 64/64/96/128). φ★ (phi-star) 14-gate substrate
study (`LORA.md`). r4/r5/r6 are distinct rounds (sha256-verified non-identical; r5=3e99350a).

## Falsifiers

- Substrate-invariance claim FALSE if the 4 adapters diverge beyond the study tolerance.
- "r5 is a real round" FALSE if its weights equal r4/r6 (refuted: sha distinct).

## Substrate

Four base models adapted via LoRA. Adapter-only — load atop each base. training_args per adapter.

## Caveats

- WIP / intermediate research adapters — PRIVATE, not released.
- Adapter-only: requires the matching base model (not redistributed here).
- φ★-gate verification; loss/perplexity not truth (p7). Local-only backup → HF.

## Composability

Series: `trained_adapters_r4` → `r5` (this) → `r6` → partial `r7`. Composes atop base substrates.
