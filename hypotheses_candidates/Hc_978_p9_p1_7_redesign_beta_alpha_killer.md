---
id: Hc_978
slug: p9-p1-7-redesign-beta-alpha-killer
title: P9 P1.7 redesign — Ablation A (r=64 data-v3) + Ablation B (r=128 data-v2) 모두 F1=0.00586 동일 → r/data NOT killer. β 0.15→0.10 + α-warmup 5K→3K 가 -33% regression cause. P1.7 reverts both
domain: training, sft, ablation
status: candidate-needs-scaffolding
source_doc: docs/p9_p1_7_redesign_2026_05_03.md
source_lines: 1-30
promoted_at: 2026-05-11
linked_h: Hc_943 (P9 P1.7 pre-spec)
notes: "P1.5 F1=0.00879 (β 0.15, α 5K, r=64, data-v2). P1.6 F1=0.00586 (β 0.10, α 3K, r=128, data-v3). Ablation A+B 모두 0.00586 동일. Killer = β + α (둘 다)."
cycle5_triage: "cycle #5 verify: WEAK_MATH_ONLY — math identity present, falsifier+honest scaffolding missing; needs F-list/L-list before re-verify can reach PROMOTE_READY"
---

## Hypothesis

P1.5 (F1=0.00879) → P1.6 (F1=0.00586, -33%) 의 4-axis confounded change 분리: Ablation A (r=64 on data-v3) F1=0.00586, Ablation B (r=128 on data-v2) F1=0.00586 — 둘 다 P1.6 와 동일. ∴ F1 killer 는 NOT data-v3 nor LoRA r=128. 잔존 두 P1.6 변경 (β 0.15→0.10 + α-warmup 5K→3K) 가 -33% regression 의 합산 원인. P1.7 = 둘 다 revert + chat-100% × LoRA-r-128 capacity bonus 가 P1.5 loss schedule 하에서 unlock 검증.

## Sub-claims

- P1.5: F1=0.00879, β=0.15, α=5K, r=64, data-v2 (chat 86%)
- P1.6: F1=0.00586, β=0.10, α=3K, r=128, data-v3 (chat 100%) — -33%
- Ablation-A: r=64, data-v3, β=0.10, α=3K → F1=0.00586 (r=128 NOT killer)
- Ablation-B: r=128, data-v2, β=0.10, α=3K → F1=0.00586 (data-v3 NOT killer)
- KILLER: β 0.15→0.10 + α-warmup 5K→3K (둘 다 합산)
- P1.7-PLAN: β=0.15 + α=5K + r=128 + data-v3

## Migration TODO

- [ ] P1.7 EXEC user OK
- [ ] β vs α individual ablation (개별 분리)
- [ ] r=128 capacity bonus 정량 (data-v3, β=0.15, α=5K 조합)
- [ ] savepoint cleanup plan
