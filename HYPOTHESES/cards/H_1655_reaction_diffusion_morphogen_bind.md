# H_1655 — Turing Reaction-Diffusion Morphogen Binding

- **tier:** 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy, no engine); gpu_recipe = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** archbrainstorm — 84-family anima-native synthesis-binding architecture census (binding-wall program, H_1603)
- **lens:** DYNAMICS — developmental morphogenesis (Turing differential-diffusion instability)
- **artifacts:** `state/binding_arch_census/BRAINSTORM_INDEX.md`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1449 (attention-block INERT@1blk) · H_1602 (recombination-objective prereg)
- **key:** `reaction_diffusion_morphogen_bind`

## Mechanism

Treat the two legs as source distributions of an activator field u (from h_A) and inhibitor field v (from h_B) over a small 1D/2D latent grid. Evolve the coupled PDE u̇ = D_u ∇²u + R(u,v,h_A), v̇ = D_v ∇²v + Q(u,v,h_B) with D_v ≫ D_u (differential diffusion) for T explicit steps. The emergent STABLE Turing pattern (spot/stripe morphology) is flattened and read out as the bound code; the conjunction lives in the nonlinear reaction term R coupling u and v.

## Why it crosses the binding wall

binding here = pattern SELECTION by a symmetry-breaking instability — intrinsically nonlinear and global; a small static conv stencil only does local linear filtering and cannot select which A-B spatial relation is the stable pattern. Distinct from traveling_wave_interference_bind (LINEAR superposition — no instability, no pattern selection) and from astrocyte_calcium_field_bind (a propagating signaling/gating field, NOT a differential-diffusion symmetry-breaking that spontaneously forms structure). ABLATION: set D_u=D_v (kill differential diffusion) → no Turing instability → uniform field → binding gone; linearize R (drop the u·v cross term) → no pattern forms → gone. Restore both → pass; isolates differential-diffusion + nonlinear coupling as the joint cause.

## Cheap test (frozen-first · $0 · decisive numpy probe)

numpy Gray-Scott / activator-inhibitor on a 16-cell ring; A and B as two feed/kill parameters. Fit a frozen linear probe on the steady pattern, then test whether the pattern class encodes the conjunction (e.g. XOR) of held-out (A,B) combos vs a linear-diffusion control (D_u=D_v). Pre-registered bar: conjunction-decode acc ≥ 0.70 with Turing ON and ≤ chance with the equal-diffusion control. $0.

## GPU recipe (cost-gated · PRE-REGISTER ONLY · NOT fired)

PRE-REGISTER ONLY (cost-gated 303M): small RD latent module (grid 32, T=10 explicit steps, learned reaction MLPs R/Q, fixed D_u ≪ D_v) bridging two trunk read-heads → flatten pattern → byte head. Train 4-cell corpus, held-out CE. Verdict = ckpt PULL → CORE --engine conv engine-native G1/G6; bar fals>0 ∧ recombine ≥ baseline.

## Scope / honesty (c9)

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). gpu_recipe 발사 시(team-lead cost-gate go): held-out 4/4 mirror-CE DESCENT 게이트(a_clm_gen_pipeline) → CORE `--engine conv` mount 위 frozen G1(H_1129 recombination)·G6(H_1464 fals) byte-exact engine-native 재측정(torch probe 아님) → ckpt PULL before teardown(a_fire_recover_complete). cheap_test 가 numpy mirror 이므로 그 결과도 DIRECTIONAL(엔진-네이티브 아님).
