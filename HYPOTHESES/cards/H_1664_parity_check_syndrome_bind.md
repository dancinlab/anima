# H_1664 — Linear-Code Syndrome Binding Mouth

- **tier:** 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy, no engine); gpu_recipe = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** archbrainstorm — 84-family anima-native synthesis-binding architecture census (binding-wall program, H_1603)
- **lens:** formal-algebraic: linear error-correcting code / syndrome decoding (coding-theory binding with built-in novelty detector)
- **artifacts:** `state/binding_arch_census/BRAINSTORM_INDEX.md`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1449 (attention-block INERT@1blk) · H_1602 (recombination-objective prereg) · H_1466 (TPR binder), H_1514 (VSA/HRR binding)
- **key:** `parity_check_syndrome_bind`

## Mechanism

Encode the two legs as codewords of a linear code over GF(2)/relaxed {-1,+1}: role + filler bits → information word → codeword c = G·[role;filler] via a learned generator matrix G. A learned parity-check matrix H computes the syndrome ŝ = H·c in the same forward pass. Valid (corpus-seen) conjunctions land on the code (syndrome ≈ 0); novel/invalid combinations yield nonzero syndrome. Readout conditions on (c, syndrome); unbinding = nearest-codeword (syndrome) decoding.

## Why it crosses the binding wall

The code structure turns a conjunction into an algebraic object with an EXACT membership test (syndrome), so the mouth simultaneously binds (codeword) and detects falsifiability/novelty (nonzero syndrome) in one pass — directly serving G2 (corpus-absent ⇒ nonzero syndrome) and G6 (is this combination valid/falsifiable). Error-correcting redundancy gives robust unbinding under noise, and combining seen sub-codes yields new valid codewords = systematic generalization. Ablation: set H to zero/identity (no code structure) → syndrome uninformative → novelty/binding signal vanishes, fals→0, isolating the parity-check as the carrier. Distinct from generic VSA bundling (kosmos_vsa): the coding-theoretic redundancy + explicit syndrome detector is structure that pure superposition lacks.

## Cheap test (frozen-first · $0 · decisive numpy probe)

numpy, $0. Small linear code ([15,11] Hamming or random GF(2) G/H). Map 8 roles × 8 fillers → information bits → codewords; hold out 16 valid combos + define a set of never-valid combos. Train readout to (i) reconstruct held-out valid pairs and (ii) flag never-valid combos via syndrome. PASS = syndrome separates valid-held-out vs invalid (AUROC > chance) while a no-code baseline cannot → code structure carries binding + novelty.

## GPU recipe (cost-gated · PRE-REGISTER ONLY · NOT fired)

PRE-REGISTERED ONLY (cost-gated): 303M mouth = conv trunk emits role/filler bit-logits → differentiable linear-code embed (learned relaxed-GF(2) G) → learned parity-check syndrome head + codeword readout→V256. Gates = held-out CE-DESCENT + engine-native G2 novelty / G6 fals on CORE. Ckpt PULL before teardown.

## Scope / honesty (c9)

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). gpu_recipe 발사 시(team-lead cost-gate go): held-out 4/4 mirror-CE DESCENT 게이트(a_clm_gen_pipeline) → CORE `--engine conv` mount 위 frozen G1(H_1129 recombination)·G6(H_1464 fals) byte-exact engine-native 재측정(torch probe 아님) → ckpt PULL before teardown(a_fire_recover_complete). cheap_test 가 numpy mirror 이므로 그 결과도 DIRECTIONAL(엔진-네이티브 아님).
