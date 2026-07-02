# H_1608 — Pulvinar Transthalamic Binding-Bottleneck Mouth (driver x modulator low-rank relay)

- **tier:** 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy, no engine); gpu_recipe = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** archbrainstorm — 84-family anima-native synthesis-binding architecture census (binding-wall program, H_1603)
- **lens:** thalamo-cortical (higher-order pulvinar) transthalamic routing; Sherman-Guillery driver vs modulator; low-rank relay bottleneck binding.
- **artifacts:** `state/binding_arch_census/BRAINSTORM_INDEX.md`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1449 (attention-block INERT@1blk) · H_1602 (recombination-objective prereg)
- **key:** `transthalamic_relay_bottleneck`

## Mechanism

The two legs (two trunk streams) are forbidden to mix directly; instead each writes to and reads from a shared higher-order thalamic relay of SMALL rank r (transthalamic/pulvinar route) within one forward. The relay applies a content-dependent gate using the Sherman-Guillery driver/modulator distinction: leg-A is the driver, leg-B's state is a MULTIPLICATIVE modulator on the relay transfer. Because both legs must traverse the same low-rank relay and modulate each other there, the relay is forced to form a compressed JOINT code that both streams then read back. Binding = a shared low-rank conjunctive bottleneck with driver x modulator gating.

## Why it crosses the binding wall

stacking attention/conv adds direct cortico-cortical capacity, but each layer mixes additively and at full rank, so the model can route legs independently and never needs a joint code. Forcing ALL cross-leg communication through a low-rank modulated relay makes the only path to use leg-B's information about leg-A a shared conjunctive variable -> binding is structurally required, not optional. Ablation: (a) widen relay to full rank -> legs route independently, binding optional, fails; (b) make leg-B a driver (additive) not a modulator -> no multiplicative join -> fails. Distinct from a parallel binding_lane: this is an IN-PATH bottleneck the signal must traverse, not an added side module.

## Cheap test (frozen-first · $0 · decisive numpy probe)

numpy, DIRECTIONAL. factored-table with a routing twist: legA carries 'which factor pair', legB carries a context that SELECTS which table entry to emit (conjunction required at the relay). Low-rank (r=4) driver x modulator relay vs full-rank additive relay. 25% held-out combos. Frozen bar: low-rank modulated held-out CE < 0.3 nats AND full-rank-additive >= 0.9x uniform; pre-register that small-rank-modulated > large-rank-additive across a rank sweep.

## GPU recipe (cost-gated · PRE-REGISTER ONLY · NOT fired)

PRE-REGISTER ONLY. 303M trunk split into two streams whose only cross-talk is a shared low-rank (r~32) driver/modulator relay at mid-depth; CE-trained; engine-native G1/G6; bars frozen. ~$15; ckpt PULL.

## Scope / honesty (c9)

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). gpu_recipe 발사 시(team-lead cost-gate go): held-out 4/4 mirror-CE DESCENT 게이트(a_clm_gen_pipeline) → CORE `--engine conv` mount 위 frozen G1(H_1129 recombination)·G6(H_1464 fals) byte-exact engine-native 재측정(torch probe 아님) → ckpt PULL before teardown(a_fire_recover_complete). cheap_test 가 numpy mirror 이므로 그 결과도 DIRECTIONAL(엔진-네이티브 아님).
