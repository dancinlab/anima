# BOLD ↔ Anima Integration Methodology — Deep Research

**Date:** 2026-05-03
**Status:** Research synthesis (no execution).
**Author:** Anima research agent (P9 Phase-2 methodology thread).
**Scope:** P_S projector design, hemodynamic alignment, evaluation stack, vertex resolution choice, consciousness markers, cross-substrate consistency framework, license compatibility, honest C3.
**Inputs read:**
- `docs/p9_paradigm_a_prime_measured_bold_2026_05_03.md`
- `docs/p9_paradigm_a_prime_runbook_2026_05_03.md`
- WebSearch findings (sources cited inline; aggregated reference list at end).
**Constraints honored:** raw#9 (no .py), raw#15 (no personal paths in references list).

---

## 0. TL;DR

| Question | Recommendation |
|---|---|
| P_S projector architecture | **Tied option A (recommended primary):** rank-256 ridge-regularized linear `R^768 → R^1000` (Schaefer-1000) with optional ICA-256 pre-reduction on the CLM hidden side. **Option B (deferred):** per-region per-layer linear stack à la Pasquiou-2022 (heavier, used as analysis-only baseline). **Option C (out-of-scope for mini-run):** TRIBE-v2-style 3-stage transformer projector (used as upper-bound reference, not as our P_S). |
| HRF alignment | **Canonical SPM double-gamma (Glover 1999) at 2 Hz internal rate, decimated to 1/TR Hz.** Subject-specific FIR HRF deferred to Phase-3 (identifiability hazard). |
| F4 thresholds | **Adopt tiered scheme: bronze 0.10 / silver 0.20 / gold 0.30 / aspirational 0.50** (lang-ROI mean Pearson r). Retire single 0.5 threshold from spec — unrealistic for mini-run; published SoTA sits ≈0.30–0.45. |
| Vertex resolution | **Schaefer-1000 (anima primary)** — matches Algonauts native, fits compute budget. fsaverage5 (10 242/hemi) used for cross-dataset comparisons after `mri_surf2surf` downsampling. |
| Consciousness marker stack | DMN-deactivation z-score + Brain Entropy (Wang 2014 BEN) + LZc (Casali-analog) computed on windowed BOLD; perturbational PCI-fMRI deferred (no TMS). |
| Cross-substrate consistency test | **Per-window Spearman ρ between φ★(CLM, window w) and BEN(BOLD, window w), aggregated subject-level via LME with subject random intercept; phase-randomization null per window.** |
| License | OpenNeuro CC0 (Lebel ds003020) > cNeuroMod CC-BY 4.0 derivatives (Algonauts 2025; Friends video itself stays Warner Bros.) > HCP DUA. Anima public model release: safe with CC0; needs legal review with CC-BY-4.0 attribution; blocked on HCP. |
| Honest C3 | 8 caveats; top-3 = (1) BOLD↔φ ontological gap, (2) projector identifiability, (3) HRF subject variability. |

---

## 1. P_S projector — model hidden → BOLD vertex space

### 1.1 Survey

| # | Approach | Source | Architecture | Train procedure | Anima fit |
|---|----------|--------|--------------|-----------------|-----------|
| 1 | **Linear ridge regression** | Wehbe 2014; Tang/Huth 2023; Naselaris 2011; Voxelwise Encoding Model framework (MIT Press 2025) | `BOLD_v = (X · W_v) + ε`, W_v fit per voxel by L2-regularized OLS; X = stacked time-delayed (2/4/6/8 s) hidden-state features. | Closed-form per voxel; α swept by 5-fold CV. | **Best fit for anima mini-run.** Cheap, identifiable, well-understood ceiling. |
| 2 | **Per-layer per-region linear** | Pasquiou 2022 ("Neural Language Models are Not Born Equal…") | Same as (1) but one ridge per (layer, brain region) pair → diagnostic surface. | Same closed-form, repeated. | **Diagnostic baseline only**, not the production P_S — too many parameters to roll into a CLM training loop. |
| 3 | **Voxelwise nonlinear** (Naselaris 2011 generalized) | Naselaris 2011 review | Feature-space mapping is allowed nonlinear; voxel mapping stays linear. | Joint training of feature + linear head. | We already let the CLM learn nonlinear features; P_S itself stays linear (rationale: identifiability, see §1.4). |
| 4 | **TRIBE v2 transformer projector** | Vu et al. 2025 (Meta FAIR) | 3-stage: (encoding LLaMA-3.2 / V-JEPA2 / Wav2Vec-BERT) → integration transformer → brain mapping head onto ~70 K voxels (cNeuroMod fsLR). | End-to-end with weighted MSE on cNeuroMod 1 000 h fMRI. | **Out-of-scope as our P_S.** TRIBE v2 IS the upstream encoder model we are escaping (paradigm A circularity). We use its NUMBERS as a ceiling reference, not as our projector. |
| 5 | **ICA-reduced linear** | classical preprocessing; combined with (1) in many encoding papers | ICA on CLM hidden side (768 → 256 components) before ridge. | Two-step: unsupervised ICA, then ridge per voxel. | **Optional Phase-2 enhancement** — reduces overfit, smaller P_S. Recommend evaluating against pure rank-256 ridge in an ablation. |
| 6 | **Reduced-rank regression / low-rank tensor** | Low-Rank Tensor Encoding (bioRxiv 2025); RRR tutorial (arXiv 2512.12467) | `W = U V^T`, rank ≤ r; can be tensorized over (semantics, time, region). | SGD-friendly; differentiable; integrates with the CLM training loop. | **Strong secondary candidate.** Differentiable form of (1) suitable for joint γ-loss with CLM gradients flowing through P_S. |

