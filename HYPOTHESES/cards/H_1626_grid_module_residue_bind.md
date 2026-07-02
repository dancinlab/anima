# H_1626 — Entorhinal grid-module residue (CRT) compositional mouth

- **tier:** 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy, no engine); gpu_recipe = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** archbrainstorm — 84-family anima-native synthesis-binding architecture census (binding-wall program, H_1603)
- **lens:** bio-neuro: entorhinal grid-cell modular periodic code as a residue number system (Fiete/Burak; Hafting-Moser grid modules); algebraic CRT decode is the binding-recovery mechanism.
- **artifacts:** `state/binding_arch_census/BRAINSTORM_INDEX.md`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1449 (attention-block INERT@1blk) · H_1602 (recombination-objective prereg)
- **key:** `grid_module_residue_bind`

## Mechanism

Borrow the entorhinal grid-cell multi-modulus periodic code as an EXACT algebraic binder. Each leg is projected to residues across several coprime periodic moduli (a learned set of low-dim ring/von-Mises bases, one per grid module). Binding of two legs = per-module residue combination (modular add for compositional position, learned bilinear within-module for feature×role); the conjunction is represented as the joint residue vector. Readout decodes via a Chinese-Remainder-Theorem-style consensus layer (a sparse winner across modules whose residues agree picks the unique combined code), feeding the mouth's output distribution.

## Why it crosses the binding wall

Unlike product_key_factored_bind (learned Cartesian codebook lookup) or hippocampal_index_conjunction (sparse pattern-separated hashing), the residue code is a positional NUMBER SYSTEM: M coprime moduli give product-of-moduli unique conjunctions with only sum-of-moduli units, and combination is exact lossless integer/phase algebra rather than approximate superposition. The conv/attention wall is the lack of any exact factor-recoverable bind; CRT consensus makes the two legs algebraically RECOVERABLE within one forward. Ablation: replace coprime moduli with identical moduli (kills CRT uniqueness) → capacity collapses to a single modulus and binding fails despite identical param count, isolating the residue-coprimality as the binder.

## Cheap test (frozen-first · $0 · decisive numpy probe)

Frozen numpy: encode integers 0..63 as residues mod {3,5,7} (coprime) vs mod {4,4,4} (degenerate control); train a tiny readout to recover held-out (a,b)→(a+b mod 64) sums never seen as pairs. Pre-registered bar: coprime residue ≥ 0.80 on held-out sums, degenerate-modulus control ≤ baseline-additive ~chance. Decision: if coprime arm doesn't beat both degenerate-control and additive-MLP, drop. Extend to a 2D feature×role variant (modular-mul) for the bind-specific signal. $0, CPU.

## GPU recipe (cost-gated · PRE-REGISTER ONLY · NOT fired)

PRE-REGISTER ONLY. 303M mouth: conv trunk → M=4 grid-module heads (coprime ring dims) → CRT-consensus readout layer → byte logits. Coprime arm vs degenerate-moduli ablation arm trained identically on 4-cell balanced corpus, held-out CE gate. Engine-native frozen bars (G6 fals>0, G1 recombination ≥ baseline) via cli/anima.hexa on CORE; degenerate ablation must FAIL. Note new engine op needed (residue/CRT layer) — engine-transform-to-fit (a_engine_native_learning). ~1-2 H100-days.

## Scope / honesty (c9)

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). gpu_recipe 발사 시(team-lead cost-gate go): held-out 4/4 mirror-CE DESCENT 게이트(a_clm_gen_pipeline) → CORE `--engine conv` mount 위 frozen G1(H_1129 recombination)·G6(H_1464 fals) byte-exact engine-native 재측정(torch probe 아님) → ckpt PULL before teardown(a_fire_recover_complete). cheap_test 가 numpy mirror 이므로 그 결과도 DIRECTIONAL(엔진-네이티브 아님).
