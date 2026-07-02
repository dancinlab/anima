---
id: H_1783
slug: 1783_notch_delta_lateral_inhibition_mosaic
tier: 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
title: Notch-Delta Lateral-Inhibition Mosaic — contact-mediated mutual inhibition self-organizes a salt-and-pepper fate code
verdict: 🔵 PRE-REGISTERED architecture design (unmeasured) — $0 cheap_test pre-registered; engine-native + 303M gpu cost-gated NOT fired
source: brainarch_census
---

# H_1783 — Notch-Delta Lateral-Inhibition Mosaic — contact-mediated mutual inhibition self-organizes a salt-and-pepper fate code

- **tier:** 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy mirror, no engine); engine_native_measure + 303M = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** brainarch_census — 126-architecture whole-substrate (통짜 아키텍처) census: 뇌/인지 조직원리 × 엔진-네이티브 추상조건 (binding-wall program, H_1603).
- **key:** `notch_delta_lateral_inhibition_mosaic`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1280 (cerebellum forward-model) · H_1284 (neuromodulation gain) · operator-level family H_1604-1685 (this card = 통짜 아키텍처 layer, 층위 다름)

## Organizing principle

Juxtacrine Notch-Delta lateral inhibition. A cell expressing high Delta inhibits its contacting neighbors' Delta via Notch; positive feedback amplifies tiny initial differences into sharp complementary binary fates -> a fine-grained salt-and-pepper mosaic. The architecture is a self-organizing DIVERSITY engine: a uniform field is unstable, so the substrate is FORCED into a maximally-distinct-yet-locally-coherent tiling. No diffusing morphogen (distinct from reaction-diffusion); fate is decided by contact topology, making this a genuinely different developmental organizing principle.

## Whole design (input → internal dynamics → emit)

