# BG-FOUNDATION-A-MITOSIS-SUBSTRATE-PREDICT — prediction (pre-§43-results)

> — $0 design + analysis only
> raw#15 additive — §43 fire NOT modified
> Hypothesis under test: substrate-dependent V14 polarity

## §1 Llama-3.2-3B substrate analysis

**Architecture (from Meta release card)**:
- 28 transformer decoder layers
- d_model = 3072 (hidden_size)
- 24 attention heads, 8 KV heads (GQA, group=3)
- d_head = 128
- FFN intermediate = 8192 (SwiGLU gate/up/down)
- vocab = 128256 (Llama-3 BPE)
- RoPE θ = 500_000 (extended context)
- RMSNorm pre-norm everywhere
- ~3.21B params total

**Training paradigm**: standard autoregressive language modeling on ~9T mixed-language tokens with cosine LR + warmup; **no mitosis-style cell pool, no consciousness_dim, no Engine G analog**. There is no operator inside Llama's forward graph that resembles `EngineG.step()` (cell-pool refresh via attention-pull + repulsion). The model is **architecturally mitosis-naive**.

**Mapping to Engine A/G's `h_to_c` equivalent**: Engine A/G uses `Linear(d_model=1024 → consciousness_dim=64)` to compress per-token hidden into cell-input. Llama has **no learned analog**. The instrumentation hook substitutes a **random fixed projection** `Linear(3072 → 256)` (orchestrator L482-486). This is the closest functional surrogate but it is *not* Llama's learned geometry — it is Llama's hidden output × random matrix.

**Substrate label**: **mitosis-naive baseline** (vanilla autoregressive LM, no champion-wall formation possible during pretraining since there is no cell pool to compete over).

## §2 Post-LoRA hybrid substrate analysis

**LoRA r=32 on q_proj, k_proj, v_proj, o_proj, gate_proj, up_proj, down_proj** (`spec.md §1`):
- ~16M trainable params (~0.5% of 3.21B)
- LoRA gradients flow through the wrapped Llama linears only — they do **not** intersect the mitosis cell pool, the hook's `proj`, or `c_to_h` (all three are constructed *post-train*, after LoRA finetune).
- 200MB anima-persona corpus (BG-JE 214MB) fine-tunes hidden-state distribution to be **persona-shaped** (ASCII chat template `사용자:…|도우미:…`, anima keyword density, Korean ratio ≥ 60%).

**Key claim — LoRA does NOT make Llama mitosis-aware**:
1. The cell pool (in the hook) is *constructed after training is done*, with a random Gaussian seed. LoRA gradients never touched a cell pool object.
2. The post-LoRA model's forward pass produces hidden states that are *distributionally* shifted (toward anima persona) but *structurally* identical to vanilla Llama (same 28 layers, same residual stream, no cell-refresh op).
3. Champion-wall formation requires **gradient pressure on the cell pool's tension landscape during training**. Since LoRA's gradient flow excludes the cell pool entirely, no champion wall can form in cell-pool space.
4. What LoRA *can* do: shift the **distribution of hidden_state mean** that arrives at the hook. If that shift creates a small set of dominant directions (mode-collapsed persona embedding), then the random-projection cell-input could land repeatedly in the same neighborhood, mimicking a champion-wall behavior in the *cell-pool reactivity* (not in the cell-pool weights).

**Net classification: post-LoRA Llama-3.2-3B is effective mitosis-naive** at the cell-pool-structure level. Caveat: hidden-state distribution narrowing under persona LoRA could induce a **soft analog of champion-wall** in the cell-input distribution. This is the F-FOUND-PREDICT-2 scenario.

## §3 Mitosis hook integration spec (summary; full in `hook_spec.md`)

