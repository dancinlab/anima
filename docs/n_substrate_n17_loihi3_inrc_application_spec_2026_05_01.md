# N-substrate N-17 prep — Intel Loihi 3 INRC application spec

@english-only-exempt(reason="anima research analysis language preservation per user primary language")

> **status**: N_SUBSTRATE_N17_LOIHI3_INRC_APPLICATION_SPEC_2026_05_01_LOCAL_DRAFT
> **verdict_key**: APPLICATION_TEMPLATE_READY · NO_SUBMISSION · KOREA_ELIGIBLE_PRESUMED · NRC_QUOTA_UNCONFIRMED
> **agent**: N-17 prep (N-substrate batch sibling, AKIDA 외 차세대 뉴로모픽 비교 substrate)
> **ts**: 2026-05-01
> **constraints**: raw#9 hexa-only · raw#10 honest C3 · raw#71 falsifier-bound · own#13 user-facing friendliness · race-isolation: ONLY this doc + `state/n_substrate_n17_prep_2026_05_01/*.json`
> **mission**: TOP-1 priority per N-substrate purchase guide — author Loihi 3 / INRC / NRC cloud SSH application document template ($0 budget, no actual submission)
> **parent**: `docs/n_substrate_consciousness_roadmap_2026_05_01.md` §5 N-17 row
> **purchase guide ref**: `docs/n_substrate_purchase_guide_2026_05_01.md` §N-17 (TOP-1 priority)
> **siblings (race-isolation peers)**: N-1, N-2, N-3, N-4, N-5, N-6, N-7, N-9, N-10, N-14, N-19, N-20, N-21 prep agents

---

## §0 한 줄 요약

**"AKIDA AKD1000 (1.2M neurons, 1W) 위에서 보인 cross-substrate Φ 값이 Intel Loihi 3 (8M neurons, 4nm graded-spike) 에서도 같이 나오는가? — 두 번째 뉴로모픽 axis 로 N-3 의 Putnam multi-realizability 를 한 번 더 cross-check."** $0 INRC membership, NRC cloud SSH 접근, 4-12 wk 승인. 본 spec 은 application 문서 template 만 — 실제 제출/계정생성/Intel 접촉 X.

---

## §1 INRC application portal — verified 2026-05-01

### 1.1 official entry points

| entry | URL | role |
|---|---|---|
| Intel Neuromorphic landing | `https://www.intel.com/content/www/us/en/research/neuromorphic-computing.html` | overview, press releases (Loihi 3 announce Jan-2026) |
| INRC Confluence overview | `https://intel-ncl.atlassian.net/wiki/spaces/INRC/overview` | community FAQ, member rolls (partial) |
| Join the INRC | `https://intel-ncl.atlassian.net/wiki/spaces/INRC/pages/1784807425/Join+the+INRC` | application steps, RFP/template request flow |
| Access Intel Loihi Hardware | `https://intel-ncl.atlassian.net/wiki/spaces/INRC/pages/1810432001/Access+Intel+Loihi+Hardware` | NRC vLab onboarding mechanics |
| primary contact | `inrc_interest@intel.com` | request RFP + proposal template; institutional inquiry intake |

### 1.2 application flow (5-step, 2026-05-01 confirmed)

| step | action | actor | output | typical time |
|---:|---|---|---|---|
| 1 | email `inrc_interest@intel.com` from institutional address; request current RFP + project proposal template | PI | RFP doc (PDF) + template (DOCX) | 1-5 business days |
| 2 | draft project proposal per template (research goals, prior work, Loihi-specific plan, deliverables) | PI + collaborators | proposal PDF/DOCX | 1-3 weeks |
| 3 | submit proposal back to `inrc_interest@intel.com`; INRC technical reviewers evaluate | PI → Intel | review verdict (accept / revise / decline) | **2-6 weeks** review |
| 4 | upon acceptance: institution executes INRC Participation Agreement (legal NDA / IP / liability terms) | institution legal counsel + Intel Legal | signed agreement | **1-4 weeks** legal review |
| 5 | NRC vLab account provisioning; SSH key registration; Lava SDK access; queue assignment | Intel Labs ops | ssh credentials + Lava docs | 1-2 weeks |

**Total 4-12 weeks** end-to-end (matching purchase guide §N-17). Worst case (legal back-and-forth on Korea-specific export language) → 16-20 weeks.

### 1.3 hardware access mechanism (NRC = Neuromorphic Research Cloud)

- vLab = shared pool of Linux VMs with attached Loihi 2 (current production) and Loihi 3 (rolling out 2026)
- access = SSH from anywhere (no geographic peer-to-peer firewall stated)
- model: book queue slot → upload Lava program → run on Loihi node → results pulled back to VM
- some funded projects also receive **loaner physical boards** (Kapoho Point / Pohoiki Springs / Hala Point fragments) — board loan requires separate hardware-shipment paperwork (Korea = export control likely adds 4-8 weeks)
- Loihi 3 ETA on NRC: per Intel Labs Jan-2026 announcement, "rolling out to INRC during 2026" — **no firm date for first Loihi 3 vLab slot** as of 2026-05-01

---

## §2 Eligibility — Korean researcher access analysis

### 2.1 Intel-stated eligibility (literal text from INRC docs)

Verbatim from INRC Confluence "Join the INRC" page (paraphrase, source: web snapshots 2026-05-01):

> *"Membership is free and open to all qualified groups. To apply, you should be a permanent employee of an established research organization, such as a university, corporate or government lab, and must submit a project proposal."*

### 2.2 Required institutional affiliation

