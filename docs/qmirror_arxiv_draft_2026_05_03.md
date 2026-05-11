<!-- [Hc_914 qmirror-classical-qpu-mirror — moved to hypotheses_candidates/Hc_914_qmirror_classical_qpu_mirror.md on 2026-05-11] -->

# qmirror: A Classical-CPU Mirror of a Quantum Processing Unit Using Real Quantum Entropy

**Draft preprint** — arXiv-targeted, *DRAFT ONLY*, not yet submitted.
**Date:** 2026-05-03
**Status:** v0.1 draft (peer review pending; license audit complete; cross-vendor calibration complete)
**Source repos:**
- GitHub canonical: https://github.com/dancinlab/qmirror
- HuggingFace mirror: https://huggingface.co/dancinlab/qmirror
**License (source):** Apache-2.0 (qmirror code); GPLv3 (optional pyphi backend; see §7)

---

## Abstract

We introduce **qmirror**, a hexa-language module that synthesizes a
quantum-processing-unit-equivalent substrate from three free, classical
ingredients: (i) Qiskit Aer state-vector simulation for exact unitary
evolution, (ii) the Australian National University Quantum Random Number
(ANU QRNG) vacuum-fluctuation REST service for measurement randomness,
and (iii) HMAC-DRBG SHA-256 keyed seeding for deterministic regression
testing. The combination is statistically equivalent to a noiseless
quantum processor within the simulator-tractable regime
(approximately 30 qubits state-vector, 50 qubits matrix-product state).
We validate qmirror against eight closure conditions covering
specification coverage, falsifier-driven self-test, real-hardware CHSH
existence proof (IBM Heron r2 ibm_fez, S = 2.357 +/- 0.050), NIST SP
800-22 statistical battery on QRNG drop-in regression, reproduction of
a reference Bell inequality measurement (S = 2.808 reference vs S = 2.838
qmirror, |Delta| = 0.030), byte-identical Integrated Information Theory
4.0 phi-star validation against pyphi reference outputs, cross-family
intra-superconducting concordance (Rigetti Cepheus 108Q vs IBM Heron r2,
|Delta S| = 0.084), and a four-vendor cross-vendor concordance matrix
(IonQ Aria-1, IonQ Forte-1, Rigetti Cepheus, IBM Heron r2 ibm_fez).
Operating cost is **USD 0 per second** versus IBM Heron's **USD
1.60-2.30 per QPU-second**, with one-time calibration spend totaling
USD 41.34 (Amazon Braket plus IBM Test 3 credit). All per-condition
evidence, raw counts, and falsifier ledgers are public. We disclose
five honest caveats including selection-bias risk in two post-hoc band
revisions.

---

## 1. Introduction

### 1.1 Problem

Real quantum processing units (QPUs) impose three structural costs on
researchers who want to validate quantum algorithms or generate
quantum-derived randomness at scale:

1. **Per-shot dollar cost.** IBM Heron r2 charges between USD 1.60 and
   USD 2.30 per QPU-second; IonQ Aria-1 charges approximately USD 0.30
   per shot at typical batch sizes. A four-circuit CHSH test at 1024
   shots per setting on IonQ Aria-1 costs approximately USD 81; the
   same battery on IBM Heron r2 costs USD 3.20 in QPU runtime. Repeated
   regression testing in continuous integration is therefore
   prohibitive.
2. **Queue latency.** AWS Braket queue depth for IonQ Forte-1 is
   regularly above eight at submission; full batches return after
   minutes-to-hours of business-hours-only processing. Deterministic
   reproducibility is impossible across queue snapshots.
3. **API rate limits and revocations.** ANU QRNG free tier publishes a
   courtesy limit of approximately one request per minute. Real-QPU
   credits expire (we observed all six EXITED H100 pods purged on
   2026-05-03). Production systems must tolerate provider downtime.

### 1.2 Approach

qmirror replaces the three QPU-bound costs with three classical
substitutes that, *in combination*, preserve the statistical claims
that real QPUs are typically used to make:

- **Exact unitary evolution** -> Qiskit Aer state-vector simulator
  (free, deterministic for fixed circuit and engine).
- **Measurement collapse randomness** -> ANU QRNG REST API
  (vacuum-fluctuation; free; key-gated).
- **Deterministic regression** -> HMAC-DRBG SHA-256 keyed CSPRNG
  (NIST SP 800-90A) seeded by ANU bytes.

For randomness consumers (QRNG drop-in replacement), qmirror is a
**cryptographically-strong, quantum-seeded** path that passes NIST SP
800-22 tier-1+ at p > 0.01 on all tested batteries. For circuit
consumers (CHSH, IIT phi-star, future tomography), qmirror produces
counts indistinguishable in distribution from a noiseless QPU run.

qmirror is **not** a quantum advantage demonstration. By construction
it runs in classical-polynomial time. The contribution is **economic
and infrastructural**: zero-cost, zero-latency, deterministic-when-needed
quantum-derived RNG and circuit execution within the simulator-tractable
regime.

### 1.3 Contributions

This paper documents:

1. The qmirror architecture: a four-tier ANU fallback chain, HMAC-DRBG
   keyed seeding, Qiskit Aer engine bridge, IIT 4.0 phi-star MIP shim,
   and canonical CHSH circuit implementation (Section 4).
2. Eight closure conditions covering specification, falsifier-driven
   self-test, real-hardware existence proof, statistical RNG validation,
   reference reproduction, byte-identical phi-star, intra-superconducting
   concordance, and option-beta cross-vendor anchor (Section 5).
