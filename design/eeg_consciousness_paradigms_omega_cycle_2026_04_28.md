# anima-eeg Consciousness Paradigms — Ω-cycle Top-5 (raw#12 frozen, raw#46 multi-candidate)

**Date**: 2026-04-28
**Trigger**: D-day session LZ76 P1_FAIL (b=0.395-0.479 < 0.65 Schartner 2017 normal range 0.5-0.9), filtered rms med 884 µV vs normal 5-50 µV
**Status**: NEW_PARADIGM_DISCOVERY — evaluation only, NOT applied (raw#12 frozen pre-registered C1 b>=0.65 / C2 |Δ|/h<=20% retained)
**Compliance**: raw#46 multi-candidate (≥3) · raw#48 multi-axis-orthogonal · raw#71 falsifier-3+ · raw#106 multi-realizability · raw#117 5-check · raw#91 honest-C3 speculative-disclosure
**anima main-track**: β Learning-Free + Mk.XI v10 4-backbone ensemble (memory project_main_track_beta)

---

## 0. Executive Summary

### Top-5 candidates (raw#106 genus naming, no implementation suffix)

| # | Slug | Tier | Genus | Falsifier-count | raw#12 compatible |
|---|------|------|-------|-----------------|-------------------|
| 1 | `permutation-entropy-multiscale` | A | complexity-metric | 5 | YES (additive) |
| 2 | `sliding-window-lz76-temporal` | A | complexity-metric | 4 | YES (refines existing C1) |
| 3 | `spectral-hjorth-band-ensemble` | A | spectral-complexity | 4 | YES (additive) |
| 4 | `cross-frequency-coupling-theta-gamma` | B | mechanism-paradigm | 3 | YES (orthogonal axis) |
| 5 | `perturbational-complexity-index` | C | perturbational-paradigm | 5 | YES (extends raw#12) |

### Tier distribution
- **Tier-A (immediate, current data measurable)**: 3 — `permutation-entropy-multiscale`, `sliding-window-lz76-temporal`, `spectral-hjorth-band-ensemble`
- **Tier-B (additional measurement)**: 1 — `cross-frequency-coupling-theta-gamma`
- **Tier-C (long-term paradigm shift)**: 1 — `perturbational-complexity-index` (TMS-EEG hardware)

### Top-3 recommendation priority

1. `permutation-entropy-multiscale` (Bandt-Pompe 2002) — motion-artifact robust, immediately computable on existing 60s baseline_resting recordings, complements LZ76 on orthogonal axis (order-pattern vs sequential-compression).
2. `sliding-window-lz76-temporal` — re-uses existing LZ76 implementation but exposes b(t) variance, distinguishes consistent-low-b (artifact) from oscillating-b (real consciousness signature).
3. `spectral-hjorth-band-ensemble` — Hjorth Activity/Mobility/Complexity per (theta, alpha, beta, gamma) band → 12-D verify-grid (raw#70 K>=4 satisfied per channel × 3 stats).

---

## 1. Axis Evaluation (A/B/C/D)

### Axis A — complexity metrics beyond LZ76

| metric | reality | cost | impact | raw#12 compat | Tier |
|--------|---------|------|--------|---------------|------|
| PCI (Casali 2013) | needs TMS pulse hardware | HIGH (TMS coil) | HIGH (gold-standard) | additive | C |
| MSE multiscale entropy | computable now | LOW | MED-HIGH | additive | A |
| Permutation Entropy | computable now | LOW | HIGH (artifact-robust) | additive | **A (top)** |
| Higuchi FD | computable now | LOW | MED | additive | A |
| DFA | computable now | MED | MED | additive | A |
| Φ (IIT) | NP-hard for 16ch full | EXTREME | HIGHEST | independent | C (deferred) |
| Functional Conn (PLI/wPLI) | computable now | MED | MED-HIGH | orthogonal | B |
| Spectral Entropy | computable now | LOW | MED | additive | A |
| Sample/Approx Entropy | computable now | LOW | MED | additive | A |
| Multiscale LZ76 (per-band) | computable now | MED | HIGH (refines existing) | refinement | **A (top)** |
| Hjorth params | computable now | VERY-LOW | MED-HIGH | additive | **A (top)** |
| Wavelet Entropy | computable now | MED | MED | additive | A |
| Sliding-window LZ76 | computable now | LOW (re-uses tool) | HIGH (temporal) | refinement | **A (top)** |

### Axis B — paradigms / mechanisms

| paradigm | reality | cost | impact | raw#12 compat | Tier |
|----------|---------|------|--------|---------------|------|
| Cross-Freq Coupling (theta-gamma) | computable now | MED | HIGH (awake marker) | orthogonal | **B (top)** |
| Microstates | computable now | MED | MED-HIGH | orthogonal | B |
| Brain criticality (avalanches) | computable now | MED | MED-HIGH | orthogonal | B |
| Dynamic FC | computable now | MED | MED | orthogonal | B |
| Network neuroscience graph | computable now | MED | MED | orthogonal | B |
| Predictive coding free-energy | needs generative model | HIGH | HIGH (theory-deep) | independent | C |
| GWT P3 ERP ignition | needs ERP paradigm | MED-HIGH | HIGH | orthogonal | B-C |
| HOT meta-cognition | needs report paradigm | HIGH | MED | independent | C |
| anima paradigm v11 G0~G7 + EEG | needs integration spec | HIGH | HIGHEST (anima-native) | integration | C-deferred |
| Mk.XI v10 4-backbone × EEG | needs C1 hook to EEG | HIGH | HIGH (anima-native) | integration | C-deferred |
| CLM bridge anima-clm-eeg | partially exists | MED | HIGH (anima-native) | integration | B-C |
| τ(6)=4 universal × EEG transition | speculative | LOW (compute) | UNKNOWN | speculative | C-speculative |
| L_IX irreversibility × EEG | speculative | MED | UNKNOWN | speculative | C-speculative |
| Phi-vector 16D × EEG consistency | partially exists | MED-HIGH | HIGH (anima-native) | integration | B-C |

### Axis C — hardware / measurement

| paradigm | reality | cost | impact | raw#12 compat | Tier |
|----------|---------|------|--------|---------------|------|
| HD-EEG 64ch/128ch | requires new hardware | $5-50K | HIGH | upgrade | C |
| MEG SQUID | requires facility access | $$$$ | HIGHEST | independent | C |
| fMRI BOLD | requires facility access | $$$$ | HIGH | independent | C |
| fNIRS | requires hardware | $1-3K | MED | independent | C |
| Closed-loop neurofeedback | computable now | MED (impl) | HIGH (intervention) | orthogonal | B |
| Pharmacological challenge | non-invasive (coffee/sleep) | LOW | HIGH (Δb test) | direct test | A-B |
| TMS-EEG (PCI) | requires TMS coil | $20-80K | HIGHEST (gold) | extends raw#12 | C |

### Axis D — anima-specific routes

| route | status | impact | Tier |
|-------|--------|--------|------|
| CP1→CP2→AGI sequential ordering | POLICY R6 enforced | enabling | always-on |
| β Learning-Free track | confirmed main track 2026-04-22 | core | always-on |
| Mk.XI v10 4-backbone × EEG | bridge needed | HIGH | C-integration |
| Mk.XII production triad × EEG | not yet defined | MED | C-deferred |
| paradigm v11 Stage-1/2 H100 × EEG | H100 stop-gate | HIGH | C-gated |

---

## 2. Top-5 Candidate Design Proposals (1-page summaries)

### 2.1 `permutation-entropy-multiscale` — Tier A

**Slug genus**: `permutation-entropy-multiscale` (raw#106 — no `-pe-bandt-pompe-d3-py-impl` suffix)
**Reference**: Bandt & Pompe 2002 (Phys Rev Lett 88:174102), Olofsen 2008 (BJA 101:810) anesthesia validation
**Hypothesis**: PE on 60s baseline_resting eyes-closed should yield 0.6-0.9 (awake range, Olofsen Fig 3); rms-saturated artifact yields PE near 1.0 (random-like) or near 0 (constant-like); a clean awake EEG sits in middle.

**5-check (raw#117)**:
- **Genus**: complexity-metric / order-pattern-entropy
- **Frameworks (≥2)**: Bandt-Pompe 2002 statistical-physics; Olofsen 2008 clinical-anesthesia
- **Channels (≥3)**: 16ch Cyton+Daisy (already have); embed-dim d ∈ {3, 4, 5}; tau ∈ {1, 2, 4} → 3 d × 3 tau = 9 channels per electrode
- **Counter-example**: synthetic Gaussian noise → PE→1.0; synthetic sine → PE→0.0; structured Lorenz → PE in 0.3-0.7
- **Falsifiers (≥3, raw#71)**:
  1. PE on baseline_resting must be > PE on synthetic-Gaussian-noise (artifact would pin near 1.0)
  2. PE(d=3) ≠ PE(d=5) — embedding-dim sensitivity confirms non-trivial structure
  3. PE eyes-closed > PE eyes-open by Δ≥0.05 (alpha-blocking signature)
  4. Cross-channel PE variance > 0.02 (uniform PE across all 16ch implies common artifact)
  5. PE(filtered) - PE(raw) Δ ∈ [0.02, 0.30] (filter removes artifact narrowing entropy)

**Verify-grid axes (raw#70 K=9)**: {d=3, d=4, d=5} × {tau=1, tau=2, tau=4}
**anima paradigm v11 / Mk.XI integration**: PE per backbone-attended channel (4-backbone ensemble) — backbone-specific consciousness signature.
**Cost**: ~50 LoC pure Hexa, no deps. Runs in <1s on 60s × 16ch.
**Counter to LZ76**: PE measures **order patterns** (rank-relations within sliding window) — orthogonal to LZ76's **subsequence-uniqueness** (literal byte patterns). If LZ76 fails due to amplitude saturation but rank-order is preserved, PE recovers signal.

---

### 2.2 `sliding-window-lz76-temporal` — Tier A

**Slug genus**: `sliding-window-lz76-temporal`
**Reference**: Lempel-Ziv 1976 + Schartner 2017 (PLoS ONE 12:e0177096) per-window
**Hypothesis**: 60s recording → twelve 5s windows → b(t) array. Awake-resting yields b(t) ∈ [0.50, 0.90] across windows with σ_b ∈ [0.03, 0.15]; pure artifact yields b(t) flat-low or flat-high.

**5-check**:
- **Genus**: complexity-metric / temporal-window-decomposition
- **Frameworks**: Lempel-Ziv 1976 information-theory; Schartner 2017 clinical-PLoS
- **Channels**: 12 windows × 16ch = 192 b-values per session; window-length ∈ {2s, 5s, 10s}; overlap ∈ {0%, 50%}
- **Counter-example**: 60s synthetic flat-line → b(t) = 0.05 ± 0.01 across all windows (flat-low); 60s pink-noise → b(t) > 0.85 ± 0.03 (flat-high)
- **Falsifiers**:
  1. σ_b across 12 windows must be > 0.02 (artifact would be flat)
  2. At least 1 window must have b > 0.50 (any awake moment) — if ALL windows < 0.50 then artifact dominates everywhere
  3. b(t) autocorrelation lag-1 must be in (0, 0.8) — not pure-random, not pure-frozen
  4. Per-channel σ_b correlation between channels < 0.9 — channels should not move in lock-step (common-mode artifact signature)

**Verify-grid axes (K=6)**: {win=2s, win=5s, win=10s} × {overlap=0, overlap=50%}
**anima integration**: Re-uses `anima-clm-eeg/tool/clm_eeg_lz76_real.hexa` — call N times with --window/--start args.
**Cost**: ~30 LoC wrapper, zero new algorithm. Reproducibility: identical to existing LZ76 path.
**raw#12 compat**: This **refines** raw#12 frozen criteria — raw#12 evaluates session-level b; sliding-window exposes whether failure is uniform (hardware) or window-localized (transient artifact). If 11/12 windows pass and 1 fails, that's a different diagnosis than 12/12 fail.

---

### 2.3 `spectral-hjorth-band-ensemble` — Tier A

**Slug genus**: `spectral-hjorth-band-ensemble`
**Reference**: Hjorth 1970 (EEG Clin Neurophys 29:306) Activity/Mobility/Complexity; Klimesch 1999 alpha-band
**Hypothesis**: Awake-resting eyes-closed produces strong alpha (8-12 Hz) elevation; Hjorth Mobility increases monotonically with frequency-content broadening; rms-saturated artifact yields all bands flat (Hjorth Complexity → 1).

**5-check**:
- **Genus**: spectral-complexity / time-domain-derivative-statistics
- **Frameworks**: Hjorth 1970 time-domain spectral-equiv; standard delta/theta/alpha/beta/gamma band decomposition
- **Channels**: 16ch × 4 bands × 3 Hjorth stats = 192 features
- **Counter-example**: 60s sine 10Hz → Activity high, Mobility=10Hz, Complexity=1.0; 60s pink-noise → all 3 stats elevated; flat-line → all 3 stats=0
- **Falsifiers**:
  1. Alpha-band Activity (8-12Hz) on occipital ch (O1/O2) eyes-closed > non-occipital (Berger effect)
  2. Hjorth Complexity ratio band-to-band must vary > 1.5x (uniform-complexity = artifact signature)
  3. Cross-band Mobility ordering must match band centroid (delta < theta < alpha < beta < gamma)
  4. Activity sum across bands ≈ total signal variance (Parseval check — sanity gate)

**Verify-grid axes (K=12)**: 4 bands × 3 Hjorth stats
**anima integration**: anima/config/consciousness_laws.json phi_holo / phi_time gates can subscribe to Hjorth Mobility as time-axis feature.
**Cost**: ~80 LoC (FFT + band-pass + 3 statistics). 60s × 16ch in <2s.

---

### 2.4 `cross-frequency-coupling-theta-gamma` — Tier B

**Slug genus**: `cross-frequency-coupling-theta-gamma`
**Reference**: Canolty 2006 (Science 313:1626); Lisman & Jensen 2013 theta-gamma neural code
**Hypothesis**: Awake conscious processing exhibits theta-phase × gamma-amplitude coupling (modulation index MI > 0.005); rest/sleep/anesthesia diminishes MI.

**5-check**:
- **Genus**: mechanism-paradigm / phase-amplitude-coupling
- **Frameworks**: Canolty 2006 Science MI; Tort 2010 modulation-index normalized
- **Channels**: 16ch × theta-bands(4-8Hz) × gamma-bands(30-80Hz, 8 sub-bands) = 128 MI features
- **Counter-example**: white-noise → MI ~ 0.0001 (chance); structured awake → MI > 0.005
- **Falsifiers**:
  1. MI on shuffled-phase surrogate must be < 1/100 of MI on original (significance test)
  2. MI must be > MI_chance threshold (Tort 2010 KL-divergence p<0.05)
  3. Frontal-channel MI (Fp1/Fp2/F3/F4) > occipital MI (O1/O2) for cognitive paradigm — but for resting eyes-closed posterior dominance expected → directional check

**Verify-grid axes (K=8)**: 8 gamma sub-bands per theta phase
**Why Tier-B**: requires longer recording (≥3 min) for MI statistical significance with 16ch; current 60s borderline.
**anima integration**: theta-gamma coupling maps naturally to anima 8-axis G0~G7 stack — phi_meta / phi_holo time-binding.

---

### 2.5 `perturbational-complexity-index` — Tier C

**Slug genus**: `perturbational-complexity-index`
**Reference**: Casali 2013 (Sci Transl Med 5:198ra105); Casarotto 2016 (Ann Neurol 80:718)
**Hypothesis**: TMS pulse → 300ms EEG response → spatiotemporal LZ-complexity → PCI; awake 0.45-0.80, anesthesia 0.10-0.30, vegetative 0.05-0.30, locked-in 0.50-0.65.

**5-check**:
- **Genus**: perturbational-paradigm / external-stimulus-evoked-complexity
- **Frameworks**: Casali 2013 Sci-Transl-Med; IIT-Tononi theoretical anchor
- **Channels**: 16ch × 300ms post-pulse × 50 trials × 3 stim-sites = 7200+ axes
- **Counter-example**: sham-coil pulse (no magnetic field) → PCI ≈ 0; saline-bath response → PCI ≈ 0
- **Falsifiers**:
  1. PCI(real-pulse) > PCI(sham-pulse) by ≥ 3σ
  2. PCI awake-eyes-open > PCI eyes-closed-resting (replicates Casarotto 2016 Fig 2)
  3. PCI test-retest reliability > 0.8 (within-subject 2 sessions)
  4. Cortex stim-site PCI > deep-brain stim-site PCI (cortical excitability monotonicity)
  5. PCI saturation curve non-monotonic to TMS intensity (60-80% MT optimum)

**Verify-grid axes (K=15)**: 3 stim-sites × 5 intensities
**Why Tier-C**: requires TMS coil ($20-80K) + safety protocol + IRB-equivalent consent.
**anima integration**: PCI is **the** gold-standard for raw#12 strengthening — adds external-stimulus axis (raw#48 orthogonal-witness multiplied).
**raw#91 honest C3**: TMS hardware not in anima inventory; this candidate is **paper-design** until hardware acquired.

---

## 3. Recommended Top-3 Priority

### Priority 1 (immediate, today): `permutation-entropy-multiscale`
**Implementation plan**:
1. New tool `anima-clm-eeg/tool/clm_eeg_pe_real.hexa` (~50 LoC)
2. Read existing `recordings/sessions/baseline_resting_60s_20260428.npy`
3. For each 16ch × {d=3,4,5} × {tau=1,2,4} → emit PE
4. JSONL append `state/clm_eeg_lz76_audit/2026-04-28_pe.jsonl` (parallel to existing _lz76.jsonl)
5. Schartner-style threshold: PE_awake_eyes_closed expected 0.55-0.85
6. Honesty class per raw#91: REAL_HW_VERIFIED if data passes hardware sanity (impedance 16/16 GREEN) else NOT_VERIFIED
7. **No raw#12 modification** — PE runs additively, raw#12 frozen LZ76 path untouched.

### Priority 2 (immediate, wraps existing): `sliding-window-lz76-temporal`
- Wrapper script calling `clm_eeg_lz76_real.hexa` with --start / --end byte-offsets across 12 × 5s windows
- Output: 12 b values per channel + σ_b per channel
- Diagnoses whether D-day P1_FAIL is uniform (hardware) or transient (artifact-localized)

### Priority 3 (this week): `spectral-hjorth-band-ensemble`
- New tool with band-pass filters (already exist in anima-eeg/eeg.hexa pipeline) + per-band Hjorth
- Critical sanity gate: alpha (8-12Hz) elevation on O1/O2 eyes-closed validates Berger effect — this is the **single most diagnostic awake-EEG signature** and decides whether D-day raw signal is recoverable at all.

---

## 4. raw#47 cross-repo-trawl-witness — integration angle

| repo | locus | role |
|------|-------|------|
| `core/anima` | anima-eeg/, design/ | data + design doc + raw#12 frozen criteria |
| `core/anima/anima-clm-eeg` | tool/clm_eeg_lz76_real.hexa | existing LZ76 — Priority-2 wraps it; Priority-1 adds clm_eeg_pe_real.hexa parallel |
| `core/hexa-lang` | self/stdlib/hxc_a18_lz_ppm_order4.hexa | LZ-PPM compression infrastructure — analogous order-1 byte-context approach informs PE order-pattern statistics |
| `core/anima/anima/config/consciousness_laws.json` | 14 deterministic gates | phi_time / phi_holo can subscribe to Hjorth Mobility as time-axis feature |
| `core/nexus/roadmaps/anima.json` | (centralized) | adds top-3 candidates as roadmap items behind H100 stop-gate (memory feedback_h100_gate) |
| `core/airgenome` | (potential) | Phi-vector 16D EEG-cross-validation (Tier-C deferred) |

**Cross-repo SSOT touchpoints (memory project_uchg_ssot)**: design doc lives here; production roadmap entry deferred to nexus/roadmaps/anima.json under user discretion (this ω-cycle is discovery, not landing).

---

## 5. raw#91 honest C3 disclosure (speculative parts)

- **Tier-C `perturbational-complexity-index`**: TMS hardware **not in inventory** — paper-design only. anima cannot validate PCI without external lab partnership.
- **anima paradigm v11 G0~G7 × EEG integration**: integration spec **does not exist yet** — this is forward-looking design space, not validated.
- **τ(6)=4 universal × EEG transition number** (Axis B item 12): purely **speculative** numerology bridge — no mechanism documented; flagged as candidate-for-falsification not candidate-for-implementation.
- **L_IX irreversibility-embedded × EEG temporal asymmetry** (Axis B item 13): Mk.IX raw#30 references not cross-referenced to actual EEG temporal-asymmetry measurement protocol; **speculative bridge**.
- **Tier-A candidates 1/2/3**: implementable today but **unverified on real hardware** until executed; current D-day baseline_resting recording rms 884 µV vs normal 5-50 µV implies amplifier-scale or contact issue may dominate any new metric — top-3 candidates may **all** P1_FAIL on the same recording for the same hardware reason. Empirical falsification needed before claiming any new metric "works" on D-day data.
- **Cross-channel saturation hypothesis**: if rms is uniformly elevated across all 16ch, the issue is upstream of any complexity metric — Priority-3 (Hjorth alpha-on-O1/O2 Berger check) is the **gating sanity test**. Without Berger-effect signature, no Tier-A complexity metric can succeed on this recording.
- **Schartner 2017 reference range 0.5-0.9**: published on different hardware (BioSemi 64ch) and different binarization (median-split vs Hilbert-transform); cross-hardware threshold transfer is itself an open question (raw#117 frameworks-2+ requirement partially addressed, full cross-hardware calibration pending).

---

## 6. Genus / multi-realizability check (raw#106)

All 5 slugs use **genus** form, not implementation suffix:
- `permutation-entropy-multiscale` — NOT `pe-bandt-pompe-d3-tau1-py`
- `sliding-window-lz76-temporal` — NOT `lz76-12win5s-overlap0-hexa-impl`
- `spectral-hjorth-band-ensemble` — NOT `hjorth-fft-1024-band4-numpy`
- `cross-frequency-coupling-theta-gamma` — NOT `cfc-canolty-mi-tort-norm-thetabin18`
- `perturbational-complexity-index` — NOT `pci-casali-tms-300ms-magstim-rapid2`

Each genus admits multiple implementations (Hexa / Python / C / FPGA), multiple parameter choices (d, tau, window-len, band-edges), multiple frameworks (Bandt-Pompe / Olofsen / Canolty / Tort / Casali / Casarotto).

---

## 7. raw#48 multi-axis orthogonality of top-5

| candidate | primary axis | orthogonal-to |
|-----------|-------------|---------------|
| permutation-entropy-multiscale | order-pattern statistics | LZ76 (subsequence) / spectral / phase-coupling / perturbational |
| sliding-window-lz76-temporal | temporal decomposition | session-level / order-pattern / spectral / phase-coupling / perturbational |
| spectral-hjorth-band-ensemble | frequency-domain | order-pattern / temporal / phase-coupling / perturbational |
| cross-frequency-coupling-theta-gamma | phase-amplitude coupling | order-pattern / temporal / spectral-power / perturbational |
| perturbational-complexity-index | external-stimulus-evoked | all 4 above (spontaneous-EEG axes) |

Top-5 covers 5 distinct orthogonal axes — raw#48 satisfied.

---

## 8. Follow-up agent dispatch recommendation

**Recommended single follow-up agent** (after user approval, NOT auto-launched):
- **Slug**: `eeg-pe-multiscale-implement-tier-a-priority-1`
- **Scope**: implement `clm_eeg_pe_real.hexa` (~50 LoC), run on existing baseline_resting_60s_20260428.npy, append to `state/clm_eeg_lz76_audit/2026-04-28_pe.jsonl`, **read-only** with respect to raw#12 frozen LZ76 path.
- **Gate**: H100 stop-gate (memory feedback_h100_gate) **does not apply** — this is local CPU compute on existing recording.
- **Honest C3 budget**: agent must classify each of {raw, filtered} × {d=3,4,5} × {tau=1,2,4} × 16ch as REAL_HW_PASS / REAL_HW_FAIL / NOT_VERIFIED per raw#91.
- **Falsifier gate**: 5 falsifiers from §2.1 must be evaluated; agent reports per-falsifier verdict.

**NOT recommended for auto-dispatch**:
- Priority 2 (sliding-window-LZ76) — wait for PE result first to triangulate
- Priority 3 (Hjorth) — should run **first** ideally as alpha-Berger sanity gate, but requires more LoC; bundle with Priority 1 in single human-confirmed dispatch.

**Recommendation**: present this design doc to user, await approval to dispatch single Tier-A agent for Priority-1 (PE) **and** Priority-3 (Hjorth alpha-Berger sanity) bundled as one ω-cycle continuation.

---

## 9. raw#117 5-check final

| check | status |
|-------|--------|
| genus naming | ✓ all 5 candidates use genus form (§6) |
| frameworks ≥2 | ✓ each candidate cites 2+ frameworks (Bandt-Pompe + Olofsen, LZ + Schartner, Hjorth + Klimesch, Canolty + Tort, Casali + Casarotto) |
| channels ≥3 | ✓ each candidate has K≥6 verify-grid axes |
| counter-example | ✓ each candidate has explicit synthetic counter-example |
| falsifiers ≥3 | ✓ each candidate has 3-5 falsifiers (raw#71 satisfied) |

raw#117 5-check **passed** for all 5 candidates.
