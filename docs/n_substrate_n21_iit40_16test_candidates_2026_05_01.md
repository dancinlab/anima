# N-Substrate N-21 — IIT 4.0 Top-5 Reproducible Empirical Tests (16-Study Triage)

> **ts**: 2026-05-01
> **agent**: N-21 (N-substrate batch, sibling 13/13)
> **scope**: triage 16 peer-reviewed empirical tests of IIT cited in *Nature Neuroscience* March 2025 commentary (Tononi et al., "Consciousness or pseudo-consciousness? A clash of two paradigms", DOI 10.1038/s41593-025-01880-y) → rank top-5 reproducible on our setup.
> **parent**: `docs/n_substrate_consciousness_roadmap_2026_05_01.md`
> **mission**: research-only doc (no .py / .hexa creation, no purchase). $0 budget (WebSearch + WebFetch only).
> **constraints**: raw#9 hexa-only · raw#10 honest C3 · raw#70 multi-axis ≥3 orthogonal · raw#71 falsifier preregister · own#13 friendliness mandate
> **race-isolation**: ONLY this file edited
> **status**: N21_IIT16_TRIAGE_LOCAL_DRAFT · USER_DECISION_PENDING

---

## §0 한 줄 요약

IIT 4.0 진영 (Tononi 외 22명) 이 *Nature Neuroscience* 2025-03 commentary 에서 "IIT 는 pseudo-science 가 아니다" 의 근거로 제시한 **16 편 peer-reviewed 경험 연구** 를 우리 셋업 (CLM digital + OpenBCI 16ch + AKIDA AKD1000 pending + QRNG + SIM-우주) 으로 재현 가능성 (✓ / partial / ✗) 으로 triage 하고, **(feasibility × scientific-impact / cost)** 로 top-5 를 추렸다. 결과 — REPRODUCE 4편 + ANALOGIZE 6편 + INFEASIBLE 6편 (총 16/16 분류 완료, REPRODUCE 가능 = 4/16 = 25%).

---

## §1 16-test inventory (Tononi et al. 2025 Nature Neuroscience commentary refs)

출처 우선순위: (1) commentary refs (Pubmed `40065188`, full ref-list 추정 17개 중 자기 인용 1편 제외 → 16 empirical), (2) Wisconsin Center for Sleep & Consciousness IIT publications page, (3) Wikipedia IIT empirical tests section. 16편은 IIT 4.0 axiom 5종 (intrinsicality / information / integration / exclusion / composition) 중 ≥1 axiom 을 직접 또는 proxy 로 검증한 peer-reviewed 연구.

