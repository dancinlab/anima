# H_1653 — Coupled Neural-ODE Continuous-Flow Binding

- **tier:** 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy, no engine); gpu_recipe = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** archbrainstorm — 84-family anima-native synthesis-binding architecture census (binding-wall program, H_1603)
- **lens:** DYNAMICS — continuous-depth dynamical systems (non-conservative Neural-ODE flow)
- **artifacts:** `state/binding_arch_census/BRAINSTORM_INDEX.md`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1449 (attention-block INERT@1blk) · H_1602 (recombination-objective prereg)
- **key:** `neural_ode_coupled_flow_bind`

## Mechanism

Mouth projects the two legs to an initial latent z(0)=enc(h_A) and integrates a LEARNED non-conservative vector field dz/dt = f_theta(z,t) over t in [0,1] with a fixed solver (RK4, ~6-8 function evals). f_theta carries an explicit bilinear cross term, e.g. f = W z + phi(z) * (h_A ⊙ U h_B), so the two legs continuously co-modulate the same trajectory. The endpoint z(1) is the bound representation feeding the byte head. Binding is the ACCUMULATED nonlinear A×B interaction along the integrated path — an effectively infinite-depth weight-tied nonlinear mixing — rather than one static op.

## Why it crosses the binding wall

conv/attention apply a fixed finite stack of static linear+pointwise ops; they cannot represent the iterated multiplicative composition that an integrated flow builds up infinitesimally. Distinct from hamiltonian_symplectic_bind (that flow is CONSERVATIVE/oscillatory — energy-preserving, no dissipative selection) and from energy_settle_attractor (pure gradient descent on a scalar Lyapunov energy — cannot express rotational / path-dependent binding that a general non-gradient vector field can). ABLATION: (a) zero the cross term → field factorizes into independent A-flow + B-flow, endpoint = sum of marginals → fals/recombination collapse; restore → recover. (b) collapse integration steps 8→1 (single residual block ≈ attention) → binding lost while parameters unchanged → proves it is the continuous flow, not the weights.

## Cheap test (frozen-first · $0 · decisive numpy probe)

numpy mini, d=32 toy: two factor variables (role one-hot ⊗ filler one-hot) as the two legs. Explicit Euler integrate dz/dt = W z + (h_A ⊙ U h_B) for N steps; fit only a linear decoder on COMBINATIONS SEEN, then test held-out role×filler combos never seen together. Pre-registered frozen bar: decode-acc on novel conjunctions with N=8 minus N=1 ≥ 0.15 AND N=8 beats an additive (h_A+h_B) baseline by ≥0.15. Decision probe, $0.

## GPU recipe (cost-gated · PRE-REGISTER ONLY · NOT fired)

PRE-REGISTER ONLY (cost-gated 303M): replace top k trunk blocks with one weight-tied ODE cell (RK4, 6-8 func evals) whose vector field bilinearly couples two learned sequence read-projections; train on 4-cell balanced corpus (a_chat_registers) with held-out CE monitor. Verdict = ckpt PULLED + mounted on CORE --engine conv, engine-native G1/G6 re-measure; frozen bar = G6 fals>0 AND G1 recombine ≥ bytegpt/convmoe baseline.

## Scope / honesty (c9)

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). gpu_recipe 발사 시(team-lead cost-gate go): held-out 4/4 mirror-CE DESCENT 게이트(a_clm_gen_pipeline) → CORE `--engine conv` mount 위 frozen G1(H_1129 recombination)·G6(H_1464 fals) byte-exact engine-native 재측정(torch probe 아님) → ckpt PULL before teardown(a_fire_recover_complete). cheap_test 가 numpy mirror 이므로 그 결과도 DIRECTIONAL(엔진-네이티브 아님).
