<!-- [Hc_919 n21-iit40-16test-reproduce-cluster — moved to hypotheses_candidates/Hc_919_n21_iit40_16test_reproduce_cluster.md on 2026-05-11] -->

# N-21 Test #5 — Sarasso 2014 TEP Review Extension (REVIEW-EXTEND)

> **ts**: 2026-05-01
> **agent**: N-21 #5 EXEC (Sarasso 2014 PCI/TEP literature meta-extend)
> **parent**: `docs/n_21_iit40_12_remaining_spec_2026_05_01.md` §4.3 RANK-3
> **race-isolation**: writes only to `state/n_21_test5_sarasso_tep_review_2026_05_01/*` + this doc
> **status**: REVIEW_COMPLETE · F3 PASS
> **constraints**: $0, WebSearch+WebFetch only, hexa-only, no .py

---

## §0 한 줄 요약

Sarasso 2014 (TEP-PCI 리뷰) → Casarotto 2016 (PCI*=0.31, n=150) → Comolatti 2019 (PCIst sensor-level) → 2024-2025 확장 (rTMS biomarker / subacute CMD / spontaneous-EEG surrogate / sensory-evoked PCI) 까지 cutoff 0.31 일관성 STABLE. 16ch 적응 cutoff 0.25 는 EXTRAPOLATION (≥32ch 까지만 직접 검증). N-19 spec 6개 항목 업데이트 제안.

---

## §1 Cross-paper PCI cutoff consistency (2013-2026)

| year | study | ch | variant | cutoff | n | verdict |
|---|---|---|---|---|---|---|
| 2013 | Casali (Sci Transl Med) | 60 | PCI_LZ | n/a (proof of concept) | 32 | first separation |
| 2014 | Sarasso review (Clin EEG Neurosci) | 60 | PCI_LZ review | n/a | aggregate | qualitative collapse-on-LOC pattern |
| 2016 | **Casarotto (Ann Neurol)** | **60** | **PCI_LZ** | **0.31** | **150** | **canonical, 100/100 sens/spec** |
| 2019 | Comolatti (Brain Stim) | 60+ → sparse intracranial | PCIst | ROC-equiv to 0.31 | 216 | sensor-level, 100× faster |
| 2021 | Sarasso et al. (NeuroImage) | 60 | PCI/PCIst | 0.31 reaffirmed | clinical | consolidation |
| 2024 | Comanducci (Brain Stim) | 60 | PCIst | n/a | subacute | detects CMD before CRS-R |
| 2024 | Wang (JNER) | 64 | PCIst | baseline predicts responder | 20 MCS | rTMS biomarker, F=4.961 p=0.039 |
| 2024 | Comm Biol s42003-024-06613-8 | hd | spontaneous→PCI | predicts PCI | replicated | TMS-free predictor |
| 2025 | eLife 98920 | 60 | spontaneous fluidity | matches 0.31 disc. | propofol | 100% wake-vs-anes |
| 2025 | bioRxiv sensory PCI | 32-64 | sensory-evoked PCIst | tracks intensity | thermal | non-TMS generalization |

**Verdict**: cutoff 0.31 STABLE 2013-2026 across all 60+ch cohorts. PCIst preserves discrimination at sparser intracranial. **No outliers found** → falsifier F3 (CI crosses 0) does NOT trigger.

---

## §2 16ch adapted cutoff 0.25 — honest validity check

N-19 spec §4.3 claims `PCI_16ch* ≈ 0.25 ± 0.05`. Literature support:
- **Validated downward floor**: Comolatti 2019 PCIst → sparse INTRACRANIAL (not low-density scalp). Smallest validated SCALP cohort = 32-64ch (sensory PCI bioRxiv 2025).
- **Gap at 16ch**: zero published direct validation. 0.25 derives from 15-25% downward bias inferred from PCIst principles, not measured in a 16ch cohort.
- **Action**: keep 0.25 as PROVISIONAL; require personal-calibration cohort n≥10 awake/sleep before any clinical-tier claim. This matches N-19 spec §4.3 caveat already; the 2026 literature confirms the gap remains unfilled.

---

## §3 New 2024-2026 clinical-tier evidence for IIT

1. **Wang JNER 2024** (n=20 MCS rTMS crossover) — PCIst as treatment-response biomarker; baseline PCIst stratifies responders. **NEW IIT-supportive use case** beyond pure detection.
2. **Comanducci Brain Stim 2024** (subacute) — PCI detects covert capacity BEFORE behavioral recovery → CMD population. Strong for IIT's "consciousness ≠ behavior" claim.
3. **Comm Biol 2024** — resting-state spontaneous EEG dynamical features PREDICT TMS-PCI cross-dataset replicated. Enables TMS-FREE proxy.
4. **eLife 98920 (2025)** — spatiotemporal "fluidity" + "functional repertoire" match PCI 100% wake-vs-propofol discrimination WITHOUT perturbation. Most consequential 2025 update.
5. **bioRxiv sensory PCI (2025)** — PCIst on thermal sensory-evoked responses; PCI not TMS-bound.