### 1.2 Recommended P_S architecture for anima (CLM-768d → Schaefer-1000)

**Production primary: rank-256 reduced-rank linear projector with optional ICA pre-reduction.**

```
Hidden  h_τ  ∈ R^768   (TR-binned mean over tokens, per §2.3 of paradigm-A' spec)
       ─►  [optional ICA-256]  ─►  z_τ ∈ R^256
       ─►  W_proj ∈ R^{1000×256}  (learnable, ridge-regularized λ ~ 10⁻²)
       ─►  ŷ_τ ∈ R^1000  (Schaefer-1000 parcels)
       ─►  HRF conv (§2)
       ─►  BOLD_pred[τ, :]
```

**Why rank-256:**
- Matches BrainEncoding-style regularization and mitigates the spec §7 caveat 8 ("if P_S is high-rank it absorbs arbitrary CLM shape and F4 PASS becomes meaningless").
- 256 is sub-rank of both source (768) and target (1000) so the bilinear factorization is informative.
- Reduced-rank regression literature (RRR tutorial, low-rank tensor 2025) shows ~2–4× lower overfit vs full-rank ridge on encoding tasks.

**Why Schaefer-1000 as default output:**
- Matches Algonauts 2025 native (cNeuroMod ships parcellated). No re-projection step in the inner loop.
- 1 000 dim ≈ ¼ M params for the full-rank linear (768·1000), 0.25 M for rank-256 — small enough to keep on GPU and cheap to ridge-fit.
- Schaefer parcellation noted to plateau in performance at ~200 parcels (boundary metric); 1 000 is safely past plateau.

**Why ICA pre-reduction is optional (run as ablation):**
- Decorrelates CLM features, often improves ridge condition number.
- Adds preprocessing complexity. Evaluate empirically on the mini-run holdout.

### 1.3 Training data for P_S

- **Primary:** Algonauts 2025 sub-01 Friends s01–s02 (already downloaded per runbook §1; 44 911 TR-steps, 118 484 tokens).
- **Cross-subject test:** sub-02 / sub-03 / sub-04 zero-shot.
- **Cross-dataset test (F4-gold):** Lebel 2023 ds003020 (CC0, 8 subj, fsaverage native — must downsample to fsaverage5 then re-project to Schaefer-1000-on-fsaverage5 to match output dim).

### 1.4 Identifiability rationale (why we keep P_S linear and small)

The MSE flows through P_S: `L = ||W · h - y||²`. If W is rank ≥ min(d_h, d_y), the projector can absorb arbitrary CLM-side rotations of h_θ and still match y, decoupling the gradient signal from any meaningful change in h_θ. Mitigations adopted:

1. **Rank cap (≤ 256).**
2. **Ridge λ on W.**
3. **Optionally freeze W after a brief warmup** (200 steps) so the rest of training cannot reabsorb gradient through W.
4. **Diagnostic:** report `rank(W)` and `||W||_F` per eval; flag if rank saturates.

This satisfies spec §7 caveat 8.

---

## 2. Hemodynamic response (HRF) alignment

### 2.1 Options & decision

