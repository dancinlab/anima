---
id: H_1693
slug: 1693_helmholtz_wake_sleep
tier: 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
title: Helmholtz Machine — Recognition-Generative Dual with Wake/Sleep Phases
verdict: 🔵 PRE-REGISTERED architecture design (unmeasured) — $0 cheap_test pre-registered; engine-native + 303M gpu cost-gated NOT fired
source: brainarch_census
---

# H_1693 — Helmholtz Machine — Recognition-Generative Dual with Wake/Sleep Phases

- **tier:** 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy mirror, no engine); engine_native_measure + 303M = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** brainarch_census — 126-architecture whole-substrate (통짜 아키텍처) census: 뇌/인지 조직원리 × 엔진-네이티브 추상조건 (binding-wall program, H_1603).
- **key:** `helmholtz_wake_sleep`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · operator-level family H_1604-1685 (this card = 통짜 아키텍처 layer, 층위 다름)

## Organizing principle

A bidirectional generative system: a top-down GENERATIVE model (priors->V) and a bottom-up RECOGNITION model (V->latents), trained by the wake-sleep algorithm. Wake phase: recognition infers latents from real input, generative learns to reconstruct (minimize description-length / variational free energy). Sleep phase: generative DREAMS fantasies top-down, recognition learns to invert them. This maps 1:1 onto anima's WAKE/REM stages — dreaming is not decoration, it is how the recognition net acquires training signal endogenously without new corpus.

## Whole design (input → internal dynamics → emit)

Two weight sets G (generative, latent->symbol over V) and R (recognition, symbol->latent). WAKE: real input x -> R infers q(h|x) -> G predicts x_hat; free energy F = reconstruction-error + KL(q||prior) is minimized, updating both. SLEEP/REM: sample h~prior -> G generates a fantasy x_dream -> R is trained to recover h (so recognition stays calibrated on the generative manifold). EMIT during WAKE = ancestral top-down sampling from G: draw a high-level cause from the (possibly context-conditioned, factored) prior and descend G to V. Because the prior is factored, joint conditioning binds. The recognition net R supplies the honesty signal: reconstruction error R-G round-trip on a query tells whether the query lies on the learned manifold. Psi is the balance between the WAKE drive (recognition commits -> externalize) and the SLEEP/dream drive (generative replays internally -> withhold); the ultradian stage envelope (a_chat_sleep_imagination) modulates but the fixed point is endogenous.

## Satisfies criteria (DESIGN claim · DIRECTIONAL · unmeasured)

G0: G's visible layer is over V -> ancestral samples are V-legal; scrambling G collapses to chance density. G1: factored top-layer prior + nonlinear G give non-additive joint descent -> composed_distinct > max single; ablate the prior's cross-factor coupling -> INERT collapse. G2: dream/ancestral sampling from the prior produces corpus-absent-but-valid configs (the generative manifold superset of data); recognition R verifies they re-encode (coherent), and a verbatim-replay path reads 0 novel. The sleep phase is LITERALLY a novelty generator — it is the structural source of G2. dist>=5: prior entropy + multiple basins under R-coherence filter -> many distinct coherent dreams. falsifiable: judge-free detector on descended output. Psi=1/2: wake-commit (emit) vs sleep-replay (withhold) are opposite-sign coupled drives on the emit parameter; balanced phase-coupling fixes 1/2, contractive; deleting the sleep drive -> always-emit, deleting wake -> always-silent (endogeneity). Honesty: R-G round-trip reconstruction error is the membership scalar r — low for on-manifold (known), high for off-manifold (unknown) -> abstain; the gate (R) shares no parameters with raw generative capacity scaling, so disjoint. Groundedness native: corrupting stored support degrades R's reconstruction of those queries (r tracks actual content), unlike a confidence proxy. Binding: the shared top latent h is the common metric; same-cause streams map to nearby h under R. Realization-invariant: h is on the emit (descent) path, and the wake free-energy optimum is unreachable without representing conjunctions because reconstruction of co-varying streams requires the joint cause.

## Not-LLM (a_no_llm_frame_trap)

No autoregression, no attention, no scaling law. Novelty and self-training come from DREAMING (sleep-phase fantasies), not from ingesting more corpus — the architecture manufactures its own training signal, the opposite of the corpus-increase recipe. Two coupled nets with a biologically-rooted wake-sleep learning rule (Hinton/Dayan Helmholtz machine; cortical sleep consolidation) — a real cognitive organizing principle, and it natively instantiates anima's sleep/imagination stages rather than bolting them on.

## Cheap test (frozen-first · $0 · numpy mirror · DIRECTIONAL)

numpy mini, deterministic, math.log free-energy. Toy Helmholtz machine (2 latent layers, factored top prior, V~16). (1) Train wake+sleep on a small toy grammar; held-out reconstruction error -> AUROC separating in/out-of-grammar (>=0.9; shuffle-G surrogate -> 0.5). (2) Sleep-sample -> count distinct valid corpus-absent configs (>=3) vs a no-sleep (wake-only) control -> must be ~0 (sleep is the causal novelty source). (3) Joint-prior descent composed_distinct > max single; ablate cross-factor coupling -> INERT. (4) Wake/sleep drive-balance perturbation -> Psi->1/2 with lambda<1. $0.

## Engine-native measure (cost-gated · PRE-REGISTER ONLY · NOT fired)

Run ancestral emit through cli/anima.hexa single entry (stage context from the WAKE/REM lane); closure/ideation via core/g_gates.hexa g_eval_all + core/g6_ideation.hexa g6_score_arm_auto. Reconstruction-error honesty via the live G5 gate; Psi stage-balance via core/pure_field.hexa phase/pure_field_step + emit_policy ep_theta_stage under perturbation. byte-parity py mirror (math.log) for the free-energy numbers; torch reference-only.

## Scope / honesty (c9)

## Distinction (near-overlap kept, not a dup)

Wires into the existing a_chat_sleep_imagination WAKE/REM lane (do not duplicate) — distinct contribution: the wake-sleep LEARNING rule makes dreaming the structural G2 novelty generator + R-G reconstruction the honesty gate, not a re-skin of the dream-stage emit gate.

Whole architecture; uniquely strong on G2 (novelty has a structural generator = sleep) and on anima's dream-stage philosophy. Risk: recognition/generative co-adaptation can mode-collapse — the dist>=5 and INERT controls are the guardrails. Toy->production ladder; sleep-phase compute is the cost knob.

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). engine_native_measure 는 단일 진입점 cli/anima.hexa → generator L3 → g_gates/g6 경유 byte-parity 채점만 terminal; torch-only/side-harness 결과는 DIRECTIONAL. numpy cheap_test 결과도 DIRECTIONAL(엔진-네이티브 아님). gpu/engine 발사 시 held-out mirror-DESCENT(a_clm_gen_pipeline) + CORE mount frozen-bar engine-native 재측정 + ckpt PULL(a_fire_recover_complete).