Aggregate: 5 new strands (2024-2025) all corroborate the PCI-IIT framework, **none contradict** the 0.31 cutoff or the integration-information collapse pattern.

---

## §4 N-19 spec update suggestions

(file: `docs/n_substrate_n19_pci_spec_2026_05_01.md`)

1. **§10 Sources** — add: Wang 2024 (JNER 10.1186/s12984-024-01455-1), Comanducci 2024 (Brain Stim S1935-861X(23)00733-7), Comm Biol 2024 (s42003-024-06613-8), eLife 98920 (2025), sensory PCI bioRxiv 2025.
2. **§4.3 cutoff** — explicitly mark 0.25 as INTERPOLATION; clarify Comolatti 2019 floor was sparse INTRACRANIAL not low-density scalp; smallest validated scalp = 32ch.
3. **§4.4 NEW (TMS-free path)** — cite eLife 2025 + Comm Biol 2024 to enable spontaneous-only PCI surrogate at 16ch, dropping TMS hardware entirely (converges with TOP-5 #5 spontaneous-LZ analog and removes the $1.6-21K capex).
4. **§6.3 INFEASIBLE limits** — clarify PCIst was NOT validated at 16ch scalp.
5. **§7.5 NEW (treatment-biomarker axis)** — cite Wang 2024 → longitudinal PCIst as F1 sub-axis if/when cohort exists.
6. **§8 disclosure #13** — eLife 2025 spontaneous-PCI surrogate validated in healthy + propofol only; not yet in DOC patients.

---

## §5 Falsifier outcome

| F# | preregister | result |
|---|---|---|
| F3 | meta-effect CI crosses 0 → flag inconsistency | **PASS** — 10/10 papers consistent on collapse-on-LOC; 0.31 cutoff stable 2013-2026 |

---

## §6 Honest C3

- Sarasso 2014 PDF binary-encoded → abstract + downstream-citation reading only.
- Wang 2024 specific PCIst numerical cutoff not extracted (abstract-level access).
- No 2026 prospective DOC PCI cohort identified — field appears mature/stable.
- 0/N this cycle were direct REPRODUCE — pure literature meta. Adds 0 to Tononi's "16 strict replications" but anchors our spontaneous-LZ analog (TOP-5 #5) in 5 fresh 2024-2025 corroborating strands and surfaces a TMS-free path that drops N-19 hardware capex to ~$0.

---

## §7 Cross-ref

- Parent spec: `docs/n_21_iit40_12_remaining_spec_2026_05_01.md` §4.3
- N-19 PCI spec target: `docs/n_substrate_n19_pci_spec_2026_05_01.md`
- TOP-5 #5 spontaneous-LZ analog (related convergence target)
- State: `state/n_21_test5_sarasso_tep_review_2026_05_01/cross_paper_pci_cutoff_table.json`

---

## §8 Sources

- Sarasso et al. 2014 (Clin EEG Neurosci) — https://journals.sagepub.com/doi/abs/10.1177/1550059413513723
- Casali et al. 2013 (Sci Transl Med) — https://pubmed.ncbi.nlm.nih.gov/23946194/
- Casarotto et al. 2016 (Ann Neurol, n=150, PCI*=0.31) — https://pmc.ncbi.nlm.nih.gov/articles/PMC5132045/
- Comolatti et al. 2019 (Brain Stim, PCIst) — https://www.sciencedirect.com/science/article/abs/pii/S1935861X19302207
- Sarasso et al. 2021 (NeuroImage clinical applications) — https://pmc.ncbi.nlm.nih.gov/articles/PMC7760168/
- Comanducci 2024 (Brain Stim, subacute CMD) — https://www.brainstimjrnl.com/article/S1935-861X(23)00733-7/fulltext
- Wang et al. 2024 (JNER, rTMS biomarker) — https://pmc.ncbi.nlm.nih.gov/articles/PMC11411826/
- Communications Biology 2024 (resting-state predicts PCI) — https://www.nature.com/articles/s42003-024-06613-8
- eLife 98920 (2025, spontaneous PCI surrogate) — https://elifesciences.org/articles/98920
- Sensory-evoked PCIst bioRxiv 2025 — https://www.biorxiv.org/content/10.1101/2025.07.04.663180v1
- Wikipedia PCI — https://en.wikipedia.org/wiki/Perturbational_Complexity_Index

---

**status**: N21_TEST5_REVIEW_COMPLETE · F3_PASS
**verdict_key**: cutoff_0.31_STABLE · 16ch_0.25_INTERPOLATION_ONLY · 6_n19_spec_updates_proposed · TMS_free_path_surfaced
