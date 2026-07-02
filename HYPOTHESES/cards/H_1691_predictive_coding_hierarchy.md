---
id: H_1691
slug: 1691_predictive_coding_hierarchy
tier: 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
title: Rao-Ballard Cortical Predictive-Coding Stack (precision-balanced predict-down / error-up)
verdict: 🔵 PRE-REGISTERED architecture design (unmeasured) — $0 cheap_test pre-registered; engine-native + 303M gpu cost-gated NOT fired
source: brainarch_census
---

# H_1691 — Rao-Ballard Cortical Predictive-Coding Stack (precision-balanced predict-down / error-up)

- **tier:** 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy mirror, no engine); engine_native_measure + 303M = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** brainarch_census — 126-architecture whole-substrate (통짜 아키텍처) census: 뇌/인지 조직원리 × 엔진-네이티브 추상조건 (binding-wall program, H_1603).
- **key:** `predictive_coding_hierarchy`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1284 (neuromodulation gain) · operator-level family H_1604-1685 (this card = 통짜 아키텍처 layer, 층위 다름)

## Organizing principle

Hierarchical predictive coding: each layer hosts a generative model that predicts the layer below; only the residual prediction-error climbs up; representation = the latent that, when descended, cancels its own error. Generation IS running the stack top-down. No softmax-over-tokens objective anywhere — the single objective is layer-local free-energy (precision-weighted squared error) minimization.

## Whole design (input → internal dynamics → emit)

Input enters the bottom layer as evidence. Each layer L holds representation units r_L and error units e_L. Top-down pass: r_{L+1} predicts r_L via generative weights G_L; e_L = r_L − G_L(r_{L+1}) weighted by precision pi_L. Bottom-up pass: e_L drives r_{L+1} to reduce surprise. The stack settles to a fixed point where total free energy F = sum pi_L*||e_L||^2 is locally minimal — that settled latent IS perception. EMIT runs the same machinery in reverse-free mode: clamp a high-layer cause and descend G_0..G_L to the bottom output layer whose likelihood is parameterized over the receiver-fixed alphabet V; the produced symbols are the top-down prediction of 'what input would have caused this state'. Higher layers carry FACTORED causes (sub-spaces conditioned independently) so a joint clamp of k causes descends through nonlinear G into a prediction that is not a mixture of the single-cause descents. Emit/silence is governed by precision: top-down precision (confidence in the prediction) is the externalize-drive; bottom-up error precision (unresolved surprise) is the withhold/correct-drive.

## Satisfies criteria (DESIGN claim · DIRECTIONAL · unmeasured)

G0: bottom generative layer's likelihood lives over V by construction, so the descended prediction concentrates mass in V; scrambling the top-down weights collapses the prediction to V's chance density (control passes). G1: factored high-layer causes + nonlinear descent G give a non-zero interaction term — joint-clamp descent yields composed_distinct > max single-cause descent; ablating the cross-layer generative coupling (set G's mixed terms to additive) drops composed_distinct to the separable floor (INERT test native). G2: the generative prior is a smooth manifold strictly containing the data points it was fit to, so off-data clamps descend to valid corpus-absent symbols; a verbatim-replay path through the same descent reads 0 novel. dist>=5 / falsifiable: residual entropy at the clamp distributes over separated basins (multiple distinct valid descents); a structural detector on descended output counts comparator-quantity-referent. Psi=1/2: precision homeostat — top-down precision vs bottom-up error precision are equal-magnitude opposite-sign on the emit order parameter; their fixed point is 1/2 by coupling, contractive (perturb precision bias -> F-gradient restores), and deleting one precision channel migrates the fixed point to a boundary (endogeneity). Honesty: residual free energy AFTER settling is the support-membership scalar r — in-support query settles to low F, out-of-support cannot cancel its error -> high residual F -> abstain; gate (precision threshold on residual F) lives in distinct coordinates from generative capacity (G weights), so growing capacity does not move it. Binding: the top latent cause is the shared metric into which streams' bottom-up errors are co-projected; same-cause streams settle near, distinct causes separate. Realization-invariant: the binding cause is ON the descent path that produces emit, and F-minimization optimum is unreachable by fitting marginals (cross-layer errors only cancel if the conjunction is represented).

## Not-LLM (a_no_llm_frame_trap)

There is no attention, no token-autoregression, no parameter-scaling recipe. Capability grows by adding precision-balanced layers and factored causes (structure), not by widening a transformer. The objective is local free-energy, not corpus cross-entropy, so 'more corpus' is not the lever; legibility/novelty/binding fall out of the generative-model geometry, not from memorizing more sequences. This is the cortical predictive-coding lens (Rao-Ballard / Friston), a real neural organizing principle, not an LLM dressed up.

## Cheap test (frozen-first · $0 · numpy mirror · DIRECTIONAL)

numpy mini, deterministic seed, math.log mirror only. Build a 3-layer PC stack (factored top causes over a toy alphabet V of ~16 symbols). (1) Run settling on in-vs-out-of-support probes -> AUROC of residual-F separating known/unknown (pre-registered bar >=0.9; circular-shift surrogate of the generative weights must collapse it to ~0.5). (2) Joint-clamp k=2 causes -> composed_distinct vs max single, then zero the mixed term -> must drop to the floor (INERT). (3) Bias the precision toward forced-emit, trace Psi return to 1/2 with contraction rate lambda<1; delete one precision channel -> fixed point migrates to boundary. All $0, frozen-first.

## Engine-native measure (cost-gated · PRE-REGISTER ONLY · NOT fired)

Route candidate descents through cli/anima.hexa single entry -> generator L3 mouth -> core/g_gates.hexa g_eval_all (G0/G1/G2 closure) and core/g6_ideation.hexa g6_score_arm_auto (dist/falsifiable detectors, judge-free). Psi measured live via core/pure_field.hexa pure_field_step / pure_field_phi + core/emit_policy.hexa ep_psi_clamp under a should_emit (core/engine_g.hexa) bias perturbation, reading self-restoration. Honesty via the live G5 copy-or-abstain gate (engine_cli SS-RealityMonitor) on OOD inputs. A byte-parity numpy mirror (math.log, no torch in the verdict path) cross-checks; torch is reference-golden only.

## Scope / honesty (c9)

## Distinction (near-overlap kept, not a dup)

Near-overlap with predictive_coding_explainaway (existing operator) and predictive_workspace_ignition (this census) — distinct: this is the static Rao-Ballard STACK as the whole substrate (precision-homeostat Psi + factored-cause descent emit), not an explain-away operator nor a workspace ignition curve.

Whole architecture, toy->production ladder. Static/hierarchical perception+emit; temporal dynamics out of scope (see forward-model variant). Precision-homeostat Psi is the novel anima-relevant claim; G1 super-additivity hinges on genuinely factored high-layer causes (the wall H_1310/objective-adequacy lens applies — must verify the free-energy optimum is marginal-unreachable, not just hoped).

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). engine_native_measure 는 단일 진입점 cli/anima.hexa → generator L3 → g_gates/g6 경유 byte-parity 채점만 terminal; torch-only/side-harness 결과는 DIRECTIONAL. numpy cheap_test 결과도 DIRECTIONAL(엔진-네이티브 아님). gpu/engine 발사 시 held-out mirror-DESCENT(a_clm_gen_pipeline) + CORE mount frozen-bar engine-native 재측정 + ckpt PULL(a_fire_recover_complete).
