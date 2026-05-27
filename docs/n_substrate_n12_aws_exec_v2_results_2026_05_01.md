# N-12 v2 IonQ Forte 1 Orch-OR Re-launch — ABORTED at Phase 2 (substrate-incapable)

Agent: `n_substrate_n12_aws_exec_v2`
Date UTC: 2026-05-01
Parent v1 report: `docs/n_substrate_n12_aws_exec_results_2026_05_01.md`
v2 state dir: `state/n_substrate_n12_aws_exec_v2_2026_05_01/`
v1 state dir (untouched): `state/n_substrate_n12_aws_exec_2026_05_01/`

## Headline

**v2 verdict: INDETERMINATE — Forte 1 substrate-incapable.**
**Total v2 AWS spend: $0.00** (vs $45 target, vs $50 cap).
The user-specified methodology fix (OpenQASM 3 verbatim + explicit `delay[Nus]`) is **not executable** on IonQ Forte 1 via AWS Braket. Per mission spec ("if Forte 1 does NOT support verbatim/pulse-delay, document and abort the v2 attempt — do NOT silently fall back to surrogate"), Phase 2 was aborted before live submit.

## Phase 1: PRNewswire SC reference extraction — FAIL

- N-20 doc check (`docs/n_substrate_n20_orch_or_2026_literature_2026_05_01.md` §1 evidence table, 2025-03 row): the quantitative field reads **"비-Orch-OR specific (general OR 정합)"** — no tau_2 numeric.
- WebFetch on the PRNewswire URL (`...consciousness-theory-302419751.html`): **no specific numeric values for tau_2, T2, decoherence time, or collapse timescale are reported**. The release describes methodology (single-bit test on IBM Eagle chip, LLM-generated quantum code) and attribution (Valis Corporation, James Tagg) but defers technical data to a "forthcoming GitHub repository."
- **Outcome: cannot replace the v1 100us placeholder with a sourced value.** Even with a fallback IBM Eagle T2 typical range (~50-300 us), no defensible single number exists. Decision recorded in `state/n_substrate_n12_aws_exec_v2_2026_05_01/prnewswire_extraction.json`.

## Phase 2: Verbatim + pulse-level delay implementation — ABORT

### Capability probe (cost: $0)

`aws braket get-device --device-arn arn:aws:braket:us-east-1::device/qpu/ionq/Forte-1` returned:

| field | value |
|---|---|
| supportedOperations | `x, y, z, h, s, si, t, ti, v, vi, rx, ry, rz, cnot, swap, xx, yy, zz` |
| supportedPragmas | `braket_result_type_*`, `verbatim` |
| supportsPartialVerbatimBox | `false` |
| nativeGateSet | `GPI, GPI2, ZZ` |
| **`delay` in supportedOperations** | **NO** |
| **idle/wait primitive in nativeGateSet** | **NONE** |

`verbatim` IS supported as a pragma — but verbatim only permits native gates, and the native set has no idle primitive.

### Live server-side validation (cost: $0 — rejected pre-billing)

Three OpenQASM 3 programs were submitted to `device.run(...)` to force Braket's server-side validator to give a definitive yes/no on `delay`. AWS Braket bills only COMPLETED tasks; ValidationException at `CreateQuantumTask` is pre-billing.

| attempt | OpenQASM 3 location of `delay` | result |
|---|---|---|
| 1. bare delay | top-level, logical qubit `q[0]` | `ValidationException: [line 5] Timing instruction 'delay' is not presently supported on device` |
| 2. delay in verbatim, logical qubit | inside `#pragma braket verbatim box`, `q[0]` | `ValidationException: [line 6] physical qubits are required in verbatim boxes` (rejected at syntax before delay was checked) |
| 3. delay in verbatim, physical qubit | inside `#pragma braket verbatim box`, `$0` | `ValidationException: [line 6] Timing instruction 'delay' is not presently supported on device` |

**Verdict: definitively NO.** Forte 1 via AWS Braket has no real wall-clock delay primitive — both inside and outside verbatim mode.

### Why no fallback

