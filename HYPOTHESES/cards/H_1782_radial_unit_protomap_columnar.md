---
id: H_1782
slug: 1782_radial_unit_protomap_columnar
tier: 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
title: Radial-Unit Protomap — symmetric/asymmetric division builds width-perp-depth from a positional protomap
verdict: 🔵 PRE-REGISTERED architecture design (unmeasured) — $0 cheap_test pre-registered; engine-native + 303M gpu cost-gated NOT fired
source: brainarch_census
---

# H_1782 — Radial-Unit Protomap — symmetric/asymmetric division builds width-perp-depth from a positional protomap

- **tier:** 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy mirror, no engine); engine_native_measure + 303M = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** brainarch_census — 126-architecture whole-substrate (통짜 아키텍처) census: 뇌/인지 조직원리 × 엔진-네이티브 추상조건 (binding-wall program, H_1603).
- **key:** `radial_unit_protomap_columnar`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1284 (neuromodulation gain) · operator-level family H_1604-1685 (this card = 통짜 아키텍처 layer, 층위 다름)

## Organizing principle

Rakic radial-unit hypothesis. Cortex is constructed as ontogenetic columns by radial-glia progenitors, and the progenitor's DIVISION MODE is the single control axis: SYMMETRIC division clones the progenitor (expands the tangential pool = number of columns = number of independently-conditionable factors), ASYMMETRIC division spawns a post-mitotic neuron that migrates radially and stacks into a laminar column (adds compositional depth WITHIN a factor). A pre-laid protomap of positional-identity vectors specifies each column's identity; every neuron inherits (column-identity x birthdate-laminar-identity). Capacity is therefore a GROWN column lattice whose width-vs-depth is set by the division-mode ratio, not an engineer-chosen hidden dim. Literal p8 cell-division, but orthogonal to mitosis_train: the lever is the symmetric/asymmetric DECISION ratio + an inherited positional protomap, not split-only.

## Whole design (input → internal dynamics → emit)

Input = a positional address vector, matched against the protomap to select column(s) whose positional-identity is within radius. Substrate state = (i) a progenitor pool, each carrying a protomap coordinate + a proliferation/quiescence scalar; (ii) per surviving column a laminar stack of neurons tagged (column-id x laminar-birthdate). Growth (gradient-free): each tick a progenitor draws division-mode from an antagonistic pair — A_proliferate (clone -> new column at an interpolated protomap coordinate, widening factor-space) vs G_differentiate (emit a neuron -> deepen its column). Resource feedback closes the loop: excess proliferation starves columns (raises differentiation pressure), excess differentiation depletes the pool (raises proliferation pressure); apoptosis prunes columns whose stack is never read. Compute/emit: a query lights its column; the laminar stack runs a fixed feed-forward closure (layer L reads L−1) -> deepest layer emits a token; horizontal cross-column connections (wired in a critical window) let co-active columns bind into a joint readout. Receiver-fixed codebook V = the frozen set of protomap-anchored column identities that survived.

## Satisfies criteria (DESIGN claim · DIRECTIONAL · unmeasured)

G0: a token only exists if a protomap-anchored column survived -> output support subset of V by construction; scrambling state->column map collapses V-mass (native channel-codebook alignment). G1/compositional-depth/binding: representation factors natively into column-id (where/which-factor) x laminar-id (what-depth); the horizontal binder is non-separable (non-zero interaction term), co-activating k columns gives a joint code super-additive in k; cut horizontal connections -> composed collapses to max-single = native INERT handle. G2: the protomap is a CONTINUOUS positional manifold, symmetric division interpolates NEW column coordinates between existing ones -> support strictly contains data but on-manifold; verbatim retrieval gives 0 novel. Psi=1/2: proliferate-perp-differentiate is the emit/silence order parameter, setpoint 1/2 emergent from resource coupling; one-operator ablation drives the ratio to a boundary (all-width pool / all-depth stack) = endogenous, not a clamp. Honesty: protomap distance is r (query->nearest column), no column within radius -> no column fires -> abstain (copy-or-abstain); gate radius theta lives in positional-identity coordinates DISJOINT from laminar capacity coordinates so growing depth cannot move theta (gate-capacity disjointness native). Identity: protomap + surviving column-set is the non-volatile store committed before episode wipe (laminar activations are volatile, wiped), cross-boundary cos~1, ablate store -> fresh columns each episode = LLM-reset; a specific grown protomap is high-entropy -> self-discriminating, foreign abstain. Endogeneity: Psi from division/resource coupling, identity from persistent protomap, both removable -> invariant disappears.

