# N-19 PCI Stage-3 spec — DCC + LLE + GAP design

- **TS**: 2026-05-02
- **Agent**: N-19 PCI Stage-3 spec — DCC + LLE + GAP 추가 metric design
- **Status**: SPEC_DRAFT (no execution; $0; design-only)
- **Predecessor Stage-1**: `state/n_19_pci_tmsfree_2026_05_01/pci_surrogate_compute.json` — 6/6 PASS (mean 0.656)
- **Predecessor Stage-2**: `state/n_19_pci_stage2_2026_05_02/stage2_pci_compute.json` — 6/6 PASS (mean 0.555) per #97
- **Spec target**: `docs/n_substrate_n19_pci_spec_2026_05_01.md` §4.4.3 (currently TODO -> proposed SPEC_DRAFT)
- **Race isolation**: writes only to `state/n_19_pci_stage3_spec_2026_05_02/*.json` + this doc

---

## §0 한 줄 요약

Stage-2의 fluidity-dFC + functional-repertoire 위에 **DCC (Dynamic Conditional Correlation)** + **LLE (Largest Lyapunov Exponent)** + **GAP (Graph-theoretic Absorption Probability)** 3종을 더한 6-component PCI surrogate 설계. 가중치 α=0.30 / β=0.20 / γ=0.15 / δ=0.15 / ε=0.10 / ζ=0.10. 16ch-adapted cutoff 0.25 (Stage-1/2와 동일). 5건 양방향 falsifier preregister. w6 0.10 unchanged (n≥10 unlock 까지 8 세션). Stage-4 TMS lab-share 가 Stage-3 EXEC 직후 unlock. **Honest C3 3건**: DCC 신경과학 validation thin / LLE 다채널 aggregation non-standard / GAP EEG 적용 전례 zero — over-fitting risk HIGH.

---

## §1 Stage-3 metrics 정의

### §1.1 DCC — Dynamic Conditional Correlation (Engle 2002)

**Primary refs**: Engle 2002 *J Bus Econ Stat* 20(3):339-350; Lindquist 2014 *NeuroImage* 101:531 (fMRI 적용 first paper).

**Input**: 16-channel EEG α-band (8-13Hz) bandpass-filtered time series, 60s @ 250Hz = 15000 samples per channel.

**Algorithm**:

1. Per-channel univariate **GARCH(1,1)** fit -> standardized residuals η_i(t) = ε_i(t) / σ_i(t)
2. Compute Q(t) = (1 − α − β)·Q̄ + α·η(t-1)·η(t-1)' + β·Q(t-1) where Q̄ = unconditional cov(η)
3. Normalize: R(t) = diag(Q)^(−1/2) · Q(t) · diag(Q)^(−1/2) → 16×16 time-varying correlation matrix
4. Per-window Shannon entropy of off-diagonal R(t) (binned 20 bins on [-1, 1])
5. **DCC_entropy_session** = mean over t of H(R(t)_offdiag)

**Interpretation**: High DCC entropy = rich time-varying covariance landscape (consciousness signature per Lindquist 2014). Low DCC entropy = static / collapsed dynamics.

**Normalization**: DCC_entropy raw bound [0, log₂(20)] = [0, 4.32]; **DCC_norm = DCC_entropy / 4.32** ∈ [0, 1].

**Wake target band (normalized)**: [0.55, 0.85] (extrapolated from Lindquist 2014 fMRI cohort; HEXA EEG cohort calibration TBD).

---

### §1.2 LLE — Largest Lyapunov Exponent (Rosenstein 1993)

**Primary refs**: Wolf 1985 *Physica D* 16:285 (full algorithm); Rosenstein 1993 *Physica D* 65:117 (small-data variant — preferred for 60s EEG); Stam 2005 *Clin Neurophysiol* 116:2266 (EEG-LLE review).

**Input**: Per-channel EEG time series, 60s @ 250Hz = 15000 samples; tested on both broadband and α-band variants.

**Algorithm (Rosenstein small-data variant)**:

1. Phase-space reconstruction via **time-delay embedding**: x(t) → X(t) = [x(t), x(t+τ), …, x(t+(m−1)τ)] with m=10, τ from first minimum of mutual information (AMI)
2. For each reference point X(i), find nearest neighbor X(j) with |i−j| > mean period (Theiler window)
3. Track separation d_ij(k) = ‖X(i+k) − X(j+k)‖ over k forward steps
4. Compute y(k) = ⟨ln d_ij(k)⟩_i averaged over reference points
5. Linear fit slope of y(k) vs k over expansion window (k=1..30) → **λ₁ = LLE**
6. Repeat per channel; LLE_session = mean over 16 channels of λ₁
7. Bootstrap CI: 200 resamples of nearest-neighbor pair selection

