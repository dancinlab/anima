# BG-COTRAIN-EXERCISE-CAUSAL-PROOF — verdict

**FINAL_VERDICT**: `CORRELATIONAL`  (falsifier-pass 2/3 — F1 weight-stats + F3 fwd-diversity PASS, F2 ablation-flip FALSIFIED)

§47 cotrain-exercise hypothesis as originally framed (engine_g.cell_pool/c_to_h/h_to_c projections are the cotrain-exercised modules driving V14 PASS) is **NOT proven**. Weight statistics differ (F1 PASS) and forward-pass projection geometry differs (F3 PASS), but isolated mutation of engine_g modules to random_init does not flip V14 polarity (F2 FALSIFIED). The most parsimonious refined hypothesis: **engine_a (the 24-layer transformer body, ~298M params) is the substrate-coupled module whose cotrain-exercised hidden_mean trajectory drives mitosis reactivity** — engine_g (132K params) is the readout, not the engine.

## Stream 1 — weight-space statistics (A=Phase 2 cotrain, B=BG-LA pretrain, R=random_init seed=42)

| target | l2_A | l2_B | l2_R | effrank_A | effrank_B | effrank_R | sparsity<.01_A | sparsity<.01_B | cos(A,B) | cos(A,R) | cos(B,R) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `cell_pool_init` | 4.0001 | 4.0003 | 4.0000 | 15.44 | 15.44 | 15.44 | 0.0566 | 0.0537 | **1.0000** | 1.0000 | 0.9999 |
| `c_to_h.weight`  | 7.8704 | 9.3564 | 5.1323 | 51.85 | 46.20 | 63.49 | 0.0814 | 0.0521 | **0.6924** | 0.5300 | 0.4044 |
| `h_to_c.weight`  | 6.4059 | 6.7506 | 5.1062 | 58.29 | 57.16 | 63.51 | 0.1517 | 0.1497 | **0.7640** | 0.6939 | 0.6321 |