| Option | Source | Cost | Identifiability | Recommendation |
|---|---|---|---|---|
| **(B) SPM canonical double-gamma (Glover 1999)** | Glover NeuroImage 1999; SPM/FSL/AFNI default; HRF FAQ MIT mindhive | 32-tap conv1d at 2 Hz | High (fixed kernel) | **PRIMARY** — adopt across all anima runs. |
| (B′) Canonical + temporal/dispersion derivatives | Henson & Friston SPM book ch 14 | 3-tap basis | Slightly lower (3 free params per voxel) | Optional Phase-3 enhancement. |
| (C) Subject-specific FIR HRF estimation | Lindquist et al. 2009; Aguirre 1998; voxel-specific HRF (Lu 2007) | Per-voxel ~20 free taps | LOW (HRF/neural entangled; spec §2.2 caveat) | Defer to Phase-3+ unless saturation observed. |
| (A) Fixed +5 s lag-shift | TRIBE v2 inventory.json default | trivial | High | **Sanity baseline only.** Discards HRF shape. |

**Decision: Option B (canonical SPM double-gamma, Glover form).**

```
y(t) = c1·t^{n1}·exp(-t/t1)  −  a2·c2·t^{n2}·exp(-t/t2),
(n1, t1, n2, t2, a2) = (6.0, 0.9, 12.0, 0.9, 0.35).
```

Peak ≈ +5 s, undershoot ≈ +15 s; sample at 2 Hz, 32 taps (16 s kernel; covers main lobe + undershoot edge).

### 2.2 Token-rate → TR-rate alignment scheme

This refines paradigm-A' spec §2.3:

1. CLM emits h_τ at internal 2 Hz (TRIBE-compatible processing freq).
2. TR-bin: `H_τ = mean_{i: floor(onset_i/TR)=τ} h_i` over tokens whose word-onset falls in TR τ (mean is the simplest baseline; attention-weighted is a Phase-2 ablation).
3. Apply P_S: `ŷ_τ = W · ICA(H_τ)` — gives parcel-rate signal at 2 Hz.
4. Convolve along time: `BOLD_pred = HRF * ŷ` (causal conv1d, 32 taps).
5. Decimate by 1.49 s × 2 Hz ≈ 3 → 1/TR Hz.
6. Trim 16 s convolution edge.
7. Per-vertex per-run z-score before MSE.

### 2.3 Subject-specific HRF — explicit defer

The literature (Aguirre 1998; Lindquist 2009; SPM ch 14) shows HRF varies by subject AND brain region (~±1.5 s peak shift, ~25 % amplitude variability). For Phase-2 we accept this as a residual error term absorbed by the per-vertex MSE; for Phase-3 we may add a per-region temporal-derivative basis (B′). We do NOT learn a per-vertex FIR because:

- 20 free taps × 1 000 parcels = 20 K extra params, comparable to the projector itself.
- HRF/neural decomposition is non-identifiable from a single dataset.
- Risk of P_S errors being absorbed into a "learned HRF."

### 2.4 Token rate vs TR — quantitative tradeoff

Anima token rate ≈ 5/sec (typical Llama generation). After TR-binning at 1.49 s:
- ≈ 7.5 tokens/TR → ample averaging for a stable mean h.
- HRF temporal smoothing then bandlimits to ~0.1 Hz, well below the TR Nyquist (0.34 Hz at TR=1.49).
- Thus token granularity is NOT the bottleneck; HRF smoothing is. Confirms canonical-HRF approach.

---

## 3. Evaluation metric stack

### 3.1 Recommended stack (in computation order)

| Layer | Metric | Per-unit | Aggregation | Source |
|---|---|---|---|---|
| 1 | **Pearson r** (per vertex/parcel × per chunk) | vertex × chunk | mean over vertices in ROI; mean over chunks | Tang/Huth 2023; Lebel 2023; standard since Naselaris 2011 |
| 2 | **R²** explained variance | vertex × chunk | reported alongside r for direct interpretability | Standard fMRI encoding |
| 3 | **Phase-randomization null** | per vertex | 1 000 phase-shuffled surrogates → p-value per vertex; FDR-q across vertices | Theiler 1992 surrogates; Frontiers Neurosci 2018 (resting-state null primer) |
| 4 | **Block-bootstrap 95 % CI** on ROI mean r | per ROI | 10 000 moving-block resamples, block length 30 s | MBB literature; Bullmore et al. 1996 wavelet bootstrap |
| 5 | **Group-level LME** | subject random intercept; chunk random slope; ROI fixed effect | t-stat, FDR-corrected | Chen et al. 2013 NeuroImage (LME for fMRI group analysis) |
| 6 | **EBME / model comparison** | only if comparing P_S architectures | log-evidence ratio | Friston et al. 2007 Bayesian model selection |

