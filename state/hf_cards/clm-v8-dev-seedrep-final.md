# clm-v8-dev-seedrep-final

One-line summary: v8 seed-replication study (seed_43/seed_45) — NEEDS-VERIFY: contains v3_routing-named ckpts.

- Family: clm
- Stage: dev-seedrep
- Step: final
- Substrate: ConsciousDecoder v8 (seed replication)

## Origin

Seed-replication study (`anima_v8_seedrep_2026_05_13`): seed_43, seed_45 each holding
`ckpt_v5mitosis_cotrain_v3_routing.pt` + step_10000. Tests run-to-run variance across seeds.
NOTE: ckpt filenames are v3_routing-derived — confirm whether seeds are distinct trainings.

## Falsifiers

- Seed-replication claim FALSE if seed_43 and seed_45 weights are identical (no real seed variance).
- "v8" lineage FALSE if these are just copies of the v3_routing checkpoint under seed dirs.

## Substrate

ConsciousDecoder (v8 seedrep), seeds 43/45. CLM line.

## Caveats

- WIP / NEEDS-VERIFY checkpoint — PRIVATE; v3_routing-named ckpts, seed-distinctness unconfirmed.
- Multiple seed dirs + intermediate steps bundled.
- Verification per simple stack (p7 — no perplexity verdict). Local-only backup → HF.

## Composability

Seed-replication over the v3_routing/v5 substrate. Cross-check seed weights for true variance.
