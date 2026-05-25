# BOLD / fMRI Dataset Landscape — Anima Paradigm A' candidate research

**Date:** 2026-05-03
**Status:** Web research synthesis (NO download, NO execution)
**Author:** Anima research agent (P9 Phase 2+ paradigm research thread)
**Substrate refs (READ-ONLY):**
- `docs/p9_paradigm_a_prime_runbook_2026_05_03.md` — current Algonauts 2025 sub-01 pre-flight state
- `docs/p9_paradigm_a_prime_measured_bold_2026_05_03.md` — Paradigm A' loss spec, F4 metric, HRF strategy

**Scope:** Comprehensive comparison of public BOLD/fMRI datasets for use as **measured supervision target** in Paradigm A'. The runbook locked Algonauts 2025 sub-01 as the primary mini-run substrate; this research evaluates 16 candidates so cross-substrate, cross-stimulus, and cross-license generalization can be planned.

---

## 0. TL;DR

**Top 3 by Anima fit:**
1. **Algonauts 2025 / cNeuroMod-Friends + movie10** — primary (already wired, CC0 derivatives, ~65 h training data, word-level TR-aligned transcripts).
2. **Lebel 2023 (ds003020)** — F4 holdout (CC0 *unrestricted*, full fsaverage surface, TextGrid word + phoneme alignment, 8 subjects × ~6 h).
3. **Narratives (ds002345)** — cross-stimulus generalization (345 subjects across 28 stories, ~5 h unique audio, time-stamped transcripts).

**Combined download size estimate (conservative parcellated subset):** ~250 GB; raw volumetric all-subjects: ~3 TB. Anima mini-run footprint stays at ~1 GB (sub-01-only Algonauts subset, already validated on ubu1).

**Multi-dataset cross-validation feasibility:** **Medium-high.** Algonauts (Schaefer-1000 parcels) ↔ Lebel (full fsaverage 163 842 v/hem) ↔ Narratives (fsaverage6 41 k v/hem) requires a vertex-/parcel-resampling step (`mri_surf2surf` + parcel pooling) but no other domain shift beyond stimulus modality (sitcom dialog vs. spoken story). HCP 7T movie watching adds 184-subject cross-subject ceiling but blocks public model release (DUA).

**Top 3 honest C3 caveats:**
1. **License heterogeneity blocks unified public release.** Algonauts/cNeuroMod = CC0 derivatives + copyrighted Friends video (we never redistribute); Lebel = CC0; Narratives = CC0; HCP / NSD / UK Biobank = restricted DUA. A model trained on the union cannot be re-released without per-dataset clearance.
2. **Vertex/parcel resolution is non-uniform and forces a coarse common space.** Schaefer-1000 (Algonauts) ≪ fsaverage5 (Anima `loss_design.json`) ≪ fsaverage6 (Narratives) ≪ fsaverage / fsLR-32k (Lebel/HCP). Cross-dataset MSE only meaningful after downsampling to the lowest common denominator, which discards spatial detail.
3. **Inter-subject Pearson r ceiling is ~0.3–0.5 in language ROIs.** F4_lang > 0.5 ("aspirational" tier) is impossible in principle; even infinite-data SoTA encoding models (Tang 2023, Lebel 2023) plateau near r ≈ 0.3–0.45.

---

## 1. Master comparison table (16 datasets, sortable by Anima fit)

Sorted by Anima fit score (high → low). **Anima fit = combined judgment on stimulus density × text alignment × license × ease-of-use × cross-validation utility.**

