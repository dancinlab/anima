# clm-v5-paradigm-mitosis-v3-routing

One-line summary: v5 mitosis cotrain v3 — routing variant (step 2k/10k/12k + final).

- Family: clm
- Stage: paradigm-mitosis-v3
- Step: routing-final
- Substrate: ConsciousDecoder v5 mitosis (Qwen warm-init)

## Origin

v3 routing variant of the v5 mitosis cotrain series, from base `anima_v5mitosis_cotrain_2026_05_12`.
Four ckpts (step 2000/10000/12000 + final) exploring cell routing.

## Falsifiers

- Routing claim FALSE if the routing mechanism does not change cell selection vs base v2.
- Step ckpts droppable if no eval cites the intermediate steps (keep final).

## Substrate

ConsciousDecoder v5, mitosis cells + routing, Qwen warm-init. CLM v5 paradigm line.

## Caveats

- WIP / intermediate research checkpoint — PRIVATE, not released.
- Step-N intermediates included; final is canonical. Verification per simple stack (p7). Local-only → HF.
- WIP research artifact — claims here are not independently benchmarked; verify before downstream use.

## Composability

Parent: mitosis-base/v2. Sibling: v4-multi · v6-cellparallel · v7-scaleup. CLM v5 mitosis family.