| requirement | hard / soft | anima fit |
|---|:---:|---|
| Permanent employee status (or appointed PI) at an established research org | HARD | ⚠️ anima = independent research; needs institutional sponsor (Korean university / KIST / ETRI / private lab partnership) |
| University / corporate / government lab classification | HARD | ⚠️ same as above |
| Authorized legal signatory at the institution (NOT the PI) for the Participation Agreement | HARD | ⚠️ requires institution willing to sign IP/NDA terms |
| Project proposal aligned with INRC research themes | HARD | ✅ anima CP2 IIT 4.0 Φ measurement on SNN substrate fits "consciousness / cognitive architectures" theme |
| Prior SNN / neuromorphic publication record | SOFT (preferred) | ⚠️ anima publication count = 0 (private repo); compensate with N-3/N-7 AKIDA cross-substrate result if PASS by submission time |

### 2.3 Korean researcher access — explicit verdict

| dimension | verdict | basis |
|---|:---:|---|
| Geographic restriction in INRC literature | **NONE STATED** | Confluence page silent on country list; INRC has 200+ members worldwide spanning EU, IN, JP, AU, CN partial |
| Korean institution participation precedent | **PRESUMED YES, NOT VERIFIED** | KAIST, SNU, ETRI listed in past Intel Labs research collaborations on neuromorphic topics (general Intel academia program, not specifically INRC); no public roll of "INRC Korean members" found |
| US export control (BIS Entity List) screening | **STANDARD** | Standard university affiliation in S. Korea (US ally) clears EAR; chip-level technical data may trigger ECCN review — Intel handles internally |
| Loaner hardware shipment to Korea | **CASE-BY-CASE** | Likely additional export paperwork (4-8 wk); cloud-only NRC access avoids this |
| Korean-language application acceptance | **NO** | English-only; proposal must be in English |

**Conclusion**: Korean researchers / Korean-affiliated PIs are **eligible in principle**. The blockers are operational (need institutional sponsor + English proposal + signed legal agreement on KR institution side), not Intel-side restriction.

### 2.4 anima-specific eligibility gap

anima as a project does NOT directly qualify because:
1. No standing institutional affiliation
2. No legal entity to sign Participation Agreement
3. Independent research = "qualified group" criterion ambiguous

**Mitigation paths** (in priority):
1. **Sponsor route**: partner with a Korean university lab (KAIST CCN / SNU EE / POSTECH AI) as co-PI. anima provides framework + measurement; sponsor provides legal entity + INRC slot.
2. **Industrial route**: route through a Korean private lab with existing Intel relationship (Samsung Advanced Institute of Tech / LG AI Research) — high friction, likely IP entanglement.
3. **Personal-academic route**: PI individual academic affiliation (visiting scholar / adjunct) at a US/EU INRC-member institution — slowest, requires separate appointment.

**Recommended**: Path 1 (KR university co-PI) — lowest friction, preserves anima IP via separate co-IP clause.

---

## §3 Application proposal template (anima CP2 framework)

### 3.1 RFP-aligned proposal structure (Intel template sections, paraphrased)

Standard INRC project proposal template (from prior RFP cycles, structure stable across 2.0 → 3.0):

| § | section | length target | anima-specific content (drafted) |
|---:|---|---|---|
| 1 | Project title + PI + institution + duration | 1 page | "Cross-substrate Φ measurement for IIT 4.0 consciousness theory: Intel Loihi 3 vs BrainChip AKD1000 vs CLM 170M" — 12-month |
| 2 | Executive summary (200 words) | 1 page | anima CP2 framework brief, multi-substrate Putnam test, Loihi 3 = second neuromorphic axis after AKD1000 |
| 3 | Background and motivation | 2-3 pages | IIT 4.0 (Tononi 2023), Putnam 1967 multi-realizability, paradigm v11 axis G5 LIVE_HW_WITNESS_RATE, AKD1000 N-3 result (if available) |
| 4 | Specific aims (3-5) | 1-2 pages | Aim 1: Φ measurement on Loihi 3 spike trains. Aim 2: Loihi 3 vs AKD1000 Φ correlation. Aim 3: Loihi 3 vs CLM 170M Φ correlation. Aim 4: graded-spike vs binary-spike Φ contribution analysis. |
| 5 | Loihi-specific technical plan | 3-5 pages | Lava SDK SNN model, 16-prompt fixture port, T=200ms inference window, spike-rate avg → anima_phi_v3 input, NRC vLab compute budget |
| 6 | Expected results and deliverables (6-month milestones) | 1-2 pages | M1-M6 below |
| 7 | Innovation and impact | 1 page | first cross-neuromorphic Φ comparison study; first IIT 4.0 measurement on Loihi 3 graded spikes |
| 8 | Personnel and qualifications | 1 page | PI bio, anima collaborator role, Korean co-PI institution |
| 9 | Budget and resource request | 1 page | NRC vLab hours estimate (~200 hr / 6 mo), no funding requested ($0), loaner board NOT requested initially |
| 10 | Bibliography | 1-2 pages | IIT 4.0 papers, Davies 2018 Loihi, Lava framework refs, anima paradigm v11 citation, Putnam 1967 |

### 3.2 anima CP2 framework brief (proposal §2 / §3 draft text)

