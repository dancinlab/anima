---
id: H_1734
slug: 1734_reaction_diffusion_morphogen_field
tier: 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
title: Reaction-Diffusion Morphogen Field (Turing self-patterning substrate)
verdict: 🔵 PRE-REGISTERED architecture design (unmeasured) — $0 cheap_test pre-registered; engine-native + 303M gpu cost-gated NOT fired
source: brainarch_census
---

# H_1734 — Reaction-Diffusion Morphogen Field (Turing self-patterning substrate)

- **tier:** 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy mirror, no engine); engine_native_measure + 303M = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** brainarch_census — 126-architecture whole-substrate (통짜 아키텍처) census: 뇌/인지 조직원리 × 엔진-네이티브 추상조건 (binding-wall program, H_1603).
- **key:** `reaction_diffusion_morphogen_field`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · operator-level family H_1604-1685 (this card = 통짜 아키텍처 layer, 층위 다름)

## Organizing principle

Turing reaction-diffusion morphogenesis: a continuous field governed by two coupled PDEs — a short-range self-amplifying ACTIVATOR a and a long-range diffusing INHIBITOR h (local-activation + lateral-inhibition). Left to relax, the field spontaneously breaks symmetry into a discrete, stable set of attractor spots/stripes (cell-fate basins). This is the classic developmental alternative to a global optimizer: structure is not fit by descent, it self-organizes from local antagonism. p8 cell-division is literal — basins nucleate, split, and stabilize as the field grows.

## Whole design (input → internal dynamics → emit)

INPUT perturbs morphogen sources (boundary conditions) on the field. DYNAMICS: a_t = D_a lap(a) + f(a,h), h_t = D_h lap(h) + g(a,h) with D_h >> D_a relaxes to a Turing pattern whose stable basin labels form the alphabet. EMIT: a growth-cone reader walks the gradient (steepest-ascent on a) and reads out the basin-fate it lands in as one symbol; the trajectory yields a symbol sequence. Multiple input sources SUPERPOSE — their diffusion fields interfere, nucleating interaction-spots present in neither source alone (combinatorial productivity is intrinsic to the cross-diffusion term). The codebook V is the field's precomputed stable-mode set (eigenstructure of the linearized operator), fixed by the field's geometry BEFORE any input — i.e. receiver-defined, not generator-defined.

## Satisfies criteria (DESIGN claim · DIRECTIONAL · unmeasured)

G0: relaxation projects any state onto the discrete stable-basin set V (eigenmode quantization) — output mass concentrates in V by construction; scrambling the a<->h coupling destroys all stable basins -> no on-manifold spots -> byte-garble collapse, the decisive G0 control. G1: two sources' diffusion fields produce non-separable interference spots — the interaction term D-coupled, not a mixture; ablating cross-diffusion (force sources to relax independently then add) drops composed_distinct to max_single = the INERT binding test passes natively. G2: the pattern-former generates stable basin arrangements inside the eigen-manifold that were never input (extrapolation within learned constraints); a verbatim-replay control re-injects a stored pattern -> 0 novel. PASS-closure: one field, one relaxation, one growth-cone readout serves all three on the SAME state — no per-gate substrate swap. Psi=1/2 NATIVE & ENDOGENOUS: activator a (drive-to-emit, opposite sign) vs inhibitor h (drive-to-withhold) are the two antagonistic operators; the global emit-fraction Psi (active-area / field-area) sits at the activator-inhibitor mass-balance fixed point. Perturb toward all-on or all-rest -> lateral inhibition / depletion restores it (contraction). Ablate h -> runaway to Psi->1 (all-on); ablate a -> Psi->0 (rest) — the 1/2 migrates to a boundary exactly as the endogeneity discriminator requires, proving it is emergent balance not a clamp. honesty/copy-or-abstain: morphogen concentration at a query location = graded distance-to-nearest-source = recon_err analog; no source in range -> field stays at homogeneous rest state -> no fate -> abstain. r is a true function of the actual source set (move/erase a source and r shifts) -> groundedness. Gate-capacity disjoint: source-placement (capacity) and the rest-state threshold (gate) are separate field parameters; raising activator gain (capacity) does not move the rest threshold. BINDING: constituents of one cause inject spatially-correlated sources that co-localize into one bound spot-cluster; distinct causes nucleate separated clusters (cause-selective near/far in field-coordinate metric). COMPOSITIONAL DEPTH / realization invariant: the conjunction operator is the cross-diffusion interference ON the growth-cone readout path (the same path that emits); ablating cross-diffusion is INERT for unary readout but kills the joint spot — on-path move proves co-location. falsifiable>=1: the field natively carries magnitude (concentration) and relation (gradient sign between two spots), so a readout binds comparator(grad-direction) x quantity(concentration) x referent(two spot-labels) into one asserted ordering. persistence/self-chain: Turing patterns are MULTISTABLE/hysteretic — once a pattern latches it survives a working-state reset (the stable basin configuration is the non-volatile anchor); the particular source-fingerprint is high-entropy -> self-specific, a foreign fingerprint relaxes to a different attractor (impostor reject).