| # | Dataset | License | Subjects | Stim hours / subj | TR (s) | Native space + atlas | Text alignment | Anima fit | Download path |
|---|---------|---------|----------|-------------------|--------|----------------------|----------------|-----------|---------------|
| 1 | **Algonauts 2025 (cNeuroMod-Friends+movie10)** | **CC0** | 4 | ~65 (55 Friends s1-6 + 10 movie10) | 1.49 | MNI152NLin2009cAsym + Schaefer-1000 | word-level TSV per-TR (`words_per_tr`, `onsets_per_tr`, `durations_per_tr`) | **HIGH** | DataLad (GitHub) — `courtois-neuromod/algonauts_2025.competitors` |
| 2 | **Lebel 2023 (ds003020)** | **CC0** | 8 (3 ext) | ~6 (UTS01-3 ~16 h) | 2.0 | T1w / MNI152NLin6Asym / fsaverage (163 842 v/hem); 2.6 mm iso voxels | TextGrid (word + phoneme) | **HIGH** | OpenNeuro public (`ds003020`); ~20 GB DataLad |
| 3 | **Narratives (ds002345)** | **CC0** | 345 | ~5 unique audio (4.6 h ~43 K words) across 28 stories | 1.5 (most) | MNI / fsaverage / fsaverage6 (preprocs available) | phoneme + word time-stamps | **HIGH** | OpenNeuro `ds002345` (134.5 GB, 4 194 files) |
| 4 | **cNeuroMod-Friends (parent)** | **CC0** | 6 | ~60+ Friends + 12 movie10 + 10 hcptrt | 1.49 | MNI + Schaefer-1000 (default); fsaverage / fsLR available | same as Algonauts 2025 | **HIGH** | DataLad `courtois-neuromod/cneuromod` (registration via cneuromod.ca) |
| 5 | **Tang 2023 (16h podcast extension)** | **CC0** (within ds003020 framework) | 3 | ~16 spoken-story h | 2.0 | fsaverage | TextGrid | MED-HIGH | OpenNeuro `ds003020` (extended subjects within Lebel collection); HuthLab GitHub `deep-fMRI-dataset` |
| 6 | **StudyForrest (ds000113)** | **PDDL (~CC0)** | 20 (7T audio) + 15 (3T AV) | ~2 h Forrest Gump (audio; AV) | 2.0 (3T); 7T variants | T1 / MNI; surface-extractable; 3 mm AV | German script + audio-description annotation (Häusler 2021) | MED | studyforrest.org / OpenfMRI ds000113; multi-TB raw |
| 7 | **Sherlock (Princeton dataspace; ds001132 OpenNeuro)** | **CC0** (research-friendly) | 16 (17 collected) | ~50 min | 1.5 | MNI / fsaverage available | language annotations (Chen 2017) but not strict word-level timing; recall transcripts | MED | dataspace.princeton.edu (~109 GB) + OpenNeuro `ds001132` |
| 8 | **Pereira 2018 (toward universal decoder)** | **CC-BY 4.0** (Nat Commun supplemental) | 15 (E1) + 8 (E2) + 6 (E3) | minimal — 180 single words + 384 + 243 sentences | 2.0 (typical Siemens) | MNI volume; semantic-search vector targets provided | sentence/word *labels* only, no time-aligned audio | MED | OSF / supplemental — small, ~1 GB |
| 9 | **BOLD Moments (Lahner 2024, ds005165)** | **CC0** | 10 | ~3.5 h | 1.75 | fsaverage / fsnative / MNI | LLM-generated frame captions (5+ per clip) | MED | OpenNeuro `ds005165`; multi-100 GB |
| 10 | **Algonauts 2023 / NSD subset** | **NSD DUA (controlled)** | 8 | ~30–40 sessions × ~1 h images | 1.6 | fsaverage (visual-cortex vertices subset) | image captions (COCO) only | MED-LOW | algonauts.csail.mit.edu; NSD Data Access Agreement gated |
| 11 | **NSD (Natural Scenes Dataset, full)** | **NSD DUA** | 8 | 30 000–40 000 trials × ~1 s viewing | 1.6 | 1.8 mm iso T1w; fsaverage; fsLR | COCO captions per image | MED-LOW (vision only) | naturalscenesdataset.org → DUA → AWS S3 |
| 12 | **HCP 7T movie watching** | **HCP DUA (Open + Restricted)** | 184 | ~1 h (4 × 15 min) | 1.0 | MSMAll / fsLR-32k | full transcripts external (subject to copyright on movie clips) | MED-LOW | ConnectomeDB (login + DUA); ~10s of GB per subj | 
| 13 | **Algonauts 2021 (mini track)** | **MIT-research-only** | 10 | ~50 min × 1 102 × 3-s clips | non-standard (FIR betas) | ROI-summarized + WB voxel pickle | none (visual videos only) | LOW | algonautsproject.com/2021 (~few GB) |
| 14 | **Wehbe 2014 Harry Potter** | **CMU research** (request via authors / CMU) | 8 | ~45 min chapter 9 RSVP | 2.0 (4 words / TR) | MNI volume | RSVP word-locked 0.5 s/word + 195 syntactic/semantic features | LOW (small sample, RSVP not naturalistic) | http://www.cs.cmu.edu/~fmri/plosone/ direct |
| 15 | **HCP 1200 R-fMRI** | **HCP Open Access DUA** | 1 200 (1 113 with R-fMRI) | 4 × 15 min R-fMRI per subj | 0.72 | fsLR-32k MSMAll | none (resting state) | LOW (text-free; only useful for FC priors) | ConnectomeDB DUA |
| 16 | **UK Biobank fMRI** | **UKB Application + Cost** | ~100 K target (~50 K released) | ~6 min R-fMRI + ~4 min task | 0.735 (multiband) | MNI / FLIRT-aligned; group-ICA 25/100 | none (R-fMRI + emotion task only) | LOW (gated, no naturalistic text) | ukbiobank.ac.uk (application + nominal fee, multi-month timeline) |
| 17 | **ABCD (NDA)** | **NIMH DUC** | ~11 875 youth | task fMRI MID + SST + EN-back | 0.8 | MNI minimally preprocessed | none (paradigmatic tasks) | LOW (no naturalistic text; minors data) | NIMH Data Archive DUC required |
| 18 | **OpenNeuro propofol/anesthesia (ds006623)** | **CC0** | 26 | 4–8 mental-imagery tasks under graded propofol | ~2 | MNI | task labels only | LOW for A' but **HIGH for separate φ★ validation** | OpenNeuro `ds006623` |