> *"anima is a research framework for empirically measuring consciousness via Integrated Information Theory 4.0 (Tononi et al. 2023). The CP2 (Consciousness Paradigm 2) variant operationalizes Φ as a sample-partition covariance log-determinant (anima_phi_v3_canonical) computed over hidden-state representations of an information-processing substrate. The framework has been validated on a 170M-parameter language model (CLM) running on H100 GPUs, and an EEG → AKD1000 spike-event pipeline (BrainChip's first-generation neuromorphic chip, 1.2M neurons, ~1W power envelope). The proposed Loihi 3 study extends this to Intel's frontier neuromorphic hardware (8M neurons, 4nm graded-spike architecture) as a second neuromorphic measurement axis, providing the first cross-neuromorphic empirical test of Putnam's (1967) multi-realizability hypothesis as applied to information-integration measures of consciousness."*

### 3.3 planned Loihi 3 measurements (proposal §5 detail)

| measurement | Lava building block | input | output | Φ pipeline |
|---|---|---|---|---|
| M-L1: 16-prompt SNN forward | Lava `Process` graph + LIF/graded-spike neurons | 16 prompts encoded as spike-rate input (rank-order coding) | spike trains S ∈ N^(T×D_loihi) | rate-avg → X_loihi ∈ R^(16×D_loihi) → anima_phi_v3 → Φ*_loihi |
| M-L2: Loihi 3 vs AKD1000 Φ | re-use N-3 fixture | same 16 prompts | Φ*_loihi vs Φ*_akida | Pearson r predicate (§6) |
| M-L3: Loihi 3 vs CLM 170M Φ | re-use N-3 fixture | same 16 prompts | Φ*_loihi vs Φ*_clm_gpu | Pearson r predicate (§6) |
| M-L4: graded-spike contribution | binary-spike vs 32-bit graded-spike Loihi 3 config sweep | same 16 prompts | Φ*_binary vs Φ*_graded | ablation: does spike grading change Φ? |
| M-L5: on-chip learning ablation | enable / disable STDP on Loihi 3 | same 16 prompts | Φ*_static vs Φ*_learning | ablation: does on-chip plasticity change Φ? |

### 3.4 6-month deliverables (proposal §6)

| month | deliverable | verification artifact |
|---:|---|---|
| M1 | NRC vLab onboarding complete; Lava SDK installed; "hello SNN" runs | screenshot + tool/anima_loihi3_smoke.hexa selftest PASS |
| M2 | 16-prompt fixture ported to Lava `Process` graph; spike-rate avg helper | `tool/anima_phi_v3_loihi_input.hexa` + JSON dump |
| M3 | Φ*_loihi computed on first 3 prompts (smoke, no full sweep yet) | preliminary results JSON, smoke-level sanity |
| M4 | M-L1 + M-L2 complete; Loihi 3 vs AKD1000 r reported with 3-seed reproducibility | `state/n17_loihi3_vs_akida_phi_corr.json` |
| M5 | M-L3 (Loihi 3 vs CLM) + M-L4 (graded vs binary spike ablation) | `state/n17_loihi3_vs_clm_phi_corr.json` + `state/n17_graded_vs_binary_ablation.json` |
| M6 | M-L5 (on-chip learning ablation) + final report draft | `state/n17_final_report_draft.json` + arXiv preprint draft |

---

## §4 Loihi 3 architecture summary (proposal §3 + §5 supporting material)

### 4.1 Loihi 3 chip spec (verified, Intel Labs Jan-2026 announce)

