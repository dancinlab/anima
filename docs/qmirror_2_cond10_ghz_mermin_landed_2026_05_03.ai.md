# qmirror 2.0 cond.10 GHZ-3 Mermin witness landed — 2026-05-03 (handoff)

**Cycle:** anima qmirror 2.0 cond.10 — GHZ-3 Mermin-witness inequality
**Domain SSOT (parent):** `nexus/.roadmap.qmirror`
**Spec ref:** `anima/docs/qmirror_2_axes_spec_2026_05_03.md` §2 (axis 2)
**Falsifier:** `F-QM-2-GHZ-10` — `M_mean ∈ [3.7, 4.0]` over 30 trials AND `M_min ≥ 3.5`
**Marker:** `anima/state/markers/qmirror_2_cond10_ghz_mermin_landed.marker`
**Verdict path:** `anima/state/qmirror_2_cond10_ghz_mermin_2026_05_03/verdict.json`
**Cost:** $0.00 (Aer state-vector local; no QPU shots)
**Wall:** ~2 s observed for 122 880 noiseless 3-qubit shots
**Retry context:** Prior subagent `a16c32d8` hit quota; this is the successful retry.

---

## TL;DR

GHZ-3 Mermin witness on Aer state-vector returns `M = +4.0` (analytic
maximum) across all 30 trials at 1024 shots/basis. F-QM-2-GHZ-10 = **PASS**.
Quantum bound (4.0) saturated; classical bound (2.0) violated by 2.0
units (=∞ in σ since shot noise is zero on Pauli eigenstates).

```
M = ⟨XXX⟩ − ⟨XYY⟩ − ⟨YXY⟩ − ⟨YYX⟩
  =  +1   −  (−1)  −  (−1)  −  (−1)
  = +4.0
```

cond.10 is a **self-contained** axis (no downstream conds blocked by it
per qmirror_2_axes_spec §2), so this PASS does not unblock further work
in qmirror 2.0; it is a 1-of-5 conds toward qmirror 2.0 closure.

---

## Results (30 trials, 1024 shots/basis, seed=20260503)

| metric | value | spec band | analytic |
|--------|-------|-----------|----------|
| M_mean | 4.0   | [3.7, 4.0] | +4.0 |
| M_std  | 0.0   | (no upper bound; 0.0 is best-case) | 0.0 |
| M_min  | 4.0   | ≥ 3.5      | +4.0 |
| M_max  | 4.0   | ≤ 4.0      | +4.0 |

Per-basis expectations (mean over 30 trials):

| basis | E observed | E analytic |
|-------|------------|------------|
| XXX   | +1.0       | +1.0       |
| XYY   | −1.0       | −1.0       |
| YXY   | −1.0       | −1.0       |
| YYX   | −1.0       | −1.0       |