### 3.2 Statistical sanity protocol

- **Phase-randomization null:** preserves spectrum of predicted BOLD, breaks alignment with measured BOLD. Null Pearson r ≈ N(0, 1/√(T-1)) before HRF smoothing, ~1.2× wider after smoothing (because HRF reduces effective T).
- **Block-shuffle null:** alternative — partitions held-out time series into 30 s blocks, shuffles block order, recomputes r. More conservative (preserves longer correlations). Use for Yeo-7 network-mean r.
- **ARMA-fit null:** fit AR(1)/AR(2) per vertex on residuals, simulate from fitted process. Use only when phase-randomization is suspected to be too liberal (rare in fMRI encoding contexts).

### 3.3 F4 falsifier — tiered ratification

Replacing spec single threshold `r > 0.5`:

| Tier | F4_lang threshold | Interpretation | Action |
|---|---|---|---|
| **F4-bronze** | r ≥ 0.10 | Above-chance brain alignment; null rejected at p<0.001 | Pass γ-only mini-run gate; proceed to Lebel supplement. |
| **F4-silver** | r ≥ 0.20 | Comparable to weak text-only encoding (early Huth-lab) | Pass extended γ-only run gate; proceed to 4-loss combo. |
| **F4-gold** | r ≥ 0.30 | Comparable to Lebel 2023 / TRIBE v2 reported numbers on language ROIs | Pass Phase-2 final gate; can claim "competitive brain encoding." |
| **F4-aspirational** | r ≥ 0.50 | Exceeds published SoTA | Standalone publishable result; would imply we matched TRIBE v2-tier performance with a CLM that is also generative. |

**Rationale for retiring the single 0.5 spec threshold:** Tang/Huth 2023 scaling-law paper shows logarithmic scaling with model size; even 30 B-param LMs reach ~0.4 in best language ROIs after days of training on full Lebel data. Our 5–10 K-step γ-only mini-run on 1 subject cannot plausibly cross 0.5. Tiered scheme is the honest version.

---

## 4. Vertex / voxel resolution decision

| Option | Resolution | Pros | Cons | Anima fit |
|---|---|---|---|---|
| **Schaefer-1000 parcels** | 1 000 (whole brain) | Algonauts native; SNR-lifted by parcel averaging; computationally cheap | Loses sub-parcel spatial detail; some functional inhomogeneity within large parcels | **PRIMARY for anima.** |
| fsaverage5 surface | 20 484 (10 242 / hemi) | Vertex-level; standard cross-subject; matches Lebel 2023 after downsample | 20× more output dim than Schaefer-1000 → 20× P_S params | Secondary; used for cross-dataset (Lebel) F4 evaluation. |
| fsaverage native | 327 684 (163 842 / hemi) | Maximal spatial detail | Statistical noise floor dominates; ~3× more compute | Avoid for training; reserve for visualization only. |
| MNI volume (~250 K voxels @ 2 mm³) | volumetric | Compatible with non-surface workflows | Mixes white matter, ventricles; partial-volume confounds | Avoid. |
| HCP-MMP1 | 360 (180 / hemi) | Multi-modal parcellation, strong functional homogeneity | Smaller dim, slightly less spatial detail than Schaefer-1000 | Useful as a sanity check / diagnostic atlas. |
| fsLR-32k (HCP) | ~64 K vertices | TRIBE v2 native target | Requires HCP DUA + fsLR registration | Out-of-scope (license + compute). |

**Decision: Schaefer-1000 for primary, fsaverage5 as secondary for cross-dataset.**

The runbook §7 caveat-3 already flagged the fsaverage5/Schaefer-1000 dimensionality mismatch in `loss_design.json`. The unified policy: P_S output dim is configurable at construction (1 000 for Algonauts, 20 484 for Lebel); reported metrics aggregate at the network level (Yeo-7) for cross-dataset comparability.

---

## 5. Consciousness markers from BOLD (cross-validation with anima φ★)

### 5.1 Marker survey

