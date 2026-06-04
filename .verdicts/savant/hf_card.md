# anima-savant-7b-rung0 (pipeline-validation forge CLM)

**SAVANT-7B campaign rung0** — a SMALL CLMConvMoE (d768/E2, int4-QAT) from-scratch byte LM
trained by the **hexa-native flame+forge** stack on a 5-language (en·fr·de·es·ru) starter corpus.

## Scope (HONEST — a_scale_honest_scope)
This is **PIPELINE VALIDATION, NOT a 7B and NOT a competent LM.** rung0 validates the end-to-end
forge train + checkpoint + recover pipeline on a real GPU before the expensive 7B-ladder rungs.
The descent verdict is on the small d768 byte corpus only; transfer to 1.5B/7B is UNVERIFIED.

## Origin
- Trainer: `hexa-lang/stdlib/flame/clm_prod.hexa` (CLMConvMoE + int4 QAT), authored in `.hexa`,
  run via the self-host-built hexa compiler (forge `forge_dispatch_matmul` GPU path). NOT torch.
- Corpus: 5-lang starter (Wikipedia CC-BY-SA + Gutenberg PD, en·fr·de·es·ru), byte-vocab V=256.
- Substrate: GPU / Lane-G (NVIDIA B200), recorded separately from any AKIDA on-chip track.
- Config: d=768, E=2, T=256, 8 epochs.

## Falsifier
- **F-CLM-PROD-DESCENT**: real-corpus mean CE strictly descends (epoch-1 > epoch-N). See VERDICT.

## License / visibility
PRIVATE (research WIP, pipeline-validation intermediate · a_hf_autonomous). Corpus license MIXED
(PD + CC-BY-SA). Part of the dancinlab CLM collection.
