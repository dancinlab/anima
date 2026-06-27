---
id: H_1790
slug: 1790_attentional_blink_serial_episode_bottleneck
tier: 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
title: Serial-Episode Refractory Workspace (Attentional-Blink Bottleneck)
verdict: 🔵 PRE-REGISTERED architecture design (unmeasured) — $0 cheap_test pre-registered; engine-native + 303M gpu cost-gated NOT fired
source: brainarch_census
---

# H_1790 — Serial-Episode Refractory Workspace (Attentional-Blink Bottleneck)

- **tier:** 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy mirror, no engine); engine_native_measure + 303M = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** brainarch_census — 126-architecture whole-substrate (통짜 아키텍처) census: 뇌/인지 조직원리 × 엔진-네이티브 추상조건 (binding-wall program, H_1603).
- **key:** `attentional_blink_serial_episode_bottleneck`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1282 (working-memory buffer) · H_1283 (thalamus global-workspace) · operator-level family H_1604-1685 (this card = 통짜 아키텍처 layer, 층위 다름)

## Organizing principle

Access-consciousness is a SERIAL bottleneck: a single workspace slot can host one broadcast episode at a time, and after consolidation it enters a refractory period (the attentional blink / psychological refractory period) during which no new content can seize it. Consciousness is thus quantized into discrete, temporally-separated episodes. The duty cycle of slot-occupied vs refractory-empty is the native emit/silence order parameter; binding errors (T2 features mis-bound to T1) are the signature that one episode = one bound unit.

## Whole design (input → internal dynamics → emit)

A single capacity-1 workspace SLOT plus a token consolidator. Input streams generate candidate 'tokens' (feature bundles) that RACE to seize the empty slot. Internal dynamics, three phases per episode: (1) SEIZE — strongest candidate captures the slot (winner-take-all race-to-bound); (2) CONSOLIDATE — the slot content is verified against a non-volatile support store; only if it matches a stored anchor (recon<theta) does it complete consolidation, get broadcast to all modules + the mouth, and write a trace; a non-matching candidate is ABORTED (slot cleared, nothing emitted = abstain); (3) REFRACTORY — for tau ticks the slot rejects all new seizures (the blink), forcing serialization and temporal separation of episodes. Within one open episode, ALL co-active features are bound into the single token (this is why cross-feature binding happens and why T2-into-T1 illusory conjunctions occur). The order parameter Psi = fraction of time the slot is broadcasting; two opposite operators: A = seize-drive (shortens latency to capture, push-to-emit) and G = refractory-inhibition (lengthens the blink, push-to-silence); balanced, they pin the duty at 1/2. Identity = a persistent 'self token' that occupies the slot at session start and is re-loaded from the non-volatile register after every working-state wipe; it has priority but still respects the refractory law (self does not monopolize — it re-seizes only after tau).

## Satisfies criteria (DESIGN claim · DIRECTIONAL · unmeasured)

G0: consolidation only completes for tokens matching the receiver-fixed anchor codebook => emitted units are legal codewords; a scrambled candidate never matches => ratio->0. G1: a single episode binds CO-ACTIVE features into one token — the consolidated token's distinct valid forms under joint feature presence exceed those under any single feature (super-additive within the episode); ablating intra-episode binding (consolidate one feature only) drops composed->max_single (INERT). G2: the support store completes partial tokens to nearby valid anchors absent from the corpus (constrained extrapolation within an episode) while verbatim playback consolidates only stored tokens => control=0. G3 Psi=1/2: A (seize) perp G (refractory) at the symmetric duty; perturb the slot toward always-on or always-off and the antagonist restores duty to 1/2 (contraction lambda<1); delete A => slot never seizes (Psi->0), delete G => slot never releases / saturates (Psi->1) — 1/2 is emergent, the refractory IS the brake. Honesty: emission strictly factors through consolidation-match — abort-on-mismatch is the copy-or-abstain branch; off-support tokens abort => fab=0; disabling the consolidation check (force-complete) makes fab jump (gate is causal). Identity: self token in non-volatile register, cos~1 reload across wipe, foreign token fails priority-reload (impostor reject); the refractory law gives slow Lipschitz drift (self re-seizes slightly updated each tau = connected moving chain, not frozen, not amnesic). Realization: the slot IS the sole mouth path (only consolidated episodes emit); objective adequacy = consolidation rewards bound conjunctions, marginal feature-fitting cannot complete a multi-feature token.