- `rx(2*pi)*N` surrogate: this is exactly the v1 mistake (likely virtual frame change, see v1 honest C3 disclosure #2). Mission spec explicitly forbids it.
- Repeated single-qubit native gate `gpi(0)*N` inside verbatim: still gate-time accumulation, not idle wait; same epistemic flaw as v1 surrogate.
- Long XX/YY/ZZ entangling sequences: would consume real time but introduce correlated noise that contaminates the Orch-OR signature (defeats the purpose).

Phase 3 (submit), Phase 4 (verify) — **SKIPPED** as Phase 2 abort precondition.

## F-N12-1 v2 verdict — vs v1 comparison

| | v1 EXEC | v2 EXEC |
|---|---|---|
| verdict | FAIL | **INDETERMINATE** |
| reason | ratio 7.82 outside [0.67, 1.5] at sc_ref=100us | substrate cannot answer the question |
| methodology integrity | flawed (surrogate + placeholder ref) | abort-before-flaw (no surrogate spent on, no ref claimed) |
| spend | $24.90 | $0.00 |
| epistemic content | "FAIL" was already disclosed in v1 C3 as likely circuit-construction artifact | honest restatement: cross-substrate Orch-OR test not measurable on Forte 1/Braket |

**Did the methodology fix change the verdict? Yes — from a flawed FAIL to an honest INDETERMINATE.** This is the correct outcome of the methodology fix attempt: we discovered the substrate cannot do the experiment, rather than producing a second flawed measurement.

## Cost ledger

- Tasks submitted (live, billable): **0**
- Validation rejections (pre-billing): 3
- Task fees: $0.00
- Shot fees: $0.00
- **Total v2 AWS spend: $0.00 USD** (target $45.00, hard cap $50.00)

## Honest C3 (top-3)

1. **Forte 1 via AWS Braket genuinely cannot do real wall-clock delay** — confirmed by direct server-side validation (3 attempts), not inferred. The methodology fix as user-specified is not executable on this substrate. Any further spend on Forte 1 with surrogate gates would be epistemically wasteful and is forbidden by mission spec.
2. **PRNewswire 2025-03 source contains no extractable tau_2 numeric** — confirmed by WebFetch. Even if Phase 2 had succeeded, the SC reference would have remained an unsourced placeholder; the mission's planned "fix flaw 2" could not be completed from the cited source. Press release defers technical data to a "forthcoming GitHub repository."
3. **To obtain a real ion-substrate tau_2 measurement, off-Braket alternatives required** — separate authorization needed for: (a) IonQ Direct API pulse-level access, (b) different vendor where `delay` IS exposed (IBM Quantum Heron/Eagle, Quantinuum H-series via Azure Quantum), or (c) re-derive an Orch-OR signature that does not require explicit wall-clock idle (e.g., gate-count-based decoherence proxy via native echo sequences with proper noise modeling).

## Precise blocker

- type: substrate_capability_gap
- device: IonQ Forte 1 via AWS Braket
- missing capability: OpenQASM 3 `delay[duration] qubit` timing instruction
- server-side error verbatim: `Timing instruction 'delay' is not presently supported on device`
- workaround within Braket+Forte 1 satisfying "no surrogate" constraint: NONE

## Files written

- `state/n_substrate_n12_aws_exec_v2_2026_05_01/forte1_capability_probe.json` — device capability + 3 validation rejection records
- `state/n_substrate_n12_aws_exec_v2_2026_05_01/prnewswire_extraction.json` — Phase 1 outcome
- `state/n_substrate_n12_aws_exec_v2_2026_05_01/v2_verdict.json` — F-N12-1 v2 verdict + v1 comparison
- `docs/n_substrate_n12_aws_exec_v2_results_2026_05_01.md` — this report

Off-repo: no new scripts written; v1 `~/n12_braket/*.py` untouched. Validation probe was inline `python3 -c '...'`.

## Race isolation audit

- v1 dir (`state/n_substrate_n12_aws_exec_2026_05_01/`): writes = 0
- Other N-* dirs: writes = 0
- alpha pod / nexus: untouched
- GPU pods: untouched
- AWS account: `267673635495` ([braket] profile, us-east-1) — only get-device + 3 ValidationException-rejected CreateQuantumTask calls (no billable resources)

## Recommended next (deferred — separate authorization)

1. Pivot to IBM Quantum (Heron r2 / Eagle r3) where OpenQASM3 `delay` IS in the supported instruction set — replicate the GHZ dephasing curve there for the ion-side equivalent OR signature (note: same-vendor caveat — both ion and SC sides on different substrates).
2. Or: redesign F-N12-1 to use a delay-free Orch-OR signature (e.g., GHZ fidelity vs gate count under fixed echo sequence) so any QPU including Forte 1 can answer.
3. Locate the Valis/Tagg "forthcoming GitHub repository" or peer-reviewed paper to obtain the actual SC tau_2 numeric, replacing the 100us placeholder permanently.
