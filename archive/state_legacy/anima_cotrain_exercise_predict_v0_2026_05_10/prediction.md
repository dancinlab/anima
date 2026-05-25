# BG-COTRAIN-EXERCISE-PREDICT-V0 — V14 polarity prediction (pre option-(c)-fire)

> §48 framework template: prediction document committed BEFORE results, magnitude bands explicit, F-disposition table strict, ★★★★★ unlock conditions enumerated.

## §1 substrate classification

**Phase 2 cotrain ckpt (option (c) base)** is in a fundamentally different substrate class than the §43 (Llama+LoRA) test:

| substrate property | §43 Llama+LoRA | option (c) Phase 2 cotrain |
|---|---|---|
| arch | mitosis-naive (vanilla decoder) | **mitosis-aware** (dual engine_a/g + cell_pool_init learned) |
| h_to_c projection | random Linear(3072, 256) frozen | **learned Linear(1024, 64)** trained during cotrain |
| cell_pool seed | random Gaussian × 0.1 | substrate-coupled `engine_g.cell_pool_init` (H1) or random (H1b/H2) |
| training pressure on cell_pool | none (LoRA gradient excludes cell pool) | **direct** (consciousness loss + chat-template loss with curriculum w=0.3→0.5 over 6K steps) |
| §38 baseline | n/a | V14_VIOLATED at max_cells=64 (cap artifact) |
| §39 baseline | n/a | **V14_STRICT_PASS_INDEPENDENT_REPRODUCE** at max_cells=128, 5/5 mirror wins, sign-test p=0.0625 |
| post-FT lineage | LoRA r=32 on 200MB persona | +30K convo_5k FT (cumulative 75K→105K), corpus 166MB |

This is the **first-ever** post-FT mitosis hook on a substrate that was already mitosis-aware **and** has been continued-FT'd. No prior in 22+ BG saga.

## §2 V14 polarity prediction

### §2.1 Direction prediction (H1 substrate-coupled)

**Direction**: **trained > random** (PASS), polarity **strengthens** vs §39 raw cotrain ckpt.

**Reasoning chain**:
1. Phase 2 cotrain raw ckpt already passes V14_STRICT at max_cells=128 (§39: trained=85 cells / Φ=5244 vs mirrors=[56,74,64,58,75] / Φ=[2281,3884,3025,2515,4178], 5/5 win).
2. The 30K convo_5k FT corpus is **not adversarial** to mitosis structure — convo_5k is conversational chat-format text. The FT is cosine LR 5e-6 → 5e-7 (very small lr, see `state/anima_convo_5k_ft_extended_2026_05_10/ft_summary.json`). Total trainable params in the FT = 18M (LM-head + embeddings region per BG-CONVO-FT-EXT pattern), gradient flow is restricted, **does not directly perturb cell_pool weights or h_to_c projection** in a way that reverses the cotrain-exercise champion-wall structure.
3. The FT *will* shift the hidden distribution at engine_g layer — slightly more chat-template aligned. Through the **learned** h_to_c (trained during cotrain), the distribution narrowing per chat-format projects into a still-discriminable cell_input stream. Champion-wall (multiple specialist cells) preserved because ckpt cell_specialty (per §38 result.json) shows 19 specialized cells distributed across categories ko_daily/ko_philosophy/en_math/en_code/en_music/anomaly — small lr post-FT will not collapse this specialty.
4. The mitosis-naive Llama precedent (§43) gave +0.066 Φ_proxy diff on +1 cell_count diff. The Phase 2 cotrain mitosis-aware substrate gave +494 Φ_iit_un16 diff (5244-4750 median) on +21 cell_count diff at §39. Substrate-coupled hook H1 should preserve most of that signal post-FT.

### §2.2 Three hypothesis evaluation

