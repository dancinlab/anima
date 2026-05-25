<!-- [Hc_958 qmirror-2-5-conds-cluster — moved to hypotheses_candidates/Hc_958_qmirror_2_5_conds_cluster.md on 2026-05-11] -->

# qmirror 2.0 cond.13 CSCS chained sequential CHSH landed — 2026-05-04 (handoff)

**Cycle:** anima qmirror 2.0 cond.13 — CSCS (Chained Sequential CHSH) on Aer state-vector
**Domain SSOT (parent):** `nexus/.roadmap.qmirror`
**Spec ref:** `anima/docs/qmirror_2_axes_spec_2026_05_03.md` §2 (axis 5)
**Falsifier:** `F-QM-2-CSCS-13` — `min(S_per_pair_mean) ≥ 2.7` AND `W_mean ≥ 2.7` AND `indep_pvalue_mean ≥ 0.05`
**Marker:** `anima/state/markers/qmirror_2_cond13_cscs_landed.marker`
**Verdict path:** `anima/state/qmirror_2_cond13_cscs_2026_05_04/verdict.json`
**Cost:** $0.00 (Aer state-vector local; optional $25 IBM Heron 2-pair anchor DECLINED per default closure path)
**Wall:** 41 s observed for 122 880 noiseless 6-qubit shots (120 Aer jobs)

---

## TL;DR

Three Bell pairs constructed in a single 6-qubit Aer register, each
independently violating CHSH at near-Tsirelson saturation (S ≈ 2.82),
with no detectable cross-pair dependence under conditional-on-setting
chi-squared independence testing. **F-QM-2-CSCS-13 = PASS.** All three
falsifier predicates cleared with comfortable margin:

| predicate | observed | spec floor | margin |
|-----------|----------|-----------|--------|
| `min(S_per_pair_mean) ≥ 2.7` | 2.8174 | 2.7 | +0.1174 |
| `W_mean ≥ 2.7`                | 2.8211 | 2.7 | +0.1211 |
| `indep_pvalue_mean ≥ 0.05`    | 0.1120 | 0.05 | +0.062  |

cond.13 is the **5th and final axis** of qmirror 2.0; with cond.9 +
cond.10 + cond.11 + cond.12 also at PASS, the qmirror 2.0 closure ledger
is **5/5 PASS** (omnibus closure marker can land in a sister cycle).

---

## Per-pair S results (30 trials, 1024 shots/setting, seed=20260504)

| pair | qubits | S_mean | S_std | S_min | S_max | Tsirelson gap |
|------|--------|--------|-------|-------|-------|---------------|
| 0    | (0, 1) | 2.8194 | 0.0426 | 2.7129 | 2.8848 | 0.0090 |
| 1    | (2, 3) | 2.8174 | 0.0473 | 2.7051 | 2.8887 | 0.0110 |
| 2    | (4, 5) | 2.8266 | 0.0414 | 2.7480 | 2.9180 | 0.0019 |

`min_S = 2.8174` (over per-pair MEANS) ≥ 2.7 ✓
`W_mean = 2.8211` (mean over pairs of pair-S, then over 30 trials) ≥ 2.7 ✓
`W_violation_above_classical = 0.8211` ⇒ **~161 σ above classical bound 2.0**
(SEM = W_std / √30 = 0.00511; (W_mean − 2.0) / SEM = 160.79).

---

## Independence test (chi-squared, conditional-on-setting, adjacent-pair)

**Why conditional-on-setting:** when pooling outcomes across the 4 CHSH
settings (each pair sees the same setting in any one Aer job), the
per-pair marginal distribution shifts with setting, creating spurious
"cross-pair correlation" via co-shifting marginals. The correct null is
*conditional* on the measurement setting: "given setting σ on all pairs,
pair k's outcome is statistically independent of pair (k+1)'s outcome."
With true register-isolation (no inter-pair CX in the chained build),
each conditional test should yield a p-value uniform on [0,1].