(18 rows; user requested ≥15.)

---

## 2. Top 5 recommended datasets per use case

### 2.1 Primary γ-only training (text→BOLD, naturalistic)

1. **Algonauts 2025 / cNeuroMod-Friends+movie10** — already wired, CC0, dense word-level TR alignment, 4 subjects deeply scanned.
2. **cNeuroMod-Friends parent (full release)** — superset of Algonauts 2025 with 6 subjects and additional sessions; same tooling.
3. **Lebel 2023 (ds003020)** — pure-language baseline (no video confound); 8 subjects; full fsaverage.
4. **Narratives (ds002345)** — 345 subjects ⇒ cross-subject power; CC0; phoneme-level alignment.
5. **StudyForrest (ds000113)** — 20-subj 7T audio version is the cleanest pure-listening signal at high SNR.

### 2.2 F4 cross-dataset holdout (generalization gauntlet)

1. **Lebel 2023 ds003020** — orthogonal stimulus type (narrative story vs. sitcom dialog); CC0; same TextGrid timing convention used by Huth-lab encoding models.
2. **Narratives ds002345** — 28 distinct stories ⇒ cross-stimulus richness within one license envelope.
3. **StudyForrest 7T audio** — German + English audiobook; tests language-agnostic vs. English-only encoding (German vocabulary → tokenizer mismatch is a feature, not a bug).
4. **HCP 7T movie watching** — 184 subjects ⇒ best statistical power for cross-subject Pearson ceiling estimation; license blocks public release but allows internal evaluation.
5. **Tang 2023 16-h extension** — within Lebel framework; useful for "depth scaling" — does training on more stimulus per subject monotonically improve F4?

### 2.3 Cross-modal probes (Phase 3+)

1. **NSD (full)** — gold-standard image→BOLD; 8 subj × 30 K images.
2. **BOLD Moments (Lahner 2024 ds005165)** — short video + LLM caption pairs.
3. **Algonauts 2023** — NSD subset with caption annotations, free of NSD DUA only for the challenge subset.
4. **Algonauts 2021** — silent video clips; tests visual-without-language alignment.
5. **StudyForrest AV (3T)** — combines video + speech + emotional context.

### 2.4 Resting-state / FC priors (no text)

1. **HCP 1200 R-fMRI** — fsLR-32k, 4 × 15 min per subject, gold-standard preprocessing.
2. **cNeuroMod resting-state** (within parent release).
3. **UK Biobank R-fMRI** — population scale; gated.
4. **ABCD R-fMRI** — adolescent dev; gated.
5. **OpenNeuro consciousness datasets (ds006623, EEG-fMRI sleep)** — for δ-loop / φ★ validation against pharmacological perturbation.

### 2.5 Consciousness-state validation (φ★ external benchmark)

