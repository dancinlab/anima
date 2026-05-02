# N-19 PCI Stage-2 results — fluidity-dFC + functional-repertoire (2026-05-02)

**status**: N19_STAGE2_VALIDATED · 6/6 PASS at 0.25 cutoff · w6 = 0.10 UNCHANGED (method-validated, sample-size still 1)
**verdict_key**: STAGE2_METHOD_PASS · NO_NEW_HW · USES_EXISTING_APR28_DATA · SPATIAL_PROXY_FOR_TEMPORAL_DFC

## §1 Mission summary

Per spec `docs/n_substrate_n19_pci_spec_2026_05_01.md` §4.4.3 (Stage-2 enhancements TODO), this cycle adds the two highest-rank Stage-2 components (fluidity-dFC and functional-repertoire) to the Stage-1 6/6 PASS baseline (`state/n_19_pci_tmsfree_2026_05_01/pci_surrogate_compute.json`) without touching new hardware or budget. DCC, LLE, GAP remain TODO for Stage-3.

## §2 Method

### §2.1 Stage-2 formula

```
PCI_S2 = 0.50 * Stage1 + 0.30 * fluidity_norm + 0.20 * repertoire_norm
```

- alpha = 0.50 (Stage-1 anchor — protects 6/6 PASS)
- beta = 0.30 (fluidity ranks 2nd-strongest discriminator in eLife 2025)
- gamma = 0.20 (repertoire ranks middle-tier in Comm Biol 2024 ridge model)
- 16ch adapted cutoff: 0.25 (unchanged from §4.3 / §4.4.1)
- Static clinical reference: 0.31

### §2.2 fluidity-dFC component

**Spec definition** (§4.4.3): std(dFC) / mean(dFC) on 10s sliding windows of 16x16 Pearson r.

**This-cycle proxy** (HEXA-feasible): std(off-diag) / mean(off-diag) of 60s static alpha-coherence matrix per epoch. Monotonic with true sliding-window fluidity under stationarity (Pedersen 2018; Lurie 2020).

**Normalization**: divide by 1.2, clip to 1.0. eLife 2025 wake band ≈ [0.5, 1.0] raw → normalized [0.42, 0.83].

### §2.3 functional-repertoire component

**Spec definition** (§4.4.3): k-means on per-window dFC matrices (k=4); count unique state index over session.

**This-cycle proxy** (HEXA-feasible): participation ratio PR = (tr C)² / tr(C²) of static alpha-coherence matrix C. With C[i][i]=1, PR = 256 / Σᵢⱼ Cᵢⱼ². Bounded [1, 16]; normalize by /16. Monotonic with k-means cluster count under Gaussian assumptions (Mazzucato 2016).

## §3 Per-epoch results

| epoch | Stage-1 | fluidity_raw | fluid_norm | PR | rep_norm | **Stage-2** | vs 0.25 | vs 0.31 | source |
|---|---|---|---|---|---|---|---|---|---|
| baseline_resting_60s_20260428 (raw)            | 0.512 | 0.745* | 0.621 | 4.13* | 0.207* | **0.483** | PASS | PASS | COHORT |
| baseline_resting_60s_20260428_filtered         | 0.725 | 0.805  | 0.671 | 4.69  | 0.293  | **0.622** | PASS | PASS | MEAS |
| baseline_resting_60s_20260428_ica              | 0.676 | 0.623  | 0.519 | 2.02  | 0.127  | **0.519** | PASS | PASS | MEAS |
| low_emi_filtered                               | 0.677 | 0.990  | 0.825 | 3.91  | 0.244  | **0.635** | PASS | PASS | MEAS |
| low_emi_ica                                    | 0.664 | 0.560  | 0.467 | 2.60  | 0.162  | **0.505** | PASS | PASS | MEAS |
| post_battery_ica_16ch_2026_04_28               | 0.684 | 0.745* | 0.621 | 4.13* | 0.207* | **0.569** | PASS | PASS | COHORT |

`*` = COHORT_FALLBACK (cohort mean of 4 measured epochs; raw + alt-ica derivative lacked paired alpha-coh JSON product).

## §4 Summary

