# N-23 — Adamatzky slime mold + mycelium protocol prep

> **Date**: 2026-05-01
> **Author**: anima agent N-23 (protocol prep, NO purchase)
> **Status**: SPEC_DRAFT — research-only, $0 spend, no vendor contact
> **Constraints**: raw#9 hexa-only · raw#10 honest C3 · raw#71 falsifier-bound (BIDIRECTIONAL) · race-isolation: ONLY this doc + `state/n_23_adamatzky_protocol_prep_2026_05_01/*.json`
> **Source mission**: `docs/strategic_alm_clm_review_2026_05_01.md` §13.1 — N-23 = $200 highest-feasibility kit, tests pre-neural information processing as Φ-substrate sibling of CLM/EEG/AKIDA paradigm v11
> **Companion N-substrate specs**: `n_substrate_n11_finalspark_access_spec_2026_05_01.md` (organoid), `anima_eeg_openbci_16ch_track_plan_2026_05_01.md` (EEG)

---

## §0 framing

N-23 occupies the **non-neural biological substrate** slot in the strategic_alm_clm_review §4.2 "missing substrate" gap. It is the cheapest entry into Putnam multi-realizability evidence outside silicon/neural and the only N-track in the roadmap whose first kit fits inside a $200 envelope without any partnership.

This document is a **prep spec only**. It specifies vendor inventory, per-component cost, measurement protocol (paradigm v11 8-axis adaptation for non-neural spike trains), 5 BIDIRECTIONAL falsifier predicates per raw#71, and an honest C3 separating sound from hand-wave claims.

**Out of scope (deliberately)**: purchase orders, vendor outreach, IRB language, biosafety SOPs (those activate only when a buy decision is made by the user separately).

---

## §1 Adamatzky inventory (UWE Bristol Unconventional Computing Laboratory)

### 1.1 lab profile

| field | value |
|---|---|
| director | Andrew Adamatzky (Professor, Unconventional Computing) |
| institution | Department of Computer Science and Creative Technologies, UWE Bristol |
| group | Unconventional Computing Laboratory (UCL) |
| research scope | reaction-diffusion computing, cellular automata, Physarum computing, fungal computing, bionics, novel hardware, future and emergent computation |
| public profile | UWE staff page, Google Scholar, ResearchGate, sciprofiles |

### 1.2 representative literature applicable to N-23

| year | citation (short) | substrate | core finding usable to N-23 |
|---|---|---|---|
| 2018 | "Towards fungal computer" — Interface Focus 8(6) — Adamatzky | mycelium | proposes Basidiomycetes as computing devices: information ≡ spike trains, computation ≡ mycelial network propagation, interface ≡ fruiting bodies |
| 2018 | "On resistive spiking of fungi" — arxiv 2009.00292 (preprint), later Biophysical Reviews and Letters 2021 | mycelium | impedance modulates spike emission; spike duration 1–21 h, amplitude 0.03–2.1 mV |
| 2021 | "Fungal electronics" — Biosystems 212 (S0303264721002288) | mycelium | mycelium-bound composites act as living electronic devices; impedance shift under stimulation |
| 2022 | "Language of fungi derived from their electrical spiking activity" — Royal Society Open Science 9(4) 211926 | mycelium (4 species) | spike-train statistics reveal species-specific "lexicon"; complexity analysis of spike sequences |
| 2022 | "Electrical spiking of psilocybin fungi" — bioRxiv 2022.07.02.498545 | psilocybin fungi | extension of language-of-fungi to a non-Basidiomycete clade |
| 2022 | "Electrical frequency discrimination by fungi Pleurotus ostreatus" — arxiv 2210.01775 | oyster mushroom | demonstrates oyster mycelium responds differentially to stimulation frequency |
| 2024 | "Sensorimotor control of robots mediated by electrophysiological measurements of fungal mycelia" | mycelium → robot | closed-loop bidirectional substrate-actuator demonstration |
| 2024 | "Exploring discrete space-time models for information transfer: Analogies from mycelial networks to the cosmic web" — Bio Systems (PubMed 39053645) | mycelium (theory) | discrete-spacetime information-transport model |
| 2025 | "Millisecond spiking units in dispersed mycelial liquid culture MEA recordings absent in dehydration and fungicidal assays" — bioRxiv 2025.08.12.669623 | mycelium liquid culture + MEA | fast spiking units in 150–3000 Hz band; trough-to-peak 1.58 ± 0.14 ms; n=177 units across triplicates |
| 2026 | "Propagation of electrical spike trains in substrates colonised by oyster fungi" — bioRxiv 2026.01.12.699130 | oyster mycelium-colonised substrate | spike-train propagation kinetics across composite substrate |
| 2025-09 | "Detection of electrical signals in fungal mycelia in response to external stimuli" — PMC12483595 | mycelium | causal stim-response coupling |

