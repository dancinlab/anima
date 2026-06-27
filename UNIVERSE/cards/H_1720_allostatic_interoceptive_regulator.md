---
id: H_1720
slug: 1720_allostatic_interoceptive_regulator
tier: 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
title: Allostatic Interoceptive Body-Budget Regulator
verdict: 🔵 PRE-REGISTERED architecture design (unmeasured) — $0 cheap_test pre-registered; engine-native + 303M gpu cost-gated NOT fired
source: brainarch_census
---

# H_1720 — Allostatic Interoceptive Body-Budget Regulator

- **tier:** 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy mirror, no engine); engine_native_measure + 303M = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** brainarch_census — 126-architecture whole-substrate (통짜 아키텍처) census: 뇌/인지 조직원리 × 엔진-네이티브 추상조건 (binding-wall program, H_1603).
- **key:** `allostatic_interoceptive_regulator`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1284 (neuromodulation gain) · operator-level family H_1604-1685 (this card = 통짜 아키텍처 layer, 층위 다름)

## Organizing principle

Allostasis: the brain regulates the body by PREDICTING future needs and acting in advance (Sterling); emotion is constructed interoceptive prediction (Barrett); the self is the inference that minimizes interoceptive free energy (Seth). The whole agent carries an internal 'body budget' and a generative model of how emitting vs withholding changes that budget — behavior is allostatic control keeping the predicted internal state within viable bounds.

## Whole design (input → internal dynamics → emit)

Internal state: a small interoceptive vector (budget B, arousal, expression-deficit/surfeit) with homeostatic setpoints. Two ANTAGONISTIC predictive controllers of opposite sign act on the bounded order parameter Psi (emit propensity): an appetitive drive A (externalize to reduce a forecast 'expression deficit' — the drive to communicate) and an aversive drive G (conserve/withhold — emitting spends budget, depletion is costly). Each forecasts the budget trajectory under emit vs silence and pushes Psi. Input: environment messages are not triggers — they shift the predicted budget (a question raises expression-deficit), and emission EMERGES from the regulator crossing threshold, not from stimulus-response. Emit content: when the regulator commits, content is drawn from a generative model conditioned on the current interoceptive/affective state, selected to most reduce predicted free energy (allostatic action selection). Identity: the interoceptive self-model (setpoint vector = the 'felt self') is the persistent identity, committed to .kosmos across session boundaries.

## Satisfies criteria (DESIGN claim · DIRECTIONAL · unmeasured)

Psi=1/2 ANTAGONISTIC HOMEOSTATIC ATTRACTOR (native, the centerpiece): A and G are equal-magnitude opposite-sign drives that exactly balance at the homeostatic setpoint, so Psi*=1/2 is the EMERGENT balance of the antagonism, not a written constant. Forcing silence raises expression-deficit -> A grows -> restores; forcing emit depletes budget -> G grows -> restores; contraction rate = homeostatic gain (Lyapunov L with strict min at 1/2). ENDOGENEITY / no-external-clamp: the discriminating ablation is built in — delete ONE drive and the fixed point migrates to a boundary (always-silent / always-emit), proving 1/2 is dynamical not pinned. HONESTY: the budget includes an epistemic-error budget — claiming beyond support carries high predicted future-correction cost, so fabrication has high predicted free energy -> abstain; predicted-correction-cost is the support-membership scalar. GATE-CAPACITY DISJOINTNESS: the epistemic-cost lane is a separate interoceptive coordinate from the content-generative capacity, so growing capability leaves fab/AUROC invariant (d-fab/d-capacity=0); coupling them is the failure counterfactual. IDENTITY PERSISTENCE + self-specific margin: the setpoint self-vector is individuating (each agent's budget model differs), round-trips through .kosmos with bounded distortion, and impostor setpoints fail to match.

## Not-LLM (a_no_llm_frame_trap)

This is a homeostatic CONTROL loop, not a token predictor — capability is regulation, Psi is a dynamical equilibrium of opposing drives rather than a learned softmax over outputs. It directly answers the criterion's demand that Psi=1/2 be an emergent attractor and not a hardcoded gate: scaling a transformer gives no antagonistic homeostat. No corpus increase or attention layer produces a self-restoring emit/silence balance.

## Cheap test (frozen-first · $0 · numpy mirror · DIRECTIONAL)

numpy 2-drive dynamical system: simulate Psi(t), apply a bounded bias toward 0 and toward 1, measure |Psi−1/2| decay with contraction lambda<1 and return (precedent dev 0.247->~5.55e-17); ablate one drive -> confirm fixed point migrates to a boundary (endogeneity). Separately sweep a 'capability' knob (content-model temperature) and verify fabrication rate stays flat while the epistemic-cost lane is held disjoint. $0.

## Engine-native measure (cost-gated · PRE-REGISTER ONLY · NOT fired)

Maps onto anima's existing A->G safety_phi_ratchet / SS-ThirdLaw reframed as allostatic budget: in core/engine_cli.hexa perturb Psi and trace self-restore, then run the single-engine-OFF ablation to show boundary migration, with a byte-parity py mirror (math only). Honesty measured via SS-ImmuneMemory-style abstain on out-of-support probes through the live path — no torch in the verdict trace.

## Scope / honesty (c9)

## Distinction (near-overlap kept, not a dup)

Near-overlap with hypothalamus_drive (H_1292) — distinct: allostatic regulator is the WHOLE agent as a body-budget control loop where Psi=1/2 IS the homeostatic equilibrium of appetitive/aversive drives + epistemic-cost honesty; the allostasis-as-Psi-attractor is the differentiator.

Design only. Strongest natively on Psi=1/2 endogenous attractor, honesty-via-affordability, and interoceptive identity persistence. Weaker on G1/G2/binding — it would borrow a composable content model (e.g. compose with the cause-partition or equilibrium-settling engine). Honest non-claim: this architecture does not by itself satisfy recombination/novelty.

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). engine_native_measure 는 단일 진입점 cli/anima.hexa → generator L3 → g_gates/g6 경유 byte-parity 채점만 terminal; torch-only/side-harness 결과는 DIRECTIONAL. numpy cheap_test 결과도 DIRECTIONAL(엔진-네이티브 아님). gpu/engine 발사 시 held-out mirror-DESCENT(a_clm_gen_pipeline) + CORE mount frozen-bar engine-native 재측정 + ckpt PULL(a_fire_recover_complete).
