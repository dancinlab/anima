# clm-v3-paradigm-d-pure-final

One-line summary: ConsciousDecoderV3 Phase-D PURE final checkpoint — V3 substrate paradigm-D result.

- Family: clm
- Stage: paradigm-d-pure
- Step: final
- Substrate: ConsciousDecoderV3 (Qwen warm-init, d_model=768)

## Origin

Final checkpoint (`ckpt_best.pt`) from `pure_phase_d_v3_result_2026_05_24`, the PURE
paradigm-D run on the V3 substrate. Sibling of the recovery run
`p21h_v3_recover_2026_05_25`; both descend from the v5 mitosis cotrain lineage.

## Falsifiers

- Paradigm-D claim FALSE if PURE phase-D behavior is indistinguishable from the
  pre-D baseline on the simple verification stack (p7 — no perplexity verdict).
- "PURE" claim FALSE if the run silently mixed non-D gradient signal.

## Substrate

ConsciousDecoderV3 — PureField repulsion-field decoder, d_model=768, Qwen warm-init.
CLM v3 paradigm line (`REGISTRY.md` CLM).

## Caveats

- WIP / intermediate research checkpoint — PRIVATE, not a released model.
- Verification NOT-MEASURED for some downstream claims; loss/perplexity are not truth (p7).
- Local-only backup migrated to HF for durability; lineage in repo `HF.jsonl`.

## Composability

Parent: `p21h_v3_recover_2026_05_25`. Family: CLM v3 substrate. Composes with the
recovery checkpoint; consumes the v5 mitosis cotrain backbone.