| Marker | Source | What it measures | BOLD compatibility | Use in anima |
|---|---|---|---|---|
| **DMN deactivation** | Raichle 2001; Crone 2011 PLOS ONE; Menon 2023 Neuron review | Task-related decrease in midline regions (mPFC, PCC, angular gyrus) — deactivation absent in vegetative state, partial in MCS | Native BOLD readout; ROI mean | **Use as primary control marker.** Compute z-scored DMN deactivation per chunk. |
| **Brain Entropy (BEN)** | Wang 2014 PLOS ONE (n=1049); Saxe 2018 (n=892, intelligence correlation) | Sample entropy of voxelwise BOLD time series; higher BEN ↔ richer dynamics | Direct from BOLD; windowable | **Use as primary cross-substrate marker** (compare to anima window-φ★). |
| **Lempel-Ziv complexity (fMRI LZc)** | Schartner 2017 (EEG); Mediano 2019 (extension to BOLD analog); Casali 2013 (PCI on TMS-EEG, analog form) | Algorithmic complexity of binarized signal; PCI-style readout without TMS | Compute on z-scored BOLD windows; coarser than EEG-LZc due to TR | Secondary marker; useful for falsification (low LZc with high-φ★ would be an alarm). |
| **Spatiotemporal complexity ST3** | eLife 2024 (Spatiotemporal brain complexity quantifies consciousness outside of perturbation) | Variance of dynamic FC + entropy of state transitions; resting-state consciousness proxy | Native BOLD; sliding window | Phase-3 enhancement; promising as PCI-without-TMS. |
| **Global Brain Connectivity (GBC)** | Cole 2010; Power 2013; Crossley 2014 (rich-club) | Mean correlation of each voxel with whole brain; high GBC marks integration hubs | Native BOLD; functional connectivity | Use to define an "integration ROI" (top-decile GBC vertices) for cross-substrate test. |
| **Integrated information from fMRI (Φ_R, ΦID)** | Toker & Sommer 2022; Mediano 2022; Luppi 2023 Comm Bio (IIT in resting fMRI) | BOLD-derived φ-proxy via state-space reduction + ΦID decomposition | Computable but coarse (TR=1.49); ΦID has known ~30 % rank-correlation to true φ on simulators | Phase-3 cross-substrate validation. NOT used as F4 target. |
| **PCI-fMRI (perturbational)** | Casali 2013 (TMS-EEG original); proposed extensions to fMRI under transient task perturbation | Algorithmic complexity of cortex's response to perturbation | Requires perturbation paradigm — anima doesn't have TMS access | Out-of-scope. |

### 5.2 Marker stack chosen for cross-substrate validation

```
BOLD-side:     [DMN_z(w), BEN(w), LZc_BOLD(w), GBC_top10(w)]    — 4 scalars per window w
CLM-side:      φ★(w)                                              — 1 scalar per window w
                                                                   (computed offline via Bayesian inversion of state-space model)
```

Window length: 30 s (≈ 20 TR). Step: 10 s. Per-chunk yields ~30 windows.

### 5.3 Why we don't try to compute "BOLD-φ" directly

Mediano 2022 / Toker 2022 explicitly note BOLD-derived φ is a *lower bound* with ~30 % rank-correlation to simulator-truth φ. Computing it on 1 000-parcel BOLD at TR=1.49 s yields a noisy, slow estimate. Using BEN (which is well-validated as a complexity proxy at similar resolution) gives more stable cross-substrate signal with clearer physical interpretation.

---

## 6. Cross-substrate consistency framework (formal statistical model)

### 6.1 Hypothesis

```
H0: φ★(CLM, w) is statistically independent of M(BOLD, w)
    for all consciousness markers M ∈ {DMN_z, BEN, LZc, GBC_top10}.

H1: ∃ M such that φ★ correlates with M at α=0.05 after Bonferroni-4
    AND the correlation survives a per-window phase-randomization null.
```

### 6.2 Formal test — primary

**Per-subject linear mixed-effects model** (per marker M):

```
M(BOLD_{s, c, w}) ~ β0 + β1·φ★(CLM, c, w)
                  + (1 | subject_s)              # subject random intercept
                  + (β1 | subject_s)             # per-subject slope (random)
                  + (1 | chunk_c)                # chunk random intercept
                  + ε_{s,c,w}                    # AR(1) residual
```

Where:
- `s` = subject index (Algonauts 4 + Lebel 8 = up to 12)
- `c` = stimulus chunk
- `w` = 30 s window inside chunk

**Test:** is fixed-effect β1 significantly nonzero? (Wald t-test, Satterthwaite df.)

**Effect-size summary (per marker):** Spearman ρ between `φ★(CLM, w)` and `M(BOLD, w)` after partialing out subject and chunk means. Spearman is preferred over Pearson because φ★ has heavy-tailed scale.

### 6.3 Falsifier (anti-overfit)

