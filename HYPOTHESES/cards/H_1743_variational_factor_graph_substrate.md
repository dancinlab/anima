---
id: H_1743
slug: 1743_variational_factor_graph_substrate
tier: 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
title: Variational Factor-Graph Free-Energy Substrate (Bayesian-brain loopy message passing)
verdict: 🔵 PRE-REGISTERED architecture design (unmeasured) — $0 cheap_test pre-registered; engine-native + 303M gpu cost-gated NOT fired
source: brainarch_census
---

# H_1743 — Variational Factor-Graph Free-Energy Substrate (Bayesian-brain loopy message passing)

- **tier:** 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy mirror, no engine); engine_native_measure + 303M = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** brainarch_census — 126-architecture whole-substrate (통짜 아키텍처) census: 뇌/인지 조직원리 × 엔진-네이티브 추상조건 (binding-wall program, H_1603).
- **key:** `variational_factor_graph_substrate`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1284 (neuromodulation gain) · operator-level family H_1604-1685 (this card = 통짜 아키텍처 layer, 층위 다름)

## Organizing principle

The cortex as a sparse probabilistic graphical model (factor graph) that minimizes variational free energy by iterative message passing — Dauwels/Friston variational message passing, the 'Bayesian brain'. The whole substrate IS the graph; computation is messages between variable-nodes and factor-nodes, never stacked layers. Prediction = forward messages from priors/likelihoods; error = backward residual messages; precision (inverse variance) weights each edge.

## Whole design (input → internal dynamics → emit)

Substrate = bipartite factor graph: variable nodes (latent causes, each a categorical/Gaussian belief) + factor nodes (learned local potentials encoding constraints). Output variable nodes are TIED to the receiver-fixed alphabet V. (1) Input clamps observation variable nodes. (2) Internal dynamics: loopy belief propagation to a free-energy minimum — each factor emits a forward prediction message, each variable returns a precision-weighted residual, iterate to convergence. (3) Emit: when an output variable's marginal concentrates on V AND the free-energy gradient is flat (converged), externalize its MAP symbol; sequential generation = re-clamping the emitted symbol and re-converging. (4) Silence while messages still circulate (free energy not minimized) or the marginal is diffuse. (5) Order parameter Psi = balance of two opposed message families — bottom-up evidence-push (commit/emit) vs top-down prior-pull (withhold-until-consistent) — whose symmetric coupling fixes the attractor. (6) A persistent 'self' subgraph (slow-prior variable+factor set) is checkpointed across episodes while fast message states are wiped.

## Satisfies criteria (DESIGN claim · DIRECTIONAL · unmeasured)

G0: output variable domain IS V, so marginal-mass-on-V legibility is structural, not bolted on. G1 binding: factor nodes coupling >=2 variables are literally joint potentials with non-zero interaction terms — a pairwise/ternary factor is not a product of unaries, so composed_distinct > max_single by construction; setting that factor to uniform (ablation) collapses composed to max_single (native INERT test). G2 novelty: sampling the joint defined by the factors yields valid configurations satisfying constraints but absent from data (supp(model) is the proper superset between noise and data); clamping all vars to a data point = verbatim control = 0 novel. dist>=5: distinct loopy-BP fixed points under varied init/precision-tempering give distinct-yet-coherent spread. falsifiable>=1: a factor binding {comparator-var x quantity-var x >=2 content-vars} emits a complement-bearing claim. Psi=1/2: opponent message families with equal-and-opposite coupling give a contractive fixed point at 1/2 (remove one family -> fixed point migrates to a 0/1 boundary = endogeneity). Honesty: residual at a variable's anchoring factor is the recon_err analog; out-of-support input concentrates no marginal so the NULL/abstain variable wins (copy-or-abstain is structural — emit requires a concentrated marginal sourced from a learned factor potential); AUROC from marginal entropy. Binding (H_961): shared belief space, same-cause constituents excite overlapping factors -> near in latent. Endogeneity: deleting the opponent factor or the persistent subgraph removes Psi-restoration / identity-continuity respectively.

## Not-LLM (a_no_llm_frame_trap)

No stacked attention, no scale lever. Capacity comes from graph TOPOLOGY (which variables share which factors) plus learned local potentials, not parameter count — the 'add the missing structure (a factor) beside it' prescription, not 'bigger transformer'. Composition is the factor potential itself (structural binding), not an emergent property of depth. Adding corpus cannot create a binding the graph lacks; you add the factor. Inference is bidirectional message passing to a free-energy minimum, the antithesis of a single feedforward softmax over a vocab.

## Cheap test (frozen-first · $0 · numpy mirror · DIRECTIONAL)

mini-numpy: 3 categorical variable nodes over a 5-symbol V + one ternary factor encoding a constraint; run loopy BP to convergence. Probe (a) composed_distinct with ternary factor ON vs uniform-ablated — must drop to max_single when ablated (G1-INERT discriminator). Probe (b) sample the joint -> count valid configs absent from a tiny training set vs verbatim-clamp control which must read 0 (G2 absence-predicate). Probe (c) perturb opponent-message gain -> check Psi returns to 1/2 vs delete one family -> migrates to boundary. $0, decisive on G1-binding, G2-control, and Psi-endogeneity.

## Engine-native measure (cost-gated · PRE-REGISTER ONLY · NOT fired)

Implement message-passing convergence as a core/*.hexa op whose output marginal is fed into generator L3 mouth dispatch (gen_auto_ideate), then score G0/G1/G2 via core/g_gates.hexa::g_eval_all through the single entry cli/anima.hexa (not a side-harness). Psi via core/engine_cli.hexa SS-ThirdLaw perturbation-return; honesty via SS-ImmuneMemory recon_err parity (anchoring-factor residual <-> recall_thr). A byte-parity py mirror cross-validates the marginals (math.log, no torch). torch only as a 3-way golden, never in the verdict path.

## Scope / honesty (c9)

## Distinction (near-overlap kept, not a dup)

Near-overlap with predictive_coding cards + nonparametric_cause_partition (this census) — distinct: explicit FACTOR-GRAPH variational message passing where each multi-variable FACTOR is the structural binder; the factor-as-binding-operator is the differentiator.

Toy-first: small sparse graph, V = byte-class subset. Loopy-BP convergence on dense graphs is a known wall — claim only on sparse/tree-like topologies until measured. Scale-transfer of factor-learning to a 303M-class symbol manifold UNVERIFIED (a_toy_scale_recheck).

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). engine_native_measure 는 단일 진입점 cli/anima.hexa → generator L3 → g_gates/g6 경유 byte-parity 채점만 terminal; torch-only/side-harness 결과는 DIRECTIONAL. numpy cheap_test 결과도 DIRECTIONAL(엔진-네이티브 아님). gpu/engine 발사 시 held-out mirror-DESCENT(a_clm_gen_pipeline) + CORE mount frozen-bar engine-native 재측정 + ckpt PULL(a_fire_recover_complete).