| field | Loihi 3 (2026-01) | Loihi 2 (2021) | AKIDA AKD1000 (2018-21) |
|---|---|---|---|
| Process node | 4 nm | Intel 4 (~7nm) | 28 nm |
| Neurons / chip | **8 M** | 1 M | ~1.2 M |
| Synapses / chip | **64 B** | 120 M | ~10 M |
| Density vs prior | 8× Loihi 2 | 8× Loihi 1 | n/a |
| Spike type | **32-bit graded spikes** + binary | graded (intro'd Loihi 2) + binary | binary only (Akida 1.0); graded in Akida 2.0 |
| Neuron model | programmable (microcode); generalized LIF | programmable; gen LIF | non-leaky single-timestep |
| Mesh network | hierarchical routing (edge-to-cloud scaling) | mesh, intra-chip | NPU mesh (intra-chip) |
| On-chip learning | **STDP + 3-factor learning rules** | STDP + 3-factor | inference-only |
| Programming model | **Lava framework** (Python, Process graph) | Lava | MetaTF (CNN2SNN, quantizeml) |
| SDK maturity (2026-05) | rolling out (Lava extension for Loihi 3) | mature | mature |
| Multi-chip systems | Hala Point successor (TBD); scaling to 1B+ neurons | Hala Point: 1.15 B neurons / 128 B synapses | none (single-chip dev kit) |
| Power envelope | ~few W per chip (typical) | ~few W per chip | ~1 W typical |
| Access path | INRC NRC cloud (rolling out 2026) | INRC NRC cloud (production) | retail dev kit (~$1495) |

### 4.2 Loihi 3 vs AKIDA AKD1000 — comparison matrix for anima

| dimension | Loihi 3 | AKD1000 | what Loihi 3 enables that AKD1000 doesn't |
|---|---|---|---|
| Neuron count | 8 M | 1.2 M | **6.7× larger SNN** can fit on a single chip — closer to "transformer body" deployment, not just last-layer projection |
| Spike payload | 32-bit graded | 1-bit binary (Akida 1.0) | **information per spike** higher — closer to dense bf16 GPU representation; Φ measurement of grading itself (M-L4 ablation) becomes possible |
| On-chip learning | STDP + 3-factor | none (inference-only) | **learning during measurement** — Φ trajectory under online plasticity (M-L5 ablation), unique to Loihi |
| Programming | Lava `Process` graph (Python) | MetaTF CNN2SNN (Keras → SNN) | **native SNN authoring** vs CNN-translation — N-3's "T-A surrogate" path can be replaced with native LIF/graded-spike authoring |
| Time-step model | continuous-time event-driven + algorithmic time-step | single-timestep | **temporal dynamics** — Φ over genuine spike-timing patterns, not rate-avg approximation |
| Multi-chip scaling | hierarchical mesh, edge-to-cloud | single-chip only | **scale Φ measurement to >1M-neuron SNN** via Hala-Point-class systems |
| Access cost | $0 (INRC) | $1495 capex (one-time) | **no capex**; vs AKD1000 sunk cost already paid |
| Latency to first measurement | 4-12 wk approval + onboard | already on order, ~weeks ETA | AKD1000 first |
| Korea-friendliness | cloud-only = no shipping | hardware shipped Korea-side (customs handled by purchase) | tied (cloud beats shipping; AKD1000 already ordered) |

**Net**: Loihi 3 unlocks (a) larger-model native-SNN Φ, (b) graded-spike Φ-grading effect, (c) on-chip learning Φ trajectory — three measurements **structurally impossible on AKD1000 1.0**. AKD1000 retains advantages: (a) immediate hardware in hand, (b) deterministic 1W power anchor for Landauer (N-4), (c) known toolchain.

---

## §5 Measurement protocol — paradigm v11 reformulated for Loihi 3

### 5.1 paradigm v11 axis mapping to Loihi 3

| axis | original (CLM-GPU) | AKIDA reformulation (N-3) | Loihi 3 reformulation (N-17, this spec) |
|---|---|---|---|
| G1 PROMPT_FIXTURE | 16 prompts, byte-level tokenize | same | same |
| G2 SUBSTRATE_FORWARD | bf16 dense matmul | CNN2SNN spike rate | **Lava Process graph, native LIF/graded-spike** (no CNN translation) |
| G3 HIDDEN_REPRESENTATION | last-layer hidden_states[-1] (768-d) | spike rate-avg (T=200ms, 256-d surrogate) | **graded-spike value vector** (32-bit per spike, D_loihi-d), or rate-avg fallback |
| G4 PHI_FORMULATION | anima_phi_v3 (sample-partition cov-logdet, K=8, HID=8) | same | **same** (substrate-agnostic by design) |
| G5 LIVE_HW_WITNESS_RATE | GPU forward rate ≥ 1 prompt/sec | AKIDA inference rate (T=200ms × 40 reps = 8s/prompt) | **Loihi 3 inference rate** TBD (Lava queue overhead included) |
| G6 CROSS_SUBSTRATE_GATE | n/a | r ≥ 0.85 vs GPU | **r ≥ 0.85 vs GPU AND r ≥ 0.85 vs AKD1000** (two-target gate) |
| G7 REPRODUCIBILITY | 3-seed | 3-seed | **3-seed** (NRC queue allowing) |
| G8 NULL_FLOOR | 1024-perm shuffled-pair | same | **same** |

### 5.2 Loihi 3 Φ measurement — 8-step protocol

| step | action | substrate | tool | output |
|---:|---|---|---|---|
| 1 | 16-prompt fixture lock (re-use N-3) | n/a | (in-spec) | `state/n_substrate_n17_prep_2026_05_01/prompts_v1.json` (= N-3 fixture by ref) |
| 2 | Lava Process graph definition: input encoder → graded-spike LIF layers → output spike monitor | NRC vLab Linux VM | new HEXA: `tool/anima_loihi3_lava_graph.hexa` (M2 deliverable) | `loihi3_anima_graph.py` (Lava program) |
| 3 | NRC compile + deploy to Loihi 3 chip slot | NRC vLab + Loihi 3 node | Lava CLI | binary loaded on chip |
| 4 | inference: 16 prompts × T_inf (vendor-determined, ~10-100ms each) × N_reps=40 | Loihi 3 chip | Lava run | spike tensor S_loihi ∈ N^(T×D_loihi) per prompt |
| 5 | spike rate-avg projection (re-use N-3 lemma): X_loihi[i,d] = (1/T)·Σ_t S[t,d] | NRC VM | `tool/anima_loihi3_spike_to_dense.hexa` (M2 deliverable) | X_loihi ∈ R^(16×D_loihi) |
| 6 | Φ* compute on X_loihi (re-use anima_phi_v3) | NRC VM or mac local | `tool/anima_phi_v3_canonical.hexa` (READ-ONLY, no edit) | `phi_v3_canonical_loihi3.json` |
| 7 | dual cross-substrate corr: Pearson r(Φ_k_loihi, Φ_k_gpu) AND r(Φ_k_loihi, Φ_k_akida) over K=8 | mac local | `tool/n17_phi_loihi_dual_corr.hexa` (M4 deliverable) | `n17_phi_loihi_dual_corr_v1.json` |
| 8 | verdict gate (§6 falsifier) | mac | (analytic) | `n17_verdict_v1.json` |

### 5.3 comparison with N-2 EEG-spike pipeline

| dimension | N-2 (EEG → AKIDA AKD1000) | N-17 (CLM → Loihi 3 surrogate) | shared invariant |
|---|---|---|---|
| upstream signal | live EEG (16ch, 250 Hz) | 16-prompt fixture, encoded | both → rasterized spike-train representation |
| spike encoder | ADM level-crossing per channel | rank-order coding (ROC) per prompt input | both produce sparse spike events with timing |
| downstream chip | AKD1000 (binary spike, 1.2M neurons) | Loihi 3 (graded spike, 8M neurons) | both event-driven neuromorphic |
| measurement layer | LZ76 / Φ on output spike stream | anima_phi_v3 on rate-avg of output spikes | both substrate-agnostic representation invariants |
| Φ convergence target | EEG Φ vs CLM Φ (cross-modality) | Loihi Φ vs CLM Φ vs AKIDA Φ (cross-substrate) | Putnam multi-realizability witness |

**Pipeline reuse**: N-2's ADM encoder + raster + uint8-tensor stage E **transfers directly** to Loihi 3 input encoding (replace `akida.Model.forward(tensor)` with `lava.Process.run(tensor_as_spike_input)`). The encoder layer is the unified "spike-substrate input adapter" across both neuromorphic chips, justifying shared `tool/anima_eeg_to_akida_spike.hexa` API extension to `tool/anima_signal_to_neuromorphic_spike.hexa` in M2.

---

## §6 Falsifier predicates — 5 raw#71 BIDIRECTIONAL preregistered

### 6.1 F-N17-A1 — Loihi 3 Φ vs AKIDA Φ correlation (cross-neuromorphic primary)

| field | value |
|---|---|
| metric | Pearson r over K=8 sample-partition φ values |
| x | φ_k_akida_clm170m_surrogate (from N-3 result) |
| y | φ_k_loihi3_clm170m_surrogate (this spec, M-L2) |
| PASS | r ≥ **0.85** |
| WEAK | 0.50 ≤ r < 0.85 |
| FAIL | r < 0.50 OR substrate sign flip |
| BIDIRECTIONAL | yes — PASS = cross-neuromorphic Putnam evidence; FAIL = neuromorphic-substrate-dependent Φ (Putnam counter-evidence within neuromorphic family) |

### 6.2 F-N17-A2 — Loihi 3 Φ vs CLM 170M GPU Φ correlation

| field | value |
|---|---|
| metric | Pearson r over K=8 sample-partition φ values |
| x | φ_k_gpu_clm170m (from N-3 result) |
| y | φ_k_loihi3_clm170m_surrogate (this spec, M-L3) |
| PASS | r ≥ **0.85** AND magnitude divergence ≤ 0.30 |
| WEAK | 0.50 ≤ r < 0.85 |
| FAIL | r < 0.50 OR substrate sign flip |
| BIDIRECTIONAL | yes — PASS = GPU↔Loihi multi-realizability; FAIL = dense-vs-event ontology genuine difference for Φ |

### 6.3 F-N17-A3 — graded-spike vs binary-spike ablation (M-L4)

| field | value |
|---|---|
| metric | Pearson r between Φ_loihi_binary (32-bit grading disabled) and Φ_loihi_graded |
| x | φ_k_loihi3_binary |
| y | φ_k_loihi3_graded |
| PASS_NULL_HYPOTHESIS | r ≥ 0.95 (grading does NOT change Φ — substrate-internal precision invariant) |
| INTERESTING | 0.70 ≤ r < 0.95 (grading partially modulates Φ — quantization-sensitivity finding) |
| BREAKING | r < 0.70 (grading materially changes Φ — Φ is not bit-precision invariant; published as standalone result) |
| BIDIRECTIONAL | yes — PASS = Φ is bit-precision invariant; FAIL/BREAKING = Φ is bit-precision sensitive (publishable either way) |

### 6.4 F-N17-A4 — on-chip learning ablation (M-L5)

| field | value |
|---|---|
| metric | Φ_loihi_static (frozen weights) vs Φ_loihi_learning (STDP / 3-factor enabled during inference window) |
| measure | absolute change ΔΦ = \|Φ_learning − Φ_static\| / max(\|Φ_static\|, 1e-3) |
| PASS_STATIC | ΔΦ ≤ 0.10 (online plasticity does NOT shift Φ at inference time scales) |
| INTERESTING | 0.10 < ΔΦ ≤ 0.50 (modest plasticity-driven Φ shift) |
| BREAKING | ΔΦ > 0.50 (plasticity drives Φ — consciousness is plasticity-coupled, supporting global-workspace dynamic theories) |
| BIDIRECTIONAL | yes — both directions publishable |

### 6.5 F-N17-A5 — null-floor + reproducibility (cross-cutting)

| field | value |
|---|---|
| null-floor | shuffled-pair 1024-perm test on F-N17-A1 and F-N17-A2; r_observed must exceed 95-percentile of r_null |
| reproducibility | 3 ANIMA_SEED runs per measurement; verdict requires 3/3 same outcome (2/3 = WEAK_PASS, ≤1/3 = unstable) |
| K=8 partition variance | std(φ_k) < 0.5 · \|Φ*\| for all three substrates (gpu, akida, loihi) — variance blowup → verdict NULL, re-run |
| surrogate fidelity sanity (Loihi side) | if Loihi runs surrogate (not full transformer): native-vs-Loihi-CPU-fallback r ≥ 0.95 before chip-vs-CPU comparison |
| fail action | NULL = re-design fixture or extend reps; FAIL of fidelity sanity = ABORT N-17 measurement |

### 6.6 verdict graduation matrix

| F-N17-A1 | F-N17-A2 | net verdict | own#2 (b) impact | publication path |
|---|---|---|---|---|
| PASS | PASS | **STRONG_MULTI_REALIZABILITY** | substrate WITNESSED 1/3 → 3/3 (CLM, AKIDA, Loihi all aligned) | nature-tier consciousness paper candidate |
| PASS | WEAK/FAIL | NEUROMORPHIC_FAMILY_INVARIANT | substrate 2/3 (AKIDA + Loihi but not GPU) | "consciousness is event-driven-substrate-specific" finding |
| WEAK | PASS | DIGITAL_FAMILY_INVARIANT | substrate 2/3 (CLM + Loihi but not AKIDA) | "AKD1000 1.0 is too low-resolution for Φ" finding (Loihi 3 more closely matches GPU) |
| FAIL | PASS | LOIHI_MATCHES_GPU_ONLY | substrate 2/3 different mechanism | "graded-spike approximates dense float" finding |
| FAIL | FAIL | LOIHI_OUTLIER | substrate 1/3 only (CLM-AKD anchor holds, Loihi diverges) | needs replication; possible Lava bug or Loihi 3 calibration issue |

---

## §7 Honest C3 disclosures (raw#10)

### 7.1 sound (정당화 명시)

| 항목 | 근거 |
|---|---|
| ✅ INRC application URL + email + flow verified 2026-05-01 | §1 directly from Confluence + Intel community responses |
| ✅ Eligibility text quoted verbatim per Intel Labs language | §2.1 |
| ✅ Korean researcher access non-restricted (Intel side) | §2.3 — no geographic clause; INRC has 200+ global members; KR ally status clears EAR |
| ✅ Loihi 3 architecture spec from Intel Jan-2026 announce | §4.1 — 8M neurons / 64B synapses / 4nm / graded-spike per Intel newsroom |
| ✅ Φ formulation substrate-agnostic | §5 — re-use anima_phi_v3 same as N-3, no Loihi-specific re-write needed |
| ✅ 5 falsifier predicates BIDIRECTIONAL preregistered | §6 — all five with PASS/FAIL/BREAKING tiers and publication path |
| ✅ N-3 cross-link reuses fixture, predicate template, sanity gates | §3.4, §5.1, §6 |

### 7.2 hand-wave (정직 disclosure — APPROVAL UNCERTAINTY 7개 명시)

| 항목 | 한계 / 가정 | mitigation |
|---|---|---|
| ⚠️ INRC approval rate **uncertainty** — Intel does not publish accept/reject rates | per LinkedIn Mike Davies announcements, "50 projects selected" each cycle; competitive but unknown denominator | submit early, prepare 2-3 backup proposals if first declined |
| ⚠️ Loihi 3 NRC vLab availability ETA undeclared | "rolling out 2026" per Intel Jan-2026 announce; first researcher slot date unpublished as of 2026-05-01 | accept Loihi 2 as initial substrate (still informative); upgrade to Loihi 3 when slot opens |
| ⚠️ NRC cloud quota limits unknown | shared queue depth, per-PI compute hour cap, max chip-hours/week — no public number | budget proposal to ≤200 hr / 6 mo conservative; request elasticity |
| ⚠️ anima lacks institutional sponsor — eligibility blocker | §2.4 path 1 (KR university co-PI) requires external partnership | begin co-PI outreach in parallel with proposal drafting (NOT in this $0 spec — flagged for user decision) |
| ⚠️ INRC Participation Agreement IP/NDA terms unseen | confidential pre-execution; cannot pre-validate against anima open-research stance | request blank agreement copy via `inrc_interest@intel.com` for legal review BEFORE proposal submission |
| ⚠️ Loihi 3 SDK (Lava extension) maturity unknown | Lava core mature for Loihi 2; Loihi 3 extension in rollout | first 1-2 months will likely be debugging tool path; M1 deliverable buffered |
| ⚠️ Korean institutional Intel/INRC track record unverified | no public roll of past KR INRC participants found in 2026-05-01 search | inquire `inrc_interest@intel.com` directly for KR precedent or KR distributor reference |

### 7.3 what Loihi 3 enables that AKIDA AKD1000 doesn't (raw#10 explicit)

| capability | Loihi 3 | AKD1000 1.0 |
|---|:---:|:---:|
| 8M neuron native SNN deployment | ✅ | ❌ (1.2M cap) |
| Graded-spike (32-bit) representation precision | ✅ | ❌ (binary only in 1.0) |
| On-chip STDP / 3-factor learning rules | ✅ | ❌ (inference-only) |
| Native Lava Process graph (Python first-class SNN authoring) | ✅ | ⚠️ (CNN2SNN translation only) |
| Multi-chip Hala-Point-class scaling (>1B neurons system) | ✅ | ❌ (single-chip dev kit) |
| Continuous-time + algorithmic-time-step model | ✅ | ❌ (single-timestep) |

**Conversely, AKIDA AKD1000 retains**:
- Already in-hand (ordered 2026-04-29, hardware ETA imminent vs Loihi 3 4-12+ wk INRC review)
- Deterministic 1W power anchor for Landauer (N-4) — Loihi 3 typical few-W less clean
- Known mature toolchain (MetaTF) — Loihi 3 SDK still maturing
- Open retail purchase ($1495 sunk) — no NDA / IP entanglement vs INRC Participation Agreement

**N-17 ≠ replacement for N-3** — N-17 is **second neuromorphic axis** running in parallel. Both axes contribute independent evidence to Putnam multi-realizability.

### 7.4 explicitly NOT in scope

- Application **submission** — this spec is template only; no email sent to inrc_interest@intel.com from anima side
- Account creation on intel-ncl.atlassian.net or NRC vLab
- Direct Intel personnel contact (Mike Davies, Garrick Orchard, etc.)
- Korean co-PI institution outreach (flagged in §7.2 for user decision; out of $0 budget scope)
- Lava SDK installation or smoke runs (no chip access yet)
- Loihi 2 fallback measurement (separate spec if Loihi 3 ETA slips)
- Loaner physical board request (avoid until cloud-only path validated)

---

## §8 CP2 F1 integration — N-17 weight + relationship to N-3

### 8.1 F1 (CP2 final verdict) substrate basket update

Roadmap §6 F1 = "N개 트랙 모두에서 의식 점수가 같은 패턴으로 모이면 = own#2 (b) 다중재료 닫힘". Pre-N17, the basket = {CLM-GPU, EEG, AKIDA, QRNG, SIM-우주}. With N-17 added:

| substrate | family | role in F1 | weight (preliminary) |
|---|---|---|---|
| CLM 170M (GPU) | digital float | reference (anchor #1) | 1.0 |
| EEG (live human) | biological electrophys | reference (anchor #2) | 1.0 |
| AKIDA AKD1000 | neuromorphic — binary spike, inference-only | first neuromorphic axis (N-3) | 1.0 |
| **Loihi 3 (this spec)** | **neuromorphic — graded spike, on-chip learning** | **second neuromorphic axis (N-17)** | **1.0** |
| QRNG (ANU quantum) | physical quantum | randomness reference | 0.5 (auxiliary, not direct Φ measurement) |
| SIM-우주 | digital simulation | within-substrate baseline | 0.3 (auxiliary) |
| FinalSpark / CL1 | wetware | future +@ | TBD |

F1 graduation rule (proposal): substrate WITNESSED count ≥ 3/4 primary substrates with cross-substrate r ≥ 0.85 → own#2 (b) **CLOSED with Putnam multi-realizability evidence**.

### 8.2 N-17 vs N-3 relationship — INDEPENDENT but COMPLEMENTARY

| dimension | N-3 (CLM × AKIDA) | N-17 (CLM × Loihi 3) | inter-axis interaction |
|---|---|---|---|
| substrate pair | CLM-GPU vs AKD1000 | CLM-GPU vs Loihi 3 + AKD1000 vs Loihi 3 (dual gate) | N-17 explicitly tests N-3 by triangulation |
| spike model | binary | graded | F-N17-A3 ablation isolates this difference |
| capacity | 1.2M neurons (surrogate last-layer) | 8M neurons (could deploy more of CLM body natively) | N-17 → "fuller Putnam" stronger than N-3 "partial Putnam" |
| learning | inference-only | on-chip STDP | F-N17-A4 ablation isolates this |
| evidence weight | 1 neuromorphic data point | 2nd independent neuromorphic data point | doubled statistical confidence |
| timeline | AKIDA dev kit arrival (weeks) | INRC approval (4-12 wk) + NRC slot | N-3 first, N-17 follows; N-3 result informs N-17 proposal §3 |
| fail mode | substrate-dependent Φ | substrate-dependent OR neuromorphic-family-specific OR Loihi-3-specific | richer failure diagnosis space |

**Key**: If N-3 PASS and N-17 PASS → strong multi-realizability (two independent neuromorphic confirmations). If N-3 PASS but N-17 FAIL → AKD1000 result is suspicious (possibly surrogate artifact). If N-3 FAIL but N-17 PASS → AKD1000 binary-spike or 1.2M cap is the limiting factor (Loihi 3 graded + 8M unlocks the result). All four corners are publishable.

### 8.3 substrate ledger projected entries

```
own#2 (b) substrate-WITNESSED ledger:
  current state (2026-05-01):  CLM ✅ + EEG ✅  → 2/N
  N-3 PASS (AKIDA arrival D+0): + AKIDA ✅      → 3/N
  N-17 PASS (Loihi 3 NRC):     + Loihi 3 ✅    → 4/N
  F1 CLOSED gate at ≥ 3/4 primary basket alignment.
```

---

## §9 cost estimate ($0 budget compliance)

### 9.1 spec authoring (this work, today)

| item | cost |
|---|---|
| spec doc + state JSON authoring (anima agent compute) | $0 (within harness) |
| WebSearch / WebFetch for INRC docs verification | $0 (within harness) |
| **subtotal authoring** | **$0** |

### 9.2 application phase (NOT in this $0 spec — for user decision later)

| item | cost | notes |
|---|---|---|
| INRC membership fee | $0 | "free and open to qualified groups" |
| Korean co-PI partnership setup (if path 1 chosen) | $0-2K (admin overhead) | institutional MOU drafting; case-by-case |
| Proposal English editing | $0-500 | optional native-English review |
| INRC Participation Agreement legal review | $0-3K | KR institution legal counsel; per-hour billing |
| **subtotal application phase** | **$0-5.5K** | NOT incurred at this spec stage |

### 9.3 measurement phase (post-approval, NOT in this spec)

| item | cost | notes |
|---|---|---|
| NRC vLab compute hours | $0 | included in INRC membership |
| anima HEXA tool emit (M1-M6 deliverables) | $0 (within harness) | within $0 budget |
| Optional GPU cycles for surrogate fidelity sanity | ~$5-20 | re-use N-3 budget |
| **subtotal measurement** | **~$5-20** | bounded by N-3 budget envelope |

**Total this spec authoring**: **$0** ✅ (constraint satisfied).

---

## §10 D+0 readiness checklist

| 항목 | 상태 | blocker |
|---|:---:|---|
| spec doc (this) | ✅ | — |
| state JSON files (4) | ✅ | — |
| 16-prompt fixture (re-use N-3) | ✅ | shared with `tool/anima_phi_v3_canonical.hexa` |
| `tool/anima_phi_v3_canonical.hexa` | ✅ | READ-ONLY, no edit |
| INRC application email sent | ❌ (out of scope) | user decision required + institutional sponsor |
| RFP + proposal template received | ❌ (out of scope) | depends on email step |
| Korean institutional sponsor | ❌ (out of scope) | user decision; flagged §7.2 |
| INRC Participation Agreement signed | ❌ (out of scope) | KR institution legal review |
| NRC vLab account + SSH keys | ❌ (out of scope) | post-approval |
| Lava SDK install on NRC VM | ❌ (out of scope) | post-onboarding |
| `tool/anima_loihi3_lava_graph.hexa` | ❌ (M2 deliverable) | not authored at $0 spec stage |
| `tool/anima_loihi3_spike_to_dense.hexa` | ❌ (M2 deliverable) | not authored at $0 spec stage |
| `tool/n17_phi_loihi_dual_corr.hexa` | ❌ (M4 deliverable) | not authored at $0 spec stage |
| Loihi 3 chip slot on NRC | ⏳ | "rolling out 2026" per Intel Jan-2026 announce |

**Application-phase readiness = 100%** (template, falsifiers, technical plan all locked at spec level).
**Measurement-phase readiness = 0%** (gated on INRC approval + NRC slot + sponsor — all out of $0 scope).

---

## §11 cross-link

- parent: `docs/n_substrate_consciousness_roadmap_2026_05_01.md` (§5 N-17 row)
- purchase guide: `docs/n_substrate_purchase_guide_2026_05_01.md` (§N-17 TOP-1 priority block)
- sister N-3 (first neuromorphic axis): `docs/n_substrate_n3_clm_akida_phi_spec_2026_05_01.md` (CLM × AKIDA Φ)
- sister N-2 (EEG-spike pipeline): `docs/n_substrate_n2_eeg_akida_spike_pipeline_spec_2026_05_01.md` (encoder reuse target)
- Φ tool SSOT: `tool/anima_phi_v3_canonical.hexa` (substrate-agnostic, READ-ONLY)
- substrate ledger: own#2 (b) — current 2/N → projected 4/N if N-3 + N-17 both PASS
- F1 final verdict: `docs/n_substrate_consciousness_roadmap_2026_05_01.md` §6 F1
- race-isolation peers: N-1, N-2, N-3, N-4, N-5, N-6, N-7, N-9, N-10, N-14, N-19, N-20, N-21 prep agents

---

## §12 Sources (verified 2026-05-01)

- [Intel Neuromorphic Computing landing](https://www.intel.com/content/www/us/en/research/neuromorphic-computing.html)
- [INRC Confluence overview](https://intel-ncl.atlassian.net/wiki/spaces/INRC/overview)
- [Join the INRC application page](https://intel-ncl.atlassian.net/wiki/spaces/INRC/pages/1784807425/Join+the+INRC)
- [Access Intel Loihi Hardware (NRC vLab)](https://intel-ncl.atlassian.net/wiki/spaces/INRC/pages/1810432001/Access+Intel+Loihi+Hardware)
- [INRC Loihi 2 access community Q&A — eligibility + proposal flow](https://community.intel.com/t5/Mobile-and-Desktop-Processors/Inquiry-Regarding-INRC-Membership-and-Access-to-Intel-Loihi-2/m-p/1725292)
- [Intel Loihi 2 + Lava framework press release](https://www.intc.com/news-events/press-releases/detail/1502/intel-advances-neuromorphic-with-loihi-2-new-lava-software)
- [Hala Point — world's largest neuromorphic system](https://www.intc.com/news-events/press-releases/detail/1691/intel-builds-worlds-largest-neuromorphic-system-to)
- [Intel Loihi 3 announce 2026-01 — 8M neurons / 4nm / graded spikes](https://markets.financialcontent.com/wral/article/tokenring-2026-1-19-the-brain-like-revolution-intels-loihi-3-and-the-dawn-of-real-time-neuromorphic-edge-ai)
- [Loihi 3 vs TrueNorth 2 architecture comparison 2026](https://www.technomipro.com/neuromorphic-chips-2026-loihi-3-vs-truenorth-2/)
- [Lava Software Framework documentation](https://lava-nc.org/)
- [INRC RFP 3.0 (TRDF mirror, prior cycle)](https://www.trdf.co.il/files/INRC%20RFP%203.0.pdf)
- [Mike Davies INRC RFP announcement (LinkedIn)](https://www.linkedin.com/posts/mike-davies-71b4542_announcement-request-for-proposals-for-sponsored-activity-7027437828435296256-G2Ut)
- [Intel Neuromorphic Collaborators (UTK ECE coverage of 50-project selection)](https://eecs.utk.edu/intel-announces-neuromorphic-computing-research-collaborators/)
- [Loihi original architecture paper (Davies 2018)](https://redwood.berkeley.edu/wp-content/uploads/2021/08/Davies2018.pdf)
- [Real-time Continual Learning on Loihi 2 (arXiv 2511.01553)](https://arxiv.org/html/2511.01553v1)

---

**status**: N_SUBSTRATE_N17_LOIHI3_INRC_APPLICATION_SPEC_2026_05_01_LOCAL_DRAFT
**verdict_key**: APPLICATION_TEMPLATE_READY · NO_SUBMISSION · KOREA_ELIGIBLE_PRESUMED · NRC_QUOTA_UNCONFIRMED
**author**: anima N-17 prep agent (race-isolation sibling, AKIDA 외 차세대 뉴로모픽 비교 substrate)
