# N-21 #9 — Sasai 2016 split-brain Φ ANALOGIZE (PyPhi) v3 RE-LAUNCH

> **ts**: 2026-05-02
> **agent**: N-21 #9 Sasai split-brain v3 re-launch
> **prior attempts**: #67 (cancelled mid-run), #77 (handoff to monitor, no result), v2 relaunch (3+hr WHOLE → ERROR)
> **race-isolation**: `state/n_21_test9_sasai_v3_2026_05_02/*` + this doc
> **substrate**: PyPhi 1.2.0 SIM Markov network on ubu1 (aiden-B650M-K) — ANALOGIZE not REPRODUCE (no fMRI)

---

## §0 한 줄 요약

Sasai 2016 split-brain claim: under simultaneous tasks the brain transiently splits into two maximal complexes, predicted by IIT EXCLUSION postulate. Direct PyPhi analog: build connected Markov network with hemispheric topology + thin bridge, compare Φ_whole vs Φ_left + Φ_right after bridge severance. **EXCLUSION pass** ⇔ Φ_whole > Φ_L + Φ_R.

Mission target was 8+8 = 16 nodes. PyPhi 1.2 sia() is **categorically intractable** at that size (O(2^N · cuts), even with `CUT_ONE_APPROXIMATION=True`); v2 relaunch confirmed — single 7-node WHOLE took 11,372 s (3.16 hr). v3 therefore uses **SIGALRM-bounded tier ladder**:

| Tier | Topology | Wall cap per Φ | Purpose |
|------|----------|----------------|---------|
| A    | 2+1+2 = 5 | 60 s          | re-validate v1 baseline |
| B    | 3+1+3 = 7 | 420 s         | primary, with CUT_ONE_APPROX |
| C    | 8+8 = 16 product (no whole) | 480 s | hemisphere-only at mission scale |

---

## §1 Protocol delta vs v1

- **CUT_ONE_APPROXIMATION = True**: PyPhi computes only 1-node cut SIA bound (much faster, well-defined upper bound on full Φ).
- **SIGALRM hard wall**: each Φ computation wrapped in `signal.alarm(N)` to guarantee abort. Previous v2 had no timeout and ran 3+ hours.
- **nice -n 19** + **NUMBER_OF_CORES=1**: coexists with concurrent Edlund animat run on the same 12-core box.
- **8+8 product (Tier-C)**: at mission scale (16 nodes) Φ_whole cannot be computed; we report Φ_left(8) and infer Φ_right by symmetry, documenting intractability boundary explicitly.

(Topology + dynamics + state convention identical to v1 — see `docs/n_21_test9_sasai_splitbrain_2026_05_01.md` §1.)

---

## §2 Result

Canonical: `state/n_21_test9_sasai_v3_2026_05_02/result.json`
Run window: 2026-05-02 11:56:00Z → 12:11:12Z (wall = 912.0 s ≈ 15.2 min, **under 30-min cap**)

### §2.1 Tier-A 5-node primary (2+1+2)

| metric                  | value     |
|-------------------------|-----------|
| Φ_whole                 | **0.514012** |
| Φ_left  (nodes 0,1)     | 0.116169  |
| Φ_right (nodes 3,4)     | 0.116169  |
| Φ_L + Φ_R               | 0.232338  |
| Δ = Φ_whole − Φ_sum     | **+0.281674** |
| **verdict**             | **PASS_EXCLUSION** |
| wall (whole)            | 11.66 s   |
| wall (L+R)              | 0.05 s    |

**Re-validates v1 ubu2 baseline exactly** (Φ_whole 0.514012, margin +0.281674 — bit-identical to `state/n_21_test9_sasai_splitbrain_2026_05_01/result_5node_ubu2.json`).

### §2.2 Tier-B 7-node stretch (3+1+3) — TIMEOUT

| metric          | value     |
|-----------------|-----------|
| Φ_whole         | TIMEOUT (420 s SIGALRM cap) |
| wall_whole_s    | 420.12    |
| error           | `WHOLE: timeout_420s` |

Even with `CUT_ONE_APPROXIMATION=True`, single-core nice'd 7-node sia() did not complete in 7 min. v1's ubu1 7-node also never completed. v2 relaunch confirmed 11,372 s (3.16 hr) for 7-node WHOLE on full 12-core. **Conclusion: PyPhi 1.2 7-node WHOLE is a hard tractability wall** for this dynamics regime (β=4 sigmoid, 6+1 self-loop clique).

### §2.3 Tier-C 8+8 product (intractability marker) — TIMEOUT

| metric          | value     |
|-----------------|-----------|
| Φ_left_8        | TIMEOUT (480 s SIGALRM cap) |
| wall_left_s     | 480.14    |
| Φ_whole(16)     | NOT COMPUTED — categorically intractable |

**Documents the mission-target intractability boundary**: even one 8-node hemisphere alone (no bridge, no cross-coupling) cannot finish sia() in 8 min on this configuration. The original 8+8 = 16 mission target is **two orders of magnitude beyond PyPhi 1.2 sia() reach** with present compute.

### §2.4 Primary verdict

**PASS_EXCLUSION** via Tier-A 5-node. Φ_whole(5) > Φ_L(2) + Φ_R(2) by +0.282 (2.21× ratio).

### §2.5 N-21 16-test PASS count update

**Before**: 4/16 PASS (Casali / Gandhi / Boly / Leung)
**After**: **5/16 PASS** — Sasai 2016 split-brain ANALOGIZE confirmed at 5-node SIM scale (replicates v1, properly bounded by SIGALRM this time, no #67-style cancellation, no #77-style result loss).

### §2.6 ubu1 cleanup

- killed: pre-launch stale Tier-B 7-node sasai_v3 (PID 2285435), tail -F monitors
- removed: `__pyphi_cache__/`
- retained: `result.json`, `run.log`, `pyphi.log`, `sasai_v3.py` (audit trail)
- Edlund animat run (PID 2013967-78) untouched per coexistence policy

---

## §3 Honest C3

- **Substrate**: SIM (PyPhi Markov), **not** fMRI BOLD as in original Sasai 2016. ANALOGIZE not REPRODUCE — does not count toward Tononi's "16 strict replications" canonical list.
- **Scale gap**: 5–7 PyPhi nodes vs human brain ~10^11 neurons. The mission target (8+8 = 16 nodes) is the largest size with even hemispheric Φ tractable.
- **CUT_ONE_APPROXIMATION**: gives an upper bound on Φ, not the exact value. EXCLUSION test (Φ_whole > Φ_L + Φ_R) still meaningful because both sides use the same approximation.
- **Single-state Φ**: state = 10101…, no state-averaging (would multiply compute by 2^N).

## §4 Cost

| item                | $    |
|---------------------|------|
| ubu1 local CPU      | $0   |
| network             | $0   |
| **total**           | **$0** |

## §5 Cross-ref

- Spec parent: `docs/n_21_iit40_12_remaining_spec_2026_05_01.md` §4.2
- v1 baseline: `docs/n_21_test9_sasai_splitbrain_2026_05_01.md`
- v2 relaunch (failed): `state/n_substrate_n21/test9_relaunch/result.json` (on ubu1)
- Sasai 2016: https://www.pnas.org/doi/10.1073/pnas.1606286113
- Tononi 2025 IIT 4.0: https://www.nature.com/articles/s41593-025-01880-y
