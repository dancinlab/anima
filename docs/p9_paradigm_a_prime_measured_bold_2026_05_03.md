# P9 Paradigm A' — Measured fMRI BOLD Active Integration Learning

**Date:** 2026-05-03
**Status:** Spec / research design (no execution)
**Author:** Anima research agent (P9 Phase 2+ paradigm research thread)
**Substrate refs (READ-ONLY):**
- `references/tribev2/inventory.json`
- `references/tribev2/tribev2/studies/{algonauts2025,lebel2023bold,lahner2024bold,wen2017}.py`
- `state/p9_sft_spec_2026_05_02/loss_design.json`

---

## 0. TL;DR

**Paradigm A** (status quo) trains the CLM to match BOLD predicted by **TRIBE v2 forward** from the same text the CLM consumes. This is structurally **circular**: the supervisor is itself a text→BOLD model, so the CLM can collapse into reproducing TRIBE's text-encoder readout rather than learning a brain-aligned latent.

**Paradigm A'** replaces the TRIBE-simulated target with **measured BOLD** from human subjects exposed to the *same* stimulus (movie clip / spoken story). The supervision signal is no longer model-internal; it is ground-truth fMRI. Circularity is removed; the residual circularity (model-of-the-brain in the loss) is reduced from "TRIBE outputs" to "the projector P_S only," which is much smaller and falsifiable.

**Top-2 candidate datasets (verdict):**

1. **Algonauts 2025 / cNeuroMod-Friends + movie10** — *USE AS PRIMARY.* CC-BY 4.0 stimuli/derivatives, DataLad-cloneable, time-aligned word-level transcripts, TR=1.49 s, MNI / Schaefer-1000 + fsaverage available. Only 4 subjects but ~1588 timelines (~150 h fMRI) per subject. Already wired in `tribev2/studies/algonauts2025.py`.
2. **Lebel et al. 2023 (OpenNeuro ds003020)** — *USE AS SECONDARY.* CC0, 8 subjects, TR=2.0 s, audio narratives + word/phoneme TextGrid, fsaverage space available. Larger per-subject data for top-3 subjects (~20 sessions). Stricter language paradigm — ideal F4 holdout.

**Hemodynamic alignment recommendation:** **canonical-HRF convolution on token-rate predictions** (the standard encoding-model approach), NOT lag-shift, NOT learnable delay (rationale §2). Combine with TRIBE v2's existing fixed +5 s offset for sanity check.

**γ-only mini-run cost (5–10 K steps, 1×H100 spot):** ≈ **9–18 USD wall, 4–8 h** (detail §4).

**F4 verification feasibility:** **YES** with held-out subject in same dataset; threshold Pearson r > 0.5 is *aspirational* — current SoTA voxel-level encoding models reach r ≈ 0.3–0.5 on held-out language fMRI. Recommend a tiered pass criterion (§5).

---

## 1. Dataset identification

All four are already enumerated as TRIBE v2 training studies (inventory.json, studies/__init__.py). For Paradigm A' we **bypass the TRIBE forward** and use these datasets *directly* as supervision targets.

| Dataset                    | License        | Subjects | Stimulus type           | Hours fMRI / subj | TR (s) | Native space + atlas                  | Cortex output                   | Text alignment                 | Accessibility |
|----------------------------|----------------|----------|-------------------------|-------------------|--------|---------------------------------------|---------------------------------|--------------------------------|---------------|
| Algonauts 2025 (cNeuroMod) | CC-BY 4.0      | 4        | Friends + 4 movies      | ~30+ h            | 1.49   | MNI152NLin2009cAsym + Schaefer-1000   | Schaefer-1000 parcels (default) | word-level TSV (per-TR)        | DataLad clone, several GB |
| Lebel 2023 (ds003020)      | CC0            | 8 (3 ext)| Spoken English stories  | ~7 h (UTS01-3)    | 2.0    | T1w / MNI152NLin6Asym / fsaverage     | fsaverage (163 842 v/hem)       | TextGrid (word + phoneme)      | OpenNeuro public, no auth |
| Wen 2017                   | CC-BY 0        | 3        | Natural video           | ~2 h              | 2.0    | MNI                                   | volumetric                      | none (visual only)             | direct download |
| Lahner 2024 BOLD Moments   | CC0            | 10       | 1 000 × 3-s videos      | ~3.5 h            | 1.75   | MNI / T1w / fsaverage / fsnative      | fsaverage 163 842 v/hem         | LLM-generated frame captions    | OpenNeuro public |
| HCP 7T movie               | (mentioned, not in TRIBE) | 184 | 4 × 15-min movie       | ~1 h              | 1.0    | MSMAll / fsLR-32k                     | fsLR 32 k vertices              | full transcripts available     | requires HCP DUA acceptance |

