# H_1617 — NMDA Coincidence Binding (tension-gated multiplicative AND)

- **tier:** 🟠 DIRECTIONAL toy-SUPPORT (variance-caveat) — torch toy ARM 측정됨(EXP-3 precursor), engine-native/303M 아님
- **wired:** DIRECTIONAL-mirror (torch toy measured; NOT engine-native). cheap_test = $0 numpy screen (Hadamard 1.00 vs additive 0.50 증명적); **toy ARM (NEW, 2026-06-27)** = 학습 trunk(d256/L4) 위 3-arm 측정 SUPPORT(mean bar) — 아래 §Toy ARM result; gpu_recipe(303M EXP-3) = 여전히 cost-gated, NOT fired.
- **source:** archbrainstorm — 84-family anima-native synthesis-binding architecture census (binding-wall program, H_1603)
- **lens:** Biology: NMDA receptor as molecular coincidence detector / dendritic AND-gate / Reichardt detector. Multiplicative conjunction vs additive superposition.
- **artifacts:** `state/binding_arch_census/BRAINSTORM_INDEX.md` · `state/binding_arch_census/exp3_arm/` (PREREG.md · trainer.py · RESULT.md · RESULT.json · ckpt/{ctrl,bind,bind_linear}_seed{7,4302,4303}.pt)
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

## Toy ARM result (NEW · 2026-06-27 · DIRECTIONAL torch toy · summer RTX5070 GPU 93% util)

학습 trunk(causal Transformer d256/L4/H4, block11) 위 3-arm 측정, compositional 재조합 task
(scene=3 obj × (8 shape, 8 color), query 결합 존재여부; 12 held-out conjunction = seen parts 의 novel
결합). **HARD split** = illusory-conjunction balanced(양=object (Qs,Qc) 존재, 음=Qs·Qc 가 *따로* 존재하나
object 없음; marginal 동일 → 덧셈 pooled rep 으로 증명적 구분불가). seeds {7,4302,4303}, steps 4000.

| arm | HARD acc mean (std) | per-seed |
|-----|---------------------|----------|
| ctrl (plain linear readout) | 0.778 (0.208) | [0.999, 0.500, 0.835] |
| **bind (Hadamard ⊙)** | **0.988 (0.016)** | [1.000, 0.965, 1.000] |
| bind_linear (⊙→+, param-matched) | 0.828 (0.232) | [0.999, 0.500, 0.984] |

- frozen bar: `bind−ctrl=0.210 ≥0.15` ∧ `bind−linear=0.161 ≥0.15` → **mean SUPPORT**; seed-consistency **1/3**.
- **해석(정직):** lift = multiplicativity 의 *robustness* 이지 trunk 가 못하던 능력 아님. attention trunk 는
  additive readout 으로도 *때때로* pre-bind(ctrl seed7 0.999) 하나 **불안정(seed4302 chance 0.50 붕괴)**.
  bind_linear(param 동일, +)도 동일하게 붕괴 → 추가 head/param 아님. **Hadamard ⊙ 만 3/3 robust** =
  param-matched ablation(⊙ vs +)이 multiplicativity 를 robustness 의 원인으로 격리(이 카드의 ⊙→+ ablation 예측 확인).
- numpy screen 의 additive 0.50-증명적 collapse 는 trunk-less 였기 때문; 학습 trunk 가 끼면 additive 도 *가끔* 넘되
  Hadamard 가 그걸 *신뢰성 있게* 만든다. 상세 = `state/binding_arch_census/exp3_arm/RESULT.md`.

## Scope / honesty (c9)
toy ARM = **DIRECTIONAL torch screen**(engine-native 아님 · 303M 아님 · `a_engine_native_learning`/`a_toy_scale_recheck`).
SUPPORT 는 *mean bar* 충족이되 seed-consistency 1/3 = robustness-driven(과장 금지). 303M EXP-3 decider(G1∧G6
co-movement engine-native)는 별개 미발사. toy-only, scale-transfer UNVERIFIED — 303M 은 권고만(자동발사 금지).


설계만 — 측정 0. tier = 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). gpu_recipe 발사 시(team-lead cost-gate go): held-out 4/4 mirror-CE DESCENT 게이트(a_clm_gen_pipeline) → CORE `--engine conv` mount 위 frozen G1(H_1129 recombination)·G6(H_1464 fals) byte-exact engine-native 재측정(torch probe 아님) → ckpt PULL before teardown(a_fire_recover_complete). cheap_test 가 numpy mirror 이므로 그 결과도 DIRECTIONAL(엔진-네이티브 아님).