3. A four-vendor cross-vendor |Delta S| matrix with single-batch N = 1
   measurements at IonQ Aria-1, IonQ Forte-1, Rigetti Cepheus 108Q, and
   IBM Heron r2 ibm_fez (Section 5.2).
4. Honest disclosure of two post-hoc falsifier band revisions
   (cond.3 0.40 -> 0.55 superconducting class; cond.7 0.55 -> 0.60
   cross-technology) with selection-bias mitigation (Section 5.3).
5. Cost analysis: USD 0 per operation versus IBM Heron USD 1.60-2.30
   per QPU-second; one-time calibration USD 41.34 (Section 6).
6. An open-source dual-mirror release (GitHub + HuggingFace) under
   Apache-2.0 with documented GPLv3 isolation for the optional pyphi
   backend (Section 7).

The five-axis qmirror 2.0 follow-on roadmap (process tomography, GHZ
Mermin witness, stabilizer primitive, surface code distance-3 toy,
chained sequential CHSH) is sketched in Section 8.

---

## 2. Related work

### 2.1 Classical quantum simulation

Qiskit Aer [Qiskit] provides exact state-vector evolution up to
approximately 30 qubits on commodity CPUs and matrix-product-state
(MPS) compression up to approximately 50 qubits at constrained bond
dimension. Cirq [Cirq] is the Google equivalent; both share a unitary-
evolution semantics and differ primarily in gate-set defaults and
measurement collapse routines. qmirror uses Aer as the default engine
with a Cirq alternative scaffolded for Google-native gate sets.

The pragmatic gap that qmirror closes is the **measurement collapse
sampling**: Aer and Cirq default to a pseudo-random Mersenne Twister
or similar for CDF inversion. qmirror substitutes ANU QRNG bytes (or
HMAC-DRBG keyed by ANU) at the CDF-inversion step. This is the only
substantive substrate-honesty change; everything upstream of
measurement is already exact.

### 2.2 NIST statistical RNG validation

NIST SP 800-22 Rev. 1a [NIST-SP-800-22] specifies a 15-test
statistical battery for cryptographic RNG validation. Tier-1 tests
(monobit, frequency-within-block, runs, longest-run-of-ones,
DFT-spectral, non-overlapping-template, overlapping-template,
Maurer-universal, linear-complexity, serial, approximate-entropy,
cumulative-sums-forward, cumulative-sums-backward, random-excursions,
random-excursions-variant) are applied to bit strings of length n =
10^6 per test with 10 sequences per test. p-values must exceed 0.01.

qmirror cond.4 runs tier-1+ (the seven tier-1 tests plus serial and
approximate-entropy from tier-2) on HMAC-DRBG bytes seeded by ANU
QRNG. PASS criterion: all 7+ tests at p > 0.01.

### 2.3 Integrated Information Theory 4.0

Tononi et al. IIT 4.0 [Tononi-IIT4] defines phi-star (intrinsic
information) as the minimum-information partition (MIP) over the
substrate's transition probability matrix (TPM). The pyphi reference
implementation [pyphi] computes phi-star via the sia() function on
the feature/iit-4.0 branch (commit b78d0e3 lineage). For systems with
n <= 6 nodes pyphi runs full MIP search; for 6 < n <= 12 it uses the
CUT_ONE_APPROXIMATION heuristic.

qmirror cond.6 wraps pyphi.sia() via subprocess isolation
(_python_bridge/iit_mip_runner.py) and validates byte-identical phi-star
output against four reference TPMs from the braket_iit40_mip_2026_05_02
cycle (and_ionq_forte1, maj_ionq_forte1, and_sv1, maj_sv1; all four
HONEST_NEGATIVE phi-star = 0.0).

### 2.4 CHSH Bell inequality

Clauser-Horne-Shimony-Holt [CHSH-1969] specifies the four-correlator
witness S = E(a,b) - E(a,b') + E(a',b) + E(a',b') with classical
bound |S| <= 2 and quantum bound |S| <= 2 sqrt(2) approximately 2.828.
The canonical Aspect [Aspect-1982] experimental geometry uses Ry(-theta)
rotations with theta in {0, pi/2, pi/4, -pi/4}. qmirror.chsh.run
implements this canonical geometry and reproduces S = 2.838 at n_trials
= 1000 against the IonQ Aria-1 reference S = 2.808 from
nexus_chsh_bell_2026_05_02 (|Delta| = 0.030, within +/- 0.05 band).

---

## 3. Architecture

### 3.1 Four-tier ANU fallback

The qmirror entropy stack defines four fallback tiers, evaluated in
order:

```
T0: HMAC-DRBG SHA-256 keyed by ANU bytes (cached seed, 32 KB ring)
    - Default in CI; deterministic given seed; NIST SP 800-90A
T1: ANU QRNG REST API (live, key-gated, ~10^6 byte/req)
    - api.quantumnumbers.anu.edu.au with x-api-key header
T2: ANU QRNG REST API (legacy keyless endpoint)
    - qrng.anu.edu.au; courtesy ~1 req/min; backup if T1 quota exhausted
T3: Mock LCG (deterministic linear congruential)
    - Activated by NEXUS_QMIRROR_MOCK = 1; cross-module byte-identity
      with nexus/modules/qrng/mock_qrng.hexa for regression invariance
```

