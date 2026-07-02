---
id: H_1799
slug: 1799_hasselmo_encode_retrieve_theta_toggle
tier: 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
title: Theta Encode/Retrieve Toggle — Plasticity-Gated Read/Write Multiplexer
verdict: 🔵 PRE-REGISTERED architecture design (unmeasured) — $0 cheap_test pre-registered; engine-native + 303M gpu cost-gated NOT fired
source: brainarch_census
---

# H_1799 — Theta Encode/Retrieve Toggle — Plasticity-Gated Read/Write Multiplexer

- **tier:** 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy mirror, no engine); engine_native_measure + 303M = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** brainarch_census — 126-architecture whole-substrate (통짜 아키텍처) census: 뇌/인지 조직원리 × 엔진-네이티브 추상조건 (binding-wall program, H_1603).
- **key:** `hasselmo_encode_retrieve_theta_toggle`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1284 (neuromodulation gain) · operator-level family H_1604-1685 (this card = 통짜 아키텍처 layer, 층위 다름)

## Organizing principle

Hasselmo's theta-phase encode/retrieve dynamics: within each theta cycle the hippocampal circuit alternates between an ENCODE mode (strong entorhinal afferent, plasticity ON, recurrent retrieval suppressed by cholinergic tone — intake, no read-out) and a RETRIEVE mode (recurrent CA3 dominates, plasticity OFF, afferent suppressed — read-out). Temporal multiplexing solves encode<->retrieve INTERFERENCE natively: the system never stores-new and reads-old in the same instant. CLS spine: encode-phase feeds the fast episodic write; retrieve-phase completions feed both emit and the slow distributed learner.

## Whole design (input → internal dynamics → emit)

An ENDOGENOUS phase variable (driven by the dynamics, NOT wall-clock — no clock-triggered speech) splits each cycle. Encode half: afferent gain HIGH, recurrent gain LOW, plasticity ON -> new input is pattern-separated and one-step-written to a fast CA3-like autoassociator; this half is SILENCE. Retrieve half: afferent gain LOW, recurrent gain HIGH, plasticity OFF -> a partial cue pattern-completes to a stored attractor; this half is EMIT. The slow neocortical learner trains ONLY on retrieve-phase completions (distilling stable attractors into distributed weights). Psi=1/2 is STRUCTURAL: it is the encode/retrieve DUTY CYCLE setpoint, the fixed point of an intake-drive (raises encode fraction when surprise high) antagonistic to an externalize-drive (raises retrieve fraction when settled), with cholinergic-like negative-feedback contraction. Honesty: retrieve completion only succeeds inside a stored basin -> completion residual = support scalar; no basin (out-of-support cue) -> completion fails -> abstain. Binding: encode writes conjunctive separated patterns; a partial cue of one constituent completes its bound partner.

## Satisfies criteria (DESIGN claim · DIRECTIONAL · unmeasured)

G0: retrieve read-out is constrained to stored attractors over V; scramble -> chance. G1 binding/depth: conjunctive encode + recurrent completion gives super-additive reachable set; ablate recurrence (no completion) -> max_single (INERT). G2: slow learner generalizes attractors -> valid corpus-absent outputs; verbatim playback = 0. dist>=5: multiple attractor basins + retrieve-phase exploration noise -> distinct-coherent completions; collapse (one basin) vs garble (no basin) are the two discriminated failures. Psi=1/2 — STANDOUT native: the encode/retrieve duty IS the order parameter; it maps directly onto the live A->G antagonist (G=withhold/encode, A=externalize/retrieve), self-restores with contraction lambda<1, and one-drive ablation migrates it to a boundary (all-encode = mute / all-retrieve = babble) proving endogeneity, not a clamp. honesty: completion-residual support gate (AUROC), phase-gain params disjoint from store capacity (gate-capacity disjointness), corrupt support -> completion fails (faithfulness). BINDING criterion: relational co-reference is native — completion-from-partial-cue recovers the bound partner above chance and selectively. Realization invariant: emit IS the retrieve-phase output (on-path); the slow learner trained on completions must represent conjunctions to predict them (objective adequacy).

## Not-LLM (a_no_llm_frame_trap)

Encode<->retrieve interference is solved by TEMPORAL multiplexing with plasticity gated to one phase — not by a parametric attention window over context. There is no simultaneous read+write; the dual learning system is a duty-cycled oscillator. Brain-rooted (Hasselmo cholinergic theta dynamics). Scaling parameters does not buy the interference-free property; the endogenous toggle does.

## Cheap test (frozen-first · $0 · numpy mirror · DIRECTIONAL)

numpy, frozen-first. Phase-gated autoassociator; interleave store/recall episodes. Pre-registered bars: (1) encode/retrieve toggle yields interference-free recall while always-on plasticity shows catastrophic interference (gap >= bar); (2) duty cycle self-restores after a forced bias perturbation with contraction lambda<1 (|dev|->~0); (3) ablate one drive -> duty -> 0/1 boundary (endogeneity); (4) completion-residual AUROC(known/unknown) ~ 1, shuffle -> 0.5.

## Engine-native measure (cost-gated · PRE-REGISTER ONLY · NOT fired)

Map encode/retrieve directly onto the live A->G engine (core/engine_cli.hexa): G=withhold/encode drive, A=externalize/retrieve drive; measure |Psi−1/2| restoration via the existing safety_phi_ratchet attractor, and run completion -> emit through core/clm_decode.hexa with G0/G1/G2 + dist scored via the single entry cli/anima.hexa -- eval (g_gates.hexa). byte-parity py mirror cross-checks; the A->G mapping makes this the most engine-tractable of the three — no torch-only verdict.

## Scope / honesty (c9)

## Distinction (near-overlap kept, not a dup)

Near-overlap with theta_gamma_phase_code / neuromod_theta_phase_pipeline (this census) — distinct: Hasselmo theta toggle makes the ENCODE/RETRIEVE duty cycle the literal Psi order parameter (plasticity gated to one phase = interference-free read/write), mapping onto the live A->G attractor; the encode/retrieve theta toggle is the differentiator.

Design-only. numpy is decisive for interference-freedom + Psi self-restoration + endogeneity + support-AUROC. The Psi=1/2 and BINDING criteria are the strongest native wins (Psi maps onto the existing engine attractor); G2 constrained-extrapolation depends on slow-learner training quality (GPU, held-out CE, a_chat_registers).

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). engine_native_measure 는 단일 진입점 cli/anima.hexa → generator L3 → g_gates/g6 경유 byte-parity 채점만 terminal; torch-only/side-harness 결과는 DIRECTIONAL. numpy cheap_test 결과도 DIRECTIONAL(엔진-네이티브 아님). gpu/engine 발사 시 held-out mirror-DESCENT(a_clm_gen_pipeline) + CORE mount frozen-bar engine-native 재측정 + ckpt PULL(a_fire_recover_complete).