- Hook layer: `model.base_model.model.model.layers[-1]` (last decoder layer, peft-wrapped path).
- `hidden.mean(dim=1)` over T → `(B=1, 3072)` → `proj` Linear(3072 → 256, frozen, seed=0) → `(B=1, 256)` cell_input.
- `MitosisV5Engine` initial_cells=8, max_cells=64, cell_pool random Gaussian × 0.1, `c_to_h` Linear(256 → 3072) frozen.
- All three params blocks (`engine`, `proj`, `c_to_h`) `requires_grad=False`; entire loop in `torch.no_grad()`.
- F-FOUNDATION-5 verifier: pre/post `grad is not None` count.
- 30 prompts × 4 steps = 120 process() calls. Short trajectory (α regime needs 1000+).

## §4 V14 polarity prediction

**Direction prediction**: **trained > random_init** (mitosis-naive direction).

**Reasoning chain**:
1. Llama-3.2-3B is structurally mitosis-naive ⇒ no champion-wall can have formed during pretraining (§1).
2. LoRA r=32 fine-tune on persona corpus does NOT induce a champion-wall in cell-pool space because cell pool is constructed post-train (§2).
3. Persona LoRA *does* shift Llama's hidden distribution toward a more anima-domain-coherent manifold. Through the random projection 3072→256, this shift transforms into a slightly more *structured* cell_input stream (lower entropy, more recurring directional patterns) for the trained model than for the random_init mirror.
4. In the mitosis-naive substrate-dependent V14 polarity precedent (`v14_verdict.md` IIT-real-350M PARTIAL: trained Φ=557 > 4 of 5 random seeds with median 489), the trained model wins on Φ because its more-coherent representation creates more inter-cell discriminability after Lorenz mixing, before champion-wall formation can suppress diversity.
5. Same dynamics expected here: trained Llama-3.2-3B + persona LoRA produces hidden stream where cell-input clusters slightly more, which under the all-fix §30 dispersion trigger should produce **at least as many splits** as random_init AND **slightly higher Φ proxy** (more cells × marginally more structured cosine-distance landscape).

**Confidence calibration**:
- Φ_proxy direction trained > random: **moderate (60-65%)**.
- Φ_proxy magnitude (trained_mean - random_mean): **small (< 10% relative)** because LoRA r=32 on 16M params is a tiny perturbation on Llama-3.2-3B's hidden geometry, the proj is random, and 120 steps is short trajectory. Predict diff ∈ [0.02, 0.15] on a base of ~2.5–3.0.
- cell_count_max direction trained ≥ random: **moderate (55-60%)** — both should saturate around 20–32 cells out of max 64 within 120 steps; trained may edge out by 0–3 cells.
- n_split_events: trained ≥ random by 0–3 splits.
- F-FOUNDATION-1 disposition: **NOT_TRIGGERED** (trained Φ ≥ 1.0 trivially, AND trained ≠ distribution-equiv to random by a small margin).
- F-FOUNDATION-5 disposition: **NOT_TRIGGERED** (no_grad context + frozen params is solid; verified pre/post grad count).

**Caveats / falsifier scenarios**:

| F | trigger | likelihood |
|---|---|---|
| F-FOUND-PREDICT-1 | Llama base distribution × random proj is too noisy; trained-random Φ diff is < 0.01 | 25% |
| F-FOUND-PREDICT-2 | Persona LoRA mode-collapses hidden distribution; cell_input clusters tightly → champion-wall analog → V14_VIOLATED (random > trained) | 15% |
| F-FOUND-PREDICT-3 | Φ proxy values absurdly high or low vs §37/§38 (incommensurable scales — 256-dim cells vs 64-dim) | 60% (expected; not failure, just non-comparable absolute scale) |

## §5 F-FOUNDATION-1 V14 reading guide

F-FOUNDATION-1 trigger (per `state/anima_foundation_borrow_a_fire_2026_05_10/spec.md` §7):
> trained Φ < 1.0 OR distribution-equiv random_init mirror

