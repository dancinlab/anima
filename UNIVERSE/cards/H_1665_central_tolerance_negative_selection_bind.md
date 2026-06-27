# H_1665 — Central-Tolerance Negative-Selection Binder

- **tier:** 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy, no engine); gpu_recipe = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** archbrainstorm — 84-family anima-native synthesis-binding architecture census (binding-wall program, H_1603)
- **lens:** 면역학 — central tolerance / thymic negative selection (deletion of self-reactive clones → survivors recognize non-self); maps non-self ≡ G2 corpus-absence ≡ G6 novelty. Substrate: anima §ImmuneMemory.
- **artifacts:** `state/binding_arch_census/BRAINSTORM_INDEX.md`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1449 (attention-block INERT@1blk) · H_1602 (recombination-objective prereg)
- **key:** `central_tolerance_negative_selection_bind`

## Mechanism

In one forward the mouth emits a cheap rank-r coincidence/outer code c(leg1,leg2) over the two leg representations, then matches every candidate conjunction against a FROZEN self-repertoire panel S — the trunk's own high-frequency co-occurrence statistics, playing the role of immune self-antigens stored in anima §ImmuneMemory. A single SUBTRACTIVE gate suppresses (deletes) any candidate whose recall against S exceeds recall_thr; the surviving NON-self conjunctions pass straight to the next-byte readout. The two legs are bound because deletion operates on the JOINT code c(leg1,leg2), not on either marginal — the bound identity is literally 'which conjunction is not already self'.

## Why it crosses the binding wall

Conv/attention combine evidence ADDITIVELY (sum/softmax-average), so a novel conjunction's signal is drowned by the two dominant marginals and depth only re-mixes the same marginal pool — exactly the H_1603 deficit. Negative selection is SUBTRACTIVE against a frozen self-set, so it specifically surfaces the joint the marginals cannot represent: G2 corpus-absence is literally the non-self set, and G6 falsifiability = a non-self (novel) conjunction. Ablation logic (two knobs, both must be necessary): (a) replace the self-panel with identity → readout reverts to additive marginal blend → G1/G6 collapse to bytegpt baseline; (b) keep the panel but gate on marginals only (drop the JOINT code) → suppression is no longer conjunction-specific → fals→0. Only the panel×joint-code pair survives both ablations.

## Cheap test (frozen-first · $0 · decisive numpy probe)

numpy, deterministic, $0. Build a synthetic 2-feature corpus whose targets require A∧B (XOR-style conjunctions that never appear as singletons). Frozen self-panel = the bigram marginal table. Compare additive-readout baseline vs negative-selection readout on held-out conjunctions; metric = recall of non-self conjunctions at a fixed false-positive rate on self (AUROC). Pre-register PASS = neg-sel beats additive by ≥0.2 AUROC AND that gap vanishes when the self-panel is zeroed (ablation control).

## GPU recipe (cost-gated · PRE-REGISTER ONLY · NOT fired)

PRE-REGISTER ONLY (cost-gated). 303M custom mouth = conv trunk → rank-r coincidence-outer layer → frozen self-panel built from trunk co-occurrence over the 4-cell corpus → subtractive recall gate wired to live §ImmuneMemory recall_thr → readout. CE-train on balanced ko/en×general/sns, held-out CE descent gate, then measure G1 recombine and G6 fals-rate ENGINE-NATIVE via cli/anima.hexa eval; pre-register both bars frozen-first; PULL ckpt before teardown.

## Scope / honesty (c9)

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). gpu_recipe 발사 시(team-lead cost-gate go): held-out 4/4 mirror-CE DESCENT 게이트(a_clm_gen_pipeline) → CORE `--engine conv` mount 위 frozen G1(H_1129 recombination)·G6(H_1464 fals) byte-exact engine-native 재측정(torch probe 아님) → ckpt PULL before teardown(a_fire_recover_complete). cheap_test 가 numpy mirror 이므로 그 결과도 DIRECTIONAL(엔진-네이티브 아님).
