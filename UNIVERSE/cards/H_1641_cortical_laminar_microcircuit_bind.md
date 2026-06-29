# H_1641 — Canonical cortical laminar microcircuit (L4→L2/3↺→L5/6 feedback) binder

- **tier:** 🟠 DIRECTIONAL NOT-SUPPORTED (303M engine-native) — **캠페인 최정밀 데이터포인트**: full-laminar arm 이 **G0 5/5 PASS(또박)+G2 89 PASS(새말)인데 G1 best_distinct=0(재조합 0)** = generic undertrain floor 아닌 **binding/recombination 특이적 결핍으로 격리**(coherent∧novel∧¬recombine). nofb/noln 동일 0·G6 fals=0. caveat: binder는 직렬화 전 DROP(=trunk-shaping scope, inference-op 아님, conv g-gates-py-1) + py 2-prod DIRECTIONAL. ckpt PULL(arm_seed7 sha cbe69285)·pod teardown.
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy, no engine); gpu_recipe = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** archbrainstorm — 84-family anima-native synthesis-binding architecture census (binding-wall program, H_1603)
- **lens:** cortical canonical microcircuit — Douglas-Martin laminar feedforward-recurrent-feedback loop + Carandini-Heeger divisive normalization
- **artifacts:** `state/binding_arch_census/BRAINSTORM_INDEX.md`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1449 (attention-block INERT@1blk) · H_1602 (recombination-objective prereg)
- **key:** `cortical_laminar_microcircuit_bind`

## Mechanism

Replace the flat transformer block with a canonical 3-laminar cell. L4 receives the two legs as separate feedforward channels; L2/3 is a recurrent horizontal associative layer with lateral excitation + Carandini-Heeger divisive normalization that super-additively amplifies co-active leg-pairs and suppresses singletons; L5/6 re-injects the partially-bound conjunction back to L4 over K (3-5) settling iterations — the settling IS the forward pass. The two legs bind because the L2/3 recurrent assembly only reaches a stable high-gain fixed point when BOTH legs co-drive a shared horizontal sublattice; divisive normalization then lets the conjunction win the gain competition over either leg alone, all within one block forward.

## Why it crosses the binding wall

Generic attention is a single feedforward convex mixture (softmax sums to 1 → OR-like); it has no recurrent normalization that makes a pair super-additive over its parts (AND-like). The laminar loop's recurrent amplification + divisive normalization gives co-active pairs super-linear gain that a stacked feedforward/softmax stack of any depth (L24 failed) cannot synthesize — depth re-mixes but never re-normalizes a settled conjunction against singletons. Ablation isolates two necessary parts: (a) set L5→L4 feedback gain=0 → reduces to a feedforward block → G1/G6 collapse to bytegpt baseline; (b) replace divisive norm with plain LayerNorm → conjunctions no longer dominate singletons → INERT. Binding survives only with both → the recurrent-normalization motif is the causal binder.

## Cheap test (frozen-first · $0 · decisive numpy probe)

numpy mini-circuit, $0: two leg embeddings A,B (random d=64); build the 3-layer laminar cell (recurrent L2/3 + divisive norm + L5 feedback), run K settling steps. Frozen-first bar: readout for the BOUND pair (A,B) must be separable — cosine to a held-out conjunction target ≥ feedforward-control(equal params) + margin 0.10 AND singleton readouts (A-alone, B-alone, A+distractor-C) below A·B by margin — across 200 random pairs, ≥4/5 of pre-registered margins HIT. Run both ablations in the same script; INERT-check = ablated lift < 0.02.

## GPU recipe (cost-gated · PRE-REGISTER ONLY · NOT fired)

PRE-REGISTER ONLY (cost-gated): 303M where each transformer block → laminar microcircuit block, param-matched (split d into L4/L2-3/L5 sublayers, 3 settling iters, divisive-norm op). Train on a_chat_registers 4-cell balanced corpus with held-out CE descent gate; verdict = ckpt mounted on CORE --engine conv, frozen engine-native G1 recombination (≥303M) ∧ G6 fals>0 bars. Ablation arms (feedback=0, plain-LN) trained as control. ckpt PULL before teardown.

## Scope / honesty (c9)

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). gpu_recipe 발사 시(team-lead cost-gate go): held-out 4/4 mirror-CE DESCENT 게이트(a_clm_gen_pipeline) → CORE `--engine conv` mount 위 frozen G1(H_1129 recombination)·G6(H_1464 fals) byte-exact engine-native 재측정(torch probe 아님) → ckpt PULL before teardown(a_fire_recover_complete). cheap_test 가 numpy mirror 이므로 그 결과도 DIRECTIONAL(엔진-네이티브 아님).