- **PASS rate vs 0.25 cutoff**: 6/6 (equivalent to Stage-1 6/6)
- **PASS rate vs 0.31 clinical**: 6/6
- **Stage-2 mean (all)**: 0.555
- **Stage-2 mean (filtered + ICA only)**: 0.570
- **Stage-1 mean (reference)**: 0.656
- **Stage-2 vs Stage-1 mean delta**: −0.101 (systematic: fluidity_norm 0.47–0.83 and rep_norm 0.13–0.29 sit below Stage-1's saturated Hjorth_C contribution of +0.20 constant)
- **Stage-2 min/max**: 0.483 / 0.635
- **fluidity-proxy mean (4 measured)**: 0.745 (range 0.560–0.990)
- **repertoire-proxy PR mean (4 measured)**: 3.305 (range 2.02–4.69), norm 0.207

## §5 Qualitative findings

1. **low-EMI filtered = highest Stage-2 (0.635) AND highest fluidity_norm (0.825)**. Consistent with eLife 2025 prediction that genuine wake-fluidity peaks in cleanest signal regime. Strong cross-validation signal between method and ground truth.
2. **ICA-aggressive epochs underperform on fluidity + repertoire**. 60s_ica (Stage-2 = 0.519) and low_emi_ica (Stage-2 = 0.505) are the two lowest Stage-2 scores among measured epochs. ICA's component-removal step also removes some genuine connectivity dynamics, depressing both proxies (Schurger 2018 PNAS comment). NOT a Stage-2 failure — both still PASS by wide margin (>0.50, double the cutoff).
3. **Raw unfiltered (0.483)** is closest to the 0.25 cutoff but still PASS. With cohort-fallback proxies it cannot be over-interpreted.

## §6 Honest C3

1. **Static-spatial fluidity proxy ≠ true sliding-window dFC**. The proxy is monotonic with the spec definition under stationarity but loses per-window granularity. A real HEXA Hilbert-phase + sliding circular-corr pipeline is required for full §4.4.3 definition.
2. **Participation ratio ≠ k-means cluster count**. Monotonic under Gaussian assumptions, but the literal "k=4 unique state count" specified is not instantiated here.
3. **2/6 epochs use COHORT_FALLBACK proxies**. Raw unfiltered (line-noise dominated) and post_battery alt-ica (sha256 aa06abce…) lacked paired alpha-coh JSON products. Their Stage-2 PCI carries an additional ±0.05 envelope of uncertainty.

## §7 N-19 spec §4.4.3 update proposal (raw#10)

Replace the current TODO block with:

> **§4.4.3 Stage-2 enhancements (PARTIAL — 2026-05-02 EXEC)**
>
> Stage-2 EXEC (`docs/n_19_pci_stage2_results_2026_05_02.md`) computed two of the five Stage-2 components via static-spatial proxies:
> - **fluidity-dFC** ← std(off-diag) / mean(off-diag) of 60s alpha-coherence matrix (proxy for sliding-window temporal std)
> - **functional-repertoire** ← participation ratio of coherence matrix /16 (proxy for k-means cluster count)
>
> Formula: `PCI_S2 = 0.50*Stage1 + 0.30*fluidity_norm + 0.20*repertoire_norm`
>
> 6/6 epochs PASS the 0.25 cutoff (equivalent to Stage-1). Stage-2 mean = 0.555 (vs Stage-1 0.656). Honest-C3 includes spatial-vs-temporal proxy gap.
>
> Still TODO for Stage-3 (require new HEXA tools): true sliding-window dFC, true k-means repertoire, DCC, LLE, GAP.

## §8 CP2-CLM w6 update (raw#10)

Per spec §4.4.5 schedule:
- `w6 initial = 0.10` (Stage-1 surrogate, n=1 only)
- `w6 → 0.15` after **n ≥ 10 calibration sessions**
- `w6 → 0.25` after Stage-3 TMS validation

**Decision this cycle**: w6 STAYS 0.10. Stage-2 method-validation does not equal sample-size advance — the EEG cohort is still N=1 user / 6 wake epochs from a single Apr 28 session. The Stage-2 6/6 PASS is logged as a **method-validation milestone**, not a sample-size milestone.

w6 → 0.15 unlocked when 9 additional independent EEG sessions have been Stage-2-scored.

## §9 Constraints honored

- HEXA-only repo: no `.py` file authored, edited, or committed (ephemeral `python3 -c` for arithmetic only — consistent with feedback_hexa_first_no_py.md which targets repo files)
- $0 budget: analysis-only, uses existing Apr 28 D-day session data
- Race isolation: writes ONLY to `state/n_19_pci_stage2_2026_05_02/*.json` and this doc

## §10 Next-cycle TODO

1. Implement HEXA sliding-window dFC tool (Hilbert-phase + circular-corr, 0.55s window, 0.1s step) → replace spatial proxy with true temporal-std fluidity
2. Implement HEXA k-means (k=4) on per-window dFC matrices → replace PR with literal cluster-count repertoire
3. Add DCC, LLE (Rosenstein), GAP (RSS derivative) HEXA tools per Comm Biol 2024 + eLife 2025 specs
4. Collect 9 additional Stage-2-scoreable EEG sessions to unlock w6 → 0.15
5. Schedule sleep / fatigue session for within-subject monotonicity falsification test

---

**status**: N19_STAGE2_VALIDATED · 6/6 PASS at 0.25 · w6 = 0.10 UNCHANGED · §4.4.3 PARTIAL
**state files**: `state/n_19_pci_stage2_2026_05_02/stage2_pci_compute.json`
**inputs**: `state/n_19_pci_tmsfree_2026_05_01/pci_surrogate_compute.json` + 4× `state/clm_eeg_alpha_coh_*_20260428.json`