### 1.3 Physarum-specific reference protocol (Adamatzky lineage, used as N-23 baseline)

- **Substrate**: 2% non-nutrient agar (10 cm Petri dish). Inoculation by oat flake colonised with clonal *P. polycephalum* on one hemisphere; bare oat flake (target) on the other hemisphere.
- **Recording window**: ≥ 5 h after inoculation, after a single protoplasmic tube bridges the two flakes.
- **Electrodes**: aluminium foil contact (Adamatzky's published preference for low-cost reproducibility) at each oat flake; substitute-grade Ag/AgCl pellet (research-grade) for higher fidelity.
- **DAQ**: PicoLog ADC-24, 24-bit, ±39 mV span, 1 Hz native sampling (sufficient for the dominant slow Physarum oscillation in the 0.01–0.1 Hz band; insufficient for the ms-scale fungal units captured in §1.2 2025-08).
- **Culture maintenance**: 28 ± 2 °C, dark, 200–400 mg oat flakes daily, sub-culture every 5 days.

This is the canonical "$200 first kit" recipe in the literature.

---

## §2 $200 first kit — vendor inventory and cost

> **DO NOT PURCHASE.** This section enumerates options. No vendor will be contacted by this agent. A future buy decision is the user's, separate from this prep doc.

### 2.1 base component table (USD; conservative point estimates from public listings 2026-05)

| # | component | vendor (one of several) | unit cost | qty | line total | notes |
|---|---|---|---:|---:|---:|---|
| 1 | Physarum polycephalum culture kit (Carolina #155825) | Carolina Biological Supply | ~$30 | 1 | $30 | living plasmodium + sclerotium + agar + oat substrate; class-of-30 scale, far exceeds research need |
| 1-alt | Physarum plasmodium living plate (Carolina #156193) | Carolina Biological Supply | ~$15 | 2 | $30 | smaller, fresher; pair allows backup on contamination |
| 1-alt2 | Ward's Physarum Culture and Study Kit (#8883627) | Ward's Science / VWR | ~$35 | 1 | $35 | sibling option; vendor diversity |
| 2 | Pleurotus ostreatus liquid culture (10–30 mL) | Field & Forest / Out-Grow / Amazon listings | ~$15–25 | 1 | $20 | oyster mushroom; matches Adamatzky 2022 Pleurotus protocol |
| 2-alt | Oyster fruiting kit (ready-to-fruit block) | Mushroom Mountain / Henosis / North Spore | ~$25–35 | 1 | $30 | faster start; less control over substrate composition |
| 3 | non-nutrient agar (powder, 100 g) | Carolina or Sigma generic | ~$20 | 1 | $20 | enough for ~30 plates at 2% |
| 4 | sterile Petri dishes (10 cm, pack of 20) | Amazon lab supply | ~$15 | 1 | $15 | single-use |
| 5 | rolled oats (Quaker Old Fashioned) | grocery | ~$5 | 1 | $5 | published Adamatzky preference; substitution ≠ recommended |
| 6 | aluminium foil + craft wire (electrode raw stock) | hardware store | ~$10 | 1 | $10 | matches Adamatzky 2015 reference protocol |
| 7 | Ag/AgCl pellet electrodes (pair, low-grade research) | Warner Instruments / WPI | ~$30 | 1 | $30 | OPTIONAL upgrade over aluminium; better SNR |
| 8 | breadboard + jumper wires + 3.5 mm connectors | Adafruit / Amazon | ~$10 | 1 | $10 | rig assembly |
| 9 | low-cost USB ADC (≥ 16-bit differential) — *substitute for PicoLog ADC-24* | DI-1100 / NI-DAQ / Arduino-MAX11253 | ~$50–150 | 1 | $50 | PicoLog ADC-24 list is ~$1100–1300, OUT of $200 budget; 16-bit substitute degrades SNR but stays within envelope |
| 10 | desk-temp thermometer + small thermal box (28 °C culture) | Amazon | ~$15 | 1 | $15 | passive culture incubation |
| 11 | misc: gloves, parafilm, ethanol wipes, sharpie, log notebook | local pharmacy / Amazon | ~$15 | 1 | $15 | aseptic basics |

### 2.2 baseline kit total

| configuration | components | total |
|---|---|---:|
| **A — minimal Physarum-only** | 1, 3, 4, 5, 6, 8, 9, 10, 11 | **~$160** |
| **B — Physarum + oyster mycelium dual-substrate (canonical N-23)** | 1, 2, 3, 4, 5, 6, 8, 9, 10, 11 | **~$180** |
| **C — B + Ag/AgCl upgrade (better SNR)** | B + 7 | **~$210** (slightly over) |
| **D — research-grade DAQ swap** | B but item 9 → PicoLog ADC-24 ~$1200 | **~$1330** (out of N-23 envelope; reserved for follow-on phase) |

**Selected for N-23 phase-1**: configuration **B at ~$180**, leaving ~$20 contingency for shipping / consumables. Configuration C is the natural phase-1.5 upgrade if the phase-1 SNR is insufficient.

### 2.3 vendor diversity (no purchase)

| component | primary | secondary | tertiary | rationale |
|---|---|---|---|---|
| Physarum culture | Carolina | Ward's / VWR | Southern Biological (live care guides) | three independent supply chains |
| oyster mycelium | Field & Forest | North Spore | Mushroom Mountain | three US suppliers |
| ADC budget | DATAQ DI-1100 | NI-USB-6001 | Arduino + MAX11253 | three off-the-shelf <$150 paths |
| ADC research grade (deferred) | Pico ADC-24 | NI-USB-6210 | LabJack T7-Pro | three reference-grade paths if budget expands |

---

## §3 measurement protocol — paradigm v11 8-axis adapted to non-neural spike trains

### 3.1 substrate-to-axis mapping

paradigm v11 was authored for HF-transformer hidden-state probes (`docs/paradigm_v11_stack_20260426.md` §1). Each axis must be re-anchored on a substrate-appropriate observable when the substrate is biological non-neural. This is the same adaptation pattern N-11 applied for FinalSpark organoids and N-1 applied for Akida SNN.

| axis | v11 source helper | v11 observable (digital) | N-23 observable (slime mold + mycelium) | gate retained? |
|---|---|---|---|---|
| **G0 primary** (AN11(b)) | family eigenvec × template signature | LoRA hidden-state cosine | spike-train ISI eigenvec × Adamatzky-language template signature | YES — substrate-specific template library required (ROC-encoded prompt → spike sequence reference dictionary) |
| **G1 B-ToM** | `anima_b_tom.hexa` | 20 ToM probes × accuracy ≥ 0.7 | DEFERRED phase-1 — no substrate-appropriate behavioral analog | NO (matches N-11 deferral pattern) |
| **G2 MCCA** | `anima_mcca.hexa` | confidence Brier ≤ 0.25 | substrate cannot self-report; PROXY = stim-response variance vs predicted (spike-rate envelope confidence) | PARTIAL — proxy-only |
| **G3 Φ\*** | `anima_phi_star.hexa` | 16-prompt covariance, K=8 random bipartitions, `phi_star_min > 0` | 16 stim-prompts (chemo-tactic gradient + light + temperature step) → multi-channel spike covariance, K=8 bipartition over electrode set; reuse `anima_phi_v3` substrate-agnostic kernel from N-11 spec | YES |
| **G4 CMT** | `anima_cmt.hexa` | per-layer zero-ablation rel-dY ≥ 0.05 | per-tube / per-mycelial-edge **mechanical ablation** (laser cut OR physical excision); rel-dΦ ≥ 0.05 across the 4 family axes (Hexad / Law / Phi / SelfRef projections of the spike-train embedding) | YES — destructive but reproducible on independent dishes |
| **G5 CDS** | `anima_cds.hexa` | 8 long-form prompts × per-token trajectory, max_stability ≥ 0.30 | 8 long stim sequences × per-tube trajectory (5 min envelope, 1 Hz sample); compute embedding stability under same definition | YES |
| **G6 SAE-bypass** | `anima_sae_steer_bypass.hexa` | sparse 4096-feature random steering, n_selective ≥ 2 | DEFERRED phase-1 — no controllable sparse feature substrate; PHASE-2 candidate via spatially patterned light / chemo-stim | NO phase-1 |
| **G7 composite** | `anima_v11_integrate.hexa` | geometric mean ≥ 0.40 over G1..G6 | geometric mean over G2_proxy, G3, G4, G5 (4 axes phase-1) ≥ 0.40 | YES — narrower base than digital |

**Phase-1 honest measurable axes**: G0, G2 (proxy), G3, G4, G5, G7 → **5 of 8** (matches the N-11 organoid coverage).

### 3.2 stim → spike-train encoding

| step | parameter | value |
|---|---|---|
| prompt vocabulary | 16 prompts (4 per family Hexad / Law / Phi / SelfRef) | reuse paradigm v11 standard prompt set, encoded as stim modality below |
| Physarum stim | nutrient drop position | 4 spatial positions × 4 nutrient compositions = 16 stim states |
| mycelium stim | bipolar electrical pulse | amplitude 50–200 mV, duration 100 ms, 4 frequencies × 4 inter-pulse-intervals = 16 stim states |
| sample rate | spike capture | Physarum: 1 Hz (slow oscillation); mycelium: 1 kHz (Adamatzky 2025 fast units) |
| per-trial duration | per stim repetition | 5 min minimum (≥ 4 spikes per Adamatzky train statistic at ~30 min spacing → use rate-density window for short-trial rate-coding) |
| reps per stim | independent trial blocks | 8 (matches v11 K=8 covariance) |
| total per-substrate runtime | 16 × 8 × 5 min | ~10.7 h continuous recording per substrate |
| total campaign | Physarum + mycelium × 3 ANIMA_SEED (raw#71 reproducibility) | ~64 h DAQ-time over 6 dishes / blocks |

### 3.3 Φ\* computation — substrate-agnostic kernel

Reuse `anima_phi_v3` (already substrate-validated on GPU, in-progress on Akida and FinalSpark). Inputs:
- per-electrode spike-rate envelope (binned at 1 s / 100 ms) → covariance matrix C
- K=8 random bipartitions of the electrode set
- φ\*_k = mutual-information-loss surrogate per bipartition; Φ\* = min_k(φ\*_k)

This is intentionally identical to the formulation already used in N-11 to keep cross-substrate comparison representation-level invariant.

### 3.4 cross-substrate alignment with paradigm v11 anchors

| anchor substrate | Φ source | role in N-23 evaluation |
|---|---|---|
| CLM (paradigm v11 4-backbone) | `state/v10_benchmark/...` | digital baseline #1 |
| EEG (Berger / openbci track) | `state/clm_eeg_*` | neural recording baseline |
| AKIDA (N-1) | `state/n_substrate_n1_*` | digital SNN sibling |
| **N-23 Physarum** | this protocol output | non-neural biological #1 |
| **N-23 mycelium** | this protocol output | non-neural biological #2 |

Cross-correlation r(Φ_k_n23, Φ_k_clm) and r(Φ_k_n23, Φ_k_eeg) drive the §4 falsifier verdicts.

---

## §4 falsifier predicates — 5 BIDIRECTIONAL per raw#71

### 4.1 P-1 — slime mold Φ vs neural Φ correlation (cross-substrate Putnam)

| verdict | predicate | meaning |
|---|---|---|
| **PASS_STRONG** | r(Φ_k_physarum, Φ_k_eeg) ≥ **0.70** AND r(Φ_k_physarum, Φ_k_clm) ≥ **0.70** AND \|Φ\*_physarum − Φ\*_eeg\| / max(\|Φ\*_eeg\|, 1e-3) ≤ **0.50** | first non-neural biological anchor of Putnam multi-realizability against both digital + neural recording substrates |
| **PASS_PARTIAL** | one of the two correlations ≥ 0.70, the other 0.40–0.70 | one-sided convergence; weaker anchor |
| **WEAK** | both correlations 0.40–0.70 | partial alignment, encoding fidelity suspect |
| **FAIL** | both correlations < 0.40; OR substrate sign flip | substrate-dependent — Putnam strong form falsified at non-neural boundary; encoding revision required |

**BIDIRECTIONAL conditions**:
- null floor: 1024 stim-shuffled permutation; observed r must exceed 95-percentile of r_null
- 3 ANIMA_SEED reps (seeded family-axis projections + seeded stim block order); 3/3 verdict alignment required for STRONG; 2/3 = WEAK_PASS
- variance gate: std(Φ_k_physarum) < 0.5 · |Φ\*_physarum| or verdict NULL

### 4.2 P-2 — mycelium Φ vs neural Φ correlation (sibling test)

Identical predicate structure to P-1 with mycelium spike-train replacing Physarum. Reported as **independent** verdict; combined verdict in §4.6.

### 4.3 P-3 — environmental complexity → information capacity (Adamatzky-canonical)

| verdict | predicate | meaning |
|---|---|---|
| **PASS** | Lempel-Ziv complexity LZ(spike_train\|stim=high-complex) > LZ(spike_train\|stim=low-complex) at p < 0.01 (paired across 8 reps × 16 stim states stratified into 8 high / 8 low complexity bins) AND linear regression slope of LZ vs stim-Shannon-entropy positive at 95% CI | substrate adapts spike-train complexity to environmental complexity — Adamatzky "language of fungi" core claim independently reproduced |
| **WEAK** | trend in correct direction but not significant at p < 0.01 | suggestive only |
| **FAIL** | no monotonic relationship OR inverted slope | substrate spike train is environment-independent; treats Φ result as decorative rather than functional |
| **REVERSE-FAIL** (BIDIRECTIONAL) | LZ saturates at near-maximum across ALL stim levels (indistinguishable from random) | substrate is producing noise, not encoding; Φ measurement is on a noise channel |

### 4.4 P-4 — mechanical-ablation causal mediation (G4 anchor)

| verdict | predicate | meaning |
|---|---|---|
| **PASS** | rel-dΦ ≥ 0.05 across all 4 family axes (Hexad/Law/Phi/SelfRef projection) when a single protoplasmic tube (Physarum) or mycelial bundle (oyster) is severed; effect persists for ≥ 30 min post-ablation | causal information channel confirmed; Φ contribution is not an artefact of recording geometry |
| **WEAK** | 2–3 of 4 family axes show rel-dΦ ≥ 0.05 | partial causal evidence |
| **FAIL** | < 2 axes affected OR effect dissipates within 5 min (electrode artefact window) | spike train is electrode-coupling noise, not substrate-mediated information |
| **REVERSE-FAIL** | Φ INCREASES post-ablation by ≥ rel +0.05 in any family axis | substrate is encoding the experimenter, not the stim — disqualifies the protocol |

### 4.5 P-5 — cross-substrate consistency (N-23 Physarum ↔ N-23 mycelium)

| verdict | predicate | meaning |
|---|---|---|
| **PASS** | r(Φ_k_physarum, Φ_k_mycelium) ≥ **0.50** across 16 matched stim states | two non-neural substrates produce convergent Φ signatures under matched stim — within-class Putnam evidence |
| **WEAK** | 0.30 ≤ r < 0.50 | weak within-class convergence |
| **FAIL** | r < 0.30 | substrate-pair-dependent; no within-non-neural consistency |
| **REVERSE-FAIL** | r negative AND \|r\| ≥ 0.30 | anti-correlated substrates → encoding maps environment-orthogonal directions; protocol-stim interaction confound |

### 4.6 N-23 composite verdict gate

```
N-23 composite =
  (P-1 AND P-2)      // both substrates agree with neural anchor
  AND P-3            // information-capacity scaling holds
  AND P-4            // causal channel confirmed
  AND P-5            // within-class consistency
```

| level | requirement |
|---|---|
| **N-23 STRONG** | all 5 PASS (P-1 and P-2 STRONG-tier) |
| **N-23 PASS** | ≥ 4 PASS, no FAIL, no REVERSE-FAIL |
| **N-23 WEAK** | 3 PASS or any WEAK; no FAIL |
| **N-23 FAIL** | any FAIL or REVERSE-FAIL |

---

## §5 honest C3 — sound vs hand-wave matrix

### 5.1 sound (defended)

| 항목 | 근거 |
|---|---|
| ✅ Adamatzky lineage protocol is the published reference | § 1.2 / 1.3 — multiple peer-reviewed RSOS / Interface Focus / Biosystems papers; not invented here |
| ✅ Φ\* kernel substrate-agnostic | `anima_phi_v3` already validated GPU + Akida + (in-progress) FinalSpark; representation-level invariance argued in N-11 spec §7.1 |
| ✅ paradigm v11 axis adaptation pattern matches N-11 / N-1 | 5/8 axis coverage, deferral of B-ToM and SAE — same compromise as organoid spec |
| ✅ falsifier 5-tier with BIDIRECTIONAL conditions per raw#71 | §4 includes REVERSE-FAIL on P-3, P-4, P-5; null-floor permutation; 3-seed reproducibility |
| ✅ $200 envelope is real, not aspirational | §2 itemized with three vendor paths per category; configuration B = ~$180 |
| ✅ no purchase, no contact — prep-only mission honored | this entire doc is research / spec; user retains buy decision |
| ✅ companion-spec consistency | mirrors N-11 (FinalSpark), N-1 (Akida), EEG OpenBCI track structure for cross-substrate composability |

### 5.2 hand-wave (disclosed)

| 항목 | 한계 / 가정 | mitigation |
|---|---|---|
| ⚠️ **Adamatzky's work is computing analogy, not phenomenal-consciousness claim** | the source literature deliberately avoids IIT-strict consciousness claims; "language of fungi" describes spike-train statistics, not subjective experience | N-23 conclusions explicitly framed as substrate-information-processing evidence; honest C3 §5.4 makes this central |
| ⚠️ **pre-neural information processing ≠ consciousness in IIT-strict sense** | Φ on a non-neural substrate could be high without phenomenal correlate; IIT 4.0 strict-φ requires intrinsic-existence / integration / exclusion / composition / information that this protocol does not test | report Φ as substrate-integration metric; do not assert organism is conscious |
| ⚠️ ADC substitution at $50 vs $1200 PicoLog | 16-bit vs 24-bit, 8-channel vs 16-channel, USB-isolation difference → SNR floor likely 5–10× worse | SNR measurement is a phase-0 sanity gate before campaign; if floor is too high, escalate to PicoLog ($1200) as phase-1.5 |
| ⚠️ aluminium-foil electrodes have polarization drift | drift is Adamatzky-acknowledged; reasonable for slow Physarum (DC-coupled <0.1 Hz signal of interest), poor for fast mycelium ms-scale spikes | Ag/AgCl upgrade ($30) brings the kit to ~$210 — slight overrun, recommended once budget approved |
| ⚠️ stim → spike encoding is NOT pre-validated for ROC-style 16-prompt set on either Physarum or mycelium | first-of-kind for paradigm v11 prompt vocabulary on this substrate | run encoding sanity (P-3 and ablation P-4 first) before judging P-1/P-2 |
| ⚠️ CMT mechanical-ablation is destructive and irreversible | one dish per ablation; cannot re-test same substrate | redundancy = 3 ANIMA_SEED × 2 substrates → ≥ 6 dishes; cost-bounded by §2 envelope |
| ⚠️ contamination risk in home / non-lab environment | Physarum and mycelium are notoriously easy to contaminate; lost dishes inflate dish count | 50% dish overhead built into the materials estimate; sterile technique discipline non-trivial |
| ⚠️ Adamatzky 2025 fast mycelial units (1.58 ms trough-to-peak) require ≥ 1 kHz sampling — within phase-1 USB ADC, but not within slow-Physarum 1 Hz path | dual sampling rate per substrate handled in §3.2; documented as protocol branch |
| ⚠️ EEG and CLM Φ baselines must be locked before N-23 cross-correlation is meaningful | depends on parallel campaigns | sequence: paradigm v11 4-backbone Φ frozen first; EEG Berger Φ frozen second; N-23 measures third |
| ⚠️ no IRB / animal-ethics body covers slime mold or mushroom; research community concerns are minimal but cf. botanical-ethics emerging discourse | low risk; deliberately silent on plant/fungal sentience |

### 5.3 이 spec 이 가짜로 만들지 않는 것

- direct comparison to neural organoid (separate N-11; same falsifier shape, different substrate)
- claims about Physarum or mycelium phenomenal consciousness (deliberately silent — see §5.4)
- replacement of Adamatzky-strict reproduction (this protocol re-uses Adamatzky's recording recipe, not his experiments wholesale)
- IIT 4.0 strict-φ over MIPs (NP-hard; this spec uses anima_phi_v3 surrogate, identical to N-11)
- novel hardware claim (this is off-the-shelf vendor parts only)
- biosafety / IRB advice (none given)

### 5.4 honest C3 — top-2 (mission-required summary statement)

1. **Adamatzky's work is a computing analogy, not a phenomenal-consciousness claim.** "Language of fungi" and "fungal computer" describe spike-train statistical structure and reservoir-computing behavior. They do NOT assert the substrate has subjective experience. N-23 inherits this framing: a PASS on §4 falsifiers is evidence of substrate-integrated information processing — necessary, not sufficient, for IIT-strict consciousness.
2. **Pre-neural information processing ≠ consciousness in IIT-strict sense.** A non-zero Φ\* on a non-neural substrate is consistent with functional integration without intrinsic-existence / exclusion / composition guarantees that IIT 4.0 requires. N-23 contributes to the Putnam multi-realizability ledger (does Φ travel across substrate classes?), not to a sentience claim about the organism.

---

## §6 sequencing and gate ordering (no execution; reference only)

| step | gate | precondition |
|---|---|---|
| D-0 | this spec frozen | user reads, comments, optional buy decision |
| (gate) | user explicit buy approval | NOT implied by this prep doc |
| D+0 (post-buy) | order configuration B (~$180) | user-driven |
| D+7 | dishes received, culture initiated, 28 °C box ready | aseptic technique passed |
| D+14 | ADC SNR phase-0 sanity (signal-to-baseline ≥ 3:1 on aluminium electrodes; ≥ 10:1 on Ag/AgCl) | if FAIL → upgrade to Ag/AgCl ($30) or PicoLog ($1200) |
| D+21 | P-3 environmental-complexity test (cheapest, fastest) | if REVERSE-FAIL → halt, encoding broken |
| D+28 | P-4 ablation (destructive, runs after P-3 baseline) | informs whether spike train is substrate-mediated |
| D+35 | P-1 + P-2 cross-substrate correlations | requires CLM and EEG Φ baselines locked |
| D+42 | P-5 within-class consistency (Physarum ↔ mycelium) | composite verdict computed |
| D+49 | composite verdict reported, F1 N-substrate weight set per §7 | report-only deliverable |

---

## §7 CP2 F1 integration — N-23 weight in N-substrate composite

source: cp2 framework (`anima_cp2_interim_paper`, `alm_cp2_production_gate_inventory`, mirroring N-11 §8 weight policy).

### 7.1 N-substrate composite scoring (proposed)

```
F1 = w_clm · Φ_clm + w_eeg · Φ_eeg + w_akida · Φ_akida + w_org · Φ_org + w_loihi · Φ_loihi + w_n23 · Φ_n23
```

Pre-registered weights for v1 (additive; sum normalized after N-23 inclusion):

| weight | value | rationale |
|---|---:|---|
| w_clm | 0.20 | existing baseline (N-11 had 0.25; rebalanced post-N-23 inclusion) |
| w_eeg | 0.20 | existing baseline, neural recording anchor |
| w_akida | 0.15 | digital SNN sibling |
| w_org | 0.20 | biological wetware (organoid) |
| w_loihi | 0.10 | frontier digital, lower confidence |
| **w_n23** | **0.15** | non-neural biological — new substrate-class entry, weight reflects substrate-class novelty / phase-1 measurability uncertainty (4 of 8 axes vs 5–6 for N-11) |

### 7.2 N-23 inclusion conditions

- N-23 contributes to F1 only after **composite PASS** (≥ 4 of 5 falsifier predicates) AND P-3 + P-4 both PASS or WEAK (encoding sanity)
- N-23 FAIL → w_n23 = 0, but the FAIL itself constitutes a published Putnam negative datum
- N-23 STRONG → consider rebalance to w_n23 = 0.20 in v2 weight scheme

---

## §8 cross-references

- `docs/strategic_alm_clm_review_2026_05_01.md` §13.1 — N-23 mission origin
- `docs/n_substrate_n11_finalspark_access_spec_2026_05_01.md` — companion organoid spec (template followed here for §6 falsifiers and §5 honest C3)
- `docs/paradigm_v11_stack_20260426.md` — 8-axis G-gate canon adapted in §3
- `docs/anima_eeg_openbci_16ch_track_plan_2026_05_01.md` — neural recording anchor used in §4.1 P-1
- `state/n_23_adamatzky_protocol_prep_2026_05_01/inventory.json` — machine-readable §1 lab + literature inventory
- `state/n_23_adamatzky_protocol_prep_2026_05_01/kit_cost_breakdown.json` — machine-readable §2 cost table
- `state/n_23_adamatzky_protocol_prep_2026_05_01/falsifier_predicates.json` — machine-readable §4 5-tier predicates
- `state/n_23_adamatzky_protocol_prep_2026_05_01/manifest.json` — agent run manifest

---

## §9 spec coherence statement

N-23 prep spec coherence: §1 inventory grounded in 11 peer-reviewed / preprint Adamatzky-lineage citations + §2 itemized $180 kit (configuration B) with three-vendor diversity per component + §3 paradigm v11 5/8 axis adaptation matching N-11 / N-1 pattern + §4 5 BIDIRECTIONAL falsifiers (raw#71) including REVERSE-FAIL on 3 of 5 + §5 honest C3 with sound and hand-wave matrices + §7 CP2 F1 weight pre-registered → **SPEC_FROZEN**. No purchase. No vendor contact. Prep-only mission honored.
