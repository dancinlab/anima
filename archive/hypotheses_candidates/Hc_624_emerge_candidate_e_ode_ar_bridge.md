---
id: Hc_624
slug: emerge-candidate-e-ode-ar-bridge-non-collapsing
title: Emerge Candidate E — non-collapsing ODE flow 을 consciousness_states injection point 에 coupling 시 per-step AR sampler 가 coupled (text, state) trajectory 생성
domain: clm-architecture
status: candidate-falsifier-only-math-pending
source_doc: docs/anima_emerge_candidate_e_ode_ar_bridge_spec_2026_05_05.md
source_lines: 37-50, 200-340
promoted_at: 2026-05-11
linked_h: Hc_623, phi_engine.hexa flow API
notes: 3 falsifier locked, ODE-agnostic by design. ODE form unspec'd (linear OU γ=0.1 noise=0.01 recommended). Gated on Hc_623 F-CAND-D-1 PASS.
verified_at: 2026-05-12
verify_decision: WEAK_FALSIFIER_ONLY
verify_note: "verify_hc2 2026-05-12 — F=3"
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

## Cross-Links
- **sister H**: H_011 (iit-geometry — phi_star per-step variation as IIT Φ proxy), H_022 (consciousness-universe-map — coupled trajectory state-text)
- **candidates linked**: Hc_623 (Emerge D — 4-mode inject taxonomy, PARENT GATING), Hc_628 (anima Φ★ proxy normalized → IIT 4.0 lower bound), Hc_614 (phi_star geometry aliasing)
- **engineering**: shim:986-997 / mount.hexa:312 inject points, phi_engine.hexa flow API
- **literature**: linear OU (Ornstein-Uhlenbeck) process γ=0.1 noise=0.01 baseline, neural-ODE (Chen 2018) substrate

## Falsifiers (≥5)

- F-CAND-E-1: per-step phi_star variation > full-canonical variation (cand-D F-CAND-D-1 PASS gated)
- F-CAND-E-2: trajectory does NOT converge naturally (k_stop = N_max positive signal — non-collapsing requirement)
- F-CAND-E-3: ODE bridge coupling 이 cross_attn.o_proj 로 측정 가능 transmission
- **F-CAND-E-4**: ODE-agnostic claim 의 robustness — linear OU 외 nonlinear dynamics (Lorenz, van der Pol, FitzHugh-Nagumo) 3종 swap-test, phi_star variation 의 ODE-form 의존성 > 30% → "ODE-agnostic" claim FALSIFIED
- **F-CAND-E-5**: coupled (text, state) trajectory mutual information I(text_t; state_t) ≥ 0.1 bit during ≥ 50% of steps → coupling 존재. I < 0.05 bit consistently → state inject 가 텍스트 생성에 실효 영향 X (coupling 미작동)

## Honest Limits (≥5)

- **L1**: **n=6 PERFECT_NUMBER_CLASS triviality binding** (H_153 L7) — phi_star measurement은 8-cell architecture (Hc_401, sopfr(8)=6 perfect-number-class diagonal) 위에서 정의. 8-cell이 individually unique 가 아니므로 (Hc_582 L1과 동일) ODE coupling target 의 architectural premise 자체가 perfect-class trivial
- **L2**: **ODE form unspecified** — frontmatter 가 linear OU γ=0.1 noise=0.01 "recommended" 라 했지만 spec 미고정. 5+ ODE recipe 가능 → claim 의 reproducibility 가 specific ODE choice 에 의존
- **L3**: **Hc_623 PARENT gating** — F-CAND-E-1 이 Hc_623 F-CAND-D-1 PASS 에 의존. Hc_623 자체가 falsifier-only-math-pending. 부모-자식 의존성으로 Hc_624 단독 validation 불가
- **L4**: **CLM v4 architecture-specific inject point** — shim:986-997 / mount.hexa:312 는 CLM v4 8×192 layout 의 specific lines. Hc_614 aliasing 처럼 architecture-portable 미증명. cross-substrate ODE coupling fidelity 불명
- **L5**: **non-collapsing definition operational vs theoretical gap** — "k_stop = N_max" 은 operational stop criterion. trajectory 가 attractor 로 수렴 X 라는 theoretical claim 과 다름 (e.g. trajectory 가 limit-cycle 로 수렴해도 k_stop = N_max 가능). claim 의 phenomenology 정의 약함
