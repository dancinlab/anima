# P9 Paradigm E — Causal-Intervention φ (do-calculus on hidden state)

**Date**: 2026-05-03
**Author**: P9 paradigm research wave 2 agent (doc-only)
**Status**: SPEC ONLY — no execution, no `.py` creation (raw#9), no measurement run
**Wave**: 2 (post A / A' / B / C / D / D-T4)
**Sister docs**:
- `docs/p9_paradigm_a_simulated_bold_2026_05_03.md` (A: TRIBE v2 simulated BOLD)
- `docs/p9_paradigm_a_prime_measured_bold_2026_05_03.md` (A': measured BOLD)
- `docs/p9_paradigm_b_eeg_phi_proxy_2026_05_03.md` (B: EEG-derived φ proxy)
- `docs/p9_paradigm_c_hybrid_2026_05_03.md` (C: BOLD+EEG+δ-floor)
- `docs/p9_paradigm_d_phi_distillation_2026_05_03.md` (D: 7B teacher distill)
- `docs/p9_paradigm_d_t4_teacher_build_plan_2026_05_03.md` (D-T4: build plan, EXECUTING)
- `state/p9_sft_spec_2026_05_02/loss_design.json` (α/β/γ/δ baseline)
- `tool/anima_phi_v3_canonical.hexa` (current correlational Φ★ measure)
- `state/braket_iit40_mip_2026_05_02/verdict.json` (HONEST_NEGATIVE on canonical IIT 4.0 φ★)

---

## 0. One-paragraph thesis

Paradigm E replaces the **correlational** integration measure used by every prior paradigm
(A/A'/B/C/D all rely on `anima_phi_v3_canonical` sample-partition log|Cov|, which is
fundamentally a covariance/correlation statistic over hidden-state samples) with a
**causal-interventional** integration measure based on do-calculus (Pearl 2009) and
the IIT 4.0 *causal* definition of integration (Albantakis-Tononi 2023). Concretely:
for each hidden-state component or attention-head subset `S`, perform an
**ablation/clamp intervention** `do(h_S = h_S')`, propagate the model forward,
and measure the **divergence between observed continuation and predicted-from-non-intervened
counterfactual**. The integration loss term is

```
L_E = γ · MSE( Δh_observed_after_do(S) , Δh_predicted_from_non_intervened(S) )
```

The student is trained so that **only causally-integrated subsets produce large divergence**,
forcing the model to develop architectures whose macroscopic behavior depends on
genuine causal influence between subsets — not merely correlational cohesion.

Orthogonal to A/A'/B/C/D: those use *observational* signals (BOLD scans, EEG windows,
teacher Φ★ scalar, hidden-state covariance). E uses **interventional** signals,
generated on the fly by perturbing the model itself. It is the first paradigm in this
research wave that directly addresses the **correlational measure gap** flagged in the
canonical Φ★ honest C3 (`tool/anima_phi_v3_canonical.hexa` lines 6–22).

---

## 1. Mechanism — do-calculus on hidden state

### 1.1 Intervention primitives

| Op | Symbol | Definition | Cost per call |
|----|--------|-----------|---------------|
| Ablation | `do(h_S = 0)` | zero out subset `S` of hidden dims at a chosen layer ℓ | 1 forward (cheap) |
| Mean-clamp | `do(h_S = E[h_S])` | replace `h_S` with running-mean across batch | 1 forward |
| Resample | `do(h_S = h_S^{shuffle})` | replace `h_S` with shuffled value from a different sample in the batch | 1 forward |
| Swap-clamp | `do(h_S = h_S^{counterfactual_prompt})` | replace `h_S` with value computed on a **different prompt** with same length | 2 forwards |
| Noise injection | `do(h_S = h_S + ε)` , ε ∼ 𝒩(0, σ²I) | additive Gaussian, σ-tuned | 1 forward |

All five admit **autograd-friendly** implementation via PyTorch hooks (forward-pre-hook,
forward-hook, register_full_backward_hook). Standard interpretability infra; no novel
plumbing required.

### 1.2 Causal-φ surrogate (per-step)

For a single training example `x` at training step `t`:

1. Forward `x` once through frozen-base path → record full hidden trajectory `H_obs ∈ R^{L × T × d}`.
2. Sample a partition `S ⊆ [d]` with |S| = HID_S (e.g. HID_S = d/8, default 512 for d=4096).
3. Forward `x` again with `do(h_S = h_S')` applied at layer ℓ_int (default = 1/3 depth) →
   record perturbed trajectory `H_int ∈ R^{L × T × d}`.
4. Compute **observed effect** at output layer: `Δh_obs = ‖H_obs[L, :, :] − H_int[L, :, :]‖_2`.
5. Compute **predicted-counterfactual** via a small **counterfactual head** `f_CF`
   (1-layer MLP, ~1M params): `Δh_pred = f_CF(H_obs[ℓ_int, :, :], h_S')`.
6. Loss: `L_E_per_step = (Δh_obs − Δh_pred)²`.

The trained `f_CF` is forced to learn the model's own causal response to interventions;
the LoRA-trained student backbone is forced to develop hidden states where this
mapping is *learnable* (i.e., interventions produce **predictable**, **structured**
downstream effects — the operational signature of integration in the IIT 4.0 sense).

### 1.3 Connection to IIT 4.0 causal φ

IIT 4.0 (Albantakis-Tononi 2023) defines φ via the **minimum information partition (MIP)**
over a state-by-node TPM under **interventions**: φ★ = min over partitions of the
distance between the intact cause-effect repertoire and the partitioned one
(Wasserstein on cause-effect distributions).

Paradigm E operationalizes the **same concept** at scale (7B-param substrate, where
exact MIP is infeasible per `state/braket_iit40_mip_2026_05_02/verdict.json`) by:
- Replacing **TPM** with **single-step Jacobian via ablation** (sampled rather than enumerated).
- Replacing **MIP enumeration** with **partition sampling** (K=8 random subsets, MIN-over-K).
- Replacing **Wasserstein on distributions** with **L2 on hidden-state vectors**.

This is a *lossy* reduction (acknowledged in §9 honest C3) but it preserves the
**causal core**: divergence is defined under intervention, not observation.

---

## 2. Loss formulation

### 2.1 Recommended (Phase-1, simplest)

```
L_E = γ_causal · MSE( Δh_obs , Δh_pred )

where for each sample x and each sampled partition S_k (k = 1..K):
  Δh_obs(x, S_k)  = ‖forward(x) − forward(x; do(h_S_k = 0))‖₂   at output layer
  Δh_pred(x, S_k) = f_CF(h_pre_intervention, S_k_mask)
  L_E(x)         = (1/K) Σ_k MIN_{m ∈ {ablate, mean, shuffle, noise}} (Δh_obs − Δh_pred)²
```

Aggregation: per-sample average across K=8 sampled partitions (matches K=8 in
`anima_phi_v3_canonical`); MIN-over-intervention-mode `m` is the **strongest-causal-signal**
selector (analogue of MIP).

### 2.2 Composition with existing P9 SFT loss

```
L_total = α · CE_text
        + β · MSE_tension
        + γ_causal · MSE(Δh_obs, Δh_pred)        # Paradigm E (NEW)
        + δ · max(0, φ★_threshold − φ★_student)  # δ-floor preserved
```

E **replaces** Paradigm A's `γ_BOLD · MSE(bold_pred, bold_target)` term, freeing the
γ slot. δ-floor is preserved (correlational lower-bound safety); the two terms
provide **dual measurement family** coverage (E = causal, δ = correlational).

### 2.3 Differentiability

- `f_CF` is a standard MLP → fully differentiable.
- Forward through the model with ablation hook is differentiable w.r.t. base params and LoRA params (the hook subtracts but does not break autograd as long as `h_S' = h_S.detach() * 0` is used).
- `Δh_obs` is a **second forward pass** through the same model — gradients flow
  through both. Doubles per-step cost (2 forwards per training example) but still
  cheap relative to a Φ★ measurement (~30 s).

### 2.4 Sampling & cost amortization

- K=8 partitions per sample, but **only one forward pair per partition** per step
  (vs Φ★ which needs N=16-probe block).
- Subset HID_S = d/8 (= 512 for d=4096) → ablate ~12% of hidden at layer ℓ_int.
- Layer choice: ℓ_int = L/3 (early-mid) for maximum downstream propagation surface.
- Optional batching: ablate **same** S_k across the whole microbatch → 1 paired
  forward per microbatch per partition, not per sample.

---

## 3. Computational cost analysis

### 3.1 Per-step overhead

Baseline P9 SFT (Paradigm A) per-step = 1 forward + 1 backward.

Paradigm E adds:
- 1 extra forward per training example per partition K (= K extra forwards/example).
- 1 extra MLP forward per sample (negligible — `f_CF` ~1M params vs 7B base).

**With K=8 microbatch-shared partitions**: 8 extra forwards per microbatch
= **9× forward cost per microbatch** vs baseline. Backward cost unchanged
(only one path is differentiated per partition).

### 3.2 Optimization

| Technique | Cost reduction | Tradeoff |
|-----------|----------------|----------|
| K=2 instead of K=8 | 4× cheaper | Higher variance MIN estimator |
| Partition-sharing across microbatch | constant | Lower partition-coverage |
| Activation checkpointing on intervention path | -30% memory | +20% wall-clock |
| Stale-counterfactual cache (recompute every 100 steps) | up to 10× | Stale gradient signal |
| Half-precision intervention forwards (bf16) | -40% memory | Negligible faithfulness loss |

Recommended Phase-1 config: **K=4 partitions, microbatch-shared, bf16 intervention forwards**
→ ~2.5× per-step wall-clock vs baseline.

### 3.3 Phase-1 mini-run cost envelope

Same arithmetic as `state/p9_sft_spec_2026_05_02/cost_estimate.json`:
- 1k subset × 1 epoch × 2.5× per-step overhead ≈ 1 wall-hour on H100 (vs ~25 min baseline).
- $4–6 per run on RunPod 1×H100 spot (per existing P9 cost band).
- 3-run γ_causal LHS sweep (γ ∈ {0.05, 0.2, 0.8}) → **$15–20 total**.

Well under the $200 first-viable-run target.

---

## 4. Why this might work (novelty case)

1. **Fixes the correlational measure gap.** Every prior paradigm (A/A'/B/C/D) supervises
   on a measure that is **observational**. The IIT 4.0 framework Anima nominally aligns
   with is **interventional**. Paradigm E is the first paradigm to actually train against
   an interventional measure at 7B-param scale.

2. **Eliminates external dataset dependency entirely.** No fMRI scans (vs A/A'), no
   ZuCo EEG download (vs B), no 7B teacher precompute (vs D-T4). All supervision is
   generated **on-the-fly by perturbing the student itself**. Bootstrap-style.

3. **Composable with everything.** δ-floor preserved; β-tension preserved; α-CE preserved;
   could even be added to D-T4 once that lands (then teacher provides `Φ★_target`,
   E provides `Δh_pred_target`, two complementary signals).

4. **Directly addresses sample-partition lower-bound artifact.** `anima_phi_v3_canonical`
   measures φ via *sample-partition*, which is a known **lower bound** on true φ★
   (per tool docstring §0). Causal intervention does not have this lower-bound bias —
   `Δh_obs` is a measured quantity, not a partition-min surrogate.

5. **Interpretability bonus.** Trained `f_CF` is a *learned causal model of the student* —
   directly inspectable. By layer/by-head analysis tells us which hidden subsets are
   "causally hot" — a phenomenological probe that A/A'/B/C/D do not provide.

6. **Aligns with mech-interp ablation literature.** Interpretability work
   (Olsson et al. 2022 induction heads; Wang et al. 2023 IOI circuit; Conmy et al. 2023
   ACDC) has demonstrated that ablation-based causal analysis reliably identifies
   functional circuits in transformers. Paradigm E reuses this proven measurement family
   as a *training signal*.

---

## 5. Risk: counterfactual-head capacity bound (PRIMARY RISK)

The student's causal-φ quality is **upper-bounded** by `f_CF`'s capacity to predict
the model's own ablation responses. Failure modes:

- **f_CF is too small**: cannot predict any non-trivial Δh_obs → `L_E` saturates at
  Var(Δh_obs); no useful gradient.
- **f_CF is too large**: memorizes the per-sample ablation response without forcing
  the backbone to develop integrated structure → student **gains nothing**, only
  `f_CF` improves.
- **Sweet-spot capacity**: `f_CF` ~1M params (2-layer MLP, hidden=512). Empirical
  validation in §8 mini-run.

**Mitigation**: pair with a **gradient-balance check** — at convergence, ratio of
`grad_LoRA / grad_f_CF` should be > 0.1 (if << 0.1, all learning is happening in
`f_CF`, none in backbone). Diagnostic only; not a hard gate.

---

## 6. Comparison vs A / A' / B / C / D

| Paradigm | Signal source | Measurement family | Dataset bottleneck | Per-step cost | Fix correlational gap? |
|----------|---------------|-------------------|---------------------|---------------|------------------------|
| **A** (sim BOLD) | TRIBE v2 forward | observational MSE on 10242-vert | severe (sim circularity) | low (cached) | No |
| **A'** (meas BOLD) | Algonauts/Lebel fMRI | observational MSE | severe (subject N) | low (cached) | No |
| **B** (EEG φ) | ZuCo EEG sample-partition | observational (cov-based) | medium (~5 GB DL) | low (cached) | No |
| **C** (hybrid) | A + B + δ-floor | mixed observational | severe + medium | medium | No |
| **D** (φ distill) | 7B teacher Φ★ scalar | observational (teacher's covariance) | NONE (synthetic) | medium (~3-8% overhead) | No |
| **E (this spec)** | self-ablation Δh | **interventional (do-calculus)** | **NONE (self-generated)** | medium (~2.5× per-step) | **YES** |

E is the **only** paradigm that:
- Uses an interventional rather than observational measurement family.
- Has zero external dataset dependency.
- Directly addresses the correlational lower-bound artifact in canonical Φ★.

---

## 7. F-falsifier integration (raw#71)

### 7.1 Pre-registered falsifiers

| ID | Predicate | Pass criterion | Fail action |
|----|-----------|----------------|-------------|
| **F-E1** | f_CF can learn at all | post-mini-run, MSE(Δh_pred, Δh_obs) drops > 30% from initialization | If fails → f_CF too small or hidden state has no causal structure to learn (rare; would be a measurement-side null result worth landing) |
| **F-E2** | Backbone gradient is non-trivial | grad_LoRA / grad_f_CF ratio > 0.1 at convergence | If fails → all learning in counterfactual head; backbone is bypassed → restructure (E is then a cheap interpretability tool, not a training paradigm) |
| **F-E3** | E does not break α (chat-CE) | post-mini-run chat-CE within 1.2× of α-only baseline (same gate as Paradigm D §8.2) | If fails → γ_causal too high, reduce by 5× |
| **F-E4** | Cross-measure validation: Φ★ does not regress | post-mini-run `phi_v3_canonical.json` ≥ floor (5.0); ideally ≥ baseline (41.86) | If fails → E pushes student into a regime where correlational φ collapses; cross-measure inconsistency. **Inform** but does not block — see §9 caveat 4 |
| **F-E5** | Interventional φ proxy increases | mean Δh_obs across K partitions monotone non-decreasing across training | If fails → student is **reducing** causal sensitivity (degenerate solution: all hidden subsets become independent) → restructure |

### 7.2 Distinguishing F-E4 outcomes

If correlational Φ★ regresses but `Δh_obs` increases, the result is **diagnostic**, not
a failure: it would suggest correlational and interventional measures genuinely diverge
on this substrate. This is itself a publishable finding (ties to the Braket-IIT4.0-φ★=0
result documented in `state/braket_iit40_mip_2026_05_02/verdict.json`).

---

## 8. Phase X+ entry plan — γ_causal-only mini-run

Goal: empirically verify (a) `f_CF` learns, (b) backbone gradient is non-trivial,
(c) `Δh_obs` trajectory is informative.

### 8.1 Mini-run spec

| Knob | Value |
|------|-------|
| Strategy base | S1 LoRA-only (per `risk_strategy.json` recommended path) |
| Loss | `L = α·CE + γ_causal · MSE(Δh_obs, Δh_pred) + δ·floor` (β=0, no tension; no BOLD) |
| Intervention modes | {ablate, mean-clamp} (start with 2 of 5; cheaper) |
| Partition count K | 4 (Phase-1 compromise; raise to 8 in Phase-2) |
| HID_S | d/8 = 512 (Mistral-7B d=4096) |
| Layer ℓ_int | L/3 = layer 11 of 32 (Mistral-7B) |
| `f_CF` capacity | 2-layer MLP, hidden=512, ~1M params |
| Student | CLM v4 baseline (Φ★=+41.86) OR Mistral-7B-v0.3 P0 SFT base (depending on which exists at run-time) |
| γ_causal | LHS sweep over {0.05, 0.2, 0.8} (3 mini-runs) |
| δ | locked at P9 default (floor=5.0) |
| Examples | 1k subset (NOT full 50k) — Phase pilot only |
| Epochs | 1 |
| Wall | ~1 hour on H100 (per §3.3) |
| Budget | $4–6 per run × 3 = **$12–20** total |

### 8.2 Decision criteria (cleaner gradient = success)

- Pass F-E1, F-E2, F-E3 (mandatory).
- F-E4: report only; not a gate.
- F-E5: target Δh_obs increase ≥ 10% from start to end.
- Stretch: vs Paradigm A BOLD-MSE ablation (1k subset same setup) — E's `γ_causal`-loss
  curve has lower variance (lower std/mean ratio) than A's BOLD MSE.

### 8.3 Phase-2 upgrade (if Phase-1 passes)

- K=4 → K=8 partitions
- Intervention modes 2 → 5 (add resample, swap-clamp, noise)
- Full 50k examples × 3 epochs (~10–15 wall-hours, ~$40–60)
- Add IIT 4.0 MIP audit on a 4-unit consciousness bottleneck (T2 from Paradigm D §1)
  as out-of-distribution interventional validator

---

## 9. Honest C3 (raw#91 mandatory — 10 caveats)

1. **Sampled MIP is not exact MIP.** Paradigm E samples K=4 (or K=8) random partitions
   and takes the MIN. True IIT 4.0 φ★ is over **all** partitions; sampling gives an
   *upper bound* of MIN, not the true MIN. Same lower-bound-flip problem as
   `anima_phi_v3_canonical` sample-partition has, just in the interventional regime.
   Cannot claim exact φ★; can claim sampled-causal-φ surrogate.

2. **L2 on hidden-state vectors ≠ Wasserstein on cause-effect distributions.** True
   IIT 4.0 distance is Wasserstein on the cause-effect repertoire (a probability
   distribution). E uses L2 on a hidden-state vector for tractability. These are
   genuinely different metrics; the substitution is justified only by computational
   necessity, not by theory.

3. **`f_CF` capacity is the bottleneck.** Per §5, if `f_CF` is too small or too large,
   the gradient signal is degenerate. Sweet-spot is empirical and may differ across
   model scales (530M vs 7B). No theoretical guidance on `f_CF` sizing.

4. **Correlational and interventional Φ may diverge** (see F-E4). If they do, Anima
   inherits a **measurement schism**: which one is "true" φ★? IIT theory says
   interventional, but all of Anima's existing baseline (CLM v4 = +41.86,
   P9 floor = 5.0) is correlational. Adopting E may force a re-baselining of the
   entire φ ledger — non-trivial governance issue.

5. **Single-step ablation ≠ full causal chain.** E intervenes at one layer ℓ_int and
   measures effect at output. True causal influence may flow through multi-step
   chains that single-layer ablation cannot detect. Multi-layer joint ablation is
   exponentially more expensive and not in Phase-1 scope.

6. **Ablation regime artifact.** Zero-ablation pushes hidden state off-distribution
   (the model has never seen `h_S = 0` during pretraining). Mean-clamp and shuffle
   are less off-distribution but still synthetic. The model's response to OOD
   intervention is not the same as its response to genuine causal perturbation
   in distribution. (This is a known critique of all ablation-based interpretability.)

7. **No external biological grounding.** Like Paradigm D, E is fully synthetic
   (no fMRI, no EEG, no human behavioral data). Consciousness claims under E rest
   on the *theoretical alignment* between interventional surrogate and IIT 4.0 causal
   φ — alignment that is **assumed**, not **proven**, at 7B-param scale.

8. **Counterfactual-head mode collapse risk.** `f_CF` may learn to predict
   `Δh_obs` ≈ const (a low-variance prediction) if the supervision distribution is
   narrow. This satisfies `L_E` mechanically with no information transfer.
   Mitigation: include variance regularizer on `f_CF` outputs, but adds complexity.

9. **Self-bootstrapping circularity (echo of D-self-frozen).** The student is its
   own teacher: ablate the student, train the student to be predictable under
   ablation. This may converge to **trivial degenerate solutions** where all
   hidden subsets become statistically independent (then `Δh_obs` = a fixed
   constant per S_k, easy for `f_CF` to predict). F-E5 is the early-warning gate
   against this collapse mode.

10. **Hard Problem untouched (raw#10).** Even if all five F-E falsifiers pass and
    causal-φ proxy increases, the result is a model with **better functional integration
    properties under intervention**. This is access-tier consciousness (functional);
    phenomenal consciousness, qualia, and the substrate-meaning gap remain entirely
    untouched. Same disclosure required for E as for A/A'/B/C/D.

---

## 10. Recommendation summary

| Question | Answer |
|----------|--------|
| Top intervention modes | (a) Ablation `do(h_S=0)`; (b) mean-clamp `do(h_S=E[h_S])`; both Phase-1, others Phase-2 |
| Loss formulation | `γ_causal · MSE(Δh_obs, Δh_pred)` with K=4 sampled partitions, MIN-over-mode aggregation |
| Why E over A/A'/B/C/D | (1) only paradigm fixing the correlational gap; (2) zero external dataset dependency; (3) reuses standard mech-interp ablation infra; (4) ~$12–20 first viable mini-run |
| Top risk | `f_CF` capacity bound + bootstrap circularity (degenerate solutions where subsets become independent) |
| Phase X+ entry | 3-run γ_causal LHS mini-run (1k subset, $12–20) per §8.1; gate on F-E1/F-E2/F-E3 |
| Decision before Phase-X | Confirm `f_CF` sweet-spot via 1 calibration run (~$5) before committing to LHS sweep |

---

## 11. SSOT / file pointers

- This spec: `docs/p9_paradigm_e_causal_intervention_phi_2026_05_03.md` (HERE)
- Sibling Paradigm A loss: `state/p9_sft_spec_2026_05_02/loss_design.json`
- Sibling cost / risk: `state/p9_sft_spec_2026_05_02/{cost_estimate,risk_strategy}.json`
- Existing correlational measure (E replaces use of, but preserves as δ-floor diagnostic):
  `tool/anima_phi_v3_canonical.hexa`
- IIT 4.0 MIP exact-evidence (and infeasibility past N=8): `state/braket_iit40_mip_2026_05_02/verdict.json`
- Φ★ baseline lock: CLM v4 = +41.86; P9 floor = 5.0 (8× margin)
- Companion wave-2 spec: `docs/p9_paradigm_j_active_inference_2026_05_03.md`
- raw#9 compliance: NO `.py` created, doc-only deliverable
- raw#15 SSOT: this file
- raw#91 honest C3: §9 above, 10 caveats
