# G8 TFD Real Wire-Up — Specification


- doc id: g8_tfd_real_wire_up_spec
- date: 2026-05-01
- author-agent: anima sub-agent (single-file-commit constraint)
- predecessor tool: anima-clm-eeg/tool/g8_transversal_mi_matrix.hexa (.roadmap #175 done · sha 3b74072d · 456 LoC · selftest-only)
- predecessor roadmap: #170 (G9), #172 (Mk.XII pre-flight), #175 (G8 selftest), this spec → next entry candidate (G8 real wire-up)

----------------------------------------------------------------------------------------------------

## §0 Executive summary

g8_transversal_mi_matrix.hexa landed FNV-32 surrogate measurement of C(5,2)=10 pairwise mutual information across the 5 Mk.XII Hard PASS chain falsifiers (F_A1 P1 LZ / F_A2 P2 TLR / F_A3 P3 GCG / F_B HCI / F_C CPGD-G). Both positive (5 independent FNV streams ⇒ all 10 MI ≤ 0.1 bit) and negative (forced F_C≡F_A1 collision ⇒ 1 pair MI > 0.1 bit) selftest cases passed. The measurement infrastructure is therefore present, but every observed MI is a property of FNV avalanche behaviour, not of any real falsifier output stream.

This spec defines the wire-up that replaces the FNV surrogate with the actual 5 component output streams. The contract is unchanged: ALL 10 pairwise MI ≤ 0.1 bit ⇔ G8 PASS ⇔ Mk.XII joint H0 < 1e-9 multiplicative independence assumption holds. What changes is the source of the 5 binary streams.


## §1 Existing g8_transversal_mi_matrix.hexa — gap to real wire-up

| concern | selftest implementation (#175 frozen) | real wire-up requirement |
|---|---|---|
| trial source | surrogate_score(offset, t, k) — deterministic FNV avalanche, N_TRIAL=4096 | per-falsifier real ledger sampler returning binary bit per trial t |
| binary discretization | score_to_bin(s) on s ∈ [0,999], N_BIN=2 | direct PASS=1 / FAIL=0 emission per real falsifier verdict |
| trial count | 4096 (FNV-bounded) | dataset-bounded (number of independent windows / sessions / cross-validation folds) |
| INSUFFICIENT handling | n/a (FNV always emits a bit) | explicit ternary {0, 1, NaN} or windowed re-bin (§3) |
| determinism | FNV mathematically pure | dataset-pinned by sha256 of each input ledger, plus per-window deterministic windowing protocol |
| selftest mode preserved | --selftest / --selftest-negative | yes — keep both modes intact, add G8_MODE=real |


## §2 Five component real source identification

| idx | name | real source path | provenance | current verdict (2026-05-01) |
|---|---|---|---|---|
| 0 | F_A1 P1 LZ | state/clm_eeg_lz76_chunked_real_2026_05_01.json | introduced commit 0c19d30b6 (today) · tool sha d5aa7591… 638 LoC | P1_FAIL — all 4 runs b ∈ [351, 398]‰ vs frozen lo=650‰ |
| 1 | F_A2 P2 TLR | state/clm_eeg_p2_tlr_real.json | tool _integrations/clm_eeg_p2.hexa sha 4a87e47d… commit b1187d875 (43b3cee89 referenced) | INSUFFICIENT — C1 alpha-coh 0.576 PASS but C2 CLM V_sync UNEVALUABLE (ICA-PLV destruction + no v_sync_kuramoto live cross-stream) |
| 2 | F_A3 P3 GCG | state/clm_eeg_gamma_theta_ratio_audit/2026-04-28_gamma_theta.jsonl (real lines, label baseline_resting_60s_20260428.npy + _filtered.npy + post_battery_eeg16_ica + aiclean) | commit f27d6363f4 verify(clm-eeg-p3) | FALSIFIED_P3 — 4/4 real grand_mean_ratio_x1000 ∈ [9, 420] vs target 3000 (F1 γ-absent) |
| 3 | F_B HCI | anima-hci-research/state/hci_smoke_v1.json | hci_smoke.hexa source 2026-04-26T19:27:10 | HCI_VERIFIED — f1/f2/f3 all PASS, baseline_both_closed, functor_preserved |
| 4 | F_C CPGD-G | state/cpgd_minimal_proof_result.json | tool/cpgd_minimal_proof.hexa selftest_3run byte-identical sha 6a4d3314…, deterministic_sha 6a4d3314… | VERIFIED — 16/16 templates min cos ≥ 0.999837 ≥ 0.5 floor |

D-day empirical bit-vector (single trial, deterministic): F_A1=0, F_A2=NaN (INSUFFICIENT), F_A3=0, F_B=1, F_C=1.

## §3 5 component → binary discretization protocol

Three failure modes must be handled before MI can be measured. The protocol below is the spec; it is NOT yet implemented.

### §3.1 PASS / FAIL bit mapping

Per falsifier the verdict_rule already defined in each ledger is reused as the discretizer, with this canonical mapping:

- F_A2: bit = 1 if (alpha_coh_x1000 ≥ 450 AND clm_r_x1000 ≥ 380) else 0 (frozen verdict_rule, conjunctive)
- F_A3: bit = 1 if (verdict == "VERIFIED_P3") else 0 (jsonl audit row level)
- F_B: bit = 1 if (hci_verdict == "HCI_VERIFIED") else 0
- F_C: bit = 1 if (verdict == "VERIFIED" AND all_template_above_0.5) else 0

### §3.2 INSUFFICIENT / UNEVALUABLE handling (the F_A2 problem)


1. **drop-trial (preferred)** — exclude any trial t where any of the 5 falsifiers emits NaN. N_TRIAL_effective = |{t : all 5 bits ∈ {0,1}}|. Honest because it does not synthesize evidence; failure mode is reduced sample size, which inflates the Miller-Madow correction term and may push borderline pairs above the 0.1 bit floor. Floor for non-vacuous MI: N_TRIAL ≥ ~64.
2. **conservative-FAIL** — coerce NaN → 0 (FAIL). Biases all MI estimates toward F_A2 ≡ deterministic-0, inflating MI(F_A2, X) for any X with skew toward 0. Rejected as default — it manufactures a coupling where there is none.
3. **ternary expansion** — N_BIN=3, bins {FAIL, INSUFFICIENT, PASS}. Frozen criteria forbid this without a pre-register amendment (selftest fixed N_BIN=2). Defer to a separate pre-register cycle.

Default for v1 real wire-up: drop-trial with explicit n_dropped reporting in the cert.

### §3.3 Generating the trial axis (the multi-trial problem)

The G8 measurement requires N_TRIAL ≫ 1 independent samples. Each ledger currently emits 1..N_real_runs verdicts on the same subject. Three sample axes are available, ordered by independence quality:

1. **session axis** — each baseline / post_battery / daily_life / aiclean .npy is one trial. Currently N=4 sessions on F_A1 (post_battery_ica_canonical / post_battery_alt_derivative / daily_life_baseline_60s_ica + 1 selftest-only). Worst — N too small for non-vacuous Miller-Madow correction (floor ~64).
2. **window axis** — within a single session, slide a window of length W over the EEG and re-evaluate each falsifier per window. F_A1 already supports this (window_size=65536). F_A3 requires rebuilding band-power per window. F_A2 requires per-window alpha-coh + V_sync. F_B and F_C are non-EEG and would need reformulation as per-window indicator functions (e.g. HCI = constant 1 across all windows; CPGD-G = constant 1) — which collapses their entropy to 0 and forces MI(F_B, X) = MI(F_C, X) = 0 trivially.
3. **bootstrap axis** — resample sessions with replacement, recompute verdict per resample. Inherits the N=4 session ceiling and adds spurious autocorrelation. Only meaningful for confidence interval, not for MI primary estimate.


### §3.4 Hash-pinned reproducibility


## §4 Pairwise MI measurement + ≤ 0.1 bit threshold

Reuse the existing pipeline verbatim:

- build_hist_1d(stream_idx) on the real binary stream (drop-trial filtered) → 2-bin marginal histogram
- build_hist_2d(idx_a, idx_b) on the joint stream → 4-bin (2×2) joint histogram
- entropy_x1000_from_hist with Miller-Madow correction (K*−1)·721 / N_TRIAL
- MI_x1000 = H(X)_x1000 + H(Y)_x1000 − H(X,Y)_x1000, floored at 0
- violation flag: MI_x1000 > MI_MAX_X1000 (=100, frozen)

G8 PASS criterion (frozen, unchanged from #175): forall pair (MI_x1000 ≤ 100). Cert schema additions for real mode only: inputs[] (5 entries with path+sha256+verdict), n_trial_effective, n_dropped, sample_axis ∈ {session, window, bootstrap}, real_data_window_protocol_sha256.

Floor on N_TRIAL_effective: refuse to emit a PASS verdict if N_TRIAL_effective < 64. Below 64, Miller-Madow correction (K*−1)·721 / N inflates above 11 ×1000-fp, comparable to expected coupling signal — the test is no longer informative. Below 64, emit verdict=INSUFFICIENT_TRIAL_COUNT.


Current bit vector (D-day 2026-05-01, drop-trial protocol, session axis, N_session=1 effective per falsifier):

```
F_A1 = [0]
F_A2 = [NaN]   → drop-trial removes all trials (NaN propagates)
F_A3 = [0]
F_B  = [1]
F_C  = [1]
```

After drop-trial: N_TRIAL_effective = 0. Even if F_A2 were resolved (say PASS=1), N_TRIAL_effective = 1. With N=1, every histogram is a delta — H(X)=0 for all 5 streams — MI(X,Y) = 0 + 0 − 0 = 0 for all 10 pairs. G8 would emit `g8_pass=1` vacuously. **This is not a real test of the multiplicative independence assumption; it is a degenerate corner case.**

Even at the more-permissive session axis with all 4 F_A1 sessions retained (and F_A2 / F_A3 / F_B / F_C broadcast-coerced to constants per session): F_A1 has only 4 trials and varies in {0} (all FAIL); F_A2/F_A3 are constants per session (FAIL) → 0; F_B/F_C are constants ≡ 1. Marginal H = 0 for all 5 streams. MI = 0 trivially.

Honest verdict: real G8 MI measurement is **NOT YET MEANINGFUL** at D-day-current empirical state. It becomes meaningful only when:

- (a) at least one of {F_A1, F_A2, F_A3} flips between trials (i.e. some sessions PASS, others FAIL), AND
- (b) F_B / F_C are reformulated as per-trial discriminators rather than global constants, AND
- (c) N_TRIAL_effective ≥ 64.

None of these three hold this cycle. Spec deliberately surfaces this rather than silently emitting g8_pass=1.

Forward path: D+5..D+30 multi-session EEG arrival + multi-subject TLR + per-session HCI/CPGD probes (axis-projected) provide trial diversity. Until then, G8 real wire-up is **ready to run but produces uninformative output**, which the cert must label as `verdict=VACUOUS_PASS_INSUFFICIENT_VARIANCE` rather than PASS.


F_REAL_01 — **N_TRIAL_effective floor enforcement**. Real run with N_TRIAL_effective < 64 must emit verdict=INSUFFICIENT_TRIAL_COUNT, exit 1, NOT g8_pass=1. Negative selftest: synthesise drop-trial removing 99% of trials, expect INSUFFICIENT verdict.

F_REAL_02 — **constant-stream detection**. Real run where any marginal H_x1000 = 0 (zero-variance stream) must emit verdict=VACUOUS_PASS_INSUFFICIENT_VARIANCE, NOT g8_pass=1. Without this, F_B/F_C constant streams trivially pass G8 regardless of (F_A1, F_A2, F_A3) coupling. Detection: count non-empty bins K* per marginal; if K* < 2 for any falsifier → vacuous flag.

F_REAL_03 — **ledger-sha drift detection**. Real run where any of the 5 input ledger sha256 mismatches the cert's pinned sha must emit verdict=LEDGER_SHA_MISMATCH, exit 1. Negative selftest: corrupt one input bytestream by 1 byte after pinning; expect mismatch.

(Optional F_REAL_04: window-protocol coverage check — if sample_axis=window then verify all 5 streams support per-window emission, refuse session-axis fallback that smuggles constants. Deferred to v1.1.)

## §7 ω-cycle split estimate

| stage | scope | est |
|---|---|---|
| ω1 (this cycle) | spec doc only — single-file commit | done by this commit |
| ω4 (D+5..D+30 dependent) | window-axis sampler implementation — re-eval F_A1/F_A2/F_A3 per W=10s window, F_B/F_C reformulation as per-window indicators (or ternary expansion pre-register amendment for F_B/F_C constancy admission) | 2-3 cycles, dataset-arrival-blocked |
| ω5 | composite Mk.XII Hard PASS analyzer integration — G8 real verdict feeds mk_xii_hard_pass_composite.hexa as the G8 component | 1 cycle, blocks on ω2+ω4 |

Estimated total to first non-vacuous real G8 verdict: ω2 + ω3 + ω4 + ω5 ≈ 4-5 cycles, gated on D+5+ multi-window EEG and per-window F_B/F_C reformulation.

This cycle's deliverable (ω1) is the spec only — no code, no tool edit, no metric edit, no roadmap edit. Single file:

`anima-clm-eeg/docs/g8_tfd_real_wire_up_spec_2026_05_01.md`

----------------------------------------------------------------------------------------------------