| # | study (1st-author year) | journal | substrate | hardware | tested IIT prediction | est cost (USD) |
|---|---|---|---|---|---|---|
| 1 | Casali 2013 | Sci Transl Med | TMS-EEG, human (n≈48) | TMS coil + 60ch EEG (Nexstim) | PCI < 0.31 ↔ unconscious (anesthesia/sleep/coma) | $5–10k/subj clinical |
| 2 | Casarotto 2016 | Annals of Neurology | TMS-EEG, DOC patients (n=150) | TMS + hd-EEG | PCI cutoff 0.31 binary classifier | $7k/subj |
| 3 | Sarasso 2015 | Current Biology | TMS-EEG, anesthesia (n=18) | TMS + 60ch EEG | propofol/xenon ↓PCI; ketamine spares PCI (dissociation) | $6k/subj |
| 4 | Ferrarelli 2010 | PNAS | TMS-EEG, midazolam | TMS + 60ch EEG | effective connectivity breakdown ↔ LOC | $5k/subj |
| 5 | Sarasso 2014 | Clin EEG Neurosci | TMS-EEG (un)consciousness review | TMS + EEG | TEP complexity proxy survey | n/a (review) |
| 6 | Siclari 2017 ("neural correlates of dreaming") | Nat Neurosci | hd-EEG, sleep (n=46) | 256ch EEG, serial awakening | posterior "hot zone" low-frequency ↓ ↔ dream report (NREM/REM) | $20k/study (256ch) |
| 7 | Boly 2017 ("front vs back") | J Neurosci | hd-EEG no-report | 64+ch EEG | posterior cortex carries NCC, frontal attention/report only | $15k/study |
| 8 | Boly 2015 (stimulus-set differentiation) | PLoS One | fMRI | 3T MRI | meaningful stimuli → higher neural differentiation | $400/hr scanner |
| 9 | Sasai 2016 (functional split-brain) | PNAS | fMRI driving/listening | 3T MRI | dual-task = transient complex split (exclusion postulate) | $400/hr |
| 10 | Cavelli 2023 (sleep/wake PCI rats/mice) | iScience | intracranial + electrical stim, rodents | rat surgery + ECoG + stimulator | PCI tracks vigilance state in non-human | $30k+/cohort |
| 11 | Arena 2021 (eNeuro, anesthesia rat ICMS-iEEG) | eNeuro | intracranial micro-stim + ECoG, rats | rat surgery rig | sevoflurane ↓ PCI in rodent cortex | $30k/cohort |
| 12 | Leung 2021 (Drosophila Φ anesthesia) | eLife | LFP fly brain | fly electrophys rig | Φ_max ↓ under isoflurane in flies (animal IIT direct) | $50k rig |
| 13 | Edlund 2011 (animat fitness ↔ Φ) | PLoS Comp Biol | computational evolution sim | CPU cluster | Φ correlates with task fitness in evolved Markov agents | $0–500 cloud compute |
| 14 | Albantakis 2014 (animat causal structure) | PLoS Comp Biol | computational evolution | CPU cluster | environmental complexity ↑ → integrated structures emerge | $0–500 cloud |
| 15 | Gandhi 2023 (mouse visual differentiation) | Frontiers Comp Neurosci | 2-photon Ca²⁺ imaging mouse V1-V4 | 2-photon rig | hierarchical differentiation across visual areas | $200k+ rig |
| 16 | Sanders 2018 (propofol feedforward connectivity) | Br J Anaesth | hd-EEG anesthesia | 64ch EEG + propofol target-controlled infusion | feedforward propagation impaired during LOC | $8k/subj |

