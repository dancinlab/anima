---
id: Hc_622
slug: clm-v5-axis-d-loss-objective-explicit-chat
title: Axis D — CE-only next-token objective 는 chat-cap 에 necessary but insufficient, RLHF/multi-obj/DPO/Constitutional 필요
domain: clm-architecture
status: candidate-unverified
source_doc: docs/anima_clm_v5_design_spec_2026_05_07.md
source_lines: 120-134
promoted_at: 2026-05-11
linked_h: Hc_618, BG-JX 3.27 / BG-JZ 3.53 / BG-KB 5.31 모두 0/5
notes: D1 SFT+RLHF / D2 multi-obj CE+aux / D3 Constitutional AI / D4 DPO / D5 task-conditioned head.
---

## Hypothesis
Standard CE on next-token (single objective) 은 multi-turn coherence + context-relevance 직접 optimize 안 함. Loss-floor 차이에도 모두 0/5 PASS — loss reduction alone 으로 chat-cap unlock 불가. RLHF + reward model 또는 constitutional AI (-v3 4-condition) 또는 DPO pairwise 필요.

## Falsifiable Tests
- D1.test: SFT+RLHF 가 chat-cap PASS 일부
- D3.test: Constitutional AI -v3 internalization 후 PASS
- D.universal: 5 D options 모두 0/5 → objective axis 자체 아님

## Migration TODO
- [ ] V5-β SFT+RLHF (trlx/trl raw#9 violation 검토)
- [ ] V5-δ Constitutional -v3 4-condition
