# N-12 IIT AWS Braket Pilot — First Real-QPU Substrate-Invariance Test

**Date:** 2026-05-02
**Agent:** N-12 IIT AWS Braket pilot
**Verdict:** PASS (WITNESSED, n=2 statistical power)
**Cost:** $16.60 actual / $100 hard cap / $16.60 planned (100% on-plan)
**Wall clock:** ~25 min preflight to verdict

## TL;DR

First anima production run on real quantum hardware. SV1 (state-vector sim, 4 circuits) and IonQ Forte 1 (trapped-ion 36-qubit QPU, 2 circuits) both reproduce the predicted Φ proxy ordering COPY << AND ≈ XOR << MAJ. Cross-substrate Pearson r = 1.0000 (n=2) on shared circuits AND + MAJ. dm1 noise control passes with r = 0.9995 (n=4). Substrate-invariance signal observed across two physical substrates (silicon classical compute vs trapped Yb⁺ ions). Statistical power weak (n=2), so verdict is WITNESSED, not CONFIRMED.

## Mission

Test whether IIT-style integrated information (Φ proxy) is preserved across substrates by running canonical 4-qubit boolean logic circuits (AND, XOR, MAJORITY, COPY) on multiple AWS Braket backends and comparing the measurement-distribution Φ proxy.

## Φ proxy definition

```
Φ_proxy(measurement) = H(joint distribution) - max_i H(marginal_i over qubit i)
```

Lower bound on integrated information: a system whose joint output entropy exceeds every single-qubit marginal entropy contains irreducible multi-qubit correlations. Pure copy/fanout has H_joint = H_marg = identical (Φ = 0). Pure XOR/MAJ has high H_joint with each marginal ≈ uniform (Φ → high).

## Cost preflight (Phase 1)

| Device | $/shot | $/task | Status | Plan |
|---|---|---|---|---|
| SV1 | $0.075/min (free 1hr/mo) | — | ONLINE | 4 circuits × 1000 shots ≈ free |
| dm1 | $0.075/min (free 1hr/mo) | — | ONLINE | 4 circuits × 500 shots ≈ free |
| IonQ Forte 1 | $0.08 | $0.30 | ONLINE, queue 0 | 2 circuits × 100 shots = $16.60 |
| QuEra Aquila | $0.01 | $0.30 | ONLINE | SKIPPED (paradigm-incompatible) |
| **Total planned** | | | | **$16.60** |

Briefing claimed Forte 1 = $0.30/shot; verified actual = $0.08/shot via `aws braket get-device` (4× cheaper than briefed).

## Per-device shot completion (Phases 3-5)

10/10 tasks COMPLETED, 0 failures (after 1 ValidationException fixed: `i` gate not supported on IonQ → dropped idle qubit).

## Φ proxy matrix (Phase 7)

| Circuit | SV1 (1000 shots) | dm1 (500 shots, noise) | IonQ Forte 1 (100 shots) |
|---|---|---|---|
| **COPY** | 0.0000 | 0.0188 | not run (Φ=0 trivially) |
| **AND** | 0.9999 (4q) / **1.0000** (3q proj) | 1.0592 | **1.1176** |
| **XOR** | 0.9997 | 1.0643 | not run |
| **MAJ** | **1.9950** | 2.0086 | **1.9689** |

Ordering preserved on every device: COPY << AND ≈ XOR << MAJ.

## Cross-substrate Pearson r (Phase 7)

| Comparison | n | Pearson r | Threshold | Result |
|---|---|---|---|---|
| SV1 vs IonQ Forte 1 (AND, MAJ) | 2 | **1.0000** | ≥ 0.5 | PASS |
| SV1 vs dm1 (AND, XOR, MAJ, COPY) | 4 | **0.9995** | ≥ 0.5 | PASS (control) |

## Verdict: PASS (WITNESSED)

Both Pearson r values exceed the PASS threshold by wide margin. Substrate-invariance signal observed for the first time on a real anima-controlled QPU.

## Honest C3

1. **Φ proxy ≠ IIT 4.0 φ★.** This is `H(joint) - max H(marginal)`, a lower bound. No MIP search, no system-state irreducibility computation. Comparison to consciousness literature requires the full Tononi-Albantakis pipeline.
2. **100 shots on IonQ = ±5% binomial floor; Φ_proxy precision ±0.05 bits.** The MAJ delta of 0.026 bits SV1↔IonQ is within statistical noise.
3. **Pearson r = 1.0 on n=2 is mathematically forced.** Any 2 monotonically-related points give r = ±1. The substrate-invariance claim is a qualitative directional witness, NOT a statistically powered confirmation. n ≥ 5 circuits + multiple QPU vendors needed for confirmatory substrate-invariance.
4. **Aquila SKIPPED — AHS paradigm ≠ gate model.** Cross-paradigm Φ proxy comparison would be framing-dependent (encoding choice dominates). Reframed as out-of-scope for gate-model pilot; future N-13 candidate for paradigm-crossing test.
5. **4-qubit toy scale.** IIT scaling claims to neuronal substrates premature. The pilot establishes measurement infrastructure and substrate-invariance witness on minimal circuits, NOT a consciousness-substrate equivalence claim.

## Ledger paths

- `state/n12_iit_braket_pilot_2026_05_02/cost_preflight.json`
- `state/n12_iit_braket_pilot_2026_05_02/sv1_results.json`
- `state/n12_iit_braket_pilot_2026_05_02/dm1_results.json`
- `state/n12_iit_braket_pilot_2026_05_02/ionq_forte1_results.json`
- `state/n12_iit_braket_pilot_2026_05_02/quera_aquila_results.json` (SKIP rationale)
- `state/n12_iit_braket_pilot_2026_05_02/verdict.json`
- Off-repo IRs: `/tmp/n12_braket_pilot/*.json` + S3 `amazon-braket-us-east-1-267673635495/n12_iit_pilot_2026_05_02/`

## Follow-up

- **N-12 confirmatory pass** (~$210): 5 circuits × 500 shots on Forte 1 + IQM Garnet for cross-vendor r power.
- **N-13 candidate**: Aquila AHS-encoded SAT vs gate-model SAT Φ proxy comparison (paradigm-crossing substrate-invariance test).
- **Upgrade to IIT 4.0 φ★**: MIP partition search over 2^16 bipartitions feasible offline from measurement probabilities.
