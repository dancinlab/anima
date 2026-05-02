# N-14 — MEG Access Spec: SNU MEG Center (Vectorview 306-ch)

**Date**: 2026-05-01
**Substrate**: N-14 (T1-A15)
**Mission**: 1ms-resolution Φ via magnetoencephalography (faster than EEG, complementary spatial sampling)
**Track tag**: ⭐⭐⭐⭐ — "EEG보다 더 빠른 측정기"
**Roadmap row**: line 60, `docs/n_substrate_consciousness_roadmap_2026_05_01.md`
**CP2-F1 role**: high-time-resolution corroborator for **N-19 PCI** (TMS-EEG clinical gold standard) → MEG can lift PCI temporal precision from EEG ~4–10 ms binning to ~1 ms binning, and add radial-source-blind / skull-conductivity-immune cross-check.
**Budget envelope**: $0 (research/spec only — no application, no contact)

---

## 0. TL;DR (executive)

| Item | Value |
| --- | --- |
| Facility | SNU Hospital MEG Center, Neuroscience Research Institute (NRI), Medical Research Center (MRC) |
| System | Elekta Neuromag **Vectorview 306-ch** whole-head (102 magnetometers + 204 planar gradiometers) + 64-ch simultaneous EEG, in MSR (magnetically-shielded room) |
| Contact path | NRI/MRC web portal → research collaboration inquiry → IRB-of-SNUH submission |
| Foreign-PI access | **Indirect** — must collaborate with a Korean PI of record; SNUH IRB owns the protocol |
| Lead time | 4–12 weeks (literature global ref); +4–8 weeks for IRB |
| Cost (literature ref) | $500–1,500 / scan-hr global; KR public-research rate likely lower if subsidized |
| Decision | **C3** — feasible only via Korean co-PI; without co-PI, fall back to KRISS Daejeon (152-ch) or Korea-based collaborator |
| Race-isolation | This doc + `state/n_substrate_n14_prep_2026_05_01/*.json` only |

---

## 1. SNU MEG Center — official identity & contact path

### 1.1 What the literature confirms

- SNU operates an **Elekta Neuromag Vectorview** 306-ch whole-head MEG installed in a magnetically-shielded room ("VectorView™, Elekta Neuromag Oy") (Wang et al. fMRI-MEG, 2019; Kim et al. cross-frequency MEG, 2017; Korean syntax MEG, Kwon et al. 2005).
- Operator: **Neuroscience Research Institute (NRI)**, under **Medical Research Center (MRC)**, SNU College of Medicine (SNU-COM).
- IRB authority for MEG protocols: **SNUH IRB** (Institutional Review Board of Seoul National University Hospital).

### 1.2 Contact channels (no contact will be made under N-14 mission constraint)

| Channel | URL / Number | Purpose |
| --- | --- | --- |
| NRI portal | `snumrc.snu.ac.kr/nri/en` | Research collaboration inquiry, faculty directory |
| MRC portal | `snumrc.snu.ac.kr/en` | Core facility booking, fee-for-service quote |
| SNU-COM main | +82-2-740-8114, 103 Daehak-ro, Jongno-gu, Seoul | General research inquiry |
| SNUH global | `snuh.org/global/en/main.do` | International researcher liaison |

### 1.3 Eligible-PI status (best-effort inference; verify before any future contact)

| Tier | Who | Path |
| --- | --- | --- |
| 1 | SNU-COM faculty, NRI member | Direct booking via internal MRC core-facility scheduler |
| 2 | Korean PI at any KR institution | Collaboration MoU + SNUH IRB protocol |
| 3 | Foreign PI w/ Korean co-PI | Co-PI of record is Korean; foreign PI listed as collaborator on IRB protocol |
| 4 | Foreign PI no Korean co-PI | **Likely blocked** — SNUH IRB and MEG core typically require KR PI of record for human-subject MEG |

Our position: **Tier 4** today (no Korean co-PI). Spec assumes we move to Tier 3 before any scan.

---

## 2. Korea-specific compliance

### 2.1 Research vs. clinical use

