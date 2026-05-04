# qmirror 2.0 axes landed — 2026-05-03 (handoff)

**Cycle:** anima qmirror 2.0 next-cycle axes synthesis
**Domain SSOT (parent):** `nexus/.roadmap.qmirror`
**Spec (LoC ~530):** `anima/docs/qmirror_2_axes_spec_2026_05_03.md`
**Ranked axes JSON:** `anima/state/qmirror_2_axes_2026_05_03/ranked_axes.json`
**Marker:** `anima/state/markers/qmirror_2_axes_landed.marker`
**Cost:** $0 (pure spec synthesis; no QPU spend, no API calls, no impl)

---

## TL;DR

`nexus.qmirror` 1.0 closed 8/8 conds on 2026-05-03. This cycle delivers
the **5 ranked next-cycle conds** for qmirror 2.0, scored by Impact ×
Feasibility (1–5 each, multiplicative floor). All 5 chosen axes execute
at **$0 default** ($25 ceiling via 1 opt-in IBM Heron anchor in cond.13)
on **Aer state-vector + ANU entropy** under the existing qmirror 1.0
substrate stack. Sequential wall ~9 days; parallel 2-lane ~5 days.

3 candidate axes (magic-state distillation, quantum-supremacy XEB, VQC)
deferred or rejected with documented rationale (§6 of spec doc).

---

## What landed this cycle

