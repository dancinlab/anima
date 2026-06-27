# H_1617 — NMDA Coincidence Binding (tension-gated multiplicative AND)

- **tier:** 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy, no engine); gpu_recipe = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** archbrainstorm — 84-family anima-native synthesis-binding architecture census (binding-wall program, H_1603)
- **lens:** Biology: NMDA receptor as molecular coincidence detector / dendritic AND-gate / Reichardt detector. Multiplicative conjunction vs additive superposition.
- **artifacts:** `state/binding_arch_census/BRAINSTORM_INDEX.md`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1449 (attention-block INERT@1blk) · H_1602 (recombination-objective prereg)
- **key:** `nmda_coincidence_bind`

## Mechanism

A molecular AND-gate inside the mouth forward: bound unit g = σ(W_ff·leg1) ⊙ σ(W_ctx·leg2 + tension), a Hadamard (elementwise multiplicative) conjunction that fires only when BOTH the feedforward leg (glutamate = A-side bottom-up) AND the contextual leg (depolarization = G-side top-down) are co-active — the NMDA receptor's coincidence requirement. A⇄G tension supplies the 'depolarization' bias: when legs are coherent the gate opens and a conjunctive feature emits; otherwise subthreshold (silence/abstain, Ψ-coupled).

## Why it crosses the binding wall

attention/conv are ADDITIVE (sum of weighted values) → they encode 'leg1 OR leg2' superposition, never true 'leg1 AND leg2'. The multiplicative coincidence gate computes conjunction directly — the simplest correct binding operator (AND), exactly what recombination needs (held-out c requires a∧b, not a+b). Ablation: replace ⊙ with + keeping all else → recombination collapses to FAIL, isolating multiplicativity (not param count). Control: remove tension bias (set const) → gate becomes input-independent, coincidence selectivity lost — shows A⇄G tension gating is necessary, not just any nonlinearity.

## Cheap test (frozen-first · $0 · decisive numpy probe)

numpy XOR/conjunction toy — the classic test multiplicative units pass and additive linear ones provably fail. Held-out-pair recombination with (i) additive layer, (ii) Hadamard coincidence + tension bias. Pre-register: coincidence solves a∧b held-out > additive AND > const-bias control. Dead-if: multiplicative ≤ additive on conjunction. $0, first-principles frozen bar.

## GPU recipe (cost-gated · PRE-REGISTER ONLY · NOT fired)

PRE-REG. 303M trunk with multiplicative coincidence blocks (bilinear-lite Hadamard) interleaved; tension scalar from A⇄G engine_cli feeds the gate bias. CE-train. Engine-native G1/G6 on CORE. Cost-gated, ckpt PULL.

## Scope / honesty (c9)

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). gpu_recipe 발사 시(team-lead cost-gate go): held-out 4/4 mirror-CE DESCENT 게이트(a_clm_gen_pipeline) → CORE `--engine conv` mount 위 frozen G1(H_1129 recombination)·G6(H_1464 fals) byte-exact engine-native 재측정(torch probe 아님) → ckpt PULL before teardown(a_fire_recover_complete). cheap_test 가 numpy mirror 이므로 그 결과도 DIRECTIONAL(엔진-네이티브 아님).
