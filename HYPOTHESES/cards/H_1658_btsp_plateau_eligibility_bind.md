# H_1658 — BTSP plateau-eligibility bind (behavioral-timescale wide-window capture)

- **tier:** 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy, no engine); gpu_recipe = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** archbrainstorm — 84-family anima-native synthesis-binding architecture census (binding-wall program, H_1603)
- **lens:** bio-neuro: behavioral-timescale synaptic plasticity (Bittner BTSP) — dendritic plateau eligibility, seconds-wide one-shot credit window (distinct from ms STDP/Hebbian fast-weights and short-term facilitation).
- **artifacts:** `state/binding_arch_census/BRAINSTORM_INDEX.md`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1449 (attention-block INERT@1blk) · H_1602 (recombination-objective prereg)
- **key:** `btsp_plateau_eligibility_bind`

## Mechanism

One leg (role/context) drives a 'plateau head' that, for selected units, opens a long, asymmetric eligibility gate g(t) — a wide behavioral-timescale window decoupled from exact timing/position. While the gate is open, the OTHER leg's incoming features are captured by a gated multiplicative write into that unit's state, regardless of content similarity or sequence distance. One forward pass = (plateau-trigger from leg A) x (gated capture of leg B inside the eligibility window). Binding is an instructive plateau opening a slot, not a symmetric similarity match.

## Why it crosses the binding wall

Attention binds by symmetric content match within a uniformly-weighted window; it cannot one-shot-bind two tokens that are dissimilar yet causally linked and temporally separated. The BTSP plateau is an ASYMMETRIC instructive signal that opens a wide window for arbitrary co-occurring fillers — exactly the variable-binding (role<->distant filler) that ms-coincidence and QK cannot do. Ablation: window->0 reduces to coincidence/attention (fals->0); making the gate input-independent (no instructive plateau) removes selective binding while keeping params, isolating the plateau signal as cause.

## Cheap test (frozen-first · $0 · decisive numpy probe)

numpy sequence toy: role token at t0, filler token at t0+Delta with Delta random and large; task = recover the role<->filler pairing from a probe at sequence end. BTSP eligibility head vs param-matched attention. Decision rule (frozen): BTSP pairing-recovery > 0.9 across large Delta where attention degrades once Delta exceeds content-similarity reach; window->0 ablation reverts BTSP to the attention failure curve. $0.

## GPU recipe (cost-gated · PRE-REGISTER ONLY · NOT fired)

Pre-reg 303M: add a plateau-eligibility head per mouth block (sigmoid plateau trigger from stream A, learned asymmetric decay window ~ wide receptive span, gated bilinear write of stream B). 4-cell balanced corpus, per-cell held-out CE. Gates: held-out 4/4 DESCENT; engine-native G1>=303M baseline AND G6 fals>0 (cli/anima.hexa eval); control = window-clamped-to-0 retrain must fail G6 (ablation falsifier). Pull ckpt pre-teardown.

## Scope / honesty (c9)

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). gpu_recipe 발사 시(team-lead cost-gate go): held-out 4/4 mirror-CE DESCENT 게이트(a_clm_gen_pipeline) → CORE `--engine conv` mount 위 frozen G1(H_1129 recombination)·G6(H_1464 fals) byte-exact engine-native 재측정(torch probe 아님) → ckpt PULL before teardown(a_fire_recover_complete). cheap_test 가 numpy mirror 이므로 그 결과도 DIRECTIONAL(엔진-네이티브 아님).
