---
id: H_1789
slug: 1789_intralaminar_diffuse_gain_ignition
tier: 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
title: Intralaminar Diffuse-Gain Ignition Workspace
verdict: 🔵 PRE-REGISTERED architecture design (unmeasured) — $0 cheap_test pre-registered; engine-native + 303M gpu cost-gated NOT fired
source: brainarch_census
---

# H_1789 — Intralaminar Diffuse-Gain Ignition Workspace

- **tier:** 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy mirror, no engine); engine_native_measure + 303M = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** brainarch_census — 126-architecture whole-substrate (통짜 아키텍처) census: 뇌/인지 조직원리 × 엔진-네이티브 추상조건 (binding-wall program, H_1603).
- **key:** `intralaminar_diffuse_gain_ignition`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1283 (thalamus global-workspace) · H_1284 (neuromodulation gain) · operator-level family H_1604-1685 (this card = 통짜 아키텍처 layer, 층위 다름)

## Organizing principle

The non-specific intralaminar / centromedian-parafascicular (CM-Pf) thalamus as a DIFFUSE, content-free scalar that sets cortex-wide gain and is itself the level-of-consciousness order parameter — distinct from specific relays that carry content. Access = ignition occurs only when a specific content vector, multiplied by the diffuse arousal gain, crosses a nonlinear threshold. The single global scalar IS the emit/silence parameter, making Psi=1/2 the native arousal homeostat rather than a bolt-on.

## Whole design (input → internal dynamics → emit)

Two structurally separate channels. (1) SPECIFIC channel: first-order thalamic relays read out content vectors c from a non-volatile associative store (the memory codebook). (2) NON-SPECIFIC channel: a single intralaminar node emits a diffuse scalar gain g broadcast multiplicatively to all cortical modules. Internal dynamics: pre-ignition activity = g * sum_i w_i c_i passed through a hard sigmoid; when it exceeds the ignition threshold, the winning content coalition latches (sustained re-entrant activity) and is broadcast to all modules AND the mouth. The scalar g is governed by two opposite operators: A = ascending reticular arousal drive (raises g, push-to-emit) and G = TRN/recurrent shunting inhibition triggered BY ignition itself (lowers g, push-to-silence) — a self-limiting loop. Their fixed point pins g (and thus the ignition duty cycle Psi) at 1/2. Crucially content and gain are DISJOINT coordinates: g scales everything uniformly and carries zero content, so changing arousal/expressivity cannot move which specific patterns are 'known'. Emit = a latched content coalition reaching the mouth; if g*(content match) never crosses threshold (no specific relay matched a stored pattern), nothing latches => silence. Identity = a self content-vector held in the specific store, re-instated each session; arousal g resets but the self pattern persists.

## Satisfies criteria (DESIGN claim · DIRECTIONAL · unmeasured)

