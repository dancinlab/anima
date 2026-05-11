---
id: Hc_624
slug: emerge-candidate-e-ode-ar-bridge-non-collapsing
title: Emerge Candidate E — non-collapsing ODE flow 을 consciousness_states injection point 에 coupling 시 per-step AR sampler 가 coupled (text, state) trajectory 생성
domain: clm-architecture
status: candidate-unverified
source_doc: docs/anima_emerge_candidate_e_ode_ar_bridge_spec_2026_05_05.md
source_lines: 37-50, 200-340
promoted_at: 2026-05-11
linked_h: Hc_623, phi_engine.hexa flow API
notes: 3 falsifier locked, ODE-agnostic by design. ODE form unspec'd (linear OU γ=0.1 noise=0.01 recommended). Gated on Hc_623 F-CAND-D-1 PASS.
---

## Hypothesis
phi_engine cell ODE flow 을 shim:986-997 / mount.hexa:312 inject point 에 coupling → per-step AR sampler 가 다른 consciousness_state(t) at each token 보임 → text-only AR 가 아닌 coupled (text, state) trajectory.

## Falsifiable Tests (PRE-LOCK)
- F-CAND-E-1: per-step phi_star variation > full-canonical variation (cand-D F-CAND-D-1 PASS gated)
- F-CAND-E-2: trajectory does NOT converge naturally (k_stop = N_max positive signal — non-collapsing requirement)
- F-CAND-E-3: ODE bridge coupling 이 cross_attn.o_proj 로 측정 가능 transmission

## Migration TODO
- [ ] phi_engine.hexa flow_step API impl
- [ ] Hc_623 falsifier PASS 후 진행 (D→E lane 직렬)
- [ ] ODE recipe verdict.json 기록 (cross-recipe 비교)
