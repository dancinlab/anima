# H_1627 — Tripartite-synapse astrocytic slow-calcium-field gating mouth

- **tier:** 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy, no engine); gpu_recipe = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** archbrainstorm — 84-family anima-native synthesis-binding architecture census (binding-wall program, H_1603)
- **lens:** bio-neuro (non-neuronal substrate): astrocyte calcium-wave gating of the tripartite synapse (Araque, Volterra); slow diffusing glial field as a dynamic coincidence-window setter — orthogonal substrate to all neuronal-pathway families.
- **artifacts:** `state/binding_arch_census/BRAINSTORM_INDEX.md`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1449 (attention-block INERT@1blk) · H_1602 (recombination-objective prereg)
- **key:** `astrocyte_calcium_field_bind`

## Mechanism

Add a NON-NEURONAL second field over the trunk: a slow, spatially-diffusing astrocytic calcium variable that integrates local neuronal coactivation over a longer timescale and a wider spatial footprint, then multiplicatively re-gates the fast feedforward stream (tripartite synapse: pre + post + glial). Two legs co-bind only if they fall inside the same astrocytic domain AND co-elevate its calcium within its slow window — the glial field acts as a dynamic, content-dependent coincidence window whose width is set by diffusion, not by a fixed kernel. The mouth output is the fast stream gated by the glial field's conjunction signal.

## Why it crosses the binding wall

Conv kernels and attention operate on ONE fast pathway at one timescale; the failure is that there is no separate slow variable to certify 'these two were jointly active in the same neighborhood.' The astrocytic field is a distinct substrate operating at a different timescale that supplies exactly a multiplicative conjunction gate the fast pathway cannot synthesize (a_substrate_disjoint: separate-lane binding survives). Ablation: clamp the glial field to a constant (or shrink diffusion length to 0 → per-channel, no spatial pooling) → the gate becomes content-independent and the mouth reverts to feedforward conv; binding must collapse, isolating the slow diffusing field as the causal binder.

## Cheap test (frozen-first · $0 · decisive numpy probe)

Frozen numpy: 2-leg spatial coincidence task on a 1D token line — target token must fire only when feature-A and feature-B appear within a window, regardless of order/position. Implement a tiny diffusing-field layer (Gaussian-smoothed product of two channels, slow EMA) vs param-matched conv. Pre-registered bar: conv ≤ 0.55 on held-out A,B placements; glial-gate ≥ 0.80, and ablation (diffusion length→0) must drop to conv level. Decision: no diffusion-length-dependent gap → drop. $0, CPU.

## GPU recipe (cost-gated · PRE-REGISTER ONLY · NOT fired)

PRE-REGISTER ONLY. 303M mouth: conv trunk + parallel astrocyte field (depthwise slow EMA + spatial diffusion conv) that multiplicatively gates the residual stream before the readout. Diffusion length & time-constant as learned scalars. Ablation arm: constant field. 4-cell balanced corpus, held-out CE. Engine-native frozen bars (G6 fals>0, G1 ≥ baseline) via cli/anima.hexa on CORE; constant-field ablation must FAIL. ~1 H100-day.

## Scope / honesty (c9)

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). gpu_recipe 발사 시(team-lead cost-gate go): held-out 4/4 mirror-CE DESCENT 게이트(a_clm_gen_pipeline) → CORE `--engine conv` mount 위 frozen G1(H_1129 recombination)·G6(H_1464 fals) byte-exact engine-native 재측정(torch probe 아님) → ckpt PULL before teardown(a_fire_recover_complete). cheap_test 가 numpy mirror 이므로 그 결과도 DIRECTIONAL(엔진-네이티브 아님).
