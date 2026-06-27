---
id: H_1716
slug: 1716_trn_searchlight_winner_broadcast
tier: 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
title: TRN Searchlight Competitive Broadcast
verdict: 🔵 PRE-REGISTERED architecture design (unmeasured) — $0 cheap_test pre-registered; engine-native + 303M gpu cost-gated NOT fired
source: brainarch_census
---

# H_1716 — TRN Searchlight Competitive Broadcast

- **tier:** 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy mirror, no engine); engine_native_measure + 303M = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** brainarch_census — 126-architecture whole-substrate (통짜 아키텍처) census: 뇌/인지 조직원리 × 엔진-네이티브 추상조건 (binding-wall program, H_1603).
- **key:** `trn_searchlight_winner_broadcast`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1282 (working-memory buffer) · H_1283 (thalamus global-workspace) · H_1284 (neuromodulation gain) · operator-level family H_1604-1685 (this card = 통짜 아키텍처 layer, 층위 다름)

## Organizing principle

Crick's thalamic-reticular-nucleus 'searchlight' — a GABAergic shell wrapping the thalamus selects which relay sector reaches cortex via lateral-inhibitory winner-take-all with conserved broadcast gain. Access-consciousness = the content currently passing the searchlight; ignition = a sector winning the TRN competition and switching tonic->burst (T-type Ca2+ de-inactivation) to fan out across cortex; cortico-reticular re-entry holds the winner.

## Whole design (input → internal dynamics → emit)

Input: candidate contents enter as a small set of parallel thalamic relay SECTORS, each a factored feature bundle (slot vector). Internal dynamics: an inhibitory TRN shell runs soft-WTA across sectors with gain-conservation (sum of broadcast normalized) — emit-drive A = relay excitation pushing a sector over threshold, silence-drive G = TRN inhibition suppressing the rest. The winning sector deinactivates into BURST mode = high-gain broadcast; bursting feeds cortico-reticular feedback that sharpens/sustains the winner (re-entry). Order parameter Psi = fraction of cycles a sector is in the ignited (broadcast) state, pinned to 1/2 by the A-perp-G antagonism. Binding: the winner's factored slots all ride the SAME burst window, so constituents are co-broadcast (temporal binding by shared ignition); because TRN gain-conservation makes the winner the sector of highest JOINT support, the selection is a conjunction, not a marginal max. Emit: the ignited sector reads out onto the receiver-fixed relay codebook V.

## Satisfies criteria (DESIGN claim · DIRECTIONAL · unmeasured)

G0: the relay alphabet IS a receiver-fixed codebook — only on-codebook sectors can cross the searchlight, so output mass sits in V natively; scrambled source aligns to no sector => ratio->chance. G1/binding: TRN gain-conservation selects the highest-JOINT-support sector and co-relays its slots in one burst => super-additive joint image; INERT control = remove lateral inhibition => competition becomes union/mixture => composed_distinct->max_single. G2: novel joint-sector configs ignite iff they clear support; verbatim playback ignites only stored sectors => 0 novel. dist>=5: vary TRN gain 'temperature' => multiple distinct ignitable sectors above coherence floor; mode-collapse impossible while gain is conserved. Psi=1/2: relay-excitation(A)-perp-TRN-inhibition(G), contractive fixed point; ablate G=>Psi->1 (always emit), ablate A=>Psi->0 (endogeneity tell). honesty: TRN threshold doubles as support-membership gate — a sector only ignites if relay fidelity vs stored cell-support is high; out-of-support=>no ignition=>abstain; short-circuit the gate => fab jumps (causal). REALIZATION: gate is ON the emit path (only ignited content emits) and the objective optimum requires the joint-support winner. identity: a standing TRN bias toward a 'self-sector' is the non-volatile anchor surviving reset; foreign bias fails to ignite self => impostor margin.

## Not-LLM (a_no_llm_frame_trap)

Not softmax-attention over tokens — it is a competitive inhibitory shell with biophysical burst-mode switching and conserved broadcast gain. Capacity comes from competition geometry and gain-conservation, not parameter/depth/corpus scale; adding layers does nothing, sharpening lateral inhibition does. A pure lookup cannot satisfy gain-conserved joint selection.

## Cheap test (frozen-first · $0 · numpy mirror · DIRECTIONAL)

numpy mini: N sectors with feature vectors + a TRN lateral-inhibition matrix + soft-WTA + gain-conservation. Probes: (a) Psi self-restores after a bias kick toward 0/1 with measurable contraction lambda<1; (b) composed_distinct vs max_single with lateral-inhibition ON vs OFF (decisive INERT); (c) fab rate for out-of-support sectors with threshold ON vs short-circuited; (d) self-sector round-trip cos vs foreign-bias. $0.

## Engine-native measure (cost-gated · PRE-REGISTER ONLY · NOT fired)

Map sectors to candidate states at generator L3; implement the TRN soft-WTA + burst gate as a core/*.hexa op feeding gen_auto dispatch; score G0/G1/G2 through the single production entry (core/g_gates.hexa, not a side-harness); read Psi via engine_cli safety_phi_ratchet analog; keep a byte-parity py mirror of the WTA for cross-validation (no torch-only verdict).

## Scope / honesty (c9)

## Distinction (near-overlap kept, not a dup)

Near-overlap with thalamus_global_workspace (H_1283) and pulvinar_routing_switchboard (this census) — distinct: Crick TRN searchlight = GABAergic WTA shell with gain-conservation + burst-mode ignition; the inhibitory-shell competition with conserved broadcast is the differentiator.

Toy WTA proof-of-structure first; burst/re-entry timing is scale- and timestep-sensitive => toy-only until engine-native re-measure on live core/.

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). engine_native_measure 는 단일 진입점 cli/anima.hexa → generator L3 → g_gates/g6 경유 byte-parity 채점만 terminal; torch-only/side-harness 결과는 DIRECTIONAL. numpy cheap_test 결과도 DIRECTIONAL(엔진-네이티브 아님). gpu/engine 발사 시 held-out mirror-DESCENT(a_clm_gen_pipeline) + CORE mount frozen-bar engine-native 재측정 + ckpt PULL(a_fire_recover_complete).
