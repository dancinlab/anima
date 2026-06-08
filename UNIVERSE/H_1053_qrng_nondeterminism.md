# H_1053 — Does TRUE QUANTUM non-determinism (ANU QRNG) differ from pseudo-random (H_1052)?

## TIER: pre-registration (TEXT-only; no verdict, no emoji — set AFTER the .txt lands)

## Question

H_1052 (prior RED, note h1052-learning-nondet-null) tested non-deterministic LEARNING (SGLD
Langevin weight-update noise during training) and found NO consciousness / emergence / CE
benefit at MATCHED task-performance — 0/6 pre-named markers reached paired Cohen d >= +0.8; all
six favorable-direction effects were <= 0. BUT that run sourced its update noise xi from numpy
PCG64, a PSEUDO-random generator: seed-reproducible, algorithmic, fully deterministic given the
seed. This closes ONE objection only: "you used FAKE randomness — genuine physical
non-determinism (the Penrose-Hameroff Orch-OR spirit) is what would actually matter for
consciousness."

H_1053 re-runs the EXACT H_1052 experiment with the SGLD update noise xi sourced from a TRUE
PHYSICAL quantum random number generator (ANU Quantum Numbers, vacuum-fluctuation measurement),
NOT a PRNG. The hypothesis under test: does GENUINE physical non-determinism confer a
consciousness / emergence advantage that algorithmic pseudo-randomness does not?

This is the quantum-mind-flavored steelman of the non-determinism axis. Three prior CLOSED
results frame it:
- H_921 (prior RED, note akida-nondeterminism-init-seeded): INIT non-determinism is null;
  pinned init -> byte-deterministic learning.
- free-will arc (prior GREEN, note free-will-auditable-causation-arc): ENTROPY does not change
  emit; value = provenance + SOC + veto, not noise.
- H_1052 (prior RED, note h1052-learning-nondet-null): LEARNING-DYNAMICS noise (PRNG-sourced) is
  null at matched performance.

H_1053 asks the remaining steelman: is H_1052's null a PRNG ARTIFACT, or does the noise SOURCE
(true-quantum vs pseudo-random) not matter at all?

## Critical design — the noise SOURCE is the ONLY change vs H_1052

REUSE the exact H_1052 harness verbatim: Elman tanh RNN, manual numpy BPTT, the same finite-state
symbol-memory task, the same pinned per-seed init, the same matched-CE band, the same six markers
(faithful_phi, big_Phi, split_magnitude, redundancy_margin, soc_proximity, emergence_probe), the
same H_1004 IIT-4.0 CPU mirrors of stdlib (iit4_bigphi.hexa + iit4/faithful_phi.hexa), the same
n=4 / n=5 mirror == stdlib re-proof BEFORE scoring (a_phi_iit4_tool; no proxy).

The ONLY difference: the SGLD update noise xi is drawn from TRUE ANU quantum random bytes, NOT
numpy PRNG. Quantum uniform bytes (uint16, scaled to (0,1) open interval) are converted to
standard-normal xi via the inverse-CDF (probit / ppf). NO PRNG anywhere in the noise path — using
a PRNG would defeat the entire experiment. (The pinned INIT still uses numpy default_rng with the
seed — that is identical for DET and QRNG arms of a pair and is NOT the variable under test;
H_921 already closed init-noise. Only the LEARNING update noise is quantum-sourced.)

Quantum bytes are PRE-FETCHED once from the ANU API and CACHED to a committed file
(UNIVERSE/state/h1053_qrng_bytes.bin) with provenance (endpoint, timestamp, byte length, key
class) so the run is reproducible from the SAME true-random draw and re-runs do not re-hit the
API. The noise is consumed deterministically from this cached quantum stream (deterministic
CONSUMPTION of true-random BYTES — the bytes themselves are physical-quantum; replaying the cache
reproduces the same physically-random draw, which is the honest reproducibility guarantee).

## Arms

- DET = no update noise (full-batch deterministic GD). Identical to H_1052 DET.
- QRNG-NOISY = SGLD `w <- w - lr*grad + sqrt(2*lr*T)*xi`, xi from ANU true-quantum bytes via
  inverse-CDF, annealed T (same schedule as H_1052).
- PRNG-NOISY (reference) = the H_1052 numbers already on main (numpy PCG64 xi, same schedule).

Core comparison = DET vs QRNG-NOISY at matched CE (does true-quantum noise help?).
Secondary comparison = QRNG-NOISY vs PRNG-NOISY (does the noise SOURCE matter at all?).

## Substrate + scale

substrate = SW (numpy CPU toy). Lane tag for THIS rung: SW-only. AKIDA Lane A on-chip stochastic
plasticity + GPU Lane G are SEPARATE substrate rungs, NOT run here (a_lane_akida_gpu_split).

