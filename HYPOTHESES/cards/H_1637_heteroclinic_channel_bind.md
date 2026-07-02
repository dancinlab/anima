# H_1637 — Heteroclinic-channel winnerless-competition mouth (metastable sequence binding)

- **tier:** 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy, no engine); gpu_recipe = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** archbrainstorm — 84-family anima-native synthesis-binding architecture census (binding-wall program, H_1603)
- **lens:** dynamical-systems / Rabinovich winnerless competition; biology = transient sequential population codes (insect olfaction, hippocampal replay sequences)
- **artifacts:** `state/binding_arch_census/BRAINSTORM_INDEX.md`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1449 (attention-block INERT@1blk) · H_1602 (recombination-objective prereg)
- **key:** `heteroclinic_channel_bind`

## Mechanism

Mouth state = population of N competing units under a generalized Lotka-Volterra (asymmetric lateral-inhibition) recurrence. Leg-A (content/concept) parameterizes the asymmetric inhibition matrix rho_ij = the CHANNEL TOPOLOGY (which saddle flows to which); leg-B (role/context) sets the initial condition / drive vector. In ONE forward pass the state walks a heteroclinic channel = a deterministic metastable SEQUENCE of saddle visits whose ORDER and dwell-time pattern is a joint function of both legs. Bound code = the ordered trajectory signature (sequence of dominant units), read by a temporal-pool head into byte logits. Same A with different B -> different visiting order -> role-filler conjunction lives in the sequence.

## Why it crosses the binding wall

conv/attention emit a single static superposition (value-vector sum) -> A and B are averaged, 'which-goes-with-which' is lost. A heteroclinic channel encodes the conjunction as an ORDERED TEMPORAL TRAJECTORY: the same active-unit set in different orders are linearly distinct codes (sequence != sum), so conjunctions are exponentially more separable and compositionally generalize. ABLATION-1: symmetrize rho_ij (remove the winnerless-competition asymmetry) -> system collapses to a single fixed-point attractor (== energy_settle), sequence vanishes, falls back to superposition. ABLATION-2: make rho_ij depend on A only (not joint) -> order independent of B -> role-binding gone. Orthogonal to energy_settle/DEQ because the carrier is a saddle-connection TRANSIENT, not a fixed point or equilibrium solve.

## Cheap test (frozen-first · $0 · decisive numpy probe)

numpy GLV simulator, N=8 units. Synthetic legs: A picks 1 of 4 channel-topology matrices, B picks 1 of 4 initial drives -> 16 (A,B) trajectories. Linear readout on the dominant-unit sequence; frozen-first bar: must classify HELD-OUT (A,B) combos unseen in fit AND beat (i) static-sum baseline A_vec+B_vec and (ii) shuffled-order control. Sweep symmetry of rho to confirm ablation curve (binding -> chance as rho symmetrizes). $0, minutes.

## GPU recipe (cost-gated · PRE-REGISTER ONLY · NOT fired)

PRE-REGISTER ONLY (cost-gated): 303M mouth, final ~2 layers replaced by a GLV heteroclinic cell (N~=d units; asymmetric rho projected from leg-A trunk slice, drive from leg-B slice), unrolled T=8 metastable steps, temporal-pool readout -> byte logits. Train on a_chat_registers 4-cell balanced corpus + held-out val. Verdict via CORE conv-mount engine-native G1(recombination)/G6(fals) re-measure (a_engine_native_learning); ckpt PULL before teardown.

## Scope / honesty (c9)

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). gpu_recipe 발사 시(team-lead cost-gate go): held-out 4/4 mirror-CE DESCENT 게이트(a_clm_gen_pipeline) → CORE `--engine conv` mount 위 frozen G1(H_1129 recombination)·G6(H_1464 fals) byte-exact engine-native 재측정(torch probe 아님) → ckpt PULL before teardown(a_fire_recover_complete). cheap_test 가 numpy mirror 이므로 그 결과도 DIRECTIONAL(엔진-네이티브 아님).
