# H_1605 — Two-Compartment Dendritic-AND Mouth (BAC / Ca-plateau coincidence)

- **tier:** 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy, no engine); gpu_recipe = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** archbrainstorm — 84-family anima-native synthesis-binding architecture census (binding-wall program, H_1603)
- **lens:** dendritic computation — BAC firing / apical Ca2+ plateau coincidence detection (Larkum); pyramidal two-compartment multiplicative gating.
- **artifacts:** `state/binding_arch_census/BRAINSTORM_INDEX.md`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1449 (attention-block INERT@1blk) · H_1602 (recombination-objective prereg)
- **key:** `dendritic_coincidence_gate`

## Mechanism

Each mouth unit is a two-compartment pyramidal model: a basal compartment receives leg-A (feedforward residual/token stream), an apical compartment receives leg-B (top-down trunk-summary/context state). Output (a 'burst') = basal_drive * plateau(apical_drive) — a thresholded Ca-plateau multiplicative AND with a coincidence window: the unit emits a strong burst only when both compartments are co-active in the same forward step, otherwise it passes a weak regular-spiking signal. The layer is a population of such Hadamard-bilinear units; logits read the burst code. Binding primitive = element-wise PRODUCT of the two streams (diagonal bilinear), per-unit conjunction.

## Why it crosses the binding wall

attention and conv outputs are additive in their values (a sum/convex-combination over value vectors), so they lie in the span of single-stream features and cannot represent the product term x_A o x_B without exponential width (parity/XOR lower bound for additive nets). The plateau multiply injects the cross-term directly. Ablation: linearize the gate (basal + apical instead of basal * plateau(apical), equal params) -> cross-term vanishes, collapses to attention-like additive -> G1/G6 fail. This isolates the MULTIPLY (not the parameter count) as the binding cause. Orthogonal to attention even though attention has multiplicative query.key — there the VALUE combination is still additive; here the content of the two streams is multiplied.

## Cheap test (frozen-first · $0 · decisive numpy probe)

numpy, DIRECTIONAL. Same factored 8x8 non-additive table + a parity task (target = A xor B, A,B in {0,1}^4). One hidden layer: gate = relu(Wa.A) o plateau(Wb.B) (Hadamard) vs additive = relu(Wa.A + Wb.B), equal params, linear readout, 25% held-out combos. Frozen bar: gate held-out CE < 0.3 nats AND additive >= 0.9x uniform; parity: gate reaches ~0 held-out bit-error, additive stuck ~0.5.

## GPU recipe (cost-gated · PRE-REGISTER ONLY · NOT fired)

PRE-REGISTER ONLY. 303M: replace every other trunk block's MLP with a two-compartment gated block (basal = residual stream, apical = trunk-summary state), burst = basal * plateau(apical) with a learned plateau threshold. CE-trained on 4-cell corpus; engine-native G1/G6 eval; bars frozen. ~$15; ckpt PULL.

## Scope / honesty (c9)

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). gpu_recipe 발사 시(team-lead cost-gate go): held-out 4/4 mirror-CE DESCENT 게이트(a_clm_gen_pipeline) → CORE `--engine conv` mount 위 frozen G1(H_1129 recombination)·G6(H_1464 fals) byte-exact engine-native 재측정(torch probe 아님) → ckpt PULL before teardown(a_fire_recover_complete). cheap_test 가 numpy mirror 이므로 그 결과도 DIRECTIONAL(엔진-네이티브 아님).
