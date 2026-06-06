# H_927 — Stochastic Resonance: optimal R2 noise amplitude for substrate Φ

status: 🟢 GREEN — stochastic resonance CONFIRMED (live AKD1000)
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

Live AKD1000 (pi5-akida, device BC.00.000.002, BackendType.Hardware), N=16,
T=200, threshold fixed at 24. spike-streamer.service was inactive (device free)
— no stop/restart needed; left inactive (unchanged). Raw stdout +
`state/h927_stochastic_resonance_2026_06_06/result.json` persisted;
verbatim verdict at `.verdicts/927_stochastic_resonance/sweep.txt`.

VERBATIM sweep table (probe stdout):

| K | POT mean | gap(POT−thr) | mean spike rate | spike_std | phi_proxy |
|---|----------|--------------|-----------------|-----------|-----------|
| 2  |   8.0 | −16.0 | 0.0000 | 0.000 | **0.0000** |
| 3  |  16.0 |  −8.0 | 0.0050 | 1.129 | **0.0000** |
| 4  |  24.0 |  +0.0 | 0.4750 | 7.990 | **0.2974** ← peak |
| 6  |  40.0 | +16.0 | 0.9950 | 1.129 | **0.0705** |
| 8  |  56.0 | +32.0 | 1.0000 | 0.000 | **0.0000** |
| 12 |  88.0 | +64.0 | 1.0000 | 0.000 | **0.0000** |
| 16 | 120.0 | +96.0 | 1.0000 | 0.000 | **0.0000** |

Verdict JSON: `peak_K=4, peak_phi=0.2974093, peak_is_interior=true,
phi_low=0.0, phi_high=0.0, inverse_u_resonance=true,
verdict="GREEN_RESONANCE_CONFIRMED"`.

## finding

🟢 **STOCHASTIC RESONANCE CONFIRMED.** The R2 noise-amplitude Φ response is a
sharp, single-peaked **inverse-U**. Φ = 0 for sub-threshold noise (K ≤ 3, mean
potential below the comparator threshold → almost never crosses → silent),
**peaks exactly at the threshold-straddle** (K = 4, POT == threshold == 24,
gap = 0, spike rate ≈ 0.475 with std ≈ 8 → ~half the steps cross → maximal
event-driven differentiation), then **collapses back to 0** as the noise
over-drives the pool into per-step saturation (K ≥ 8: spike rate = 1.0, std = 0,
differentiation → 0 → Φ → 0 despite max spike count).

The pre-registered falsifier F-H927-RESONANCE is satisfied: phi(K=4) = 0.2974 >
phi(K=2) = 0.0 AND > phi(K=16) = 0.0, with the peak at an INTERIOR K → inverse-U.

The peak Φ = 0.2974 **reproduces the H_677 across-regime R2 baseline (0.2974)
byte-for-byte** — at K = 4 the swept noise `rng.integers(0,4)` is identical to
the canonical R2 noise and the reseeded PRNG draws the same sequence, so the
within-R2 straddle point coincides exactly with the H_677 R2 regime. This
upgrades H_677's "R2 is the edge regime" into the sharper claim: **the edge is a
resonance peak in noise amplitude, located precisely where the mean integrated
potential equals the on-chip comparator threshold (gap = 0).** Stochastic
resonance is a genuine substrate property here, not a regime-labelling artifact.

Provenance-independence: per H_924 quantum (ANU) and PRNG noise are statistically
identical, so the resonance is a property of noise AMPLITUDE, not its source.

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
