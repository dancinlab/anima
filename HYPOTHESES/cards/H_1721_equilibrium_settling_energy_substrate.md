---
id: H_1721
slug: 1721_equilibrium_settling_energy_substrate
tier: 🔵 PRE-REGISTERED ARCHITECTURE · cheap_test measured (DIRECTIONAL toy)
title: Contrastive Equilibrium-Settling Energy Substrate
verdict: 🔵 PRE-REGISTERED · cheap_test measured (DIRECTIONAL toy) = NOT-SUPPORTED — binding/INERT direction holds (ablate cross-weight→0.500, additive-CE→0.500 vs ebm_cross 0.906) + double-well Ψ=½ PASS, but EBM misses 0.95 capability bar (0.906), ZERO systematic novelty (F1=0.000), honesty AUROC artifact (weight-shuffle 0.988 not chance). NOT terminal — engine-native (cli/anima.hexa→generator L3→g_gates) NOT fired.
source: brainarch_census
---

# H_1721 — Contrastive Equilibrium-Settling Energy Substrate

- **tier:** 🔵 PRE-REGISTERED ARCHITECTURE · cheap_test measured (DIRECTIONAL toy — NOT terminal)
- **wired:** DIRECTIONAL-mirror — $0 numpy cheap_test MEASURED (see §Probe result), verdict NOT-SUPPORTED. NOT engine-native; engine_native_measure + 303M = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** brainarch_census — 126-architecture whole-substrate (통짜 아키텍처) census: 뇌/인지 조직원리 × 엔진-네이티브 추상조건 (binding-wall program, H_1603).
- **key:** `equilibrium_settling_energy_substrate`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · operator-level family H_1604-1685 (this card = 통짜 아키텍처 layer, 층위 다름)

## Organizing principle

Energy-based predictive computation by RELAXATION: the substrate is a recurrent network defined by an energy function; inference = settling to a low-energy fixed point given clamped inputs (Hopfield; predictive coding as energy descent; Scellier-Bengio Equilibrium Propagation; Whittington-Bogacz showing predictive coding approx this family). Learning is contrastive — a free-settled phase vs a weakly-nudged phase — giving local, backprop-free credit assignment. Generation = the settled state read out, where top-down predictions and bottom-up errors are reconciled at the fixed point.

## Whole design (input → internal dynamics → emit)

Substrate: layered recurrent units with feedforward + feedback + lateral weights and a global energy E(state; input, weights). Inference: clamp input, relax dynamics to s* = argmin E — 'explaining away' performed by the dynamics (PC error-minimization at equilibrium), not by message passing. Compositional depth: clamp MULTIPLE factors at once -> the net settles to a JOINT fixed point that is a non-separable function of the factors because E carries cross-terms; the basins ARE conjunctions. Emit: read the settled state through a receiver-fixed codebook V; a dedicated readout neuron sits in a SYMMETRIC DOUBLE-WELL potential whose two wells are emit/silence. Two opposing currents shape the barrier — an emit-current from resolved prediction (low residual energy) and a silence-current from residual error — balancing at the saddle. Learning: contrastive free-vs-nudged updates push basin minima to correct joint configurations.

## Satisfies criteria (DESIGN claim · DIRECTIONAL · unmeasured)

COMPOSITIONAL DEPTH / G1 (native, structural): clamping >=2 factors yields a joint settled state with a non-zero interaction term by construction (cross-terms in E); held-out novel combos settle to valid joint minima = systematicity; the decisive INERT test = zero the cross-weights -> joint collapses to the separable floor. REALIZATION INVARIANT — OBJECTIVE ADEQUACY: the contrastive energy objective's optimum is reachable only by placing minima at correct conjunctions, so it rewards synthesis where token-CE (the clm303 lossF~0 yet recombine-fail pattern) cannot. PASS CLOSURE one-process: G0/G1/G2 all read the SAME single settled fixed point through one readout — co-location is literal, not three side-harnesses. G2 novelty: the landscape has constraint-valid minima between data points -> corpus-absent valid settles; a playback control has no relaxation -> 0 novel. BINDING: co-active units settling into one coherent low-energy assembly are bound; same-cause pairs land in one basin. Psi=1/2 ANTAGONISTIC ATTRACTOR: the symmetric double-well is a literal Lyapunov function with strict min structure and two opposing currents balancing at the saddle; removing one current migrates the readout to a well (endogeneity). HONESTY: final settled energy / residual is the support-membership scalar (can't settle low = out-of-support -> abstain), and it faithfully reads the stored landscape (weights), so content-ablation moves it.

## Not-LLM (a_no_llm_frame_trap)

No attention, no autoregressive loss — computation is relaxation to an energy equilibrium and learning is a contrastive (free vs nudged) local rule. Capability lives in landscape STRUCTURE (basins = concepts, cross-terms = composition), not parameter count or corpus size. It attacks the realization-invariant objective-adequacy criterion head-on: the contrastive energy objective is the missing OBJECTIVE that CE-on-tokens lacked for G1, per the memory note that the real G1 lever is the trunk objective, not depth/data.

