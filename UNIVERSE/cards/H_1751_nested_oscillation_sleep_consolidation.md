---
id: H_1751
slug: 1751_nested_oscillation_sleep_consolidation
tier: 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
title: Nested-Oscillation Sleep Conductor (SO-superset-spindle-superset-ripple triple-coupled transfer + wake/sleep limit cycle)
verdict: 🔵 PRE-REGISTERED architecture design (unmeasured) — $0 cheap_test pre-registered; engine-native + 303M gpu cost-gated NOT fired
source: brainarch_census
---

# H_1751 — Nested-Oscillation Sleep Conductor (SO-superset-spindle-superset-ripple triple-coupled transfer + wake/sleep limit cycle)

- **tier:** 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy mirror, no engine); engine_native_measure + 303M = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** brainarch_census — 126-architecture whole-substrate (통짜 아키텍처) census: 뇌/인지 조직원리 × 엔진-네이티브 추상조건 (binding-wall program, H_1603).
- **key:** `nested_oscillation_sleep_consolidation`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1283 (thalamus global-workspace) · operator-level family H_1604-1685 (this card = 통짜 아키텍처 layer, 층위 다름)

## Organizing principle

Active systems consolidation during NREM: hierarchically NESTED oscillations orchestrate fast->slow transfer — cortical slow-oscillation (SO) up-states GATE thalamic spindles, which GATE hippocampal sharp-wave ripples; ONLY reactivations that are TRIPLE phase-coupled (SO-up AND spindle AND ripple) are written to the slow cortical store, with homeostatic downscaling (SHY) clearing the fast buffer after transfer. The WAKE<->SLEEP alternation is itself the architecture's limit cycle and emit/silence order parameter — a direct extension of anima's existing 5-stage sleep lane, not a bolt-on.

## Whole design (input → internal dynamics → emit)

WAKE: input encoded into a fast episodic buffer (recent traces, salience-tagged); emission via codebook readout reading slow store + buffer. SLEEP: three coupled oscillators (SO omega_so superset spindle omega_sp superset ripple omega_rp) with phase-amplitude coupling; a transfer event fires ONLY at the triple-coincidence — one prioritized fast trace is time-compressed-replayed and distilled into the slow store via a small interleaved update, then cleared from the buffer (downscaling). Psi = wake-emission-drive vs sleep-consolidation-drive; the duty-cycle's symmetric point (equal pressures) = 1/2. Antagonism: accumulated unconsolidated load -> sleep pressure (withhold/consolidate); accumulated consolidated-but-unexpressed content -> wake pressure (emit).

## Satisfies criteria (DESIGN claim · DIRECTIONAL · unmeasured)

Psi=1/2 is the CLEANEST because the wake/sleep oscillation IS the emit/silence order parameter: two-phase limit cycle with a symmetric duty point, antagonism between encode-load and express-readiness, Lyapunov |phi_duty−1/2|, contraction (over-wake fills buffer->sleep pressure up; over-sleep depletes novel content->wake pressure up); endogeneity by INERT (remove sleep-pressure -> always-wake/always-emit boundary; remove wake-pressure -> always-silent), mapped to safety_phi_ratchet. HONESTY: fast buffer = episodic support (r = buffer resonance + slow-store distance, AUROC->1); the TRIPLE-COINCIDENCE gate is a strict provenance filter — content reaches the slow store ONLY via gated replay of ACTUAL stored traces, so there is no fabrication channel into semantic memory; copy-or-abstain = un-replayed/un-consolidated -> abstain; gate-capacity disjoint (ripple/coupling threshold separate from slow-store capacity); groundedness because replay reads actual buffer traces. G2 novelty: slow store distills REAL replayed compounds -> valid off-data emission; retrieval control = bypass-sleep (no consolidation, emit verbatim buffer) => 0 novel — native control arm. G1/BINDING: a ripple-compressed sequence co-reactivates constituents inside ONE SO up-state window -> bound into a single cortical conjunction update (composed>max_single); interaction-ablation = DECOUPLE the oscillators (no triple coincidence) -> only marginal single-trace updates -> drops to max_single; binding-via-temporal-compression, cross-frequency coupling = the binding clock, shared-cause traces co-replayed map near (retrieval@1). COMPOSITIONAL DEPTH = co-replay conjunction is non-separable (needs co-occurrence within one SO window) + slow-store systematicity. REALIZATION INVARIANT: slow store is on the wake-emit path; objective adequacy = distillation target is the COMPRESSED COMPOUND REPLAY, not raw next-byte marginals -> can't be minimized by fitting parts (defuses lossF~0 trap). SELF-CHAIN: identity anchor consolidated to slow store survives the fast-buffer wipe each sleep AND the session boundary; ongoing re-consolidation = slow drift; ablate slow anchor -> chance; high-entropy anchor -> impostor reject. CLOSURE/G0/dist/falsifiable: V-tied readout (scramble->collapse), dist from slow-store multi-attractor + sampling, falsifiable from co-replayed comparator x magnitude x referents. Measurement-faithfulness: wake-emission path = deployed, single dispatch.