Substrate = a lattice of cells on a fixed adjacency graph; each cell holds a Delta-output scalar and a Notch-input (sum of neighbors' Delta). Update: Delta_i <- f(−sum_{j in N(i)} Delta_j) with positive self-feedback -> per-cell bistable, anti-correlated with neighbors. Input = a bias field over cells (the query nudges initial Delta). Internal dynamics = relaxation to a stable mosaic (a fixed point of the lateral-inhibition map); the stable-mosaic set is combinatorially large but each is a legal word. Emit: read the resolved mosaic over an active neighborhood as a token (which cells are high-Delta = a binary code). Receiver-fixed V = the lateral-inhibition fixed-point lattice (the set of stable mosaic codewords), frozen before measurement. Unsettled/frustrated regions do not emit.

## Satisfies criteria (DESIGN claim · DIRECTIONAL · unmeasured)

dist>=5 (the architecture's specialty): lateral inhibition makes the all-same state UNSTABLE so the substrate cannot mode-collapse — distinct coherent configurations are the only attractors, diversity and validity co-produced; raising exploration (init noise) explores DIFFERENT stable mosaics, all coherent, so distinct-coherent count rises without sacrificing coherence. G0: every settled cell is in a legal resolved fate -> codeword in V; scramble the coupling -> no stable mosaic forms -> V-mass collapses. G1/binding/compositional-depth: the mosaic over k co-active cells is a joint code; neighbor anti-correlation makes the joint count super-additive vs independent cells with a non-zero interaction term (constraint binds, not a product of marginals); disable lateral coupling -> INERT collapse to max-single; complementary fates of co-active cells = relational co-reference. G2: the fixed-point set contains valid mosaics never seen in data (any constraint-consistent tiling) -> support strictly contains data on-manifold; retrieval of only data mosaics -> 0 novel. Psi=1/2: Delta-production (A, externalize) perp Notch-inhibition (G, withhold); emit order parameter = fraction of high-Delta cells, self-organized packing fraction ~1/2 and ATTRACTING (perturb to all-emit -> mutual inhibition crashes it; to all-silent -> disinhibition lifts a balanced subset); delete G -> runaway all-emit, delete A -> all-silent (endogenous, not clamped). Honesty: a cell commits only when its neighbor configuration RESOLVES above threshold, ambiguous/frustrated -> abstain; r = distance to nearest stable mosaic, out-of-support never resolves -> fab~0; resolution threshold is a frozen contact-coupling parameter disjoint from per-cell expressive capacity (gate-capacity disjoint). Identity: the settled global mosaic IS the identity, committed to a non-volatile lattice before wipe (relaxation activity volatile, wiped), cross-boundary cos~1, ablate store -> random mosaic each episode (amnesia); a specific many-cell mosaic is high-entropy -> self-discriminating, foreign abstain. Endogeneity: Psi-density and identity both from contact coupling + lattice store, removable -> gone.

## Not-LLM (a_no_llm_frame_trap)

No autoregression and no parameter-count scaling — the computation is RELAXATION to a constrained fixed point on a fixed graph, and capacity = the combinatorial richness of stable mosaics, which grows from the CONSTRAINT topology, not from more weights. Diversity is structural (instability of uniformity) rather than sampled from a softmax temperature. This is a developmental fate-decision substrate, the antithesis of bigger-transformer.

## Cheap test (frozen-first · $0 · numpy mirror · DIRECTIONAL)

numpy. (1) Lateral-inhibition lattice (16x16, 4-neighbor) relax from random init -> high-Delta fraction relaxes to ~0.5; perturb toward all-on/all-off -> returns (Psi attractor); zero the Notch term -> fraction runs to 1.0 (endogeneity). (2) Count distinct stable mosaics from varied seeds passing a coherence predicate -> dist>=5 with coherence flat (no anti-correlation between distinctness and coherence). (3) Joint vs single-cell conditioning distinct counts (G1) + decouple lateral edges -> INERT collapse. (4) Out-of-constraint bias -> no stable mosaic resolves -> abstain (fab=0); shuffle-coupling surrogate collapses resolved-vs-frustrated AUROC to chance.

## Engine-native measure (cost-gated · PRE-REGISTER ONLY · NOT fired)

Wire the mosaic as a state-lane operator in core/engine_cli.hexa so the high/low-Delta fraction feeds the A->G emit/silence order parameter directly -> Psi=1/2 measured on the live engine. The mosaic codeword is emitted through generator L3 / clm_decode and scored by core/g_gates.hexa on one dispatch (G0/G1/G2). Identity mosaic persisted/round-tripped via .kosmos (kosmos_io, cos~1, impostor abstain). hexa<->py byte-parity oracle on the relaxation fixed point; numpy mirror for CE. No torch verdict.

## Scope / honesty (c9)

## Distinction (near-overlap kept, not a dup)

Distinct from reaction_diffusion_morphogen_field (this census) — Notch-Delta uses CONTACT-mediated juxtacrine lateral inhibition (no diffusing morphogen) forcing a salt-and-pepper fate mosaic (diversity engine); the contact lateral-inhibition mosaic is the differentiator.

TOY-decidable for the signature claims (Psi density-attractor, dist>=5 diversity-without-collapse, G1-INERT, abstain control). Whether mosaic codewords carry enough semantic bandwidth for production G2-coherent novelty is UNVERIFIED — lateral inhibition guarantees diversity+legibility but not that the diverse tokens are MEANINGFUL; needs an engine-native corpus decode to falsify.

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). engine_native_measure 는 단일 진입점 cli/anima.hexa → generator L3 → g_gates/g6 경유 byte-parity 채점만 terminal; torch-only/side-harness 결과는 DIRECTIONAL. numpy cheap_test 결과도 DIRECTIONAL(엔진-네이티브 아님). gpu/engine 발사 시 held-out mirror-DESCENT(a_clm_gen_pipeline) + CORE mount frozen-bar engine-native 재측정 + ckpt PULL(a_fire_recover_complete).