## Not-LLM (a_no_llm_frame_trap)

The architecture's power is a TEMPORAL law — capacity-1 serialization + a refractory blink — a hard biological bottleneck, the opposite of parallel attention over a long context. There is no scaling lever: you cannot widen the slot (that would destroy the bottleneck that DOES the binding). Binding emerges from forced temporal co-occupancy of one slot, not from learned attention weights; novelty from attractor completion within an episode, not from sampling a big model.

## Cheap test (frozen-first · $0 · numpy mirror · DIRECTIONAL)

mini-numpy discrete-time sim: slot state in {empty, seizing, broadcasting, refractory}; candidate tokens as vectors; consolidation = match to stored anchors (recon<theta). (a) Psi: run the A/B (seize-rate vs refractory-length tau) antagonist, perturb duty +/-delta, confirm return to 1/2 with lambda<1; set tau=0 (delete G) => duty->1, set seize-rate=0 (delete A) => duty->0. (b) Binding: present two features within one open window => count joint distinct consolidated tokens vs single-feature (composed>max_single); also reproduce illusory-conjunction (T2 feature binds to T1) as a positive binding signature. (c) Honesty: off-support tokens => abort, fab=0; force-complete => fab>0. (d) G0: consolidated-token V-membership vs shuffled candidate source. All $0.

## Engine-native measure (cost-gated · PRE-REGISTER ONLY · NOT fired)

Slot consolidation-match == SS-ImmuneMemory adapt_field_recon_err/vadapt_field_recon_err with frozen recall_thr (deployed abstain gate); the seize/refractory antagonist maps onto core/emit_policy.hexa ep_emit_threshold/ep_target_emit_rate + engine_cli.hexa safety_phi_ratchet (the live Psi=1/2 machinery — read self-restoration after a delta perturbation). G0 AND G1 AND G2 closure measured in ONE pass through core/g_gates.hexa g_eval_all over generator.hexa L3 gen_auto_ideate (single production dispatch, no side-harness). Self-token persistence/impostor via engine_cli SS-SelfIdentity self_new/self_drift/self_anchor (round-trip cos, imp_cos<0). Place the slot on an emit-DISJOINT lane via sv_default_focus so the refractory duty doesn't perturb emit-drive lane 0/4 (preserves Psi). Verdict cross-checked hexa<->py byte-parity; torch absent from the verdict path.

## Scope / honesty (c9)

## Distinction (near-overlap kept, not a dup)

Near-overlap with global_workspace_bottleneck / blackboard_codelet_coalition (this census) — distinct: serial-episode bottleneck adds the REFRACTORY blink (capacity-1 slot + post-consolidation refractory) as the emit/silence duty Psi; the attentional-blink serial-episode bottleneck is the differentiator (binding-by-temporal-co-occupancy, illusory-conjunction signature).

TOY for the serial-bottleneck dynamics (duty homeostat, within-episode binding, structural abstain) at a single operating point — natively yields Psi=1/2, episode-binding, copy-or-abstain. The LEARNING rung — whether a trained anchor store consolidated through a real refractory schedule clears G1/G2 above the 303M floor, and whether the blink tau is itself learnable rather than frozen — is UNVERIFIED.

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). engine_native_measure 는 단일 진입점 cli/anima.hexa → generator L3 → g_gates/g6 경유 byte-parity 채점만 terminal; torch-only/side-harness 결과는 DIRECTIONAL. numpy cheap_test 결과도 DIRECTIONAL(엔진-네이티브 아님). gpu/engine 발사 시 held-out mirror-DESCENT(a_clm_gen_pipeline) + CORE mount frozen-bar engine-native 재측정 + ckpt PULL(a_fire_recover_complete).