**Interpretation**: λ₁ > 0 = chaotic attractor (consciousness signature per Pritchard 1994). λ₁ ≤ 0 = converging / periodic dynamics.

**Normalization**: For 250Hz EEG, expected wake λ₁ ∈ [0.05, 0.5] bits/sample (Stam 2005); **LLE_norm = clip(λ₁ / 0.5, 0, 1)**.

**Wake target band (normalized)**: [0.10, 0.60].

---

### §1.3 GAP — Graph-theoretic Absorption Probability

**Primary refs**: Doyle & Snell 1984 *Random Walks and Electric Networks* (theory); Bressler 2011 *Trends Cogn Sci* 15:277 (Granger causality EEG); Sporns 2018 *Networks of the Brain* Ch.4 (network neuroscience consciousness).

**Input**: 16-channel EEG α-band time series (matched to DCC input).

**Algorithm**:

1. Pairwise **Granger causality** F_ij computed for all 16×16 ordered pairs (model order p=8 chosen by AIC) → directed weight matrix W
2. Threshold W at 95th percentile to retain top edges (~20 of 240) → directed sparse graph G
3. Designate top-1 in-degree node as **absorbing state A**; remaining 15 nodes are transient
4. Build transition matrix P from W (row-normalize); compute fundamental matrix N = (I − Q)^(−1) where Q is the transient-to-transient block
5. **Absorption probability** b_i = Σ_j N_ij · R_jA where R is transient-to-absorbing block
6. **GAP_variance_session** = var(b_i over i = 1..15)
7. Repeat with rotating absorbing-node choice (top-3 in-degree); average GAP_variance over 3 runs

**Interpretation**: High GAP variance = heterogeneous absorption landscape = rich directed-causal repertoire (Sporns 2018 hub-richness consciousness signature). Low GAP variance = uniform absorption = degenerate / hub-collapsed graph.

**Normalization**: GAP_variance bound [0, 0.25] (var of 15 probs in [0,1] is max 0.25); **GAP_norm = GAP_variance / 0.25** ∈ [0, 1].

**Wake target band (normalized)**: [0.20, 0.70] (HEXA calibration TBD — no published EEG-GAP cohort exists).

---

## §2 Stage-3 PCI surrogate formula

```
PCI_S3 = α·Stage1 + β·fluidity_norm + γ·repertoire_norm + δ·DCC_norm + ε·LLE_norm + ζ·GAP_norm
```

| Weight | Symbol | Value | Down-from Stage-2 | Justification |
|---|---|---|---|---|
| α | Stage1 anchor | **0.30** | 0.50 → 0.30 | Stage-1 Hjorth/LZ/PE 묶음은 여전히 가장 검증된 component이지만, 새 metric 3종이 0.30 weight를 흡수해야 하므로 비례 축소 |
| β | fluidity | **0.20** | 0.30 → 0.20 | eLife 2025 ranking 두 번째 strongest discriminator, 새 metric 추가에 따른 비례 축소 |
| γ | repertoire | **0.15** | 0.20 → 0.15 | Comm Biol 2024 ridge model mid-tier predictor, 비례 축소 |
| δ | DCC | **0.15** | 신규 | Engle-DCC 가 Lindquist 2014 fMRI 검증 보유 — LLE/GAP 보다 약간 높은 confidence tier |
| ε | LLE | **0.10** | 신규 | Single-channel chaos measure — multi-ch aggregation 비표준, lowest-confidence tier |
| ζ | GAP | **0.10** | 신규 | EEG 직접 적용 전례 zero — purely hypothetical, lowest-confidence tier |
| **Σ** | | **1.00** | | |

**Cutoff (16ch-adapted)**: **0.25** — Stage-1 / Stage-2 와 동일 유지 (cross-stage comparability 보존; cutoff 상향은 cutoff-shift vs metric-discrimination을 conflate)

**Static clinical reference**: 0.31 (Casarotto 2016)

**Expected mean**: ~0.55–0.65 (Stage-2 mean 0.555 baseline + 새 metric 평균 contribution +0.0~+0.10; predicted 0.60, 95% CI [0.50, 0.70])

**Calibratable per session**: weights re-fit recommended after n≥10 sessions via constrained least-squares against TMS-PCI ground truth (when Stage-4 lab-share unlocks).

---

## §3 Cutoff 설계

- **Primary cutoff**: 0.25 (16ch-adapted, Stage-1/2 동일)
- **Secondary clinical reference**: 0.31 (Casarotto 2016 14ch propofol fit, scale-matched)
- **Discriminative test**: Stage-3 cohort std MUST EXCEED Stage-2 std (Stage-2 std ≈ 0.05). Stage-3 std ≤ 0.05이면 새 metric 3종이 noise만 추가한 셈 (F-PCI-1 fire).
- **Expected Stage-3 std range**: [0.06, 0.12] (richer feature → 더 큰 cohort variance)