1. **`anima/docs/qmirror_2_axes_spec_2026_05_03.md`** (~530 LoC, 9 sections)
   - Executive summary with 5×ranked-axes table (rank, I, F, I×F, cost,
     wall, dependency)
   - §1 Ranking methodology (rubric + tie-break order)
   - §2 Top-5 per-cond full spec (description, substrate, falsifier with
     reproducible verifier, cost, time, dependencies, rank rationale)
   - §3 Cost matrix (per-axis $ ladder, wall ladder, compute ladder, hexa
     LoC + python_bridge concession)
   - §4 Falsifier ledger (5-row single-table summary)
   - §5 Roadmap mutation block (paste-target JSON for `.roadmap.qmirror`)
   - §6 Deferred/rejected axes (3 items with I×F + rationale + path-forward)
   - §7 Honest C3 caveats (5 items, raw#10)
   - §8 References
   - §9 Closure verdict

2. **`anima/state/qmirror_2_axes_2026_05_03/ranked_axes.json`**
   - schema_version 1
   - Ranking methodology block + raw_compliance block
   - 5 ranked axes (each with cond_id, scores, falsifier, cost, deps,
     LoC, rank rationale)
   - 3 deferred/rejected axes
   - Falsifier ledger
   - Cost matrix summary
   - 5 honest caveats array

3. **`anima/state/markers/qmirror_2_axes_landed.marker`**
   - Status SPEC_LANDED + per-rank summary table
   - Cost matrix + falsifier ledger
   - Deferred/rejected list
   - 5 caveats

---

## 5 ranked axes summary

| rank | cond | name | I | F | I×F | $ | wall | qubits | deps |
|------|------|------|---|---|-----|---|------|--------|------|
| 1 | cond.9  | quantum_process_tomography  | 5 | 5 | 25 | $0       | 2 d   | 4  | qmirror.closure.full |
| 2 | cond.10 | ghz3_mermin_witness         | 5 | 5 | 25 | $0       | 1 d   | 3  | qmirror.closure.full |
| 3 | cond.11 | stabilizer_measurement      | 4 | 5 | 20 | $0       | 1.5 d | 4  | cond.9 |
| 4 | cond.12 | surface_code_d3_toy         | 5 | 4 | 20 | $0       | 2 d   | 17 | cond.11 |
| 5 | cond.13 | cscs_chained_chsh           | 4 | 5 | 20 | $0/$25   | 1.5 d | 4  | qmirror.closure.full |

**Tie-break at IxF=25** (rank #1 vs #2): cond.9 wins because it blocks
3 downstream conds; cond.10 is self-contained.

**Tie-break at IxF=20** (rank #3 / #4 / #5): cond.11 → cond.12 follows
"build primitive before consumer"; cond.13 trails because it does not
unlock new module surface.

---

## Cost matrix (final)

| dim | floor | ceiling |
|-----|-------|---------|
| total qmirror 2.0 cost USD              | $0 | $25 |
| sequential wall days                    | 9  | 9   |
| parallel 2-lane wall days               | 5  | 5   |
| new .hexa files                         | 5  | 5   |
| nexus python_bridge file additions      | 2  | 2   |
| anima Mac repo .py file additions       | 0  | 0   |

Default closure path is fully **$0**. The $25 cond.13 IBM Heron 2-pair
anchor is **opt-in** and gated by a separate sister credit cycle decision.
Even at the $25 ceiling, qmirror 2.0 sits an order of magnitude below
the $200 IBM Cloud one-shot calibration burst that anchored qmirror 1.0
v2.0/v3.0 calibration (spec 1.0 §14).

---

## Deferred / rejected axes

| axis | decision | I×F | rationale (1-line) |
|------|----------|-----|--------------------|
| magic_state_distillation         | DEFERRED | 10 | Needs ≥30 qubits → saturates Aer SV ceiling; revisit at qmirror 3.0 after cond.12 surface-code lands |
| quantum_supremacy_random_circuit | REJECTED | 8  | Sycamore XEB requires 144 PB SV RAM at full scale; even toy-XEB is metric-inverted on classical sim |
| variational_quantum_classifier   | DEFERRED | 9  | Trivial quantum kernel + no anima/nexus downstream consumer identified |

---

## 5 honest C3 caveats (raw#10)

1. **Selection bias toward Aer-friendly conds.** All 5 axes execute at
   $0 on Aer. Deliberate retrenchment after qmirror 1.0 cond.3/cond.7
   hardware-burst band-revision pain. Hardware-burst axes deferred to a
   parallel qmirror 2.0-anchor cycle. Means qmirror 2.0 by itself does
   **not** improve cond.7 cross-tech band-revision exposure from 1.0.

2. **All falsifiers are noiseless-Aer thresholds** (0.99 fidelity, 0.99
   syndrome ratio, 2.7 Bell bound). Real-hardware execution would
   require ZNE/DD/readout-correction to clear; if a downstream re-runs
   on real QPU and FAILs, the spec must be amended (parallel to cond.3
   0.40→0.55 revision) before interpreting as a 2.0 failure.

3. **cond.12 surface-d3 is a primitive demonstration, NOT fault tolerance.**
   No syndrome decoder, no logical error rate, no Pauli-frame tracking,
   no logical Cliffords. Calling it "surface-code on qmirror" without
   the "toy" qualifier would mislead.

4. **python_bridge debt grows by 2 files** (`tomo_runner.py`,
   `mid_measure_runner.py`) in nexus repo. **raw#9 STRICT honored on Mac
   repo (anima): 0 .py files added** in this cycle. Nexus bridge file
   count rises 1 → 3 over qmirror 1.0+2.0; defers Phase 4 FFI retirement.

5. **Optional $25 anchor in cond.13 is opt-in, NOT load-bearing.**
   Default closure path is fully $0. If a sister credit cycle elects to
   land it, verdict.json must distinguish Aer-path PASS from
   hardware-anchor PASS — conflating would re-introduce the cond.3-style
   band-revision selection-bias risk that 1.0 disclosed.

---

## What this cycle did NOT do

- Did NOT execute any of the 5 conds (this is spec only)
- Did NOT mutate `nexus/.roadmap.qmirror` (mutation block in §5 of spec
  is a paste-target for the downstream landing agent)
- Did NOT create any .py file under the Mac repo (raw#9 STRICT)
- Did NOT include personal paths in artifact bodies (raw#15)
- Did NOT submit any QPU job (cost = $0)
- Did NOT touch qmirror 1.0 closure verdicts or cond.4 NIST sister BG

---

## Next steps for downstream agents

1. **Roadmap mutation lander**: paste §5 of the spec into
   `nexus/.roadmap.qmirror`; commit with msg
   `roadmap(qmirror 2.0): land 5 next-cycle conds (cond.9..cond.13)`.

2. **Per-axis impl agents** (5, can run in parallel after cond.9 + cond.11
   ordering respected):
   - **cond.9 lane (Day 0):** impl `tomography.hexa` + `tomo_runner.py`
     bridge → run F-QM-2-TOMO-9 → land verdict
   - **cond.10 lane (Day 0, parallel):** impl `ghz.hexa` → run
     F-QM-2-GHZ-10 → land verdict
   - **cond.11 lane (Day 2, after cond.9 lands):** impl `stabilizer.hexa`
     + `mid_measure_runner.py` + `circuit.hexa` patch → run F-QM-2-STAB-11
     (includes cond.9 cross-check) → land verdict
   - **cond.12 lane (Day 3.5, after cond.11 lands):** impl
     `surface_code.hexa` → run F-QM-2-SURF-12 → land verdict
   - **cond.13 lane (Day 0, parallel):** impl `cscs.hexa` → run
     F-QM-2-CSCS-13 (default $0 path) → land verdict; optional $25 IBM
     Heron anchor only if a sister credit cycle authorizes it

3. **qmirror 2.0 closure synthesizer** (after all 5 verdicts land):
   author `nexus_qmirror_2_closure_<date>.md` mirroring 1.0 closure
   structure; flip `qmirror.2.closure = met` in roadmap.

---

## Files touched (4 total)

1. **NEW** `anima/docs/qmirror_2_axes_spec_2026_05_03.md` (530 LoC spec)
2. **NEW** `anima/docs/qmirror_2_axes_landed_2026_05_03.ai.md` (this handoff)
3. **NEW** `anima/state/qmirror_2_axes_2026_05_03/ranked_axes.json`
4. **NEW** `anima/state/markers/qmirror_2_axes_landed.marker`

No file mutations in nexus repo; no `.roadmap.qmirror` edit (downstream
lander owns that mutation).

---

## Closure verdict (final line)

**qmirror 2.0 axes spec landed at 2026-05-03; 5 ranked conds
(cond.9 / cond.10 / cond.11 / cond.12 / cond.13) define the next-cycle
closure target with $0 default execution / $25 ceiling / 5–9 wall-day
window / raw#9-STRICT-on-Mac compliance / 5 honest caveats embedded.
Top-3 deferred axes (magic-state distillation, supremacy sampling, VQC)
documented with I×F rationale. Downstream impl agents may launch under
the dependency graph cond.9 → cond.11 → cond.12; cond.10 + cond.13
parallel-lane unconstrained.**
