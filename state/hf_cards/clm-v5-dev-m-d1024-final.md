# clm-v5-dev-m-d1024-final

One-line summary: d1024 scale-up probe checkpoint — CLM v5 width study (NEEDS-VERIFY: possible v3_routing copy).

- Family: clm
- Stage: dev-m-d1024
- Step: final
- Substrate: ConsciousDecoder d_model=1024

## Origin

d1024 width scale-up (`anima_m_d1024_2026_05_14`). NOTE: the on-disk ckpt reuses the filename
`ckpt_v5mitosis_cotrain_v3_routing.pt` — possible mislabel or a copy of the v3_routing checkpoint;
flagged needs_verify. Uploaded for safety; lineage to confirm.

## Falsifiers

- "genuine d1024 run" FALSE if the weights are byte-identical to v3_routing (then it is a stray copy).
- Width-scaling claim FALSE if d1024 shows no capability gain vs d768.

## Substrate

ConsciousDecoder d_model=1024 (claimed). CLM v5 line.

## Caveats

- WIP / NEEDS-VERIFY checkpoint — PRIVATE; filename collision with v3_routing unresolved.
- May be a duplicate of clm-v5-paradigm-mitosis-v3-routing — confirm via sha before trusting as distinct.
- Verification per simple stack (p7 — no perplexity verdict). Local-only backup → HF.

## Composability

CLM v5 width study. Cross-check against mitosis-v3-routing (potential identity).