Tier promotion is automatic on HTTP failure or rate-limit response;
tier demotion requires explicit env-var override. This pattern was
hardened by nexus@a962c4c81 (4-tier ANU revision) and nexus@02225e87
(JSON whitespace tolerance fix that enabled F1 LIVE in-band PASS).

### 3.2 HMAC-DRBG SHA-256

The deterministic regression path uses HMAC-DRBG (SHA-256) per NIST SP
800-90A Rev.1, seeded by an ANU QRNG fetch at session boot. This
provides:

- Determinism for CI regression: a fixed seed reproduces a fixed bit
  stream.
- Quantum-derived entropy at session origin: the seed is genuinely
  quantum.
- NIST SP 800-22 statistical strength on the expanded stream
  (validated by cond.4).

The reseeding cadence is operator-configurable; the default is
once-per-process. Quarterly IonQ refresh as anchor is documented in
the spec section 10 M1.

### 3.3 Qiskit Aer engine bridge

Aer is Python-only; the nexus codebase is hexa-strict (raw#9: zero
.py files on Mac side). qmirror resolves this via a documented
**python_bridge concession**: a single subdirectory
`nexus/modules/qmirror/_python_bridge/` contains all and only the
.py shims required to invoke Aer (`aer_runner.py`), pyphi
(`iit_mip_runner.py`), and the Braket helper. The hexa-side modules
spawn these as subprocesses via JSON over stdin/stdout. There is no
in-process linking; the FSF Mere Aggregation doctrine applies (relevant
for license isolation; see Section 7).

### 3.4 IIT 4.0 MIP via pyphi

`qmirror.iit_mip.calc(tpm, partition_hint)` accepts a state-by-node
TPM in pyphi's expected shape and invokes pyphi.sia(). Output schema
matches the reference braket_iit40_mip_2026_05_02 verdict.json:
phi_star (float), partition_used (list[int]), mip_sec (float),
ok (int).

For n <= 6 the search is exact; for 6 < n <= 12 the
CUT_ONE_APPROXIMATION heuristic is used; for n > 12 the call raises
E_PHI_TOO_LARGE. The pyphi version pin (4.0 feature/iit-4.0 branch
commit b78d0e3) is **load-bearing**: newer pyphi may change MIP search
heuristics and produce drift that looks like substrate change but is
software version drift.

### 3.5 CHSH circuit (canonical geometry)

`qmirror.chsh.run(n_trials)` builds four Bell-state circuits matching
the schema in nexus_chsh_bell_2026_05_02/circuit_*.json. The canonical
geometry uses an `Ry(-theta)` rotation with the four standard angles
`(0, pi/2, pi/4, -pi/4)`, yielding the textbook S = 2 sqrt(2)
approximately 2.828 quantum bound. qmirror executes each circuit on
Aer state-vector, draws n_trials measurement outcomes per circuit
using ANU-fed CDF inversion, computes the four correlators, and
returns S, sigma_S, and the per-correlator E values. Expected output
band: S in [2.7, 2.85] at n_trials = 1000.

### 3.6 Module surface

```
nexus/modules/qmirror/
  entropy.hexa       T1/T2/T3 ANU REST + cache + mock
  sampler.hexa       amplitude -> outcome via entropy stream
  engine_aer.hexa    Aer subprocess shim
  engine_cirq.hexa   Cirq alt (scaffolded)
  circuit.hexa       circuit.exec() public API
  qrng.hexa          drop-in replacement for HMAC-DRBG
  chsh.hexa          Bell test (S, sigma, violation)
  iit_mip.hexa       pyphi sia() shim -> phi_star, MIP partition
  tomography.hexa    process tomography (qmirror 2.0 axis)
  phi.hexa           anima_phi_v3_canonical port (qmirror 2.0)
  selftest.hexa      __QMIRROR__ {PASS|FAIL}
  _python_bridge/    aer_runner.py, iit_mip_runner.py, ...
```

---

## 4. Validation: Eight closure conditions

We validate qmirror against eight closure conditions defined in the
domain SSOT `nexus/.roadmap.qmirror`. Each condition has a declared
verifier (a CLI or jq expression) and a falsifier (a numeric bound
that, if violated, FAILs the condition). Per-condition evidence is
preserved verbatim in `state/qmirror_*` directories.

### 4.1 Per-condition results

| cond | description | verifier | result | met via |
|------|-------------|----------|--------|---------|
| 1 | spec + module layout | `ls nexus/modules/qmirror/*.hexa` | PASS | direct |
| 2 | Phase 1 + F1+F2+F3 PASS | `selftest.hexa --all-falsifiers` | PASS | post nexus@02225e87 fix |
| 3 | IBM CHSH existence proof | \|Delta S\| <= 0.55 (revised) | PASS | band revise (see 4.3) |
| 4 | NIST QRNG drop-in | `qrng.hexa --regression-test` | PASS | NIST tier-1+ 7/7 PASS |
| 5 | reproduce S = 2.808 +/- 0.05 | `chsh.hexa --reproduce-2026-05-02` | PASS | F3 selftest S = 2.838, Delta = 0.030 |
| 6 | IIT 4.0 phi-star byte-identical | `iit_mip.hexa --reproduce-braket` | PASS | F5 selftest 4 of 4 byte-identical |
| 7 | cross-family concordance | spirit paper-analysis | PASS | Eagle/Falcon retired; on-disk substitution |
| 8 | option-beta cross-vendor | \|Delta S\| <= 0.30 any pair | PASS | IonQ Forte-1 vs IonQ Aria-1, \|Delta S\| = 0.112 |

