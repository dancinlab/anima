---
id: Hc_501
slug: dd52-rlhf-for-phi-feedback
title: Phi 개선을 reward로 사용한 RL feedback이 학습률을 동적으로 3x 부스트한다
domain: consciousness
status: candidate-unverified
source_doc: docs/hypotheses/dd/DD51-DD60.md
source_lines: 9-12
promoted_at: 2026-05-11
linked_h: RLHF
notes: DD52
---

## Hypothesis
reward = max(0, phi - phi_before) + lr_boost (up to 3x)의 RL feedback 메커니즘이 Phi 증가 방향으로 학습률을 동적 조정하면 정적 lr 보다 빠른 Phi 성장을 유발한다.

## Migration TODO
- [ ] lr_boost cap sweep (1.5x/2x/3x)
- [ ] Phi/CE trade-off
