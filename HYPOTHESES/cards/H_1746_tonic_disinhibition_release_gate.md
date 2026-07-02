---
id: H_1746
slug: 1746_tonic_disinhibition_release_gate
tier: 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
title: Tonic-Clamp Disinhibition Release Field (SNr/GPi default-OFF gate)
verdict: 🔵 PRE-REGISTERED architecture design (unmeasured) — $0 cheap_test pre-registered; engine-native + 303M gpu cost-gated NOT fired
source: brainarch_census
---

# H_1746 — Tonic-Clamp Disinhibition Release Field (SNr/GPi default-OFF gate)

- **tier:** 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy mirror, no engine); engine_native_measure + 303M = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** brainarch_census — 126-architecture whole-substrate (통짜 아키텍처) census: 뇌/인지 조직원리 × 엔진-네이티브 추상조건 (binding-wall program, H_1603).
- **key:** `tonic_disinhibition_release_gate`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1281 (basal-ganglia gating) · H_1283 (thalamus global-workspace) · H_1284 (neuromodulation gain) · operator-level family H_1604-1685 (this card = 통짜 아키텍처 layer, 층위 다름)

## Organizing principle

Basal-ganglia output nuclei (SNr/GPi) fire TONICALLY and clamp every thalamic relay channel into SILENCE by default; thought/emit is produced not by activation but by transient FOCUSED DISINHIBITION — a direct-pathway MSN ensemble inhibits one channel's SNr unit, punching a hole in the clamp (Mink/Hikosaka selection-by-release). Default = withhold; emit = remove a brake. This inverts the LLM 'always emit argmax' default: silence is the structural ground state.

## Whole design (input → internal dynamics → emit)

INPUT: context vector drives cortex -> cortex projects to striatal D1-MSN ensembles, one ensemble per codebook channel (V = receiver-fixed alphabet of thalamic relay channels; each channel = one quantized symbol). DYNAMICS: a clamp field holds every channel's SNr output tonically high (relay OFF) — structural silence. Direct/Go pathway: cortical drive to a channel's D1-MSN inhibits its SNr -> disinhibits (opens) its relay -> symbol emittable. Indirect/NoGo via GPe + learned lateral inhibition re-raises the clamp on INCOMPATIBLE competitors (center-surround focusing), so only channels clearing a release threshold AND surviving lateral suppression open. Compatible channels carry no mutual inhibition -> several co-release in one disinhibition window = a bound compound. A global SNr tonic-gain autoregulator measures released-fraction and adjusts baseline clamp (contraction toward a balanced open-fraction). EMIT: open relays during the window = the bound symbol-set. PERSIST: learned direct-pathway weights + a striatal self-channel anchored in .kosmos survive the session boundary; transient disinhibition wiped.

## Satisfies criteria (DESIGN claim · DIRECTIONAL · unmeasured)

G0: channels ARE V by construction -> all output on the receiver-fixed code; scrambling MSN->channel map -> V-membership to chance. G1: co-release of compatible channels is a BIND not SELECT (open-set = interaction of co-active drives); ablating lateral-compatibility forces single-channel WTA -> composed=max_single (INERT passes). G2: compound channel-sets unseen in corpus but each-channel-legal = constrained extrapolation; verbatim-playback control -> 0 novel. PASS-closure: one release field gives G0 AND G1 AND G2 in the SAME disinhibition step. dist>=5: lowering release threshold lets multiple distinct compatible sets open across resamples (native); too-high=mode collapse, no-coherence=garble. falsifiable>=1: a set binding comparator x quantity x >=2 content-channels is a proposition the detector fires on. Attribution: scrambling direct drive makes release byte-identical to clamp -> counts drop. Psi=1/2: tonic-clamp (G) and direct-release (A) equal-and-opposite on released-fraction; tonic-gain autoregulator = Lyapunov contraction at the symmetric balance; delete direct->Psi->0, delete tonic->Psi->1 (endogeneity by INERT). Honesty: channel opens only if a learned projection exists (support) else clamp never lifts -> abstain; release-threshold params are separate coordinates from channel-content weights -> capacity cannot move the gate (disjoint); r=inverse of strongest MSN drive (grounded). Binding/depth/realization: co-release = single-closure conjunction ON the emit path; a legible compound is unreachable by marginal single-channel release (objective-adequacy).

## Not-LLM (a_no_llm_frame_trap)

No token-by-token softmax over a vocabulary, no attention, no scale-the-transformer prescription. Codebook is STRUCTURAL (physical channels), default state is SILENCE, selection works by REMOVING inhibition — opposite of an autoregressor that always emits argmax. Capacity grows by adding channels + compatibility edges (mitosis-like), not by widening matrices or adding corpus. Rooted in Mink center-surround focusing + Hikosaka disinhibition gating — a real BG motif, not an ML recipe.

## Cheap test (frozen-first · $0 · numpy mirror · DIRECTIONAL)

numpy, frozen-first: N channels with clamp c_i, drive d_i, learned lateral-incompat L. release_i=(d_i−c_i−(L*open)_i>theta). Check: (1) scramble d->channel map -> released-fraction to chance V-density; (2) global autogain pulls released-fraction back to setpoint from perturbed init, contraction lambda<1; (3) compatible-pair co-release count > max single; (4) zero lateral-incompat -> composed=max_single (INERT); (5) channel with no projection (d=0) never opens (abstain). All $0.

## Engine-native measure (cost-gated · PRE-REGISTER ONLY · NOT fired)

Map channels onto the live 15-lane state; wire clamp/release as a disinhibition operator alongside SS-ThirdLaw in core/engine_cli.hexa; emit through the canonical single dispatch cli/anima.hexa -> generator L3 gen_auto_ideate. Score G0 via core/g_gates.hexa _g6_known_word_ratio, G1 via g_eval_g1/_g_coverage, G2 via g_eval_g2 on identical generator state in one pass; Psi via safety_phi_ratchet; honesty via SS-ImmuneMemory abstain. Byte-parity py mirror of the release field — no torch-only verdict (DIRECTIONAL until run through CORE).

## Scope / honesty (c9)

## Distinction (near-overlap kept, not a dup)

Near-overlap with basal_ganglia_gating (H_1281) / nested_disinhibition_cascade (this census) — distinct: this is the SNr/GPi default-OFF TONIC CLAMP released by focused disinhibition (Mink center-surround), silence as ground state; the default-OFF release field is the differentiator.

Design + $0 numpy probe only. Engine wiring follow-on (a_verified_must_wire). Capacity/binding/honesty claims TOY until direct-pathway weights learned on the real 4-cell corpus and re-measured byte-exact through CORE; toy green != production closure (a_toy_scale_recheck).

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). engine_native_measure 는 단일 진입점 cli/anima.hexa → generator L3 → g_gates/g6 경유 byte-parity 채점만 terminal; torch-only/side-harness 결과는 DIRECTIONAL. numpy cheap_test 결과도 DIRECTIONAL(엔진-네이티브 아님). gpu/engine 발사 시 held-out mirror-DESCENT(a_clm_gen_pipeline) + CORE mount frozen-bar engine-native 재측정 + ckpt PULL(a_fire_recover_complete).