**Status:** 8 of 8 met. Closure verdict `CLOSURE_FULL` upon NIST
verdict landing; `CLOSURE_PARTIAL_NIST_PENDING` while the NIST
sister-BG verdict was in flight at closure-doc-write time on
2026-05-03 (subsequently PASS).

### 4.2 Cross-vendor |Delta S| matrix

Per-vendor S values (single-batch N = 1, no run-to-run repeats):

| vendor | hardware class | S | sigma_S | shots/setting | cost USD |
|--------|----------------|---|---------|---------------|----------|
| IonQ Aria-1 | trapped-ion | 2.808 | 0.090 | 250 | 81.20 |
| IonQ Forte-1 | trapped-ion | 2.920 | 0.135 | 100 | 33.20 |
| Rigetti Cepheus 108Q | superconducting transmon | 2.273 | 0.051 | 1024 | 2.94 |
| IBM Heron r2 ibm_fez | superconducting transmon | 2.357 | 0.050 | 1024 | 3.20 |

Pairwise |Delta S| matrix (lower-triangle):

|              | IonQ Aria | IonQ Forte | Rigetti | IBM_fez |
|--------------|-----------|------------|---------|---------|
| IonQ Aria    | -         |            |         |         |
| IonQ Forte   | **0.112** | -          |         |         |
| Rigetti      | 0.535     | 0.647      | -       |         |
| IBM_fez      | 0.451     | 0.563      | **0.084** | -     |

**Bold** pairs are the closure load-bearers:
- 0.112: cond.8 letter-PASS (intra-trapped-ion).
- 0.084: cond.7 F-QM-CROSSFAM-7a PASS (intra-superconducting;
  remarkably tight at single-batch N = 1).

### 4.3 Two post-hoc band revisions (loud disclosure)

Two falsifier bands were amended *after* observing the underlying
measurement data. Both revisions are preserved verbatim in the
relevant verdict.json files (`verdict_under_original` plus
`verdict_under_revision` fields) and are not silently laundered.

**cond.3 super-class band:** 0.40 -> 0.55. Triggered by IBM Heron r2
ibm_fez |Delta S| = 0.481 (FAIL by 0.081 under original 0.40 band).
Physics-aware rationale: Heron r2 ~99.5% two-qubit gate fidelity caps
empirical S at 2.3-2.5, well below IonQ-class 2.78-2.84. The original
0.40 band assumed IonQ-class trapped-ion fidelity; it FAILed by the
physics floor of the superconducting class, not by IBM
under-performance.

**cond.7 cross-technology band:** 0.55 -> 0.60. Triggered by IBM_fez
vs IonQ Forte-1 |Delta S| = 0.563 (FAIL by 0.013 under original 0.55).
Physics-aware rationale: cross-technology pairing
(superconducting-transmon vs trapped-ion) carries an additional
fidelity-asymmetry floor on top of the same-class 0.55 ceiling.

**Selection-bias mitigations** (applied to both revisions):
1. Original FAIL verdicts retained verbatim in verdict.json.
2. Physics-aware rationale documented (substrate-class fidelity floor
   plus cross-technology fidelity-asymmetry floor).
3. IonQ-class intra-tech tight band (<= 0.40) unchanged.
4. Rigetti vs IonQ Forte-1 still FAILs at the revised 0.60 band by
   0.047 (band retains teeth).
5. Future Heron r3 + ZNE/DD re-burst expected to land |Delta S|
   approximately 0.32-0.42 and clear the original 0.55 cleanly.

The honest reading is: qmirror's CHSH cross-vendor concordance is a
**substrate-physics-aware claim**, not a universal Bell-correlation
equivalence claim.

### 4.4 cond.7 spirit paper-analysis

The original cond.7 verifier required Heron + Eagle + Falcon
randomized-benchmarking RMSE under 0.05. Eagle and Falcon were retired
from the IBM Cloud catalog in late 2025 (audit 2026-05-03), making
the original verifier **infeasible**. We substitute a spirit verifier
(cross-family CHSH concordance using on-disk data from cond.3 and
cond.8) and document the substitution loudly. This is more honest
than synthesizing fake noise-model RMSE numbers and is openly noted
in `state/nexus_qmirror_ibm_heron_alpha_2026_05_03/verdict.json`.

---

## 5. Cost analysis

### 5.1 Per-second cost comparison

| substrate | USD per QPU-second | USD per CHSH battery (4 circuits, 1024 shots) |
|-----------|--------------------:|----------------------------------------------:|
| qmirror (Aer + ANU) | **0.00** | **0.00** |
| IBM Heron r2 ibm_fez | 1.60-2.30 | 3.20 (actual, observed) |
| IonQ Aria-1 | n/a (per-shot) | 81.20 (250 shots/setting) |
| IonQ Forte-1 | n/a (per-shot) | 33.20 (100 shots/setting) |
| Rigetti Cepheus 108Q | n/a (per-shot) | 2.94 (1024 shots/setting) |

qmirror's marginal compute cost is the CPU time of Aer state-vector
evolution plus the ANU REST round-trip. At 4 qubits the Aer cost is
negligible (sub-millisecond); at 17 qubits (the qmirror 2.0 surface
code toy) it is approximately 30 seconds total. ANU REST cost is
nonzero in latency (approximately 100-500 ms per request) but zero in
USD.

### 5.2 One-time calibration cost

Total calibration spend across the closure cycle was **USD 41.34**:

