# H_1644 — Presynaptic short-term facilitation (calcium gain variable u) temporal binder

- **tier:** 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy, no engine); gpu_recipe = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** archbrainstorm — 84-family anima-native synthesis-binding architecture census (binding-wall program, H_1603)
- **lens:** presynaptic short-term synaptic plasticity — Tsodyks-Markram facilitation; Mongillo-Barak-Tsodyks synaptic-gain working memory (continuous gain, not a slot buffer)
- **artifacts:** `state/binding_arch_census/BRAINSTORM_INDEX.md`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1449 (attention-block INERT@1blk) · H_1602 (recombination-objective prereg)
- **key:** `short_term_facilitation_bind`

## Mechanism

Each head carries a presynaptic facilitation state u_t (a calcium-like utilization variable, Tsodyks-Markram), updated within the forward as the sequence streams: leg A's appearance raises u on a shared channel; when leg B arrives later, its effective drive is multiplied → B·u(A). u decays with a short time-constant, so binding is conjunction-of-recent. Distinct from a discrete WM buffer (no slots/addresses): it is a continuous per-synapse multiplicative GAIN that is itself a function of leg A's content, so leg B's value gets bilinearly modulated by A within the same forward.

## Why it crosses the binding wall

Attention binds by weighted retrieval — a convex mixture that cannot multiply the retrieved value by the query's content. Short-term facilitation makes the synaptic gain a function of leg A, so leg B contributes the product u(A)·B — a true bilinear temporal conjunction; depth re-mixes mixtures but never produces this content×content gain. Differs from a compose buffer (which stores+composes discrete items) by being a stateless-decaying continuous gain. Ablation: (a) freeze u=const → reduces to standard attention/recurrence → G1/G6 collapse; (b) make the update additive (read u+B instead of u·B) → no product → INERT. Binding survives only with multiplicative facilitation → it is the causal binder.

## Cheap test (frozen-first · $0 · decisive numpy probe)

numpy sequence model with facilitation variable u, $0: feed [A … B] vs [A' … B]; pre-register that readout regresses onto bilinear u(A)·B with R² ≥ additive-trace-control + 0.15, that binding strength decays monotonically with the A–B gap, and bound-vs-singleton separability margin ≥ 0.10, over 200 sequences. ≥4/5 HIT. Additive-update ablation lift < 0.02 = INERT.

## GPU recipe (cost-gated · PRE-REGISTER ONLY · NOT fired)

PRE-REGISTER ONLY (cost-gated): 303M with a per-head presynaptic gain u_t updated by a tiny scalar recurrence (Tsodyks-Markram facilitation), u multiplies the value stream; param overhead negligible, matched. 4-cell balanced corpus, held-out CE descent gate, verdict via CORE engine-native frozen G1∧G6. Control arms = frozen-u and additive-u. ckpt PULL pre-teardown.

## Scope / honesty (c9)

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). gpu_recipe 발사 시(team-lead cost-gate go): held-out 4/4 mirror-CE DESCENT 게이트(a_clm_gen_pipeline) → CORE `--engine conv` mount 위 frozen G1(H_1129 recombination)·G6(H_1464 fals) byte-exact engine-native 재측정(torch probe 아님) → ckpt PULL before teardown(a_fire_recover_complete). cheap_test 가 numpy mirror 이므로 그 결과도 DIRECTIONAL(엔진-네이티브 아님).