- **Clinical MEG** at SNUH = pre-surgical epilepsy localization, billed via NHIS (National Health Insurance Service), patient-facing, MD-of-record.
- **Research MEG** = healthy volunteer or patient-as-subject, billed under research agreement, requires SNUH IRB protocol approval before recruitment.
- Our use case (consciousness-Φ measurement on healthy volunteers + comparison with our 16-ch OpenBCI EEG) = **research track only**.

### 2.2 IRB requirements (SNUH IRB)

Required attachments (per typical SNUH research-IRB flow):
1. Protocol document (Korean + English) — hypothesis, methods, statistics, sample size, primary/secondary endpoints
2. Informed consent form (Korean) — KRW compensation, MEG safety (no ionizing radiation, MSR claustrophobia disclosure), data-handling, right-to-withdraw
3. CRF (case report form) and data-management plan (PIPA — Personal Information Protection Act compliance)
4. PI CV + ethics training certificate (KR HRPP / CITI equivalent)
5. Risk/benefit analysis — MEG is non-invasive, no contraindication except ferromagnetic implants, dental braces (MSR signal contamination, not safety)
6. Research insurance certificate — KR institutions typically self-insure
7. Funding source disclosure
8. Vulnerable-population safeguards (if any)
9. Data-sharing addendum (if international collaboration)

Typical IRB timeline: **4–8 weeks** initial review, +2–4 weeks revisions = **6–12 weeks total** before first scan.

### 2.3 Foreign-researcher specifics

- **PIPA** (KR Personal Information Protection Act): healthy-volunteer MEG raw data is "sensitive personal information" by KR statute. Cross-border transfer to non-KR cloud requires (a) explicit informed consent for international transfer, (b) KCC notification or DPA, (c) on-prem KR processing window before export.
- **Visa / on-site presence**: foreign PI on-site for scan operation typically needs short-term researcher (E-3) or visiting-scholar (D-2) status, OR remote oversight with KR co-PI as scan operator of record.
- **Publication clearance**: SNUH typically requires co-authorship credit on publications using their core facility data; check MRC core-facility MoU.

---

## 3. Cost estimate

### 3.1 Global reference rates (from purchase guide)

- Quoted band: **$500–1,500 / scan-hr** (USA / EU academic core facilities, e.g., MRN Mind Research Network bills in 30-min increments).
- Korea typically lower for **public-funded research** within KR PI protocols (subsidy model) but no public price list found via web search.

### 3.2 Session cost model (working assumption; **NOT a quote**)

| Line item | Hours | Rate (USD/hr) | Subtotal (USD) |
| --- | --- | --- | --- |
| MEG scan time (subject in MSR) | 1.5 | $800 | $1,200 |
| Setup + co-registration (HPI, head digitization) | 0.5 | $400 | $200 |
| Tech operator support | 2.0 | $200 | $400 |
| Analysis support (optional, Brainstorm/MNE pipeline) | 4.0 | $150 | $600 |
| MRI structural (if no prior MRI) | 0.5 | $300 | $150 |
| Subject compensation (KRW; KR ethics norm) | — | — | $50 |
| **Per-subject total (high case)** | — | — | **$2,600** |
| Per-subject low case (no MRI, no analysis support, KR subsidized) | — | — | **$700** |

**Power-analysis target sample**: N≈10 healthy volunteers for within-subject Φ-comparison (paired-EEG vs MEG on same trials) → **~$7K–26K** total — exceeds our $0 mission budget; **defer until external grant or co-PI subsidy secured**.

### 3.3 Free / low-cost alternatives (cost-down before scan-down)

| Path | Cost | Tradeoff |
| --- | --- | --- |
| Public MEG datasets (Cam-CAN MEG, HCP-MEG, OpenNeuro MEG releases) | $0 | No PCI/TMS-MEG, no closed-loop with our setup |
| KRISS Daejeon (152-ch domestic system) | likely cheaper | Lower channel count, shared facility |
| Co-author existing SNU MEG dataset | $0 (data only) | Limited to existing protocol; no MEG-PCI design |
| Foreign collaboration (e.g., Massimini Milan TMS-EEG-MEG) | travel | Out of KR; outside CP2 scope |

