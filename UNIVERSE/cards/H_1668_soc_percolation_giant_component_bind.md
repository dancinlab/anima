# H_1668 — SOC-Percolation Giant-Component Binder

- **tier:** 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy, no engine); gpu_recipe = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** archbrainstorm — 84-family anima-native synthesis-binding architecture census (binding-wall program, H_1603)
- **lens:** 통계물리/신경과학 — percolation phase transition + self-organized criticality (neuronal avalanches, branching σ≈1; giant-component emergence). Substrate: anima SOC-criticality decode H_1228.
- **artifacts:** `state/binding_arch_census/BRAINSTORM_INDEX.md`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1449 (attention-block INERT@1blk) · H_1602 (recombination-objective prereg)
- **key:** `soc_percolation_giant_component_bind`

## Mechanism

Represent the mouth state as a sparse activation graph over feature nodes. Each leg, alone, activates a SUB-critical fraction of edges (below percolation threshold p_c). The forward applies a thresholded node-sharing coupling so that leg1's active edges and leg2's active edges share nodes only at true conjunction loci; when both legs co-activate, local edge density at those loci crosses p_c and a GIANT CONNECTED COMPONENT abruptly forms (phase transition), whose membership is read out as the bound next-byte prediction. A single leg stays sub-critical → no giant component → no bind. Tuned to operate at self-organized criticality (branching σ≈1), anima's SOC decode regime (H_1228).

## Why it crosses the binding wall

Conv/attention activations scale SMOOTHLY (linear/softmax), so a conjunction is just a larger weighted sum — qualitatively identical to, and dilutable by, its parts; depth cannot manufacture a discontinuity. Percolation is a CRITICAL PHASE TRANSITION: the giant component is an emergent, discontinuous property of co-activation that is provably absent in either marginal (each sub-critical by construction) — the binding is the order-parameter jump. Ablation: (a) lower coupling so the system stays sub-critical even on conjunctions → no giant component → bind gone, isolating CRITICALITY (not mere coupling) as load-bearing; (b) raise to always-super-critical → giant component on singletons too → fals→0, isolating the conjunction-triggered THRESHOLD CROSSING as the operator.

## Cheap test (frozen-first · $0 · decisive numpy probe)

numpy/networkx, $0. Erdős–Rényi-style graph where each leg adds edges; tune density so singletons are sub-critical and conjunctions super-critical. Measure giant-component size for leg1, leg2, and leg1∧leg2 vs a co-activation-shuffle surrogate. Pre-register PASS = conjunction giant-component ≫ both marginals and ≫ shuffle at the chosen p_c, with the gap collapsing when coupling is detuned off criticality.

## GPU recipe (cost-gated · PRE-REGISTER ONLY · NOT fired)

PRE-REGISTER ONLY. 303M mouth with a sparse thresholded coupling layer (k-WTA + node-sharing) held at criticality (branching σ≈1); CE-train balanced corpus + held-out descent; measure G1/G6 engine-native via cli/anima.hexa eval, bars frozen-first; PULL ckpt.

## Scope / honesty (c9)

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). gpu_recipe 발사 시(team-lead cost-gate go): held-out 4/4 mirror-CE DESCENT 게이트(a_clm_gen_pipeline) → CORE `--engine conv` mount 위 frozen G1(H_1129 recombination)·G6(H_1464 fals) byte-exact engine-native 재측정(torch probe 아님) → ckpt PULL before teardown(a_fire_recover_complete). cheap_test 가 numpy mirror 이므로 그 결과도 DIRECTIONAL(엔진-네이티브 아님).
