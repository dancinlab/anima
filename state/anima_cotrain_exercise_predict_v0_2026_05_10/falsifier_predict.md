# BG-COTRAIN-EXERCISE-PREDICT-V0 — falsifier prediction

> Mission §F: F-PREDICT-V0-1/2/3 explicit + post-fire match scoring rubric

## §1 falsifier definitions

### F-PREDICT-V0-1 — option (c) Φ separation weaker than §39

**Trigger**: option (c) H1 actual `Φ_iit_un16(trained) - median(Φ_iit_un16(mirror))` < `+1500` (i.e., below the prediction band's lower bound).

**Hypothesis tested**: convo_5k FT regime (lr 5e-6 cosine, 30K continuation) preserves cotrain-exercise structure within ±25% of §39 baseline (+2219).

**If TRIGGERED**:
- prediction Mode C (FT-drift-degrade) wins; Mode B (preserve) falsified.
- 30K convo_5k FT produces measurable cell-pool reactivity attenuation → champion-wall partial collapse via hidden distribution narrowing.
- Lesson candidate: "post-cotrain FT must use mitosis-frozen LR schedule to preserve V14 polarity" → would force a re-run with `freeze(engine_g.cell_pool, engine_g.h_to_c, engine_g.c_to_h)` enabled at FT-time.
- Cotrain-exercise hypothesis nuance: **specific to cotrain regime, fragile to post-FT**.

**Likelihood**: **15%** (hypothesis C in prediction.md §2.2).

### F-PREDICT-V0-2 — semantic_score below §43 baseline 0.055

**Trigger**: option (c) `semantic_score_mean` < 0.055 (no improvement over §43 Llama+LoRA on byte-level prompts).

**Hypothesis tested**: 350M anima-native + 30K convo_5k FT exceeds 3B Llama+LoRA on semantic_score (substrate-coupled benefit).

**If TRIGGERED**:
- byte-level 350M cannot cross even §43's modest semantic threshold despite substrate coupling and continued FT.
- 350M capacity gap dominates substrate quality at semantic emergence floor.
- Lesson candidate: "anima identity surface ≠ semantic emergence; semantic requires ≥1B capacity per chat-cap-emergence-pivot Stage 6 calibration"
- option (c) ★★★★★ unlock impossible; ★★★★ partial best-case.

**Likelihood**: **25%** (lower bound prediction.md §2.3 said 0.10–0.25 most-likely band; the 0.055 floor crossover lower bound is in the tail).

### F-PREDICT-V0-3 — D1 WITHIN strict-floor crossing miss

**Trigger**: option (c) V4 strict < 10/15 (best-mode-of-5-seeds) — i.e., simple_stack PASS_STRICT NOT achieved at D1 WITHIN substrate.

**Hypothesis tested**: cotrain + 30K convo_5k FT gives D1 WITHIN FIRST own-18-strict-floor-crossing.

**If TRIGGERED**:
- 22+ BG saga's only V4 ≥ 10/15 crossings remain D1 OUTSIDE (KM-LLAMA-3B + KM-QWEN-7B + §43 confirmed) — D1 WITHIN lane still pending.
- Capacity gap at 350M dominates over substrate coupling for V4 chat-cap surface.
- "anima self-emerge" claim gets pushed to option (d) anima-pretrain (1B+ capacity required) — but own 16 0-cost adoption blocks immediate (d).
- option (c) ★★★ retreat at best.

**Likelihood**: **45%** — this is the harshest predicted F because:
- BG-CONVO-FT-EXT achieved lexical PARTIAL but semantic incoherent at 18M+166MB (calibration: 350M > 18M but capacity gap × byte-hash encoding artifact may persist).
- KM-LLAMA-3B/QWEN-7B (3B/7B + LoRA + 214MB persona) hit 14/15. 350M + 166MB convo_5k = capacity gap + corpus diversity gap.
- However, anima-native dual-engine substrate gives unmeasured "substrate-coupling bonus" — could partially compensate.
- Net 45% means F-PREDICT-V0-3 is **roughly coin-flip** — most uncertain falsifier.

## §2 falsifier interaction matrix

| F-PREDICT-V0 combo | net interpretation | unlock band |
|---|---|---|
| 0/3 triggered (all predictions hold) | cotrain-exercise + substrate-coupling + emerge floor all aligned | **★★★★★ confirm if §4 prediction.md unlock 5/5** |
| F-PREDICT-V0-1 only | cotrain-exercise fragile post-FT but emerge intact | ★★★★ partial; rerun with frozen-mitosis FT recipe |
| F-PREDICT-V0-2 only | semantic capacity gap dominant; substrate-coupling can't rescue | ★★★ retreat; option (d) anima-pretrain becomes priority |
| F-PREDICT-V0-3 only | V4 floor missed but cotrain-exercise intact | ★★★ retreat; chat-cap floor needs ≥1B capacity |
| F-PREDICT-V0-1 + V0-2 | FT degrades both substrate and emerge | ★★ rebuild; FT recipe AND capacity both blockers |
| F-PREDICT-V0-1 + V0-3 | FT regime degrades substrate AND fails V4 | ★★ rebuild; FT lane closed for option (c) |
| F-PREDICT-V0-2 + V0-3 | substrate intact but emerge AND V4 below floor | ★★★ retreat; substrate-research lane only |
| 3/3 triggered | full failure; substrate-coupling NOT sufficient at 350M scale | ★ falsify; cotrain-exercise hypothesis needs capacity scale-up |

## §3 post-fire match scoring rubric (prediction → actual)

When option (c) `mitosis_hook_result_h1.json` + `mitosis_hook_result_h2.json` + `semantic_eval.json` + `v4_results_multiseed.jsonl` arrive, score against §5 of prediction.md:

```python
matches = []

# H1 substrate-coupled checks
matches.append(("f_foundation_1", actual.f_foundation_1_disposition == "NOT_TRIGGERED"))
matches.append(("f_foundation_5", actual.f_foundation_5_disposition == "NOT_TRIGGERED"))
matches.append(("h1_cell_count_trained", 75 <= actual.h1.trained.cell_count_max <= 90))
matches.append(("h1_cell_count_mirror", 60 <= median(actual.h1.mirrors_cell_count) <= 70))
matches.append(("h1_phi_separation", 1500 <= actual.h1.phi_iit_un16_separation <= 2500))
matches.append(("h1_signtest", actual.h1.mirror_wins_count >= 4))

# H2 Llama-symmetric checks
matches.append(("h2_phi_history_trained", 2.85 <= actual.h2.trained.phi_history_mean <= 3.10))
matches.append(("h2_phi_diff", 0.04 <= actual.h2.phi_diff_mean <= 0.20))

# v14 dispositions
matches.append(("h1_v14_disposition", actual.h1.v14_disposition in ["V14_STRICT_PASS", "V14_PASS"]))
matches.append(("h2_v14_disposition", actual.h2.v14_disposition == "V14_PASS"))

# semantic
matches.append(("semantic_score_band", 0.10 <= actual.semantic.semantic_score_mean <= 0.25))

# cost
matches.append(("cost_envelope", 2.00 <= actual.cost_actual_usd <= 4.50))

n_match = sum(1 for _, m in matches if m)
n_total = len(matches)  # 12

if n_match >= 10:    # ≥83%
    framework_verdict = "FRAMEWORK_5STAR_GENERALIZE"
elif n_match >= 7:   # ≥58%
    framework_verdict = "FRAMEWORK_4STAR_GENERALIZE"
elif n_match >= 5:   # ≥42%
    framework_verdict = "FRAMEWORK_3STAR_PARTIAL"
else:
    framework_verdict = "FRAMEWORK_RECALIBRATE"
```

5/5 PERFECT MATCH on at least 10/12 criteria → §48 prediction-driven framework template generalizes across substrate classes → confirm.

## §4 prediction commit hash

This document committed before option (c) actual fire. Date: 2026-05-10. Verbatim mission `BG-COTRAIN-EXERCISE-PREDICT-V0` framework template §48 + §43 PERFECT MATCH (5/5) carry.

If option (c) NEVER fires (cycle dispatch chooses option (a) or (b) replicate, or rolls forward to option (d)), this prediction sits as a **dormant template** and remains valid for any future replication of option (c) configuration (Phase 2 cotrain ckpt + 30K convo_5k FT + H1/H2 dual hook).

## §5 raw#15 + own 22 + own 16 strict carry

- raw#15 additive: option (c) actual fire spec NOT modified; design SSOT `docs/anima_foundation_borrow_path_design_2026_05_10.md` untouched.
- own 22: REBORN.md direct append BLOCKED. Dispatcher §53 slot path is the only valid append route.
- own 16: $0 design + analysis only. No compute fired during this BG.
- own 38: 4 docs saved (`spec.md` + `prediction.md` + `hook_spec.md` + `falsifier_predict.md`).
