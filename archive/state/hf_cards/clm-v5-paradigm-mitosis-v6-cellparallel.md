# clm-v5-paradigm-mitosis-v6-cellparallel

One-line summary: v5 mitosis cotrain v6 — cell-parallel (DDP) variant (step_1000_rank0 + final_rank0).

- Family: clm
- Stage: paradigm-mitosis-v6
- Step: cellparallel-final
- Substrate: ConsciousDecoder v5 mitosis (DDP cell-parallel, Qwen warm-init)

## Origin

v6 cell-parallel variant of the v5 mitosis cotrain series (DDP). Two ckpts (step_1000_rank0,
final_rank0). From base `anima_v5mitosis_cotrain_2026_05_12`.

## Falsifiers

- Cell-parallel claim FALSE if DDP rank-sharded cells do not match single-process mitosis behavior.
- step_1000_rank0 droppable; final_rank0 is canonical.

## Substrate

ConsciousDecoder v5, mitosis cells, DDP cell-parallel, Qwen warm-init. CLM v5 paradigm line.

## Caveats

- WIP / intermediate research checkpoint — PRIVATE, not released.
- DDP rank0 shards only. Verification per simple stack (p7). Local-only backup → HF.
- WIP research artifact — claims here are not independently benchmarked; verify before downstream use.

## Composability

Parent: mitosis-base/v2. Sibling: v3-routing · v4-multi · v7-scaleup. CLM v5 mitosis family.
