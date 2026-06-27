# H_1674 — Tag-and-Capture Binding (local marker × global depletable resource competition)

- **tier:** 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy, no engine); gpu_recipe = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** archbrainstorm — 84-family anima-native synthesis-binding architecture census (binding-wall program, H_1603)
- **lens:** synaptic plasticity — synaptic tagging & capture (Frey-Morris): local tag × global depletable resource with cross-slot competition
- **artifacts:** `state/binding_arch_census/BRAINSTORM_INDEX.md`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1449 (attention-block INERT@1blk) · H_1602 (recombination-objective prereg)
- **key:** `synaptic_tag_capture_bind`

## Mechanism

Asymmetric two-leg roles (Frey-Morris STC). Leg-A (weak/specific) sets local TAGS t_i = sigmoid(W_a a_i) at each slot — marks WHERE binding may occur. Leg-B (strong/salient) synthesizes a GLOBAL, CAPACITY-LIMITED resource pool P (total budget = learned scalar) distributed by a softmax-share over slots weighted by leg-B drive — marks the budget and WHICH slots are salient. Bound output at slot i = t_i · captured_P_i, where capture allocates the limited pool to tagged slots under a hard capacity cap (Σ captured ≤ P_total, via differentiable top-k / entmax) → tagged slots COMPETE for the shared resource. Capacity makes binding sparse and exclusive: only tagged slots capture, and limited resource forces winner-takes-most among them.

## Why it crosses the binding wall

the distinguishing principle is a GLOBAL DEPLETABLE shared resource gated by a LOCAL tag — neither additive attention nor a local coincidence gate has a capacity-limited cross-slot COMPETITION for a pool produced by one leg and consumed by the other. Binding = (local tag from A) AND (captured global resource from B): ablate A → no tags → pool floats unused → 0 bound output; ablate B → no resource → tags decay → 0. Critically, the capacity cap forbids two unbound distractor features from both lighting up (they compete and starve), which is exactly the EXCLUSIVITY G6 ideation needs (one idea binds, distractors suppressed) — a property additive depth and plain coincidence gates lack. Ablation logic: (1) remove capacity cap (P_total→∞) → cross-slot competition gone; if exclusivity / distractor-suppression collapses, the limited-resource competition is load-bearing (this is what separates it from a local coincidence gate). (2) make tag and resource symmetric (both legs do both roles) → if it degrades, the local-marker × global-pool ROLE asymmetry is essential. Distinct from btsp_plateau_eligibility (single-cell seconds-long eligibility window, no global shared depletable pool / no cross-slot competition).

## Cheap test (frozen-first · $0 · decisive numpy probe)

numpy, frozen-first, CPU, math.log mirror. Synthetic task WITH DISTRACTORS: each example = 1 target conjunction + K distractor single-features; held-out novel target combos. Compare capped tag-capture vs UNcapped tag-capture vs additive. Pre-registered bar: capped variant must (a) lower held-out novel-combo CE by ≥0.15 nats vs additive AND (b) show distractor-suppression — prob mass on distractor tokens < half that of the uncapped variant (proving competition starves distractors). GO only if uncapping (ablation 1) erases the distractor suppression.

## GPU recipe (cost-gated · PRE-REGISTER ONLY · NOT fired)

PRE-REGISTERED ONLY, cost-gated, NOT fired. 303M mouth: conv trunk + tag-capture binding blocks (capacity learned per block; differentiable top-k / entmax allocation for capture). 4-cell corpus, held-out DESCENT + engine-native G1/G6. Control arm = uncapped (infinite-resource) variant, same params, isolating the capacity-competition principle. 1×H100 ~$35. Frozen bar: G6 fals > 0 AND distractor-fab (G5-adjacent abstain) not worsened AND > uncapped control. PULL ckpt before teardown.

## Scope / honesty (c9)

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). gpu_recipe 발사 시(team-lead cost-gate go): held-out 4/4 mirror-CE DESCENT 게이트(a_clm_gen_pipeline) → CORE `--engine conv` mount 위 frozen G1(H_1129 recombination)·G6(H_1464 fals) byte-exact engine-native 재측정(torch probe 아님) → ckpt PULL before teardown(a_fire_recover_complete). cheap_test 가 numpy mirror 이므로 그 결과도 DIRECTIONAL(엔진-네이티브 아님).
