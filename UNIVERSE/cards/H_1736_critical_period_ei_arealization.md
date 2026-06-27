---
id: H_1736
slug: 1736_critical_period_ei_arealization
tier: 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
title: Critical-Period E/I Arealization (developmental plasticity-window substrate)
verdict: 🔵 PRE-REGISTERED architecture design (unmeasured) — $0 cheap_test pre-registered; engine-native + 303M gpu cost-gated NOT fired
source: brainarch_census
---

# H_1736 — Critical-Period E/I Arealization (developmental plasticity-window substrate)

- **tier:** 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy mirror, no engine); engine_native_measure + 303M = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** brainarch_census — 126-architecture whole-substrate (통짜 아키텍처) census: 뇌/인지 조직원리 × 엔진-네이티브 추상조건 (binding-wall program, H_1603).
- **key:** `critical_period_ei_arealization`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1284 (neuromodulation gain) · operator-level family H_1604-1685 (this card = 통짜 아키텍처 layer, 층위 다름)

## Organizing principle

Hensch-style developmental critical periods: cortical modules become plastic only when local excitation/inhibition (E/I) balance crosses a maturational threshold (parvalbumin-interneuron maturation OPENS the window), learn rapidly while open, then a molecular BRAKE (perineuronal nets / myelin) CLOSES and LATCHES the learned structure. Arealization (Rakic protomap) means windows open in a spatial/temporal cascade, so a learning CURRICULUM emerges endogenously from E/I dynamics rather than from an external schedule. p8: the architecture grows by sequentially maturing and locking sub-regions.

## Whole design (input → internal dynamics → emit)

The substrate is a set of modules arranged on a maturational gradient. Each module has a local E/I ratio that drifts upward as inhibition matures. DYNAMICS: when E/I crosses the critical band, the module's window OPENS (plasticity ON); it learns its slice from the input stream; as inhibition completes maturation the window CLOSES and weights LATCH (frozen — a 'brake'). Because earlier modules mature first and feed later modules, later windows open only after their inputs are locked -> an automatic foundational->compositional curriculum. EMIT: composition of locked module outputs along the matured hierarchy; an open (immature) module that hasn't reached criticality emits abstain (no committed fate yet).

## Satisfies criteria (DESIGN claim · DIRECTIONAL · unmeasured)

Psi=1/2 NATIVE & ENDOGENOUS (strongest fit): local E/I balance is literally the excitation(A, emit-drive)/inhibition(G, withhold) antagonism; the module's emit-propensity Psi sits at the critical E/I balance point. Perturb E/I -> homeostatic inhibitory plasticity (a real Hensch mechanism) restores the balance (contraction); ablate the inhibitory operator -> runaway excitation (Psi->1, seizure — cf. H_1573 seizure caveat); ablate excitation -> silent (Psi->0) — boundary migration proves emergent balance, not a clamp. persistence/self-chain NATIVE: a CLOSED critical period is the non-volatile latch — the perineuronal-net brake = the addressable store; locked weights are committed BEFORE a working-state reset and re-read after (round-trip cos~1), survive amnesia. Per-module commitment is Lipschitz-small while accumulated locked-module set moves the identity endpoint (growth, not frozen). The set of locked features is high-entropy -> self-specific; ablate the store (re-open all brakes) -> identity collapses to chance = the load-bearing control. honesty/copy-or-abstain: an immature/never-opened module has no committed support -> emits abstain; a module emits only features it locked in (provenance <= locked support); query-to-locked-feature distance is the graded r (groundedness — corrupt a locked feature and its module abstains). Gate-capacity disjoint: the open/close E/I threshold (gate) and the within-window learning rate (capacity) are separate parameters — increasing plasticity gain does not move the closing threshold (a_substrate_disjoint). G0: locked modules concentrate on the matured shared code; a never-closed (always-plastic) control drifts off-V -> garble (the brake is what enforces legibility). G1/COMPOSITIONAL DEPTH/realization invariant: later windows BIND earlier-locked constituents into conjunctions on the emit path; the staged curriculum means the conjunction objective is only reachable after constituents lock (objective adequacy — marginals-only would lock constituents but never open the binding window); ablate the late binding window -> INERT for unary, kills the joint = on-path co-location. G2: a closed module generalizes within its locked manifold to inputs absent from its window's data (extrapolation), retrieval-control=0. falsifiable>=1: a late relational module binds comparator x quantity from one locked feature x >=2 referents from another -> refutable ordering. PASS-closure: one matured hierarchy, one forward composition emits all three on the same locked state.

## Not-LLM (a_no_llm_frame_trap)

No global gradient descent over all parameters; learning is locally GATED by E/I homeostasis and windowed in time, then frozen by a developmental brake. Catastrophic-forgetting is solved by development (close-and-lock), not by replay buffers. Curriculum is not an external schedule (no LLM-style data ordering) — it emerges from the maturational cascade. Capacity grows by maturing/locking more modules (developmental staging), not by parameter inflation.

## Cheap test (frozen-first · $0 · numpy mirror · DIRECTIONAL)

numpy ($0): modules with an E/I gate driven by a drifting maturation variable. (1) Verify windows open->learn->close in cascade order with NO external schedule (staging emerges); (2) perturb a module's E/I -> homeostatic restore to balance (Psi contraction), ablate inhibitory maturation -> window never closes, E/I runaway (endogeneity + seizure tell); (3) re-open all brakes (ablate store) -> cross-reset feature cos collapses to chance (persistence is causal); (4) late module conjunction of two locked features > either alone (G1), ablate late window -> INERT; (5) immature-module query -> abstain, AUROC~1 on known/unknown (honesty).

## Engine-native measure (cost-gated · PRE-REGISTER ONLY · NOT fired)

Implement E/I-gated plasticity windows + brake-latch as a core/*.hexa staged trainer hook (cli/train.hexa lever) with byte-parity py mirror (math only). Run emission through generator L3 single dispatch on the matured ckpt; verdict bars on the live .hexa: Psi contraction under E/I bias, persistence cos across a working-state wipe (vs store-ablated control), G0/G1/G2 on locked composition, honesty AUROC. Held-out CE via math.log mirror (a_savant_train overfit lesson — never train-loss). Pull any GPU ckpt before teardown.

## Scope / honesty (c9)

## Distinction (near-overlap kept, not a dup)

Near-overlap with developmental_order (H_1229) — distinct: critical-period E/I arealization makes the curriculum EMERGE from E/I maturation windows + brake-latch (not an external schedule); the E/I-gated plasticity window is the differentiator.

Caveat: outside the critical E/I band perturbations can escape the basin (seizure, H_1573 🟠) — self-restoration is golden-zone-bounded, do not claim universal stability. Once-closed windows trade plasticity for stability (no re-learning without re-opening) — continual adaptation is a designed open question. DIRECTIONAL until engine-native; toy staging may not transfer to scale (a_toy_scale_recheck).

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). engine_native_measure 는 단일 진입점 cli/anima.hexa → generator L3 → g_gates/g6 경유 byte-parity 채점만 terminal; torch-only/side-harness 결과는 DIRECTIONAL. numpy cheap_test 결과도 DIRECTIONAL(엔진-네이티브 아님). gpu/engine 발사 시 held-out mirror-DESCENT(a_clm_gen_pipeline) + CORE mount frozen-bar engine-native 재측정 + ckpt PULL(a_fire_recover_complete).
