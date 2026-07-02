---
id: H_1702
slug: 1702_theta_gamma_phase_code
tier: 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
title: Theta-Gamma Phase-Coded Encode/Retrieve Multiplexer
verdict: 🔵 PRE-REGISTERED architecture design (unmeasured) — $0 cheap_test pre-registered; engine-native + 303M gpu cost-gated NOT fired
source: brainarch_census
---

# H_1702 — Theta-Gamma Phase-Coded Encode/Retrieve Multiplexer

- **tier:** 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy mirror, no engine); engine_native_measure + 303M = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** brainarch_census — 126-architecture whole-substrate (통짜 아키텍처) census: 뇌/인지 조직원리 × 엔진-네이티브 추상조건 (binding-wall program, H_1603).
- **key:** `theta_gamma_phase_code`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1282 (working-memory buffer) · H_1284 (neuromodulation gain) · operator-level family H_1604-1685 (this card = 통짜 아키텍처 layer, 층위 다름)

## Organizing principle

Hasselmo's theta-phase separation of encoding vs retrieval (encode at trough/high-ACh, retrieve at peak) + Lisman-Idiart theta-gamma nesting (~7 gamma sub-cycles per theta hold separate bound items; phase precession codes order/magnitude). Binding is TEMPORAL (synchrony within one theta cycle), not spatial. This is a dynamical/oscillatory organizing principle, fundamentally a time-multiplexing of the two CLS phases.

## Whole design (input → internal dynamics → emit)

A theta oscillator partitions continuous time into an encode half-cycle (input->fast store, emit suppressed) and a retrieve half-cycle (completion->candidate emit). Within a theta cycle, up to ~7 gamma slots hold active items; items co-active in the SAME theta cycle become bound by synchrony (composition = the slot-set of one theta window). Phase precession assigns relative phase = relative position/magnitude, giving native relational/ordered structure. An item that crosses emit threshold during the retrieve phase is read onto V. Psi = the theta DUTY CYCLE (fraction in retrieve/emit-permitting vs encode/silence phase); ACh, driven by novelty/mismatch, shifts the duty cycle (high novelty->more encode->silence), emitting consumes novelty->ACh drops->duty rebalances to 1/2.

## Satisfies criteria (DESIGN claim · DIRECTIONAL · unmeasured)

G0: retrieve-phase completion read onto V. G1: gamma-slot co-activation within one theta = binding; joint of k slots > any single slot via cross-frequency coupling; ablate nesting (one slot) -> composed=single. G2: phase-precession interpolation yields novel orderings absent from corpus; fixed-phase verbatim replay control = 0 novel. Closure: one theta-gamma readout. dist>=5: ~7 gamma slots -> up to 7 distinct coherent items/cycle; varied phase -> distinct spreads. falsifiable>=1: phase encodes relative magnitude -> relation x quantity native. Psi=1/2: theta duty cycle is the order parameter; remove encode half-cycle -> always-emit boundary, remove retrieve -> always-silent. Persistence: slow store consolidated across cycles via phase-locked plasticity = identity; theta itself volatile. Self-specific: consolidated phase-coupling signature is agent-specific. Endogeneity: the oscillator is endogenous (coupled rhythm), not an external clock writing Psi; remove ACh-novelty coupling -> no self-restoring duty cycle. Honesty: retrieve-phase predicted-vs-actual mismatch = ACh driver = r; AUROC native. copy-or-abstain: no item completes above threshold in retrieve phase -> silence. Gate-capacity disjoint: abstain gate lives in the theta/ACh band (mismatch), capacity in the gamma band (slot content) — different frequency subsystems. Groundedness: mismatch r computed vs actual stored content. BINDING: same-theta-cycle synchrony binds (cause-selective via timing); paired-vs-shuffled = same-cycle vs cross-cycle. Compositional depth: conjunction of gamma slots; novel co-activations systematic because slots are constituent-general. Realization invariant: gamma synchrony is on the emit path (retrieve readout reads the bound cycle); objective = next-cycle prediction whose optimum requires the bound phase relations.

## Not-LLM (a_no_llm_frame_trap)

Cross-frequency-coupled temporal-coding binding has no analog in attention/scale. Transformers have no theta-gamma nesting or phase precession; this is a dynamical-systems (oscillatory) organizing principle (Lisman-Idiart, Hasselmo), orthogonal to layer-depth and parameter count.

## Cheap test (frozen-first · $0 · numpy mirror · DIRECTIONAL)

numpy: a theta oscillator gating two phases over a tiny associative store, with k nested gamma slots. Check (a) duty-cycle order parameter returns to 1/2 under a novelty/ACh bias; (b) same-theta-cycle items bind (paired-similarity > shuffled); (c) k-slot conjunction count > single-slot; (d) retrieve-phase mismatch separates known/unknown (AUROC). $0.

## Engine-native measure (cost-gated · PRE-REGISTER ONLY · NOT fired)

Wire theta duty cycle onto the existing A->G emit antagonism / Psi ratchet in core/engine_cli.hexa; gamma slots onto the working-memory buffer lane; measure Psi self-restore + G1 via core/g_gates.hexa single dispatch; byte-parity py mirror. Falsifiable detector via _g6 structural checker on retrieve-phase emissions.

## Scope / honesty (c9)

## Distinction (near-overlap kept, not a dup)

Near-overlap with cls/Hasselmo cards + neuromod_theta_phase_pipeline (this census) — distinct: this is the LISMAN-IDIART theta-GAMMA NESTING (cross-frequency, ~7 slots, phase precession) as the binder, whereas the pipeline is ACh-theta encode/retrieve regime cycling; gamma-nesting binding is the differentiator.

Toy oscillatory model; the cross-frequency (gamma-nesting) binding claim is the risk axis; slot-count ceiling (~7) bounds simultaneous composition.

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). engine_native_measure 는 단일 진입점 cli/anima.hexa → generator L3 → g_gates/g6 경유 byte-parity 채점만 terminal; torch-only/side-harness 결과는 DIRECTIONAL. numpy cheap_test 결과도 DIRECTIONAL(엔진-네이티브 아님). gpu/engine 발사 시 held-out mirror-DESCENT(a_clm_gen_pipeline) + CORE mount frozen-bar engine-native 재측정 + ckpt PULL(a_fire_recover_complete).