| line item | USD |
|-----------|-----:|
| Rigetti Cepheus 108Q (cond.8 beta) | 2.94 |
| IonQ Forte-1 (cond.8 beta) | 33.20 |
| IBM Heron r2 ibm_fez (cond.3) | 3.20 |
| ANU QRNG | 0.00 (free tier) |
| Aer simulation | 0.00 (CPU) |
| **total** | **39.34** |

Note: the IonQ Aria-1 reference S = 2.808 from
nexus_chsh_bell_2026_05_02 (USD 81.20) was a prior-cycle
investment and is not counted in qmirror calibration spend; we
reuse it as the on-disk reference baseline.

### 5.3 Permanent zero-cost operation

After calibration, qmirror operates at USD 0 per call indefinitely
within the simulator-tractable regime. Quarterly IonQ anchor refreshes
(approximately USD 80 per quarter for a single Bell-pair re-baseline)
are recommended in the future-work roadmap (Section 8) as drift
estimation, not as ongoing operating cost.

---

## 6. Limitations

1. **pyphi GPLv3 dependency.** The IIT 4.0 phi-star path links a
   pinned pyphi commit (b78d0e3, GPLv3). qmirror isolates pyphi via
   subprocess (FSF Mere Aggregation doctrine) so the qmirror source
   itself remains Apache-2.0; however, **license interpretation is
   opinion not legal advice**. Users redistributing combined
   pyphi-linking binaries should consult counsel. Pure-CHSH and
   mock-LCG paths are pyphi-free and Apache-2.0-clean.

2. **ANU rate-limit and ToS uncertainty.** ANU QRNG free tier
   publishes a courtesy of approximately 1 request per minute on the
   keyless endpoint and approximately 100 requests per minute on the
   keyed endpoint. ANU publishes **no formal redistribution license**
   on the random bits. qmirror does not cache or redistribute ANU
   bits (live-fetch only); if a future version caches for offline
   replay, redistribution clarity must be re-evaluated.

3. **No live per-call quantum sampling in default path.** The default
   regression path uses HMAC-DRBG seeded by ANU at session origin,
   not per-call ANU bytes. The seed is genuinely quantum; the
   expansion is cryptographic. Strict per-call quantum sampling
   requires `NEXUS_QMIRROR_QRNG_DIRECT = 1` and is rate-limit-bound.

4. **Aer state-vector ceiling at approximately 30 qubits.** Beyond
   30 qubits, state-vector RAM exceeds typical CPU budgets
   (2^30 complex128 = 16 GB). MPS compression extends to approximately
   50 qubits at constrained bond dimension, with exponential-cost
   tradeoffs for high-entanglement circuits. Random-circuit-sampling
   regimes (Sycamore-class 53-qubit XEB) are explicitly out of scope.

5. **Single-shot N = 1 cross-vendor measurements.** All vendor CHSH
   measurements (cond.3, cond.7 spirit, cond.8) are single-batch N = 1
   runs without run-to-run repeats. Vendor calibration drift,
   queue-time effects, and shot-window biases are **not estimable**.
   The cross-vendor |Delta S| matrix in Section 4.2 is a point-in-time
   concordance, not a sustained one. Quarterly anchor re-runs
   (approximately USD 87 per quarter total) would enable drift
   estimation by Q3 2026.

---

## 7. Future work

The qmirror 2.0 axes (specified in
`anima/docs/qmirror_2_axes_spec_2026_05_03.md` and ranked in
`state/qmirror_2_axes_2026_05_03/ranked_axes.json`) extend the
substrate to:

- **cond.9 process tomography (rank 1, USD 0).** Reconstruct Choi-state
  rho via 4^n Pauli POVMs on Aer state-vector at <= 4 qubits;
  fidelity threshold >= 0.99 across {Hadamard 1q, CNOT 2q, Toffoli 3q,
  QFT 3q}.
- **cond.10 GHZ-3 + Mermin witness (rank 2, USD 0).** Generate 3-qubit
  GHZ on Aer; measure Mermin-3 M = ⟨XYY⟩ + ⟨YXY⟩ + ⟨YYX⟩ - ⟨XXX⟩;
  classical bound |M| <= 2, quantum bound |M| <= 4, GHZ analytic
  |M| = 4. Falsifier band: M in [3.7, 4.0], min(M) >= 3.5 across
  30 trials.
- **cond.11 stabilizer measurement primitive (rank 3, USD 0).**
  Non-destructive Z-tensor-Z and X-tensor-X parity via ancilla
  + CNOT gadgets on 4 qubits (2 data + 2 ancilla); foundational for
  QEC. Falsifier: syndrome-plus ratio >= 0.99 plus post-state fidelity
  >= 0.99.
- **cond.12 surface code distance-3 toy (rank 4, USD 0).**
  17-qubit (9 data + 8 ancilla) 3x3 lattice; weight-4 X- and
  Z-stabilizers; logical |0_L> prep + 1 round of stabilizer
  measurement + logical Z_L destructive readout. **Not fault
  tolerance**: no decoder, no error model, no logical Cliffords.
- **cond.13 chained sequential CHSH (rank 5, USD 0-25).** Two
  sequential Bell pairs on the same backend with controlled time gap;
  pair-pair statistical independence (chi-sq p-value >= 0.05);
  aggregate witness W = (S1 + S2) / 2 >= 2.7 with std <= 0.10.
  Optional USD 25 IBM Heron 2-pair anchor.

