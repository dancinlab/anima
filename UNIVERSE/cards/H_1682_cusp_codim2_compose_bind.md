# H_1682 — Codimension-2 Cusp-Catastrophe Mouth (two-control joint bifurcation)

- **tier:** 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy, no engine); gpu_recipe = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** archbrainstorm — 84-family anima-native synthesis-binding architecture census (binding-wall program, H_1603)
- **lens:** catastrophe theory / codimension-2 bifurcation (cusp normal form; distinct from heteroclinic-channel saddle sequencing)
- **artifacts:** `state/binding_arch_census/BRAINSTORM_INDEX.md`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1449 (attention-block INERT@1blk) · H_1602 (recombination-objective prereg)
- **key:** `cusp_codim2_compose_bind`

## Mechanism

Each mouth unit is the cusp normal form V(x)=¼x⁴+½a·x²+b·x with TWO control parameters: a=Wᴬh from leg-A, b=Wᴳh from leg-G. The unit output = the selected equilibrium x*(a,b) (root of x³+ax+b=0) settled in one forward via ~3 Newton steps; A⇄G tension drives the slow state across the cusp. The cusp set (where branch count changes) is the codim-2 locus 4a³+27b²=0 — reachable ONLY when a AND b jointly satisfy it. The catastrophic sheet-jump plus a hysteretic latch (which branch x* lands on) IS the bound event; readout maps sheet + jump magnitude to logits.

## Why it crosses the binding wall

conv/attention are locally smooth additive maps whose mixed second derivative can vanish (separable to first order); they cannot represent a SHARP branch-selection that depends on the joint product-structure of two controls — a single control only ever yields a fold, never a conjunction, because the cusp is intrinsically codim-2. The discontinuous sheet selection is the binding nonlinearity. ABLATION: clamp leg-G's b=0 (single control) → only a fold, x* becomes a smooth function of a alone → collapses to additive baseline → conjunction provably requires BOTH controls at the codim-2 locus.

## Cheap test (frozen-first · $0 · decisive numpy probe)

numpy cubic solver, $0. 2-bit XOR-hard conjunction: label = which sheet x* lands on for (a,b) sampled so each leg's marginal of a and of b is class-balanced (single-control provably at chance), but the joint sheet selection encodes XOR. Frozen bar: cusp sheet readout AUROC ≥0.90 on XOR; single-control (b=0) ablation ≤0.55. PASS iff cusp ≥0.90 AND single-control ≤0.60 over 1000 draws, with a hysteresis latch consistent with savant cusp-anneal precedent (H_1562, used here as substrate prior — note: binding mechanism, NOT inhibition).

## GPU recipe (cost-gated · PRE-REGISTER ONLY · NOT fired)

Pre-registration only (~1 H100, explicit go). Replace mid mouth nonlinearity with a bank of cusp units (a=Wᴬh, b=Wᴳh), 3 Newton settle steps, sheet+jump→readout, reusing savant §ThirdLaw cusp/latch wiring as substrate prior. 4-cell corpus, held-out CE-descent gate. Pre-register engine-native: two-control ON → G6 fals>0 AND G1≥baseline; single-control (b=0) ablation → FAIL. ckpt PULL before teardown.

## Scope / honesty (c9)

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). gpu_recipe 발사 시(team-lead cost-gate go): held-out 4/4 mirror-CE DESCENT 게이트(a_clm_gen_pipeline) → CORE `--engine conv` mount 위 frozen G1(H_1129 recombination)·G6(H_1464 fals) byte-exact engine-native 재측정(torch probe 아님) → ckpt PULL before teardown(a_fire_recover_complete). cheap_test 가 numpy mirror 이므로 그 결과도 DIRECTIONAL(엔진-네이티브 아님).