1. **OpenNeuro propofol mental-imagery (ds006623)** — graded sedation × volitional task; closest fMRI analog to PCI/φ★ measurement.
2. **Simultaneous EEG-fMRI sleep dataset (OpenNeuro)** — 33 subj across REM/NREM; supports level-of-consciousness gradient.
3. **DoC anesthesia + sevoflurane datasets** (cited in Comm Bio 2025 thalamic paper) — pathological unconsciousness benchmark.
4. **LSD/psilocybin fMRI** (e.g., Carhart-Harris OpenNeuro releases) — psychedelic state shifts in functional connectivity.
5. **Casali 2013 PCI** — TMS-EEG (NOT fMRI) but the gold-standard ground-truth label for "is this brain conscious." Cite as theoretical anchor only — Anima cannot run TMS.

---

## 3. Multi-dataset cross-validation strategy

### 3.1 Resampling to common space

The Anima `loss_design.json` references **fsaverage5 (10 242 v/hem = 20 484 total)**. To use multiple datasets:

| Dataset | Native | → fsaverage5 path | Notes |
|---------|--------|-------------------|-------|
| Algonauts 2025 | Schaefer-1000 (volumetric pooled) | parcels do not naturally map to vertices; either keep as 1 000-dim target OR re-project from cNeuroMod surface derivatives (`*.func.gii` at fsaverage6) → `mri_surf2surf --trgsubject fsaverage5` | Easier path: keep two `P_S` heads, one (1 000-dim parcel) and one (20 484 vertex) |
| Lebel 2023 | fsaverage 163 842 v/hem | `mri_surf2surf --srcsubject fsaverage --trgsubject fsaverage5 --hemi {lh,rh}` | Standard Huth-lab pipeline |
| Narratives | fsaverage6 (41 k v/hem) | same `mri_surf2surf` | Preprocs already include fsaverage6 derivatives |
| StudyForrest | T1w / MNI volume | `vol2surf` then downsample | Extra step; well documented |
| HCP 7T | fsLR-32k | `wb_command -metric-resample fs_LR → fsaverage` then to fsaverage5 | Crosses surface conventions; ~5 % info loss |

### 3.2 Cross-substrate consistency design

**Three-tier holdout cascade:**

- **Tier A (within-dataset, within-subject):** Algonauts s06 episode chunk withheld; baseline.
- **Tier B (within-dataset, cross-subject):** Algonauts sub-04 entirely withheld; tests projector subject-invariance.
- **Tier C (cross-dataset):** Train on Algonauts s01-s05 → eval on **Lebel 2023 UTS01 stories** (story domain) AND **Narratives "Pieman" + "Sherlock recall"** (multi-story).

Pass criterion (per spec §4.3): F4_lang ≥ 0.20 silver across **Tier B**, ≥ 0.10 bronze across **Tier C** = strong cross-substrate evidence.

### 3.3 Stimulus orthogonality matrix

Whether two datasets are "independent" for cross-validation purposes:

|             | Algonauts 2025 | Lebel 2023 | Narratives | StudyForrest | HCP 7T mov |
|-------------|:--------------:|:---------:|:----------:|:------------:|:----------:|
| Algonauts 2025 | self | independent | independent | partial overlap (audio only) | independent |
| Lebel 2023 | indep | self | partial (some Moth stories appear in both) | indep | indep |
| Narratives | indep | partial | self | indep | indep |
| StudyForrest | partial | indep | indep | self | indep |
| HCP 7T mov | indep | indep | indep | indep | self |

"Partial overlap" rows (Lebel ↔ Narratives) require explicit story-ID exclusion for honest cross-validation.

---

## 4. License compatibility matrix — public release vs research-only

Anima's downstream goal: be able to publish trained model weights. Dataset license determines whether weights derived from training on that dataset can be redistributed.

