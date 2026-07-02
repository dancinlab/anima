# H_1685 — Graduated-non-convexity temperature-continuation bind (deterministic Sinkhorn homotopy)

- **tier:** 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy, no engine); gpu_recipe = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** archbrainstorm — 84-family anima-native synthesis-binding architecture census (binding-wall program, H_1603)
- **lens:** DYNAMICS — deterministic graduated-non-convexity / temperature-continuation (Sinkhorn optimal-transport homotopy); binding = tracking the assignment minimizer as objective smoothness anneals from convex blur to combinatorial commitment.
- **artifacts:** `state/binding_arch_census/BRAINSTORM_INDEX.md`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1449 (attention-block INERT@1blk) · H_1602 (recombination-objective prereg)
- **key:** `graduated_nonconvexity_anneal_bind`

## Mechanism

Compose the two legs by minimizing a binding energy whose SMOOTHNESS is scheduled within one forward pass (deterministic annealing / graduated non-convexity / GNC). State z is a soft assignment matrix binding content-features (leg-A) to role-slots (leg-B); E_T(z) couples leg-A scores and leg-B scores with an entropy term scaled by temperature T (Sinkhorn-style optimal-transport coupling). Start at high T: z is a blurred near-uniform mixture (no commitment, both legs averaged). Run a FIXED continuation schedule T: T_hi→T_lo (e.g. 6–8 outer steps), at each T doing mean-field/Sinkhorn updates and TRACKING the minimizer as it deforms. As T→0 the soft assignment crystallizes into a near-permutation that uniquely binds each content to its role. Logits read from z* applied to leg-A. The schedule itself is the binding operator.

## Why it crosses the binding wall

A single fixed-temperature softmax (what attention does) sits in the convex blur: at its operating temperature the assignment is smooth and content-magnitude dominates, so it cannot resolve which content goes to which role (G1 fails). Homotopy continuation follows the easy convex optimum continuously down to the hard combinatorial binding, escaping the blur that a one-shot read is trapped in — the TEMPERATURE SCHEDULE, not extra capacity, does the work. ABLATION: (a) run at fixed low T (no schedule) → predict collapse to local-min / attention-like blur; (b) fixed high T → no commitment (near-uniform). Only the schedule binds; if a single fixed T matches it the mechanism is INERT. Distinct from diffusion_denoise_compose (stochastic Gaussian noise in data space) — GNC is deterministic and anneals OBJECTIVE smoothness; distinct from energy_settle_attractor (fixed energy landscape).

## Cheap test (frozen-first · $0 · decisive numpy probe)

mini-numpy, $0, frozen-first. 4 content × 4 role assignment with a hidden true permutation; legA=content scores, legB=role scores (FROZEN). Implement Sinkhorn at fixed-T (baseline) vs GNC schedule (T 5.0→0.1, 8 outer iters). Pre-registered bar: held-out permutation-recovery / conjunction accuracy; PASS iff GNC > fixed-T by ≥+0.15 AND the fixed-low-T ablation collapses (≤+0.02). No training.

## GPU recipe (cost-gated · PRE-REGISTER ONLY · NOT fired)

PRE-REGISTER ONLY (cost-gated). 303M: conv-trunk → legA(content map),legB(role map); GNC binding head = unrolled Sinkhorn with annealing (8 iters, learned T-schedule) → bind → byte logits. Train CE on balanced 4-cell corpus with fail-loud per-cell byte/epoch report. Single H100. Engine-native G1/G6 via CORE mount + held-out 4/4 DESCENT, frozen pre-registered bars.

## Scope / honesty (c9)

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). gpu_recipe 발사 시(team-lead cost-gate go): held-out 4/4 mirror-CE DESCENT 게이트(a_clm_gen_pipeline) → CORE `--engine conv` mount 위 frozen G1(H_1129 recombination)·G6(H_1464 fals) byte-exact engine-native 재측정(torch probe 아님) → ckpt PULL before teardown(a_fire_recover_complete). cheap_test 가 numpy mirror 이므로 그 결과도 DIRECTIONAL(엔진-네이티브 아님).