**Vertex resolution clarification:** the **fsaverage5 = 10 242 / hemisphere = 20 484 total** convention used in `loss_design.json` corresponds to a **downsampled fsaverage** that TRIBE v2 plotting uses (`tribev2/plotting/cortical.py`). Lebel 2023 / Lahner 2024 are stored at **full fsaverage = 163 842 / hemi** and must be downsampled (FreeSurfer `mri_surf2surf --trgsubject fsaverage5`) before MSE comparison. Algonauts 2025 default is parcellated (1 000 parcels) — needs surface re-projection or use of cNeuroMod surface derivatives (`*.func.gii`).

**Selection ranking for Paradigm A':**

1. **Algonauts 2025** — best stimulus / text density (movies + sitcom dialog). Word-level TR-aligned transcripts already provided (`stimuli/transcripts/*.tsv` with `words_per_tr`, `onsets_per_tr`, `durations_per_tr` columns — see `algonauts2025.py:240-244`). Ideal for token↔BOLD pairing.
2. **Lebel 2023** — purely linguistic (spoken stories), TextGrid timing, full fsaverage surface. Use for **F4 holdout** (cross-dataset generalization test) and as a pure-language sanity training set.
3. **Lahner 2024** — captioned videos but stimuli are 3-s clips → poor for token-rate sequence learning. Use only for F-stage cross-modal probes.
4. **HCP 7T movie** — high-resolution, many subjects, but DUA + lower text density. Defer.
5. **Wen 2017** — no text. Out of scope for Paradigm A'.

---

## 2. Loss formulation & hemodynamic alignment

### 2.1 Loss form

Refining `loss_design.json` `L_bold` term:

```
L_bold_measured(θ) = γ · (1 / (B·T_TR·V)) · Σ_{b,τ,v} (BOLD_pred[b,τ,v] − BOLD_meas[b,τ,v])²
```

where:
- `BOLD_pred[b,τ,v] = (HRF * (P_S · h_θ))[b, τ, v]` — model hidden states `h_θ` projected through projector `P_S` (alm_clm_bridge_p_s_projector_spec_20260425.md), **resampled to TR rate**, **convolved with canonical HRF**.
- `BOLD_meas[b,τ,v]` — measured fMRI from one subject, on the **same** chunk of stimulus (Friends episode chunk, story segment).
- `τ` indexes TR steps (one every 1.49 s for Algonauts), `v` indexes vertices/parcels.
- Optional **z-score per run per vertex** before MSE (standard fMRI encoding-model preprocessing — removes drift/scanner gain).

### 2.2 Three alignment options (decision)

| Option | Description | Pros | Cons | Recommendation |
|--------|-------------|------|------|----------------|
| (A) Lag-shift | Shift model output by fixed +5 s before MSE (TRIBE v2 default, inventory.json `hemodynamic_lag_offset_seconds: 5`) | Cheap; matches TRIBE pipeline | Discards HRF shape; assumes peak-only matters; brittle to dataset TR | Sanity baseline only |
| (B) **Canonical HRF convolution** | Convolve `P_S(h_θ)` with double-gamma SPM canonical HRF before downsampling to TR | Standard encoding-model practice (Huth, Lebel); differentiable; matches BOLD physics | One extra conv1d (cheap); fixes HRF shape | **PRIMARY — adopt** |
| (C) Learnable per-vertex HRF | Add small MLP / FIR filter to learn delay | Flexible; per-region HRF differences | Identifiability problem (HRF vs. neural signal entangled); risk of absorbing model errors into "HRF"; ~10× params | Defer to Phase 3+ if (B) saturates |