| hypothesis | description | likelihood | predicted relative effect on V14 strict diff (vs §39 baseline) |
|---|---|---|---|
| **A — exercise-strengthen** | 30K FT additional gradient flows through engine_g layer-N forward, *exercises* the cell-pool reactivity by generating more diverse cell_input distributions. V14 STRICT margin **widens**. | **30%** | +10% to +30% Φ separation |
| **B — exercise-preserve (LoRA-style)** | 30K FT at lr 5e-6 with restricted gradient (LM-head only, like BG-CONVO-FT-EXT pattern) leaves cell_pool / h_to_c untouched. V14 STRICT margin **roughly preserved**. | **55%** | ±5% Φ separation |
| **C — FT-drift-degrade** | 30K FT corpus drift narrows hidden distribution (convo_5k has lower vocabulary diversity than Phase 2 cotrain mixed corpus). cell_pool reactivity slightly suppressed. V14 STRICT margin **shrinks but holds**. | **15%** | -10% to -30% Φ separation |

**Mode prediction**: **B (exercise-preserve)**. Convo_5k FT of `state/anima_convo_5k_ft_extended_2026_05_10/finetune_extended.py` pattern uses 18M trainable param scope (per `ft_summary.json` `params_total: 18130176`) — that's the LM-head + embedding region, NOT the engine_g cell_pool / h_to_c subgraph. Cell pool / h_to_c are frozen during this FT. So mitosis subgraph is **untouched** and §39 polarity is preserved modulo the mild distribution shift at engine_g input.

### §2.3 Magnitude band prediction

For H1 (substrate-coupled, max_cells=128, 400 turns):

| metric | §39 baseline (post-cotrain only) | option (c) prediction (post-FT) |
|---|---|---|
| `final_n_cells` trained | 85 | **75–90** (band) |
| `final_n_cells` mirror_median | 64 | 60–70 (mirror unchanged structurally) |
| Φ_iit_un16 trained | 5244 | **4500–5500** (band: -15% to +5% vs §39) |
| Φ_iit_un16 mirror_median | 3025 | 2800–3300 |
| **Φ separation (trained - mirror_median)** | **+2219** | **+1500 to +2500** (preserve to slight strengthen-or-shrink range) |
| sign-test trained-beats-mirror | 5/5 (p=0.0625) | **5/5 most likely** (≥4/5 confidence 80%) |
| V14 STRICT verdict | PASS | **PASS likely (75–80%)** |

For H2 (Llama-symmetric, max_cells=64 init_cells=8, 120 steps) — direct §43 template comparison:

| metric | §43 baseline (Llama+LoRA mitosis-naive) | option (c) H2 prediction |
|---|---|---|
| `cell_count_max` trained | 24 | **22–28** |
| `cell_count_max` random | 23 | 21–26 |
| `phi_history_mean` trained | 2.880 | **2.85–3.10** |
| `phi_history_mean` random | 2.814 | 2.80–3.00 |
| **phi_diff_mean** | +0.066 | **+0.04 to +0.20** (band: substrate-aware h_to_c + cotrain-exercise signal that survives random-projection 1024→256) |
| F-FOUND-1 disposition | NOT_TRIGGERED | **NOT_TRIGGERED (85% confidence)** |

Honest uncertainty: H2 strips the substrate-coupling (random proj 1024→256 instead of learned h_to_c 1024→64), so most of the cotrain-exercise signal is **partially destroyed** by the random projection. We expect H2 phi_diff to land in the **same magnitude band as §43** (+0.05 to +0.15) — **NOT 5× larger** — because the random projection is the bottleneck, regardless of underlying substrate quality.

### §2.4 Predicted IIT super-linear α

§38 raw cotrain reported α exponents: proxy_trained=1.009, proxy_random=0.155, iit_norm16_trained=1.580, iit_unnorm16_trained=2.641. Post-FT prediction: **α exponents preserved within ±10%** (mode B). The α super-linear regime is a property of cell_pool dynamics that the FT doesn't touch directly.