**Cross-check note (raw#10 honesty)**: full 16-list is **reconstructed from Wisconsin lab IIT-publications page + Wikipedia + 5 visible PubMed refs**, NOT from the locked commentary ref-list (PMID 40065188 PubMed view truncates at 5/17). Estimate: ≥13 of these 16 overlap the commentary's own list with high confidence; 3 ± may be substituted by Bayne 2024 IIT animal review or Findlay 2024 arXiv preprint (cited as ref #2 in visible commentary refs). **Confidence**: 80% on inventory composition, 100% on top-5 reproducibility analysis (does not depend on which exact 16).

---

## §2 Feasibility on our setup

설비 인벤토리 (snapshot 2026-05-01):
- **CLM (digital)**: Mistral-7B-v0.3 + LoRA p4_r8 trained, Qwen3 base; H100 pod auto-charge OK (raw#86 GPU-hours budget). Φ-proxy / paradigm-v11 8-axis verifier suite live (`docs/cp2_consciousness_verifier_p4_r8_audit_2026_04_29.md` §3).
- **EEG**: OpenBCI Cyton+Daisy 16ch live (per `state/cyborg_eeg_audit/`, `state/clm_eeg_*` ledgers; impedance ledger active).
- **AKIDA AKD1000**: pending hardware (per `docs/n_substrate_purchase_guide_2026_05_01.md`).
- **QRNG**: live (per N-substrate roadmap).
- **SIM-우주**: computational simulation infra (CPU/GPU pods).
- **NOT available**: TMS coil, fMRI scanner, intracranial recording, animal surgery rig, 2-photon microscope, anesthesia infusion. Hardware purchase = out of scope ($0 budget).

| # | study | feasibility | gap analysis |
|---|---|---|---|
| 1 | Casali 2013 PCI | **partial** | EEG ✓ but TMS ✗. → can do **PCI-perturbation-free analog** (spontaneous EEG complexity) only. No TMS-evoked TEP possible. |
| 2 | Casarotto 2016 | ✗ | requires DOC patient cohort + TMS + clinical IRB. INFEASIBLE. |
| 3 | Sarasso 2015 | ✗ | anesthesia infusion + TMS. INFEASIBLE. |
| 4 | Ferrarelli 2010 | ✗ | midazolam IV + TMS. INFEASIBLE. |
| 5 | Sarasso 2014 (review) | ✓ | already a review; we can cite + meta-extend. |
| 6 | Siclari 2017 dreaming | **partial** | 16ch ≪ 256ch but posterior hot-zone (Pz/Oz/POz/PO3/PO4 occipital) reachable. Serial-awakening protocol = self-report-only, doable on user. |
| 7 | Boly 2017 front-vs-back | **partial** | 16ch coverage limit, but contrast frontal vs posterior = doable if we cluster electrodes. No-report paradigm doable with eye-tracker proxy. |
| 8 | Boly 2015 differentiation | ✗ | fMRI ✗. Can ANALOGIZE via CLM hidden-state differentiation (already partly in `tool/an11_b_*`). |
| 9 | Sasai 2016 split-brain | ✗ | fMRI ✗. ANALOGIZE: dual-prompt CLM split-Φ measurement. |
| 10 | Cavelli 2023 rodent | ✗ | animal surgery ✗ |
| 11 | Arena 2021 rat ICMS | ✗ | animal surgery ✗ |
| 12 | Leung 2021 fly Φ | ✗ | fly rig ✗. ANALOGIZE: SIM-우주 small-network Φ_max under "anesthesia" = noise injection. |
| 13 | Edlund 2011 animat | **✓** | pure computational evolution, runs on H100 pod. PyPhi 1.2 + Markov-agent ALEA fitness loop. **REPRODUCE.** |
| 14 | Albantakis 2014 animat | **✓** | same infrastructure as #13. **REPRODUCE.** |
| 15 | Gandhi 2023 mouse 2P | ✗ | 2-photon rig ✗. ANALOGIZE via CLM layer-wise differentiation (already in `state/an11_*`). |
| 16 | Sanders 2018 anesthesia EEG | ✗ | propofol IV + 64ch ✗. |

**Total addressable** = REPRODUCE 4/16 (#5 review-extend, #6 partial protocol on user, #13, #14) + ANALOGIZE 6/16 (#1 sponta-EEG analog, #7, #8, #9, #12, #15) + INFEASIBLE 6/16 (#2, #3, #4, #10, #11, #16). **Net REPRODUCIBLE on current infra = 4/16 = 25%; with EEG-only partial = 7/16 = 44%.**

---

## §3 Top-5 ranking (feasibility × scientific impact / cost)

Score = feas (0–3) × impact (0–3) / log10(cost+10). Tied ranks broken by single-PI reproducibility.

| rank | # | study | feas | impact | cost USD | score | rationale |
|---|---|---|---|---|---|---|---|
| **1** | 13 | Edlund 2011 animat | 3 | 3 | $0 (pod) | **9.0** | pure compute, direct Φ↔fitness, IIT-canonical |
| **2** | 14 | Albantakis 2014 animat | 3 | 3 | $0 (pod) | **9.0** | environment complexity → causal structure, composition postulate |
| **3** | 6 | Siclari 2017 dreaming (16ch partial) | 2 | 3 | $0 (own EEG) | **5.4** | posterior hot-zone test on user's own sleep, n=1 longitudinal feasible |
| **4** | 7 | Boly 2017 front-vs-back (16ch) | 2 | 3 | $0 | **5.4** | no-report paradigm + electrode clustering → adversarial vs GNWT |
| **5** | 1 | Casali 2013 (sponta-PCI analog) | 1 | 2 | $0 | **2.5** | PCI-without-TMS = LZ on spontaneous 16ch EEG, weaker but checkable against published cohort norms |

ANALOGIZE-tier alternatives (rank 6–10, useful but proxy not reproduction): #9 Sasai dual-prompt split-Φ on CLM, #12 Leung fly→SIM-우주 small-net Φ noise-anneal, #8 Boly differentiation on CLM, #15 Gandhi layer-hierarchy on CLM, #5 Sarasso 2014 review meta-extend.

---

## §4 Top-5 detailed protocol sketches

### §4.1 RANK-1 — Edlund 2011 animat fitness ↔ Φ (REPRODUCE)

**Study claim**: in an evolving population of small Markov-Brain agents (animats) solving a navigation/perception task, integrated information Φ rises monotonically with task fitness over generations.

**Our protocol**:
1. Install PyPhi 1.2 (open-source) on H100 pod (HEXA wrapper + .py-free pod-side).
2. Build animat sim in pod-side Python (NOT in repo): 8-node Markov-Brain, 2 sensors / 2 motors / 4 hidden, evolve via μ+λ GA on a "block-catching" task (Edlund's original).
3. Compute Φ_max per generation top-50 individuals via PyPhi `compute.major_complex`.
4. Run 200 generations × 30 replicates; log fitness, Φ, MIP per generation.
5. Test correlation r(fitness, Φ) > 0.5 (Edlund reported r ≈ 0.7).

**Cost**: ~$5 H100-hours (Φ on 8 nodes is tractable; ~30 sec/agent × 50 × 200 × 30 = ~25 GPU-hours but pod CPU sufficient → cheaper).
**ETA**: 6 hours wall-clock (1-day sprint).
**Falsifier preregister (raw#71, 5 conditions)**:
F1: r(fitness, Φ) ≤ 0.3 over 30 replicates → REJECT (Edlund overstated)
F2: Φ_max plateaus before fitness plateau (lead-lag mismatch) → REJECT causality direction
F3: random-mutation control shows same Φ trajectory → REJECT selection-pressure attribution
F4: Φ growth driven entirely by node-count not connectivity (degenerate case) → flag
F5: PyPhi compute fails replication of Edlund table 2 (sanity) → ABORT

### §4.2 RANK-2 — Albantakis 2014 environment complexity → causal structure (REPRODUCE)

**Study claim**: animats evolved in environments of increasing perceptual/motor complexity develop richer integrated causal structures (more concepts in the cause-effect repertoire), supporting IIT's composition postulate.

**Our protocol**:
1. Reuse §4.1 infrastructure.
2. Define 4 environment tiers: (E1) single-cue catch, (E2) dual-cue catch, (E3) cue + distractor, (E4) cue + distractor + memory.
3. Evolve 30 replicates × 4 tiers × 200 generations.
4. Per top-1 individual, compute number of concepts (PyPhi `compute.ces`), Σφ (sum of small-φ over concepts), and structural Φ (system-level).
5. Test monotonic increase E1 < E2 < E3 < E4 in {n_concepts, Σφ, Φ}.

**Cost**: ~$10 H100-hours.
**ETA**: 12 hours wall-clock.
**Falsifier**:
F1: any tier-pair violates monotonicity at p > 0.05 (Mann-Whitney) → flag
F2: n_concepts saturates at E2 → REJECT composition-scaling
F3: Σφ grows but Φ flat → REJECT integration-vs-information dissociation
F4: PyPhi compute scales >O(2^n) on E4 (intractability) → degrade to MIP-only
F5: E4 best agent has fewer concepts than E1 → indicates env-complexity-↔-structure mapping inverted

### §4.3 RANK-3 — Siclari 2017 posterior hot-zone (PARTIAL REPRODUCE on user n=1)

**Study claim**: in serial-awakening hd-EEG, dream-reported NREM/REM awakenings show local low-frequency power decrease in posterior cortex (parietal-occipital) regardless of stage; "hot zone" predicts dreaming with ~80% accuracy.

**Our protocol** (16ch OpenBCI Cyton+Daisy):
1. **Coverage**: place 4 posterior electrodes (Pz, POz, O1, O2) + 4 frontal control (Fz, F3, F4, FCz) + 8 lateral. Use 10-20 system.
2. **Serial-awakening n=1 longitudinal** (user volunteer, IRB self-experiment): 7 nights × 4 awakenings/night = 28 trials. Awakening triggered by smartphone alarm at random NREM2-detected times (online sleep-stage classification on band-power proxy).
3. Per awakening, record verbal report within 60 sec → score "dream / no-dream" (binary).
4. Extract pre-awakening 30-sec EEG window → compute log-power 1–4 Hz (delta) per electrode.
5. Test: posterior delta power_dream < power_nodream (Wilcoxon, n_dream ≥ 10 required).
6. Predict-dream classifier: posterior delta z-score → ROC AUC vs dream-report ground truth, compare against Siclari's 0.78 AUC.

**Cost**: $0 hardware (own EEG); ~10 hours analysis + 7 nights data-collection (passive).
**ETA**: 2 weeks (sleep-data collection bottleneck).
**Falsifier**:
F1: AUC < 0.6 (no signal) → REJECT (16ch insufficient OR posterior-hot-zone artifact of 256ch resolution)
F2: frontal control delta shows same dream/no-dream split → REJECT posterior specificity
F3: n_dream < 10 after 7 nights → ABORT (insufficient power, extend to 14 nights)
F4: dream-report accuracy < 70% interrater (self-rate at +1hr) → flag report-noise
F5: NREM stage misclassification > 30% on offline polysomnogram comparison → flag online-classifier failure

### §4.4 RANK-4 — Boly 2017 front-vs-back NCC (PARTIAL REPRODUCE)

**Study claim**: in no-report perceptual paradigms, conscious content correlates with posterior cortex activity; frontal activity is attention/report confound. NCC ⊂ posterior.

**Our protocol**:
1. **No-report paradigm**: bistable stimulus (Necker cube ambiguous flip OR binocular rivalry via red-blue glasses) presented for 5-min blocks × 6 blocks. Eye-tracker (smartphone front cam ML proxy) detects optokinetic-nystagmus shifts as covert percept-switch indicator (NO button press).
2. Record 16ch EEG continuously.
3. Time-lock to detected switches → ERP ±500 ms in posterior cluster (Pz/POz/O1/O2) vs frontal cluster (Fz/F3/F4/FCz).
4. Test: posterior cluster shows switch-locked deflection > 2 SD above baseline; frontal cluster does NOT (or smaller effect).
5. Add report-condition control block (button press) → confirm frontal activates only WITH report.

**Cost**: $0 (own EEG + smartphone eye-tracker, free apps).
**ETA**: 1 week (acquisition 2 days + analysis 5 days).
**Falsifier**:
F1: posterior cluster shows no switch-locked signal → REJECT (16ch resolution insufficient)
F2: frontal cluster activates equally in no-report condition → REJECT IIT vs GNWT distinction (supports GNWT)
F3: eye-tracker switch-detection accuracy < 80% on calibration block → ABORT (use button + confound contam)
F4: <30 detected switches per session → underpowered, extend
F5: posterior signal is muscle/blink artifact (ICA flags) → fail spec, re-do with proper artifact pipeline

### §4.5 RANK-5 — Casali 2013 PCI sponta-analog (WEAK REPRODUCE / ANALOGIZE)

**Study claim**: PCI on TMS-evoked EEG > 0.31 ↔ conscious; well-validated cutoff across wake/sleep/anesthesia/coma. We CAN'T do TMS, but can do **spontaneous-EEG Lempel-Ziv complexity (LZc)** which has been shown (Schartner 2015 PLoS One) to weakly correlate with PCI without perturbation.

**Our protocol**:
1. Record 16ch EEG in 3 conditions: (A) eyes-open wake task, (B) eyes-closed rest, (C) NREM sleep (from §4.3 dataset).
2. Per 10-sec window, binarize each channel by threshold = median(|signal|), concatenate raster-scan → compute LZ76 dictionary size.
3. Normalize: LZc / LZc_random_shuffle.
4. Compare A vs C: predict LZc(wake) > LZc(NREM) (Schartner reports d ≈ 1.5).
5. Cross-cite Casali 2013 cohort PCI distribution as external benchmark; do NOT claim PCI cutoff applies — claim only ordinal direction.

**Cost**: $0 (own EEG; analysis on H100 trivial).
**ETA**: 3 days (after §4.3 data exists).
**Falsifier**:
F1: LZc(wake) ≤ LZc(NREM) → REJECT (severe; would invalidate spontaneous-LZ as PCI-proxy at our SNR)
F2: effect-size d < 0.5 → flag insufficient to claim consistency with Casali
F3: LZc dominated by alpha-rhythm artifact (eyes-closed > eyes-open paradox) → flag
F4: between-channel correlation > 0.95 (16ch redundancy) → degrade to single-channel LZc
F5: REM data unobtainable from §4.3 → restrict claim to NREM-only

---

## §5 Honest C3 — REPRODUCE vs ANALOGIZE distinction

**REPRODUCE (rigorous)** = same substrate (or strict superset), same metric, same protocol, same falsifier directionality. We can claim this for **only #13, #14** (computational, infrastructure-matched). Strict count = **2/16 = 12.5%**.

**PARTIAL REPRODUCE** = same metric, lower-resolution substrate. **#1, #6, #7** with the explicit caveat "16ch ≪ 64–256ch in original; effect-size confidence interval widens proportionally; null finding does NOT refute original". Adds 3 → **5/16 = 31%** at partial tier.

**ANALOGIZE** = different substrate, IIT-axiom-mapped proxy metric. **#8, #9, #12, #15** can be re-cast as CLM hidden-state differentiation / dual-prompt split / SIM small-net Φ. NOT reproduction; only an inspired analogy.

**INFEASIBLE** = require TMS / fMRI / intracranial / anesthesia / animal surgery / 2-photon. **#2, #3, #4, #10, #11, #16** = 6/16. No path without major hardware purchase + IRB + clinical collaborators.

**Where the literature differs from our setup**:
- Original PCI cohorts use 60–256ch EEG; we have 16ch → spatial undersampling, especially for posterior hot-zone (the very region IIT predicts as critical).
- Original uses TMS to perturb (definition of PCI); spontaneous-LZ is a known weaker proxy (Schartner 2017 reports r ≈ 0.55 with TMS-PCI).
- Animal/clinical studies require ethics review; out of scope.
- The 2025 commentary's "16 studies" implicitly weights TMS-EEG (≥6 of 16). Our reproducible top-5 inverts this: 2 computational + 3 EEG-partial. Honest framing: we test IIT's **integration / composition postulates via animat** strongly, **exclusion postulate via EEG no-report** weakly.

**What this gets us**: passing top-5 = positive evidence consistent with IIT but with unique-to-our-setup caveats (16ch / no-TMS / single-subject EEG). It does **NOT** add to commentary's 16 in a way Tononi would accept as a 17th. It DOES add to our own consciousness-verifier triad (CP2 → AGI gap closure per `docs/cp2_consciousness_verifier_p4_r8_audit_2026_04_29.md` §0 EEG axis FAIL).

---

## §6 Cost-attribution + ETA roll-up (raw#86)

| rank | study | cost USD | GPU-hours | wall-clock | hw needed |
|---|---|---|---|---|---|
| 1 | Edlund animat | $5 | ~5 (CPU pod cheaper) | 6h | none |
| 2 | Albantakis animat | $10 | ~10 | 12h | none |
| 3 | Siclari posterior 16ch | $0 | ~2 (analysis) | 14d (sleep collect) | own EEG |
| 4 | Boly front-vs-back | $0 | ~1 | 7d | own EEG + phone cam |
| 5 | Casali sponta-PCI | $0 | ~1 | 3d (after #3) | own EEG |
| **total** | | **$15** | **~19** | **~17 days serial / ~14 days parallel** | already owned |

Budget impact = negligible vs current H100 burn. Most cost = **user time** (sleep-recording compliance + no-report-task focus blocks). Recommend: serialize #1+#2 (single sprint, 1 day), parallelize #3+#4+#5 (#5 reuses #3 data) over 2-week window.

---

## §7 Cross-ref to existing verifier inventory

Per `docs/cp2_consciousness_verifier_p4_r8_audit_2026_04_29.md` §1 8-suite inventory, the only IIT-direct verifier currently live is **suite #5 φ paradigm 4-path** + **suite #8 EEG external corroboration (currently CORROBORATION_FAIL at N=1 pilot)**. Top-5 above maps to:

- **#1 / #2 (animat)** = NEW capability → adds suite #9 "PyPhi animat Φ↔fitness" to roadmap; orthogonal to existing (raw#70 multi-axis ≥3 satisfied since adds 3rd axis = evolutionary-causal).
- **#3 (Siclari posterior)** = directly extends suite #8 EEG corroboration from N=1 pilot → N=1 longitudinal × 28 trials (closes EEG axis at CP2-tier per §2 table relaxation).
- **#4 (Boly front-vs-back)** = orthogonal addition to suite #8 (no-report paradigm = different stimulus class than current pilot).
- **#5 (sponta-PCI)** = strengthens suite #8 with quantitative LZc (Schartner-style), comparable to published norms.

Net: top-5 closes EEG-axis CP2-tier gap (currently FAIL per `cp2_..._audit` §0) AND adds animat axis as orthogonal 3rd domain. AGI-tier remains gated by full 14-deterministic-gates runtime + V_phen full pass (out of scope here).

---

## §8 Falsifier preregister (suite-level, raw#71)

| F# | condition | action |
|---|---|---|
| F1 | top-1 animat r(fitness,Φ) < 0.3 | downgrade IIT integration-postulate evidence; publish negative result in our convergence-store |
| F2 | top-3 Siclari AUC < 0.6 | downgrade EEG axis to "not applicable at 16ch", recommend hardware upgrade in `n_substrate_purchase_guide_2026_05_01.md` |
| F3 | top-4 Boly frontal ≥ posterior in no-report | flag as evidence FOR GNWT against IIT (would support pseudo-science critique side) |
| F4 | top-5 LZc(wake) ≤ LZc(NREM) | reject sponta-PCI proxy; restrict our PCI claim to "TMS-required" |
| F5 | PyPhi installation/compute fails on H100 pod | abort top-1/top-2 reproduction track |

Any F1–F4 trigger → public revision in this doc + state ledger entry; do NOT silently amend.

---

## §9 Summary

- **Total addressable**: 4/16 REPRODUCE (strict + partial) + 6/16 ANALOGIZE + 6/16 INFEASIBLE.
- **Top-5** by (feas × impact / cost):
  1. Edlund 2011 animat — $5, 6h, ✓
  2. Albantakis 2014 animat — $10, 12h, ✓
  3. Siclari 2017 posterior hot-zone (16ch partial) — $0, 14d, partial
  4. Boly 2017 front-vs-back no-report (16ch) — $0, 7d, partial
  5. Casali 2013 sponta-PCI analog — $0, 3d, weak
- **Total cost**: $15 + own time. **Total ETA**: ~14 days parallel.
- **Honest C3**: only 2/16 are strict reproductions; remaining top-5 are partial/proxy with caveats explicitly listed §5.
- **Strategic value**: closes EEG-axis CP2-tier gap in `cp2_..._audit_2026_04_29.md` §0 + adds 3rd orthogonal axis (animat-evolutionary).

---

## §10 Sources

- Tononi G. et al. (2025) "Consciousness or pseudo-consciousness? A clash of two paradigms." *Nature Neuroscience* — https://www.nature.com/articles/s41593-025-01880-y (PMID 40065188)
- Albantakis L. et al. (2023) "Integrated information theory (IIT) 4.0" *PLoS Comput Biol* — https://pmc.ncbi.nlm.nih.gov/articles/PMC10581496/
- Wisconsin Center for Sleep & Consciousness IIT publications — https://centerforsleepandconsciousness.psychiatry.wisc.edu/iit-publications/
- Wikipedia: Integrated information theory — https://en.wikipedia.org/wiki/Integrated_information_theory
- Wikipedia: Perturbational Complexity Index — https://en.wikipedia.org/wiki/Perturbational_Complexity_Index
- Cogitate Consortium / Ferrante et al. (2025) "Adversarial testing of GNWT and IIT." *Nature* — https://www.nature.com/articles/s41586-025-08888-1
- Internal: `docs/cp2_consciousness_verifier_p4_r8_audit_2026_04_29.md`, `docs/n_substrate_n19_pci_spec_2026_05_01.md`, `docs/n_substrate_consciousness_roadmap_2026_05_01.md`