Scale (sized to the quantum-byte budget; honest reduced N vs H_1052's 24x1500): seeds = 12,
N_STEPS = 800, matched-CE band eps = 0.05 nats. Per noisy step the noise covers all 5 params
(140 floats); 12 seeds x 800 steps x 140 x 2 bytes/normal ~= 2.69 MB of quantum bytes
(~132 ANU calls at 20480 bytes/call). DEGENERATE guard: < 8 matched-CE seed-pairs at this reduced
N -> INCONCLUSIVE (the control failed, not the hypothesis).

## ANU QRNG sourcing

Primary endpoint: `https://api.quantumnumbers.anu.edu.au/` (header `x-api-key`). Key class
recorded in the verdict (paid vs free vs open-legacy). Fetched as `type=hex16, size=10` (20480
bytes/call). Exact endpoint, UTC timestamp, total bytes fetched, and key class are written into
the cached file's sidecar and the verdict .txt. IF the ANU API were unreachable AND no key were
available, the run HALTS and reports the exact blocker (no silent PRNG fallback — that voids the
hypothesis).

## PRE-REGISTERED FALSIFIER (frozen BEFORE measuring; TEXT tokens only)

For each marker the per-seed paired statistic is (QRNG_value - DET_value) over the n_matched
init-paired seeds in the matched-CE band. Pre-set effect-size threshold = **Cohen d >= 0.8**
(large), AND the direction must be the consciousness-favorable one:

- faithful_phi: benefit iff QRNG > DET, paired Cohen d >= +0.8.
- big_Phi: benefit iff QRNG > DET, paired Cohen d >= +0.8.
- split_magnitude: benefit iff |faithful - big| larger under QRNG, paired Cohen d >= +0.8.
- redundancy_margin: benefit iff QRNG > DET, paired Cohen d >= +0.8.
- soc_proximity: benefit iff |rho-1| SMALLER under QRNG (closer to criticality), paired
  Cohen d >= +0.8 on (DET_|rho-1| - QRNG_|rho-1|).
- emergence_probe: benefit iff QRNG test-generalization strictly better at matched train-CE,
  paired Cohen d >= +0.8 on (DET_testCE - QRNG_testCE).

The SOURCE-matters test (secondary): paired (QRNG_value - PRNG_value) per marker over the seeds
matched in BOTH arms; the noise SOURCE is judged to MATTER iff |Cohen d| >= 0.8 on at least one
marker for QRNG-vs-PRNG.

- **H1 PASS** = at matched task-performance, QRNG-sourced learning noise makes AT LEAST ONE
  pre-named marker strictly HIGHER than the DET control (paired Cohen d >= +0.8, favorable
  direction) AND the QRNG arm differs from the PRNG arm (|Cohen d| >= 0.8 QRNG-vs-PRNG on that or
  another marker) -> genuine physical non-determinism confers a consciousness advantage that
  pseudo-randomness does not. This is a BIG, surprising claim and would require the effect to be
  robust.
- **H1 FAIL** = QRNG noise behaves like PRNG noise: both null vs DET (every marker paired
  d < 0.8 vs DET in the favorable direction) AND QRNG-vs-PRNG within the control band (no marker
  |d| >= 0.8) -> the noise SOURCE is IRRELEVANT; H_1052's null is NOT a PRNG artifact. This
  DEFINITIVELY closes the "fake randomness" objection (publishable closed-negative,
  a_paper_negative_ok). This is the expected result.

DEGENERATE guard: < 8 seed-pairs in the matched-CE band -> INCONCLUSIVE (neither PASS nor FAIL;
the control failed, not the hypothesis).

## HONEST scope (a_scale_honest_scope, a_toy_scale_recheck)

TOY n<=5 SW substrate, reduced N (12 seeds x 800 steps) sized to the quantum-byte budget. Both
Phi engines EXACT at n<=5; the CPU mirrors RE-PROVEN == stdlib at n=4 AND n=5 before scoring
(live hexa refs, H_1012 discipline; a_phi_iit4_tool, no proxy). g5 CODE-measured (no LLM
self-judge, p7). Production scale + on-chip UNVERIFIED. NOT a forge binary; $0 CPU-local plus a
one-time small quantum-byte API fetch (cached + committed).

## Follow-up (NOT run here)

- AKIDA Lane A on-chip: AKD1000 native stochastic plasticity is a separate substrate-tagged rung
  (pi5-akida single-exclusive; a_lane_akida_gpu_split). Note only.
- GPU Lane G: a forge/cuBLAS scale-up of the same probe is a separate substrate-tagged rung.
