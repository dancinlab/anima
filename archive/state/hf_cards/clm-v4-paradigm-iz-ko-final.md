# clm-v4-paradigm-iz-ko-final

One-line summary: CLM v4 Korean continued-pretrain (iz) — final + step_1000.

- Family: clm
- Stage: paradigm-iz-ko
- Step: final
- Substrate: CLM v4 continued-pretrain (Korean)

## Origin

Korean continued-pretrain run (`anima_iz_clm_continued_pretrain_ko_2026_05_07`). Two ckpts:
final + step_1000. Continues CLM v4 pretraining on Korean corpus.

## Falsifiers

- Korean-CPT claim FALSE if Korean perplexity/coherence does not improve vs the v4 base (use the
  simple script-in/out stack, not perplexity as truth — p7).

## Substrate

CLM v4 base + continued pretraining on Korean. CLM v4 line.

## Caveats

- WIP / intermediate research checkpoint — PRIVATE, not released.
- step_1000 is an intermediate; final is canonical.
- Verification per simple stack (p7 — no perplexity verdict). Local-only backup → HF.

## Composability

CLM v4 paradigm family (iz = Korean continued-pretrain branch).