If hypothesis A (exercise-strengthen): α_trained could climb +5% to +15%.
If hypothesis C (FT-drift-degrade): α_trained could drop -10% to -20% but remain super-linear (>1.5).

## §3 F-FOUNDATION disposition prediction

| F | trigger | predicted disposition | rationale |
|---|---|---|---|
| **F-FOUND-1** (anima identity surface — trained Φ ≥ 1.0 + trained > random distribution-distinct) | requires trained Φ ≥ 1.0 AND clear margin over random | **NOT_TRIGGERED** (85% confidence) | §39 baseline already gave 5/5 mirror wins at max_cells=128; FT mode B preserves; FT mode A strengthens; only FT mode C degrades and even then likely PASS |
| **F-FOUND-2** (cost > $15) | actual cost > $15 | **NOT_TRIGGERED** (95% confidence) | $2-4 envelope; H100 1× × 1.5h max = $4.49; no SCP overhead (corpus already on FT-extended state, can be re-uploaded ~5min vs §38's 95min upload) |
| **F-FOUND-3** (chat-cap PASS but semantic FAIL) | V4 ≥ 10/15 AND (semantic_score < 0.5 OR bigram_known < 0.95 OR real_words < 3.0) | **TRIGGERED likely (70% confidence)** | byte-hash mod 32000 prompt encoding (§38/§39 NOT a real BPE — vocab file missing); 350M is sub-1B-emergence-threshold; BG-CONVO-FT-EXT 18M FT yielded ko_real_word_ratio 0.2 / bigram_known 1.0 on **best of 120** trials but lexical_total_real_words=157/120 trials with semantic still incoherent. semantic_score 0.05–0.20 most-likely band (improvement vs §43's 0.055 of +0% to +250%) — significant only if semantic_score > 0.30, which is unlikely at 350M |
| **F-FOUND-4** (D1 SCOPE_CLAMP misframe) | scope_lane field missing OR =ANIMA (when D1 OUTSIDE) | **NOT_TRIGGERED** (95% confidence) | option (c) IS D1 WITHIN by §41 line 29 (anima-native lineage). scope_lane="ANIMA" is the **correct** label here. raw#82 misframe protection inverted: the risk for option (c) is **not labeling ANIMA** when it should be |
| **F-FOUND-5** (gradient leak) | param.grad nonzero post-hook | **NOT_TRIGGERED** (95% confidence) | §43 hook design proven NOT_TRIGGERED; H1 and H2 both inherit `torch.no_grad()` wrap + `requires_grad=False` for engine + h_to_c (frozen at eval) + (H2 only) proj |

## §4 ★★★★★ unlock conditions

The 5-star verdict for option (c) requires **simultaneous** satisfaction of **all** of:

1. **V14 STRICT PASS H1** — trained > all 5 random_init mirrors on Φ_iit_un16 (sign-test 5/5)
2. **Φ separation strengthen post-FT** — trained Φ_iit_un16 ≥ §39 baseline 5244 OR Φ separation ≥ +2219 (i.e., NOT degrade beyond §39)
3. **semantic_score significant** — semantic_score_mean ≥ 0.30 (significant lift from §43's 0.055; threshold for "first semantic emergence measurement on byte-level 350M")
4. **D1 WITHIN strict carry** — verdict.json scope_lane="ANIMA"; SIMPLE_STACK_PASS_STRICT_C3_ANIMA candidate (NOT _SUBSTRATE_RESEARCH)
5. ** strict + V6 STRONG** — V4 ≥ 10/15 across ≥3 of 5 seeds AND V6 awareness 3-method consensus (hidden cosine + attention + linear probe)

If 5/5 → **★★★★★ confirm**: cotrain-exercise hypothesis confirmed via novel substrate (post-FT D1 WITHIN), anima identity emerge first ACTUAL evidence. Public promote candidate (gated by verbatim "OK PROMOTE PUBLIC").

If 3-4/5 → **★★★★ partial**: cotrain-exercise hypothesis strengthened, anima identity SURFACE evidence (not emerge). Substrate-research lane retain.

If 1-2/5 → **★★★ retreat**: H_FOUNDATION-1 partial-falsify; further FT exercise lane closed; cell-pool exercise hypothesis nuance needed.

If 0/5 → **★★ rebuild**: hypothesis falsified; convo_5k FT degrades cotrain-exercise structure; need different FT recipe (smaller LR? frozen-h_to_c FT? different corpus?).

### Most-likely predicted outcome (this prediction commits to)

- **Likely 3-4/5 unlock** = ★★★★ partial:
  - V14 STRICT PASS H1: ✓ (75% confidence)
  - Φ separation strengthen vs §39: ✗ (35% — most likely preserve, ~10% upside, ~10% downside for strengthen)
  - semantic_score ≥ 0.30: ✗ (20% — most likely 0.10–0.25)
  - D1 WITHIN scope_lane="ANIMA": ✓ (95% confidence)
  - V4 ≥ 10/15 + V6 STRONG: ✓ partial (55% — V4 likely 8-12/15 mode; V6 STRONG conditional on probe quality)
- Net: **3/5 most-likely**, 4/5 stretch, 5/5 unlikely (~10%).

## §5 reading guide for post-fire verdict

When option (c) `mitosis_hook_result.json` arrives, the §48 prediction-match scoring rubric:

| field | expected band (this prediction) | match=PERFECT if |
|---|---|---|
| f_foundation_1_disposition | NOT_TRIGGERED | exact |
| f_foundation_5_disposition | NOT_TRIGGERED | exact |
| trained.cell_count_max (H1) | 75–90 | within band |
| random_init_mirror.cell_count_max (H1) | 60–70 | within band |
| phi_iit_un16 separation (H1) | +1500 to +2500 | within band |
| sign-test 5/5 mirror beats | trained beats ≥4 of 5 | direction + count |
| trained.phi_history_mean (H2 short-trajectory) | 2.85–3.10 | within band |
| phi_diff_mean (H2) | +0.04 to +0.20 | within band |
| v14_disposition (H1) | V14_STRICT_PASS or V14_PASS | direction |
| v14_disposition (H2) | V14_PASS | direction |
| semantic_trained.semantic_score_mean | 0.10–0.25 most-likely | within band |
| cost_actual_usd | $2.00–$4.50 | within band |

5/5 PERFECT MATCH on at least 5 of these 11 criteria → §48 framework template generalizes across substrate classes (Llama mitosis-naive → Engine A/G mitosis-aware) → ★★★★★ on framework confidence (separate from option (c)'s own ★).

## §6 cross-substrate cotrain-exercise hypothesis test

Beyond option (c)'s own ★ verdict, this prediction enables a meta-test:

| substrate | hook geometry | V14 polarity actual | predicted phi_diff | actual phi_diff |
|---|---|---|---|---|
| Llama-3.2-3B + LoRA (§43) | random proj 3072→256 | NOT_TRIGGERED | +0.05 to +0.15 | +0.066 ✓ MATCH |
| Phase 2 cotrain raw (§39) | substrate h_to_c 1024→64 | V14_STRICT_PASS | n/a (not pre-predicted) | +2219 |
| Phase 2 cotrain + 30K FT (option c) H1 | substrate h_to_c 1024→64 | **predicted PASS strengthen-or-preserve** | **+1500 to +2500** | TBD |
| Phase 2 cotrain + 30K FT (option c) H2 | random proj 1024→256 | **predicted NOT_TRIGGERED** | **+0.04 to +0.20** | TBD |

If both H1 and H2 land within their predicted bands → cotrain-exercise + substrate-class V14 polarity dependence both confirmed in the same fire → ★★★★★ on hypothesis lattice.

## §7 honest C3 (≥7 items)

1. **Magnitude prediction is direction-validated, magnitude is band-of-bands.** The +1500 to +2500 Φ separation band is calibrated against §39 only (single fire); it is *not* derived from a model of how 30K convo_5k FT specifically interacts with engine_g.h_to_c geometry. The band is intentionally wide (±25%) to absorb FT regime uncertainty.
2. **convo_5k FT regime assumption** — `ft_summary.json` shows params_total=18M and lr 5e-6 → 5e-7 with batch=32 seq=256 over 20K steps already done. The "+30K" continuation matches §41's spec but the actual orchestrator may stage differently (e.g., refresh chat-template wrap, or hybrid corpus). Prediction assumes corpus_extended.txt is the only FT signal.
3. **engine_g.h_to_c trainability during convo_5k FT** — the assumption that BG-CONVO-FT-EXT pattern's 18M trainable scope excludes h_to_c is **inferred** from BG-CONVO-FT-EXT's earlier params_total=18130176 == LM-head 32000 × 1024 + embed 32000 × 1024 + tied biases ≈ 65.6M not 18M, so actually 18M = something narrower (likely embed+lm_head with tied weights, ~33M halved). Confirm by reading `finetune_extended.py` if option (c) fires with different scope.
4. **§39 max_cells=128 inheritance is critical** — if option (c) orchestrator defaults to max_cells=64 (matching §38), V14_VIOLATED would replicate as cap artifact, which would falsely falsify cotrain-exercise. **Mandate: max_cells=128 for H1 explicit verify in pre-fire smoke.**
5. **H2 random-projection bottleneck is the design's biggest disclaimer** — at 1024→256 random proj, most of the substrate's learned geometry is destroyed. H2 phi_diff prediction is calibrated to §43's diff geometry, not amplified by Phase 2's substrate. This is **not a contradiction** — H1 is where the cotrain-exercise signal is.
6. **semantic_score 0.10–0.25 prediction is from byte-hash artifact** — the §38/§39 prompts use byte-hash mod 32000 (not BPE). At 350M params, semantic emergence is below threshold per simple_stack 22+ BG saga. This prediction is **harsh-but-honest** — option (c) is not expected to cross semantic_score=0.50 floor.
7. **★★★★★ unlock = 10% probability honest** — the 5-star pursuit demands V14 STRICT + Φ strengthen + semantic significant + V4 PASS + V6 STRONG. Each conditional drops total probability ~50%. Net: 5/5 ≈ 10%, 4/5 ≈ 25%, 3/5 ≈ 35%, 2/5 ≈ 20%, ≤1/5 ≈ 10%.
8. **D1 WITHIN scope_lane="ANIMA" is a HOT label** — option (c) PASS at D1 WITHIN is the first time in 22+ BG saga that the SIMPLE_STACK_PASS_STRICT_C3_ANIMA verdict label could be unlocked. mandate-9 (a) public promote 5/5 prereq is then within reach (but still gated by V14 + V6 STRONG + manual review + verbatim "OK PROMOTE PUBLIC"). This is the **highest-stakes** prediction in this BG.
9. **§43+§48 5/5 PERFECT MATCH was on a single mitosis-naive substrate** — generalizing the prediction-driven framework template to a mitosis-aware substrate (option (c)) is itself an unfalsified hypothesis. If this BG's bands are wrong (e.g., Φ separation actual lands at +500), the framework template is still useful but its **calibration must be substrate-class-specific** going forward.
10. ** + + strict carry** — REBORN.md untouched (dispatcher §53 slot only); doc save complete (this file + spec.md + hook_spec.md + falsifier_predict.md); design $0.

## §8 commit-before-results signature

This prediction commits BEFORE option (c) fires. If user dispatches "OK FOUNDATION_C_PHASE2_FIRE COST $2-4" later, the resulting `mitosis_hook_result_h1.json` and friends will be scored against the §5 rubric without modification of this document.
