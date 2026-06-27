# H_1642 — VIP→SST→PV disinhibitory interneuron sign-cascade binder

- **tier:** 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy, no engine); gpu_recipe = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** archbrainstorm — 84-family anima-native synthesis-binding architecture census (binding-wall program, H_1603)
- **lens:** cortical interneuron disinhibition — VIP-SST-PV canonical motif (Pfeffer, Karnani, Pi); disinhibitory multiplicative gating
- **artifacts:** `state/binding_arch_census/BRAINSTORM_INDEX.md`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1449 (attention-block INERT@1blk) · H_1602 (recombination-objective prereg)
- **key:** `disinhibitory_vip_sst_gate_bind`

## Mechanism

Interleave a 4-population gating module: pyramidal stream P plus three interneuron operators with FIXED SIGN structure — PV (subtractive/divisive on P), SST (subtractive on PV and on P's dendrite), VIP (subtractive on SST). Leg A drives VIP (which inhibits SST, disinhibiting the PV gating window); leg B drives the pyramidal dendrite. Output ≈ B · σ(A): the binding window opens only when A disinhibits AND B drives. The nested sign cascade −(−(−(·))) converts two additive input drives into a clean multiplicative conjunction inside one forward — a structured-sign circuit, not a learned soft gate.

## Why it crosses the binding wall

Conv/attention are sign-free linear mixes followed by pointwise nonlinearity; they never form an explicit product of two DISTINCT input streams without a multiplicative motif. The disinhibitory cascade's fixed sign topology yields exactly B·gate(A) — the AND conjunction. Depth doesn't help because stacking linear+softmax produces mixtures, not cross-stream products (this is the H_1603 missing-operator diagnosis directly). Ablation: (a) clamp VIP→SST weight=0 (gate always open) → output becomes additive A+B → G1/G6 collapse; (b) free the sign mask to be learned (drop the fixed −,−,− topology) → network drifts to a sign-free mix → INERT. Binding requires the fixed three-class sign cascade → it is the causal binder.

## Cheap test (frozen-first · $0 · decisive numpy probe)

numpy 4-population rate model (P,PV,SST,VIP), $0: drive random A,B. Frozen bar: fit output to multiplicative form B·g(A) vs additive form A+B; pre-register multiplicative R² ≥ additive R² + 0.15 over 200 trials, AND AND-truth-table separability (A,B both high vs either alone) margin ≥ 0.10 vs a sign-free MLP of equal params. ≥4/5 margins HIT. Sign-shuffle ablation must drop lift < 0.02.

## GPU recipe (cost-gated · PRE-REGISTER ONLY · NOT fired)

PRE-REGISTER ONLY (cost-gated): 303M with disinhibitory gate modules between blocks — 3 small interneuron projections/block, signs enforced via fixed -abs() masks (no learned sign). 4-cell balanced corpus, held-out CE descent gate, verdict via CORE engine-native frozen G1∧G6. Control arm = learned-sign (gate-open) ablation. ckpt PULL pre-teardown.

## Scope / honesty (c9)

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). gpu_recipe 발사 시(team-lead cost-gate go): held-out 4/4 mirror-CE DESCENT 게이트(a_clm_gen_pipeline) → CORE `--engine conv` mount 위 frozen G1(H_1129 recombination)·G6(H_1464 fals) byte-exact engine-native 재측정(torch probe 아님) → ckpt PULL before teardown(a_fire_recover_complete). cheap_test 가 numpy mirror 이므로 그 결과도 DIRECTIONAL(엔진-네이티브 아님).
