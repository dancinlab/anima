---
id: H_1701
slug: 1701_cls_replay_consolidation
tier: 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
title: Interleaved-Replay Complementary Learning Systems
verdict: 🔵 PRE-REGISTERED architecture design (unmeasured) — $0 cheap_test pre-registered; engine-native + 303M gpu cost-gated NOT fired
source: brainarch_census
---

# H_1701 — Interleaved-Replay Complementary Learning Systems

- **tier:** 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy mirror, no engine); engine_native_measure + 303M = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** brainarch_census — 126-architecture whole-substrate (통짜 아키텍처) census: 뇌/인지 조직원리 × 엔진-네이티브 추상조건 (binding-wall program, H_1603).
- **key:** `cls_replay_consolidation`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · operator-level family H_1604-1685 (this card = 통짜 아키텍처 layer, 층위 다름)

## Organizing principle

McClelland-McNaughton-O'Reilly CLS: two stores with complementary plasticity. Fast hippocampal store = sparse, pattern-separated, one-shot conjunctive codes (high learning rate). Slow neocortical store = dense overlapping distributed codes that extract statistical structure ONLY through offline interleaved replay (low learning rate). Consolidation = hippocampus replays distinct episodes INTERLEAVED into cortex during idle/sleep, which is structurally what avoids catastrophic interference AND is the source of composition.

## Whole design (input → internal dynamics → emit)

Input is dual-encoded: (a) a sparse k-WTA conjunctive code written one-shot to the fast store (an episodic trace, indexed), emit suppressed during write (silence); (b) a neocortical projection. During idle, a replay buffer INTERLEAVES distinct fast-store episodes with samples from the slow store and takes small gradient/Hebbian steps on the slow store — co-presenting distinct factors in replay is what forces the slow store's overlapping code to learn their interaction term. Emit = slow-store pattern completion from a partial cue -> readout onto the receiver-frozen codebook V. Novel outputs = completions that interpolate between consolidated episodes (manifold-filling). Order parameter Psi = balance of encode-drive (write+silence, dominant when pattern-separation novelty is high) vs retrieve-drive (complete+emit, dominant when familiarity is high); high novelty->more encoding->familiarity rises->retrieve-drive rises->emit->novelty consumed->returns to 1/2.

## Satisfies criteria (DESIGN claim · DIRECTIONAL · unmeasured)

G0: slow-store readout objective is reconstruction onto frozen V. G1: composition is native to interleaved replay (distinct episodes co-replayed -> super-additive joint completions); ablate interleaving (replay singly) -> composed_distinct->max_single (the structural INERT test). G2: completion interpolates corpus-absent valid points; verbatim playback of an episodic trace yields 0 novel by construction. Closure: one completion path. dist>=5: stochastic k-WTA + sparse coding -> many separable coherent attractors. falsifiable>=1: relational magnitude structure consolidated across episodes lets a completion assert an ordering. Psi=1/2: encode/retrieve antagonism IS the order parameter; delete one drive -> fixed point migrates to a boundary. Persistence: slow consolidated store = non-volatile identity (fast store wiped at episode boundary); drift = slow learning rate (Lipschitz-small/tick). Self-specific: consolidated statistics are agent-specific; foreign slow store doesn't collide. Endogeneity: Psi and continuity emerge from two-store coupling; ablate consolidation -> amnesia. Honesty support-membership: fast-store pattern-separation recon-distance = r (the hippocampal novelty signal); AUROC native. copy-or-abstain: completion below energy threshold + no index hit -> abstain. Gate-capacity disjoint: abstain gate = FAST store's separation metric; capacity = SLOW store completion — physically disjoint stores. Groundedness: r = distance to actual stored sparse codes (corrupt episode -> r shifts). BINDING: conjunctive code binds one episode's constituents into one sparse neighborhood (cause-selective). Compositional depth: interleaving forces conjunction representation; held-out combos reachable via distributed overlap (systematicity). Realization invariant: the conjunctive code is on the emit path because consolidation transfers it into the completion store that generates; objective (completion-reconstruction over interleaved replay) has its optimum unreachable by marginal fit.

## Not-LLM (a_no_llm_frame_trap)

No attention, no scale, no corpus-increase. The generative power comes from two associative stores with DIFFERENT plasticity rates plus offline interleaved replay dynamics — a consolidation mechanism. Scaling a transformer gives neither one-shot pattern-separated encoding nor interleaved-replay structure extraction. This is a memory-systems/plasticity organizing principle, orthogonal to feedforward depth.

## Cheap test (frozen-first · $0 · numpy mirror · DIRECTIONAL)

numpy mini: fast = sparse k-WTA one-shot Hebbian autoencoder; slow = small dense completion net trained by interleaved replay of fast traces. Present two factors as SEPARATE episodes, then test whether interleaved-replay-trained slow store completes a novel JOINT (composed_distinct>max_single) while a single-replay control collapses it to max_single; verify pattern-separation recon-distance separates known/unknown (AUROC); verify encode/retrieve order parameter returns to 1/2 under an emit/silence bias. All $0.

## Engine-native measure (cost-gated · PRE-REGISTER ONLY · NOT fired)

Map fast store->core/engine_cli.hexa SS-ImmuneMemory (recon_err is already the abstain gate), slow store->consolidated mouth via generator L3; score G0/G1/G2 through the single dispatch in core/g_gates.hexa on the consolidated state; Psi self-restore via safety_phi_ratchet; identity via SS-SelfIdentity .kosmos round-trip. Cross-check with a byte-parity numpy mirror using math.log CE (avoid the dt_ln engine-CE artifact, H_1579).

## Scope / honesty (c9)

## Distinction (near-overlap kept, not a dup)

Near-overlap with existing CLS cards (cls_ach_gate, replay_recombination, perturbed_replay_consolidation) — distinct: this is the canonical MMO CLS as a WHOLE substrate where INTERLEAVED replay is the structural source of G1 composition + the two stores give native gate-capacity disjointness; the interleaving-as-binder claim is the differentiator.

Full architecture; toy-scale cheap-test first. Load-bearing claim = interleaved-replay consolidation actually produces super-additive coherent joints (not just a mixture); scale-transfer unverified (a_toy_scale_recheck).

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). engine_native_measure 는 단일 진입점 cli/anima.hexa → generator L3 → g_gates/g6 경유 byte-parity 채점만 terminal; torch-only/side-harness 결과는 DIRECTIONAL. numpy cheap_test 결과도 DIRECTIONAL(엔진-네이티브 아님). gpu/engine 발사 시 held-out mirror-DESCENT(a_clm_gen_pipeline) + CORE mount frozen-bar engine-native 재측정 + ckpt PULL(a_fire_recover_complete).
