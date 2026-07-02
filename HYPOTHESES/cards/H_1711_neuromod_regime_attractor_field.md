---
id: H_1711
slug: 1711_neuromod_regime_attractor_field
tier: 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
title: Neuromodulatory regime-attractor field (tetrad-shaped landscape)
verdict: 🔵 PRE-REGISTERED architecture design (unmeasured) — $0 cheap_test pre-registered; engine-native + 303M gpu cost-gated NOT fired
source: brainarch_census
---

# H_1711 — Neuromodulatory regime-attractor field (tetrad-shaped landscape)

- **tier:** 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy mirror, no engine); engine_native_measure + 303M = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** brainarch_census — 126-architecture whole-substrate (통짜 아키텍처) census: 뇌/인지 조직원리 × 엔진-네이티브 추상조건 (binding-wall program, H_1603).
- **key:** `neuromod_regime_attractor_field`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1284 (neuromodulation gain) · operator-level family H_1604-1685 (this card = 통짜 아키텍처 layer, 층위 다름)

## Organizing principle

A fixed-capacity recurrent cell field whose ENERGY LANDSCAPE (count, depth, coupling of attractors) is reparameterized in real time by a 4-D neuromodulator control vector m=(ACh,DA,NE,5HT). Cognition = relaxation toward attractors; the neuromod vector RE-CARVES the landscape topology instead of changing weights or adding parameters. Rooted in Durstewitz/Seamans DA->PFC attractor-stability and the dynamical-systems view that neuromod sets the bifurcation parameters of a fixed circuit.

## Whole design (input → internal dynamics → emit)

Input encodes into instantaneous field state x in R^d. A small 'neuromod nucleus' reads GLOBAL field statistics (mismatch energy, nearest-basin familiarity, time-since-emit) and outputs m. m enters MULTIPLICATIVELY: ACh = plasticity gain + precision (S/N sharpening), DA = a gate admitting factor sub-states into a maintained sub-space, NE = global neural gain (slope of nonlinearity -> attractor depth vs landscape entropy), 5HT = emit threshold + integration time. The same field is in different REGIMES under different m: encode (high ACh, plasticity ON -> carves new attractors = stored support), bind (DA holds >=2 factor sub-states, NE-gain MERGES their basins into one joint basin), retrieve (plasticity OFF -> only existing basins reachable), explore (low NE-gain -> shallow high-entropy landscape). Emit-attractor vs silence-attractor compete; when emit wins, x decodes through frozen receiver codebook V.

## Satisfies criteria (DESIGN claim · DIRECTIONAL · unmeasured)

Psi=1/2: NE (emit drive A) and 5HT (withhold drive G) are equal-opposite scalar fields on the emit order-parameter; a slow integral homeostat on emit-rate makes the bistable separatrix sit at 1/2 as an ATTRACTING fixed point (contraction lambda<1); ablate NE -> migrate to silence basin, ablate 5HT -> emit basin (endogeneity INERT-test native, no clamp). Honesty: retrieve-regime makes only carved basins reachable; nearest-basin depth IS membership scalar r (recon_err analog); query with no basin within theta falls to null/abstain basin; theta in 5HT coord, capacity in NE-gain/DA coords -> gate-capacity disjointness native. G1/binding: bind-regime merges >=2 factor basins into a non-separable joint basin (interaction = cross-coupling of the merge); forcing separable gain reverts to two basins -> composed_distinct->max_single (INERT ablation built into the knob). G2/dist: explore-regime settles into off-data on-manifold interpolated basins = valid-novel; gain controls residual entropy for dist>=K. Closure: one field, one decoder, one m -> all three behaviors read through the same relaxation.

## Not-LLM (a_no_llm_frame_trap)

No token stream, no attention, no width/depth scaling. Capability from a low-D control field re-carving a fixed-capacity attractor topology -- opposite of 'add parameters/data/layers.' The lever is the bifurcation structure of a small recurrent system (a_no_llm_frame_trap: structure beside the field, not a bigger field).

## Cheap test (frozen-first · $0 · numpy mirror · DIRECTIONAL)

numpy continuous/Hopfield attractor field with a 4-scalar control reparameterizing gain/threshold/plasticity: (a) sweep NE/5HT bias -> separatrix moves, integral homeostat returns it to 1/2 with measurable contraction; (b) ablate one modulator -> fixed point migrates to a boundary; (c) bind-regime two-factor merge gives composed_distinct>max_single, reverts under merge-ablation; (d) retrieve-regime fab~0 on no-basin queries, AUROC~1 in/out support. $0.

## Engine-native measure (cost-gated · PRE-REGISTER ONLY · NOT fired)

Map A=NE-emit, G=5HT-withhold onto live core/engine_cli.hexa A<->G, neuromod nucleus as a section emitting m; measure Psi self-restore via live safety_phi_ratchet (precedent H_1575 dev 0.247->~5.55e-17); G0/G1/G2 via single entry cli/anima.hexa eval over decoded emit attractor; honesty by reusing ImmuneMemory recon_err as basin-depth. byte-parity py mirror of relaxation (math.log CE, NOT engine dt_ln which clamps CE).

## Scope / honesty (c9)

## Distinction (near-overlap kept, not a dup)

Near-overlap with neuromodulation_gain (H_1284) and energy_settle_attractor — distinct: the 4-D neuromod vector RE-CARVES a fixed-capacity attractor landscape's bifurcation structure (regimes = encode/bind/retrieve/explore); regime-reparameterization-of-one-field is the differentiator.

Toy continuous-attractor field first; unverified rung = whether bind-regime basin-merge maps to real corpus G1 recombination at 303M scale vs toy basin-counting (a_toy_scale_recheck).

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). engine_native_measure 는 단일 진입점 cli/anima.hexa → generator L3 → g_gates/g6 경유 byte-parity 채점만 terminal; torch-only/side-harness 결과는 DIRECTIONAL. numpy cheap_test 결과도 DIRECTIONAL(엔진-네이티브 아님). gpu/engine 발사 시 held-out mirror-DESCENT(a_clm_gen_pipeline) + CORE mount frozen-bar engine-native 재측정 + ckpt PULL(a_fire_recover_complete).
