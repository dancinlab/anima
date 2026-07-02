# H_1683 — Leaky-Competing-Accumulator race binding (drift-diffusion to threshold)

- **tier:** 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy, no engine); gpu_recipe = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** archbrainstorm — 84-family anima-native synthesis-binding architecture census (binding-wall program, H_1603)
- **lens:** DYNAMICS — leaky temporal evidence-integration to threshold (drift-diffusion / leaky competing accumulator); binding = the race winner among combinatorial accumulators, with leak enforcing temporal-AND and lateral inhibition enforcing exclusivity.
- **artifacts:** `state/binding_arch_census/BRAINSTORM_INDEX.md`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1449 (attention-block INERT@1blk) · H_1602 (recombination-objective prereg)
- **key:** `ramp_to_threshold_accumulator_bind`

## Mechanism

Replace the final additive logit projection with a bank of leaky competing accumulators (Usher-McClelland LCA / Ratcliff drift-diffusion) over the candidate bytes, run R internal micro-steps inside ONE forward pass (recurrent in a fixed-size register, no extra emitted tokens). The trunk emits leg-A (content) and leg-B (role/position). Each candidate y has an accumulator a_y with dynamics a_y += dt*( -lambda*a_y + f(W_A·legA, W_B·legB)_y ) - beta*sum_{y'≠y} a_{y'}, where the drive f is a MULTIPLICATIVE conjunction (legA gates legB, not a sum) and beta is lateral inhibition. After R steps the byte whose accumulator first crosses threshold (or is highest) is emitted; logits = a (post-settle). The two legs meet in the multiplicative drive AND in the temporal integral.

## Why it crosses the binding wall

conv/attention sum features then read ONE instantaneous softmax, so a single high-magnitude leg dominates the sum (content overrides role → G1/G6 fail). The LEAK lambda is the binding gate: an instantaneous additive co-occurrence decays unless BOTH legs co-drive the SAME accumulator persistently across micro-steps (temporal-AND), and lateral inhibition forces exclusive selection of the conjunctive winner among combinatorially-many candidates. The conjunction is encoded by WHICH accumulator wins the race and its crossing-time, information absent from any single instantaneous projection. ABLATION (two orthogonal knobs): (a) lambda=0 AND beta=0 reduces exactly to summed softmax → predict collapse to bytegpt baseline (isolates that the dynamics, not added params, carry binding); (b) replace multiplicative drive f with additive → predict partial collapse (isolates multiplicative-AND vs leak-AND contributions). If either ablation matches the binding result, the mechanism is INERT.

## Cheap test (frozen-first · $0 · decisive numpy probe)

mini-numpy, $0, <120 lines, frozen-first. Synthetic V=16 = 4 content × 4 role conjunction task; two leg vectors, FROZEN random W_A,W_B. Implement LCA recurrence (R=10, sweep lambda,beta) vs plain summed-softmax baseline. Pre-registered frozen bar: compositional held-out conjunction accuracy on (content,role) pairs whose conjunction was never co-presented. PASS iff LCA exceeds softmax by ≥+0.15 absolute AND the lambda=0,beta=0 ablation collapses LCA→softmax (≤+0.02). Decision-only, no training.

## GPU recipe (cost-gated · PRE-REGISTER ONLY · NOT fired)

PRE-REGISTER ONLY (cost-gated, user-go). Custom-spec 303M mouth = bytegpt conv-trunk (frozen-init) + dual projection legA(d),legB(d) + LCA decode layer with R=8 micro-steps unrolled, lambda/beta as learned per-head scalars. Train CE on the 4-cell {ko,en}×{general,sns} balanced corpus with fail-loud per-cell byte counts. Single H100. Engine-native acceptance: clm/bytegpt-side G1 recombination ≥ bytegpt baseline AND G6 fals>0, plus held-out 4/4 mirror DESCENT gate (a_clm_gen_pipeline). Verdict only via CORE --engine mount, not torch probe.

## Scope / honesty (c9)

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). gpu_recipe 발사 시(team-lead cost-gate go): held-out 4/4 mirror-CE DESCENT 게이트(a_clm_gen_pipeline) → CORE `--engine conv` mount 위 frozen G1(H_1129 recombination)·G6(H_1464 fals) byte-exact engine-native 재측정(torch probe 아님) → ckpt PULL before teardown(a_fire_recover_complete). cheap_test 가 numpy mirror 이므로 그 결과도 DIRECTIONAL(엔진-네이티브 아님).