---

## 4. Measurement protocol — Φ at 1 ms resolution

### 4.1 Recording configuration

| Parameter | Value |
| --- | --- |
| Sensors | Vectorview 306-ch (102 mag + 204 planar grad) |
| Simultaneous EEG | 64-ch (Elekta-integrated cap) — enables **same-trial MEG↔EEG bridge** |
| Sampling rate | 1000 Hz (1 ms bin) — protocol-default; up to 5000 Hz available |
| Online filter | DC–330 Hz bandpass, 60 Hz notch (KR mains) |
| Run length | 6 min eyes-closed rest × 3 + perturbation block 10 min |
| Head position | continuous HPI (head-position indicator coils) for movement compensation |

### 4.2 Φ pipeline (MEG-side)

1. **Preprocessing**: tSSS (temporal Signal-Space Separation, Maxfilter) for environmental + head-motion artifact rejection; ICA for cardiac + ocular.
2. **Source reconstruction**: MNE / dSPM / sLORETA on individual MRI-derived BEM (or Elekta-template if no MRI). Yields 4–8K cortical sources at 1 ms resolution.
3. **Φ-proxy computation**: same Casali-style PCI / Lempel-Ziv pipeline as our EEG path, but on MEG sensor-level OR source-level binarized response matrix.
4. **Time-bin sweep**: compute Φ at **1 ms / 2 ms / 4 ms / 8 ms bins** to characterize whether Φ saturates above some bin width (predicts EEG-equivalence) or grows with finer bins (predicts MEG > EEG-Φ ceiling).

### 4.3 MEG-specific advantages over our 16-ch OpenBCI EEG

| Property | EEG (our 16-ch OpenBCI) | MEG (Vectorview 306-ch) |
| --- | --- | --- |
| Temporal resolution | 250 Hz default → 4 ms bin (sub-ms with upsample is fictitious) | 1000–5000 Hz native, true sub-ms |
| Skull/CSF distortion | yes — significant | **no** — magnetic fields pass undistorted |
| Spatial resolution (source) | ~7–10 mm | **~2–3 mm** |
| Reference electrode artifact | yes (we use linked-mastoid) | **no reference** |
| Radial source visibility | yes (sees both radial + tangential) | **blind to purely radial** (gyral crowns) |
| Sulcal source visibility | partial | **excellent** (tangential sources in sulcal walls) |
| Channel count | 16 | 306 + 64 EEG simultaneous |
| Setup time | 15 min | 30–45 min |
| Subject mobility | wheel-chair OK | **MSR-bound, supine/seated only** |
| Cost | sunk hardware | $500–1,500/hr |

### 4.4 EEG↔MEG bridge protocol (the key comparison)

