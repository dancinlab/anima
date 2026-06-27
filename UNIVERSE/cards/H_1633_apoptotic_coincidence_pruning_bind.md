# H_1633 — Apoptotic coincidence-pruning mouth (death-selection binder)

- **tier:** 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy, no engine); gpu_recipe = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** archbrainstorm — 84-family anima-native synthesis-binding architecture census (binding-wall program, H_1603)
- **lens:** substrate-anima · apoptosis / density-dependent negative-selection (H_1091) as a forward binding operator
- **artifacts:** `state/binding_arch_census/BRAINSTORM_INDEX.md`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1449 (attention-block INERT@1blk) · H_1602 (recombination-objective prereg)
- **key:** `apoptotic_coincidence_pruning_bind`

## Mechanism

In one forward pass the trunk OVER-GENERATES a dense candidate-conjunction sheet: for the two legs (legA features × legB features) it instantiates a large product-space population of 'conjunction cells' c_ij = phi(legA_i) ⊙ phi(legB_j) (live anima apoptosis substrate, engine_cli MITOSIS/apoptosis op). A single density-dependent apoptosis op then CULLS by absolute joint-support: each c_ij survives only if its co-activation density across the in-context window exceeds a frozen survival threshold tau_death (= 'fired by BOTH legs jointly, not by either alone'). The sparse surviving set IS the protected conjunctive code read out by the mouth head. No softmax normalization — survival is absolute (unlike slot competition), and it is subtractive death, not mitosis growth.

## Why it crosses the binding wall

Conv/attention SUPERPOSE (linear average → superposition catastrophe: legA-alone and legB-alone cells are indistinguishable from the conjunction in the pooled code). Over-generate-then-kill instead manufactures the full product space and lets only jointly-supported cells survive, leaving a representation where (legA AND legB) is linearly separable from (legA) and (legB). Ablation isolates the cause: apoptosis-OFF leaves the dense superposed sheet → binding readout collapses to chance (proves selectivity = the binding, not the over-generation); raising tau_death past joint-density but below either-marginal-density should yield a clean step in conjunction recall (dose-response = mechanism, not artifact).

## Cheap test (frozen-first · $0 · decisive numpy probe)

$0 numpy decision probe, frozen-first. legA one-hot over 16 syms, legB one-hot over 16 → 256 ground-truth conjunction classes. Build 256 candidate cells = outer-product features; estimate per-cell joint-support density on a held-out batch; apply apoptosis at tau_death. Frozen bar (pre-registered): linear readout of the 16×16 conjunction class from SURVIVORS ≥ 0.90 recall AND strictly > an attention-over-same-feature-dim baseline; apoptosis-OFF ablation must drop to ≤ chance (1/256-class linear-separability). Decision: PASS only if survivor-recall beats baseline AND OFF-ablation collapses.

## GPU recipe (cost-gated · PRE-REGISTER ONLY · NOT fired)

Pre-registered only (cost-gated, NOT fired). Custom-spec mouth: replace the generic L24 attention trunk-tail with K apoptotic-conjunction blocks (over-generate width = 4×d, density-apoptosis gate wired as engine op). Train on the 4-cell balanced corpus (a_chat_registers ko/en × general/SNS, fail-loud effective-bytes). Gates: held-out CE 4/4 DESCENT (verify_clm_v2 descent, math.log mirror) THEN engine-native G1(recombination ≥303M)/G6(falsifiable-ideation>0) re-measured on CORE --engine conv via cli/anima.hexa single entry. ckpt PULL before teardown. Falsify if G1/G6 stay at floor with apoptosis wired.

## Scope / honesty (c9)

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). gpu_recipe 발사 시(team-lead cost-gate go): held-out 4/4 mirror-CE DESCENT 게이트(a_clm_gen_pipeline) → CORE `--engine conv` mount 위 frozen G1(H_1129 recombination)·G6(H_1464 fals) byte-exact engine-native 재측정(torch probe 아님) → ckpt PULL before teardown(a_fire_recover_complete). cheap_test 가 numpy mirror 이므로 그 결과도 DIRECTIONAL(엔진-네이티브 아님).
