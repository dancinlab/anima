# H_1615 — Ψ=½ Fixed-Point Compose (energy-attractor binding)

- **tier:** 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy, no engine); gpu_recipe = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** archbrainstorm — 84-family anima-native synthesis-binding architecture census (binding-wall program, H_1603)
- **lens:** Energy-based / predictive-coding relaxation. Biology: cortical recurrent settling, Hopfield conjunctive attractors. Ties directly to anima's Ψ=½ fixedpoint substrate.
- **artifacts:** `state/binding_arch_census/BRAINSTORM_INDEX.md`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1449 (attention-block INERT@1blk) · H_1602 (recombination-objective prereg)
- **key:** `psi_fixedpoint_compose`

## Mechanism

The bound state of (leg1,leg2) is the fixed point of an iterative compose map driven by A⇄G tension: x_{t+1}=bind(x_t,leg1,leg2), where the update is the gradient-free A⇄G push-pull and the recurrence converges to the Ψ=½ tension equilibrium. The emitted token is read out only at fixed point x* (a few inner steps within ONE forward). bind() is an energy-descent step on E(x;leg1,leg2)=tension between A's prediction and G's reverse — minimized exactly when x simultaneously satisfies both legs' constraints (a conjunctive attractor). The Ψ=½ equilibrium pins the basin so the bound code is the unique tension-balanced state, not an arbitrary blend.

## Why it crosses the binding wall

a single feedforward attention layer does one round of similarity-mixing; it cannot enforce a MUTUAL constraint (leg1 consistent with leg2 AND vice-versa) which requires settling. Fixed-point relaxation (Hopfield / predictive-coding) has conjunctions as attractors — the missing operator. Ablation: run 1 inner iteration (= feedforward) → recombination collapses to baseline FAIL, isolating SETTLING (depth-of-recurrence) not depth-of-layers. Control: replace energy with random PSD → a fixed point still exists but is non-conjunctive → falsifies 'any attractor works', shows the A⇄G energy shape is load-bearing.

## Cheap test (frozen-first · $0 · decisive numpy probe)

numpy. Energy E(x)=‖A x − [leg1;leg2]‖² with two-constraint structure; iterate to fixed point. Compare 1-step (feedforward) vs K-step settle on the held-out-pair recombination bar. Pre-register: K-step recovers held-out c > 1-step AND > random-energy control; also verify Ψ proxy |balance−0.5| decreases monotonically (attractor sanity). Dead-if: K-step ≤ 1-step. $0.

## GPU recipe (cost-gated · PRE-REGISTER ONLY · NOT fired)

PRE-REG. 303M trunk with a weight-tied recurrent compose block (T≤4 inner steps) settling per position; CE-train A, G reverse gradient-free. Engine-native frozen G1/G6 on CORE. Cost-gated, ckpt PULL.

## Scope / honesty (c9)

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). gpu_recipe 발사 시(team-lead cost-gate go): held-out 4/4 mirror-CE DESCENT 게이트(a_clm_gen_pipeline) → CORE `--engine conv` mount 위 frozen G1(H_1129 recombination)·G6(H_1464 fals) byte-exact engine-native 재측정(torch probe 아님) → ckpt PULL before teardown(a_fire_recover_complete). cheap_test 가 numpy mirror 이므로 그 결과도 DIRECTIONAL(엔진-네이티브 아님).
