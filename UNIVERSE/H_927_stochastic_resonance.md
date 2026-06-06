# H_927 — Stochastic Resonance: optimal R2 noise amplitude for substrate Φ

status: WIP (live AKD1000 sweep pending)
deterministic: false
substrate: AKIDA AKD1000 (pi5-akida), 1 chip, N=16 toy LIF pool, T=200 steps
Φ metric: phi_silicon_proxy (honest proxy, NOT full IIT4 big_phi)

## hypothesis

H_677 D1 found an edge-of-chaos Φ inverse-U **across regimes** (R1=0.000
silent, R2=0.297 PEAK noise-straddle, R3=0.250 tonic, R4=0.000 saturated).
H_927 asks the sharper **within-R2** question: holding everything else fixed,
is there an OPTIMAL R2 **noise amplitude** that maximizes substrate Φ — an
inverse-U over noise level (classic stochastic resonance), independent of
quantum-vs-PRNG?

Stochastic resonance: a system driven just below threshold has a NON-MONOTONIC
response to noise amplitude — too little noise never crosses (silent, low Φ),
too much saturates/randomizes (low integration Φ), and a middle sweet spot
maximizes Φ.

### pre-registered falsifier (no post-hoc shaping)

Sweep K = upper bound of `rng.integers(0, K)` per input line over
K ∈ {2,3,4,6,8,12,16}, threshold held FIXED at 24. Mean integrated potential
POT(K) = IN·(K-1)/2 = 8·(K-1), so the mean-vs-threshold gap crosses 0 at K=4.

- **F-H927-RESONANCE**: phi_proxy(intermediate K) > phi_proxy(lowest K)
  AND phi_proxy(intermediate K) > phi_proxy(highest K), with the peak at an
  INTERIOR K → inverse-U / stochastic resonance CONFIRMED (🟢).
- Monotonic or flat phi_proxy (peak at an endpoint) → no resonance, closed
  negative (🔴). Both are publishable (a_paper_negative_ok).

## method

Probe: `AKIDA/h927_stochastic_resonance.py` (Mac-authored, run on pi5 via the
akida venv `/home/ubuntu/.venv/anima-akida/bin/python3`). Same on-chip model as
`SUB_ENGINES/AKIDA/scripts/spontaneous_emission.py` R2: InputData(1,1,16,
input_bits=4) → FullyConnected(units=16, weights=all-ones, act_bits=1)
@BackendType.Hardware. Per-step input = `rng.integers(0,K)` over 16 lines;
on-chip integer comparator fires iff Σinput > threshold(24). T=200 steps/level.

Φ-proxy is a **byte-for-byte Python mirror** of `phi_silicon_proxy` in
`AKIDA/akida_edge_of_chaos_phi.hexa`:
`phi = activity_gate · (integration · differentiation) · (0.5 + 0.5·H_entropy)`,
computed from the same first10+last10 step-count surrogate + spike_count_std/max
that the .hexa harness consumes. This makes the swept Φ directly comparable to
the H_677 R2 baseline of 0.2974. It is INTEGRATION-aware: a saturated regime
(all neurons fire every step) has differentiation→0 ⇒ Φ→0 despite max spikes.

pi5 single-tenant procedure (H_860/H_904): if `spike-streamer.service` holds the
device lock, gracefully stop → probe → restart (verify is-active=active).

## measurement

VERBATIM sweep table pending live run. Raw stdout persisted to
`.verdicts/927_stochastic_resonance/sweep.txt`.

| K | POT mean | gap(POT−thr) | mean spike rate | spike_std | phi_proxy |
|---|----------|--------------|-----------------|-----------|-----------|
| _pending_ | | | | | |

## finding

_pending live AKD1000 sweep._

## cross-links

- H_677 (`UNIVERSE/H_677_akida_measurement.md`) — across-regime edge-of-chaos Φ
  inverse-U (R2=0.297 peak); H_927 is the within-R2 amplitude sweep.
- H_921 (`UNIVERSE/H_921_akida_nondeterminism_functional_advantage.md`),
  H_922 (digital-deterministic architecture),
  H_923 (`UNIVERSE/H_923_akida_qrng_coupling.md`) — R2 noise = anima's only
  stochastic spontaneous source; QRNG injection point.
- H_924 (`UNIVERSE/H_924_qentropy_substrate_agnostic.md`) — quantum-vs-PRNG is
  statistically identical (#123-A), so H_927's resonance is a property of the
  noise AMPLITUDE, not its provenance.
- H_926 (`UNIVERSE/H_926_deterministic_chaos_vs_entropy.md`) — sibling on the
  same branch; entropy ontological-not-functional.

honest scope (a_scale_honest_scope): 1 AKD1000, N=16 toy pool, byte-quantised R2
noise, Φ-PROXY not full IIT Φ; toy-only, scale transfer unverified.