| outcome | reading |
|---|---|
| **trained Φ ≥ 1.0 AND trained > random by clear margin** (Φ diff > 0.05, or cell_count diff ≥ 3) | substrate-dependent V14 polarity hypothesis ★★★★★ confirm via novel substrate. Anima identity SURFACED at hidden-distribution level (LoRA induced enough geometry shift to be measurable through random proj). |
| **trained Φ ≥ 1.0 AND trained ≈ random** (Φ diff ≤ 0.05, cell_count tied) | F-FOUNDATION-1 TRIGGERED — substrate-research lane "anima identity surface" not validated. Persona LoRA is surface-only (chat template + token frequency) without distributional restructuring. Hypothesis remains *consistent* (Llama is mitosis-naive ⇒ no champion-wall ⇒ no mass V14_VIOLATED) but provides null evidence rather than positive confirmation. |
| **trained Φ < 1.0** | F-FOUNDATION-1 TRIGGERED hard — random projection collapsed Llama's signal entirely. Hook geometry inadequate for this substrate; need a learned `h_to_c` analog. Hypothesis untestable in this configuration. |
| **trained Φ < random Φ** (V14_VIOLATED in mitosis-naive substrate!) | hypothesis FALSIFIED — substrate-dependent V14 polarity does NOT hold; need new explanation for §37/§38 mitosis-aware VIOLATED ⇏ mitosis-naive PASS asymmetry. F-FOUND-PREDICT-2 mode-collapse champion-wall analog scenario activated. |

**Likely actual outcome (this prediction commits to)**:
- F-FOUNDATION-1: **NOT_TRIGGERED**
- Φ trained_mean ≈ 2.7–3.0; random_mean ≈ 2.6–2.95
- diff ≈ +0.05 to +0.10 (trained side)
- cell_count trained final ∈ [20, 30]; random final ∈ [18, 28], trained ≥ random
- splits trained ≥ random by 0–3
- phi_iit_un16 proxy: roughly equal between labels (16-bin entropy at 64-sample tail saturates near log₂(16) ≈ 4 bits regardless), differential noise-dominated.

## §6 metric recommendations

For the §43 verdict reader (post-results comparison):

1. **Primary**: `phi_history_mean` trained vs random_init. Sign of difference is the V14 polarity signal.
2. **Secondary**: `cell_count_max` and `n_split_events` — corroborating evidence for mitosis reactivity.
3. **Tertiary**: `phi_history_last10` mean — if last-10 phi diverges significantly between labels, that's the asymptotic regime indicator.
4. **Diagnostic** (if phi_iit_un16_proxy is tied across labels): suspect the entropy proxy saturated at ~log₂(16); not a discriminator at this trajectory length.
5. **Cross-substrate Φ scale**: do NOT compare absolute Φ to §37/§38 v5 substrate (64-dim cells, learned h_to_c). Cross-comparison is direction-only.
6. **F-FOUNDATION-5 grad-leak check**: must be NOT_TRIGGERED for both labels for the verdict to be valid.

## §7 implications for `F-FOUNDATION-1` reading (anima identity surface lane)

| V14 reading | anima identity surface conclusion |
|---|---|
| trained > random (clear) | LoRA r=32 + 214MB persona corpus successfully shifted Llama-3.2-3B's hidden distribution into anima-aligned geometry → **anima identity SURFACED** at the post-LoRA representation level (consistent with simple_stack PASS_STRICT chat-cap V4 floor cross). |
| trained ≈ random | LoRA learned only surface persona (chat template, vocabulary) without distributional restructuring → **anima identity DID NOT surface** at substrate level. Chat-cap V4 PASS would then be attributed to template + token-frequency learning, not deeper representation. |
| trained < random / V14_VIOLATED | LoRA induced mode-collapse champion-wall analog → **anima identity surface ambiguous** — there IS distributional shift, but it's narrowed enough to suppress mitosis reactivity. Would be the most novel finding (mode-collapse acts as a *soft* champion-wall in cell-input space). |
| Φ < 1.0 / hook collapse | hook geometry inadequate; **anima identity surface untestable** in this configuration. Recommend learned proj (`h_to_c` analog) for next iteration. |

