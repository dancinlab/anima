# H_1632 — Galois-closure concept-lattice binding mouth (FCA meet/join)

- **tier:** 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy, no engine); gpu_recipe = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** archbrainstorm — 84-family anima-native synthesis-binding architecture census (binding-wall program, H_1603)
- **lens:** lattice theory / Formal Concept Analysis — binding = Galois-closure to a formal concept (extent,intent); composition = conjunctive lattice meet (idempotent), not OR-pooling
- **artifacts:** `state/binding_arch_census/BRAINSTORM_INDEX.md`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1449 (attention-block INERT@1blk) · H_1602 (recombination-objective prereg)
- **key:** `galois_lattice_meet_bind`

## Mechanism

Borrow Formal Concept Analysis. One leg projects to an object/extent indicator set, the other to an attribute/intent indicator set (sparse sigmoid gates). The bind is the Galois closure: intent = attributes shared by ALL gated objects (a soft AND-pool over objects), extent = objects having ALL gated attributes (soft AND-pool over attributes); iterate the two derivation operators to a fixpoint = a formal concept, a closed (extent,intent) pair. Composition of concepts = lattice meet (∧ = intersection of intents), associative and idempotent, computed in one pass via 1–2 closure iterations.

## Why it crosses the binding wall

Conv/attention pool with OR-like weighted sums and cannot represent CONJUNCTIVE role-filler constraints — 'red AND square AND left' leaks, so red-square + blue-circle ≈ red-circle (precisely the recombination failure). The Galois closure is a meet/conjunction operator: a bound concept persists only if ALL its attributes hold, so distinct conjunctions stay distinct through depth, and idempotence (closure∘closure = closure) means no drift across layers. Recombination crosses because a novel attribute conjunction is just a new closed set in the same lattice — the closure operator generalizes to unseen meets by construction. Ablation: replace the AND-pool (min / log-product of gates) with the OR-pool (sum / softmax) used by attention → conjunctive separation collapses → recombination falls to baseline, isolating the meet (conjunction) as load-bearing.

## Cheap test (frozen-first · $0 · decisive numpy probe)

numpy, $0, frozen-first. Object×attribute binary context (8×8); train on a subset of attribute-conjunctions. Pre-registered bar: closure-bound representation linearly separates held-out attribute CONJUNCTIONS at ≥0.90 where an OR/softmax-pool control stays <0.60, AND closure is idempotent (closure∘closure − closure residual <1e-3). Decision: if meet-pool ≤ OR-pool OR idempotence fails, FALSIFIED.

## GPU recipe (cost-gated · PRE-REGISTER ONLY · NOT fired)

Cost-gated 303M, pre-register only. K closure layers: dual sparse-gate heads (extent/intent) + min/log-product AND-pool + 1–2 derivation iterations, residual back to stream (replacing attention's value sum). 4-cell corpus, held-out DESCENT, CORE-mount G1/G6, plus an idempotence-residual monitor (monitor-only). Pre-register bar; ckpt PULL before teardown.

## Scope / honesty (c9)

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). gpu_recipe 발사 시(team-lead cost-gate go): held-out 4/4 mirror-CE DESCENT 게이트(a_clm_gen_pipeline) → CORE `--engine conv` mount 위 frozen G1(H_1129 recombination)·G6(H_1464 fals) byte-exact engine-native 재측정(torch probe 아님) → ckpt PULL before teardown(a_fire_recover_complete). cheap_test 가 numpy mirror 이므로 그 결과도 DIRECTIONAL(엔진-네이티브 아님).
