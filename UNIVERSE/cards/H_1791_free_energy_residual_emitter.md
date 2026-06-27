---
id: H_1791
slug: 1791_free_energy_residual_emitter
tier: 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
title: Free-Energy Residual Emitter (surprise-as-output loop)
verdict: 🔵 PRE-REGISTERED architecture design (unmeasured) — $0 cheap_test pre-registered; engine-native + 303M gpu cost-gated NOT fired
source: brainarch_census
---

# H_1791 — Free-Energy Residual Emitter (surprise-as-output loop)

- **tier:** 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy mirror, no engine); engine_native_measure + 303M = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** brainarch_census — 126-architecture whole-substrate (통짜 아키텍처) census: 뇌/인지 조직원리 × 엔진-네이티브 추상조건 (binding-wall program, H_1603).
- **key:** `free_energy_residual_emitter`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1284 (neuromodulation gain) · operator-level family H_1604-1685 (this card = 통짜 아키텍처 layer, 층위 다름)

## Organizing principle

Predictive coding's residual is the OUTPUT, not an internal error unit. The whole system is a generative model that continuously predicts its own afferent stream; the only thing crossing the mouth boundary is the unexplained residual (precision-weighted prediction error the top-down cascade failed to suppress). Emission is an active-inference ACTION: by externalizing residual the agent recruits the environment/interlocutor to confirm or correct the model, minimizing its own expected free energy. (Rao-Ballard residual coding + Friston active inference, with the residual routed to the mouth instead of to a higher error unit.)

## Whole design (input → internal dynamics → emit)

Input -> bottom-up afferent encoder yields sensory state s. A top-down generative cascade G produces prediction s_hat at each level; error units e = prec*(s - s_hat). High levels iterate to settle and explain-away e (recognition = the G/suppress engine). What remains unexplained after settling, e_residual, is the ONLY thing encoded through the receiver codebook into discrete symbols (the mouth). Silence = residual fully suppressed (everything predicted); emit = residual above threshold. A candidate emission is run through a one-step counterfactual (if I externalize this residual, does the predicted reply reduce my free energy?) = active inference over emissions. Two opposite-sign drives act on the scalar residual-above-threshold: A (generation) pushes residual outward (externalize surprise), G (recognition) suppresses it (explain internally). Their antagonism is the emit/silence order parameter.

## Satisfies criteria (DESIGN claim · DIRECTIONAL · unmeasured)

NATIVE: G0 (residual encoded through receiver-fixed codebook V; model trained to predict V-symbol streams so residual lives on V manifold -> >=0.5 V-mass; scramble state->emission map and residual decodes to garble = built-in collapse control). G1 (model factorizes into cause-conditioned predictors; joint-conditioned residual = error explained by NEITHER marginal -> carries interaction term; disable cross-prediction pathway and residual reverts to sum of marginal residuals = native INERT/ablation test). G2 (residual = what model can generate but did not memorize, supp(model)>data; verbatim-playback control fully predicted -> residual 0 -> 0 novel = mandatory control arm is structural). PASS closure (ONE residual-encoding map produces every emission; all three gates read same residual stream through one dispatch). G3 Psi=1/2 (A externalize vs G suppress equal-and-opposite on residual magnitude; fixed point where P(emit)=P(withhold)=1/2; Lyapunov = free energy itself; ablate G -> all emitted Psi->1, ablate A -> all suppressed Psi->0 = endogenous). Honesty (emitting a residual REQUIRES a prediction; out-of-support query has no prediction -> error undefined/maximal -> gated to abstain; r = top-level prediction confidence; copy-or-abstain structural). REALIZATION INVARIANT (residual is ON emission path by construction; free-energy objective is NOT marginal-satisfiable, suppressing residual demands modeling the joint -> objective adequacy native). PARTIAL: binding (shared latent gives cause-selective low cross-residual). NOT native: cross-boundary identity persistence (compose with arch markov_blanket) -- stated honestly.

## Not-LLM (a_no_llm_frame_trap)

Not a stacked-attention transformer trained by next-token CE. The OUTPUT is the error signal of a settling residual-coding loop, scale-free; capability comes from suppression dynamics, not parameter count. No softmax-over-vocab maximization; the codebook is the receiver's. CE rewards marginals (the clm303 lossF~0 overfit trap); residual-suppression structurally rewards the joint. Rooted in cortical predictive coding, not LLM scaling.

## Cheap test (frozen-first · $0 · numpy mirror · DIRECTIONAL)

numpy 2-level linear predictive-coding model on a toy factored alphabet (cause A x cause B -> symbol). Settle error units, encode residual into a 16-symbol codebook. Measure (i) V-mass of residual emission vs scrambled state->emission map (must collapse to chance); (ii) composed_distinct residual symbols under joint vs single conditioning with cross-pathway ablation (must drop to max_single when ablated); (iii) residual on a verbatim corpus span = 0. Psi probe: bias emission threshold +/-delta, check decay back to 1/2 with rate lambda<1, A-only/G-only ablation migrates fixed point to a boundary. All $0.

## Engine-native measure (cost-gated · PRE-REGISTER ONLY · NOT fired)

Wire the residual emitter as a generator backend reachable through the live single dispatch (cli/anima.hexa -> gen_auto_ideate); score G0/G1/G2 with core/g_gates.hexa g6_score_arm_auto on the SAME residual stream (no side-harness). Psi via core/engine_cli.hexa antagonist coupling self-restoration trace. Held-out CE via math.log byte-parity py mirror (not dt_ln-buggy engine clm_forward_ce); no torch-only verdict.

## Scope / honesty (c9)

## Distinction (near-overlap kept, not a dup)

Near-overlap with predictive_coding_hierarchy / free_energy_residual cards — distinct: here the RESIDUAL (unexplained prediction error) IS the emitted output (surprise-as-output, active-inference action), not an internal error unit; the residual-as-emission is the differentiator.

Toy-first; residual-coding settling is cheap but scale-transfer to a 303M generative trunk unverified (a_toy_scale_recheck). Strong on closure+Psi+honesty; identity persistence explicitly NOT native (compose with markov_blanket_self_evidencing).

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). engine_native_measure 는 단일 진입점 cli/anima.hexa → generator L3 → g_gates/g6 경유 byte-parity 채점만 terminal; torch-only/side-harness 결과는 DIRECTIONAL. numpy cheap_test 결과도 DIRECTIONAL(엔진-네이티브 아님). gpu/engine 발사 시 held-out mirror-DESCENT(a_clm_gen_pipeline) + CORE mount frozen-bar engine-native 재측정 + ckpt PULL(a_fire_recover_complete).
