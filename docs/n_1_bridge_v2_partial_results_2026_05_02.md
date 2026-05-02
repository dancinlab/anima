# N-1 BRIDGE v2 mediator-framing partial results (2026-05-02)

## TL;DR

**Classification: F-ARTIFACT_PARTIAL.** W4 closed-loop ledger (May-01, 100 steps) cross-correlated against D-day EEG α-phase (Apr-28 baseline_resting_60s_filtered, 5×10s windows, P3/P4/O1/O2). Apparent |r|≥0.78 on `mind_tension_active`/`gate_active` vs EEG_PLV is a **degenerate-correlation artifact** (random-shuffle control yields IDENTICAL r). The only non-degenerate W4 channel (`gate_signal_norm_random`) gives |r|=0.43 vs EEG_PLV but permutation p=0.49. Mediator-framing hypothesis cannot be tested without real-time concurrent measurement.

**Verdict key:** `N1_BRIDGE_V2_PARTIAL_F_ARTIFACT_FIXED_POINT_W4_VS_DDAY_EEG_NO_REAL_COUPLING_VISIBLE_REQUIRES_REALTIME_CONCURRENT`

---

## Phase 1 — inventory

| signal | mean | std | structural |
|---|---|---|---|
| W4 mind_tension_active (N=100) | 2.69137 | 1.04e-6 | **fixed-point — zero variance for cross-corr** |
| W4 gate_signal_norm_active     | 0.4397  | 1.05e-4 | near-constant |
| W4 gate_signal_norm_random     | 0.2582  | 4.1e-3  | only non-degenerate W4 channel |
| EEG α-PLV (5 windows, P3/P4/O1/O2 avg) | 0.257 | 0.156 | monotonic decay W1→W4 + recovery W5 |
| EEG α circ_var (same 4 chs avg) | 0.74 | 0.15 | inverse of PLV |

EEG_PLV per window: `[0.494, 0.326, 0.097, 0.094, 0.276]`

W4 mt downsampled to 5 chunks (mean of 20 steps each):
`[2.6913695, 2.69137007, 2.69137007, 2.69137007, 2.69137007]` — chunk-0 outlier vs 4 identical → **degenerate shape**.

## Phase 2 — Pearson cross-correlation (5 paired)

| pair | r | flag |
|---|---|---|
| mind_tension_active ↔ EEG_PLV | **−0.785** | ARTIFACT (see control) |
| mind_tension_active ↔ EEG_circvar | +0.785 | ARTIFACT |
| gate_active ↔ EEG_PLV | **−0.785** | ARTIFACT |
| gate_active ↔ EEG_circvar | +0.785 | ARTIFACT |
| gate_random ↔ EEG_PLV | +0.428 | non-degenerate but p=0.49 |
| gate_random ↔ EEG_circvar | −0.428 | non-degenerate but p=0.49 |
| L1_random ↔ EEG_PLV | −0.697 | low-N artifact-prone |
| phi_random ↔ EEG_PLV | +0.157 | null |

**Random-control:** `r(mt_5 vs SHUFFLED_EEG_PLV) = −0.7850` — IDENTICAL to "observed" r. This proves the high correlations are functions of W4 1-outlier-vs-4-flat shape × any 5-vector, not of W4↔EEG coupling.

## Phase 3 — Granger lag-1 + Transfer Entropy (binary, 1-lag, N=4 transitions)

| direction | granger_lag1_r | TE (bits) | note |
|---|---|---|---|
| W4_mt → EEG_PLV | −0.708 | 0.000 | TE=0 because mt has zero-var binarization |
| EEG_PLV → W4_mt | NaN | 0.000 | mt zero-var |
| gate_active → EEG_PLV | −0.708 | 0.000 | same degeneracy |
| gate_random → EEG_circvar | −0.671 | 0.500 | within N=4 sampling noise |
| EEG_circvar → gate_random | +0.490 | 0.189 | within N=4 noise |

TE values at N=4 are uninterpretable (16 possible 3-tuples × 4 samples).