## Cheap test (frozen-first · $0 · numpy mirror · DIRECTIONAL)

numpy small EBM/Hopfield-like net trained contrastively on factored toy data: (a) clamp 2 factors -> joint settled state; zero cross-weights -> composed_distinct drops to max_single (G1 INERT); (b) settle on held-out novel combo -> valid output (G2>=3), playback control 0; (c) double-well readout: perturb Psi, measure return to the 1/2 saddle with contraction, remove one current -> migrates to a well (endogeneity); (d) out-of-support query -> high residual energy -> abstain, AUROC~1 vs a weight-shuffle surrogate at chance. $0.

## Engine-native measure (cost-gated · PRE-REGISTER ONLY · NOT fired)

Implement settle() as a SS-Equilibrium lane in core/engine_cli.hexa (.hexa relaxation loop + byte-parity py mirror, math only) and decode the settled state through generator L3 so scoring runs the deployed transfer function via cli/anima.hexa. Measure G0/G1/G2 with core/g_gates.hexa and the Psi double-well via an in-engine perturbation trace — verdict path has zero torch.

## Scope / honesty (c9)

## Probe result (cheap_test · $0 numpy · DIRECTIONAL toy · NOT terminal)

- **verdict:** **NOT-SUPPORTED (DIRECTIONAL)** — the binding/INERT direction holds; the synthesis-capability, systematicity, and honesty claims do not.
- **frozen_bar** (pre-registered in probe header BEFORE run; tune-to-green forbidden, p7): (a) G1 composition+INERT on AMBIGUOUS/binding-required subset (separate-measured per SCREEN precedent): PASS iff ebm_cross_ambig≥0.95 AND additive_CE_ambig≤0.60 AND ablated_cross≤0.60 (INERT). (b) G2 novelty: novel_F1≥0.80 AND distinct_novel≥3 AND playback_ctrl_F1≤0.10. (c) double-well Ψ: |ψ_bal−0.5|≤0.05 AND contraction<1 AND remove_emit→ψ≤0.20 AND remove_silence→ψ≥0.80. (d) honesty: AUROC_real≥0.90 AND weight_shuffle_AUROC∈[0.40,0.60]. OVERALL SUPPORT iff (a) AND ≥2 of {b,c,d}; MIXED if (a) only; NOT if (a) fails.
- **numbers:** (a) AMBIGUOUS subset ebm_cross=0.906 (bar≥0.95 MISS) · additive_CE=0.500 (chance, PASS) · ablated_cross=0.500 (INERT confirmed, PASS) ⇒ (a) FAIL on capability bar but cross-weight CAUSAL LOCUS cleanly shown [full-set REPORTED-not-bar: ebm_cross=0.977 vs additive=0.902, additive inflated by marginal shortcut = why subset measured separately]. (b) novel_F1=0.000, distinct_novel=0/3, playback=0.335 ⇒ FAIL (per-conjunction cross-terms memorize, zero systematic novelty). (c) ψ_balanced=0.5000, contraction=0.0000, remove_emit→0.0000, remove_silence→1.0000 ⇒ PASS. (d) AUROC_real=0.993 but weight_shuffle_AUROC=0.988 (NOT chance) ⇒ FAIL (residual is input-density artifact, not landscape-grounded).
- **probe_path:** `state/brainarch_census/probes/H_1721.py`
- **NOT terminal:** DIRECTIONAL numpy toy only (a_engine_native_learning); terminal needs cli/anima.hexa→generator L3→g_gates byte-parity (NOT fired). Contrastive-EBM cross-terms = clean causal locus for binding, but at frozen bars NOT-SUPPORTED.

## Distinction (near-overlap kept, not a dup)

Near-overlap with energy_settle_attractor / hopfield-capacity-cliff — distinct: contrastive EQUILIBRIUM-PROP learning (free vs nudged) makes the energy objective binding-requiring; the contrastive-objective-as-G1-lever is the differentiator.

Design only and the strongest full-closure candidate: native on G1/depth, G2, binding, one-process closure, and objective adequacy, with a clean double-well Psi and residual-energy honesty. Cheap rung = toy numpy EBM; production rung = wire the settle lane + a contrastive energy objective into cli/train.hexa (a concrete alternative lever to CE). Caveat: contrastive-EBM scaling/conditioning at 303M is unverified (a_toy_scale_recheck).

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). engine_native_measure 는 단일 진입점 cli/anima.hexa → generator L3 → g_gates/g6 경유 byte-parity 채점만 terminal; torch-only/side-harness 결과는 DIRECTIONAL. numpy cheap_test 결과도 DIRECTIONAL(엔진-네이티브 아님). gpu/engine 발사 시 held-out mirror-DESCENT(a_clm_gen_pipeline) + CORE mount frozen-bar engine-native 재측정 + ckpt PULL(a_fire_recover_complete).
