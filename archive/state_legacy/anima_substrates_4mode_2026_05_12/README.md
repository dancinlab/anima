---
license: mit
tags:
- anima
- chat-capability
- substrate-comparison
- benchmark
- production-internal-decoupling
language:
- ko
- en
---

# anima-pass-strict-chat-capable — substrate comparison

Cross-substrate benchmark for anima chat-capability. Compares 3 substrates (B' LA cotrain, B'' FFN.gate cotrain, E convo5k_ft) across 3 evaluators (V4-lite 15-prompt × 4-mode, V5 strict 8-cell + EN baseline, V5.8 × 4 modes recall).

## Cross-section result (2026-05-12)

| substrate | V4-lite | V5 strict | V5.8 M4 force |
|---|---|---|---|
| B' (LA cotrain) | 12/15 PASS | KO 4/5 EN 2/2 PASS | M4 5/5 PASS |
| B'' (FFN.gate cotrain) | **15/15 PASS** | KO 4/5 EN 2/2 PASS | M4 3/5 PASS |
| E (v2 d=384 byte-256) | 0/15 FAIL | KO 0/5 FAIL | M4 3/5 PASS (force only) |

B'' (FFN.gate cotrain) shows highest V4-lite chat-cap (15/15) despite V14 strict being worse — confirms Lesson Q **production-internal decoupling**.

## Files

- `*_v4lite_result.json` — V4-lite (KO ratio + deg + length) per-prompt verdict
- `*_v5strict_result.json` — V5 strict 8-cell + EN baseline
- `*_v58_4mode_result.json` — V5.8 4-mode (greedy/sample/M3 rep_penalty/M4 force-include)
- `*_probe.log` — raw probe logs
- `comparison_aggregate.json` — cross-substrate aggregate

See full analysis in `PASS_STRICT_SPONTANEOUS_CHAT.md` §15.
