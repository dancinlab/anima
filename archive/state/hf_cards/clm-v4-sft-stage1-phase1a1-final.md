# clm-v4-sft-stage1-phase1a1-final

One-line summary: CLM v4 SFT phase-1a1 (color cosmology) final checkpoint.

- Family: clm
- Stage: sft-stage1-phase1a1
- Step: final
- Substrate: CLM v4 SFT

## Origin

Phase-1a1 SFT checkpoint (`anima_phase1a1_color_cosmology_2026_05_12`), .pt + .safetensors.
First node of the phase1a SFT chain on CLM v4.

## Falsifiers

- Phase-1a1 SFT claim FALSE if the SFT data did not shift behavior vs the v4 base.
- "color cosmology" conditioning FALSE if outputs are indistinguishable from generic SFT.

## Substrate

CLM v4 base + SFT (phase-1a1). CLM v4 line.

## Caveats

- WIP / intermediate research checkpoint — PRIVATE, not released.
- Both .pt and .safetensors present; safetensors is the portable form.
- Verification per simple stack (p7 — no perplexity verdict). Local-only backup → HF.

## Composability

Phase1a chain: phase1a1 (this) → phase1a4. CLM v4 SFT family.