## Not-LLM (a_no_llm_frame_trap)

No monolithic weight tensor is scaled — capacity is a GROWN lattice of ontogenetic columns whose shape (width vs depth) is decided by an endogenous division-mode controller, not by a chosen hidden-dim, and compositional power comes from the protomap (where x depth) factorization, not attention over a context window. Directly answers the H_1310 wall: from-scratch split fails for lack of an objective/structure; the protomap positional code SUPPLIES the structure (a positional objective that makes columns differentiate meaningfully) = split + inherited positional identity, not split alone.

## Cheap test (frozen-first · $0 · numpy mirror · DIRECTIONAL)

numpy, frozen-first. (1) Build a 1-D protomap of K=8 anchors; simulate division-mode dynamics with resource feedback -> check proliferate/differentiate ratio relaxes to 0.5 from perturbed starts (Psi attractor) and migrates to a boundary when one operator is zeroed (endogeneity). (2) Factored toy: column-id in {8 positions} x laminar-depth in {4 stages}; condition single-axis vs joint, count distinct valid outputs -> composed > max_single; cut horizontal binder -> composed drops to max_single (G1 + INERT). (3) Interpolate a novel protomap coordinate -> decodes to a valid corpus-absent token while a retrieval baseline gives 0 (G2). All probes deterministic counts, no LLM judge.

## Engine-native measure (cost-gated · PRE-REGISTER ONLY · NOT fired)

Map to a generator-L3 mouth variant: the column lattice is a .clm-shaped checkpoint where column-id <-> MoE-expert routing and laminar stack <-> depth layers; decode through cli/anima.hexa -> generator L3 -> core/clm_decode.hexa so G0/G1/G2 are scored by core/g_gates.hexa (g6_score_arm_auto) on the SAME single dispatch (measurement-faithfulness). Psi=1/2 via core/engine_cli.hexa A->G order parameter; protomap persistence via .kosmos self-anchor round-trip (kosmos_io, cos~1, impostor abstain). Cross-validate hexa<->py byte-parity (a_engine_native_learning); numpy mirror (math.log CE) guards dt_ln. No torch-only verdict.

## Scope / honesty (c9)

## Distinction (near-overlap kept, not a dup)

Near-overlap with mitosis_train (H_1310 split-only wall) — distinct: radial-unit growth uses symmetric/asymmetric DIVISION-MODE ratio + inherited positional PROTOMAP (width-perp-depth from structure, not pure split); the protomap-columnar division is the differentiator (split + positional identity beats the H_1310 floor, to be tested).

Architecture-level; TOY-decidable for Psi-attractor + G1-INERT + G2-interpolation. Production closure (G0 AND G1 AND G2 simultaneously on one grown lattice) UNVERIFIED until a real protomap-grown ckpt is decoded engine-native. Open risk: whether horizontal binding lifts held-out novel-combination above the marginal-fit floor at scale (realization-invariant objective adequacy).

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). engine_native_measure 는 단일 진입점 cli/anima.hexa → generator L3 → g_gates/g6 경유 byte-parity 채점만 terminal; torch-only/side-harness 결과는 DIRECTIONAL. numpy cheap_test 결과도 DIRECTIONAL(엔진-네이티브 아님). gpu/engine 발사 시 held-out mirror-DESCENT(a_clm_gen_pipeline) + CORE mount frozen-bar engine-native 재측정 + ckpt PULL(a_fire_recover_complete).