For each marker M, also compute a **phase-randomization null** on `φ★`:
- Phase-randomize the φ★(w) time series per chunk (preserve power spectrum, break temporal alignment).
- Recompute β1_null over 1 000 surrogates.
- Declare cross-substrate consistency PASS only if observed β1 lies above 95th percentile of β1_null AND absolute Spearman ρ > 0.10.

### 6.4 Mediation analysis (Phase-3, exploratory)

If consistency PASS on primary, test whether the BOLD marker mediates the CLM→behavior relationship (where "behavior" = next-token CE). Causal mediation `(φ★ → BEN → CE_loss)` would be strong evidence that φ★ captures something brain-relevant, not just an arbitrary internal scalar.

### 6.5 Reduction strategies (the "compare scalar to vertex pattern" problem)

Three reduction strategies for "single CLM φ★ vs BOLD vertex pattern":

| Strategy | Description | Pros | Cons |
|---|---|---|---|
| **A. ROI scalar** (recommended) | Reduce BOLD to scalar per window via DMN_z / BEN / LZc / GBC_top10 → scalar↔scalar correlation. | Interpretable, stable, well-validated markers. | Loses spatial detail. |
| B. CCA (canonical correlation) | Find linear combos of BOLD vertices and CLM hidden state that maximize correlation. | Uses spatial detail. | Identifiability issues; requires train/test split; risk of overfit. |
| C. Mutual information | Estimate I(φ★; BOLD_pattern) via k-NN entropy estimator. | Captures nonlinear dependence. | High variance estimator at our window count; coarse for small N. |

**Decision: A is the production framework. B and C reserved for Phase-3 exploratory analyses.**

---

## 7. License compatibility ranking

| Dataset | License | Anima training use | Anima public model release | Notes |
|---|---|---|---|---|
| **Lebel 2023 ds003020** | CC0 (OpenNeuro default) | YES, no restrictions | YES, model derived OK | Best license for downstream release. No HIPAA identifiers per OpenNeuro policy. |
| **cNeuroMod / Algonauts 2025 derivatives** | CC-BY 4.0 (CONP / Brain Canada) | YES, with attribution | YES with attribution + provenance disclosure | Requires citing cNeuroMod, Brain Canada, CONP, Algonauts 2025. Underlying Friends video stays Warner Bros. — we never redistribute video. Transcripts are short consumed-as-input quotations; legal review recommended before any public release of a model trained on Friends transcripts. |
| **Wen 2017** | CC-BY 0 | YES | YES with attribution | No text — out of scope for anima. |
| **Lahner 2024 BOLD Moments** | CC0 | YES | YES | Captioned 3 s clips; poor token-rate density; Phase-3 only. |
| **HCP 7T movie** | HCP DUA (researcher agreement) | YES with DUA | **NO** unless explicit re-licensing — model trained on HCP cannot be released openly. | Blocks anima public release by default. Defer. |

**Ranking for anima public release safety:** Lebel ds003020 > Algonauts (legal review required) > Lahner > Wen > HCP (blocked).

**IRB / ethics:** Anima training on these datasets does NOT itself require new IRB approval (we use already-approved derivative data). However, if anima is later used in any human-subjects experiment (e.g., decoding from new fMRI), that experiment requires fresh IRB review at the executing institution.

**Privacy:** Subject-level BOLD does NOT contain PHI per OpenNeuro / cNeuroMod policy (face-stripped structurals; no DOB / zip). Anima must NOT log raw subject identifiers in evaluation outputs — use opaque hashes (e.g., `sub-h_a3f9` instead of `sub-01-aiden-...`) in any released artifacts.

---

## 8. Honest C3 (≥5 caveats; mandatory per raw#91)

1. **Linear projector limit.** A linear P_S can only express the part of the brain↔CLM mapping that is linear in CLM hidden coordinates. Whatever residual is genuinely nonlinear becomes irreducible MSE — we will see this as an SNR ceiling on F4 r. We accept this in exchange for identifiability (§1.4); a nonlinear P_S would invalidate the meaning of "brain alignment" by absorbing arbitrary CLM-side rotations.

2. **HRF subject variability.** The canonical Glover-1999 HRF assumes a fixed double-gamma form with peak +5 s and undershoot +15 s. Real HRFs vary by ±1.5 s in peak latency and ±25 % in amplitude across subjects and brain regions. Our γ-loss treats this as residual MSE; group-level r will systematically underestimate per-subject best-case r by an amount roughly equal to inter-subject HRF dispersion (~10–15 % of ceiling).