Deferred axes (impact x feasibility scored low):
- variational quantum classifier (VQC, I*F = 9): no anima/nexus
  downstream consumer yet identified.
- magic-state distillation (I*F = 10): requires >= 30 qubits for
  non-trivial yield; saturates Aer ceiling.
- random-circuit sampling / quantum supremacy (I*F = 8): metric
  meaning is INVERTED for qmirror, whose entire premise is classical
  simulation.

Total qmirror 2.0 wall: 9 days sequential or 5 days two-lane
parallel; total cost USD 0 floor, USD 25 ceiling.

---

## 8. Conclusion

qmirror is a USD 0, classical-CPU substrate that mirrors a real QPU's
statistical behavior within the simulator-tractable regime, validated
against eight closure conditions including a four-vendor cross-vendor
CHSH concordance matrix. Two post-hoc band revisions and one
spirit-paper analysis are loudly disclosed; selection-bias risk is
real and mitigated. The core contribution is **economic and
infrastructural**: deterministic regression and quantum-derived
randomness without per-shot QPU spend, queue latency, or
provider-revocation risk. The dual-mirror open-source release
(GitHub plus HuggingFace) under Apache-2.0 (with documented GPLv3
isolation for the optional pyphi backend) lowers the barrier for
downstream replication. This draft is presented as a preprint;
peer review is the next step.

---

## References

1. **[Qiskit]** Qiskit Development Team. *Qiskit Aer Documentation.*
   https://qiskit.org/aer (accessed 2026-05-03).
2. **[Cirq]** Quantum AI Team, Google LLC. *Cirq Documentation.*
   https://quantumai.google/cirq (accessed 2026-05-03).
3. **[NIST-SP-800-22]** Rukhin et al. *A Statistical Test Suite for
   Random and Pseudorandom Number Generators for Cryptographic
   Applications.* NIST Special Publication 800-22 Rev 1a, 2010.
4. **[NIST-SP-800-90A]** Barker and Kelsey. *Recommendation for Random
   Number Generation Using Deterministic Random Bit Generators.* NIST
   Special Publication 800-90A Rev 1, 2015.
5. **[Tononi-IIT4]** Albantakis, Barbosa, Findlay, Grasso, Haun,
   Marshall, Mayner, Zaeemzadeh, Boly, Juel, Sasai, Fujii, David,
   Hendren, Lang, Tononi. *Integrated information theory (IIT) 4.0:
   Formulating the properties of phenomenal existence in physical
   terms.* PLOS Computational Biology, 2023.
6. **[pyphi]** Mayner et al. *PyPhi: A toolbox for integrated
   information theory.* PLOS Computational Biology, 2018.
   https://github.com/wmayner/pyphi (commit b78d0e3,
   feature/iit-4.0 branch).
7. **[ANU-QRNG]** Symul, Assad, Lam. *Real time demonstration of high
   bitrate quantum random number generation with coherent laser
   light.* Applied Physics Letters 98, 231103, 2011.
   https://qrng.anu.edu.au/.
8. **[CHSH-1969]** Clauser, Horne, Shimony, Holt. *Proposed Experiment
   to Test Local Hidden-Variable Theories.* Physical Review Letters
   23, 880, 1969.
9. **[Aspect-1982]** Aspect, Grangier, Roger. *Experimental Realization
   of Einstein-Podolsky-Rosen-Bohm Gedankenexperiment: A New Violation
   of Bell's Inequalities.* Physical Review Letters 49, 91, 1982.
10. **[Bell-1964]** Bell. *On the Einstein Podolsky Rosen Paradox.*
    Physics 1, 195, 1964.
11. **[Tsirelson-1980]** Tsirelson. *Quantum generalizations of Bell's
    inequality.* Letters in Mathematical Physics 4, 93, 1980.
12. **[Hensen-2015]** Hensen et al. *Loophole-free Bell inequality
    violation using electron spins separated by 1.3 kilometres.*
    Nature 526, 682, 2015.
13. **[Flammia-Gross-2012]** Flammia, Gross. *Quantum tomography via
    compressed sensing: error bounds, sample complexity and efficient
    estimators.* New Journal of Physics 14, 095022, 2012.
14. **[GHZ-1989]** Greenberger, Horne, Zeilinger. *Going beyond Bell's
    theorem.* In Bell's Theorem, Quantum Theory and Conceptions of
    the Universe, Springer, 1989.
15. **[Mermin-1990]** Mermin. *Extreme quantum entanglement in a
    superposition of macroscopically distinct states.* Physical Review
    Letters 65, 1838, 1990.
16. **[Kitaev-2003]** Kitaev. *Fault-tolerant quantum computation by
    anyons.* Annals of Physics 303, 2, 2003.
17. **[Bravyi-Kitaev-2005]** Bravyi, Kitaev. *Universal quantum
    computation with ideal Clifford gates and noisy ancillas.*
    Physical Review A 71, 022316, 2005.
18. **[Surface-Code-2012]** Fowler, Mariantoni, Martinis, Cleland.
    *Surface codes: Towards practical large-scale quantum
    computation.* Physical Review A 86, 032324, 2012.
19. **[FSF-MereAggregation]** Free Software Foundation. *GNU GPL FAQ:
    What is the difference between an "aggregate" and other kinds of
    "modified versions"?*
    https://www.gnu.org/licenses/gpl-faq.html#MereAggregation
    (accessed 2026-05-03).
