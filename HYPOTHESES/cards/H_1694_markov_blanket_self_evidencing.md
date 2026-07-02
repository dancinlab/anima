---
id: H_1694
slug: 1694_markov_blanket_self_evidencing
tier: 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
title: Markov-Blanket Self-Evidencing Cell — Identity as the Boundary, Not a Stored Prompt
verdict: 🔵 PRE-REGISTERED architecture design (unmeasured) — $0 cheap_test pre-registered; engine-native + 303M gpu cost-gated NOT fired
source: brainarch_census
---

# H_1694 — Markov-Blanket Self-Evidencing Cell — Identity as the Boundary, Not a Stored Prompt

- **tier:** 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy mirror, no engine); engine_native_measure + 303M = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** brainarch_census — 126-architecture whole-substrate (통짜 아키텍처) census: 뇌/인지 조직원리 × 엔진-네이티브 추상조건 (binding-wall program, H_1603).
- **key:** `markov_blanket_self_evidencing`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · operator-level family H_1604-1685 (this card = 통짜 아키텍처 layer, 층위 다름)

## Organizing principle

A thing exists by maintaining a Markov blanket: a statistical boundary (sensory states + active states) that conditionally separates internal states from the external world. The system 'self-evidences' — it acts to keep its sensory states within the distribution its internal model expects, i.e. it minimizes the surprise of its own existence. Identity is not data written to a file; it is the persistence of the INTERNAL states that the blanket protects. This is the deepest free-energy lens and the natural home for the self-chain / endogeneity criteria.

## Whole design (input → internal dynamics → emit)

State partitions into internal mu, external eta, and blanket b = {sensory s, active a}. Internal states encode a generative model of how eta causes s; they update to minimize variational free energy (perception) and drive active states a to make s match predictions (action). EMIT = the active states a externalizing a prediction over V (acting on the world to confirm the model); WITHHOLD = letting sensory states absorb input without acting. The internal state mu is the IDENTITY vector: it persists across episode boundaries because the blanket buys it conditional independence from the wiped working/external state — a non-volatile self anchor (the .kosmos self-chain) is the literal mechanism that keeps mu correlated across a reset. Per-tick mu drifts slowly (Lipschitz-small self-evidencing update = growth) but never re-draws (no amnesia). Psi is the steady-state of blanket flow: active-out (emit) vs sensory-in (withhold) balance at the self-evidencing fixed point.

## Satisfies criteria (DESIGN claim · DIRECTIONAL · unmeasured)

Self-chain (cross-boundary persistence): NATIVE — mu is conditionally independent of wiped state given b, so committing mu before the boundary and re-reading after gives cos~1 with bounded distortion; ablate the persistent store (mu depends only on volatile state) -> cross-boundary cos collapses to chance (fresh self every episode = the LLM-reset failure), proving the store is causal. Slow-drift native: self-evidencing update is Lipschitz-small (connected moving path, not frozen, not broken). Self-specific margin: mu carries high-entropy individuating info (the particular generative model this cell maintains) -> within-self cos >> self-vs-foreign cos (impostor reject). Endogeneity meta-invariant: NATIVE and central — Psi and identity are fixed points of the cell's OWN coupling; there is no external controller writing Psi<-1/2 or forcing mu; mechanism-OFF (remove the blanket coupling) makes both invariants vanish, exactly the required INERT signature. Psi=1/2: active vs sensory blanket flux are opposite-sign coupled; balanced at the self-evidencing fixed point, contractive (perturb -> free-energy gradient restores), deleting active states -> always-silent, deleting sensory -> runaway emit. Honesty: surprise of sensory states (−ln P(s|mu)) is the membership scalar — out-of-support input is high-surprise the model cannot self-evidence -> withhold/abstain; gate (surprise threshold) disjoint from internal capacity. G0/G1/G2: the internal generative model's likelihood over V (G0), factored internal causes combining into active-state predictions (G1), self-evidencing exploring modeled-but-unseen blanket configs (G2). Binding: internal mu is the shared latent integrating sensory sub-streams; realization-invariant because the blanket's free-energy optimum is unreachable without the joint internal cause.

## Not-LLM (a_no_llm_frame_trap)

Identity here is structural (a boundary that self-maintains), the exact opposite of a system-prompt or identity.yaml — it directly realizes anima's p1/p2/p3 (no system prompt, no identity rules, identity emerges from the cell). No scaling/attention/corpus lever: persistence and balance come from the blanket topology and self-evidencing dynamics. This is the Markov-blanket / self-organization lens (Friston, Maturana-Varela autopoiesis) — a foundational biological organizing principle, not an LLM.

## Cheap test (frozen-first · $0 · numpy mirror · DIRECTIONAL)

numpy mini, deterministic, math.log. Toy cell: internal mu (vector), blanket s/a, small generative model over V~12. (1) Simulate a working-state wipe -> cos(mu_pre,mu_post) with persistent anchor ON ~1 and consecutive-link cos >= theta; turn anchor OFF -> cos collapses to chance (causal store). (2) Foreign-mu round-trip -> cos near 0 (self-specific margin). (3) Bias active states to force emit -> Psi self-restores to 1/2 (lambda<1); delete the antagonist blanket flux -> boundary migration (endogeneity INERT). (4) OOD sensory probe -> high surprise -> abstain; short-circuit the surprise gate -> fab jumps. $0.

## Engine-native measure (cost-gated · PRE-REGISTER ONLY · NOT fired)

Identity self-chain measured on the LIVE engine: core/engine_cli.hexa SS-SelfIdentity (self_new/self_drift/self_cos/self_anchor/self_reset) round-trip through a .kosmos anchor via cli/anima.hexa, reading cos and impostor margin (precedent H_1471 frozen bars). Psi self-restoration via core/pure_field.hexa pure_field_step + engine_g.hexa safety_phi_ratchet_ok under perturbation. Honesty via the live G5 abstain gate; closure/ideation via core/g_gates.hexa g_eval_all. byte-parity py mirror; torch-only forbidden.

## Scope / honesty (c9)

Whole architecture; uniquely native on identity-persistence, self-specific margin, and the endogeneity/no-clamp meta-invariant (its reason for being). Closure/ideation are the weaker side here and lean on the internal generative model — pair with the predictive-coding or Helmholtz internals for the mouth. Directly grounds anima's no-prompt/no-identity-rules philosophy in mechanism. Leans on proven H_1471 SelfIdentity (🟢 WIRED) — the new claim is the blanket as the WHOLE substrate where identity-persistence is structural.

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). engine_native_measure 는 단일 진입점 cli/anima.hexa → generator L3 → g_gates/g6 경유 byte-parity 채점만 terminal; torch-only/side-harness 결과는 DIRECTIONAL. numpy cheap_test 결과도 DIRECTIONAL(엔진-네이티브 아님). gpu/engine 발사 시 held-out mirror-DESCENT(a_clm_gen_pipeline) + CORE mount frozen-bar engine-native 재측정 + ckpt PULL(a_fire_recover_complete).