**Aggregation:** per trial we run 4 settings × (n_pairs−1)=2 adjacent
pair tests = **8 conditional 4×4 χ² tests**, then report the **MIN**
p-value (conservative). Over 30 trials we average those mins.

| stat | observed | expected under null | falsifier band |
|------|----------|----------------------|----------------|
| `indep_pvalue_mean` | 0.1120 | ~1/9 = 0.111 (E[min of 8 uniform]) | ≥ 0.05 ✓ |
| `indep_pvalue_min`  | 0.00026 | ~1/241 = 0.0042 (E[min of 240 uniform]) | (informational) |

The `indep_pvalue_mean = 0.112` is a **textbook null-distribution**
match — true independence confirmed. The single low `indep_pvalue_min =
0.00026` is a **multiple-testing artifact** (240 χ² tests under the
null), NOT a genuine independence failure; only `indep_pvalue_mean` is
the falsifier-bearing statistic per F-QM-2-CSCS-13.

---

## CSCS construction

```
qubits (0,1) -> pair 0
qubits (2,3) -> pair 1
qubits (4,5) -> pair 2

per pair k (one Aer job per setting):
    H(2k)
    CX(2k, 2k+1)
    Ry(-theta_a, 2k)         # canonical SSOT recipe — NOT Ry(-2*theta)
    Ry(-theta_b, 2k+1)
measure all 6 qubits in Z basis
```

4 CHSH settings per trial (canonical SSOT angle set):

| setting | (theta_a, theta_b) | name |
|---------|--------------------|------|
| 1 | (0,    π/4)  | `circuit_a_b` |
| 2 | (0,   −π/4)  | `circuit_a_bprime` |
| 3 | (π/2,  π/4)  | `circuit_aprime_b` |
| 4 | (π/2, −π/4)  | `circuit_aprime_bprime` |

This is the **register-isolation** form of CSCS: 3 Bell pairs share one
statevector but have no inter-pair CX, so they're entanglement-isolated
by construction. The chained property tested is "outcome distributions
remain independent when pairs share the simulator backend register."

S formula (per pair, per trial):
```
S_pair = E_ab + E_abp + E_apb − E_apbp
```
On the SSOT angle set with `Ry(-θ)` recipe, `E_ab = E_abp = E_apb ≈ +0.71`
and `E_apbp ≈ −0.71` ⇒ S ≈ 4·(√2/2) = +2√2 ≈ 2.828 (Tsirelson).

---

## Files landed