| Dataset | License | Train ✓ | Internal eval ✓ | Public weight release? | Caveat |
|---------|---------|---------|------------------|-----------------------|--------|
| Algonauts 2025 (cNeuroMod-derivatives) | CC0 | ✓ | ✓ | ✓ on derivatives; ✗ if model regurgitates Friends transcript verbatim (Warner copyright on underlying script) | Need (a) memorization audit, (b) legal sign-off |
| cNeuroMod-Friends parent | CC0 | ✓ | ✓ | same as Algonauts 2025 | same |
| Lebel 2023 ds003020 | CC0 | ✓ | ✓ | ✓ unrestricted (Moth podcast stories cleared by HuthLab for distribution) | Cleanest license in the set |
| Narratives ds002345 | CC0 | ✓ | ✓ | ✓ | Story authors' rights pre-cleared by Hasson lab |
| Tang 2023 16h | CC0 (within ds003020) | ✓ | ✓ | ✓ | same as Lebel |
| StudyForrest | PDDL (≈ CC0) | ✓ | ✓ | ✓ on neural data; movie audio is copyrighted (we never redistribute) | Functionally equivalent to CC0 |
| Sherlock (dataspace + ds001132) | CC0 derivatives | ✓ | ✓ | ✓ on neural data; BBC clips not redistributed | OK |
| Pereira 2018 | CC-BY 4.0 | ✓ (with attribution) | ✓ | ✓ with attribution clause | Mind the BY clause in model card |
| BOLD Moments ds005165 | CC0 | ✓ | ✓ | ✓ | OK |
| Algonauts 2023 / NSD subset | NSD Data Access Agreement | ✓ (post-signing) | ✓ | **✗** — NSD DUA prohibits redistribution of model trained on NSD without per-use approval | Use only for internal benchmarking |
| NSD (full) | NSD DUA | ✓ | ✓ | ✗ | same |
| HCP 7T movie | HCP Open Access DUA | ✓ | ✓ | ✗ — DUA prohibits redistribution of derived models without HCP approval | Internal-only |
| Algonauts 2021 | research-only license | ✓ | ✓ | ✗ | small dataset; not worth the contamination risk for public release |
| Wehbe 2014 | CMU research | ✓ (after request) | ✓ | ✗ unless authors approve | small sample |
| HCP 1200 R-fMRI | HCP DUA | ✓ | ✓ | ✗ | same as 7T |
| UK Biobank | UKB Material Transfer | ✓ post-application | ✓ | ✗ — UKB requires destruction of derived artifacts after project end | Multi-month gating; not suitable for open Anima release |
| ABCD | NIMH DUC | ✓ post-DUC | ✓ | ✗ | minors data; strict |
| OpenNeuro consciousness (ds006623) | CC0 | ✓ | ✓ | ✓ | OK |

**Public-release-safe union (Anima v1 weight publishability):**
**Algonauts 2025 + cNeuroMod-Friends + Lebel 2023 + Narratives + StudyForrest + Sherlock + Pereira 2018 + BOLD Moments + ds006623.**

Combined CC0/PDDL pool size ≈ **~500 GB raw, ~100 GB parcellated/downsampled to fsaverage5**. Sufficient for Phase 2+ scaling.

---

## 5. Honest C3 (≥5 caveats; raw#91 mandatory)

1. **License heterogeneity does not just affect "public release" — it also affects what mixed-batch training can claim.** A model whose loss is averaged over [CC0 dataset] + [DUA dataset] cannot be cleanly disentangled later: the gradients commingle. **Mitigation:** train on CC0-pool first, then run DUA datasets only for evaluation. Document the boundary in the model card.

2. **Vertex/parcel resolution mismatch is non-trivial.** Schaefer-1000 (Algonauts) is a *parcel* representation (voxel pooling under a hard atlas), while fsaverage / fsLR are *vertex* meshes. Casting one to the other involves either (a) re-projecting raw BOLD via cNeuroMod's surface derivatives, or (b) computing a parcel average from vertex data. Either way, MSE on the lowest-common-denominator surface (fsaverage5, 20 484 v) discards spatial detail that the original 163 842-vertex Lebel data carried. Information-theoretic ceiling on F4 drops accordingly.

3. **Inter-subject Pearson r ceiling ≈ 0.3–0.5 in language ROIs.** Even two humans hearing the same Friends episode show only r ≈ 0.3–0.5 per parcel in language regions; the ceiling is even lower in higher-order cortex. F4_lang ≥ 0.5 ("aspirational" tier in Anima spec) is **physically unattainable** without exceeding inter-human reliability — meaning, encoding human individuality, which violates the "subject-agnostic projector" assumption baked into our P_S spec.

4. **Hemodynamic temporal smearing imposes a hard ceiling on temporal resolution.** TR=1.49 s (Algonauts) or TR=2.0 s (Lebel/Narratives) + canonical HRF (peak +5 s, undershoot +15 s) means sub-second neural integration signatures (50–300 ms ignition, gamma-band binding) are invisible. **Paradigm A' supervises the slow vascular envelope only.** Strong F4 ≠ "matching brain integration" in any IIT/GWT sense. This must be repeated in every public claim.

