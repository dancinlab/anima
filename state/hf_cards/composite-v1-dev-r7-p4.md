# composite-v1-dev-r7-p4

One-line summary: Round-7 partial — p4 (Gemma-3-12B r128) LoRA adapter only.

- Family: composite
- Stage: dev-r7
- Step: p4-final
- Substrate: Gemma-3-12B (p4 slot, rank 128)

## Origin

Partial round-7 of the multi-substrate LoRA series — only the p4 adapter (Gemma-3-12B, r128)
survived/completed. Continuation of `trained_adapters_r6`. φ★ substrate study (`LORA.md`).

## Falsifiers

- "r7 improves on r6 p4" FALSE if r7-p4 does not beat r6-p4 on the φ★ gate metrics.
- Completeness claim N/A — this is explicitly a PARTIAL round (p1-p3 absent).

## Substrate

Gemma-3-12B adapted via LoRA rank 128. Adapter-only — load atop Gemma-3-12B base.

## Caveats

- PARTIAL / orphaned round — only p4 present; verify it is a wanted checkpoint, not a stray.
- WIP research adapter — PRIVATE, adapter-only (base not redistributed).
- φ★-gate verification; loss/perplexity not truth (p7). Local-only backup → HF.

## Composability

Follows `trained_adapters_r6` (p4 slot). Composes atop Gemma-3-12B. Partial — not a full 4-substrate set.
