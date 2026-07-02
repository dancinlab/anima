# H_1666 — Φ-Ratchet Coincidence Rectifier

- **tier:** 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy, no engine); gpu_recipe = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** archbrainstorm — 84-family anima-native synthesis-binding architecture census (binding-wall program, H_1603)
- **lens:** 비평형 통계역학 — Brownian/Feynman ratchet, broken detailed balance, molecular motors (rectify thermal noise into directed motion via a pawl). Substrate: anima safety_phi_ratchet Ψ=½ attractor.
- **artifacts:** `state/binding_arch_census/BRAINSTORM_INDEX.md`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1449 (attention-block INERT@1blk) · H_1602 (recombination-objective prereg)
- **key:** `phi_ratchet_rectify_bind`

## Mechanism

Repurpose anima's safety_phi_ratchet (an irreversible monotone pawl that only advances toward Ψ=½) as a binding operator. Inside the mouth forward, A (forward logits) and G (reverse field) each emit a fluctuating partial vote across K inner micro-ticks; a pawl element advances a bound-state register one notch ONLY when both legs co-fire within the same micro-tick (conjunction at the pawl), and the ratchet's no-backslip latch makes each advance persistent (hysteretic). Over the K micro-iterations the rectified A⇄G tension accumulates a directed code recording WHICH conjunctions co-fired; that register is read out as the next-byte distribution. Marginal-only fluctuations have zero net rectification — they average out and never advance the pawl.

## Why it crosses the binding wall

Conv/attention layers are (per-layer) linear time-invariant and effectively reversible — symmetric averaging cannot rectify, so a lone conjunction's transient is integrated symmetrically and cancels; stacking depth just adds more symmetric mixers. The ratchet is NONLINEAR and IRREVERSIBLE (broken detailed balance): it converts a coincidence into a persistent asymmetric state — precisely the 'weld two legs into one persistent unit' operation attention-depth lacks. Ablation: (a) make the ratchet reversible (remove pawl asymmetry) → net advance from coincidences → 0 → binding vanishes, isolating IRREVERSIBILITY (not merely nonlinearity) as load-bearing; (b) let the pawl advance on single-leg firing → advance becomes marginal-driven → fals→0, isolating the CO-FIRE requirement.

## Cheap test (frozen-first · $0 · decisive numpy probe)

numpy, $0. Two noisy leg-streams with rare synchronous coincidences that carry the label. Compare a reversible-integrator baseline vs the rectifying no-backslip ratchet readout; surrogate control = phase-shuffle the two legs to destroy synchrony. Pre-register PASS = ratchet recovers coincidence rate above shuffle by a margin AND the reversible baseline ≈ shuffle (proves rectification, not integration, recovers the conjunction).

## GPU recipe (cost-gated · PRE-REGISTER ONLY · NOT fired)

PRE-REGISTER ONLY. 303M mouth with an inner K-microstep ratchet block placed between A(forward) and G(reverse) before readout, pawl-gated on A∧G co-fire, wired to live safety_phi_ratchet. CE-train balanced corpus + held-out descent; measure G1/G6 engine-native via cli/anima.hexa eval, bars frozen-first; PULL ckpt.

## Scope / honesty (c9)

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). gpu_recipe 발사 시(team-lead cost-gate go): held-out 4/4 mirror-CE DESCENT 게이트(a_clm_gen_pipeline) → CORE `--engine conv` mount 위 frozen G1(H_1129 recombination)·G6(H_1464 fals) byte-exact engine-native 재측정(torch probe 아님) → ckpt PULL before teardown(a_fire_recover_complete). cheap_test 가 numpy mirror 이므로 그 결과도 DIRECTIONAL(엔진-네이티브 아님).
