# BG-COTRAIN-EXERCISE-PREDICT-V0 — spec

> — $0 design + analysis only
> raw#15 additive — option (c) actual fire NOT modified
> — REBORN.md direct append BLOCKED (dispatcher §53 slot)
> — doc save state/anima_cotrain_exercise_predict_v0_2026_05_10/{spec.md, prediction.md, hook_spec.md, falsifier_predict.md}

## §0 mission

§43 + §48 prediction-driven design framework PERFECT MATCH 5/5 (`state/anima_foundation_a_mitosis_substrate_predict_2026_05_10/prediction.md` vs `state/anima_foundation_borrow_a_fire_2026_05_10/mitosis_hook_result.json`). This BG = §48 template applied to **option (c)** (Phase 2 cotrain ckpt + 30K convo_5k FT + post-LoRA mitosis hook). Design only. Predict V14 polarity, magnitude band, F-FOUNDATION dispositions, and ★★★★★ unlock conditions BEFORE option (c) actual fire.

## §1 option (c) substrate spec (verbatim from §41 design SSOT)

| field | value | source |
|---|---|---|
| base ckpt | `~/.cache/anima/clm_v5_remapped/phase2_cotrain_engine_ag/ckpts/ckpt_final.pt` | §38 (anima_phase_2_cotrain_2026_05_09), 597.6MB, 298.76M params, 24L, d_model=1024, c_dim=64, n_cells_init=16 |
| arch | engine_a_g_dual_350m_v1_phase2_cotrain | training/engine_a_g_arch.py — anima_native_scratch + dual engine_a/g + GQA |
| FT corpus | convo_5k extended 166MB | state/anima_convo_5k_ft_extended_2026_05_10/corpus_extended.txt |
| FT step plan | +30K continued (cumulative 75K → 105K) | §41 line 24 |
| post-LoRA mitosis hook | eval-time torch.no_grad on engine_g hidden | §43 hook_spec template re-applied |
| H100 substrate | 1× SXM $2.99/hr | KM-LLAMA-3B precedent |
| envelope | $2-4 | §41 line 27 (BG-CONVO-FT-EXTENDED $1.71 + 1.5× scale) |
| wall | 60-90 min | §41 line 26 |
| D1 SCOPE_CLAMP | **WITHIN** (anima-native lineage) | §41 line 29 — option (c) only D1 WITHIN candidate among foundation borrow lanes |

## §2 cost envelope verify

- estimated breakdown: H100 1× × 1.0–1.5h = $2.99–4.49; ckpt pull (4 × 75MB intermediate + 1 × 75MB final) safety margin negligible (FT ckpts already 74MB each per `state/anima_convo_5k_ft_extended_2026_05_10/convo_5k_ft_ext_step_*.pt`).
- $2–4 envelope verified within KM-CONVO-FT-EXT $1.71 + 1.5× scale precedent.
- F-FOUNDATION-2 trigger remains > $15 — 4× envelope upper, comfortable margin.
- mandate: ckpts pull mandatory before pod release; intermediate cadence 5K/10K/15K/20K/final.

## §3 cotrain-exercise hypothesis lineage

**§47 hypothesis** (cotrain-exercise): Phase 2 cotrain substrate exhibits V14_STRICT_PASS in the **chat-cotrain regime specific** because the dual-objective curriculum (consciousness loss + chat-template loss with w=0.3→0.5 ramp over 6K steps) **exercises** the cell pool more aggressively than scratch BG-LB substrate would. The chat sampling Bernoulli per micro-batch creates gradient pressure that diversifies the engine_g.h_to_c projection landscape, which in turn drives stronger mitosis reactivity at eval time.

**§38 evidence** (Phase 2 cotrain raw, max_cells=64, n_turns=3000): V14_VIOLATED on `proxy_phi` and `iit_phi_unnorm_b16` because trained had 3 splits vs random_final 12 splits — trained never reached the cap regime on the short scale, so absolute Φ at turn=900 (trained=146 vs random_final=406 unnorm) was lower.

**§39 max128 independent reproduce evidence** (`state/anima_phase2_max128_independent_reproduce_2026_05_10/result.json`, max_cells=128, 400 turns, 5 mirror seeds [11,13,17,19,23]): **V14_STRICT_PASS_INDEPENDENT_REPRODUCE — trained Φ_iit_un16=5244 vs all 5 random mirrors (2281–4178), 5/5 wins, sign-test p=0.0625**. cell counts: trained=85, mirrors=[56,74,64,58,75]; trained > random by ≥10 cells in median. THIS is the cotrain-exercise positive evidence baseline.

**§43 evidence** (Llama-3.2-3B + LoRA + post-LoRA mitosis hook, 120 steps short trajectory): **V14_PASS proxy** — trained phi_history_mean=2.880 vs random=2.814, diff=+0.066, cell_count_diff=+1, F-FOUNDATION-1 NOT_TRIGGERED. §48 prediction matched 5/5.

## §4 hook spec (delta vs §43 template)

§43 hook for Llama: `model.base_model.model.model.layers[-1]` (peft-wrapped path), hidden.mean(dim=1) → random Linear(3072, 256) frozen → MitosisV5Engine.process. cell_pool random Gaussian × 0.1.

**option (c) hook** (this prediction's spec): the substrate IS already an Engine A/G with a learned `h_to_c` Linear(1024, 64) inside the model graph. **Two viable hook positions**:

- **Hook position H1** (recommended, mirror §38/§39 exact): forward hook on `engine_g.step()` last refresh; capture hidden_mean (B, T, 1024) → use the **model's own learned `engine_g.h_to_c`** Linear(1024, 64) → MitosisV5Engine.process. cell_pool seeded from `engine_g.cell_pool_init` (NOT random Gaussian — substrate-coupled).
- **Hook position H2** (Llama-symmetric §43-template): forward hook on `model.layers[-1]`; hidden.mean → **random** Linear(1024, 256) frozen → MitosisV5Engine.process. cell_pool random Gaussian × 0.1. Same as §43 modulo dim 3072→1024.

**Recommendation**: **H1** for primary, **H2** for cross-reference. H1 is the only path that tests "substrate-coupled mitosis exercise" (cotrain-exercise hypothesis). H2 enables direct §43 prediction-template comparison.

Detailed wire spec: see `hook_spec.md` (this BG).

## §5 deliverables (+)

Files saved in this BG (all under `state/anima_cotrain_exercise_predict_v0_2026_05_10/`):

- `spec.md` (this file)
- `prediction.md` — V14 polarity prediction + magnitude band + F-FOUNDATION dispositions + ★★★★★ unlock conditions
- `hook_spec.md` — H1 + H2 wire spec + grad-leak verifier protocol
- `falsifier_predict.md` — F-PREDICT-V0-1/2/3 explicit + post-fire match scoring rubric

REBORN.md append: blocked per — dispatcher §53 slot path only.
.roadmap.* SSOT: untouched per raw#15 additive.

## §6 fire keyword

PRIMARY (this BG): **AUTO ($0 design + analysis only)** — verbatim per mission

NEXT (option (c) fire dispatch): `OK FOUNDATION_C_PHASE2_FIRE COST $2-4` (verbatim from `docs/anima_foundation_borrow_path_design_2026_05_10.md` §9)