1. **`/Users/ghost/core/qmirror/modules/cscs.hexa`** (~165 LoC)
   - hexa-strict module wrapper (raw#9-compliant; no Python in this file)
   - `fn cscs_run(n_pairs, n_shots, n_trials, seed) -> CscsVerdict`
   - `_selftest()` runs the full F-QM-2-CSCS-13 check
   - `__QMIRROR_CSCS__ <PASS|FAIL>` sentinel
   - Bridge resolver pattern identical to `chsh.hexa` / `ghz_mermin.hexa`
     (`NEXUS_QMIRROR_BRIDGE_PATH` env override → HOME-relative fallback)

2. **`/Users/ghost/core/qmirror/modules/_python_bridge/cscs_runner.py`** (~440 LoC)
   - **3rd .py file under qmirror standalone modules** (after
     `aer_runner.py` and `ghz_mermin_runner.py`). raw#9 disclosure block
     in module docstring.
   - Engines: `qiskit_aer` (default) + `numpy_native` fallback (auto-engaged
     if qiskit-aer unimportable)
   - Imports the **shared SSOT** `chsh_circuits.py`
     (`SETTINGS`, `make_bell_chsh`, `correlator`) via dynamic import
     resolved through `CHSH_CIRCUITS_SSOT` env, sibling-file fallback,
     then HOME-relative anima staging path
   - Includes a pure-python χ² survival function (no scipy dep) built
     from the regularized incomplete gamma series + continued fraction
   - Uses `_canonical_S(Es) = E_ab + E_abp + E_apb − E_apbp` instead of
     the SSOT `compute_S` (see caveat #3); SSOT primitives unchanged

3. **`/Users/ghost/core/anima/state/qmirror_2_cond13_cscs_2026_05_04/verdict.json`**
   - F-QM-2-CSCS-13 verdict payload (PASS), per-pair S means/stds/min/max,
     W mean/std, indep p-value mean/min, all 4 caveats inline

4. **`/Users/ghost/core/anima/state/qmirror_2_cond13_cscs_2026_05_04/per_pair_S.json`**
   - Detailed per-pair statistics + full S_per_trial 30×3 matrix

5. **`/Users/ghost/core/anima/state/qmirror_2_cond13_cscs_2026_05_04/witness_W.json`**
   - W aggregate witness + violation σ + per-trial independence p-value list
   - Falsifier predicate breakdown

6. **`/Users/ghost/core/anima/state/qmirror_2_cond13_cscs_2026_05_04/run.log`**
   - Execution log (configuration, results, falsifier check, caveats)

7. **`/Users/ghost/core/anima/state/qmirror_2_cond13_cscs_2026_05_04/_full_run.json`**
   - Raw bridge stdout (preserved for reproducibility)

8. **`/Users/ghost/core/anima/state/markers/qmirror_2_cond13_cscs_landed.marker`**
   - Land marker (this cycle)

9. **`/Users/ghost/core/anima/docs/qmirror_2_cond13_cscs_landed_2026_05_04.ai.md`**
   - This handoff document

---

## raw#10 caveats (4, embedded in verdict.json)

1. **Noiseless Aer perfection vs hardware decay.** Aer reproduces
   near-Tsirelson per-pair S ≈ 2.82 with shot-noise std ≈ 0.04 at 1024
   shots. Real hardware (IBM Heron / IonQ / Rigetti) exhibits two
   compounding decays: (a) per-pair single-Bell fidelity loss dropping S
   to ~2.3–2.5, (b) chained-register decoherence accumulating across 6
   qubits in a single circuit. **Optional $25 IBM Heron 2-pair anchor
   was DECLINED** for this $0 default closure path (per spec §2 axis 5).

2. **Chain construction is "register-isolation," not "temporal-sequential."**
   3 Bell pairs share one 6-qubit statevector with NO inter-pair CX.
   The independence tested is *register-isolation* (no spurious
   cross-pair dependence from sharing the simulator register). An
   alternative *temporal-sequential* form (3 Bell pairs prepared and
   measured back-to-back on the *same 2 qubits* with mid-circuit reset)
   would test PRNG/state-reset independence; that variant is OUT OF
   SCOPE for cond.13 and a candidate for a future qmirror 3.0 axis.

3. **S formula deviation from `chsh_circuits.py` SSOT compute_S.**
   The SSOT defines `S = E_ab − E_abp + E_apb + E_apbp` (per docstring,
   matching cond.3 ibm_fez Heron r2 hardware where `E_abp` came out
   NEGATIVE). On *noiseless Aer* with the SSOT angle set
   `(0, π/2, π/4, −π/4)` and `Ry(−θ)` recipe, `E_ab`, `E_abp`, `E_apb`
   are all POSITIVE (~+0.71) while `E_apbp` is NEGATIVE (~−0.71), so the
   SSOT formula yields S ≈ 0 (cancellation) instead of saturating
   Tsirelson. `cscs_runner.py` uses
   `S = E_ab + E_abp + E_apb − E_apbp` (canonical CHSH sign convention),
   giving S ≈ +2.83 on Aer. **The SSOT compute_S is bugged on the
   noiseless backend** (it works only for the cond.3 hardware sign
   pattern). All other SSOT components (`SETTINGS`, `make_bell_chsh`,
   `correlator`) are used unchanged. SSOT amendment recommended in a
   sister cycle.

4. **`indep_pvalue_min = 0.00026` is a multiple-testing artifact, NOT an
   independence failure.** Each trial runs 8 conditional χ² tests
   (4 settings × 2 adjacent-pair tests); 30 trials = 240 tests under the
   independence null. The expected MIN of 240 uniform p-values is
   ~1/241 = 0.0042; observed 0.00026 is within natural fluctuation of
   that null. The falsifier-bearing statistic per F-QM-2-CSCS-13 is
   `indep_pvalue_mean` (= 0.112, matching the ~1/9 = 0.111 expected
   E[MIN of 8 uniform draws] under TRUE independence). Cross-doc readers
   must NOT interpret `indep_pvalue_min` as a scientific failure mode.

---

## Reproduce

Aer ($0 default, ~41 s wall):

```bash
echo '{"mode":"cscs_run","n_pairs":3,"n_shots_per_setting":1024,"n_trials":30,"seed":20260504,"engine":"aer"}' \
  | /Users/ghost/etc/anima-quantum/.venv/bin/python \
    /Users/ghost/core/qmirror/modules/_python_bridge/cscs_runner.py
```

Hexa wrapper:

```bash
hexa run /Users/ghost/core/qmirror/modules/cscs.hexa --selftest
# expects: __QMIRROR_CSCS__ PASS
```

Reproducible verifier (per spec §5):

```bash
ls anima/state/qmirror_2_cond13_cscs_2026_05_04/verdict.json && \
jq '.W_mean >= 2.7 and .indep_pvalue_mean >= 0.05 and .min_S >= 2.7' \
   anima/state/qmirror_2_cond13_cscs_2026_05_04/verdict.json
# expects: true
```

---

## qmirror 2.0 closure status

| cond | falsifier | verdict | landed | marker |
|------|-----------|---------|--------|--------|
| cond.9  tomography | F-QM-2-TOMO-9  | PASS | 2026-05-03 | `qmirror_2_cond9_tomography_landed.marker` |
| cond.10 GHZ-3      | F-QM-2-GHZ-10  | PASS | 2026-05-03 | `qmirror_2_cond10_ghz_mermin_landed.marker` |
| cond.11 stabilizer | F-QM-2-STAB-11 | PASS | 2026-05-04 | `qmirror_2_cond11_stabilizer_landed.marker` (verify) |
| cond.12 surface-d3 | F-QM-2-SURF-12 | PASS | 2026-05-04 | `qmirror_2_cond12_surface_landed.marker` (verify) |
| **cond.13 CSCS**   | F-QM-2-CSCS-13 | **PASS** | **2026-05-04** | `qmirror_2_cond13_cscs_landed.marker` (this) |

**qmirror 2.0 axis closure: 5/5 PASS.** The omnibus
`qmirror.closure.full.v2` marker can land in a sister cycle once the
`nexus/.roadmap.qmirror` flips all 5 statuses to `closed`.

---

## Next-cycle suggestions

- **Sister cycle: SSOT compute_S amendment.** `chsh_circuits.py`
  `compute_S` is bugged on noiseless Aer (caveat #3); a clean fix is to
  add an `_canonical_compute_S` alias and update the docstring to make
  the cond.3 sign-pattern dependency explicit. Keeps both formulas
  available, avoids breaking the cond.3 hardware-anchored verdict.
- **qmirror 3.0 axis candidate:** *temporal-sequential* CSCS (caveat
  #2) — 3 Bell pairs back-to-back on the same 2 qubits with mid-circuit
  reset; tests PRNG/state-reset independence directly.
- **Optional $25 anchor:** IBM Heron 2-pair anchor (per spec §2 axis 5)
  remains opt-in; would require submitting a 4-qubit chained-Bell
  circuit to `ibm_fez` (or current Heron-class device) under the
  cond.3-style budget.
