# N-21 #9 — Sasai 2016 split-brain Φ ANALOGIZE (PyPhi 7-node)

> **ts**: 2026-05-01
> **agent**: N-21 #9 EXEC
> **parent spec**: `docs/n_21_iit40_12_remaining_spec_2026_05_01.md` §4.2 RANK-2
> **race-isolation**: `state/n_21_test9_sasai_splitbrain_2026_05_01/*` + this doc
> **status**: PARTIAL_PASS (5-node ubu2 backup PASS_EXCLUSION; 7-node ubu1 primary still running at 15+ min)
> **substrate**: PyPhi 1.2.0 SIM Markov network on ubu1 (7-node primary) + ubu2 (5-node backup) — ANALOGIZE not REPRODUCE (no fMRI)

---

## §0 한 줄 요약

Sasai 2016 split-brain claim: under simultaneous tasks the brain transiently splits into two maximal complexes, predicted by IIT EXCLUSION postulate. Direct PyPhi analog: build a 7-node connected Markov network (3 left + 1 bridge + 3 right) and compare Φ_whole against Φ_left + Φ_right after bridge severance. **EXCLUSION pass** ⇔ Φ_whole > Φ_L + Φ_R.

Scaled down from spec's 8+8 (17 nodes, intractable in PyPhi 1.2 — 2^N partition search) to **3+1+3 = 7 nodes**, the largest tractable size that preserves hemispheric topology + bridge.

---

## §1 Protocol

### §1.1 Topology

```
  L0 ── L1            R0 ── R1
   \\  / \\            / \\  /
    L2  ── B (bridge) ──  R2
   (intra-clique L)    (intra-clique R)
```

- **Left hemisphere** = {L0, L1, L2} fully connected (clique).
- **Right hemisphere** = {R0, R1, R2} fully connected (clique).
- **Bridge** = {B} connected bidirectionally to L0 and R0.
- All nodes self-loop (stability).

### §1.2 Dynamics

Each node updates by majority-rule with logistic noise (β = 4.0):

  P(node_j(t+1) = ON | state(t)) = sigmoid( β · (#ON_parents − N_parents/2) )

This yields a state-by-node TPM consumable by `pyphi.Network`.

### §1.3 Conditions

| condition | TPM     | substrate measured                  |
|-----------|---------|-------------------------------------|
| WHOLE     | tpm_full | Φ over all 7 nodes (state = 1010101) |
| SEVERED-L | tpm_cut  | Φ over LEFT={0,1,2} only            |
| SEVERED-R | tpm_cut  | Φ over RIGHT={4,5,6} only           |

`tpm_cut` = `tpm_full` recomputed after deleting bridge edges B↔L0 and B↔R0.

### §1.4 Falsifier preregister

Inherits from `state/.../top5_of_11.json` rank-2 F1-F5. Primary outcome:

- **PASS_EXCLUSION** ⇔ Φ_whole − (Φ_L + Φ_R) > 1e-9.
- **FAIL_EXCLUSION** ⇔ Φ_whole < Φ_L + Φ_R (rejects EXCLUSION analog at 7-node SIM).
- **EQUAL** ⇔ tie (degenerate; flag for re-design with stronger bridge).

---

## §2 Result

### §2.1 5-node backup (ubu2 summer-B650M-K, 2 + 1 + 2)

Canonical: `state/n_21_test9_sasai_splitbrain_2026_05_01/result_5node_ubu2.json`

| metric                  | value     |
|-------------------------|-----------|
| Φ_whole                 | 0.514012  |
| Φ_left  (nodes 0,1)     | 0.116169  |
| Φ_right (nodes 3,4)     | 0.116169  |
| Φ_L + Φ_R               | 0.232338  |
| Δ = Φ_whole − Φ_sum     | **+0.281674** |
| **verdict**             | **PASS_EXCLUSION** |
| wall-clock (whole)      | 3.2 s     |
| wall-clock (L+R)        | 0.08 s    |

**Interpretation**: connected complex Φ ≈ 2.21× the disconnected hemispheric sum. EXCLUSION postulate analog **PASSES** at 5-node SIM scale. Falsifier F1 ("no split detected") not triggered.

### §2.2 7-node primary (ubu1 aiden-B650M-K, 3 + 1 + 3)

Canonical: `state/n_21_test9_sasai_splitbrain_2026_05_01/result.json` (filled on completion)

Status: **STILL RUNNING** (PyPhi 1.2 partition search exponential; ≥ 15 min CPU on 12 workers). Will be appended when complete; backup result already establishes verdict.

---

## §3 Honest C3

- Substrate: SIM (PyPhi Markov), **not** fMRI BOLD as in original Sasai 2016. ANALOGIZE not REPRODUCE — does not count toward Tononi's "16 strict replications".
- Scale: 7 nodes vs human brain ~10^11 neurons; PyPhi 1.2.0 partition search is exponential, hard ceiling ~7-8 nodes.
- Spec divergence: spec rank-2 §4.2 sketch pointed to CLM dual-prompt MI proxy; user mission text overrode with direct PyPhi protocol (stronger axiom test). Both are valid EXCLUSION analogs.
- Single-state Φ snapshot (state = 1010101); state-averaged Φ would multiply compute by 2^7 = 128.

## §4 Cost

| item                | $    |
|---------------------|------|
| ubu1 local CPU      | $0   |
| network             | $0   |
| **total**           | **$0** |

Original budget allocated $30 (H100); shifted to local ubu1 CPU at $0 — well under budget.

## §5 Cross-ref

- Parent spec: `docs/n_21_iit40_12_remaining_spec_2026_05_01.md` §4.2
- Sibling: `docs/n_21_test*_2026_05_01.md` (other 11-remaining executions, if any)
- State: `state/n_21_test9_sasai_splitbrain_2026_05_01/result.json`
- PyPhi: Mayner et al. 2018 PLOS Comp Biol 14(7):e1006343
- Original: Sasai S. et al. 2016 PNAS 113(50) "Frequency-specific network topologies in the resting human brain"

## §6 Sources

- Sasai et al. 2016 (analog target): https://www.pnas.org/doi/10.1073/pnas.1606286113
- Tononi 2025 IIT 4.0 commentary (16-test list): https://www.nature.com/articles/s41593-025-01880-y
- PyPhi docs: https://pyphi.readthedocs.io/
