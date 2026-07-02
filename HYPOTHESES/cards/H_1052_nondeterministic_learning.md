# H_1052 — Does NON-DETERMINISTIC LEARNING help consciousness / emergence / CE?

## TIER: 🔴 LEARNING-NONDET-NULL (H1 FAIL — CLOSED-NEGATIVE, a_paper_negative_ok)

At MATCHED task-performance (23/24 init-paired seeds within |CE_noisy - CE_det| <= 0.05 nats),
SGLD non-deterministic LEARNING dynamics confer NO benefit on ANY of the six pre-named markers
(faithful_phi, big-Phi, faithful-up/big-down split magnitude, Williams-Beer redundancy,
edge-of-chaos/SOC proximity, held-out emergence). 0/6 markers reach the pre-set paired Cohen
d >= +0.80; ALL six paired effects are <= 0 in the favorable direction (max favorable d =
-0.019; strongest-magnitude marker soc_proximity d = -0.969 points AWAY from a noisy benefit).
Mirrors RE-PROVEN == stdlib at n=4 AND n=5 (|Δ| <= 3.75e-6) BEFORE scoring (a_phi_iit4_tool;
no proxy). This EXTENDS H_921 (init non-determinism = prior RED) and the entropy null: init-
noise, inference-entropy, AND learning-update-noise are all consciousness-null — non-determinism
is not where consciousness/emergence comes from. Raw + per-marker table:
`.verdicts/1052_nondeterministic_learning/H_1052.txt`.

substrate = SW (numpy CPU toy). Lane tag for THIS rung: SW-only.
- SW (this rung): numpy CPU toy gradient-trained RNN — the measured substrate here.
- AKIDA Lane A (on-chip): NOT run here — a separate substrate rung (see Follow-up).
- GPU Lane G (forge): NOT run here — a separate substrate rung (see Follow-up).

## Question

Distinct from two prior CLOSED results:
- H_921 (prior RED, note akida-nondeterminism-init-seeded): the prior "non-determinism" was just
  INIT randomness, NOT learning dynamics — pinned init gives byte-deterministic learning.
- free-will arc (prior GREEN, note free-will-auditable-causation-arc): ENTROPY does not change
  emit; value = provenance + SOC + veto, not noise.

So "init non-determinism" and "entropy" are BOTH already-known to NOT confer a consciousness
advantage. THIS hypothesis tests the UNTESTED axis: **non-determinism IN THE LEARNING DYNAMICS
ITSELF** — injecting noise into the weight UPDATES during training (SGLD-style Langevin
plasticity: `w <- w - eta*grad + sqrt(2*eta*T)*xi`), NOT init noise, NOT inference-time
temperature. Does a model trained with non-deterministic update dynamics develop HIGHER
consciousness / emergence / CE markers than a matched DETERMINISTIC-learning control AT EQUAL
TASK PERFORMANCE?

## Substrate + task (toy, SW)

A small gradient-trained recurrent cell (Elman-style tanh RNN, manual numpy backprop through
time, $0 CPU). Toy task = a deterministic symbol-sequence memory/prediction task (fixed
finite-state source) so that hidden-state structure is non-trivial but the system is exactly
big-Phi-computable at n<=5 after discretization. Identical architecture + identical task +
identical INIT (pinned per seed) across the two regimes — the ONLY difference is the update rule.

- DET regime: full-batch deterministic gradient descent (no update noise).
- NOISY regime: SGLD Langevin updates `w <- w - eta*grad + sqrt(2*eta*T)*xi`, xi ~ N(0,1) fresh
  per step. Update noise is in the LEARNING DYNAMICS, not the init (init is pinned identical to
  the DET run of the same seed) and not inference (markers measured noise-free post-training).

## CONTROL (critical — isolate noise from performance)

The two regimes are matched to EQUAL final task performance (cross-entropy within a pre-set
band eps) on the SAME toy data. Procedure: train DET to convergence; record DET final CE.
Train NOISY and select (via a pre-frozen anneal of T over training so the chain settles) the
checkpoint whose final CE is closest to the DET final CE; ACCEPT a seed-pair into the matched
analysis ONLY if |CE_noisy - CE_det| <= eps (eps stated below). Any marker difference at matched
CE is then attributable to the LEARNING NON-DETERMINISM, not to one model being better at the
task (p7 — perplexity/CE is NOT the truth, it is the CONTROL variable here).

- >=20 seeds per regime (paired by init).
- matched-CE band eps = 0.05 nats (absolute CE difference); seed-pairs outside the band are
  EXCLUDED from the marker test and reported (n_matched / n_total).

## Markers (measure several; a benefit on ANY pre-named one = the signal)

