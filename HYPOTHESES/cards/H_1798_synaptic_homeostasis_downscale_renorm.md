---
id: H_1798
slug: 1798_synaptic_homeostasis_downscale_renorm
tier: 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
title: Sleep-Downscaling Renormalizer — Consolidation by Competitive Removal
verdict: 🔵 PRE-REGISTERED architecture design (unmeasured) — $0 cheap_test pre-registered; engine-native + 303M gpu cost-gated NOT fired
source: brainarch_census
---

# H_1798 — Sleep-Downscaling Renormalizer — Consolidation by Competitive Removal

- **tier:** 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy mirror, no engine); engine_native_measure + 303M = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** brainarch_census — 126-architecture whole-substrate (통짜 아키텍처) census: 뇌/인지 조직원리 × 엔진-네이티브 추상조건 (binding-wall program, H_1603).
- **key:** `synaptic_homeostasis_downscale_renorm`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1281 (basal-ganglia gating) · H_1284 (neuromodulation gain) · operator-level family H_1604-1685 (this card = 통짜 아키텍처 layer, 층위 다름)

## Organizing principle

Synaptic Homeostasis Hypothesis (Tononi & Cirelli): wake nets net synaptic POTENTIATION; sleep applies a global MULTIPLICATIVE downscale plus sub-threshold pruning. This renormalizes total synaptic weight (energy homeostasis) and improves SNR — weak one-off (noise/episodic) synapses fall below survival theta and die, while synapses re-potentiated across many wake epochs (recurring regularities = semantic gist) survive. Consolidation is therefore NOT replay; it is competition during renormalization. The fast and slow systems are the SAME weights at different points on the survival gradient (weak-recent = episodic, strong-survivor = semantic).

## Whole design (input → internal dynamics → emit)

Wake phase: episodic input drives purely ADDITIVE, saturating potentiation onto a shared weight tensor W (no second network). SNR degrades as both signal and noise accumulate; total synaptic load rises = 'sleep pressure' (interoceptive setpoint). Sleep phase (triggered when load crosses the homeostatic setpoint): W <- alpha*W (alpha<1 global multiplicative downscale) then prune {|w|<theta_survive -> 0}. Over repeated wake-potentiate/sleep-downscale cycles, only synapses re-potentiated by RECURRING structure clear theta each cycle; one-off traces decay to zero. The surviving subnetwork is the slow semantic store; the volatile above-noise top layer is the episodic store. Emit: read W; abstain when query is not reconstructable from the SURVIVOR subnetwork (recon residual > theta). Psi: wake = externalize/emit (W is read out), sleep = withhold/silence (W is renormalized, no emit). An emit-drive (low load, settled) perp a withhold-drive (high load, sleep pressure); emitting settles load, encoding accumulates it -> antagonist fixed point at a balanced wake/sleep duty.

## Satisfies criteria (DESIGN claim · DIRECTIONAL · unmeasured)

G0: survivors define the legible code V (strong consolidated symbol associations); scramble survivors -> chance V-mass. G1: conjunction-specific synapses survive only when the conjunction RECURS (re-potentiated by co-occurrence), so the surviving reachable set is super-additive vs marginal-only survivors; ablate downscaling -> noise fills, interference, composed=max_single. G2: downscaling extracts the gist (regularity), not instances -> survivor manifold interpolates valid corpus-absent points; no-downscale (instance memory) playback = 0 novel. dist>=5: multiple surviving basins -> distinct-coherent spread. honesty cluster: support-membership = reconstructable-from-survivors residual -> AUROC; theta_survive is frozen-first and disjoint from raw synapse COUNT (capacity) -> gate-capacity disjointness; content-ablation of stored support degrades survivor reconstruction (faithfulness), shuffle surrogate collapses AUROC. Psi=1/2: wake/sleep duty homeostat, self-restoring, one-drive ablation -> all-wake (babble) or all-sleep (mute) boundary (endogeneity). Realization invariant: emit reads W on-path; ablating downscale (mechanism-OFF) removes both the SNR gain and the survivor-gate (INERT test).

## Not-LLM (a_no_llm_frame_trap)

Consolidation by SUBTRACTION — global multiplicative downscaling + competitive pruning sculpts the slow store by removing synapses, the exact opposite of the scale-up/add-parameters/add-corpus prescription. Brain-rooted (SHY). No gradient, no attention, no replay; the regularity is revealed by surviving renormalization, not by fitting more data.

## Cheap test (frozen-first · $0 · numpy mirror · DIRECTIONAL)

numpy, frozen-first. Shared W; wake-potentiate with interleaved recurring-signal + one-off-noise streams; apply N downscale+prune cycles. Pre-registered bars: (1) SNR = (signal-synapse mass / noise-synapse mass) strictly increases across cycles; (2) recurring conjunctions survive while one-offs die (survival-rate gap >= bar); (3) ablate downscale -> SNR flat/degrades (INERT); (4) survivor-reconstruction AUROC(known/unknown) ~ 1, shuffle -> 0.5.

## Engine-native measure (cost-gated · PRE-REGISTER ONLY · NOT fired)

Implement downscale-renorm as an engine consolidation op over the live weight store; route survivors to a mouth via generator L3; compute support residual on the survivor subnetwork through SS-ImmuneMemory; run G0/G1/G2 + dist via single entry cli/anima.hexa -- eval. byte-parity py mirror (math.log CE) cross-checks; no torch-only verdict.

## Scope / honesty (c9)

## Distinction (near-overlap kept, not a dup)

Near-overlap with cls / sleep-consolidation cards — distinct: SHY consolidates by SUBTRACTION (global multiplicative downscale + competitive pruning, no replay) — survivors = recurring gist; the sleep-downscaling renormalizer is the differentiator (consolidation by removal).

Design-only. numpy is decisive for SNR-gain, competitive survival, prune, and support-AUROC. HONEST RISK to flag: G1 objective-adequacy — marginals also recur, so downscaling could consolidate marginal structure as readily as conjunctions; the binding ablation (does removing co-occurrence-specific survivors drop composed to max_single?) is the at-risk decisive gate and must be the frozen falsifier. Strong native wins: honesty/membership and consolidation-without-replay; G1 is the wall to test first.

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). engine_native_measure 는 단일 진입점 cli/anima.hexa → generator L3 → g_gates/g6 경유 byte-parity 채점만 terminal; torch-only/side-harness 결과는 DIRECTIONAL. numpy cheap_test 결과도 DIRECTIONAL(엔진-네이티브 아님). gpu/engine 발사 시 held-out mirror-DESCENT(a_clm_gen_pipeline) + CORE mount frozen-bar engine-native 재측정 + ckpt PULL(a_fire_recover_complete).
