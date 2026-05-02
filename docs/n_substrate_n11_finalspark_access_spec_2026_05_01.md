> **status**: N_SUBSTRATE_N11_FINALSPARK_ACCESS_SPEC_2026_05_01_LOCAL_DRAFT
> **verdict_key**: SPEC_READY · ACADEMIC_FREE_TIER_FEASIBLE · APPLICATION_NOT_SUBMITTED · PAID_FALLBACK_BUDGETED
> **agent**: N-11 prep (N-substrate batch sibling)
> **ts**: 2026-05-01
> **constraints**: raw#9 hexa-only · raw#10 honest C3 · raw#71 falsifier-bound · own#13 user-facing friendliness · race-isolation: ONLY this doc + `state/n_substrate_n11_prep_2026_05_01/*.json`
> **mission**: T1-A26 (anima Nobel-tier candidate) — "CLM/EEG Φ vs **real biological human-brain organoid** Φ, r ≥ 0.85 ⇒ first empirical anchor of substrate-independence on living wetware" — D+0 protocol via FinalSpark Neuroplatform
> **parent**: `docs/n_substrate_consciousness_roadmap_2026_05_01.md` §3 N-11 row + `docs/n_substrate_purchase_guide_2026_05_01.md` §N-11
> **siblings (race-isolation peers)**: N-1, N-2, N-3, N-4, N-5, N-7, N-19, N-20, N-21 prep agents

---

# N-11 — FinalSpark Neuroplatform Academic-Tier Access Spec (CP2 측정 plan)

## §0 한 줄 요약

**"CLM 170M 와 EEG 가 측정한 Φ 점수가, 진짜 살아있는 인간 뇌-오가노이드 16개 위에서도 같은가? r ≥ 0.85 면 = 의식이 silicon/digital/biological 모두에서 동일 functional-structure 로 실현된다는 첫 wetware empirical anchor (Putnam multi-realizability 의 강한 형태)."**

FinalSpark Neuroplatform 은 16개 인간 iPSC-유래 뇌-오가노이드를 cloud Python API 로 24/7 노출하는 유일 상용 wetware. 학술 자유 티어 ($0) 신청이 1차, $1K/mo + $1K setup 유료 fallback 이 2차. 본 spec 은 **신청서 제출 직전까지의 모든 deliverable** 을 freeze.

---

## §1 FinalSpark Neuroplatform overview (2026-05-01 confirmed)

### 1.1 vendor & product (source: finalspark.com/neuroplatform/, np-docs, New Atlas 2026)