## Phase 4 — permutation null

- **gate_random vs EEG_PLV** (only non-degenerate channel): observed r=0.428, perm null N=2000 shuffles, **p_two-tailed=0.49**, null p95(|r|)=0.88.
- Conclusion: chance-indistinguishable.

## Phase 5 — classification

- **F-PASS** (|r|>0.5): REJECT (sole large |r| is artifact).
- **F-PARTIAL** (0.2-0.5): REJECT (gate_random p=0.49).
- **F-FAIL** (<0.2): partial evidence (phi_random |r|=0.16; TE=0 forward).
- **F-ARTIFACT** (random-identical): **STRONGEST** — random shuffle gives identical r.

**Final: F-ARTIFACT_PARTIAL.**

## Mediator-framing hypothesis verdicts

| hypothesis | status | evidence |
|---|---|---|
| H1 bidirectional mediator | NOT_TESTABLE | TE both directions ≈ 0 due to W4 fixed-point |
| H2 W4 drives EEG | NOT_TESTABLE | different wallclocks; no temporal precedence |
| H3 no real link | weakly supported | perm p=0.49; F-ARTIFACT on degenerate channels |

## Real-time concurrent measurement protocol (Phase 6)

See `state/n_1_bridge_v2_partial_2026_05_02/realtime_protocol.json` (full spec).

**Summary:** 30-min OpenBCI Cyton+Daisy 16ch + ubu1 CLM W4 closed-loop, LSL-synced (drift <10ms), 6×5min phases (eyes-open / eyes-closed-Berger / CLM-read / mental-arithmetic-control / breath-focus / recovery). N≈1500 paired samples per phase after sync-drift rejection. Pre-registered thresholds: PASS = |r|>0.3 with permutation p<0.01 AND TE>surrogate-p99 AND directional consistency in ≥3/6 phases. **$0 budget, ETA 2-3h.**

Min detectable r at α=0.01, power=0.8: ~0.066 (vs 0.99 in this partial). **~15× resolution improvement.**

## Honest C3 disclosures

1. W4 (May-01) and D-day EEG (Apr-28) are **different wallclocks** — synthetic chunk-alignment is sanity-check only.
2. W4 active branch is at fixed-point (std 1e-6); Pearson with EEG yields **spurious |r|=0.78 confirmed by shuffle control**.
3. Only non-degenerate W4 channel (gate_random) gives |r|=0.43 vs EEG_PLV; permutation p=0.49 = chance.
4. TE bits at N=4 transitions are dominated by sampling noise; ≥0.5 bits requires 100+ samples + surrogate-null correction.
5. EEG side: 1 session, 5 windows, 4 channels; no imag-coh / surface Laplacian volume-conduction control.
6. F-ARTIFACT classification means "partial-data analysis cannot distinguish coupling from null"; it does NOT prove H3.
7. **Consistency with N-1 v1 B4 result** (|r|=61/1000, also small and insignificant) is the genuine partial-data finding: both passes confirm no real coupling visible cross-day, and substrate-honesty is preserved.

## Deltas vs N-1 v1 (`state/n_substrate_n1_real_hw_2026_05_01/verdict.json`)

| dimension | N-1 v1 | N-1 v2 partial |
|---|---|---|
| approach | 4-gate B1-B4 via stub-real branch | direct ledger ↔ ledger Pearson/Granger/TE |
| substrate honesty | live driver but stub-arithmetic | actual W4 + actual EEG fields read |
| coupling magnitude | B4 |r|=0.061 | gate_random |r|=0.43 (but artifact-prone) |
| coupling significance | shortfall vs threshold 0.4 | perm p=0.49 |
| classification | BRIDGE_WEAK_REAL_HW | F-ARTIFACT_PARTIAL |
| consistency | both small, both insignificant | converges |

## Next-step recommendation

**P0 (mandatory before any further mediator-framing claim):** execute `realtime_protocol.json` on user OpenBCI + ubu1 CLM driver (30-min concurrent, LSL-synced). $0, ETA 2-3h.