5. **Stimulus exposure asymmetry.** Subjects watched movies once, with attention, embodiment, prior life context, and audiovisual richness. The CLM consumes only the transcript text. Visual / auditory / emotional / autobiographical context is missing. Expected ceiling on F4 for text-only models is correspondingly lower than for multimodal models (TRIBE v2 itself uses video+audio+text). Reporting F4 without this asymmetry caveat is misleading.

6. **Tokenization mismatch (especially for German StudyForrest).** Llama-3 BPE tokenization is English-biased; transcripts in Algonauts are word-level English; StudyForrest is German; Narratives includes ESL accent variation. A long word may span TRs; a TR may contain many BPE tokens. The TR-binning step (mean-over-tokens) is lossy and biases toward content words.

7. **Projector P_S identifiability risk.** MSE flows through P_S; if P_S is high-rank, it can absorb arbitrary CLM-state shape and still match BOLD without the CLM learning anything brain-like. Cross-dataset evaluation partially mitigates this (a P_S that overfits one dataset's noise won't transfer), but P_S must be kept **low-rank ≤ 256** AND regularized OR Anima must report per-dataset P_S norms to detect identifiability collapse.

8. **NSD / HCP / UKB / ABCD have stricter use terms than the CC0 pool — and accidental contamination is hard to undo.** Once a checkpoint has seen NSD-trained gradients, that checkpoint inherits NSD DUA constraints. **Mitigation:** keep DUA-trained variants in a separate `state/anima_dua_internal/` checkpoint family that is never published.

9. **Story stimuli overlap.** Lebel 2023 and Narratives both draw from The Moth podcast. Several stories appear in both. Naive cross-dataset evaluation that doesn't exclude overlapping stories overstates generalization. Need explicit story-ID exclusion list before any cross-dataset F4 number is reported.

10. **Algonauts 2023 / NSD use beta values, not BOLD time series.** The "BOLD" target in Algonauts 2023 is a single FIR-derived beta per image, NOT a TR time series. MSE against beta is fundamentally different from MSE against time series; it cannot be combined with Algonauts 2025 (TR-resolved) under one loss term without explicit re-formulation. Treat as a separate evaluation modality.

---

## 6. Pointers / next steps (no execution)

- **Confirmed primary plan unchanged:** Algonauts 2025 sub-01 mini-run (per runbook §1) remains the right starting point. Pre-flight is DONE.
- **Suggested Phase 2 expansion order:**
  1. Add Algonauts 2025 sub-02 → sub-04 (no extra clearance needed; same DataLad sibling).
  2. Add Lebel 2023 ds003020 UTS01-3 (~16 h podcast extension); pre-clone size check; project from full fsaverage → Schaefer-1000 OR keep dual-head P_S.
  3. Add Narratives ds002345 subset (3-4 stories with cleanest preprocessing per Nastase 2021 README); cross-dataset F4 first checkpoint.
  4. (Optional) StudyForrest 3T audio for German cross-lingual probe.
