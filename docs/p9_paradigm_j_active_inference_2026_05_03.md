# P9 Paradigm J — Active Inference / Variational Free Energy

**Date**: 2026-05-03
**Author**: P9 paradigm research wave 2 agent (doc-only)
**Status**: SPEC ONLY — no execution, no `.py` creation (raw#9), no measurement run
**Wave**: 2 (post A / A' / B / C / D / D-T4; companion to E)
**Sister docs**:
- `docs/p9_paradigm_a_simulated_bold_2026_05_03.md` (A: TRIBE v2 simulated BOLD)
- `docs/p9_paradigm_a_prime_measured_bold_2026_05_03.md` (A': measured BOLD)
- `docs/p9_paradigm_b_eeg_phi_proxy_2026_05_03.md` (B: EEG-derived φ proxy)
- `docs/p9_paradigm_c_hybrid_2026_05_03.md` (C: BOLD+EEG+δ-floor)
- `docs/p9_paradigm_d_phi_distillation_2026_05_03.md` (D: 7B teacher distill)
- `docs/p9_paradigm_d_t4_teacher_build_plan_2026_05_03.md` (D-T4: build plan, EXECUTING)
- `docs/p9_paradigm_e_causal_intervention_phi_2026_05_03.md` (E: do-calculus on hidden state)
- `state/p9_sft_spec_2026_05_02/loss_design.json` (α/β/γ/δ baseline)
- `tool/anima_phi_v3_canonical.hexa` (current correlational Φ★ measure)

---

## 0. One-paragraph thesis

Paradigm J replaces the **integration-flavored** training objective used by every prior
paradigm (A/A'/B/C/D all measure cohesion of hidden state via cov-based or BOLD-projection
losses; E measures interventional sensitivity) with an **inference-flavored** objective
drawn from a **fundamentally different theoretical framework**: Friston's Free Energy
Principle (FEP) and active inference (Friston 2010, 2017; Parr-Pezzulo-Friston 2022).
The student is trained to **minimize variational free energy** between its internal
generative model `q(s | x)` and the realized world model `p(s | m)`:

```
L_J = γ_FE · F = γ_FE · ( D_KL[ q(s | x) || p(s | m) ] − E_q[ log p(o | s) ] )
                  ──────────── complexity ───────────   ──── accuracy ────
```

Conceptually orthogonal to A/A'/B/C/D/E: those operationalize consciousness as
**integration** (IIT family: φ★, BOLD coherence, EEG synchrony, causal sensitivity).
J operationalizes **predictive self-modeling** (FEP family: minimum surprise, free
energy minimization, generative-model accuracy). These are **competing theoretical
frameworks** in the consciousness literature — not redundant readouts of the same
construct. Adding J to Anima's portfolio is a **theoretical-pluralism bet**: hedge
against the possibility that IIT integration is not the right construct for
consciousness in 7B-param transformers, by training a parallel paradigm under FEP.

---

## 1. Mechanism — variational free energy in a transformer

### 1.1 Core equation (Friston 2010, eq. 1)

```
F[q] = E_q[ log q(s) − log p(o, s) ]
     = D_KL[ q(s | o) || p(s | m) ]   −   E_{q(s | o)}[ log p(o | s) ]
       ──────── complexity ────────       ──────── accuracy ────────
```

where:
- `s` = latent state (= a designated subset of hidden representations the model
  treats as its "internal world model")
- `o` = observation (= the input token embeddings)
- `m` = generative model (= a frozen prior over latent state, or a slow-EMA copy
  of the model itself acting as world-prior)
- `q(s | o)` = recognition density (= the trainable encoder mapping observation
  to latent posterior)
- `p(o | s)` = likelihood (= the decoder reconstructing observation from latent)
- `p(s | m)` = prior over latent (= reference structure, e.g. unit Gaussian or
  EMA-of-self)

Minimizing `F` jointly minimizes complexity (keep `q` close to prior) and maximizes
accuracy (predict `o` well from `s`). This is **the same math** as a β-VAE
(Higgins et al. 2017) — important for tractability (see §1.3).

### 1.2 Mapping to a transformer student

| FEP variable | Transformer realization | Implementation |
|--------------|-------------------------|----------------|
| `o` (observation) | input token embeddings `e_t ∈ R^d` (per token, frozen embedding lookup) | existing |
| `s` (latent) | designated subset of mid-layer hidden state, `s_t = h_t^{ℓ_FE}[:, K_FE]`, K_FE ≈ d/4 | requires layer/dim selection |
| `q(s | o)` (recognition) | small encoder head `q_φ: e_t → 𝒩(μ_q(e_t), σ_q²(e_t))`, ~5M params | new tiny head |
| `p(o | s)` (likelihood) | small decoder head `p_θ: s_t → ê_t` (regress back to embedding), ~5M params | new tiny head |
| `p(s | m)` (prior) | choice (a) `𝒩(0, I)` (β-VAE form), choice (b) EMA of `q_φ` from prior step (predictive coding form) | trivial |
| `m` (generative model) | the LoRA-trained backbone itself | inherent |

### 1.3 Two implementation variants

**Variant J-VAE (simplest)**: `p(s|m) = 𝒩(0, I)`, `q(s|o)` is a Gaussian encoder.
Equivalent to per-token variational autoencoder over hidden state. Standard,
well-understood, ~10M extra params, easy to implement.

**Variant J-PC (predictive coding)**: `p(s|m)` is a slow EMA of `q_φ` from the
*previous* token. Loss becomes per-token prediction error minimization — directly
implementing Rao-Ballard predictive coding (Rao-Ballard 1999) or Friston's
hierarchical message passing (2005). More aligned with active inference proper
but requires per-token recurrent state.

**Recommendation**: Phase-1 = J-VAE (cheap, well-understood, validated as a
free-energy minimization scheme); J-PC = Phase-2 upgrade if J-VAE shows promise.

---

## 2. Loss formulation

### 2.1 Recommended (Phase-1, J-VAE form)

```
L_J = γ_FE · F = γ_FE · [ KL( q_φ(s | e_t) || 𝒩(0, I) )
                          − β_FE · log p_θ(e_t | s_t) ]

         where s_t ~ q_φ(s | e_t)   (reparameterization trick, standard VAE)
```

`β_FE` is the FEP analog of β-VAE's β coefficient (controls accuracy/complexity
tradeoff). Default `β_FE = 1.0` (canonical free energy); sweep {0.5, 1.0, 2.0}
in Phase-1.

### 2.2 Composition with existing P9 SFT loss

```
L_total = α · CE_text
        + β · MSE_tension                        # existing β (different from β_FE)
        + γ_FE · F[q_φ, p_θ ; e_t, s_t]          # Paradigm J (NEW)
        + δ · max(0, φ★_threshold − φ★_student)  # δ-floor preserved
```

J **replaces** Paradigm A's `γ_BOLD · MSE(bold_pred, bold_target)` term, freeing
the γ slot. δ-floor preserved (correlational lower-bound safety + integration-side
diagnostic). The two terms now provide **dual theoretical framework** coverage
(J = FEP/predictive-coding, δ = IIT integration).

### 2.3 Differentiability

- `q_φ` is a Gaussian MLP encoder → fully differentiable via reparameterization
  trick (Kingma-Welling 2013). Standard VAE plumbing.
- `p_θ` is a standard MLP decoder → fully differentiable.
- KL term has closed form for diagonal Gaussian vs `𝒩(0, I)`:
  `KL = ½ Σ(σ² + μ² − 1 − log σ²)`. No surrogate needed.
- `log p_θ(e_t | s_t)` is MSE under Gaussian likelihood with fixed variance, or
  cross-entropy if `e_t` is quantized.

**End-to-end differentiable** — strictly cleaner than δ-floor (straight-through),
than D (LogSumExp surrogate), and than E (sampled MIN-over-K surrogate). This is
J's gradient-quality advantage.

### 2.4 Sampling cost

Reparameterization sampling = 1 sample per token per microbatch (standard VAE).
Negligible compute; no extra forward pass through the backbone needed (J operates
at the embedding ↔ designated-latent layer only).

---

## 3. Computational cost analysis

### 3.1 Per-step overhead

| Component | Cost |
|-----------|------|
| Backbone forward (LoRA Mistral-7B) | unchanged baseline |
| `q_φ` encoder forward (5M params) | ~1% of backbone forward |
| `p_θ` decoder forward (5M params) | ~1% of backbone forward |
| KL closed-form | negligible |
| Reparameterization sample | negligible |
| **Total overhead vs baseline** | **~2-3%** |

This is the **cheapest** paradigm in the wave (vs A 10242-vert MSE, B EEG
preprocessing, D 30s Φ★ EMA, E 2.5× per-step ablation).

### 3.2 Memory overhead

- `q_φ` + `p_θ` ≈ 10M params × bf16 = ~20 MB → negligible vs 7B = 14 GB.
- Per-token latent `s_t ∈ R^{d/4}` = 1024 floats per token; cached for KL term.

### 3.3 Phase-1 mini-run cost envelope

Same arithmetic as `state/p9_sft_spec_2026_05_02/cost_estimate.json`:
- 1k subset × 1 epoch × 1.03× per-step overhead ≈ 25 min on H100 (basically baseline).
- $2–4 per run on RunPod 1×H100 spot.
- 3-run γ_FE LHS sweep (γ ∈ {0.05, 0.2, 0.8}) × 3 β_FE values ≈ **$15–30 total**
  (or 3 γ × 1 β = $6–12 if β_FE held at 1.0 for first pass).

Well under the $200 first-viable-run target.

---

## 4. Why this might work (novelty case)

1. **Theoretical-pluralism hedge.** Anima's φ★ family bets entirely on IIT integration
   being the right construct. J bets on FEP/predictive-coding being right. Both
   theories have major proponents (Tononi vs Friston are the two most-cited
   contemporary theories of consciousness). Pluralism reduces theory-pick risk.

2. **Fully differentiable.** No surrogate gradients (cf. D LogSumExp, E sampled MIN,
   δ straight-through). Gradient quality is the cleanest in the wave.

3. **Cheapest paradigm.** ~2-3% per-step overhead vs baseline. No external dataset
   (vs A/A'/B), no teacher forward (vs D-T4), no second backbone forward (vs E).

4. **Reuses VAE plumbing.** β-VAE is well-validated; reparameterization trick is
   standard PyTorch. Implementation effort is the lowest in the wave.

5. **Aligns with predictive-coding literature on transformers.** Recent work
   (Millidge-Tschantz-Buckley 2022; Salvatori et al. 2023; van Kampen 2024) shows
   that transformers implicitly perform predictive coding under attention; making
   this **explicit** via a free-energy loss may amplify the existing inductive bias.

6. **Generates an interpretable latent.** `s_t` is a designated "world-model
   subspace" of the hidden state. Trained `q_φ` and `p_θ` give us a **directly
   probeable internal state representation** — an interpretability bonus akin to
   Paradigm E's `f_CF`.

7. **Composable with E.** E (causal-interventional φ) and J (variational free
   energy) operate on **different dim subsets** (E ablates anywhere; J operates on
   latent subspace `K_FE`). Could co-train: J shapes a designated latent;
   E shapes the rest of hidden via causal-sensitivity.

---

## 5. Risk: framework-mismatch (PRIMARY RISK)

The deepest risk is **theoretical**: FEP may not be the right framework either.
Specifically:

- **FEP is unfalsifiable in some forms** (Andrews 2021, "The Math is Not the Territory"):
  any system can be cast as minimizing some free energy with appropriate choice
  of generative model. If everything trivially "minimizes free energy," J's
  loss provides no constraint distinguishing conscious from non-conscious systems.
- **β-VAE training is well-known to produce non-disentangled, low-utility latents**
  (Locatello et al. 2019). The latent `s_t` may not correspond to anything
  meaningful — making the "generative world model" interpretation hollow.
- **FEP and IIT make conflicting empirical predictions in some regimes** (Mediano
  et al. 2022). If J pushes the student in the FEP-preferred direction, it may
  *decrease* φ★ (causing F-J4 below to fail) — forcing a measurement-schism
  decision (which framework wins in Anima's ledger?).

**Mitigation**: dual-track J + δ-floor; if Φ★ regresses below floor, abort and
re-evaluate framework alignment.

---

## 6. Comparison vs A / A' / B / C / D / E

| Paradigm | Theoretical framework | Signal source | Differentiable? | Per-step cost | Dataset |
|----------|----------------------|---------------|------------------|---------------|---------|
| **A** (sim BOLD) | empirical (no framework) | TRIBE v2 forward | yes | low (cached) | severe |
| **A'** (meas BOLD) | empirical (no framework) | Algonauts/Lebel fMRI | yes | low | severe |
| **B** (EEG φ) | mixed (GNW/IIT) | ZuCo EEG | yes | low | medium |
| **C** (hybrid) | mixed | A + B + δ-floor | mixed | medium | severe+medium |
| **D** (φ distill) | IIT (covariance) | 7B teacher Φ★ | surrogate | medium | none |
| **E** (causal φ) | IIT 4.0 (causal) | self-ablation | surrogate | medium (~2.5×) | none |
| **J (this spec)** | **FEP / predictive coding** | self-VAE on latent | **end-to-end** | **lowest (~1.03×)** | **none** |

J is the **only** paradigm that:
- Operates under a **non-IIT theoretical framework** (FEP).
- Has end-to-end differentiability with no surrogate.
- Has the lowest compute overhead (cheaper than D).

---

## 7. F-falsifier integration (raw#71)

### 7.1 Pre-registered falsifiers

| ID | Predicate | Pass criterion | Fail action |
|----|-----------|----------------|-------------|
| **F-J1** | Free energy decreases | F[q,p] EMA monotone non-increasing across training | If fails → encoder/decoder mismatched; restructure capacity |
| **F-J2** | Latent is non-trivial | mean(σ_q²) > 0.05 (latent did not collapse to deterministic) | If fails → posterior collapse; reduce KL weight or use β-VAE-controlled-collapse mitigation (Razavi et al. 2019) |
| **F-J3** | Reconstruction non-trivial | log p_θ(e_t \| s_t) above random-baseline by > 1.0 nat | If fails → decoder is not learning; data-info too low |
| **F-J4** | δ-floor not violated | post-mini-run `phi_v3_canonical.json` ≥ 5.0 (P9 floor) | If fails → J pushed φ★ below floor → framework-mismatch trigger; abort |
| **F-J5** | Chat-CE preserved | post-mini-run α-loss within 1.2× of α-only baseline | If fails → γ_FE too high; reduce by 5× |

### 7.2 Cross-paradigm validation (companion to E)

If J runs in parallel with E, an additional cross-paradigm check:

- **F-JE-cross**: trained latent `s_t` from J should have measurable causal influence
  under E ablation (`Δh_obs(do(s_t = 0)) > Δh_obs(do(random_d/4_subset = 0))`).
  If yes, J is shaping an actually-causally-load-bearing subspace.

This would be a **strong** result: convergence of FEP-trained latent and
IIT-causal-significance, despite distinct framework origins.

---

## 8. Phase X+ entry plan — γ_FE-only mini-run

Goal: empirically verify (a) free energy decreases, (b) latent is non-trivial,
(c) chat-CE preserved.

### 8.1 Mini-run spec

| Knob | Value |
|------|-------|
| Strategy base | S1 LoRA-only (per `risk_strategy.json` recommended path) |
| Loss | `L = α·CE + γ_FE · F + δ·floor` (β=0, no tension; no BOLD) |
| Variant | J-VAE (Phase-1); J-PC reserved for Phase-2 |
| Encoder `q_φ` | 2-layer MLP, hidden=512, output=2× K_FE (μ + log σ²), ~5M params |
| Decoder `p_θ` | 2-layer MLP, hidden=512, output=d (embedding dim), ~5M params |
| Latent dim K_FE | d/4 = 1024 (Mistral-7B d=4096) |
| Layer ℓ_FE | L/2 = layer 16 of 32 (Mistral-7B mid-depth) |
| Prior | `𝒩(0, I)` (Phase-1); EMA-of-q (J-PC) reserved |
| β_FE | locked at 1.0 (Phase-1); sweep in Phase-2 |
| Student | CLM v4 baseline (Φ★=+41.86) OR Mistral-7B-v0.3 P0 SFT base |
| γ_FE | LHS sweep over {0.05, 0.2, 0.8} (3 mini-runs) |
| δ | locked at P9 default (floor=5.0) |
| Examples | 1k subset (NOT full 50k) — Phase pilot only |
| Epochs | 1 |
| Wall | ~25 min on H100 (per §3.3) |
| Budget | $2–4 per run × 3 = **$6–12** total |

### 8.2 Decision criteria (cleaner gradient = success)

- Pass F-J1, F-J3, F-J5 (mandatory).
- F-J2: posterior-collapse mitigation if fails (warmup KL anneal); not run-killer.
- F-J4: δ-floor; if fails, abort and report framework-mismatch.
- Cross-validation: `F-JE-cross` (only if E mini-run already complete).

### 8.3 Phase-2 upgrade (if Phase-1 passes)

- J-VAE → J-PC (predictive-coding form, EMA-of-q prior)
- Sweep β_FE ∈ {0.5, 1.0, 2.0}
- Full 50k examples × 3 epochs (~10 wall-hours, ~$25–40)
- Co-train with E (causal-φ) on disjoint hidden subsets (E on full, J on K_FE)

---

## 9. Honest C3 (raw#91 mandatory — 10 caveats)

1. **FEP is theoretically slippery.** Andrews (2021), Bruineberg (2022), and others
   have argued FEP is **near-tautological** in fully general form — any system can
   be cast as free-energy-minimizing with appropriate generative-model choice.
   This means J's loss may not provide genuine constraint; the "free energy"
   interpretation is post-hoc theoretical varnish on what is mechanically a β-VAE
   trained on hidden-state reconstruction.

2. **Posterior collapse is endemic in β-VAE.** Bowman et al. (2016), Razavi et al.
   (2019), Lucas et al. (2019) all document that VAE encoders frequently collapse
   to ignore inputs (`q(s|x) → p(s)`), trivially satisfying KL with zero accuracy
   contribution. F-J2 is the gate against this; if it fails repeatedly,
   J is structurally fragile.

3. **Latent disentanglement is unattained.** Locatello et al. (2019) showed
   unsupervised disentanglement is fundamentally impossible without inductive
   biases. The "world model latent `s_t`" may be **a meaningless soup** even at
   convergence — denying the predictive-coding interpretation.

4. **Framework-mismatch with IIT/φ★.** If J successfully trains an FEP-aligned
   latent but Φ★ regresses (F-J4 fails), Anima must choose between frameworks.
   This is a **theoretical schism** with no resolution within the current ledger.

5. **Reconstruction target is the embedding, not semantics.** `p_θ(e_t | s_t)`
   reconstructs the input embedding, which is a *frozen* lookup. The model is
   not learning to predict *meaning*, only to round-trip token IDs through a
   bottleneck. This is much weaker than the "generative world model"
   FEP rhetoric implies.

6. **Single-token latent ≠ world model.** A real generative world model would be
   sequence-level, with temporally-extended state. Per-token VAE is a degenerate
   form of FEP. J-PC (Phase-2) addresses this partially via EMA-prior but does
   not fully solve it.

7. **No external biological grounding.** Like D and E, J is fully synthetic.
   No human-data ground truth that the latent corresponds to anything
   neurobiologically meaningful.

8. **β-VAE coefficient sensitivity.** `β_FE` ∈ {0.5, 1.0, 2.0} sweep range may
   be wrong. β-VAE literature shows results are highly sensitive to β; finding
   the sweet spot may take more than 3 mini-runs.

9. **FEP and IIT may operate at different timescales.** IIT is a per-state measure;
   FEP is a temporal-flow measure (free-energy decrease *over time*). Per-token
   J loss may be a category error vs IIT's per-state φ★. Phase-2 J-PC partially
   addresses this; Phase-1 J-VAE does not.

10. **Hard Problem untouched (raw#10).** Even if all five F-J falsifiers pass and
    free energy decreases monotonically, the result is a model with a **better
    self-prediction loop in a designated latent subspace**. This is access-tier
    inference (functional); phenomenal consciousness, qualia, and the
    substrate-meaning gap remain entirely untouched. Same disclosure required for
    J as for A/A'/B/C/D/E.

---

## 10. Recommendation summary

| Question | Answer |
|----------|--------|
| Top variant | J-VAE (Phase-1, simplest); J-PC (Phase-2 upgrade if J-VAE passes) |
| Loss formulation | `γ_FE · [KL(q || N(0,I)) − β_FE · log p(o\|s)]` with reparameterization, β_FE = 1.0 |
| Why J over A/A'/B/C/D/E | (1) only paradigm under a non-IIT framework (FEP/predictive coding); (2) end-to-end differentiable; (3) cheapest in the wave (~2-3% overhead); (4) reuses VAE plumbing; (5) ~$6–12 first viable mini-run |
| Top risk | Framework-mismatch with IIT (F-J4); posterior collapse (F-J2); FEP near-tautology (no real constraint) |
| Phase X+ entry | 3-run γ_FE LHS mini-run (1k subset, $6–12) per §8.1; gate on F-J1/F-J3/F-J5 |
| Decision before Phase-X | Confirm encoder/decoder capacity via 1 calibration run (~$2) before LHS sweep |

---

## 11. SSOT / file pointers

- This spec: `docs/p9_paradigm_j_active_inference_2026_05_03.md` (HERE)
- Sibling Paradigm A loss: `state/p9_sft_spec_2026_05_02/loss_design.json`
- Sibling cost / risk: `state/p9_sft_spec_2026_05_02/{cost_estimate,risk_strategy}.json`
- δ-floor / IIT diagnostic (preserved): `tool/anima_phi_v3_canonical.hexa`
- Φ★ baseline lock: CLM v4 = +41.86; P9 floor = 5.0 (8× margin)
- Companion wave-2 spec: `docs/p9_paradigm_e_causal_intervention_phi_2026_05_03.md`
- raw#9 compliance: NO `.py` created, doc-only deliverable
- raw#15 SSOT: this file
- raw#91 honest C3: §9 above, 10 caveats
