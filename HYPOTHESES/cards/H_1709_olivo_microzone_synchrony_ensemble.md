---
id: H_1709
slug: 1709_olivo_microzone_synchrony_ensemble
tier: 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
title: Olivo-cerebellar microzone array — synchrony-bound forward models at criticality
verdict: 🔵 PRE-REGISTERED architecture design (unmeasured) — $0 cheap_test pre-registered; engine-native + 303M gpu cost-gated NOT fired
source: brainarch_census
---

# H_1709 — Olivo-cerebellar microzone array — synchrony-bound forward models at criticality

- **tier:** 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy mirror, no engine); engine_native_measure + 303M = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** brainarch_census — 126-architecture whole-substrate (통짜 아키텍처) census: 뇌/인지 조직원리 × 엔진-네이티브 추상조건 (binding-wall program, H_1603).
- **key:** `olivo_microzone_synchrony_ensemble`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1280 (cerebellum forward-model) · H_1284 (neuromodulation gain) · operator-level family H_1604-1685 (this card = 통짜 아키텍처 layer, 층위 다름)

## Organizing principle

The olivo-cerebellar system is an array of microzones (microcomplexes), each a small forward model for one factor, coupled through the inferior olive's gap-junction network that synchronizes/desynchronizes their complex-spike timing. Binding is by SYNCHRONY (temporal co-firing of microzones for the same event); the climbing-fiber error clock gates plasticity and emission. Generation = the ensemble rolls forward in time; co-synchronized microzones bind their factors into one emitted event. The emit order parameter is ensemble synchrony, pinned to the edge of synchrony (criticality).

## Whole design (input → internal dynamics → emit)

N microzones, each a forward model FM_i (factor i) with phase phi_i. Inferior-olive coupling K synchronizes phases (Kuramoto-like); climbing-fiber error e_i desynchronizes (phase noise/reset). Synchrony order parameter R = |mean(e^{i phi})| in [0,1]. Input excites relevant microzones; their forward models roll out predicted consequences; synchrony-locked microzones co-fire a bound ensemble -> emit bound factors decoded onto V; unsynchronized stay silent. System held at the EDGE of synchrony (self-organized criticality, H_1228 precedent) for max sensitivity. Binding = which microzones synchronize together; recombination = a synchronized SET emits a combination none emits alone.

## Satisfies criteria (DESIGN claim · DIRECTIONAL · unmeasured)

G0: each microzone forward model decodes only onto V; synchronized emit = union of V-symbols on-manifold; desynchronized random-phase emit -> chance V-mass = native garble-control. G1: a synchronized SET emits factor-combos unreachable by any single microzone => super-additive; set K=0 (no co-fire) -> only single outputs -> composed_distinct->max_single = decisive INERT. G2: rollouts of synchronized ensembles reach corpus-absent combos within constraints; no-coupling control -> 0 joint-novel. Psi=1/2: IO coupling A (R up emit) vs climbing-fiber error G (R down silence); firing-rate homeostasis on K pins R to critical 1/2, attracting; delete coupling -> R->0 always silent, delete error -> R->1 always emit = boundary migration proving endogeneity. Honesty: a query no microzone can forward-predict -> high error everywhere -> no synchrony -> abstain; synchrony gate threshold frozen & microzone-count-independent (gate-perp-capacity). Binding: synchrony IS relational co-reference (Singer temporal binding); same-cause microzones phase-lock (true-pair R high) vs shuffle (R~0).

## Not-LLM (a_no_llm_frame_trap)

Coupled-oscillator dynamics + self-organized criticality + temporal binding — zero relation to attention/scale. Capacity scales by adding microzones, not parameters to a monolith; binding is a physical synchrony phenomenon, not a learned weight pattern. The boldest LLM-frame break (a_no_llm_frame_trap): generation is a dynamical phase-transition process and Psi=1/2 falls out of criticality rather than being a written setpoint.

## Cheap test (frozen-first · $0 · numpy mirror · DIRECTIONAL)

numpy Kuramoto: N=8 oscillators, coupling K with homeostatic adaptation, error noise e_i. (a) Psi: K-homeostasis drives R->~0.5 (edge); perturb R, measure contraction; K=0->R->0, kill error->R->1 (boundary endogeneity control). (b) binding: factor groups, same-cause inputs -> within-group phase-lock R high vs shuffle R~0, retrieval@1>>1/N. (c) G1: synchronized-set emit count vs single-microzone max; INERT when K=0. (d) honesty: unpredictable query -> all e_i high -> R below gate abstain; surrogate (shuffle supports) -> no synchrony selectivity. $0.

## Engine-native measure (cost-gated · PRE-REGISTER ONLY · NOT fired)

Microzone array as a core/*.hexa generator backend; synchronized-ensemble emit decodes via core/clm_decode.hexa onto V through cli/anima.hexa single dispatch. Psi=R maps directly to core/engine_cli.hexa A->G order parameter (IO-coupling=A, climbing-fiber-error=G) — self-restore measured natively. G0/G1/G2 via core/g_gates.hexa one-pass. synchrony-membership abstain via SS-ImmuneMemory analog. hexa<->py byte-parity on phase trajectories and emit decisions; SOC criticality is an anima precedent (H_1228), so engine-measurable not torch-only.

## Scope / honesty (c9)

## Distinction (near-overlap kept, not a dup)

Near-overlap with kuramoto cards + coherence_gated_broadcast (this census) — distinct: microzone forward-model BANK bound by inferior-olive synchrony at SOC criticality (H_1228 lens); the forward-model-per-microzone + olivary edge-of-sync is the differentiator.

8-oscillator numpy probe is a $0 decision test of synchrony-binding + criticality-Psi; chat-scale combinatorial content at 303M UNVERIFIED and the boldest scale risk (a_toy_scale_recheck, a_scale_honest_scope). Lane-tag: GPU/CE-substrate design, distinct from any AKIDA non-det trace (a_lane_akida_gpu_split). Production closure needs engine-native G0-G1-G2 on a mounted ckpt, ckpt pulled pre-teardown.

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). engine_native_measure 는 단일 진입점 cli/anima.hexa → generator L3 → g_gates/g6 경유 byte-parity 채점만 terminal; torch-only/side-harness 결과는 DIRECTIONAL. numpy cheap_test 결과도 DIRECTIONAL(엔진-네이티브 아님). gpu/engine 발사 시 held-out mirror-DESCENT(a_clm_gen_pipeline) + CORE mount frozen-bar engine-native 재측정 + ckpt PULL(a_fire_recover_complete).