**Decision: adopt (B) canonical HRF.** Implementation:
1. Sample `P_S(h_θ)` at the model token rate (assume ~2 Hz "processing frequency" per inventory.json).
2. Convolve along time axis with SPM canonical HRF (peak ~5 s, undershoot ~15 s; precomputed 32-tap kernel at 2 Hz).
3. Downsample (decimate) to 1/TR Hz.
4. Trim transient to discard convolution edge.
5. MSE against `BOLD_meas` after per-vertex z-scoring (per run).

This reuses TRIBE v2's `utils_fmri.py` HRF utilities where possible — but **without** any other TRIBE forward path. The projector `P_S` is the only learned brain-side surface, and it is small (linear or low-rank, per existing P_S spec).

### 2.3 Pairing CLM input to brain signal (token↔TR)

The CLM is a next-token transformer over **the same stimulus text** the subject heard/saw. Concretely for an Algonauts Friends episode chunk:

- Stimulus = `friends_s01e01a.mkv` (≈5 min).
- Transcript = TSV with `words_per_tr` (lists of words seen during each TR).
- BOLD = h5 array `[1000_parcels, T_TR]` for the same chunk.

Training pair construction:
1. Concatenate all words in the chunk in onset order → token sequence `x_{1..N}` (Llama-3 tokenization).
2. For each token `i`, record the TR index `τ(i) = floor(onset_i / 1.49)`.
3. Forward CLM on `x` → hidden states `h_{1..N} ∈ R^d`.
4. **Bin** hidden states by TR: `H_τ = mean_{i: τ(i)=τ} h_i` (or attention-weighted; mean is the simplest baseline).
5. Apply `P_S` per TR: `BOLD_pred[τ, :] = P_S(H_τ)`.
6. Convolve over τ with HRF; align to `BOLD_meas[τ:τ+T_chunk, :]`.

**TR-step alignment cheat-sheet:**
- TRIBE v2 inventory.json: model `processing_frequency_hz: 2`, `output_frequency_hz: 1`, TR 1.49 s.
- We mirror this: 2 Hz internal, 1/1.49 ≈ 0.671 Hz output, HRF lag baked in by convolution (no manual +5 s shift).

### 2.4 Combined Phase 2 loss

Updating `loss_design.json` formula for Paradigm A':

```
L = α·CE(text)
  + β·MSE(tension_pred, tension_target)
  + γ·MSE(BOLD_pred_HRF, BOLD_measured)        # ← was TRIBE-simulated; now measured
  + δ·max(0, φ★_threshold − φ★(model))
```

Same shape as Paradigm A; only the γ-target changes from `TRIBE_v2_forward(text)` to `measured_fMRI(subject, same_text)`.

---

## 3. Compute estimate (γ-only mini-run)

### 3.1 Data volume

Algonauts 2025 only:
- 4 subjects × 1 588 timelines (Friends + movie10 train split) = ~6 350 timelines.
- Avg chunk ≈ 5 min = 300 s ⇒ ~200 TR / chunk ⇒ ~1.27 M TR-steps total.
- 1 000 parcels per TR ⇒ ~1.27 G TR-vertex pairs.
- Token-text scale: ~5 M words across Friends 7 seasons (~7 M tokens).

Lebel 2023 supplement:
- 8 subj × ~26 stories × ~10 min × 30 TR/min ≈ 60 K TR-steps × 163 842 vertices (or 10 242 if fsaverage5).

**Mini-run scope:** subset = sub-01 only, Friends seasons 1–2 (~25 episodes × 4 chunks = 100 chunks ≈ 8 h fMRI ≈ 20 K TR-steps). Token count ≈ 200 K tokens. Sequence length 1 024 ⇒ ~200 microbatches per epoch.

### 3.2 Compute budget — 1×H100 spot

Assumptions:
- Llama-3.2-3B base CLM (TRIBE-compatible).
- Frozen base + LoRA-adapter + projector P_S (low-rank 2 048 → 1 000 parcels).
- HRF conv: 32-tap conv1d, negligible.
- Batch=8, seq=1 024, BF16, ZeRO-1.
- ~2.5 steps/sec for LoRA-only Llama-3.2-3B on H100 at 1 024 ctx (empirical anchor: P9 P0 warmup numbers in `state/p9_p0_warmup_live_2026_05_03/`).