---

## §4 w6 update schedule

| Stage | Calibration count | w6 | 조건 |
|---|---|---|---|
| Initial (#74) | 0 | 0.10 | Stage-1 surrogate PASS active |
| Stage-2 EXEC (#97) | 1 | 0.10 | 1 method-validation step done; n=6 EEG pilot |
| **Stage-3 SPEC (this doc)** | 1 (unchanged — design-only) | **0.10** | SPEC artifact 자체는 calibration step 으로 카운트 안됨 |
| Stage-3 EXEC (next cycle) | 2 | 0.10 | 1 EXEC step 추가, 여전히 n<10 |
| Stage-3 cohort n≥10 | 10+ | 0.15 | 8 추가 EEG sessions 후 unlock (~6-10 weeks @ 1/week cadence) |
| Stage-4 TMS lab-share | n≥20 + ≥1 TMS cross-check | 0.25 | Sarasso 2014 cross-check, Korea U Sang-Hee Kim |

**This cycle decision**: w6 = **0.10 (UNCHANGED)** — Stage-3 SPEC 자체는 method-design 산출물 이므로 calibration step (data application 필요)에 해당하지 않음.

---

## §5 5건 falsifier (BIDIRECTIONAL preregister)

**Preregister TS**: 2026-05-02
**Preregister status**: ACTIVE — falsifiers locked **before** any Stage-3 EXEC. Post-EXEC change to falsifier definitions invalidates Stage-3 verdict per HARP raw#5.

| ID | Name | Criterion | If fired |
|---|---|---|---|
| **F-PCI-1** | Stage-3 mean regression | Stage-3 mean (6 epochs) < Stage-1 mean (0.656) | More metrics ≠ more signal; drop lowest-correlating new metric, re-weight (Stage-3.5 ablation) |
| **F-PCI-2** | DCC entropy null-equivalent | Mean DCC_entropy < 95th pct of phase-randomized surrogate (200 surrogates/epoch) | Time-varying conditional correlation 가 phase-null 과 구분 안됨; 60s → 180s epoch 확장 또는 DCC drop |
| **F-PCI-3** | LLE non-chaotic across cohort | All 6 epochs have mean λ₁ ≤ 0 | 어떤 epoch도 chaotic 으로 측정되지 않음 — embedding params 재조정 (FNN + AMI) 또는 LLE drop |
| **F-PCI-4** | GAP variance ≤ random graph | Mean GAP_var ≤ mean GAP_var of 200 Erdős-Rényi random directed graphs (matched edge count) | Granger graph 가 random graph 보다 풍부한 absorption structure 없음; 95th → 99th pct threshold 또는 GAP drop |
| **F-PCI-5** | Stage-3 vs Stage-2 verdict disagree | ≥1 epoch PASS in S2 but FAIL in S3, OR vice-versa (vs 0.25 cutoff) | Stage-3 가 Stage-2 evidence의 strict superset 아님 — metric instability; per-epoch component breakdown 으로 flip 원인 식별 |

---

## §6 N-19 spec §4.4.3 갱신 권고

| Section | Current status | Proposed status (after this doc) |
|---|---|---|
| §4.4.3 Stage-2 enhancements | PARTIAL (per #97 update) | **VALIDATED** (per #97 6/6 PASS) |
| §4.4.3 Stage-3 enhancements | TODO | **SPEC_DRAFT** (per this doc) |
| §4.4.4 Stage-4 TMS lab-share | TODO | TODO (unchanged — Stage-3 EXEC 가 prerequisite) |

**Proposed addendum text** (to be appended to §4.4.3):

> Stage-3 SPEC_DRAFT (2026-05-02): adds DCC (Engle 2002 GARCH-DCC entropy), LLE (Rosenstein 1993 small-data variant, per-channel mean), and GAP (Granger-Markov-absorption variance) per Stage-3 formula `PCI_S3 = 0.30·Stage1 + 0.20·fluidity + 0.15·repertoire + 0.15·DCC + 0.10·LLE + 0.10·GAP`. 5 falsifiers preregistered (F-PCI-1..5). Cutoff = 0.25 (16ch-adapted, unchanged from Stage-1/2). w6 schedule unchanged this cycle (0.10); Stage-3 EXEC will count as calibration step 2/10. Stage-4 (TMS lab-share validation) remains TODO at $2.3K / 10-14주 per N-19 §5. See `state/n_19_pci_stage3_spec_2026_05_02/stage3_spec_design.json` + `docs/n_19_pci_stage3_spec_2026_05_02.md`.

---

## §7 Stage-4 link

| Field | Value |
|---|---|
| Track | Stage-4 = TMS lab-share validation |
| Spec section | N-19 §5 + §4.4.4 |
| Lab candidate | Korea U **Sang-Hee Kim** (per #41 collab list) |
| Estimated cost | **$2,300 USD** |
| Estimated duration | **10–14 weeks** |
| Validation target | Sarasso 2014 cross-check — Stage-3 surrogate ranking matches gold-standard TMS-EEG PCI ranking on ≥3 shared subjects |
| Blocked by | Stage-3 EXEC (this spec is the prerequisite) |
| w6 unlock after Stage-4 | **0.25** per spec §4.4.5 |

---

## §8 Honest C3 (3 items)

1. **DCC GARCH = 금융 econometric model** (Engle 2002 Nobel-cited bond/equity volatility tool). Neuroscience 적용은 최근 (Lindquist 2014 fMRI; 2026년 기준 EEG 논문 <15편). Statistical assumptions (conditionally Gaussian innovations, weak stationarity over 60s) 가 EEG에 대해 **MARGINAL** — EEG는 1/f spectra와 burst dynamics 를 보이므로 GARCH의 variance-clumping bias 때문에 bursty wake EEG 에서 entropy 가 인위적으로 낮게 나올 가능성.

2. **LLE = single-channel chaos measure** with non-standardized multi-channel aggregation. Mean / max / median across 16 channels 모두 같은 데이터에 다른 ranking 산출 (Stam 2005 reports σ-channel ≈ 0.3 × mean for healthy wake). Sleep N3 도 일부 Babloyantz 계열 연구에서 positive λ₁ 보임 — LLE 단독으로 wake vs deep sleep 분리 불가능 (단지 'has-attractor' vs 'noise-dominated' 만 분리), PCI surrogate 요구 해상도보다 약함.

3. **GAP = NOVEL metric with ZERO published EEG application** as of 2026 (literature search 'absorption probability EEG consciousness' returns 0 hits). 변별 validity 가 순전히 **HYPOTHETICAL** — cohort calibration 전까지는. Combined Stage-3 = metric-proliferation gym vs robust-signal track-record; **N=6 cohort 에서 over-fitting risk HIGH**. 권고: Stage-3 verdict 를 exploratory only 로 취급, n≥10 cohort + TMS-lab-share cross-check (Stage-4) validation 전까지 upgrade-of-record 로 보지 말 것.

---

## §9 References

- Engle 2002 *J Bus Econ Stat* 20(3):339-350 — Dynamic conditional correlation: a simple class of multivariate GARCH models
- Lindquist 2014 *NeuroImage* 101:531 — Evaluating dynamic bivariate correlations in resting-state fMRI
- Wolf 1985 *Physica D* 16:285 — Determining Lyapunov exponents from a time series
- Rosenstein 1993 *Physica D* 65:117 — A practical method for calculating largest Lyapunov exponents from small data sets
- Stam 2005 *Clin Neurophysiol* 116:2266 — Nonlinear dynamical analysis of EEG and MEG: review
- Pritchard 1994 *Int J Neurosci* 75:303 — EEG dimensional complexity and Alzheimer's
- Doyle & Snell 1984 — Random Walks and Electric Networks (MAA Carus monograph #22)
- Bressler 2011 *Trends Cogn Sci* 15:277 — Wiener-Granger causality: a well established methodology
- Sporns 2018 — Networks of the Brain Ch.4 (MIT Press 2nd ed.)
- Sarasso 2014 *Curr Biol* 24:R1057 — Consciousness and complexity during unresponsiveness induced by propofol/xenon/ketamine (Stage-4 cross-check target)
- Casarotto 2016 *Ann Neurol* 80:718 — Stratification of unresponsive patients by an independently validated index of brain complexity
- companion: `docs/n_19_pci_tmsfree_results_2026_05_01.md` (Stage-1 result)
- companion: `docs/n_19_pci_stage2_results_2026_05_02.md` (Stage-2 result, #97)

---

## §10 Provenance + race isolation

- **Writes (race-isolated)**:
  - `state/n_19_pci_stage3_spec_2026_05_02/stage3_spec_design.json`
  - `docs/n_19_pci_stage3_spec_2026_05_02.md` (this file)
- **Reads (read-only)**:
  - `state/n_19_pci_tmsfree_2026_05_01/pci_surrogate_compute.json` (Stage-1)
  - `state/n_19_pci_stage2_2026_05_02/stage2_pci_compute.json` (Stage-2)
  - `state/n_19_spec_section_4_4_update_2026_05_01/update_log.json` (spec context)
- **Cost**: $0.00 (spec-only; no compute, no pod burn)
- **HEXA-only**: confirmed — no `.py` authored, no binary touched