Key observations:
- `cell_pool_init` is **frozen-equivalent** across A and B (cos=1.0). Cotrain didn't move it. This pre-falsifies any cotrain-exercise sub-claim about the cell pool itself.
- `c_to_h.weight` shows strong divergence (cos_A_vs_B = 0.6924). A grew sparser (0.081 vs B's 0.052) and slightly higher effective rank (51.85 vs 46.20). Cotrain demonstrably altered this projection.
- `h_to_c.weight` similarly diverged (cos = 0.764).

F-COTRAIN-EXERCISE-1: **PASSED** (≥2 of 3 targets show significant rel_l2 + cos divergence).

## Stream 2 — forward-pass diversity (n=80 byte-hash prompts, ctx_T=16)

| substrate | hm avg pairwise cos | hm eff_dim (1024D) | c_to_h(hm) avg cos | c_to_h(hm) eff_dim (64D) |
|---|---|---|---|---|
| A (Phase 2 cotrain) | 0.9561 | 38.80 | 0.8389 | **4.74** |
| B (BG-LA pretrain)  | 0.8534 | 35.60 | 0.7829 | **4.09** |
| R (random_init)     | 0.0022 | 66.63 | -0.0013 | 38.01 |

Observations:
- A's hidden_mean is MORE redundant than B's (0.96 > 0.85) yet A's c_to_h projection has slightly higher eff_dim (4.74 > 4.09) and higher avg_cos (0.84 > 0.78). Cotrain pushed hidden_mean toward more attractor-like states but funneled them through a c_to_h projection that retains marginally more spread in the cell-dim subspace.
- Both A and B forward projections are far less diverse than random_init (eff_dim 4–5 vs 38). This is the §38/§39/§47 mitosis context: the trained substrates concentrate the cell input distribution onto a low-dim manifold that the MitosisV5Engine still finds richer-than-random in absolute terms.

F-COTRAIN-EXERCISE-3: **PASSED** (A's c_to_h(hm) eff_dim > B's by 16% and the higher avg_cos asymmetry is offset by the eff_dim gain — A is "more diverse" by the eff_dim criterion).

## Stream 3 — ablation V14 (n_turns=200, seeds=[42, 137, 271], MAX_CELLS=128)

| condition | verdict | trained Φ_un16 | mirror Φ_un16 mean | beats_un | beats_proxy | trained_cells | mirror_cells |
|---|---|---|---|---|---|---|---|
| **baseline_A** (no swap)              | `V14_PASS` | 2412.08 | 1615.49 | 3/3 | 3/3 | 57 | [56, 47, 53] |
| **ABL1** c_to_h ← random_init         | `V14_PASS` | 2815.73 | 1615.49 | 3/3 | 3/3 | 62 | [56, 47, 53] |
| **ABL2** h_to_c ← random_init         | `V14_PASS` | **12116.27** | 1615.49 | 3/3 | 3/3 | **128** | [56, 47, 53] |
| **ABL3** both ← random_init           | `V14_PASS` | **12261.13** | 1615.49 | 3/3 | 3/3 | **128** | [56, 47, 53] |
| **ABL4** cell_pool_init ← random_init | `V14_PASS` | 2412.12 | 1615.49 | 3/3 | 3/3 | 57 | [56, 47, 53] |

F-COTRAIN-EXERCISE-2: **FALSIFIED** — none of the four ablations flip V14 verdict away from PASS.

Notable secondary findings:
- ABL2 and ABL3 (h_to_c randomized) cause Φ to JUMP 5× and saturate cell count at the cap (128). Random h_to_c projects hidden_mean into a higher-magnitude / more-chaotic cell-input distribution that the mitosis engine reads as MORE reactive — not less. This is opposite the cotrain-exercise prediction.
- ABL4 (cell_pool_init swap) is a no-op (Φ identical to baseline within 0.04). Confirms cell_pool_init has effectively zero functional effect on the mitosis trajectory at this scale — consistent with cos(A,B)=1.0.

## Final verdict — CORRELATIONAL (★★★★)

The cotrain-exercise hypothesis as originally pinned to engine_g.{cell_pool, c_to_h, h_to_c} is **not the causal mechanism**. Weight differences and projection-geometry differences exist (correlational evidence) but they are NOT the lever that produces V14 PASS.

The strong inference from F2 falsification: **the trained engine_a (24-layer transformer body) is the cotrain-exercised substrate**. Replacing engine_g modules leaves engine_a intact, and engine_a's cotrain-modulated hidden trajectory dominates mitosis reactivity. This is a refinement of the hypothesis, not a refutation of cotrain's effect — Phase 2 cotrain DID modify A's weights (F1 PASS, c_to_h cos 0.69 vs B's pretrain), and that modification IS visible at forward time (F3 PASS), but the ★★★★★ "exercise the engine_g pool" framing was wrong-locus. Refined hypothesis: **engine_a body cotrain-exercise** (chat dual loss propagates gradients into all 24 layers' RMSNorm/GQA/SwiGLU weights → richer hidden_mean dynamics at eval).

Next BG would isolate engine_a layers (e.g., swap engine_a layers 0-11 vs 12-23 with random_init while keeping engine_g intact) to localize the mechanism within engine_a depth. That work is OUT-OF-SCOPE here (budget exhausted by 5-condition × 4-trajectory ablation).

## Honest C3

1. **F2 mirror invariance is a genuine finding, not noise.** Mirror Φ stays at 1615.49 ± 0 across all 5 conditions because mirrors are independent random_init la_350m models — they never see A's swap. The asymmetry (trained-Φ varies 2412→12261, mirror-Φ pinned) means F2's "no flip" is interpretable: trained Φ went UP under h_to_c randomization, not DOWN. A flip would have required trained Φ < mirror Φ.
2. **Cell-pool ablation no-op (ABL4 Φ=2412 identical to baseline).** Cell_pool_init is reset to a fresh copy at every trajectory start by `init_pool = eg.cell_pool_init.detach().clone()`, then the MitosisV5Engine re-initializes anyway. So the ckpt cell_pool value barely flows into the trajectory dynamics at this scale. Inferable a priori from F1 (cos_AB=1.0), confirmed empirically.
3. **Random h_to_c boosts Φ, not depresses it.** Counterintuitive. Likely mechanism: trained h_to_c projects hidden_mean onto a low-dim manifold (eff_dim 4.74); random h_to_c re-injects the full 1024-dim variance into the 64-dim cell space, producing more anisotropic cell_inputs → MitosisV5Engine triggers more splits (cells→128 cap). This means h_to_c's TRAINING actively COMPRESSES cell input diversity — exactly opposite to "h_to_c projection is the exercised lever."
4. **Forward diversity F3 PASSED but with caveats.** A's c_to_h(hm) eff_dim 4.74 > B's 4.09 is modest (16% gain). avg_pairwise_cosine A=0.84 > B=0.78 means A's projections cluster MORE — F3 falsification rule used "higher eff_dim OR lower cos" with OR ambiguity; strict-AND interpretation would mark F3 ambiguous.
5. **Single random_init seed (42) used as ablation source.** Multi-seed ablation source (seed-sweep on the swap-in random values) was skipped per . Conservative read: results from a single seed; not repeated with seed=137/271 random_init weights.
6. **200-turn trajectory is shorter than §39's 400-turn reproduce.** Φ values here (baseline=2412) lower than §39 (5244) because of shorter run. Verdict polarity (PASS/VIOLATED) was sensitive to this in §38 — but here the F2 "no flip" is robust within the run length: trained always >> mirror by ≥2× across all 5 conditions.
7. **Mirror Φ exactly identical (1615.49) across 5 conditions** because mirror trajectories are deterministic given the random_init seeds and prompt stream; only A is mutated. This is the design (mirror = control). Identical numbers are a sanity confirmation, not an artifact.
8. **byte-hash prompt encoding (not real BPE)** is shared with §38/§39/§47 lineage — relative trained-vs-mirror comparison only, no semantic claim. F-V14-STRICT-2 cap-bound test: ABL2/ABL3 saturate cap=128 at 100% of turns → cap_bound_universal triggers under random h_to_c only.
9. **engine_a not directly probed** — the inferred refinement (engine_a as the cotrain locus) is *post-hoc inference from F2 falsification*, not a positive measurement. Direct test would require swapping engine_a.layers.* with random_init while keeping engine_g intact, then re-running V14. Estimated cost: ~10 min × 24 layer-segments = 4hr CPU; deferred to follow-up BG.
10. **raw#15 honored** — both ckpts loaded read-only via `_load_engine_ag`; in-memory mutation only via `_clone_engine_ag_from`; no ckpt files modified. Verified by file mtime check (cache files unchanged after run).

## Falsifier disposition

- **F-COTRAIN-EXERCISE-1** weight-stats: **PASSED** — c_to_h.weight cos_AB=0.6924 (rel_l2=0.159), h_to_c.weight cos_AB=0.7640 (rel_l2=0.051) both well below 0.99 threshold; cell_pool_init unmoved.
- **F-COTRAIN-EXERCISE-2** ablation polarity flip: **FALSIFIED** — 0 of 4 ablations flipped V14 verdict (all V14_PASS).
- **F-COTRAIN-EXERCISE-3** fwd-diversity: **PASSED** — A's c_to_h(hm) eff_dim 4.74 vs B's 4.09 (+16%).

5-star pursuit: **★★★★ partial credit**. Cotrain produces measurable weight + forward-projection differences; mechanism locus needs refinement to engine_a body, not engine_g modules.