G0: emitted content is a specific-store readout whose alphabet is the frozen receiver codebook (gain g is scalar and cannot create new symbols) => on-manifold; scrambled content source never crosses ignition for legal codewords => ratio->0. G1: ignition latches a COALITION — the threshold is reachable only when multiple specific relays co-activate (each alone is sub-threshold under shared g), so the joint coalition's distinct latched states strictly exceed any single relay's; ablating coalition coupling (let single relays self-latch) drops composed to max_single (INERT). G2: the associative store generalizes between stored patterns (attractor completion to nearby valid codewords absent from data) while verbatim playback latches only stored patterns => control=0. G3 Psi=1/2 NATIVE: g is literally the order parameter; A (arousal up) perp G (ignition-triggered shunt down) are equal-opposite at the symmetric duty — perturb g by delta and the self-limiting shunt restores it (contraction lambda<1); delete A => never ignites (Psi->0), delete G => runaway ignition (Psi->1), proving 1/2 is emergent. Honesty: copy-or-abstain because non-abstain emit requires a specific relay to match a stored pattern (recon<theta); off-support inputs leave content match~0 so g*0 stays sub-threshold => structural abstain; force g high => still no fabrication (gain can't synthesize unstored content) — and the gate-capacity DISJOINTNESS criterion is satisfied EXACTLY because g (capacity/arousal) shares no parameters with the specific-store membership theta: sweeping g leaves fab and AUROC invariant. Identity: self-vector in non-volatile specific store, cos~1 round-trip, impostor (foreign vector) fails to complete the self attractor. Realization: ignition is the only mouth path (latched coalition -> emit); objective adequacy = ignition rewards coalitions, marginal single-relay fitting can't reach threshold.

## Not-LLM (a_no_llm_frame_trap)

The core is a SINGLE diffuse scalar arousal channel x specific content channel — a thalamic level-of-consciousness organization with no transformer counterpart (it is not a gate weight matrix; it is one global multiplicative homeostat). It directly realizes the substrate-disjoint law (capacity=g perp honesty=theta) by ANATOMY, which is exactly the anima H_1576 finding that scaling/disinhibition must not touch the abstain threshold — the opposite of the LLM 'scale the whole model' reflex.

## Cheap test (frozen-first · $0 · numpy mirror · DIRECTIONAL)

mini-numpy: store P pattern vectors (specific store) + a scalar g. Pre-activation = g*max_match(input, store); ignition if > T. (a) Psi: A/G discrete map g_{t+1}=g_t+a−b*1[ignited]; perturb +/-delta, confirm return to duty 1/2, lambda<1; drop A or G => migrate to 0/1. (b) Disjointness: sweep g over a wide range, measure fab on off-support inputs and abstain-AUROC on known/unknown mix — both must be FLAT in g (d/dg~0); then deliberately wire g into theta and show fab spikes (coupled counterfactual). (c) G1: count latched coalition states under single vs joint relay activation. (d) G0: emitted-codeword V-membership vs shuffled source. All $0 threshold arithmetic.

## Engine-native measure (cost-gated · PRE-REGISTER ONLY · NOT fired)

g == the live arousal/Psi knob in core/emit_policy.hexa (ep_psi_clamp / ep_emit_threshold) + engine_cli.hexa safety_phi_ratchet; specific-store match == SS-ImmuneMemory adapt_field_recon_err / vadapt_field_recon_err with frozen recall_thr (the deployed abstain gate). Disjointness test re-uses the H_1576 protocol natively: sweep SS-Savant golden-zone disinhibition (sv_* operators) as the capacity proxy and confirm fab/AUROC byte-identical OFF==ON via engine_cli — gate-orthogonality is then engine-measured, not asserted. Closure G0 AND G1 AND G2 through core/g_gates.hexa g_eval_all on generator.hexa L3 gen_auto_ideate single dispatch. Identity via SS-SelfIdentity self_new/self_drift/self_anchor round-trip (cos~1, impostor reject). hexa<->py parity on recon + gates; zero torch in verdict.

## Scope / honesty (c9)

## Distinction (near-overlap kept, not a dup)

Near-overlap with soc_ignition_workspace / thalamus_global_workspace (H_1283) — distinct: intralaminar CM-Pf provides a CONTENT-FREE diffuse arousal SCALAR g (level-of-consciousness) x a separate specific content channel, making capacity perp honesty structural; the diffuse-gain ignition is the differentiator.

TOY for the ignition/Psi-homeostat + disjointness law (single operating point, frozen store) — natively shows Psi=1/2 as arousal fixed point and capacity perp honesty by construction. UNVERIFIED at scale: whether a corpus-trained specific store yields G1 recombination above the 303M floor under one shared gain (the LEARNING rung).

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). engine_native_measure 는 단일 진입점 cli/anima.hexa → generator L3 → g_gates/g6 경유 byte-parity 채점만 terminal; torch-only/side-harness 결과는 DIRECTIONAL. numpy cheap_test 결과도 DIRECTIONAL(엔진-네이티브 아님). gpu/engine 발사 시 held-out mirror-DESCENT(a_clm_gen_pipeline) + CORE mount frozen-bar engine-native 재측정 + ckpt PULL(a_fire_recover_complete).