| Item                | Value |
|---------------------|-------|
| Steps               | 5 000 (low) – 10 000 (high) |
| Throughput          | ~2.5 steps/s |
| Wall time           | 33 min – 67 min compute, +I/O & eval ⇒ **2 – 4 h end-to-end** |
| H100 spot price     | ~2.20 USD/h (RunPod typical) |
| **Cost estimate**   | **5 – 10 USD** for 5 K steps; **10 – 18 USD** for 10 K steps |

Storage: Algonauts 2025 sub-01 chunk = ~25 GB raw + ~5 GB parcellated. Network egress one-time. Acceptable.

### 3.3 Triangulation against existing P9 P0 numbers

Compare to `state/p9_p0_warmup_live_2026_05_03/` (1 K SFT subset, similar config) — that ran in well under 1 h. 5–10 K steps with added BOLD MSE branch (extra ~10 % FLOPs) ⇒ **2–4 h end-to-end is consistent**. Confidence: medium-high.

---

## 4. F4 verification path

**F4 = "Does the trained CLM produce BOLD that matches measured BOLD on UNSEEN data?"**

### 4.1 Holdout design

- **Within-subject holdout** (easier): hold out Friends season 7 (Algonauts test split — already has no fMRI public; use a season-6 episode chunk we artificially exclude from training).
- **Cross-subject holdout** (medium): train on sub-01,02; test on sub-03 (zero-shot subject). TRIBE inventory.json claims `zero_shot_subjects: true` so the projector should be subject-agnostic if implemented as such; if subject-conditional, swap to subject-embedding leave-one-out.
- **Cross-dataset holdout** (hardest): train on Algonauts; eval on Lebel ds003020. Gold standard but penalized by domain shift (sitcom dialog → narrative story).

### 4.2 Metric

Per held-out (subject × chunk × vertex) tuple:

```
r_v = Pearson( BOLD_pred[:, v], BOLD_meas[:, v] )
F4_score = mean over vertices of r_v          # whole-cortex mean
F4_lang  = mean over language-network vertices of r_v   # ROI focus
```

### 4.3 Pass thresholds (tiered)

| Tier | Threshold | Interpretation |
|------|-----------|----------------|
| F4-bronze | F4_lang ≥ 0.10 | Above-chance brain alignment |
| F4-silver | F4_lang ≥ 0.20 | Comparable to weak text-only encoding models (early Huth-lab) |
| F4-gold | F4_lang ≥ 0.30 | Comparable to strong contemporary encoding models (Lebel 2023, TRIBE v2 reported numbers) |
| F4-aspirational | F4_lang ≥ 0.50 (user-spec) | Exceeds published SoTA — would be a publishable result by itself |

**Honest verdict on the user-spec >0.5 threshold:** this is *not realistic* for a 5–10 K-step γ-only mini-run on 1 subject. Published encoding models trained for days on full Lebel data hit r ≈ 0.30–0.45 in language ROIs. A mini-run reaching F4-bronze (0.10) would already be a positive signal; F4-silver (0.20) is the realistic Phase-2 target.

### 4.4 Statistical sanity

- Compute null distribution by phase-randomizing predicted BOLD time series (preserves spectrum, breaks alignment); declare F4 PASS only if observed r exceeds 95th-percentile null.
- Report per-subject + per-network breakdown (Yeo-7 networks); a CLM that only matches the **language network** is meaningful even if global r is low.

---

## 5. Integration claim — honest gap analysis

The Paradigm A' loss term `γ·MSE(BOLD_pred, BOLD_meas)` is sometimes pitched as "matching brain integration." This is **not literally true**. The honest chain of inference is:

```
neural firing  →  metabolic demand  →  cerebral blood flow  →  BOLD signal  →  φ★ (offline, via Bayesian
                                                                                    inversion of state-space model)
```

What MSE-on-BOLD actually optimizes:
- ✅ Match the **vascular response** to stimulus content (good proxy for regional engagement).
- ✅ Match **inter-regional coactivation patterns** (functional connectivity shape).
- ⚠️ Does NOT directly match **integrated information** φ — BOLD is a coarse spatiotemporal smear; φ (IIT 4.0, Tononi 2014; Mediano et al. 2022 ΦID) is computed on neural state-spaces and requires a much higher-resolution causal model.
- ⚠️ Does NOT match **ignition / global workspace** (Dehaene-Changeux) signatures directly — those need EEG/MEG temporal precision (TR=1.49 s misses the 50–300 ms ignition window).