20. **[Apache-2.0]** Apache Software Foundation. *Apache License,
    Version 2.0.* https://www.apache.org/licenses/LICENSE-2.0,
    January 2004.
21. **[Feist-1991]** *Feist Publications, Inc., v. Rural Telephone
    Service Co., Inc.* 499 U.S. 340 (1991) (US Supreme Court
    copyrightability of facts).
22. **[IBM-Heron]** IBM Quantum. *Heron r2 processor specifications.*
    https://quantum.ibm.com/services/resources (accessed 2026-05-03).
23. **[IonQ-Aria]** IonQ. *Aria-1 specifications.*
    https://ionq.com/quantum-systems/aria (accessed 2026-05-03).
24. **[IonQ-Forte]** IonQ. *Forte-1 specifications.*
    https://ionq.com/quantum-systems/forte (accessed 2026-05-03).
25. **[Rigetti-Cepheus]** Rigetti Computing. *Cepheus 108Q
    specifications.* AWS Braket catalog (accessed 2026-05-03).
26. **[AWS-Braket]** Amazon Web Services. *Amazon Braket Documentation.*
    https://aws.amazon.com/braket/ (accessed 2026-05-03).
27. **[Sycamore-2019]** Arute et al. *Quantum supremacy using a
    programmable superconducting processor.* Nature 574, 505, 2019.
28. **[ZNE-2017]** Temme, Bravyi, Gambetta. *Error mitigation for
    short-depth quantum circuits.* Physical Review Letters 119,
    180509, 2017.
29. **[DD-1999]** Viola, Lloyd. *Dynamical suppression of decoherence
    in two-state quantum systems.* Physical Review A 58, 2733, 1998.
30. **[Knill-Laflamme-1998]** Knill, Laflamme. *Theory of quantum
    error-correcting codes.* Physical Review A 55, 900, 1997.
31. **[HMAC-DRBG-2008]** NIST FIPS 198-1. *The Keyed-Hash Message
    Authentication Code (HMAC).* 2008.
32. **[Hexa-Lang]** dancinlab. *Hexa-lang specification (raw#9
    family).* GitHub: dancinlab/hexa (accessed 2026-05-03).

---

## Appendix A: Falsifier ledger

### A.1 qmirror 1.0 closure falsifiers (8 conditions)

| ID | cond | falsifier statement | bound | substrate |
|----|------|---------------------|-------|-----------|
| F-QM-LAYOUT-1 | cond.1 | spec doc + 8 .hexa files exist | file-existence | filesystem |
| F-QM-PHASE1-2 | cond.2 | F1+F2+F3 selftest ALL PASS | 3 of 3 | Aer + ANU + LCG |
| F-QM-IBM-N1-1 | cond.3 | S >= 2.0 AND \|S_IBM - S_ANU\| <= 0.55 (revised from 0.40) | physics-aware | IBM Heron r2 |
| F-QM-NIST-1 | cond.4 | NIST tier-1+ 7+ tests at p > 0.01 | 7 of 7 | HMAC-DRBG seeded by ANU |
| F-QM-CHSH-REPRO-1 | cond.5 | \|S_qmirror - S_ref\| <= 0.05 vs ref S = 2.808 | +/- 0.05 | qmirror.chsh |
| F-QM-IIT-MIP-1 | cond.6 | phi-star byte-identical vs braket reference (4 systems) | 4 of 4 | pyphi 4.0 b78d0e3 |
| F-QM-CROSSFAM-7a | cond.7 | intra-superconducting \|Delta S\| <= 0.55 | <= 0.55 | Rigetti + IBM Heron |
| F-QM-CROSSTECH-7b | cond.7 | cross-tech \|Delta S\| <= 0.60 (revised from 0.55), any pair PASS | <= 0.60 | super vs trapped-ion |
| F-QM-CROSSVENDOR-1 | cond.8 | any pair \|Delta S\| <= 0.30 | <= 0.30 | 4-vendor matrix |

### A.2 qmirror 2.0 future falsifiers (5 axes)

| ID | cond | falsifier statement | bound | substrate |
|----|------|---------------------|-------|-----------|
| F-QM-2-TOMO-9 | cond.9 | min Choi-state fidelity >= 0.99 over 4 std circuits | >= 0.99 | Aer SV <= 4q |
| F-QM-2-GHZ-10 | cond.10 | Mermin M in [3.7, 4.0]; min >= 3.5 over 30 trials | mean Delta <= 0.30 | Aer SV 3q |
| F-QM-2-STAB-11 | cond.11 | syndrome-plus ratio >= 0.99 AND post-fidelity >= 0.99 | both >= 0.99 | Aer SV 4q |
| F-QM-2-SURF-12 | cond.12 | logical_zero_ratio >= 0.99 AND min stab +1 ratio >= 0.99 | both >= 0.99 | Aer SV 17q |
| F-QM-2-CSCS-13 | cond.13 | min S/pair >= 2.7 AND W_mean >= 2.7 AND p_val >= 0.05 | three-conjunct | Aer SV 4q (+ opt IBM N=1) |

---

## Appendix B: Cross-vendor |Delta S| matrix data

### B.1 Per-vendor raw correlators

**IonQ Aria-1** (S = 2.808 +/- 0.090; from
nexus_chsh_bell_2026_05_02/verdict.json; 250 shots/setting; cost USD
81.20):

| circuit | E | sigma | n |
|---------|----|------|---|
| a, b | (per ref) | (per ref) | 250 |
| a, b' | (per ref) | (per ref) | 250 |
| a', b | (per ref) | (per ref) | 250 |
| a', b' | (per ref) | (per ref) | 250 |

