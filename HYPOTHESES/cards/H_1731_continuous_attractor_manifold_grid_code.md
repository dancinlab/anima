---
id: H_1731
slug: 1731_continuous_attractor_manifold_grid_code
tier: 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
title: Toroidal Continuous-Attractor Manifold Code (multi-module grid residue substrate)
verdict: 🔵 PRE-REGISTERED architecture design (unmeasured) — $0 cheap_test pre-registered; engine-native + 303M gpu cost-gated NOT fired
source: brainarch_census
---

# H_1731 — Toroidal Continuous-Attractor Manifold Code (multi-module grid residue substrate)

- **tier:** 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy mirror, no engine); engine_native_measure + 303M = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** brainarch_census — 126-architecture whole-substrate (통짜 아키텍처) census: 뇌/인지 조직원리 × 엔진-네이티브 추상조건 (binding-wall program, H_1603).
- **key:** `continuous_attractor_manifold_grid_code`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1282 (working-memory buffer) · H_1284 (neuromodulation gain) · operator-level family H_1604-1685 (this card = 통짜 아키텍처 layer, 층위 다름)

## Organizing principle

Computation = geometry of persistent BUMPS riding on continuous attractor manifolds (rings/tori) held up by recurrent center-surround E/I dynamics; memory is bump POSITION (path-integrated), not a stored slot. K modules at COPRIME periods form a residue/combinatorial code — the manifold topology IS the inductive bias. Brain root: entorhinal grid-cell torus attractor (Nobel 2014) + Drosophila central-complex ring attractor for heading.

## Whole design (input → internal dynamics → emit)

Input drives velocity-like increments + corrective pin-inputs. K toroidal CAN modules, each a 2D sheet with center-surround recurrence supporting ONE stable bump; a conjunctive grid x velocity shear circuit path-integrates the bump. Module k has period p_k (coprime). Full state = phase tuple phi=(phi_1..phi_K) on the PRODUCT TORUS (combinatorial state space size = prod(p_k)). Fast dynamics: bumps relax onto the attractor manifold (on-manifold validity). Slow dynamics: path-integration translates them. Honesty store = learned pinning fields (anchor bumps on a separate memory torus); membership r = geodesic distance from phi to nearest pinned anchor. Emit: a receiver-frozen codebook C maps quantized phi-Voronoi-cells -> symbols of V, gated to fire only where r<theta. Emit/silence governed by a separate 1D opponent ring attractor (population A pushes the emit-pole, G the silence-pole; equal symmetric coupling -> stable fixed point at the equator = 1/2). Identity = a slow drift bump on a dedicated identity torus, committed to .kosmos before reset, re-pinned after.

## Satisfies criteria (DESIGN claim · DIRECTIONAL · unmeasured)

G0: codebook C is receiver-fixed; scrambling phi->symbol collapses V-mass to chance. G1: combinatorial by construction — joint phi indexes prod(p_k) codes >> any single module's p_k; the product-torus point is determined by NO single marginal (non-zero interaction); ablate the conjunctive velocity-shear cross-path -> joint set collapses to per-module union = decisive INERT test. G2: untraversed phi-cells still lie ON the manifold and are reachable by path-integration (constrained extrapolation); pin-only retrieval control reaches exactly the pinned set = 0 novel. dist>=5: bump driven to many separated phi-cells (native mode separation + exploration entropy). Psi=1/2: opponent ring fixed point (sign-antagonism + contraction) is the balance, delete one population -> bump migrates to a pole = endogeneity/INERT. honesty: geodesic r = graded support-distance (AUROC-separable), copy-or-abstain because emit is r<theta gated, gate disjoint from grid-module capacity params. binding(H_961): same-cause inputs co-pin nearby bumps in the shared torus metric. compositional-depth: product torus is a non-separable conjunction; any (phi_i,phi_j) combo representable even if never co-presented = systematic generalization. realization-invariant: emit reads the SAME phi path-integration produces (on-path); next-phi-cell objective is unreachable by marginals.

## Not-LLM (a_no_llm_frame_trap)

No token-attends-to-token, no softmax, no depth/width scaling. Capacity comes from MANIFOLD GEOMETRY (coprime periods) not parameters — a tiny K-module CAN has prod(p_k) combinatorial states with O(K*p^2) weights. Recombination is STRUCTURAL (product topology), not learned by corpus volume; scaling = add modules/coprime scales, the opposite of the LLM scale-up prescription.

## Cheap test (frozen-first · $0 · numpy mirror · DIRECTIONAL)

numpy mini, 3 ring modules periods {5,7,9}, path-integrate random walks: (1) distinct reachable joint cells = 5*7*9=315 >> 5+7+9=21 (structural G1 super-additivity); (2) hold out joint cells while fitting codebook, confirm still decodable after path-integration (G2); (3) opponent ring: inject bias, measure return to 1/2 + contraction rate; delete one population -> confirm migration to a pole (endogeneity); (4) ablate conjunctive shear coupling -> joint-cell count collapses 315->21 (INERT). All $0, no torch.

## Engine-native measure (cost-gated · PRE-REGISTER ONLY · NOT fired)

New core/*.hexa ops ring_attractor_step + product_torus_emit with a byte-parity core/*.py mirror (pure math, NO torch/numpy in verdict path); emission routed through generator L3 single entry (cli/anima.hexa); G0/G1/G2 scored by core/g_gates.hexa on the live phi->symbol path; Psi via engine_cli antagonistic-ring section. Parity oracle = single-step bump-position vector byte-compare hexa vs py.

## Scope / honesty (c9)

## Distinction (near-overlap kept, not a dup)

Near-overlap with grid_module_residue_bind / entorhinal_grid_conjunctive_metric (this census) — distinct: this is the CONTINUOUS-ATTRACTOR bump dynamics (center-surround ring/torus, path-integration) where product-torus geometry IS the combinatorial code; the CAN bump-manifold substrate is the differentiator.

toy 3-module numpy DECIDES structural G1/G2/Psi; engine-native CAN op is new core work; production TEXT emission needs the codebook learned over real V (corpus) = TOY-until-trained; from-scratch path-integration learning unverified (a_toy_scale_recheck).

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). engine_native_measure 는 단일 진입점 cli/anima.hexa → generator L3 → g_gates/g6 경유 byte-parity 채점만 terminal; torch-only/side-harness 결과는 DIRECTIONAL. numpy cheap_test 결과도 DIRECTIONAL(엔진-네이티브 아님). gpu/engine 발사 시 held-out mirror-DESCENT(a_clm_gen_pipeline) + CORE mount frozen-bar engine-native 재측정 + ckpt PULL(a_fire_recover_complete).