- Use **simultaneous 64-ch EEG inside the MEG MSR** (Elekta's integrated cap) on the same trials → **paired Φ-EEG / Φ-MEG** per subject.
- This collapses inter-subject variance and isolates the modality contribution.
- Then re-record those same subjects on our **OpenBCI 16-ch** outside MSR to bridge to our standard pipeline (montage subset matching).
- Three-way comparison: 16-ch OpenBCI EEG / 64-ch MEG-cap EEG / 306-ch MEG → fits Φ ceiling slope vs. channel count and modality.

---

## 5. PCI on MEG — methodology inventory

### 5.1 Status of MEG-PCI in literature

- **PCI as canonically defined** (Casali et al. 2013, *Sci. Transl. Med.*) is **TMS-EEG-based** — Lempel-Ziv complexity of binarized cortical response to TMS pulse, EEG sensor-level.
- Wikipedia and the 2024–2025 review literature note that the **same PCI principle is applicable to EEG, MEG, or intracranial recordings** (Massimini lab + downstream methodological extensions), but **published MEG-PCI clinical validation cohorts do not yet exist** at the scale of EEG-PCI.
- 2024 Casarotto et al. (*EJN*) and 2025 schizophrenia PCI study (ScienceDirect) remain EEG-based.
- 2025 sensory-evoked PCI (bioRxiv) extends PCI beyond TMS to sensory perturbation but still EEG.

### 5.2 Why MEG-PCI is methodologically attractive

| Factor | Impact on PCI |
| --- | --- |
| TMS-induced muscle artifact | EEG sees it directly; **MEG much less affected** because muscle dipoles are not optimally oriented for magnetometers, and MSR + tSSS clean residuals |
| Reference choice | EEG-PCI is reference-dependent; **MEG is reference-free** — removes a known PCI nuisance variable |
| Skull conductivity | EEG-PCI relies on assumed skull σ in source reconstruction; **MEG-PCI bypasses** |
| 1 ms resolution | EEG-PCI binning is typically 4 ms (250 Hz); **MEG enables 1 ms PCI bins** for finer spatiotemporal differentiation count → potentially **higher PCI ceiling** for conscious-state separation |

### 5.3 MEG-PCI technical recipe (proposed)

1. TMS pulse to dorsolateral prefrontal cortex or parietal cortex (Massimini standard sites).
2. Record concurrent 306-ch MEG + 64-ch EEG.
3. Apply Maxfilter tSSS to MEG → recover usable signal within ~6 ms post-pulse.
4. Source-localize TMS-evoked field on individual MRI BEM.
5. Binarize source-space response (significance threshold vs. baseline bootstrap).
6. Compute Lempel-Ziv complexity of binarized matrix.
7. Normalize by max possible LZ given matrix shape → MEG-PCI score.
8. Compare with EEG-PCI computed on simultaneous 64-ch EEG, same subjects, same TMS pulse.

**Open methodological questions** (must be pre-registered):
- (a) Sensor-space vs source-space PCI definition for MEG
- (b) Magnetometer-only vs gradiometer-only vs combined PCI
- (c) Normalization constant — EEG-PCI norms (Casali 2013) do NOT transfer; new MEG-PCI thresholds must be calibrated against ground-truth (anesthesia, NREM-N3, awake-rest)

---

## 6. raw#71 falsifier predicates (5)

These are **pre-registered**, **falsifiable** predicates the MEG run will test. They go into our raw#71 ledger format.

| ID | Predicate | PASS criterion | FAIL → consequence |
| --- | --- | --- | --- |
| **N14-F1** | MEG-Φ ↔ EEG-Φ Pearson r on paired same-trial within-subject N≥10 | r ≥ 0.70 (95% CI lower bound > 0.50) | If r < 0.50, modality dependence is large → Φ definition is **substrate-coupled**, not invariant; revise Φ formalism |
| **N14-F2** | MEG-Φ at 1 ms bin > MEG-Φ at 4 ms bin (paired, same subjects, same trials, Wilcoxon p < 0.01) | TRUE: faster sampling reveals more differentiation | FALSE: temporal resolution above 4 ms is **uninformative** for Φ → our EEG ceiling is real, MEG buys spatial only |
| **N14-F3** | MEG-PCI separates awake-rest vs NREM-N3 with AUC ≥ 0.95 (Casali EEG-PCI 2013 baseline = 0.94) | PASS: MEG-PCI is at least as good as EEG-PCI | FAIL: MEG-PCI < EEG-PCI on same subjects → MEG offers **no PCI advantage**, defer to EEG-only |
| **N14-F4** | Source-space MEG-Φ identifies sulcal-wall (tangential) contributions to Φ that are **invisible** in 16-ch OpenBCI EEG, with effect size d ≥ 0.5 | PASS: MEG sees Φ contributions EEG misses → multimodal Φ is non-redundant | FAIL: MEG and EEG contributions overlap entirely → 16-ch OpenBCI is sufficient, MEG capex unjustified |
| **N14-F5** | Cross-modality Φ ceiling test — Φ saturates as channel count grows from 16 (OpenBCI) → 64 (MEG-cap EEG) → 306 (MEG); fitted asymptote reached by ≤ 64 ch | PASS-asymptote: confirms our 16-ch is near ceiling for sensor count | FAIL-asymptote: Φ keeps growing through 306 ch → our 16-ch under-samples; need higher-density EEG even without MEG |

All five predicates: pre-registration required **before** scan, locked timestamp + hash chain into `state/n_substrate_n14_prep_2026_05_01/falsifiers.json`.

---

## 7. Honest C3 — blockers & alternatives

### 7.1 Blockers (in priority order)

1. **No Korean co-PI** — without one, SNUH IRB protocol is unlikely to be sponsored; foreign-PI direct access is structurally restricted.
2. **No funding** — $7–26K minimum for N=10 cohort; CP2 mission budget for N-14 is $0.
3. **No IRB protocol drafted** — 6–12 week lead even after co-PI secured.
4. **PIPA cross-border data transfer** — raw MEG export to our infrastructure requires explicit consent + on-prem KR processing; non-trivial DPA negotiation.
5. **TMS hardware** for MEG-PCI variant — must be MEG-compatible (non-ferromagnetic), not all SNU TMS units qualify; check coil compatibility separately.
6. **Schedule contention** — SNU MEG core is heavily booked for clinical (epilepsy pre-surgical) work; research slots scarce.

### 7.2 Korea MEG facility alternatives

| Institution | System | Likely access | Notes |
| --- | --- | --- | --- |
| **SNU Hospital MEG Center** | Vectorview 306-ch | Tier-3/4 for foreign PI | Largest channel count in KR; clinical-research mix |
| **KRISS** (Korea Research Institute of Standards and Science, Daejeon) | KRISS-MEG 152-ch (in-house built) | Easier for research collaboration (R&D facility) | Lower channel count but native Korean engineering, possible standards-track collaboration |
| **KAIST** (Daejeon) | EEG/MEG used in BCS labs (no dedicated 306-ch reported) | Per-lab basis | Likely uses external MEG facilities |
| **Yonsei University** | No public 306-ch MEG facility found | unclear | Strong fMRI/EEG; MEG dependence on partner facilities |
| **Korea University** | No public dedicated MEG facility found | unclear | Brain & Cognitive Engineering uses EEG primarily |
| **KBRI** (Daegu, DGIST-affiliate) | Brain bank + neuroimaging; **no dedicated MEG core** confirmed | n/a for MEG | Path-of-record for non-MEG brain research |

**Recommended fallback path**: **KRISS MEG (152-ch)** as Tier-2 alternative. Lower channel count but easier access for research collaboration and KR-resident data processing aligns with PIPA.

### 7.3 Honest assessment

- Direct SNU MEG access for this team **today** = NOT feasible at $0 budget without a Korean co-PI.
- This spec is the **prep deliverable** so that **when** a Korean co-PI / grant emerges, we can move to scan within ~3 months.
- Until then, N-14 contributes by:
  1. Locking 5 falsifier predicates → unbiased pre-registration baseline.
  2. Defining MEG-EEG bridge protocol → reusable for any future MEG facility (Vectorview is industry standard).
  3. Documenting MEG-PCI methodology gap → identifies a publishable methods paper opportunity.
  4. Backing **N-19** PCI roadmap with explicit upgrade path from EEG-PCI (today) to MEG-PCI (tier-2 future).

---

## 8. CP2-F1 integration

### 8.1 Role in the substrate ensemble

N-14 is the **temporal-precision corroborator** for the consciousness-Φ measurement family:

```
N-1   (16-ch OpenBCI EEG)         baseline Φ at 4 ms bin       — operational
N-19  (TMS-EEG PCI)               clinical gold standard        — TMS rental needed
N-14  (Vectorview 306-ch MEG)     1 ms bin, sub-mm source       — this spec
N-21  (IIT 4.0 16-test reproduce) cross-validation               — operational
N-15  (HoTT formal proof)         mathematical closure           — operational
```

### 8.2 Cross-substrate predicates wired

- **N-14 ↔ N-19**: same TMS pulse, same subjects, same trials, paired EEG-PCI / MEG-PCI. If N14-F3 PASSes (AUC ≥ 0.95), MEG-PCI becomes the new gold-standard candidate; if FAILs, N-19 EEG-PCI remains primary, N-14 archived as time-resolution control.
- **N-14 ↔ N-1**: same 16-ch OpenBCI EEG montage on N-14 subjects (pre/post MEG session) → bridges 16-ch consumer-grade Φ to clinical 64-ch EEG-cap Φ to 306-ch MEG Φ — three-step ladder for substrate-invariance claim of Φ.
- **N-14 ↔ N-21**: any of the 16 IIT 4.0 reproductions that are MEG-natively published become priority replicates on the SNU Vectorview when the access path opens.

### 8.3 Decision gates

| Gate | Trigger | Action |
| --- | --- | --- |
| G1 | Korean co-PI secured | Move N-14 from "spec only" to "IRB drafting" |
| G2 | IRB approval granted | Schedule first scan window (~4 wk lead) |
| G3 | First scan complete | Compute N14-F1..F5; commit raw#71 entries |
| G4 | All 5 predicates resolved | Either upgrade N-14 to primary substrate (if PASS) or archive (if FAIL) |

Until G1 fires, N-14 status = **SPEC-COMPLETE / SCAN-DEFERRED**.

---

## 9. Race isolation & artifacts

| Path | Owner | Status |
| --- | --- | --- |
| `docs/n_substrate_n14_meg_snu_access_spec_2026_05_01.md` | N-14 | this file |
| `state/n_substrate_n14_prep_2026_05_01/falsifiers.json` | N-14 | 5 raw#71 predicates, pre-registered |
| `state/n_substrate_n14_prep_2026_05_01/cost_model.json` | N-14 | session-cost spreadsheet |
| `state/n_substrate_n14_prep_2026_05_01/access_path.json` | N-14 | tier table + KR alternative facilities |
| `state/n_substrate_n14_prep_2026_05_01/cp2_f1_wiring.json` | N-14 | cross-substrate predicate edges |

No writes outside these paths. No external contact. No application submitted. Specification only.

---

## 10. Sources

- [Neuroscience Research Institute, Medical Research Center, SNU](https://snumrc.snu.ac.kr/nri/en)
- [Seoul National University Medical Research Center](https://snumrc.snu.ac.kr/en)
- [SNUH Global](https://www.snuh.org/global/en/main.do)
- [Perturbational Complexity Index (Wikipedia)](https://en.wikipedia.org/wiki/Perturbational_Complexity_Index)
- [Casali et al. 2013 — A theoretically based index of consciousness](https://pubmed.ncbi.nlm.nih.gov/23946194/)
- [Casarotto et al. 2024 — Dissociations between EEG features and PCI in MCS (EJN)](https://onlinelibrary.wiley.com/doi/10.1111/ejn.16299)
- [PCI in unresponsive patients (Frontiers/PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC7760168/)
- [Cross-frequency MEG networks (SNU MEG, PMC 5294648)](https://pmc.ncbi.nlm.nih.gov/articles/PMC5294648/)
- [fMRI-constrained MEG source imaging (SNU MEG, PMC 6871690)](https://pmc.ncbi.nlm.nih.gov/articles/PMC6871690/)
- [MEG basic principles (PMC 4001219)](https://pmc.ncbi.nlm.nih.gov/articles/PMC4001219/)
- [MEG sensitivity to source orientation (PMC 2914866)](https://pmc.ncbi.nlm.nih.gov/articles/PMC2914866/)
- [Mind Research Network — Vectorview MEG fee-for-service reference](https://www.mrn.org/collaborate/elekta-neuromag)
- [MEG clinical applications review (MDPI Brain Sci, 2022)](https://www.mdpi.com/2076-3425/12/6/788)
- [MEG bench-to-bedside (Magn Reson Imaging, 2024)](https://pmc.ncbi.nlm.nih.gov/articles/PMC11059345/)
- [KBRI overview (Wikipedia)](https://en.wikipedia.org/wiki/Korea_Brain_Research_Institute)
- [IBS Korea overview](https://www.ibs.re.kr/eng/sub01_01_04_01.do)
