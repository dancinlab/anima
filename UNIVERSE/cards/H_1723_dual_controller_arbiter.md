---
id: H_1723
slug: 1723_dual_controller_arbiter
tier: 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
title: Dorsomedial-perp-Dorsolateral Dual-Controller Arbiter (model-based perp model-free)
verdict: 🔵 PRE-REGISTERED architecture design (unmeasured) — $0 cheap_test pre-registered; engine-native + 303M gpu cost-gated NOT fired
source: brainarch_census
---

# H_1723 — Dorsomedial-perp-Dorsolateral Dual-Controller Arbiter (model-based perp model-free)

- **tier:** 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy mirror, no engine); engine_native_measure + 303M = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** brainarch_census — 126-architecture whole-substrate (통짜 아키텍처) census: 뇌/인지 조직원리 × 엔진-네이티브 추상조건 (binding-wall program, H_1603).
- **key:** `dual_controller_arbiter`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1281 (basal-ganglia gating) · H_1282 (working-memory buffer) · H_1283 (thalamus global-workspace) · H_1284 (neuromodulation gain) · operator-level family H_1604-1685 (this card = 통짜 아키텍처 layer, 층위 다름)

## Organizing principle

Two striatal controllers run in parallel — dorsolateral (habitual, model-FREE cached values) and dorsomedial (goal-directed, model-BASED forward simulation) — and a reliability-weighted ARBITER (infralimbic/uncertainty signal) decides which drives each emission. The core loop is META-CONTROL: arbitration over controllers, the Daw/Dolan/Glascher dual-system. Orthogonal to pbwm gating (which is slot read/write) — here the principle is uncertainty-weighted competition between two whole controllers.

## Whole design (input → internal dynamics → emit)

Input cortical state fans to BOTH controllers. MF: a fast cached state->action habit table (retrieval-like). MB: a forward world-model + tree-rollout that simulates multi-step consequences (slow, recomputed, compositional). The arbiter computes each controller's reliability — MF reliability = inverse recent prediction-error; MB reliability = inverse rollout-variance — and forms arbitration weight w=softmax(reliabilities). The emission distribution is w*(MB) + (1−w)*(MF) over V union {abstain}, resolved by thalamic disinhibition to a winner. When NEITHER controller is reliable the arbiter defaults to abstain. Learning: MF by RPE, MB world-model by self-supervised next-state prediction. The two are antagonists in tempo — MF=impulsive emit-now, MB=deliberative (can elect to withhold).

## Satisfies criteria (DESIGN claim · DIRECTIONAL · unmeasured)

Psi=1/2 (G3/endogeneity): A=MF impulsive-emit drive, G=MB deliberative-withhold drive; the arbiter weight w sits at a reliability-matching fixed point w*=1/2 that is attracting via the running-error low-pass (a contraction): MF dominance => habits misfire => MF prediction-error rises => w shifts to MB => MB withholds more => Psi down, and symmetrically up. Ablate the arbiter => one controller dominates => Psi->boundary (emergent, not clamped). HONESTY (this architecture's STRONGEST native fit): abstain fires when r=min(MF-error^-1, MB-variance^-1) is low for BOTH (out of support for both) => arbiter selects abstain; copy-or-abstain is structural because MF can only emit CACHED (copy) content and MB only what its grounded world-model supports — synthesis neither supports => abstain; the reliability gate is disjoint from each controller's capacity (d-fab/d-capacity=0); content-ablating the MF cache for known states drops MF reliability and reroutes to MB/abstain (faithful). BINDING + COMPOSITIONAL DEPTH + REALIZATION INVARIANT: the MB tree-rollout is the non-separable conjunction operator — f(state,action) is non-separable and rollouts generalize to novel state-action combos never co-presented (Fodor-Pylyshyn systematicity); it is ON the emit path (arbiter reads it) and its objective (multi-step next-state consistency) is unreachable by marginal-fit, so PATH-ablating the rollout drops composed_distinct to MF's max_single = native G1. SELF-PERSISTENCE + self-specific margin: the MF habit cache is the non-volatile addressable store; identity = the cache signature, committed pre-boundary, re-read post-boundary, agent-history-specific (foreign cache => low cos), ablate store => continuity->chance.

## Not-LLM (a_no_llm_frame_trap)

Dual-process model-based/model-free RL with explicit world-model rollout + habit cache + uncertainty arbitration — no attention, no CE-corpus fit. Composition arises by SIMULATION (forward model), not memorized sequence statistics, directly answering the clm303 lossF~0-yet-recombine-fail pattern: the MB controller can compose novel conjunctions a flat next-token model cannot. Capacity = arbitration quality + rollout depth, not scale. a_no_llm_frame_trap: lens is dual-system control, not a bigger sequence model.

## Cheap test (frozen-first · $0 · numpy mirror · DIRECTIONAL)

numpy two-step Markov task (the canonical MB/MF dissociation). Frozen-first ($0): (a) reward-revaluation probe — MB adapts, MF does not => arbiter weight shifts (proves genuine dual control); (b) both-uncertain state => abstain rate high, AUROC vs known~1, shuffle surrogate => 0.5; (c) MB-rollout ablation => recombination composed_distinct->max_single; (d) cache round-trip cos~1, foreign cache cos~0, ablate cache => cross-boundary cos->chance.

## Engine-native measure (cost-gated · PRE-REGISTER ONLY · NOT fired)

Map MB rollout onto core/engine_cli.hexa forward-model lane (cerebellum precedent H_1280), MF cache onto SS-ImmuneMemory recall, arbiter onto SS-ThirdLaw. Measure G1 via live core/g_gates.hexa g_eval_g1 through cli/anima.hexa single entry with MB on/off ablation; abstain AUROC + fab=0 via SS-ImmuneMemory frozen bars; self-chain cos via SS-SelfIdentity .kosmos round-trip. py mirror with math.log for value/CE cross-check — no torch-only verdict.

## Scope / honesty (c9)

## Distinction (near-overlap kept, not a dup)

Near-overlap with basal_ganglia_gating (H_1281) and pbwm_gated_slot_register (this census) — distinct: dual-controller arbiter is uncertainty-weighted META-CONTROL between two WHOLE controllers (MB forward-sim vs MF cache), not slot read/write; the model-based-vs-model-free arbitration is the differentiator.

two-step TOY verdict only; MB rollout depth and a literal chat-corpus world-model at 303M scale UNVERIFIED (a_toy_scale_recheck). The honesty/abstain and self-chain bars are engine-checkable today; whether MB simulation lifts held-out novel-combination above the marginal-fit floor at scale is the in-flight question.

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). engine_native_measure 는 단일 진입점 cli/anima.hexa → generator L3 → g_gates/g6 경유 byte-parity 채점만 terminal; torch-only/side-harness 결과는 DIRECTIONAL. numpy cheap_test 결과도 DIRECTIONAL(엔진-네이티브 아님). gpu/engine 발사 시 held-out mirror-DESCENT(a_clm_gen_pipeline) + CORE mount frozen-bar engine-native 재측정 + ckpt PULL(a_fire_recover_complete).
