---
id: H_1750
slug: 1750_synaptic_tag_capture_consolidation
tier: 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
title: Tag-and-Capture Consolidation Cell (behavioral/synaptic tagging gate)
verdict: 🔵 PRE-REGISTERED architecture design (unmeasured) — $0 cheap_test pre-registered; engine-native + 303M gpu cost-gated NOT fired
source: brainarch_census
---

# H_1750 — Tag-and-Capture Consolidation Cell (behavioral/synaptic tagging gate)

- **tier:** 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy mirror, no engine); engine_native_measure + 303M = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** brainarch_census — 126-architecture whole-substrate (통짜 아키텍처) census: 뇌/인지 조직원리 × 엔진-네이티브 추상조건 (binding-wall program, H_1603).
- **key:** `synaptic_tag_capture_consolidation`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1284 (neuromodulation gain) · operator-level family H_1604-1685 (this card = 통짜 아키텍처 layer, 층위 다름)

## Organizing principle

Synaptic Tagging & Capture (Frey-Morris) as the CLS conversion gate: a fast episodic event deposits a transient DECAYING TAG at the coordinates it activates; a SEPARATE, SCARCE, slowly-replenished pool of plasticity-related products (PRP) is synthesized only on strong/novel/salient events and is CAPTURED only by sites currently bearing a tag. Persistent (semantic) weight change = tag AND PRP-availability. Most episodic tags decay UNconsolidated; only tagged-AND-funded sites become permanent. No replay and no sleep dependence — consolidation is a chemical coincidence gate, and PRP scarcity is the native honesty/novelty regulator.

## Whole design (input → internal dynamics → emit)

Input -> activates a sparse set of representational sites, each tag t_i(0)=1 decaying e^{−t/tau}. A global salience/novelty signal s = prediction-mismatch triggers PRP synthesis into a scarce, slow-replenishing, capped budget B. Each tick: permanent Delta w_i = kappa*t_i*min(B,demand)*sign — capture CONSUMES budget. Emit = codebook readout over consolidated (captured) weights + currently-tagged (still-labile) episodic sites. Tag field = short-lived addressable episodic store; captured weights = semantic store. Psi order parameter = PRP-budget fraction vs tag-demand: high budget + fresh tags -> externalize/consolidate-and-speak; depleted budget -> withhold/silence to replenish.

## Satisfies criteria (DESIGN claim · DIRECTIONAL · unmeasured)

HONESTY native and STRUCTURALLY ENFORCED: support-membership r = distance to nearest captured anchor + tag field -> AUROC->1; copy-or-abstain because you cannot CONSOLIDATE (assert into semantic store) what you did not FUND — PRP scarcity removes the fabrication channel, so off-support unfunded emit = abstain; gate-capacity disjoint (capture coincidence threshold separate from semantic expressivity, d-fab/d-capacity=0); groundedness because r reads actual captured weights (corrupt a captured site -> it begins to abstain). G2 novelty native: PRP synthesis is NOVELTY-GATED (s=prediction-error) -> only surprising compositions get consolidated -> builds semantic structure where data was absent = constrained extrapolation; retrieval control = freeze tags + zero budget -> emits only already-captured => 0 corpus-absent. G1/BINDING native: coincident tags from two co-active factors at a CONJUNCTION site get co-captured under one PRP allocation -> a bound conjunction weight neither factor alone produced (composed>max_single); interaction-ablation = separate per-factor budgets (block co-capture) -> drops to max_single. COMPOSITIONAL DEPTH = co-capture is non-separable (needs both tags + shared PRP) + tag-field systematicity. REALIZATION INVARIANT: captured weights are on the emit path; objective adequacy = consolidation funds reduction of prediction-error on TAGGED COMPOUNDS, unreachable by marginal-fit — marginals never surprise -> never trigger PRP -> no spurious consolidation (defuses lossF~0 trap: only conjunction-error is funded). Psi=1/2: budget<->demand antagonism, Lyapunov |Psi−1/2|, contraction (over-consolidate depletes budget->withhold up; over-withhold accumulates tags->demand up); endogeneity by INERT (infinite PRP -> always-emit boundary; remove tag-demand -> always-silent). SELF-CHAIN: identity = a super-funded, PRP-protected non-decaying captured anchor surviving the tag-field wipe at the session boundary; tiny ongoing re-capture = slow drift; ablate anchor -> chance; high-entropy anchor -> impostor reject. CLOSURE/G0/dist/falsifiable: V-tied readout (scramble->collapse), residual entropy from multiple captured attractors, falsifiable from co-captured comparator x magnitude x referents. Measurement-faithfulness: capture state IS the deployed weights, single dispatch.

## Not-LLM (a_no_llm_frame_trap)

STC is a CELLULAR consolidation gate where SCARCITY of plasticity-products regulates what may be asserted — transformers consolidate by gradient over the whole corpus indiscriminately (no tag, no scarcity, every pattern fit) and therefore CANNOT abstain natively. The lever is the tag AND PRP coincidence + a scarce budget, not parameter count or more data (a_no_llm_frame_trap).

## Cheap test (frozen-first · $0 · numpy mirror · DIRECTIONAL)

numpy: tag field over a toy factored grammar, scalar PRP budget B with novelty-gated synthesis. Frozen-first: (a) drive out-of-support unfunded inputs -> fabrication ~0; force-funded (short-circuit gate) -> fab jumps (causal gate proof); (b) co-capture two factors -> composed >=2 AND >max_single; separate budgets -> drops to max_single; (c) zero-budget mode -> 0 novel (control); (d) perturb B off 1/2 -> restoration; ablate anchor -> cross-boundary cos->chance. $0.

## Engine-native measure (cost-gated · PRE-REGISTER ONLY · NOT fired)

Tag field -> OsmoticStore transient/labile cells; capture -> osmotic_should_split/osmotic_learn permanent commit; PRP budget -> a SS-HomeostaticDrive/SS-Neuropharm scalar (pharm_perturb_recon). Non-fab via osmotic_retains AUROC + fab on out-of-support (g_eval_g5-style abstain). G0/G1/G2 via cli/anima.hexa eval -> core/g_gates.hexa g_eval_g0/g1/g2; falsifiable via core/g6_ideation.hexa g6_score_arm_auto. Psi via safety_phi_ratchet; self-chain via self_* round-trip across a simulated boundary. Byte-parity engine_cli.py mirror — no torch-only verdict.

## Scope / honesty (c9)

## Distinction (near-overlap kept, not a dup)

Near-overlap with cls cards + dual_timescale_fast_slow_weights (this census) — distinct: STC's consolidation gate is tag AND PRP-scarcity coincidence (you cannot assert what you did not FUND); the scarce-PRP-as-honesty is the differentiator.

Toy numpy first; PRP replenish rate & capture kappa are scale-sensitive (a_scale_honest_scope). Directional until engine-native fire on a live ckpt. The scarcity-as-honesty claim is the load-bearing novelty — verify the gate is causal (ablation jump), not corpus-confounded.

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). engine_native_measure 는 단일 진입점 cli/anima.hexa → generator L3 → g_gates/g6 경유 byte-parity 채점만 terminal; torch-only/side-harness 결과는 DIRECTIONAL. numpy cheap_test 결과도 DIRECTIONAL(엔진-네이티브 아님). gpu/engine 발사 시 held-out mirror-DESCENT(a_clm_gen_pipeline) + CORE mount frozen-bar engine-native 재측정 + ckpt PULL(a_fire_recover_complete).