All Phi via the stdlib faithful IIT-4.0 engines (a_phi_iit4_tool, note
iit4-real-engine-in-stdlib-not-proxy): the H_1004 CPU mirrors of
hexa-lang/stdlib/consciousness/iit4_bigphi.hexa (system big-Phi) and
.../iit4/faithful_phi.hexa (MIP-EI scalar), RE-PROVEN == stdlib at n=4 AND n=5 BEFORE scoring
(H_1012 prove_mirrors_at_n discipline). NO variance-times-energy proxy anywhere.

Pre-named markers (each with an a-priori threshold):
1. **faithful_phi** of the hidden-state macro-system (n<=5 EXACT, discretized H_1004 path).
2. **big-Phi** (IIT-4.0 system Phi_s) of the same hidden-state macro-system (n<=5 EXACT).
3. **split_magnitude** = the H_1004/H_1037 planning-split phenomenon proxy here measured as the
   gap (faithful_phi - big-Phi) on the trained hidden state — the "faithful-up / big-down"
   structure magnitude.
4. **redundancy_margin** — Williams-Beer PID redundancy (H_1017/H_1020): redundant MI between
   two source hidden-units about a target, measured on the trained hidden-state traces.
5. **soc_proximity** — edge-of-chaos / self-organized-criticality proximity (H_931 criticality
   measure): proximity of the trained recurrent Jacobian spectral radius to 1.0 (|rho - 1|,
   smaller = closer to criticality), measured at the trained weights.
6. **emergence_probe** — a capability/structure appearing ONLY in the noisy-trained model: a
   held-out generalization gap (test-CE on unseen continuations) at matched train-CE — if the
   noisy model generalizes strictly better at matched train-CE, that is an emergence signal.

## PRE-REGISTERED FALSIFIER (frozen BEFORE measuring; TEXT tokens only)

For each marker, the per-seed paired statistic is (noisy_value - det_value) over the n_matched
init-paired seeds (matched-CE band). Pre-set effect-size threshold = **Cohen d >= 0.8** (large)
for a marker to count as a benefit, AND the direction must be the consciousness-favorable one:

- faithful_phi: benefit iff noisy > det with paired Cohen d >= +0.8.
- big_Phi: benefit iff noisy > det with paired Cohen d >= +0.8.
- split_magnitude: benefit iff |faithful - big| larger under noisy with paired Cohen d >= +0.8.
- redundancy_margin: benefit iff noisy > det with paired Cohen d >= +0.8.
- soc_proximity: benefit iff |rho-1| SMALLER under noisy (closer to criticality) with paired
  Cohen d >= +0.8 on (det_|rho-1| - noisy_|rho-1|).
- emergence_probe: benefit iff noisy test-generalization strictly better at matched train-CE
  with paired Cohen d >= +0.8 on (det_testCE - noisy_testCE).

- **H1 PASS** = at matched task-performance (|CE_noisy - CE_det| <= 0.05 over the n_matched
  paired seeds), AT LEAST ONE pre-named marker is strictly HIGHER (in its consciousness-favorable
  direction) under non-deterministic learning with paired Cohen d >= 0.8 -> non-deterministic
  LEARNING confers a consciousness/emergence advantage that the init/entropy non-determinism
  (H_921, entropy-null) did NOT.
- **H1 FAIL** = no marker benefits at matched performance (all within the control band, or
  noisy-learning is neutral/harmful: every marker's paired d < 0.8 in the favorable direction)
  -> learning non-determinism is ALSO not a consciousness advantage, consistent with H_921 (init)
  and the entropy-null (publishable closed-negative, a_paper_negative_ok).

DEGENERATE guard: if fewer than 10 seed-pairs fall within the matched-CE band (the regimes
cannot be matched on performance), the result is INCONCLUSIVE/DEGENERATE (neither PASS nor FAIL)
and reported as such (the control failed, not the hypothesis).

## HONEST scope (a_scale_honest_scope, a_toy_scale_recheck)

TOY n<=5 SW substrate. Both Phi engines EXACT at n<=5; the CPU mirrors RE-PROVEN == stdlib at
n=4 AND n=5 before scoring (live hexa refs, H_1012 discipline). g5 CODE-measured (no LLM
self-judge, p7). Production scale UNVERIFIED. NOT a forge binary; $0 CPU-local.

## Follow-up (NOT run here)

- AKIDA Lane A on-chip: AKD1000 native stochastic plasticity (non-deterministic learning ON
  silicon) is a separate substrate-tagged rung; do NOT conflate it with this SW verdict
  (pi5-akida single-exclusive; a_lane_akida_gpu_split).
- GPU Lane G: a forge/cuBLAS scale-up of the same probe is a separate substrate-tagged rung;
  do NOT conflate it with this SW verdict.
