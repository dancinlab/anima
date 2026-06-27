# H_1629 — Compact-closed type-contraction mouth (DisCoCat cup binding)

- **tier:** 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy, no engine); gpu_recipe = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** archbrainstorm — 84-family anima-native synthesis-binding architecture census (binding-wall program, H_1603)
- **lens:** category theory — compact-closed / pregroup (DisCoCat); binding = type-driven tensor contraction (cup ε), the categorical dual of outer-product
- **artifacts:** `state/binding_arch_census/BRAINSTORM_INDEX.md`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1449 (attention-block INERT@1blk) · H_1602 (recombination-objective prereg)
- **key:** `compact_closed_contract_bind`

## Mechanism

Each token emits not a flat vector but a TYPED tensor whose order is set by a learned pregroup grammatical type (noun = order-1 in N; transitive verb = order-3 in N⊗S⊗N). In one forward pass a tiny type-tagger assigns each position a type, then the binding op is the compact-closed CONTRACTION (cup ε: N⊗N→scalar): a verb's argument legs are glued to neighbors' noun legs by tensor contraction along grammatically-licensed index pairs, leaving the sentence-type S vector as the bound composite. The two legs (role tensor, filler vector) meet in a single type-driven einsum, not in a softmax-weighted sum.

## Why it crosses the binding wall

Conv/attention smear all pairs with learned weights but never CONTRACT indices, so role-filler identity dissolves into a weighted blend (bag-of-vectors) — nothing forces 'agent-of-EAT' ≠ 'patient-of-EAT', which is the G1≡G6 fals=0 signature. Compact-closed contraction is the algebraic DUAL of the excluded tpr_outer_bind: TPR builds the ⊗, here the BIND is the cup ε that consumes it under type control. A novel role-filler combo is just the same contraction over a new index pairing, so recombination is structurally free (no per-pair weight needed). Ablation: replace the type-driven cup with an untyped sum-pool (cut the contraction) → recombination must collapse to bag-of-words (G1/G6 to floor), isolating the contraction; separately randomize the type-tagger → contractions misalign → binding lost. Both ablations restore the conv/attention failure, proving the cup is load-bearing.

## Cheap test (frozen-first · $0 · decisive numpy probe)

numpy, $0, frozen-first. Micro-grammar SUBJ verb OBJ over 8 byte-words, order-3 verb tensors random-init d=16. Pre-registered bar: on held-out SUBJ×OBJ pairs that NEVER co-occur in train, the contracted S vector linearly decodes (agent,patient) at ≥0.90 vs a sum-pool control at chance, AND swapping subj↔obj flips the decode (an asymmetry bag-of-words structurally cannot represent). Decision: if contraction-decode ≤ sum-pool OR no swap-asymmetry, family FALSIFIED for $0.

## GPU recipe (cost-gated · PRE-REGISTER ONLY · NOT fired)

Cost-gated 303M, pre-register only. Replace L24 generic attention with K typed-contraction layers: per-position type head (softmax over ~8 pregroup types) → reshape hidden into typed legs → batched einsum contraction over type-licensed index pairs → S-leg residual back to stream. Train byte-CLM on 4-cell balanced corpus (a_chat_registers), held-out DESCENT gate, then engine-native G1/G6 on CORE --engine mount (a_engine_native_learning). ckpt PULL before teardown.

## Scope / honesty (c9)

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). gpu_recipe 발사 시(team-lead cost-gate go): held-out 4/4 mirror-CE DESCENT 게이트(a_clm_gen_pipeline) → CORE `--engine conv` mount 위 frozen G1(H_1129 recombination)·G6(H_1464 fals) byte-exact engine-native 재측정(torch probe 아님) → ckpt PULL before teardown(a_fire_recover_complete). cheap_test 가 numpy mirror 이므로 그 결과도 DIRECTIONAL(엔진-네이티브 아님).
