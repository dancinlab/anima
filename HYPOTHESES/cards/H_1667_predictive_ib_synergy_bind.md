# H_1667 — A⇄G Synergistic Information-Bottleneck Channel

- **tier:** 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy, no engine); gpu_recipe = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** archbrainstorm — 84-family anima-native synthesis-binding architecture census (binding-wall program, H_1603)
- **lens:** 정보이론 — partial information decomposition (synergy vs redundancy) + information bottleneck / minimal sufficient statistic. A⇄G realized as a rate-limited encoder→decoder channel.
- **artifacts:** `state/binding_arch_census/BRAINSTORM_INDEX.md`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1449 (attention-block INERT@1blk) · H_1602 (recombination-objective prereg)
- **key:** `predictive_ib_synergy_bind`

## Mechanism

Cast A (forward) as an encoder of the leg1-context and G (reverse) as a decoder predicting the leg2-target, and force ALL A→G communication through a narrow rate-limited bottleneck variable Z (small d_z, e.g. VQ or noisy-linear). One forward: leg1 → A → Z → G → readout. The bottleneck is sized so G can only reconstruct the target when Z carries SYNERGISTIC information (partial-information-decomposition synergy) — information present in the joint (leg1,leg2) but in NEITHER marginal. Because Z is capacity-limited, redundant marginal info is squeezed out and the channel preferentially keeps the conjunction; the bound representation = the synergistic component that survives compression.

## Why it crosses the binding wall

Conv/attention impose NO rate constraint, so the cheap additive (redundant-marginal) solution always dominates and synergy is never forced — depth just adds capacity to pass more marginals. A capacity bottleneck makes the conjunction the CHEAPEST sufficient code (compression pressure structurally privileges binding). Crucially this is an architectural CHANNEL-CAPACITY operator, orthogonal to a recombination training-objective (which leaves the easy additive optimum reachable). Ablation: (a) widen Z to full rank → synergy no longer forced → reverts to marginal blend, G1 collapses — proves the bottleneck (not merely the A⇄G pairing) is load-bearing; (b) directly measure PID synergy(Z; leg1,leg2) — should be high for narrow-Z, near-0 for wide-Z baseline.

## Cheap test (frozen-first · $0 · decisive numpy probe)

numpy PID toy ($0). XOR-like target where 100% of task info is synergistic. Sweep d_z; for each, measure synergy(Z;leg1,leg2) via Williams-Beer/BROJA and held-out conjunction prediction. Pre-register PASS = narrow-Z predicts held-out conjunctions via high synergy while wide-Z (and a conv baseline) solve training via redundancy and fail held-out (synergy≈0).

## GPU recipe (cost-gated · PRE-REGISTER ONLY · NOT fired)

PRE-REGISTER ONLY. 303M = conv trunk → A-encoder → bottleneck Z (small d_z, VQ or noisy linear) → G-decoder → readout. CE-train balanced corpus + held-out descent; measure G1/G6 engine-native via cli/anima.hexa eval AND report Z synergy; bars frozen-first; PULL ckpt.

## Scope / honesty (c9)

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). gpu_recipe 발사 시(team-lead cost-gate go): held-out 4/4 mirror-CE DESCENT 게이트(a_clm_gen_pipeline) → CORE `--engine conv` mount 위 frozen G1(H_1129 recombination)·G6(H_1464 fals) byte-exact engine-native 재측정(torch probe 아님) → ckpt PULL before teardown(a_fire_recover_complete). cheap_test 가 numpy mirror 이므로 그 결과도 DIRECTIONAL(엔진-네이티브 아님).
