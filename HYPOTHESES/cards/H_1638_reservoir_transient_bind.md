# H_1638 — Echo-state reservoir transient-kernel mouth (fixed random recurrence Volterra binding)

- **tier:** 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy, no engine); gpu_recipe = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** archbrainstorm — 84-family anima-native synthesis-binding architecture census (binding-wall program, H_1603)
- **lens:** reservoir computing / liquid-state machine (Maass, Jaeger); biology = generic cortical microcircuit as a high-dim transient expander at edge-of-chaos
- **artifacts:** `state/binding_arch_census/BRAINSTORM_INDEX.md`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1449 (attention-block INERT@1blk) · H_1602 (recombination-objective prereg)
- **key:** `reservoir_transient_bind`

## Mechanism

A FIXED, UNTRAINED random recurrent reservoir of M>>d nonlinear units at spectral radius ~=1 (edge of chaos). Leg-A and leg-B are injected on two separate input-weight banks and the reservoir is driven for K steps. The reservoir's transient state is a fixed nonlinear (fading-memory Volterra) functional of the JOINT input history, so it automatically contains all cross-product terms A_i*B_j produced by recurrent nonlinear mixing over time. ONLY a linear readout is trained: the conjunction A(x)B already lives in the transient and the readout selects it. Binding requires no settling and no training of the recurrence.

## Why it crosses the binding wall

The universal-approximation property of ESN/LSM means an edge-of-chaos reservoir manufactures the full bilinear/Volterra product basis for FREE via temporal nonlinear feedback. conv/attention with trained shallow mixing do not synthesize the A_i*B_j cross-basis without an explicit bilinear op; the reservoir generates it as a side-effect of fading-memory recurrence. ABLATION-1: spectral radius -> 0 (kill recurrence -> pure feedforward random projection of [A;B]) -> transient cross-products vanish, only separate-leg linear features remain, binding collapses; the binding-vs-spectral-radius curve IS the proof. ABLATION-2: drive A and B on identical timestep with linear units (no temporal/nonlinear mixing) -> no product terms -> fails. Distinct from DEQ (no equilibrium solve) and energy_settle (readout uses the non-converged transient, never an attractor).

## Cheap test (frozen-first · $0 · decisive numpy probe)

numpy ESN, M=200, tanh, sweep spectral radius 0->1.2. Encode A,B as one-hot input streams; train linear readout for conjunction class on 16 (A,B) pairs, test held-out combos. Frozen-first bar: held-out conjunction accuracy peaks at edge-of-chaos and drops to chance at radius=0 (ablation), and beats a feedforward random-projection-of-concat baseline. $0.

## GPU recipe (cost-gated · PRE-REGISTER ONLY · NOT fired)

PRE-REGISTER ONLY: 303M trunk feeds a FROZEN random reservoir block (M~=4d, fixed edge-of-chaos) at the mouth; train only reservoir-readout + byte head (cheap, recurrence untrained), K=6 driven steps. Balanced 4-cell corpus + held-out val. Engine-native CORE-mount G1/G6 re-measure; ckpt PULL pre-teardown.

## Scope / honesty (c9)

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). gpu_recipe 발사 시(team-lead cost-gate go): held-out 4/4 mirror-CE DESCENT 게이트(a_clm_gen_pipeline) → CORE `--engine conv` mount 위 frozen G1(H_1129 recombination)·G6(H_1464 fals) byte-exact engine-native 재측정(torch probe 아님) → ckpt PULL before teardown(a_fire_recover_complete). cheap_test 가 numpy mirror 이므로 그 결과도 DIRECTIONAL(엔진-네이티브 아님).
