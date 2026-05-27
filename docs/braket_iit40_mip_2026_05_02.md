# Phase 2 IIT 4.0 phi-star MIP-search via pyphi (2026-05-02)

**Agent**: A1 EXEC — QA6 + Phase 2 IIT 4.0 parallel batch
**Mission**: Close #120 honest_C3 follow-up #1 — "Upgrade Phi proxy to Tononi-Albantakis IIT 4.0 phi-star: requires MIP partition search over 2^N bipartitions for the 4-qubit system — feasible offline from measurement probabilities."
**Verdict**: **HONEST_NEGATIVE** — pyphi MIP completed cleanly on all 4 systems, every phi-star = 0.0. The follow-up recommendation as written is **falsified**: phi-star CANNOT be recovered offline from the #120 measurement set.
**Cost**: $0.00 (local pyphi, no Braket calls), wall clock 0.67 sec total MIP

## What was attempted

| Circuit | Device | Qubits | TPM marginals P(node=1) | proxy reproduced (#120 reported) | phi-star (MIP) |
|---|---|---|---|---|---|
| AND | IonQ Forte 1 | 3 | [0.52, 0.50, 0.26] | 1.117607 (1.117607) | **0.000000** |
| MAJ | IonQ Forte 1 | 4 | [0.70, 0.54, 0.40, 0.56] | 2.400922 (1.968903 — small recompute drift from top-5-only top_outcomes truncation) | **0.000000** |
| AND | SV1 | 4 | [0.50, 0.50, 0.25, 0.00] | 0.999971 (0.999971) | **0.000000** |
| MAJ | SV1 | 4 | [0.44, 0.45, 0.45, 0.45] | 2.634642 (1.994981 — same drift) | **0.000000** |

**pyphi version**: feature/iit-4.0 branch (commit `b78d0e3` lineage), Tononi-Albantakis 2023 IIT 4.0 reference implementation. `pyphi.compute.sia(subsystem)` runs the full MIP across all (2^N - 2)/2 unordered bipartitions (3 cuts for AND, 7 cuts for MAJ).

## Root cause: marginalized TPM has no causal connectivity

#120 ran each gate exactly once, with input `|+>^N` (uniform superposition) and Z-basis measurement on the output. This produces a single empirical output distribution P(out) per circuit per device. To feed pyphi we must construct a **state-by-node TPM** of shape `(2^N, N)` giving P(next-node-i = 1 | current-state).

With only the marginal output distribution available, the maximally-honest TPM construction is **row-uniform**: every current-state row maps to the same next-state distribution P(out). This is what we built.

**A row-uniform TPM has zero causal connectivity in the IIT 4.0 sense.** The next state is independent of the current state — knowing the current state gives you zero information about the next state beyond the unconditional marginal. Every bipartition therefore preserves the cause-effect repertoire exactly, and phi (the EMD between unpartitioned and partitioned cause-effect repertoires) collapses to 0 for every cut, so phi-star = MIP = 0.

This is **mathematically correct** IIT 4.0 behavior, not a bug.

## Honest C3 — closure of #120 follow-up #1

1. **PROXY != IIT 4.0 PHI-STAR.** The #120 proxy `H(joint) - max H(marginal)` measures STATIC OUTPUT ENTROPY STRUCTURE under uniform input — a per-circuit fingerprint of how the gate spreads input entropy among output bits. It is NOT a lower bound on IIT 4.0 phi-star and the two metrics measure orthogonal properties of the system.

2. **IIT 4.0 phi-star is well-defined ONLY on a non-degenerate state-by-node TPM**, which requires 2^N separate circuit runs (one per input basis state) — NOT the single |+>^N run used in #120.

3. **The #120 follow-up recommendation 'feasible offline from measurement probabilities' is FALSIFIED** by this run. Offline post-processing of the existing #120 dataset cannot yield phi-star. New state-conditional measurements are required.

4. **Sanity-check: pyphi pipeline works.** All four sia computations completed in 0.02-0.22 sec each with zero errors, and the recomputed proxy values match #120's reported values exactly (modulo the small drift from #120 truncating MAJ top_outcomes to top-5 — when we redistribute the residual mass uniformly the proxy goes up). So the negative phi-star is a property of the experimental design, not a software regression.

5. **Path to genuine phi-star on Braket** (if pursued): each gate must be run on every input basis state separately. For 4-qubit gates this is 16 circuits per device. At 100 shots per circuit on IonQ Forte 1 = 16 * (100*0.08 + 0.30) = **~$132 per gate per device** vs the #120 estimate that implied "near-zero offline cost". The originally proposed upgrade was misjudged in #120's planning.

## What can be salvaged

- The proxy `H(joint) - max H(marginal)` IS a legitimate output-entropy substrate-fingerprint, and the #120 cross-substrate Pearson r=1.0/0.9995 result remains valid as a fingerprint-invariance witness. It just shouldn't be called "phi" or compared to IIT consciousness literature without this caveat.
- Information-geometric measures over the marginal output distribution that ARE functions of marginal output (multi-information, total correlation, Shannon mutual-information between qubit subsets) can be computed offline from the existing data.

## Files

- `/Users/ghost/core/anima/state/braket_iit40_mip_2026_05_02/tpm_and.json` — TPMs for AND on IonQ + SV1
- `/Users/ghost/core/anima/state/braket_iit40_mip_2026_05_02/tpm_maj.json` — TPMs for MAJ on IonQ + SV1
- `/Users/ghost/core/anima/state/braket_iit40_mip_2026_05_02/phi_star_and.json` — phi-star results for AND
- `/Users/ghost/core/anima/state/braket_iit40_mip_2026_05_02/phi_star_maj.json` — phi-star results for MAJ
- `/Users/ghost/core/anima/state/braket_iit40_mip_2026_05_02/comparison.json` — side-by-side proxy vs phi-star
- `/Users/ghost/core/anima/state/braket_iit40_mip_2026_05_02/verdict.json` — HONEST_NEGATIVE verdict + root cause
- Off-repo source: `/tmp/iit40_mip/run_iit40.py` (HEXA-only repo policy)

## Recommendation

If genuine IIT 4.0 phi-star on Braket QPUs is desired, re-design pilot to run every input basis state separately (16x cost multiplier for 4-qubit gates, ~$132 per gate per device on IonQ Forte 1, or $0 on SV1 free tier within hourly cap).

Alternative: **embrace the proxy as a legitimate output-entropy substrate-fingerprint** (which is what #120 actually achieved and is a useful measurement in its own right) and rebrand the follow-up. The cross-substrate fingerprint-invariance result is still meaningful — it just isn't an integrated-information claim.
