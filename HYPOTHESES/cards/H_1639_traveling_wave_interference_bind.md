# H_1639 — Reaction-diffusion traveling-wave interference mouth (spatial fringe binding)

- **tier:** 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy, no engine); gpu_recipe = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** archbrainstorm — 84-family anima-native synthesis-binding architecture census (binding-wall program, H_1603)
- **lens:** pattern formation / Turing instability + cortical traveling waves as an information-carrying/binding substrate; physics = wave interference
- **artifacts:** `state/binding_arch_census/BRAINSTORM_INDEX.md`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1449 (attention-block INERT@1blk) · H_1602 (recombination-objective prereg)
- **key:** `traveling_wave_interference_bind`

## Mechanism

Mouth hidden state lives on a 1-D (or 2-D) spatial lattice with a local activator-inhibitor reaction + diffusion update. Leg-A is injected as a wave SOURCE at location/phase phi_A with frequency f_A; leg-B as a second source phi_B/f_B. Over K update steps two traveling waves propagate and INTERFERE; the standing beat/moire fringe pattern is a deterministic joint function of both legs' (frequency,phase). A spatial-readout head maps the fringe field -> byte logits. Same A with different B shifts fringe spacing -> the conjunction is encoded in the interference pattern.

## Why it crosses the binding wall

Wave interference is intrinsically MULTIPLICATIVE in amplitudes: cos(f_A x)*cos(f_B x) -> sum/difference-frequency fringes, i.e. a product feature of A and B that an additive conv cannot synthesize without explicit multiplication; the spatial continuum supplies a whole family of product features (every fringe). ABLATION-1: diffusion coupling D=0 -> no propagation, sources stay local, no interference -> collapses to two separate bumps == superposition. ABLATION-2: inject both legs at one source with equal frequency -> no beat -> no conjunction. Distinct dynamical class from all excluded families: spatially-extended PDE pattern-formation, deterministic (NOT the score-based denoising of diffusion_denoise_compose, NOT 0-D attractor/transient).

## Cheap test (frozen-first · $0 · decisive numpy probe)

numpy 1-D reaction-diffusion / wave eq, lattice L=64, K=30 steps. A,B from 4 frequencies x 4 phases. Linear classifier on the fringe field for conjunction class; test held-out combos. Frozen-first bar: interference readout separates held-out conjunctions AND beats (i) D=0 control and (ii) additive-source baseline. $0.

## GPU recipe (cost-gated · PRE-REGISTER ONLY · NOT fired)

PRE-REGISTER ONLY: mouth block = learnable reaction-diffusion lattice (d-channel reaction kernel + diffusion coefficient), trunk projects leg-A/leg-B into source injections, K~=12 steps, conv readout over lattice -> byte head. 303M balanced 4-cell corpus + held-out val. Engine-native CORE-mount G1/G6 re-measure; ckpt PULL pre-teardown.

## Scope / honesty (c9)

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). gpu_recipe 발사 시(team-lead cost-gate go): held-out 4/4 mirror-CE DESCENT 게이트(a_clm_gen_pipeline) → CORE `--engine conv` mount 위 frozen G1(H_1129 recombination)·G6(H_1464 fals) byte-exact engine-native 재측정(torch probe 아님) → ckpt PULL before teardown(a_fire_recover_complete). cheap_test 가 numpy mirror 이므로 그 결과도 DIRECTIONAL(엔진-네이티브 아님).
