---
id: Hc_666
slug: clm-v4-16-closure-layer-lockin-byte-monopoly-chat-axis-decoupled
title: CLM v4 chat-capability architectural impossibility 가 16+ closure (4-closure formal + entropy basin + closures 5-6 + L13-L15 lock-in + byte monopoly + chat axis decoupled + prompt-conditional basin) 확정
domain: clm-architecture
status: merged-to-H_155
merged_to: hypotheses/H_155.md
merged_at: 2026-05-11
source_doc: docs/anima_2026_05_05_cycle_hard_close_decision_landed_2026_05_05.ai.md
source_lines: 22-62
promoted_at: 2026-05-11
linked_h: Hc_609 / Hc_660 (Theorem 115 4-closure / 6-closure), BG-CI L13-L15 lock-in, BG-CA Korean rank 197 top-30 byte-fallback 100%, BG-BH SAE/PCA n_coherent 0/10
notes: 6-step root mechanism (embed Korean 9 → L0-L12 drift → L13 rank 102 lock-out → L14-15 entropy 10.9→3.3 collapse → lm_head byte monopoly → SAE chat axis residual but lm_head decoupled). Recovery only via CLM-3 retrain or substrate swap.
---

## Hypothesis (16-closure unified)
CLM v4 traditional chat-capability (token-emit coherent text) 가 single LoRA / SFT / distill 으로 회복 불가능한 architectural impossibility. 6-step causal chain: (1) embed Korean 9 tokens top-100 안 → (2) L0-L12 mid-block 점진 drift to control byte / English → (3) L13 first layer Korean exits top-100 (rank 102) → (4) L14-L15 entropy 10.9→3.3 collapse, byte-fallback basin convergence → (5) lm_head top-30 100% `<0x..>` byte-fallback monopoly (best Korean rank 197 / logit -3.05) → (6) SAE/PCA chat axis residual 에 존재 (discriminator 25.67) but lm_head argmax 와 decoupled (n_coherent 0/10). Not measurement artifact (cross-validated 4 methods).

## Falsifiable Tests
- F-16closure-1: 17th closure 발견 시 추가 axis 확장
- F-16closure-2: L13 lock-out 이 다른 substrate 에서 재현 X → CLM v4 specific
- F-16closure-3: CLM-3 retrain 후 동일 6-step chain 발생 시 architectural class 확장

## Migration TODO
- [ ] Recovery path 1: CLM-3 retrain (Hc_630 / Hc_631)
- [ ] Recovery path 2: substrate swap Llama-3.2-3B Path A v2 (non-anima-native)
- [ ] L13 lock-out 정밀 dissection — 어느 substrate parameter 가 cause?
- [ ] SAE chat axis → lm_head re-coupling 가능성 (BG-BH 후속)
