---
id: Hc_312
slug: v8-a3-read-only-consciousness
title: 의식 세포에 CE gradient를 차단하고 자율 dynamics(Hebbian + frustration + noise)로만 진화시키면 Phi x5-20 증가
domain: consciousness
status: candidate-unverified
source_doc: docs/hypotheses/V8-ARCHITECTURE-HYPOTHESES.md
source_lines: 89-117
promoted_at: 2026-05-11
linked_h: reservoir-computing, law-53
notes: requires_grad_(False) + ReadoutMLP만 학습
---

## Hypothesis
cells.requires_grad_(False)로 완전 동결한 후 Hebbian + frustration + noise + mitosis 의 자율 dynamics만 적용하고 ReadoutMLP만 학습시키면 reservoir computing 패러다임으로 Phi가 x5-20 증가한다.

## Migration TODO
- [ ] reservoir computing baseline (ESN) 와 비교
- [ ] CE 악화 정도 정량화