- **Skip for Phase 2:** NSD / HCP / UKB / ABCD (license blocks public release; not worth the contamination cost yet). Revisit if Anima develops a "research-only" checkpoint family.
- **Author state config:** `state/p9_paradigm_a_prime_dataset_landscape_2026_05_03/{table.json, license_matrix.json, holdout_strategy.json}` (config only, no .py per raw#9).
- **Coordinate with P_S projector spec author:** confirm dual-head (1 000-parcel + 20 484-vertex) support before Phase 2 expansion.

---

## 7. Sources

### Algonauts series
- [Algonauts Project 2025 — Challenge page](https://algonautsproject.com/challenge)
- [courtois-neuromod/algonauts_2025.competitors GitHub](https://github.com/courtois-neuromod/algonauts_2025.competitors)
- [The Algonauts Project 2025 Challenge: How the Human Brain Makes Sense of Multimodal Movies (arXiv 2501.00504)](https://arxiv.org/abs/2501.00504)
- [Algonauts 2023 — Challenge page (CSAIL)](http://algonauts.csail.mit.edu/challenge.html)
- [Algonauts 2023 — Brain Data spec](http://algonauts.csail.mit.edu/braindata.html)
- [Algonauts 2021 — Challenge page](http://algonauts.csail.mit.edu/2021/challenge.html)

### cNeuroMod
- [Courtois NeuroMod Datasets](https://docs.cneuromod.ca/en/latest/DATASETS.html)
- [cNeuroMod data access](https://docs.cneuromod.ca/en/latest/ACCESS.html)
- [CNeuroMod Data Collection Complete: 200h of individual fMRI (CCN 2025)](https://2025.ccneuro.org/abstract_pdf/Boyle_2025_CNeuroMod_Data_Collection_Complete_200h_individual.pdf)

### Lebel 2023 / Tang 2023 / HuthLab
- [Lebel et al. 2023 — A natural language fMRI dataset for voxelwise encoding models (Sci Data)](https://www.nature.com/articles/s41597-023-02437-z)
- [ds003020 on OpenNeuro](https://openneuro.org/datasets/ds003020/versions/2.0.0)
- [HuthLab/deep-fMRI-dataset GitHub](https://github.com/HuthLab/deep-fMRI-dataset)
- [Tang et al. 2023 — Semantic reconstruction of continuous language from non-invasive brain recordings (Nat Neurosci)](https://www.nature.com/articles/s41593-023-01304-9)

### Narratives
- [Nastase et al. 2021 — The "Narratives" fMRI dataset (Sci Data)](https://www.nature.com/articles/s41597-021-01033-3)
- [ds002345 on OpenNeuro](https://openneuro.org/datasets/ds002345)
- [snastase/narratives GitHub](https://github.com/snastase/narratives)

### StudyForrest
- [studyforrest.org overview](https://studyforrest.org/)
- [studyforrest.org — Data Access (PDDL)](https://www.studyforrest.org/access.html)
- [Hanke et al. 2014 — A high-resolution 7T fMRI dataset from complex natural stimulation (Sci Data)](https://www.nature.com/articles/sdata20143)

### Sherlock / Hasson lab
- [Sherlock Movie Watching Dataset — Princeton DataSpace](https://dataspace.princeton.edu/handle/88435/dsp01nz8062179)
- [Sherlock_Merlin on OpenNeuro (ds001110)](https://openneuro.org/datasets/ds001110/versions/00003)
- [Sherlock on OpenNeuro (ds001132)](https://openneuro.org/datasets/ds001132/versions/00003)
- [Chen et al. 2017 — Mapping fMRI responses to natural language annotations (NeuroImage)](https://www.sciencedirect.com/science/article/pii/S1053811917305128)

### Pereira 2018
- [Pereira et al. 2018 — Toward a universal decoder of linguistic meaning (Nat Commun)](https://www.nature.com/articles/s41467-018-03068-4)

### Wehbe 2014
- [CMU PLOS ONE Story Reading dataset (Wehbe et al. 2014)](http://www.cs.cmu.edu/~fmri/plosone/)
- [Wehbe et al. 2014 — Simultaneously Uncovering Patterns of Brain Regions Involved in Different Story Reading Subprocesses (PLOS ONE)](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0112575)

### NSD / Algonauts visual
- [NSD — Allen et al. 2021 (Nat Neurosci)](https://www.nature.com/articles/s41593-021-00962-x)
- [naturalscenesdataset.org](https://naturalscenesdataset.org/)
- [NSD on AWS Open Data Registry](https://registry.opendata.aws/nsd/)

### BOLD Moments
- [Lahner et al. 2024 — BOLD Moments (Nat Commun)](https://www.nature.com/articles/s41467-024-50310-3)
- [ds005165 on OpenNeuro / BOLDMomentsDataset GitHub](https://github.com/blahner/BOLDMomentsDataset)

### HCP / UK Biobank / ABCD
- [HCP S1200 Reference Manual (PDF)](https://www.humanconnectome.org/storage/app/media/documentation/s1200/HCP_S1200_Release_Reference_Manual.pdf)
- [HCP 7T movie subset DataLad](https://github.com/datalad-datasets/hcp_movies)
- [UK Biobank brain imaging (FMRIB)](https://www.fmrib.ox.ac.uk/ukbiobank/)
- [Miller et al. 2016 — UK Biobank brain imaging (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC5086094/)
- [ABCD on NIMH Data Archive](https://nda.nih.gov/abcd)
- [ABCD Study Data Sharing](https://abcdstudy.org/scientists/data-sharing/)

### Consciousness datasets
- [Open fMRI resource for consciousness under anesthesia (ds006623, Sci Data 2025)](https://www.nature.com/articles/s41597-025-06442-2)
- [OpenNeuro index](https://openneuro.org/)

---

*End of research doc. No code, no execution, no download. Doc-only per raw#9.*