3. **BOLD ↔ φ★ ontological gap.** BOLD is a 5-s-smoothed vascular response to metabolic demand. φ★ (IIT 4.0 per Albantakis 2023; ΦID per Mediano 2022) is defined on causal mechanisms in a system's state space. The two quantities are NOT in 1:1 correspondence. Strong F4 (good BOLD prediction) does NOT entail strong φ★. Likewise, high CLM φ★ does NOT guarantee BOLD-similarity. We treat these as complementary, not redundant — the cross-substrate test (§6) is a correlation hypothesis, NOT a reduction.

4. **Vertex resolution tradeoff.** Schaefer-1000 averages voxels within parcels, lifting SNR but losing within-parcel functional heterogeneity. Functions known to be sub-parcel (e.g., fine semantic gradients in left ATL per Huth 2016) become invisible. fsaverage5 (20× more output dim) recovers some of this but at 20× the P_S parameter count. We accept the Schaefer-1000 floor as the price for compute tractability and Algonauts-native compatibility.

5. **Inter-subject reliability ceiling.** Human-to-human correlation on the same Friends episode chunk is itself only r ≈ 0.3–0.5 per parcel (Algonauts 2025 inter-subject ceiling). Our F4 cannot exceed this ceiling — even a perfect model trained on subject A's brain CANNOT predict subject B's BOLD with r > 0.5. The aspirational F4-tier (r ≥ 0.50) is therefore unreachable without subject-specific fine-tuning, regardless of model quality.

6. **Stimulus modality asymmetry.** Subjects watched Friends with full audio + video + emotional context; CLM consumes only the transcript. Visual face cues, music, laugh tracks, embodiment — all missing. TRIBE v2 itself uses video+audio+text and reaches r ≈ 0.3 on movie ROIs; our text-only model has a structurally lower ceiling, perhaps r ≈ 0.2 on visual / auditory cortices. F4_lang is the relevant slice; whole-cortex F4 will be diluted.

7. **Window-level cross-substrate test power.** §6 LME has ~12 subjects × ~100 chunks × ~30 windows ≈ 36 000 observations BUT effective N is far smaller after autocorrelation deflation (~5–10 K independent samples). Cross-substrate Spearman ρ has CI roughly ±0.02 at this N — small effects detectable, but β1 estimates need the LME random-slope structure to avoid Simpson reversal across subjects.

8. **License heterogeneity.** Mixing CC0 (Lebel) with CC-BY-4.0 (cNeuroMod / Algonauts) in a single training run produces a derived model whose redistribution is governed by the MOST restrictive parent license — CC-BY 4.0 with attribution. The Friends underlying video remains Warner Bros. copyright; transcripts are quotations consumed as training input only. Pre-release legal sign-off required for any public anima model trained on Algonauts data.

---

## 9. Concrete recommendations for paradigm-A' runbook updates

The following deltas can be folded into `docs/p9_paradigm_a_prime_runbook_2026_05_03.md` and `loss_design.json` at the next planning checkpoint:

1. **P_S architecture:** lock to rank-256 reduced-rank linear (768 → 256 → 1 000) with ridge λ=10⁻²; freeze after 200 warmup steps; report rank and Frobenius norm per eval. (§1.2, §1.4)
2. **HRF kernel:** SPM canonical Glover-1999 double-gamma at 2 Hz, 32 taps, 16 s coverage. No subject-specific HRF in Phase-2. (§2.1, §2.3)
3. **F4 thresholds:** retire single `r > 0.5` from spec; adopt tiered bronze 0.10 / silver 0.20 / gold 0.30 / aspirational 0.50. (§3.3)
4. **Vertex resolution:** Schaefer-1000 primary; P_S output dim configurable for fsaverage5 cross-dataset eval. (§4)
5. **Add consciousness-marker eval pass** (DMN_z + BEN + LZc + GBC_top10 per 30 s window) and cross-substrate LME (§6) as a Phase-2 closure deliverable. Compute requirement: marginal (BEN/LZc are ~O(T_window · V) per subject; LME fits in seconds).
6. **License posture:** anima public release plan must specify "Lebel-only model" vs "Lebel + Algonauts model"; second option requires legal review.

---

## 10. References (selected)