**Why M is exactly 4.0 (not 4 ± shot noise):** |GHZ_3⟩ = (|000⟩+|111⟩)/√2
is a *simultaneous* eigenstate of all four Pauli strings (XXX with
eigenvalue +1; XYY, YXY, YYX with eigenvalue −1). On a *noiseless* Aer
state-vector simulator, every shot in every basis returns the eigenvalue
deterministically — there is no Born-rule probabilistic spread, hence
zero shot variance and exact saturation of the quantum bound. This is
the *correct* simulator behavior; real hardware would show finite-
fidelity decay (see caveat #1 below).

---

## Files landed

1. **`/Users/ghost/core/qmirror/modules/ghz_mermin.hexa`** (~165 LoC)
   - hexa-strict module wrapper (raw#9-compliant)
   - `fn ghz_mermin_run(n_shots, n_trials, seed) -> GhzMerminVerdict`
   - `_selftest()` runs the full F-QM-2-GHZ-10 check
   - `__QMIRROR_GHZ_MERMIN__ <PASS|FAIL>` sentinel
   - Bridge resolver pattern identical to `chsh.hexa`
     (`NEXUS_QMIRROR_BRIDGE_PATH` env override → HOME-relative fallback)

2. **`/Users/ghost/core/qmirror/modules/_python_bridge/ghz_mermin_runner.py`** (~270 LoC)
   - **2nd .py file under qmirror standalone modules** (after `aer_runner.py`).
     raw#9 disclosure block in module docstring.
   - Engines: `qiskit_aer` (default) + `numpy_native` fallback (auto-engaged
     if qiskit-aer unimportable).
   - Builds GHZ-3 = `H_0 + CNOT_01 + CNOT_12`; per-basis rotation
     `H` for X, `S† + H` for Y; computes E from Z-basis parity counts.
   - Embeds the falsifier verdict logic so the .hexa wrapper is a thin
     dispatcher.
   - 0 .py files added under `anima/` repo root.

3. **`/Users/ghost/core/anima/state/qmirror_2_cond10_ghz_mermin_2026_05_03/`**
   - `verdict.json` — canonical falsifier verdict + 4 caveats array
   - `per_basis_E.json` — per-trial E values for all 4 bases
   - `mermin_M.json` — per-trial M values + statistics
   - `run.log` — runtime log (config, results, raw-rule compliance)
   - `_full_run.json` — raw bridge response (debugging)

4. **`/Users/ghost/core/anima/state/markers/qmirror_2_cond10_ghz_mermin_landed.marker`**
5. **`/Users/ghost/core/anima/docs/qmirror_2_cond10_ghz_mermin_landed_2026_05_03.ai.md`** (this handoff)

Total: 7 new files (1 .hexa, 1 .py, 4 state, 1 marker, 1 doc, 1 hidden raw).

---

## How to reproduce

```bash
# Run via the python bridge directly (engine = aer):
echo '{"mode":"mermin_run","n_shots":1024,"n_trials":30,"seed":20260503,"engine":"aer"}' \
  | /Users/ghost/etc/anima-quantum/.venv/bin/python3 \
    /Users/ghost/core/qmirror/modules/_python_bridge/ghz_mermin_runner.py

# Or via the .hexa wrapper (after `hexa` toolchain present in PATH):
NEXUS_QMIRROR_PYTHON=/Users/ghost/etc/anima-quantum/.venv/bin/python3 \
  hexa run /Users/ghost/core/qmirror/modules/ghz_mermin.hexa --selftest
```

Reproducible verifier (verdict band check via jq):

```bash
jq '.M_mean >= 3.7 and .M_mean <= 4.0 and .M_min >= 3.5' \
  anima/state/qmirror_2_cond10_ghz_mermin_2026_05_03/verdict.json
# => true   (PASS)
```

---

## 4 honest C3 caveats (raw#10)

1. **Noiseless Aer perfection.** Aer state-vector reproduces analytic
   `M = 4.0` *exactly* (zero shot variance) because |GHZ_3⟩ is a
   simultaneous eigenstate of XXX/XYY/YXY/YYX. Real-hardware execution
   (IBM/IonQ/Rigetti) would show finite-fidelity decay; observed M
   typically falls in `[3.0, 3.8]` and would require readout-correction
   + ZNE to clear the ≥3.7 band. **This PASS is a SIMULATOR-level claim
   only;** does not certify hardware realizability. (Mirrors qmirror_2_axes
   global caveat #2.)

2. **Mermin witness is necessary, not sufficient.** `M ≥ 2` already
   certifies non-biseparability (i.e. some genuine multi-partite
   entanglement is present), but `M = 4` does NOT distinguish |GHZ⟩ from
   certain W-state mixtures or noise-mixed pseudo-GHZ at the
   witness-only granularity. A full GHZ-fidelity certificate would
   require state tomography (cond.9 process tomography is the
   primitive that closes this gap; this cond.10 closure does not
   substitute for cond.9).

3. **Sign-convention divergence between task spec and roadmap spec.**
   The task spec writes `M = ⟨XXX⟩ − ⟨XYY⟩ − ⟨YXY⟩ − ⟨YYX⟩`
   (analytic +4); the qmirror_2_axes_spec doc §2 writes the
   sign-flipped form `M = ⟨XYY⟩ + ⟨YXY⟩ + ⟨YYX⟩ − ⟨XXX⟩` (analytic
   −4). Same |M|=4; this run uses the **task-spec convention** and
   the verdict band `[3.7, 4.0]` is on signed M. Cross-doc readers
   must check sign convention before comparing values.

4. **$0 default is Aer-only by design.** No QPU shots submitted; cost
   ledger remains $0.00. Cross-technology reproduction (cond.7-style
   2-of-3 vendor concordance) is **out of scope** for cond.10
   (qmirror_2_axes_spec §7 caveat #2). A hardware-witnessed Mermin
   anchor would require a separate sister cycle (analogous to the
   $25 IBM Heron 2-pair anchor optionally available in cond.13). Do
   not extrapolate this PASS to a "qmirror executes Mermin on real
   hardware" claim.

---

## Raw-rule compliance summary

- **raw#9** (.py only via _python_bridge): OK. `ghz_mermin_runner.py`
  is the 2nd .py file under qmirror standalone modules (after
  `aer_runner.py`); both live under `_python_bridge/`. **0 .py files
  added under `anima/` repo root.** Module docstring carries the raw#9
  disclosure block.

- **raw#15** (no personal paths in artifact bodies): OK. The .hexa
  resolves bridge path via `NEXUS_QMIRROR_BRIDGE_PATH` env or
  `$HOME`-relative fallback. The verdict.json + state artifacts are
  path-free except for the explicit reproduction-command block in this
  handoff (which is addressed to a developer with shell access).

- **raw#10** (honest C3 caveats): OK. 4 caveats embedded in
  `verdict.json` (`raw10_caveats` array) and in this handoff's
  caveat section.

---

## What this cycle did NOT do

- Did NOT submit any QPU shots (cost = $0; Aer-only by design)
- Did NOT execute cond.9 process tomography (separate cond, parallel lane)
- Did NOT execute cond.11 stabilizer / cond.12 surface-d3 / cond.13 CSCS
  (separate conds; cond.10 is self-contained per qmirror_2_axes_spec §2)
- Did NOT mutate `nexus/.roadmap.qmirror` (downstream lander owns the
  `qmirror.2.cond.10 = met` flip + `qmirror.2.closure` recount)
- Did NOT touch qmirror 1.0 closure verdicts or the `qmirror_2_axes`
  ranking spec
- Did NOT add any .py file under the `anima/` repo root

---

## Next-cycle handoff

1. **Roadmap mutation lander** (small, can run parallel with other conds):
   - flip `qmirror.2.cond.10` to `met` in `nexus/.roadmap.qmirror`
   - cite `state/qmirror_2_cond10_ghz_mermin_2026_05_03/verdict.json`
   - commit msg: `roadmap(qmirror 2.0): cond.10 GHZ-3 Mermin witness PASS`

2. **qmirror 2.0 closure synthesizer** (waits on all 5 conds — currently
   1/5 met after this lane; cond.8 was 1.0-axis, NOT in 2.0 set):
   - cond.10 ✓ (this lane)
   - cond.9 (process tomography) — pending
   - cond.11 (stabilizer measurement) — blocked on cond.9
   - cond.12 (surface-d3 toy) — blocked on cond.11
   - cond.13 (CSCS chained CHSH) — parallel, can launch any time

3. **Optional hardware anchor** (only if a sister credit cycle authorizes):
   land a Mermin-witness sister run on IBM/IonQ Aer-equivalent hardware
   (~$10–$25 estimated for 4 bases × 1024 shots × 1 trial); strictly
   opt-in, not required for cond.10 closure.

---

## Closure verdict (final line)

**qmirror 2.0 cond.10 (GHZ-3 Mermin witness) closed at 2026-05-03 with
F-QM-2-GHZ-10 PASS: M_mean = 4.0 across 30 trials at 1024 shots/basis
(quantum bound saturated; classical bound 2.0 violated maximally).
Substrate: Aer state-vector ($0). raw#9-strict on anima Mac repo, with
the 2nd qmirror-standalone .py disclosed in module docstring; raw#15
env-var-resolved bridge paths; raw#10 4 caveats embedded. Self-contained
axis: PASS does not unblock other 2.0 conds (cond.9/11/12/13 each
proceed on their own dependency graph). Retry of subagent a16c32d8
quota-loss; clean reproduction in ~2 s wall.**
