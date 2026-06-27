# H_1640 — Conservative coupled-Hamiltonian orbit mouth (symplectic joint-invariant binding)

- **tier:** 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy, no engine); gpu_recipe = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** archbrainstorm — 84-family anima-native synthesis-binding architecture census (binding-wall program, H_1603)
- **lens:** classical mechanics / symplectic (volume-preserving) dynamics, contrasted with dissipative gradient settle; neural action-angle oscillator coupling
- **artifacts:** `state/binding_arch_census/BRAINSTORM_INDEX.md`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1449 (attention-block INERT@1blk) · H_1602 (recombination-objective prereg)
- **key:** `hamiltonian_symplectic_bind`

## Mechanism

Define H(q,p) = H_A(q_A,p_A) + H_B(q_B,p_B) + lambda*C(q_A,q_B), where leg-A initializes (q_A,p_A), leg-B initializes (q_B,p_B), and C is a bilinear coupling term. Evolve with a symplectic (leapfrog) integrator for K steps -- ENERGY-CONSERVING, no settling. The coupling C continuously exchanges action between the two oscillators, so A's orbit is modulated by B and vice versa; the bound code = a time-averaged / Poincare-section action vector that is a JOINT INVARIANT of both legs, fed to the byte head. Same A with different B -> different action exchange -> different invariant.

## Why it crosses the binding wall

Conservative coupling yields a conserved cross-action that is genuinely a function of the PAIR, and -- unlike dissipative energy_settle which collapses the input into one basin and discards 'which-with-which' -- symplectic flow PRESERVES a continuous family of bound states parameterized by both legs (no information thrown away to an attractor). ABLATION-1: lambda=0 (decouple) -> oscillators evolve independently -> any time-average factorizes into separate A and B statistics -> conjunction vanishes (pure superposition); the binding-vs-lambda curve is the proof. ABLATION-2: replace symplectic integrator with gradient descent on H -> reduces to energy_settle (dissipative) and loses the orbit-coupling invariant. Distinct from energy_settle (dissipative, fixed point) and DEQ (root-find): volume-preserving flow with no attractor.

## Cheap test (frozen-first · $0 · decisive numpy probe)

numpy leapfrog on a 2-oscillator coupled Hamiltonian (coupled pendula / Henon-Heiles-like), 4 A-inits x 4 B-inits. Time-averaged action features -> linear readout for conjunction; test held-out combos; sweep lambda (accuracy rises from chance at lambda=0). Frozen-first bar: held-out conjunction accuracy > additive [A;B] baseline AND > lambda=0 control. $0.

## GPU recipe (cost-gated · PRE-REGISTER ONLY · NOT fired)

PRE-REGISTER ONLY: mouth = symplectic-integrator block (learned quadratic H_A,H_B + bilinear coupling C from trunk projections), K~=10 leapfrog steps, time-pooled action vector -> byte head. 303M balanced 4-cell corpus + held-out val. Engine-native CORE-mount G1/G6 re-measure; ckpt PULL pre-teardown.

## Scope / honesty (c9)

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). gpu_recipe 발사 시(team-lead cost-gate go): held-out 4/4 mirror-CE DESCENT 게이트(a_clm_gen_pipeline) → CORE `--engine conv` mount 위 frozen G1(H_1129 recombination)·G6(H_1464 fals) byte-exact engine-native 재측정(torch probe 아님) → ckpt PULL before teardown(a_fire_recover_complete). cheap_test 가 numpy mirror 이므로 그 결과도 DIRECTIONAL(엔진-네이티브 아님).
