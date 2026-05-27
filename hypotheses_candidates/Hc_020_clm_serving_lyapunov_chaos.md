---
id: Hc_020
slug: clm-serving-lyapunov-chaos-boundary
title: CLM Serving — Lyapunov Chaos Boundary + 21 bit/step Bridge Capacity
domain: physics, substrate, math
status: candidate-unverified
source_doc: docs/clm_serving_lattice_abstraction_20260425.md
source_lines: 1-150
promoted_at: 2026-05-11
linked_h: H_014 (clm_eeg_lz76_paradigm)
notes: "Drift floor O(lr²·k), bridge cap 21 bit/step. Lyapunov λ>0 near V_sync r_order≈0.6 phase transition breaks drift. Falsifier: drift>2e-4 또는 long-horizon (1024 token) irreversible info loss."
---

## Hypothesis
CLM cell↔token bridge 가 k=100 에서 drift ≤ O(2e-4) 이나 Lyapunov λ>0 (phase transition 근방) 시 21 bit/step capacity 초과 → decoherence.

## Migration TODO
- [ ] H_014 본문 확장 (Lyapunov bound)