- Albantakis, L. et al. (2023). *Integrated Information Theory (IIT) 4.0: Formulating the properties of phenomenal existence in physical terms.* PLOS Comp Biol.
- Bullmore, E. et al. (1996). *Statistical methods of estimation and inference for functional MR image analysis.* Magnetic Resonance in Medicine.
- Casali, A.G. et al. (2013). *A theoretically based index of consciousness independent of sensory processing and behavior.* Sci Transl Med — Perturbational Complexity Index (PCI).
- Chen, G. et al. (2013). *Linear mixed-effects modeling approach to FMRI group analysis.* NeuroImage.
- Cole, M.W., Yarkoni, T., Repovš, G., Anticevic, A., Braver, T.S. (2012). *Global Connectivity of Prefrontal Cortex Predicts Cognitive Control and Intelligence.* J Neurosci.
- Crone, J.S. et al. (2011). *Deactivation of the Default Mode Network as a Marker of Impaired Consciousness.* PLOS ONE.
- Friston, K., Henson, R. (2007). *Convolution models for fMRI.* (and Henson & Friston SPM book ch 14 on HRF basis sets).
- Glover, G.H. (1999). *Deconvolution of impulse response in event-related BOLD fMRI.* NeuroImage — the canonical double-gamma HRF.
- Huth, A.G. et al. (2016). *Natural speech reveals the semantic maps that tile human cerebral cortex.* Nature.
- LeBel, A. et al. (2023). *A natural language fMRI dataset for voxelwise encoding models* (OpenNeuro ds003020). Scientific Data.
- Lindquist, M.A. et al. (2009). *Modeling the hemodynamic response function in fMRI: Efficiency, bias and mis-modeling.* NeuroImage.
- Luppi, A.I. et al. (2023). *An implementation of integrated information theory in resting-state fMRI.* Communications Biology.
- Mediano, P.A.M. et al. (2022). *The strength of weak integrated information theory.* Trends Cog Sci. (and ΦID — Information decomposition and the informational architecture of the brain, Trends Cog Sci 2023).
- Menon, V. (2023). *20 years of the default mode network: a review and synthesis.* Neuron.
- Naselaris, T. et al. (2011). *Encoding and decoding in fMRI.* NeuroImage — the encoding-model primer.
- Nichols, T.E., Holmes, A.P. (2002). *Nonparametric permutation tests for functional neuroimaging.* HBM.
- Pasquiou, A. et al. (2022). *Neural Language Models are Not Born Equal to Fit Brain Data, but Training Helps.* arXiv:2207.03380. (and *Information-Restricted Neural Language Models…*, Neurobiology of Language 2023).
- Raichle, M.E. et al. (2001). *A default mode of brain function.* PNAS.
- Saxe, G.N. et al. (2018). *Brain entropy and human intelligence: A resting-state fMRI study.* PLOS ONE.
- Schaefer, A. et al. (2018). *Local-Global Parcellation of the Human Cerebral Cortex from Intrinsic Functional Connectivity MRI.* Cerebral Cortex.
- Schartner, M. et al. (2017). *Complexity of multi-dimensional spontaneous EEG decreases during propofol induced general anaesthesia.* PLOS ONE — LZc methodology.
- Tang, J., LeBel, A., Jain, S., Huth, A.G. (2023). *Semantic reconstruction of continuous language from non-invasive brain recordings.* Nature Neuroscience. (and *Scaling laws for language encoding models in fMRI*, NeurIPS 2024 / PMC 2024.)
- Theiler, J. et al. (1992). *Testing for nonlinearity in time series: the method of surrogate data.* Physica D.
- Toker, D., Sommer, F.T. (2022). *Information integration in large brain networks.* PLoS Comp Biol.
- Tononi, G. (2014). *Integrated Information Theory.* Scholarpedia.
- VEM tutorial (2025). *The Voxelwise Encoding Model framework: A tutorial introduction to fitting encoding models to fMRI data.* Imaging Neuroscience (MIT Press).
- Vu, M.A. et al. (2025) *TRIBE: TRImodal Brain Encoder for whole-brain fMRI response prediction.* arXiv 2507.22229; Meta AI release notes; *A foundation model of vision, audition, and language for in-silico neuroscience* (Meta FAIR research).
- Wang, Z. et al. (2014). *Brain Entropy Mapping Using fMRI.* PLOS ONE.
- Wehbe, L. et al. (2014). *Aligning context-based statistical models of language with brain activity during reading.* EMNLP.
- eLife (2024). *Spatiotemporal brain complexity quantifies consciousness outside of perturbation paradigms.* eLife reviewed preprint 98920.

---

*End of research doc. No code, no execution. Doc-only per raw#9.*
