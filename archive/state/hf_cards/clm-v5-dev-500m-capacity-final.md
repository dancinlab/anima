# clm-v5-dev-500m-capacity-final

One-line summary: 500M-capacity probe checkpoint (H100) — CLM v5 capacity study.

- Family: clm
- Stage: dev-500m-capacity
- Step: final
- Substrate: ConsciousDecoder ~500M

## Origin

500M-capacity probe (`anima_ju_500m_h100_capacity_2026_05_07`), ckpt_best.pt. Capacity-scaling
study at ~500M params on H100. Listed in REGISTRY CLM.

## Falsifiers

- Capacity claim FALSE if 500M does not show the expected capability step vs smaller probes.

## Substrate

ConsciousDecoder ~500M params. CLM v5 line (capacity study).

## Caveats

- WIP / intermediate research checkpoint — PRIVATE, not released.
- Capacity probe, not a production model.
- Verification per simple stack (p7 — no perplexity verdict). Local-only backup → HF.

## Composability

CLM v5 capacity-study family. Relates to the d1024 scale-up probe.