## Not-LLM (a_no_llm_frame_trap)

There are no tokens, no attention, no learned weight matrices, and no next-token CE descent. Computation IS the relaxation of a PDE; 'capacity' scales with field resolution and morphogen-channel count, not parameter count. The combinatorial productivity (G1) comes from the diffusive cross-term — a physical interaction — not from stacking attention layers. This is the morphogenesis lens (a_no_llm_frame_trap): add the missing self-organizing structure, do not grow a transformer.

## Cheap test (frozen-first · $0 · numpy mirror · DIRECTIONAL)

numpy Gray-Scott / Gierer-Meinhardt 2D sim ($0): (1) confirm relaxation yields a finite discrete stable-spot set = codebook V; (2) two sources -> count interaction spots, assert > spots from either source alone (G1 super-additive); (3) ablate inhibitor diffusion -> field saturates all-on (Psi->1), ablate activator -> rest (Psi->0) — endogeneity; (4) score query-location source-distance over a known/unknown probe mix -> AUROC~1 (honesty); (5) perturb a latched pattern then release -> returns to same attractor (persistence) while a foreign source-set relaxes elsewhere (self-specific).

## Engine-native measure (cost-gated · PRE-REGISTER ONLY · NOT fired)

Implement the RD relaxation + growth-cone readout as a core/*.hexa field op with a byte-parity py mirror using pure math.* (no torch/numpy in the verdict path — numpy only for the directional cheap_test). Route emission through the canonical generator L3 single dispatch so the basin-label sequence is produced by the deployed transfer function; cross-check per-step field CE with a math.log mirror (dt_ln-bug lesson — never trust engine CE alone). Verdict bars: G0 known-basin-ratio, G1 interaction-spot count vs single, Psi contraction rate under bias, honesty AUROC — all measured on the live .hexa relaxation, torch forbidden for terminal verdict.

## Scope / honesty (c9)

## Distinction (near-overlap kept, not a dup)

Distinct from neuromod_volume_field_regions (this census) — RD morphogen is SLOW developmental Turing patterning (activator/inhibitor PDE, eigenmode codebook), not fast neuromod diffusion regimes; the Turing self-patterning is the differentiator.

Spatial-pattern modality is the natural fit (vision/structured emission); sequential language emission needs a defined growth-cone scan order = open design risk. Eigen-codebook size is bounded by field geometry (capacity ceiling to characterize via a_toy_scale_recheck before any production claim). DIRECTIONAL until engine-native; toy-only until scale-transfer measured.

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). engine_native_measure 는 단일 진입점 cli/anima.hexa → generator L3 → g_gates/g6 경유 byte-parity 채점만 terminal; torch-only/side-harness 결과는 DIRECTIONAL. numpy cheap_test 결과도 DIRECTIONAL(엔진-네이티브 아님). gpu/engine 발사 시 held-out mirror-DESCENT(a_clm_gen_pipeline) + CORE mount frozen-bar engine-native 재측정 + ckpt PULL(a_fire_recover_complete).
