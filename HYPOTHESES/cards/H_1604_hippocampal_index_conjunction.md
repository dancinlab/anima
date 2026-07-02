# H_1604 — CA3 Conjunctive-Attractor Mouth (DG sparse-separation -> CA3 pattern-completion)

- **tier:** 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy, no engine); gpu_recipe = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** archbrainstorm — 84-family anima-native synthesis-binding architecture census (binding-wall program, H_1603)
- **lens:** hippocampal index theory — dentate-gyrus pattern separation + CA3 autoassociative pattern completion (Marr; Treves-Rolls); conjunctive memory index.
- **artifacts:** `state/binding_arch_census/BRAINSTORM_INDEX.md`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1449 (attention-block INERT@1blk) · H_1602 (recombination-objective prereg)
- **key:** `hippocampal_index_conjunction`

## Mechanism

In one forward, the two legs (trunk context-state h_ctx and current-token feature h_tok) are concatenated and pushed through a dentate-gyrus sparse expansion with k-winners-take-all (k<<N) producing a high-dim sparse index where each active unit codes a (legA,legB) PAIR, not either marginally. That index seeds a CA3-style recurrent autoassociative attractor (learned Hebbian fast-weight matrix, ~3 settling iterations unrolled inside the forward) that pattern-completes to the stored bound assembly; the settled attractor is read to logits. Binding = a conjunctive sparse code that only exists when both legs are co-active, then hardened into a fixed point by completion.

## Why it crosses the binding wall

conv/attention combine values additively (convex combination over a value bank), so they cannot store a pair-specific code without O(pairs) capacity collapse. DG k-WTA gives near-orthogonal conjunctive codes (pattern separation) and the CA3 attractor makes the bound code a stable fixed point, so ambiguous/partial input completes to the JOINT pattern. Ablation: (a) 0 settling iters -> degrades to a sparse additive bag-of-features = G1 fails; (b) raise k toward N (kill sparsity) -> codes overlap, conjunctions interfere = fails. Passing only with both sep+completion attributes binding to those two ops, not to extra params. Distinct from a WM compose-buffer: there is no persistent scratchpad slot read/written across tokens — it is per-forward conjunctive completion.

## Cheap test (frozen-first · $0 · decisive numpy probe)

numpy mini, DIRECTIONAL. 2 latent factors A,B in {0..7}; target byte = T[A,B], a frozen 8x8 table with a non-additive (rank>1, A-xor-B-structured) component. Train on 75% of the 64 (A,B) pairs, HOLD OUT 25% of combos. Build DG (random sparse proj to 256 + k-WTA k=4) + CA3 (Hebbian outer-product memory, 3 settling iters) + linear readout, vs additive baseline (embA+embB->linear), equal params. Frozen bar (pre-registered): attractor held-out-combo CE < 0.3 nats AND additive baseline held-out CE >= 0.9x uniform. Decisive because additive provably cannot represent the non-additive table on held-out combos.

## GPU recipe (cost-gated · PRE-REGISTER ONLY · NOT fired)

PRE-REGISTER ONLY. 303M trunk with a DG+CA3 conjunctive head replacing the final mixing block (k-WTA ~4k-dim sparse, 3 settling iters unrolled, Hebbian fast-weights as learned params). Train on 4-cell corpus (ko/en x general/sns, a_chat_registers). Eval engine-native via cli/anima.hexa eval, frozen G1(recombine>=303M baseline) AND G6(fals>0). Bars frozen before run. ~1xH100 ~6h ~= $15; ckpt PULL before teardown (a_fire_recover_complete).

## Scope / honesty (c9)

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). gpu_recipe 발사 시(team-lead cost-gate go): held-out 4/4 mirror-CE DESCENT 게이트(a_clm_gen_pipeline) → CORE `--engine conv` mount 위 frozen G1(H_1129 recombination)·G6(H_1464 fals) byte-exact engine-native 재측정(torch probe 아님) → ckpt PULL before teardown(a_fire_recover_complete). cheap_test 가 numpy mirror 이므로 그 결과도 DIRECTIONAL(엔진-네이티브 아님).
