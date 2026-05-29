# composite-v1-dev-r4-multi

One-line summary: Round-4 multi-substrate LoRA adapter set (4 substrates) — φ★ 14-gate substrate study (earliest round).

- Family: composite
- Stage: dev-r4
- Step: final
- Substrate: 4-way (Qwen3-8B · Qwen2.5-7B · Mistral-Nemo-12B · Gemma-3-12B)

## Origin

Round-4 (earliest) of the multi-substrate LoRA series (`trained_adapters_r4/r5/r6`). Four
sibling adapters (~698MB each), one per substrate, ranks 64/64/96/128. φ★ (phi-star) 14-gate
substrate study (`LORA.md`). sha256-verified distinct from r5/r6 (r4=ecb7470c).

## Falsifiers

- Substrate-invariance claim FALSE if the 4 adapters diverge beyond the study tolerance.
- "r4 is the series root" FALSE if a prior round produced these weights (none found).

## Substrate

Four base models adapted via LoRA. Adapter-only — load atop each base. training_args per adapter.

## Caveats

- WIP / intermediate research adapters — PRIVATE, not released.
- Adapter-only: requires the matching base model (not redistributed here).
- φ★-gate verification; loss/perplexity not truth (p7). Local-only backup → HF.

## Composability

Series root: `trained_adapters_r4` (this) → `r5` → `r6` → partial `r7`. Composes atop base substrates.