## Not-LLM (a_no_llm_frame_trap)

This is OFFLINE TEMPORAL ORCHESTRATION via nested oscillations — a sleep ARCHITECTURE, not a bigger forward net. Transformers have no sleep phase, no SO-superset-spindle-superset-ripple triple-coupling gate, no homeostatic downscaling; they consolidate in a single wake-time gradient pass. The lever is the gated offline transfer scheduler (WHEN/WHAT transfers), rooted in NREM neuroscience — orthogonal to scale/attention (a_no_llm_frame_trap).

## Cheap test (frozen-first · $0 · numpy mirror · DIRECTIONAL)

numpy: 3 coupled phase oscillators (SO/spindle/ripple) + fast buffer + slow store; transfer gated on triple-coincidence. Frozen-first: (a) decouple oscillators -> composed drops to max_single (interaction-ablation = binding came from coupling); (b) bypass-sleep mode -> 0 novel (retrieval control); (c) perturb duty cycle off 1/2 -> restoration with lambda<1; (d) ablate slow anchor, simulate sleep+session wipe -> cross-boundary cos->chance vs ~1.0. $0.

## Engine-native measure (cost-gated · PRE-REGISTER ONLY · NOT fired)

Wake/sleep maps to live SS-SCN + the 5-stage a_chat_sleep_imagination lane; fast buffer -> OsmoticStore; slow store -> .clm mouth via core/generator.hexa gen_auto_backend; transfer = osmotic_learn distillation at gated ticks (triple-coincidence computed in engine). Measure via cli/anima.hexa eval -> core/g_gates.hexa g_eval_g0/g1/g2 + core/g6_ideation.hexa g6_score_arm_auto; Psi via safety_phi_ratchet duty perturbation; self-chain via self_new/self_drift/self_cos/self_anchor/self_reset across a simulated sleep boundary; honesty via osmotic_retains AUROC + fab. Byte-parity engine_cli.py mirror — no torch-only verdict.

## Scope / honesty (c9)

## Distinction (near-overlap kept, not a dup)

Near-overlap with rem_offline_world_model_consolidation / a_chat_sleep_imagination — distinct: the SO-spindle-ripple TRIPLE-COINCIDENCE gate is a strict provenance filter (only triple-coupled replay transfers) + wake/sleep as the Psi limit cycle; the nested-oscillation transfer gate is the differentiator.

Toy numpy first (a_toy_scale_recheck): oscillator coupling constants & replay-priority are scale-sensitive; directional until engine-native fire. NOTE it overlaps anima's existing sleep/SS-SCN lane — wire into that lane (a_verified_must_wire), do not duplicate; the new content is the triple-coincidence transfer gate + compound-replay distillation objective.

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). engine_native_measure 는 단일 진입점 cli/anima.hexa → generator L3 → g_gates/g6 경유 byte-parity 채점만 terminal; torch-only/side-harness 결과는 DIRECTIONAL. numpy cheap_test 결과도 DIRECTIONAL(엔진-네이티브 아님). gpu/engine 발사 시 held-out mirror-DESCENT(a_clm_gen_pipeline) + CORE mount frozen-bar engine-native 재측정 + ckpt PULL(a_fire_recover_complete).