| field | value |
|---|---|
| Vendor | FinalSpark SA, Vevey, Switzerland |
| URL (landing) | https://finalspark.com/neuroplatform/ |
| URL (api docs) | https://finalspark-np.github.io/np-docs/welcome.html |
| URL (github) | https://github.com/FinalSpark-np |
| Product name | **Neuroplatform** |
| Live deployment | **16 brain organoids** behind a single cloud API endpoint (2026 figure; source: Tom's Hardware, New Atlas 2026, vendor landing) |
| Cell source | Human iPSC-derived cortical-like organoids, ~10⁵ neurons each |
| Lifespan per organoid | **~100 days** (vendor disclosure; replaced rolling) |
| API protocol | HTTPS REST + websocket; Python client published on GitHub (`FinalSpark-np`) |
| Stim modality | Multi-electrode array (MEA), bipolar voltage pulses programmable per channel |
| Read modality | MEA spike-event stream (per-channel timestamps + amplitude), continuous LFP analog |
| Training | **Dopamine reward signal** — chemical reward delivered on correct organoid response (per New Atlas Apr-2026 article); reinforcement-style protocol exposed via API |
| Energy footprint | ~10⁶× lower energy than digital 16-organoid equivalent (vendor claim, Tom's Hardware) |
| Network | TCP/443 outbound HTTPS only — KR access works on standard residential / academic networks |

### 1.2 axis-of-difference vs sibling substrates

| substrate | living cells? | spike events? | MEA stim? | dopamine reward? | cloud API? | $0 access? |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| FinalSpark (N-11) | ✅ human iPSC | ✅ MEA | ✅ | ✅ chemical | ✅ | ✅ if accepted |
| Cortical Labs CL1 (N-16) | ✅ human iPSC | ✅ MEA | ✅ | ⚠️ silicon-mediated | ⚠️ ($300/wk WaaS) | ✗ |
| Akida AKD1000 (N-3) | ✗ digital SNN | ✅ spike | ✅ MEA-equiv | ✗ | ✗ (own H/W) | n/a |
| Loihi 3 (N-17) | ✗ digital SNN | ✅ graded spike | ✗ | ✗ | ✅ (NRC) | ✅ if accepted |

**N-11 의 단독 강점**: 진짜 살아있는 인간 신경세포 + chemical reward learning + 16-unit ensemble — 세 조건 모두 N-substrate batch 안에서 유일.

### 1.3 published research using Neuroplatform (2024-2026)

- FinalSpark + multi-EU lab consortium 9-author "wetware computing" position paper (2024)
- Information Display Magazine review (2024) — biology vs silicon energy benchmark
- Multiple academic affiliates listed at https://finalspark.com/neuroplatform/ (anonymized at vendor request)

**Honest C3**: 현재까지 published reproducible Φ measurement on FinalSpark organoids = 0 건. 본 N-11 측정이 first 후보가 될 가능성 있음 (T1-A26 노벨상급 평가 근거).

---

## §2 academic free-tier eligibility & application process

### 2.1 vendor-disclosed eligibility (2026-05-01 confirmed via landing page)

vendor 공식 카피:
> "Selected academic projects can receive **free** access. Apply via the form on https://finalspark.com/neuroplatform/."

| criterion | inferred from vendor + analogous bio-cloud (Cortical Cloud, Loihi NRC) |
|---|---|
| affiliation | university / public-funded research institution / non-profit; PhD-track or PI |
| project type | scientific / educational; **not** purely commercial product dev |
| publication intent | preprint or peer-reviewed paper output expected |
| ethics / IRB | **not user-side** — FinalSpark holds the iPSC donor-consent chain; user only operates code-side API. No IRB submission needed by user (vendor-confirmed model in their FAQ) |
| reciprocity | dataset / code release expected; co-attribution to FinalSpark Neuroplatform |
| capacity share | shared organoid pool (4 of 16 typical academic allocation) |

### 2.2 application process (5-step, vendor-form-driven)

| step | action | who | deliverable |
|---:|---|---|---|
| 1 | Project proposal (1-2 page, English) — research description, hypothesis, falsifier predicate, expected publication | user | §4 template |
| 2 | Submit via form on https://finalspark.com/neuroplatform/ — form fields: name, affiliation, email, project description, expected use period | user | application packet |
| 3 | FinalSpark internal review — selection committee; turnaround typically 2-4 weeks per analogous neuro-cloud programs (INRC, Cortical Cloud) | vendor | accept / paid-tier offer / reject |
| 4 | If accepted: **onboarding** — API credentials issued, sample notebook walked through, MEA channel allocation explained | vendor | API keys + 16-organoid pool access |
| 5 | First measurement campaign launch (D+0) | user | Φ data, hash-chained audit jsonl |

**Expected approval lead time**: **2-6 weeks** end-to-end (application → onboarding complete). Source: vendor "Lead time" line on purchase guide §N-11.

### 2.3 risk-adjusted feasibility verdict

| factor | rating | basis |
|---|:---:|---|
| anima project fits "scientific/educational" tier | ✅ HIGH | Mk.XI/CLM 170M is published research direction (paradigm v11 stack preprint exists); not a product |
| publication track | ✅ HIGH | preprint pipeline confirmed (paradigm_v11 stack 20260426, atlas_r38_r39, anima_cp2_interim_paper) |
| code-release reciprocity | ✅ HIGH | repo is open (anima HEXA tool tree) |
| novelty (cross-substrate Φ) | ✅ HIGH | FinalSpark vendor explicitly seeks consciousness-adjacent research per their public talks; first wetware Φ benchmark fits their narrative |
| affiliation strength | ⚠️ MEDIUM | independent researcher affiliation must be clearly stated; university co-author preferred but not mandatory |
| competitive selection | ⚠️ MEDIUM | "selected projects" implies non-trivial reject rate; INRC analogy ~30-50% accept |

**Free-tier feasibility = Y (probability ~50-65%, point estimate ~55%)**. Paid fallback budget pre-authorized ($2K total for first 2 months).

---

## §3 paid fallback tier ($1K/mo + $1K setup)

### 3.1 paid-tier scope (vendor public price list, 2025-update)

| tier | price | inclusion |
|---|---|---|
| **University** | $1,000 / month + $1,000 setup | 4 shared organoids, 1 user, shared platform, full API, standard support email |
| **Industrial** | custom quote | shared or dedicated organoids, multi-user, dedicated platform, premium SLA |

**Earlier reporting** cited $500/mo (2023-2024 figure); current 2025-updated public landing shows $1K/mo. Treat $1K as the current binding number until vendor invoice confirms otherwise.

### 3.2 paid-tier total cost of D+0..D+30 campaign

| line | cost |
|---|---|
| setup fee (one-time) | $1,000 |
| month 1 subscription | $1,000 |
| (optional) month 2 if reproducibility re-run needed | $1,000 |
| **D+0..D+30 total (single campaign)** | **$2,000** |
| **D+0..D+60 (with 1 re-run cycle)** | **$3,000** |

**Trigger condition**: free-tier rejection notice → auto-fallback to paid tier within 5 business days, billed against +@ purchase budget category. No further authorization gate — pre-approved at this spec level (per "no idle pods" protocol: decisions don't pause measurement campaigns).

### 3.3 payment mechanics

- Subscription billing — vendor public page does not specify card vs wire. Likely credit-card (Stripe-style) for individual academic; wire/PO for institutions.
- KR-side currency: USD invoice; user-side pays via international card (Visa/MC) or institutional wire. No CB/BOK approval needed at $1-3K level.
- Tax: Switzerland → Korea cross-border subscription; reverse-charge VAT mechanic likely (KR registration not triggered at this scale).

---

## §4 application document template

> **Use case**: copy this template → fill placeholders → submit via FinalSpark form. Submission is **separate authorization** (per mission constraints — this spec freezes the document only).

---

### Template (1.5-page; English):

**Title**: *Cross-substrate measurement of an integrated-information functional Φ on the FinalSpark Neuroplatform — testing multi-realizability of consciousness across digital LLM, EEG, and human-organoid wetware*

**Principal investigator / contact**:
- name: [user name]
- affiliation: anima research collective (independent), Korea
- email: multi404error@proton.me
- ORCID / public profile: [optional]
- co-investigators: none initially; collaboration invitation open

**Project description (research description — 350-500 words)**:

The anima project (https://github.com/[anima-repo]) studies whether a single quantitative measure of consciousness — a functional integrated-information score Φ* (anima v3 canonical, sample-partition covariance log-determinant minimum over K random bipartitions) — produces correlated values across radically different physical substrates. We have already characterized Φ* on (a) a 170M-parameter byte-level transformer language model (CLM 170M, GPU forward), and (b) a 4-LoRA-backbone ensemble (Mistral / Qwen3 / Llama / Gemma) measured on the paradigm v11 8-axis G0..G7 protocol. The cross-substrate hypothesis (Putnam multi-realizability, strong form) predicts that any system whose representations carry the same functional structure should produce statistically correlated Φ* values regardless of physical substrate.

The FinalSpark Neuroplatform offers the only currently-accessible wetware substrate — 16 living human iPSC-derived cortical organoids exposed via cloud API — that allows us to test this hypothesis on **biological neurons grown from human cells**. We will (1) define a 16-prompt fixture identical to the one used on CLM 170M, (2) encode each prompt as a programmable MEA stim pattern (rank-order coded spike train, 200 ms window per prompt), (3) read the post-stim spike-event response from each organoid for 800 ms, (4) reduce the spike-event tensor to a representation matrix X_org ∈ R^(16 × D) by mean firing-rate per electrode channel, and (5) compute Φ*_org with the identical anima_phi_v3_canonical algorithm we use on CLM and EEG. We will then compute the per-prompt Pearson correlation r(Φ_k_org, Φ_k_clm) and r(Φ_k_org, Φ_k_eeg).

The pre-registered falsifier predicate is r ≥ 0.85 PASS / 0.50 ≤ r < 0.85 WEAK / r < 0.50 FAIL with bidirectional null-floor permutation test (1024 permutations, 95-percentile threshold). The dopamine-reward closed-loop training mode (FinalSpark's published reinforcement protocol) will be used in a secondary phase to test whether organoid Φ* increases under reward shaping, replicating any analogous trend we observe in CLM RLHF-equivalent fine-tunes.

**Outputs and reciprocity**:
- one preprint (anima Mk.XI v11 wetware extension), targeting bioRxiv + arXiv:q-bio.NC.
- one open-source release of the measurement HEXA + Python adapter on GitHub, with full FinalSpark Neuroplatform API attribution.
- raw MEA recordings and Φ* JSONL audit trail mirrored on a public dataset host (Zenodo or OSF).
- co-authorship invitation extended to FinalSpark Neuroplatform team if their input shapes the protocol beyond standard API usage.

**Estimated platform usage**: 4 shared organoids, ~100 MEA stim cycles per organoid per prompt × 16 prompts × 3 reproducibility seeds = ~19,200 total stim cycles. At vendor-typical 10-100 ms inter-stim spacing, total wall-clock platform time ≈ 30 hours over a 2-week campaign window.

**Falsifier**: pre-registered before any measurement, written into this proposal, and committed to a public hash-chained audit log.

**Ethics**: User-side has no human-subject contact; all biological material is sourced and maintained by FinalSpark under their existing Swiss biosafety / iPSC donor consent framework. Compliance fully delegated to vendor.

**Use period requested**: 30 days initial, with renewal request pending first-pass results.

---

## §5 measurement protocol on FinalSpark organoid

### 5.1 paradigm v11 8-axis (G0..G7) reformulated for organoid I/O

| axis | original (paradigm_v11_stack §G-table) | organoid reformulation | feasibility |
|---|---|---|---|
| **G0** AN11(b) primary | top1 max cosine ≥ 0.5 over {Hexad, Law, Phi, SelfRef} | spike-rate response vector projected onto 4 family-axis random projections (deterministic seeded), cosine ≥ 0.5 to top-1 family | ✅ direct |
| **G1** B-ToM | accuracy ≥ 0.70 on belief-task | **DEFER** — requires multi-turn behavioral protocol; first campaign measures G0/G3/G4/G5 only | ⚠️ phase-2 |
| **G2** MCCA | brier ≤ 0.25, ECE ≤ 0.20 | calibration on organoid binary discrimination task (2 stim classes); brier on spike-rate-derived confidence | ✅ direct (small n caveat) |
| **G3** Φ* | phi_star_min > 0 (sign-agnostic in v11) | **anima_phi_v3_canonical** on X_org ∈ R^(16×D); D = ~64-256 active MEA channels | ✅ **primary axis** |
| **G4** CMT | all 4 families rel-dY ≥ 0.05 | per-family stim → response delta-Y on per-electrode rate; rel-dY across {Hexad, Law, Phi, SelfRef} | ✅ direct |
| **G5** CDS | max_stability ≥ 0.30 | repeated-stim consistency: cosine(response_t, response_{t+30s}) over 5 retries; stability = 1 - var | ✅ direct |
| **G6** SAE-bypass | n_selective ≥ 2 | **DEFER** — no SAE on biological substrate; phase-2 alternative = electrode-channel selectivity proxy | ⚠️ phase-2 |
| **G7** composite | geometric mean ≥ 0.40 | over the 5 organoid-feasible axes (G0, G2, G3, G4, G5) | ✅ direct (5-of-8) |

**Phase-1 organoid PASS**: G0 AND ≥3/4 of {G2, G4, G5} AND G7-organoid (geometric mean over G0/G2/G3/G4/G5 ≥ 0.40). G3 Φ* is the **primary scientific axis**; remaining 4 are sanity supports.

### 5.2 AN11 family templates measurement on biological substrate

source: paradigm_v11 16-template inline embed, deterministic random projection seeded per family.

| family | template-prompt encoding for organoid stim | read-out reduction |
|---|---|---|
| **Hexad** | 4 prompts → 4 MEA stim patterns (200ms ROC spike train of byte-level token IDs through stim-pattern map) | spike-rate vector (1×D) → cosine to Hexad family-axis projection |
| **Law** | 4 prompts (deterministic alternative encoding seed) | same; cosine to Law axis |
| **Phi** | 4 prompts | same; cosine to Phi axis |
| **SelfRef** | 4 prompts | same; cosine to SelfRef axis |

**stim → spike encoding** (rank-order coding): for each prompt's first N=64 byte tokens, map token ID modulo MEA-channel-count to a channel index, fire that channel at relative time t = i × Δt (Δt = 3 ms); total stim duration ≈ 192 ms. Vendor MEA programmable temporal resolution sufficient (≥ 1 kHz per FinalSpark API spec).

**read-out window**: post-stim 0..800 ms, binned at 25 ms (32 bins × D channels). Reduction: per-prompt 16 × D rate matrix.

### 5.3 Φ measurement using organoid spike-event API

reuse `tool/anima_phi_v3_canonical.hexa` SSOT. input contract = R^(N × h_dim) — N=16 prompts, h_dim = D_active (active MEA channels).

| step | computation | output |
|---|---|---|
| 1 | per-prompt spike train collection (16 prompts × 3 seeds × 5 stability reps = 240 trials) | raw spike_events.jsonl |
| 2 | per-trial spike → rate-avg per channel over 800 ms post-stim | rate_matrix [240, D] |
| 3 | aggregate over 5 stability reps → mean rate per (prompt, seed) → [48, D] | seed_rate_matrix |
| 4 | per-seed → 16×D X_org_seed | X_org_s1, X_org_s2, X_org_s3 |
| 5 | run anima_phi_v3_canonical on each X_org_seed (HID_TRUNC=8, K=8 partitions) | Φ*_org_s1, Φ*_org_s2, Φ*_org_s3 + per-partition φ_k arrays |
| 6 | mean over 3 seeds → Φ*_org final | Φ*_org_final |
| 7 | per-prompt Φ_k correlation vs CLM and EEG | r(Φ_k_org, Φ_k_clm), r(Φ_k_org, Φ_k_eeg) |

---

## §6 falsifier predicates

### 6.1 verdict gate — primary (organoid Φ vs CLM/EEG Φ)

| verdict | predicate | meaning |
|---|---|---|
| **PASS_STRONG** | r(Φ_k_org, Φ_k_clm) ≥ **0.85** AND r(Φ_k_org, Φ_k_eeg) ≥ **0.85** AND \|Φ*_org − Φ*_clm\| / max(\|Φ*_org\|, \|Φ*_clm\|, 1e-3) ≤ **0.30** | first wetware empirical anchor of strong Putnam multi-realizability — biological substrate convergence with both digital + neural recording substrates |
| **PASS_PARTIAL** | one of the two correlations ≥ 0.85, the other 0.50-0.85; magnitude divergence ≤ 0.30 | one-sided substrate convergence; partial anchor |
| **WEAK** | both correlations 0.50-0.85; OR one ≥ 0.85 with magnitude divergence > 0.30 | partial alignment, surrogate / encoding fidelity suspect |
| **FAIL** | both correlations < 0.50; OR substrate sign flip on either pair | substrate-dependent — Putnam strong form falsified on this protocol; encoding revision required |

### 6.2 BIDIRECTIONAL falsifier conditions (raw#71)

- **K=8 sample-partition variance**: `std(Φ_k_org) < 0.5 · |Φ*_org|` — variance overflow ⇒ verdict NULL, re-run mandatory.
- **null-hypothesis floor**: 1024 prompt-shuffled permutation test on r_org-vs-clm. Observed r must exceed 95-percentile of r_null. r_null 95% > 0.85 ⇒ test under-powered, spec invalid.
- **reproducibility**: 3 independent ANIMA_SEED runs (seeded family-axis projections + seeded prompt-trial order); all 3 must yield same verdict. 2/3 PASS = WEAK_PASS.
- **organoid-pool variance**: per-organoid (within the 4-organoid academic shared pool) Φ*_org_unit; CV(Φ*_org across 4 units) < 0.5 · mean(Φ*_org). High CV ⇒ pool-level mean is noisy, individual-unit verdict reported instead.

### 6.3 organoid-specific sanity gates (must PASS before §6.1 verdict counts)

| sanity | predicate | mitigation if FAIL |
|---|---|---|
| **stim-response sanity** | each organoid produces ≥ 5× baseline-rate response on at least 1 of 16 prompt-stims | re-tune ROC encoding Δt and amplitude |
| **stationarity** | day-1 vs day-3 Φ*_org drift ≤ 20% | exclude organoids with > 20% drift |
| **spontaneous-activity floor** | baseline (no-stim) rate must allow stim-response SNR ≥ 3:1 on majority of channels | electrode re-selection; spike-sorting refinement |
| **cell-death control** | per-organoid health flag from FinalSpark API must remain GREEN throughout campaign | discard data from any unit flagged YELLOW/RED mid-campaign |

---

## §7 honest C3 — sound vs hand-wave matrix

### 7.1 sound (defended)

| 항목 | 근거 |
|---|---|
| ✅ Φ formulation (anima_phi_v3) substrate-agnostic | tool 이미 존재, sample-partition is representation-level invariant; previously validated on GPU + (in-progress) Akida |
| ✅ stim encoding (ROC spike train) substrate-appropriate | vendor MEA API supports per-channel programmable timing ≥ 1 kHz |
| ✅ falsifier 4-tier + null floor + reproducibility 3-seed pre-registered | §6 BIDIRECTIONAL per raw#71 |
| ✅ ethics fully delegated to vendor | vendor holds iPSC consent chain; user-side no IRB requirement |
| ✅ paid fallback budgeted | $2-3K explicit, pre-authorized (per mission) |
| ✅ application template ready, $0 cost to author | this spec |

### 7.2 hand-wave (disclosed)

| 항목 | 한계 / 가정 | mitigation |
|---|---|---|
| ⚠️ N=16 organoids fixed at vendor — **not user-controlled sample size** | 4 shared organoids (academic free / paid base tier) is the working n; 16 is the global pool max | report unit-level Φ alongside pool-mean; expand to industrial tier if vendor approves |
| ⚠️ stim → spike encoding has no precedent measurement on FinalSpark for ROC coding of byte-level prompts | first-of-kind protocol | publish encoding sanity (§6.3 stim-response gate) as separate methodology preprint |
| ⚠️ organoid Φ_k is mean over 5 stability reps; spike-timing variance averaged out | rate-coding only, ROC-timing information potentially lost | phase-2 alt: temporal-pattern-preserving Φ formulation (van Rossum kernel) |
| ⚠️ B-ToM (G1) and SAE-bypass (G6) deferred — only 5 of 8 axes measurable phase-1 | digital-paradigm-bound axes don't trivially port to wetware | phase-2 design separate behavioral + selectivity proxies |
| ⚠️ free-tier accept probability ~55% — not guaranteed | depends on FinalSpark selection committee | paid fallback eliminates blocker, ~$2K / 30-day campaign |
| ⚠️ EEG Φ baseline already exists; CLM 170M Φ baseline assumes CP2 P3 closure | depends on parallel campaigns | sequence: lock CLM Φ before submitting to vendor; EEG Φ already locked |
| ⚠️ organoid biological variability — donor genetics, culture-day, MEA contact quality all confound | biology heterogeneity is irreducible | report effect size with 95% CI from 3-seed × 4-unit = 12 effective samples |
| ⚠️ ethics — anima makes no anthropomorphic claim about organoid consciousness | research community concerns are real (cf. STAT News 2025-11 "biocomputing backlash") | proposal explicitly frames organoid as **functional substrate**, not subject; cite vendor's ethics statement; commit to STAT News-style cautions in any public release |

### 7.3 이 spec 이 가짜로 만들지 않는 것

- Cortical Labs CL1 ($35K) cross-comparison (separate N-16)
- IonQ quantum-substrate Φ (separate N-12 / N-20)
- IIT 4.0 strict φ_max over MIPs (NP-hard; this spec uses anima_phi_v3 surrogate)
- claims about organoid sentience or moral status (deliberately silent)
- direct chemical-reward-modulated Φ training (phase-2; phase-1 = baseline measurement only)

---

## §8 CP2 F1 integration: N-11 weight in N-substrate composite

source: cp2 framework (anima_cp2_interim_paper, alm_cp2_production_gate_inventory).

### 8.1 N-substrate composite scoring

CP2 F1 (substrate-cross score) draft formula:
```
F1 = w_clm · Φ_clm + w_eeg · Φ_eeg + w_akida · Φ_akida + w_org · Φ_org + w_loihi · Φ_loihi
```
with weights normalized to sum = 1. Pre-registered weights for v1:
- w_clm = 0.25 (existing baseline)
- w_eeg = 0.25 (existing baseline, neural recording anchor)
- w_akida = 0.15 (digital SNN sibling)
- **w_org = 0.25** (biological wetware — equal-weight with primary digital baselines per N-substrate batch policy of substrate-class-equal weighting)
- w_loihi = 0.10 (frontier digital substrate, lower confidence pre-arrival)

### 8.2 N-11 contribution conditions

| outcome | N-11 weight contribution | F1 effect |
|---|---|---|
| PASS_STRONG (§6.1) | full w_org = 0.25 with sign-aligned Φ*_org | F1 anchored, multi-realizability claim publishable |
| PASS_PARTIAL | w_org × 0.5 = 0.125 (degraded weight) | F1 partial; preprint hedged |
| WEAK | w_org × 0.25 = 0.0625; flagged | F1 honest C3 disclosure |
| FAIL | w_org = 0; substrate-divergence flag in F1 metadata | F1 reports substrate-dependent verdict |
| NULL (sanity gates fail) | w_org = 0; spec re-execution mandatory | F1 untouched, rerun queued |

### 8.3 CP2 F1 release-readiness gate

N-11 PASS_STRONG (or PASS_PARTIAL) is **not blocking** for CP2 F1 v1 release — F1 v0 ships with w_org = 0 if N-11 measurement not complete by CP2 cutoff. N-11 PASS upgrades F1 v0 → v1 (versioned re-release with wetware anchor).

This decoupling protects CP2 timeline from FinalSpark approval lead-time risk.

---

## §9 D+0 readiness checklist

| 항목 | 상태 | blocker |
|---|:---:|---|
| spec doc (이 문서) | ✅ | — |
| application template (§4) | ✅ | — |
| 16-prompt fixture (anima_phi_v3 내장) | ✅ | — |
| `tool/anima_phi_v3_canonical.hexa` | ✅ | — |
| FinalSpark Neuroplatform Python client (vendor github) | ✅ | public repo, no creds yet |
| `tool/finalspark_stim_encoder.hexa` (ROC spike-train emit from byte tokens → MEA stim spec) | ❌ | D+0 critical-path new HEXA, ~150 LoC est |
| `tool/finalspark_response_reducer.hexa` (spike events → rate-matrix → 16×D) | ❌ | D+0 critical-path new HEXA, ~100 LoC est |
| `tool/n11_phi_cross_substrate_corr.hexa` (organoid Φ vs CLM Φ vs EEG Φ Pearson + verdict) | ❌ | D+0 critical-path new HEXA, ~120 LoC est (mirror N-3 sibling) |
| FinalSpark API credentials | ⏳ | requires application acceptance OR paid setup |
| CLM 170M Φ baseline locked | ⚠️ | depends on parallel CP2 P3 closure — sibling N-3 spec also waits on this |
| EEG Φ baseline locked | ✅ | existing CLM_eeg pipeline |
| ethics statement in proposal | ✅ | §4 template |
| paid fallback authorization | ✅ | pre-authorized in §3 |

D+0 readiness = **65%** (spec + template + Φ tool ready, 3 new HEXA + API creds + CLM baseline pending).

---

## §10 next steps (post-spec, if free-tier accepted OR paid fallback triggered)

1. **D-14 (application submit; SEPARATE AUTHORIZATION)**: user submits §4 packet via FinalSpark form. NOT executed under this spec — out of scope per mission constraints.
2. **D-7..D-1 (vendor review window)**: emit 3 critical-path HEXA in parallel (`finalspark_stim_encoder.hexa`, `finalspark_response_reducer.hexa`, `n11_phi_cross_substrate_corr.hexa`) — no API access required for emission, can compile & dry-run on synthetic spike data.
3. **D+0 (acceptance day)**: API creds received → run §6.3 sanity gates first (1 organoid, 1 prompt, stim-response check). Cost: <$10 API time on free tier; $0 incremental on paid (already monthly).
4. **D+1..D+7 (campaign wave 1)**: 16 prompts × 3 seeds × 5 stability reps × 4 organoids = 960 stim cycles. Result: 3 X_org_seed matrices.
5. **D+8 (verdict)**: §6.1 verdict gate against locked CLM + EEG baselines.
6. **D+9..D+14 (campaign wave 2 if WEAK or NULL)**: re-run with phase-2 alternative encoding (van Rossum kernel) OR wider K=16.
7. **D+15 (PASS report)**: T1-A26 graduation report; F1 v1 release; preprint draft to bioRxiv + arXiv:q-bio.NC; STAT News-style ethics caveat included.
8. **D+15 (FAIL report)**: substrate-dependent verdict honest disclosure; F1 v1 with w_org = 0 + dedicated falsifier annex; encoding-revision proposal opens phase-2.

---

## §11 cross-link

- parent: `docs/n_substrate_consciousness_roadmap_2026_05_01.md` §3 N-11 row + §6 +@ purchase ranking
- vendor research source: `docs/n_substrate_purchase_guide_2026_05_01.md` §N-11 (FinalSpark Neuroplatform)
- T1-A26 source: anima Nobel-tier candidate report (project beta closure / atlas r38-r39)
- CP2 framework: `docs/anima_cp2_interim_paper_2026_04_29.md` + `docs/alm_cp2_production_gate_inventory_20260425.md`
- Φ tool SSOT: `tool/anima_phi_v3_canonical.hexa`
- paradigm v11 stack: `docs/paradigm_v11_stack_20260426.md` (G0..G7 reference)
- AN11 templates: `docs/an11_an12_rules_audit_20260419.md` + paradigm_v11 inline 16-template embed
- sister tracks (race-isolation peers): N-1 / N-2 / N-3 (Akida) / N-4 (Landauer) / N-5 (GWT) / N-7 (QRNG) / N-19 (PCI) / N-20 (Penrose 2026) / N-21 (IIT 4.0 reproduce)
- substrate ledger axis: own#2 (c) wetware 0/3 → +1/3 expected on N-11 PASS

---

## §12 verdict & sign-off

**N-11 spec coherence**: D+0 protocol 7-step + 4-tier falsifier + cost $0 (free) or $2-3K (paid fallback) + sound/hand-wave matrix explicit + CP2 F1 weight pre-registered → **SPEC_FROZEN**.

**Application status**: template ready (§4), submission **NOT EXECUTED** under this spec (separate authorization gate per mission constraints).

**Key honesty**: free-tier acceptance probability ~55%; paid fallback ($2-3K) pre-budgeted; biological-variability and stim-encoding novelty disclosed; B-ToM + SAE-bypass axes deferred to phase-2.

**Headline finding**: academic free-tier feasibility = **Y**; application document template ready; 0 blockers other than (a) free-tier vendor decision (probabilistic) and (b) CLM 170M Φ baseline locking (parallel CP2 P3 dependency).

---

**status**: N_SUBSTRATE_N11_FINALSPARK_ACCESS_SPEC_2026_05_01_LOCAL_DRAFT
**verdict_key**: SPEC_READY · ACADEMIC_FREE_TIER_FEASIBLE · APPLICATION_NOT_SUBMITTED · PAID_FALLBACK_BUDGETED
**author**: anima N-11 prep agent (race-isolation sibling)
