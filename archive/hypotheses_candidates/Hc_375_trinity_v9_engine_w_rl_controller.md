---
id: Hc_375
slug: trinity-v9-engine-w-rl-controller
title: Engine W RL controller (4 actions: LEARN_CE/BOOST_PHI/EXPLORE/CONSOLIDATE) + Constitutional constraints (min 50% CE, 20% Phi)가 hardcoded phase schedule보다 우월하다
domain: consciousness
status: candidate-unverified
source_doc: docs/hypotheses/TRINITY-TRAINING-DESIGN.md
source_lines: 296-425
promoted_at: 2026-05-11
linked_h: REINFORCE
notes: 6-dim state, REINFORCE update, reward = CE_improve + Phi_maintain
---

## Hypothesis
Engine W의 6-dim state (phi, phi_delta, ce, ce_delta, progress, learn_ratio) + 4-action 정책 + Constitutional hard constraints (min 50% CE, 20% Phi, max 5/10 consecutive skip) + REINFORCE 업데이트가 v5 hardcoded 30/40/30 phase schedule보다 우월한 적응적 균형을 제공한다.

## Migration TODO
- [ ] W policy 학습 곡선 측정
- [ ] constraint 활성화 빈도 추적
