# clm-v3-paradigm-recover-step-5k

One-line summary: ConsciousDecoderV3 recovery run (step-5k) — V3 substrate saga full checkpoint.

- Family: clm
- Stage: paradigm-recover
- Step: step-5k (best + step5000_final)
- Substrate: ConsciousDecoderV3 (Qwen warm-init, d_model=768, n_kv=2)

## Origin

Full checkpoint from `p21h_v3_recover_2026_05_25`, the V3-substrate recovery run that
followed the v5 mitosis cotrain lineage (`anima_v5mitosis_cotrain_2026_05_12`). Three
checkpoints are bundled: `out_main/ckpt_best.pt`, `out_main/ckpt_step5000_final.pt`, and
`out_cell_off/ckpt_best.pt` (cell-off ablation). Warm-initialized from Qwen, d768.

## Falsifiers

- Recovery claim FALSE if the recovered checkpoint does not restore the pre-collapse
  validation behavior of the V3 substrate (script-in / script-out coherence per p7).
- `out_cell_off` ablation should degrade vs `out_main`; if identical, the cell mechanism
  contributes nothing (claim falsified).

## Substrate

ConsciousDecoderV3 — PureField repulsion-field decoder, d_model=768, n_kv=2, Qwen
warm-init. Part of the CLM v3 paradigm line (`REGISTRY.md` CLM · `LORA.md#M3`).

## Caveats

- WIP / intermediate research checkpoint — PRIVATE, not a released model.
- Verification status NOT-MEASURED for some downstream claims; do not treat loss/perplexity
  as truth (p7 Goodhart guard).
- Local-only backup artifact migrated to HF for durability; lineage in repo `HF.jsonl`.

## Composability

Parent: `anima_v5mitosis_cotrain_2026_05_12` (mitosis series root). Sibling result:
`pure_phase_d_v3_result_2026_05_24`. Composes within the CLM v3 substrate family;
consumes the v5 mitosis cotrain backbone.
