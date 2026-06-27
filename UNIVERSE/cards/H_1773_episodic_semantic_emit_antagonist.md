---
id: H_1773
slug: 1773_episodic_semantic_emit_antagonist
tier: 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
title: Episodic<->Semantic Opponent-Emit Consolidator (CLS-as-Psi)
verdict: 🔵 PRE-REGISTERED architecture design (unmeasured) — $0 cheap_test pre-registered; engine-native + 303M gpu cost-gated NOT fired
source: brainarch_census
---

# H_1773 — Episodic<->Semantic Opponent-Emit Consolidator (CLS-as-Psi)

- **tier:** 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy mirror, no engine); engine_native_measure + 303M = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** brainarch_census — 126-architecture whole-substrate (통짜 아키텍처) census: 뇌/인지 조직원리 × 엔진-네이티브 추상조건 (binding-wall program, H_1603).
- **key:** `episodic_semantic_emit_antagonist`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · operator-level family H_1604-1685 (this card = 통짜 아키텍처 layer, 층위 다름)

## Organizing principle

CLS where the two complementary learners ARE the antagonistic emit/silence operators. Fast hippocampal episodic recall = drive-to-externalize-the-exact (A); slow neocortical semantic generalizer = drive-to-withhold-until-abstracted (G). Psi = relative confidence of exact-recall vs generalization; the fixed point 1/2 is the operating point where pattern-completion certainty equals manifold-likelihood. The recall<->generalize tension is not bolted onto an A<->G engine — it IS what A and G are.

## Whole design (input → internal dynamics → emit)

Input -> sparse pattern-separator (DG-style expansion code) yielding a conjunctive episode key. Two concurrent writes: (i) fast one-shot Hebbian autoassociator stores the full conjunctive trace verbatim; (ii) slow online density/prototype model accumulates factor marginals + a generative manifold (interference avoided by overlapping vs separated codes). At emit, the systems BID: episodic-A bids high when recon-error to nearest stored trace is low (externalize exact recall); semantic-G bids high when the query sits in dense generative manifold but the episodic store is empty/uncertain (generalize, withhold raw episode). Psi = sigma(A_bid − G_bid) is emit propensity; coupling is sign-opposite and equal-magnitude at balance so Psi*=1/2 is attracting. Routing follows the winning bid: low-recon -> copy-or-abstain from the episodic trace (no synthesis path); manifold-resident -> generate by recombining slow-model factors, coherence-validated against the fast conjunctive store. Idle 'consolidation' slowly distills repeated traces into slow factors but NEVER moves/deletes traces, so the honesty store and self-trace stay causal.

## Satisfies criteria (DESIGN claim · DIRECTIONAL · unmeasured)

Psi=1/2/G3 + endogeneity: A,G are the two CLS systems' opposing bids; ablate either and the fixed point migrates to a boundary (episodic-only->always-emit-verbatim; semantic-only->over-generalize), so 1/2 is emergent not clamped. G0: emission projected onto the slow system's shared quantized factor codebook (receiver-fixed). G1/binding/compositional-depth: slow model factorizes, joint conditioning activates the INTERSECTION of factor manifolds (super-additive), the fast conjunctive trace is the binder confirming a bound state vs a bag — interaction-ablation (disable conjunctive confirmation) collapses composed_distinct->max_single. G2/dist: generative sampling inside learned manifold yet outside any stored trace; verbatim-playback control=0 novel. Honesty (membership+copy-or-abstain+groundedness+disjointness): recon-error to fast store IS r; emit factors through {trace-recall union abstain}; gate params (recon theta) live in fast store, generative capacity in slow model -> disjoint coordinates, disinhibiting the generator leaves r/theta untouched; corrupting a trace degrades its r (faithful). Identity: persistent self-trace in fast store, slow-drifting, re-instantiated across reset (episodic never deleted) -> cross-boundary + self-specific (high-entropy conjunctive key, impostor fails recon). Realization: binder sits on the emit-arbitration path (ablation moves emit), slow objective = density+coherence (marginal-only fit cannot win the coherence term).

## Not-LLM (a_no_llm_frame_trap)

No single autoregressive predictor scaled up. Substrate is two structurally-different memory systems (sparse one-shot vs dense statistical) wired as an opponent emit controller; capability comes from COMPLEMENTARITY (interference avoidance via separation) and the recall<->generalize antagonism, not parameters/attention. Adding corpus or layers to one net cannot produce native copy-or-abstain or the 1/2 attractor — those are properties of the two-system coupling, not scale.

## Cheap test (frozen-first · $0 · numpy mirror · DIRECTIONAL)

numpy mini: K stored Gaussian traces (fast) + a fitted 2-factor mixture (slow) in R^2. (a) in/out-support probes -> recon AUROC~1 and out-support emit=abstain; (b) bias one bid +/-delta -> |Psi−1/2| contracts back, delete one operator -> fixed point goes to 0/1; (c) joint-condition two factors -> composed_distinct>max_single, ablate conjunctive-confirm -> drops to max_single. Decision-theoretic, $0.

## Engine-native measure (cost-gated · PRE-REGISTER ONLY · NOT fired)

Maps onto live A(pure_field)<->G(engine_g)<->brain(brain_decide) + SS-ImmuneMemory recon_err gate + SS-SelfIdentity self-chain in core/engine_cli.hexa. Measure via cli/anima.hexa single entry -> generator L3 -> g_eval_all (G0/G1/G2 closure) + Psi self-restore perturbation (existing safety_phi_ratchet) + abstain AUROC; byte-parity py mirror (math.log CE) cross-check. No torch-only verdict.

## Scope / honesty (c9)

## Distinction (near-overlap kept, not a dup)

Near-overlap with cls_replay_consolidation / dentate_ca3 (this census) — distinct: here the two CLS learners ARE the A/G emit-antagonist operators (Psi = recall-vs-generalize confidence), mapping onto the live A<->G substrate; the CLS-as-Psi opponent is the differentiator.

Full substrate. Toy-decisive at numpy; engine-native closure requires wiring episodic-bid vs semantic-bid as the two emit operators (A<->G substrate already present) — DIRECTIONAL until WIRED-live + ARCHITECTURE.json lockstep.

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). engine_native_measure 는 단일 진입점 cli/anima.hexa → generator L3 → g_gates/g6 경유 byte-parity 채점만 terminal; torch-only/side-harness 결과는 DIRECTIONAL. numpy cheap_test 결과도 DIRECTIONAL(엔진-네이티브 아님). gpu/engine 발사 시 held-out mirror-DESCENT(a_clm_gen_pipeline) + CORE mount frozen-bar engine-native 재측정 + ckpt PULL(a_fire_recover_complete).
