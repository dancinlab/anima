# clm-v4-sft-stage1-phase1a4-final

One-line summary: CLM v4 SFT phase-1a4 (lr5e6) final checkpoint.

- Family: clm
- Stage: sft-stage1-phase1a4
- Step: final
- Substrate: CLM v4 SFT

## Origin

Phase-1a4 SFT checkpoint (`anima_phase1a4_lr5e6_2026_05_12`), lr=5e-6, .pt + .safetensors.
Continuation of the phase1a SFT chain (after phase1a1).

## Falsifiers

- "lr5e6 improves on phase1a1" FALSE if the lower-LR run does not beat phase1a1 on the simple stack.
- Phase-1a4 SFT claim FALSE if SFT had no behavioral effect.

## Substrate

CLM v4 base + SFT (phase-1a4, lr5e6). CLM v4 line.

## Caveats

- WIP / intermediate research checkpoint — PRIVATE, not released.
- Both .pt and .safetensors present.
- Verification per simple stack (p7 — no perplexity verdict). Local-only backup → HF.

## Composability

Phase1a chain: phase1a1 → phase1a4 (this). Parent: phase1a1. CLM v4 SFT family.