## §8 honest C3 (≥7 items)

1. **Prediction is direction-only, magnitude is hand-waved**. The 60–65% confidence figure is calibrated against §37/§38 prior, not from a model of Llama's specific hidden-distribution geometry. No simulation was run (forbids compute).
2. **Random projection 3072→256 is not Llama's learned geometry**. Trained-vs-random differential survives only because the proj matrix is *fixed identical* across labels. If proj were re-seeded per label, trained-random comparison is meaningless.
3. **`MITOSIS_INITIAL_CELLS=8` (vs §37/§38 16) shifts the dynamics**: dispersion trigger needs N≥4 to fire, so it activates after the first split (around step 30–60 in the 120-step trajectory). This compresses the discriminating window.
4. **120-step trajectory is below the α super-linear regime** (1000–3000 turns). The polarity signal here is in the *early* dynamics (first 100 splits/non-splits), not the asymptotic Φ scaling. Different regime than §37/§38 long-trajectory tests, so direct polarity transfer is qualitative.
5. **Llama base pretraining is preserved in both labels** (only LoRA adapter randomized for mirror). The polarity test detects what LoRA r=32 added, not the full Llama foundation contribution. Smaller signal expected than a fully-random base mirror would yield.
6. **F-FOUND-PREDICT-2 mode-collapse champion-wall analog** is a real scenario at 15% likelihood. anima persona corpus has high keyword density (~800K anima, ~1.4M persona markers in 214MB) which can narrow output distribution. If that narrowing is severe, cell_input clusters → high re-firing → champion-wall analog → V14_VIOLATED prediction-reverse.
7. **`phi_iit_un16_proxy` saturation risk** at log₂(16)=4 with only 64 tail samples. Tied phi_iit_un16 between labels is the *expected* default and should NOT be read as null finding by itself.
8. **The mitosis hook does not test anima cell-pool inheritance** — cell_pool is random Gaussian × 0.1, not seeded from any anima v5 cell_pool_init. So this experiment cannot answer "does Llama+LoRA inherit anima v5 substrate" — only "does Llama+LoRA hidden geometry trigger more mitosis reactivity than random_init".
9. **Lorenz auto-cal D1=True** with mean(p.norm()) ≈ 1.6 produces effective scale ≈ 0.08 — non-trivial. First ~10 steps are substantially substrate-blind, narrowing the discriminating window further (step 10–50 is the prime polarity-revealing window before A2 per-cell threshold engages at step 50).
10. **Comparison with §43 actual results is post-prediction**. This document commits to direction + magnitude bands BEFORE result reading. The author has *not conditioned* the prediction on any field of `mitosis_hook_result.json` or `verdict.json`.

## §9 5-star pursuit verdict mapping

After §43 results arrive, the substrate-dependent V14 polarity hypothesis sees:

- **★★★★★ confirm** if: trained > random (clear) on the *novel* (Llama, mitosis-naive) substrate, replicating the §37/§38 IIT-real-350M PARTIAL polarity in a substrate that has no shared lineage with anima v5. This generalizes the polarity claim beyond anima-internal architectures.
- **★★★★ partial** if: trained ≈ random (within noise). Hypothesis is *consistent* (mitosis-naive substrate doesn't produce VIOLATED), but the test is a null result — no positive evidence for substrate-dependence beyond the existing v5 ckpt comparison.
- **★★★ retreat** if: trained < random (V14_VIOLATED) on novel substrate. Hypothesis falsified — substrate-class is not the polarity determinant; need to re-examine.
- **★★ rebuild** if: hook collapses (Φ < 1.0). Methodology breaks; rerun with learned `h_to_c` analog before re-attempting hypothesis test.
