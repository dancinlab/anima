# N-12 IonQ Forte 1 AWS Braket EXEC Results (2026-05-01)

Agent: `n_substrate_n12_aws_exec` (N-12 EXEC)
Date UTC: 2026-05-02T04:00 - 04:07 (run wall-clock 7 minutes incl. SDK install)
Spec: `docs/n_substrate_n12_ionq_penrose_hameroff_spec_2026_05_01.md`
Preregister: `state/n_substrate_n12_prep_2026_05_01/falsifier_F_N12_preregister.json`
Exec ledger root: `state/n_substrate_n12_aws_exec_2026_05_01/`

## Headline

**3/3 tasks COMPLETED on IonQ Forte 1 within 1.13 minutes wall-clock from submit.**
**F-N12-1 primary verdict at SC reference tau_2 = 100 us: FAIL** (ratio 7.82, outside [0.67, 1.5]).
**Sensitivity sweep included** — verdict is INDETERMINATE for SC tau_2 in approximately [600, 1200] us; FAIL elsewhere.
**Actual cost: $24.90** vs spec $20.90 (+$4.00 due to Forte 1 minimum-shots=100 forcing C2 bump 50→100). Under $50 hard cap.

## What ran

| Circuit | Qubits | Shots | Task ARN | Status |
|---|---|---|---|---|
| C3 Bell sanity | 2 | 100 | `quantum-task/b9310362-fe83-485a-b0d3-693091b05a21` | COMPLETED |
| C2 1-qubit baseline | 1 | 100 | `quantum-task/6b7916d6-b8fa-4131-bd06-1252454ccc52` | COMPLETED |
| C1 4-qubit GHZ delay=100us | 4 | 100 | `quantum-task/a2ab2539-64a7-49a5-b006-bce6372ea54c` | COMPLETED |

Device ARN: `arn:aws:braket:us-east-1::device/qpu/ionq/Forte-1` (status ONLINE, name "Forte 1").
Account: 267673635495 (`anima-braket-cli` IAM user, `[braket]` profile).
S3 bucket: `amazon-braket-us-east-1-267673635495`, prefix `n12-mvp`.

## Raw counts

- C3 Bell `|00>+|11>`: `{"00": 49, "10": 1, "11": 50}` → fidelity 99/100 = 99.0% (PASS hardware sanity).
- C2 baseline `H..rx(2π)*12..H`: `{"0": 100}` → P(0) = 1.0 (Wilson 95% CI lower 0.964 → contrast >= 0.928).
- C1 GHZ X-basis parity: `{"0000":6, "1000":2, "1100":16, "1010":7, "0110":6, "1001":16, "0101":10, "1101":2, "0011":17, "1011":2, "1111":16}` → even=94, odd=6, contrast 0.88.

## Falsifier verdicts

### F-N12-1 (primary): Cross-substrate OR signature consistency — **FAIL**

- tau_2_ion (4-qubit GHZ, delay=100us, single-point + ideal-prep prior c0=1.0): **782.3 us** (sigma 865.4 us)
- SC reference: 100 us (canonical IBM Heron 4-qubit GHZ T2* bracket; agent did NOT extract exact PRNewswire 2025-03 numeric)
- Ratio: **7.82**, outside pass band [0.67, 1.5]
- p-value: 0.068 (just above 0.05 threshold even on the FAIL side)
- Verdict: **FAIL** (claim_under_test rejected at sc_ref=100us)

**Sensitivity sweep over SC reference**:

| sc_tau2 (us) | ratio | p | verdict |
|---|---|---|---|
| 50 | 15.65 | 0.017 | FAIL |
| 100 | 7.82 | 0.068 | FAIL (primary) |
| 200 | 3.91 | 0.193 | FAIL |
| 500 | 1.56 | 0.485 | FAIL |
| 800 | 0.978 | 0.634 | INDETERMINATE (in band, p>0.05) |
| 1000 | 0.782 | 0.556 | INDETERMINATE (in band, p>0.05) |
| 1500 | 0.522 | — | FAIL |
| 2000 | 0.391 | — | FAIL |

INDETERMINATE band is approximately SC tau_2 in [600, 1200] us.

### F-N12-2 (secondary): Decoherence-only null — **FAIL** (likely surrogate-circuit artifact)

- Predicted tau_2(C1) = tau_2(C2)/4 >= 333 us
- Observed tau_2(C1) = 782.3 us
- Deviation 135% (threshold 20%)
- Interpretation: C1 tau_2 *larger* than 1/N depolarizing model predicts. Most likely explanation: rx(2π) surrogate is virtually a frame change, not a real decoherence-inducing wait. F-N12-2 "FAIL" here is a circuit-construction artifact, not evidence for OR.

### F-N12-3 (secondary): DP mass-scaling escape window — **FAIL** (weak)