**Cited literature (selected):**
- Tononi 2014 IIT3.0, Albantakis 2023 IIT4.0 — φ defined on causal mechanisms, not BOLD.
- Mediano et al. 2022 (ΦID, integrated information decomposition) — explicitly notes BOLD-based φ proxies are *lower bounds* and have ~30 % rank correlation with simulator-truth φ.
- Casali et al. 2013 PCI — BOLD-derived complexity measures correlate with conscious state but have ~5–10 % AUC vs PCI on TMS-EEG.
- Lebel 2023 / Huth 2016 — text→BOLD encoding models reach r ≈ 0.3–0.5 on language ROIs without making any φ claim.

**Bottom-line statement Anima can defend:**

> "Paradigm A' trains the model so its internal state, when projected through a small linear map P_S and convolved with the canonical HRF, matches measured fMRI responses of human subjects to the same text. This is a faithfulness constraint on the *external* projection of the model's state, not a direct optimization of φ★. We separately monitor φ★ via L_phi (δ term) on the model's own dynamics; the two losses are *complementary* — A' grounds the projection in human data, L_phi enforces the integration property internally."

---

## 6. Phase 2 entry plan

### 6.1 Sequencing

1. **Pre-flight (no compute):** lock dataset to Algonauts 2025 sub-01, Friends s01–s02; verify DataLad clone works on RunPod node; prebake parcellated h5 + transcript TSV pairs into a flat Parquet (`pair_id, token_ids, tr_index, parcel_bold[1000]`). Output: `state/p9_paradigm_a_prime_data_v0/`.
2. **γ-only mini-run (5 K steps, 1×H100 spot, ~5–10 USD):**
   - α=0, β=0, γ=1.0, δ=0 (lock all but BOLD MSE).
   - LoRA-only on Llama-3.2-3B, projector P_S trainable, HRF kernel fixed.
   - Eval cadence: F4 within-subject holdout every 500 steps.
   - **Gate to Phase 2 full:** F4-bronze (lang r ≥ 0.10) within 5 K steps.
3. **γ-only extended (10 K steps, +Lebel ds003020 supplement):** target F4-silver (0.20).
4. **Phase 2 4-loss combo:** unfreeze all four (α, β, γ, δ) with the user's existing Latin Hypercube sweep over 9-of-81 combos (loss_design.json `balance_strategy`). γ now uses *measured* targets.
5. **Phase 2 closure:** report F4 + F1/F2/F3 jointly; honest C3 covers all four loss tradeoffs.

### 6.2 Suggested weights for combo (initial guess, to be swept)

Based on raw activation magnitudes (rough order-of-magnitude):

| term | weight | rationale |
|------|--------|-----------|
| α (CE)        | 1.0   | reference scale |
| β (tension)   | 0.1   | tension MSE typically 10× larger than CE in nats |
| **γ (BOLD measured)** | **0.05** | BOLD MSE per-vertex ≈ 1–2 (z-scored), mean over 1 000 parcels ≈ 1; downweight to keep CE dominant during early SFT |
| δ (φ★ floor)  | 0.01  | only fires when φ★ < 5; usually zero |

Run LH-9 sweep within ±0.5 dex of these.

### 6.3 Integration with existing P9 spec

- This doc **supersedes** `loss_design.json` `L_bold` *only* for runs labeled "Paradigm A'". Paradigm A (TRIBE-simulated) remains as the simulator-based baseline.
- The projector P_S (alm_clm_bridge_p_s_projector_spec_20260425) is **shared** between A and A' — same architecture, different supervision target.
- F4 metric definition in §4 should be added as a new state file: `state/p9_paradigm_a_prime_f4_spec/metric.json` (no .py — config only).

---

## 7. Honest C3 (≥5 caveats)

Per raw#91 mandatory.

