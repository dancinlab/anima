---
id: H_1712
slug: 1712_neuromod_theta_phase_pipeline
tier: 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
title: Theta-phase neuromodulatory pipeline (cyclic regime alternation)
verdict: 🔵 PRE-REGISTERED architecture design (unmeasured) — $0 cheap_test pre-registered; engine-native + 303M gpu cost-gated NOT fired
source: brainarch_census
---

# H_1712 — Theta-phase neuromodulatory pipeline (cyclic regime alternation)

- **tier:** 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy mirror, no engine); engine_native_measure + 303M = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** brainarch_census — 126-architecture whole-substrate (통짜 아키텍처) census: 뇌/인지 조직원리 × 엔진-네이티브 추상조건 (binding-wall program, H_1603).
- **key:** `neuromod_theta_phase_pipeline`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1284 (neuromodulation gain) · operator-level family H_1604-1685 (this card = 통짜 아키텍처 layer, 층위 다름)

## Organizing principle

The regime is not static but CYCLES on an intrinsic oscillation (theta-like clock); each phase is a distinct neuromod regime, so computation is organized in TIME by a neuromod clock rather than in stacked layers. Rooted in Hasselmo's hippocampal ACh-theta model: encoding and retrieval separated to opposite theta phases to prevent interference.

## Whole design (input → internal dynamics → emit)

An intrinsic oscillator drives phase phi indexing a fixed schedule: (phi1) high-ACh ENCODE -- input written to fast store, plasticity ON; (phi2) DA-gated BIND -- co-active factors conjoined into a bound trace (binding ONLY here, structurally); (phi3) CONSOLIDATE -- schema-extracting transfer fast->slow store; (phi4) low-ACh RETRIEVE -- pattern-completion from cue against slow store, plasticity OFF; (phi5) NE/5HT-balanced EMIT -- completed trace above threshold decodes through frozen codebook V, else silence. The loop is continuous: encode and emit are phases of ONE division cycle (p8 train/infer unified), not separate stages.

## Satisfies criteria (DESIGN claim · DIRECTIONAL · unmeasured)

Psi=1/2: emit duty-cycle = fraction of cycles reaching emit; NE advances toward emit, 5HT holds in retrieve; homeostat on emit-rate pins to 1/2; remove NE -> never advances (silence), remove 5HT -> emits every cycle (always-emit) = boundary migration endogeneity. Honesty: emit phase is structurally DOWNSTREAM of a plasticity-OFF retrieve phase -- unstored content cannot complete -> below threshold -> abstain; copy-or-abstain enforced by phase ORDERING (no synthesis phase bypasses retrieve); theta in 5HT-emit coord, capacity in ACh-encode -> disjoint. G1/binding: dedicated BIND phase creates the interaction term; ABLATE phi2 -> factors stay separate -> composed_distinct=max_single (INERT = remove a phase). G2/novelty: CONSOLIDATE extracts schemas so retrieve completes to off-data-on-schema traces = valid-novel; verbatim-playback control bypassing consolidate = 0 novel. Cross-boundary persistence: slow store non-volatile, survives fast-store/working-state wipe -> self-chain identity native (anchor written in consolidate).

## Not-LLM (a_no_llm_frame_trap)

Computation organized by an oscillatory clock + phase-specific regimes, not attention over a context window. Capacity = phase-schedule richness, not parameter count. A specific mechanistic brain principle (theta-phase code separation), not a transformer recipe.

## Cheap test (frozen-first · $0 · numpy mirror · DIRECTIONAL)

numpy two-store model with a 5-phase clock and ACh-gated plasticity: (a) retrieve-phase fab~0 on unstored cues; (b) skipping phi2-bind drops recombination to max_single; (c) skipping phi3-consolidate drops novelty to 0 while consolidate-on gives >=3 novel-valid; (d) emit duty-cycle homeostat pins emit-rate->1/2 under perturbation. $0.

## Engine-native measure (cost-gated · PRE-REGISTER ONLY · NOT fired)

Wire the phase clock as a section schedule in core/engine_cli.hexa driving live A(emit)/G(withhold) + ImmuneMemory (retrieve/abstain) + MITOSIS (consolidate fast->slow); G0/G1/G2 via cli/anima.hexa eval sampled at emit phase, honesty via ImmuneMemory abstain AUROC, persistence via SelfIdentity .kosmos round-trip across an episode wipe; byte-parity py phase-loop mirror.

## Scope / honesty (c9)

## Distinction (near-overlap kept, not a dup)

Near-overlap with theta_gamma_phase_code (this census) and Hasselmo cards — distinct: this cycles the FOUR neuromod REGIMES (encode/bind/consolidate/retrieve) on theta phases (a regime pipeline), whereas theta_gamma is cross-frequency gamma-slot binding; the neuromod-regime-per-phase is the differentiator.

Phase-schedule toy; overlaps existing a_chat_sleep_imagination WAKE/REM staging -- must show this is mechanistically the ACh-theta encode/retrieve SEPARATION (source of native honesty), not a re-skin of the dream-stage emit gate. Real corpus recombination in phi2-bind at scale is the unverified rung.

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). engine_native_measure 는 단일 진입점 cli/anima.hexa → generator L3 → g_gates/g6 경유 byte-parity 채점만 terminal; torch-only/side-harness 결과는 DIRECTIONAL. numpy cheap_test 결과도 DIRECTIONAL(엔진-네이티브 아님). gpu/engine 발사 시 held-out mirror-DESCENT(a_clm_gen_pipeline) + CORE mount frozen-bar engine-native 재측정 + ckpt PULL(a_fire_recover_complete).