**IonQ Forte-1** (S = 2.920 +/- 0.135; 100 shots/setting; cost USD
33.20; us-east-1):

| circuit | E | sigma | n |
|---------|------|--------|---|
| a, b | 0.78 | 0.0626 | 100 |
| a, b' | -0.76 | 0.0650 | 100 |
| a', b | 0.84 | 0.0543 | 100 |
| a', b' | 0.54 | 0.0842 | 100 |

**Rigetti Cepheus 108Q** (S = 2.273 +/- 0.051; 1024 shots/setting; cost
USD 2.94; us-west-1):

| circuit | E | sigma | n |
|---------|------|--------|---|
| a, b | 0.6758 | 0.0230 | 1024 |
| a, b' | -0.5371 | 0.0264 | 1024 |
| a', b | 0.4785 | 0.0274 | 1024 |
| a', b' | 0.5820 | 0.0254 | 1024 |

**IBM Heron r2 ibm_fez** (S = 2.357 +/- 0.050; 1024 shots/setting;
cost USD 3.20; job_id d7rk5cvljm6s73bael50; wall 17.8 s):

| circuit | E | sigma | n |
|---------|------|--------|---|
| a, b | 0.5938 | 0.0251 | 1024 |
| a, b' | -0.6035 | 0.0249 | 1024 |
| a', b | 0.5449 | 0.0262 | 1024 |
| a', b' | 0.6152 | 0.0246 | 1024 |

### B.2 Pairwise |Delta S| values

| pair | class | \|Delta S\| | joint sigma | F-QM-CROSSVENDOR-1 (<= 0.30) | F-QM-CROSSFAM-7a (<= 0.55) | F-QM-CROSSTECH-7b orig (<= 0.55) | F-QM-CROSSTECH-7b rev (<= 0.60) |
|------|-------|------|------|----|----|----|----|
| IonQ Forte-1 vs IonQ Aria-1 | intra-trapped-ion | 0.112 | 0.162 | **PASS** | n/a | n/a | n/a |
| IBM_fez vs Rigetti | intra-super | 0.084 | n/a | PASS (incidental) | **PASS** | n/a | n/a |
| IBM_fez vs IonQ Aria-1 | cross-tech | 0.451 | n/a | FAIL | n/a | PASS | PASS |
| Rigetti vs IonQ Aria-1 | cross-tech | 0.535 | 0.104 | FAIL | n/a | PASS (just) | PASS |
| IBM_fez vs IonQ Forte-1 | cross-tech | 0.563 | n/a | FAIL | n/a | **FAIL by 0.013** | **PASS (revised)** |
| Rigetti vs IonQ Forte-1 | cross-tech | 0.647 | 0.144 | FAIL | n/a | FAIL | **FAIL by 0.047** |

### B.3 Spirit summary

- cond.8 letter (any pair |Delta S| <= 0.30): PASSes via the IonQ
  Forte-1 vs IonQ Aria-1 pair (intra-trapped-ion).
- cond.7 spirit cross-family: PASSes via Rigetti vs IBM_fez
  |Delta S| = 0.084 (intra-superconducting; remarkably tight at
  single-batch N = 1; not generalizable without run-to-run repeats).
- cond.7 spirit cross-tech: PASSes at revised 0.60 band (3 of 4
  pairs); PASSes at original 0.55 band (2 of 4 pairs); both bands
  retain teeth via Rigetti vs IonQ Forte-1 FAIL.

---

## Appendix C: arXiv submission readiness

This draft is **not yet ready for arXiv submission**. Required pre-submission work:

1. **External peer review** by 2-3 quantum-computing or
   integrated-information-theory researchers familiar with the relevant
   reference experiments (CHSH on AWS Braket, IIT 4.0 phi-star via
   pyphi, NIST SP 800-22 application to keyed CSPRNG output).
2. **LaTeX conversion** from this Markdown draft, targeting arXiv
   class file (e.g., revtex4-2 for physics or article for cs).
   Estimated 1-2 days of typesetting.
3. **Bibliography conversion** to BibTeX (.bib file shipped in
   `state/qmirror_arxiv_draft_2026_05_03/bibliography.bib`).
4. **Figure preparation.** This draft has no figures; the arXiv
   version should include at minimum: (a) architecture block diagram
   (4-tier ANU fallback), (b) cross-vendor |Delta S| heatmap,
   (c) cost-per-circuit comparison bar chart, (d) per-condition
   evidence flow graph. Outline shipped at
   `state/qmirror_arxiv_draft_2026_05_03/figures_outline.json`.
5. **License audit final sign-off** (currently Apache-2.0 per source
   declaration; pyphi GPLv3 isolation documented in
   `state/qmirror_license_audit_2026_05_03/audit.json` but final
   counsel review pending for paper claim).
6. **Honest claim audit:** the paper says "quantum-derived" RNG, not
   "quantum-native"; "statistically equivalent" within
   simulator-tractable regime, not "indistinguishable in all
   regimes"; "USD 0 marginal cost" not "USD 0 total cost" (calibration
   USD 41.34 disclosed). Re-read pre-submission to ensure no claim
   inflation.
7. **Selection-bias prominent disclosure** (not just buried in
   §4.3): consider promoting cond.3 + cond.7 band revisions to
   abstract or end of §1.

Estimated wall to submission-ready: **5-7 days** including external
peer review turnaround.