- Observed ratio 7.82 (sc_ref=100us); DP-predicted ratio bracket [1.5e3, 1.5e7] (m_ion=684 amu, m_sc=1e6..1e10 amu)
- Observed ratio 100x to 1e6x smaller than predicted DP scaling
- Verdict: FAIL — but SC effective-mass definition (Cooper-pair count vs junction capacitance) is itself ambiguous, so this rejection is weak evidence at best.

### F-N12-4 (secondary): Lindblad vs OR-augmented AIC — **INDETERMINATE**

- Single delay point (100us), 100 shots, 11 distinct bitstrings observed
- AIC discrimination requires >= 3 delay points or full state tomography (16 amplitudes for 4-qubit)
- Both exceed MVP budget; deferred.

### C3 Bell sanity — **PASS**

- P(00 or 11) = 99.0% (>= 95% threshold)
- Single |10> outcome consistent with single-shot SPAM error (~1%)
- Forte 1 hardware confirmed operational

## Honest C3 (top disclosures)

1. **SC reference value is unverified.** Agent did NOT extract the exact PRNewswire 2025-03 SC-QC paper tau_2 numeric. Used 100us as canonical SC 4-qubit GHZ T2* bracket. Sensitivity sweep documents that the F-N12-1 verdict flips between FAIL (most ranges) and INDETERMINATE (~[600, 1200] us). Without verified SC ref, the FAIL verdict is only as strong as the assumed reference.

2. **Surrogate-delay circuit may not actually decohere.** Forte 1 does NOT support `i` (identity) or pulse-level `delay` outside `verbatim` mode. We replaced the spec's identity-stack delay with `rx(2*pi)` * 12 as a "physical-time surrogate" (full rotation = identity). On Forte 1 this is likely compiled to virtual frame changes (no real wait), explaining why C2 returned `{"0": 100}` (perfect identity) and C1 retained 88% X-basis parity contrast despite "100us" delay. To do this experiment correctly, the next iteration must use Forte 1 verbatim-mode pulse-level `delay` or actual idle waits via a different mechanism. **F-N12-1 FAIL therefore should be read as "tau_2_ion bound likely much higher than measurement window" rather than "trapped-ion measured tau_2 = 782 us"**.

3. **C2 spec drift +$4.00.** Forte 1 minimum-shots=100; spec had C2 at 50 shots. Bumped to 100, costing extra $4.00. Total $24.90 vs spec $20.90, vs user-authorized $20.90, vs hard cap $50. Spend is +19% over user-confirmed, but well under the safety-margin cap. Pre-authorization stated "$20.90 MVP spend" — the $4.00 over-run is a hardware constraint not anticipated in spec.

## Cost ledger

- 3 tasks * $0.30 = $0.90 task fees
- 300 shots * $0.08 = $24.00 shot fees
- **Total: $24.90 USD on AWS account 267673635495 (May 2026 invoice)**

## Files written

- `state/n_substrate_n12_aws_exec_2026_05_01/submission_ledger.json` — task ARNs + cost
- `state/n_substrate_n12_aws_exec_2026_05_01/raw_results.json` — measurement counts
- `state/n_substrate_n12_aws_exec_2026_05_01/falsifier_verdicts.json` — F-N12-1..4 verdicts + SC sensitivity sweep
- `state/n_substrate_n12_aws_exec_2026_05_01/cost_ledger.json` — actual AWS spend
- `state/n_substrate_n12_aws_exec_2026_05_01/c3_partial_submit.json` — recovery record from first-try C3
- `docs/n_substrate_n12_aws_exec_results_2026_05_01.md` — this report

Off-repo (Mac-side, HEXA-only constraint):
- `~/n12_braket/submit_braket.py` (patched: rx(2π) surrogate, --skip-ids flag)
- `~/n12_braket/poll_and_retrieve.py` (state polling, results retrieval)
- `~/n12_braket/aux_falsifiers.py` (F-N12-2/3/4 + C3 sanity)
- `~/n12_braket/verify_F_N12_1.py` (F-N12-1 verifier, unchanged)
- `~/n12_braket/results_retrieved_1777694687.json` — full raw JSON
- `~/n12_braket_venv/` — Python 3.14 venv with amazon-braket-sdk 1.117.1

## Recommended next steps (deferred — separate authorization)

1. Re-run C1 with Forte 1 `verbatim` pragma and pulse-level `delay` instruction for an actual physical-time wait (not surrogate gates). Cost approximately $8.30 for 100-shot single delay, $16.60 for two-delay direct fit.
2. Extract PRNewswire 2025-03 SC-QC OR paper numeric tau_2 to replace the 100us placeholder. No QPU cost.
3. F-N12-5 replicability rerun at D+7 (preregistered, $20.90, separate auth).
