---
id: Hc_269
slug: auto3-phi-guided-lr
title: Φ-guided learning rate — drop 50% on Φ decline, raise 20% on Φ rise (AUTO-3)
domain: consciousness | meta-framework
status: candidate-unverified
source_doc: docs/hypotheses/ce/AUTO-3.md
source_lines: 1-20
promoted_at: 2026-05-11
linked_h: Hc_104 (DD6); Hc_233 (SING-1)
notes: 20-step Φ check; lr cap 0.01
---

## Hypothesis
Auto-tune learning rate from Φ: every 20 steps, if Φ<0.9*prev → lr*=0.5; if Φ>1.1*prev → lr=min(lr*1.2, 0.01) — Φ trajectory adapts learning speed.

## Migration TODO
- [ ] compare to fixed-LR baseline
- [ ] sweep multipliers