1. **Hemodynamic temporal smearing.** BOLD lags neural activity by ~5 s and smears it over ~15 s. Even perfect HRF deconvolution loses sub-second dynamics — most ignition / binding signatures live there. Paradigm A' can match the **slow envelope** of brain activity but will be blind to fast integration phenomena.
2. **Subject variability.** Algonauts 2025 has only 4 subjects; cross-subject Pearson r between two humans on the same Friends episode is itself only ~0.3–0.5 per parcel (the inter-subject correlation ceiling). Our F4 target inherits this ceiling — we cannot exceed inter-human reliability.
3. **Vertex-/parcel-level noise.** Single-trial BOLD has SNR ~0.1–0.3 per voxel. Schaefer-1000 parcellation averages voxels and lifts SNR but loses spatial detail. Either way, MSE on raw BOLD chases substantial irreducible noise — γ should be tuned so this noise floor doesn't dominate gradients.
4. **Dataset license heterogeneity.** Lebel ds003020 is CC0 (commercial OK). Algonauts/cNeuroMod data are CC-BY 4.0 for derivatives but the underlying Friends video is **copyrighted** (Warner Bros.); we never redistribute the video, only consume its transcript + the cNeuroMod-released BOLD. HCP requires DUA. **Action:** confirm Anima's downstream model release does not embed copyrighted text verbatim; transcripts are short quotations in training data only. Get legal sign-off before any model release that was trained on Friends transcripts.
5. **"BOLD ≈ φ" gap.** §5 above. MSE-on-BOLD optimizes a vascular-spatial proxy. Strong F4 does NOT imply φ★ improvement; we must continue to measure φ★ on the model's *own* dynamics and not collapse the two metrics.
6. **Tokenization mismatch.** TRIBE / Llama-3.2 tokenizes BPE; transcripts in Algonauts are word-level. A long word may span TRs; a short TR may contain many tokens. The TR-binning step (§2.3 step 4) is a lossy aggregation and may bias toward content words over function words. Sensitivity analysis required.
7. **Stimulus exposure asymmetry.** Subjects watched the movies once or a few times, with attention, embodiment, and prior life context. The CLM consumes only the transcript text. Visual / auditory / emotional context is missing — we are asking text-only CLM internals to predict BOLD that was driven by full audiovisual stimuli. Expected ceiling on F4 is correspondingly lower than for a multimodal model (TRIBE v2 itself uses video+audio+text).
8. **Projector P_S identifiability.** The MSE loss flows through P_S; if P_S is high-rank, it can absorb arbitrary CLM-state shape and still match BOLD without the CLM learning anything brain-like. Mitigation: keep P_S **low-rank (≤ 256)** and freeze it after a brief warmup, OR regularize with a sparsity prior on P_S. Without this guard, F4 PASS is meaningless.
9. **Mini-run statistical power.** 5–10 K steps on 1 subject's Friends s01–s02 produces ~20 K TR-steps. F4 r-values computed on a single held-out chunk (~200 TR) have wide CIs (±0.07 at r=0.2). Treat mini-run F4 as directional, not definitive.

---

## 8. Pointers / next steps (no execution)

- Author state config: `state/p9_paradigm_a_prime_spec_2026_05_03/{datasets.json, alignment.json, loss.json, f4_metric.json, mini_run_plan.json}` (config only, no .py per raw#9).
- Verify HRF kernel availability in `tribev2/utils_fmri.py` (read-only inspection) — if absent, plan to use `nilearn.glm.first_level.glover_hrf` (already a transitive dep).
- Pre-flight DataLad clone size check on RunPod (read-only Bash on next session).
- Coordinate with P_S projector spec author to confirm low-rank constraint is enforced.

---

## 9. Decision summary table

| Question (from prompt) | Decision |
|---|---|
| Top-2 candidate datasets | Algonauts 2025 (primary), Lebel 2023 ds003020 (secondary) |
| Hemodynamic alignment scheme | Canonical HRF convolution at token rate (option B); reject lag-shift and learnable HRF for Phase 2 |
| Token↔TR pairing | TR-bin token hidden states by mean over tokens whose word-onset falls in that TR |
| Mini-run cost | 5–18 USD, 2–4 h on 1×H100 spot for 5–10 K steps |
| F4 feasibility | Yes; user >0.5 target unrealistic for mini-run; tiered F4-bronze 0.10 / silver 0.20 / gold 0.30 / aspirational 0.50 |
| Integration claim status | "BOLD-projection faithfulness," NOT "φ optimization"; keep L_phi separate |
| Phase 2 entry | γ-only mini-run gated by F4-bronze, then 4-loss LH-9 sweep with γ measured |
| Honest C3 caveats | 9 listed (≥5 required) |

---

*End of spec. No code, no execution. Doc-only per raw#9.*
