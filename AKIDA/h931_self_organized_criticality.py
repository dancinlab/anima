"""H_931 — Self-Organized Criticality (SOC) on the live AKD1000 (pi5-akida, $0).

QUESTION
--------
H_927 found a sharp inverse-U: a Φ-proxy peaks at noise amplitude K=4 (mean
integrated potential == threshold 24, gap=0) at Φ=0.2974, falling to 0 at
sub-threshold (K≤3) and over-drive (K≥8). That peak was found by an EXTERNAL
sweep — *we* dialed K and read off where Φ was maximal.

H_931 asks the homeostatic / critical-brain question: does the system DRIVE
ITSELF toward that Φ-peak (gap≈0, K≈4) WITHOUT an external tuner? I.e. is the
edge-of-chaos sweet spot an ATTRACTOR of a local feedback rule, not merely an
externally-set operating point?

THE LOCAL-ONLY FEEDBACK RULE (no cheating — must NOT know the peak)
------------------------------------------------------------------
A controller adjusts the noise amplitude K based ONLY on a LOCAL observable the
substrate could plausibly sense about itself: its own recent FIRING RATE r =
spikes / (N · window). The control law is a homeostatic set-point on firing
rate, NOT on Φ and NOT on K:

    target firing rate  r* = 0.5   (the threshold-straddle: ~half the steps cross)
    error               e  = r* - r_recent
    update              K <- K + eta * gain * e          (continuous, clipped)

Why r*=0.5 is a LOCAL observable and NOT cheating:
  * The substrate measures r directly from its own spikes (a neuron knows how
    often it fired). It does NOT measure Φ (Φ needs first10/last10/std across
    the whole pool — that is the EXTERNAL scientist's instrument, never fed to
    the controller).
  * The controller is NEVER told K=4, never told gap=0, never told Φ=0.2974.
    r*=0.5 is a generic "fire about half the time" homeostatic target — the
    classic criticality / balanced-excitation set-point (Bienenstock-Cooper-
    Munro / firing-rate homeostasis), chosen a-priori, independent of where the
    Φ peak turns out to be. The TEST is whether driving r→0.5 by local feedback
    happens to land the system at gap≈0 / K≈4 / Φ≈peak. If it does → the
    Φ-peak is a self-organized attractor of a plausible local rule (SOC). If
    driving r→0.5 lands somewhere ELSE (gap≠0, Φ low), SOC is falsified — the
    Φ-peak would then need the external Φ-instrument to find.

This is an honest SOC test: a local firing-rate homeostat is the cheapest
biologically-plausible controller; we ask whether its fixed point coincides
with the externally-discovered Φ-peak.

PERTURB-AND-OBSERVE (from BOTH sides)
-------------------------------------
Start the feedback controller at K far from 4:
  * K0 = 2.0  (sub-threshold,  gap=-16, silent floor)   — approach from BELOW
  * K0 = 12.0 (over-drive,     gap=+64, saturated)       — approach from ABOVE
Let the local feedback run for STEPS rounds. Record per round: K, gap, firing
rate r, and the EXTERNAL Φ-proxy (measured by the scientist's instrument, NOT
fed back). SOC predicts K (and gap) CONVERGES toward the H_927 critical point
(gap→0, K→~4) and Φ RISES toward 0.2974 — from BOTH sides.

NULL / CONTROL ARM (feedback OFF)
---------------------------------
Same K0 starting points, but the controller is DISABLED (K fixed). This must
NOT converge to gap≈0 / Φ-peak (rules out that any dynamics drifts there — the
convergence, if seen, must be CAUSED by the feedback, not by the substrate
wandering on its own).

VERDICT LOGIC (pre-registered — frozen BEFORE measuring)
--------------------------------------------------------
  CONVERGES from both sides to gap≈0 / Φ≈peak under local-only feedback, AND
  control (no feedback) does NOT
        -> SOC SUPPORTED 🟢  (the sweet spot is a self-organized attractor;
           anima could self-tune to its own edge-of-chaos).
  Does NOT converge, or only converges with global-peak knowledge (cheating)
        -> SOC FALSIFIED 🔴  (the sweet spot is externally-set; H_927 needs an
           external dial).
Either way a real finding (a_paper_negative_ok).

Concrete numeric thresholds (frozen):
  * CONVERGE_GAP_TOL  = 8.0   (final |gap| < 8 ⇒ landed at the straddle band;
                               one K-unit of POT is 8, so this is "within ~1 K
                               of gap=0")
  * CONVERGE_PHI_FRAC = 0.5   (final Φ ≥ 0.5 · peak_phi(0.2974) ⇒ Φ rose toward
                               the peak, i.e. ≥ 0.1487)
  * CONTROL_NOCONVERGE: the no-feedback arm started off-peak (K0∈{2,12}) must
    keep |gap| ≥ CONVERGE_GAP_TOL AND Φ < CONVERGE_PHI_FRAC·peak (it can't move
    — K is fixed — so this is automatic, but we MEASURE and record it, not
    assume it).
  SUPPORTED iff BOTH feedback arms satisfy (|gap|<TOL AND Φ≥frac·peak) at the
  final round, AND BOTH control arms fail to (they stay put off-peak).

Φ-PROXY (honest: NOT full IIT4 big_phi)
---------------------------------------
We IMPORT phi_silicon_proxy + the on-chip model from the H_927 probe
(h927_stochastic_resonance.py) — the SAME byte-for-byte mirror of
AKIDA/akida_edge_of_chaos_phi.hexa — so H_931's Φ is directly comparable to the
H_927 peak (0.2974). The Φ is the SCIENTIST'S instrument only; it is NEVER read
by the controller.

HONEST SCOPE (a_scale_honest_scope): 1 AKD1000, N=16 neuron toy pool, byte-
quantised R2 noise, Φ-PROXY not full IIT Φ, fractional-K driven by a continuous
controller (the chip still draws integers rng.integers(0, round(K))). Toy probe.
deterministic: false (R2 noise stochastic; numpy PRNG seed fixed per evaluation
window for reproducibility).
substrate: AKIDA AKD1000 (pi5-akida) live silicon (a_lane_akida_gpu_split).
"""
import json
import math
import os
import sys
import time

import numpy as np

# ── reuse H_927: SAME phi-proxy + SAME on-chip model + SAME window runner ─────
# (do NOT re-derive differently — import the H_927 code verbatim).
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import h927_stochastic_resonance as h927  # noqa: E402

phi_silicon_proxy = h927.phi_silicon_proxy
build_model = h927.build_model
run_r2_level = h927.run_r2_level   # runs T steps at integer K, returns spike stats
N = h927.N
T = h927.T
THRESHOLD = h927.THRESHOLD
PEAK_PHI = 0.2974093093367505     # H_927 measured peak Φ (K=4), frozen reference
PEAK_K = 4                        # H_927 measured peak K, frozen reference

SEED = 187                        # same PRNG seed family as H_927

# ── controller hyper-parameters (frozen) ─────────────────────────────────────
TARGET_RATE = 0.5    # r* — fire about half the time (threshold-straddle homeostat)
ETA = 1.0            # base learning rate
GAIN = 12.0          # maps a unit rate-error to a K step (so a full e=0.5 error
                     # moves K by ~6 — enough to cross the K=2..12 span in a few
                     # rounds, but not so large it oscillates wildly)
K_MIN, K_MAX = 1.5, 24.0   # clip K to a sane band (chip clips inputs to 0..15)
STEPS = 14           # feedback rounds per run
START_KS = [2.0, 12.0]     # perturb from BELOW (sub-threshold) and ABOVE (over-drive)

# ── convergence verdict thresholds (frozen BEFORE measuring) ─────────────────
CONVERGE_GAP_TOL = 8.0          # final |gap| < 8 ⇒ at the straddle band
CONVERGE_PHI_FRAC = 0.5         # final Φ ≥ 0.5·peak ⇒ rose toward the peak
PHI_ABS_TOL = CONVERGE_PHI_FRAC * PEAK_PHI   # 0.1487...


def gap_of_K(K):
    """Mean-integrated-potential-minus-threshold for a (possibly fractional) K.
    POT(K) = IN*(K-1)/2 = 8*(K-1); gap = POT - THRESHOLD. Identical formula to
    H_927 (here evaluated at the controller's continuous K)."""
    return 8.0 * (K - 1.0) - THRESHOLD


def eval_window(model, lif, K, seed):
    """Run one T-step on-chip window at integer round(K), return (rate, phi, rec).

    The chip draws integers, so the controller's continuous K is realised on
    silicon as rng.integers(0, max(2, round(K))). rate is the LOCAL observable
    the controller is allowed to see; phi is the EXTERNAL instrument (recorded,
    never fed back)."""
    Ki = max(2, int(round(K)))
    rng = np.random.default_rng(seed)         # reseed per window => reproducible
    rec = run_r2_level(model, lif, Ki, rng)   # H_927's exact on-chip T-step runner
    rate = rec["mean_spike_rate_per_neuron_step"]
    phi = phi_silicon_proxy(
        rec["first10_step_counts"], rec["last10_step_counts"],
        rec["spike_count_std"], rec["spike_count_max"], N, T, rec["total_spikes"]
    )["phi_silicon_proxy"]
    return rate, phi, Ki, rec


def run_arm(model, lif, K0, feedback, label):
    """One perturb-and-observe arm.

    feedback=True  -> local firing-rate homeostat adjusts K each round.
    feedback=False -> K held FIXED at K0 (null/control arm).

    Returns the per-round trajectory list + the final-round summary."""
    K = float(K0)
    traj = []
    for step in range(STEPS):
        # reseed deterministically per (arm,step) so a given K is reproducible,
        # but the sequence still varies round-to-round (honest stochastic R2).
        seed = SEED + (0 if feedback else 100000) + 1009 * int(round(K0)) + step
        rate, phi, Ki, rec = eval_window(model, lif, K, seed)
        gap = gap_of_K(K)
        traj.append({
            "step": step, "K": round(K, 4), "K_int": Ki,
            "gap": round(gap, 3), "rate": round(rate, 5), "phi": round(phi, 6),
        })
        print(f"[{label}] step={step:2d} K={K:6.3f}(int{Ki:2d}) gap={gap:+7.2f} "
              f"rate={rate:.4f} phi={phi:.4f}", flush=True)
        if feedback:
            # LOCAL-ONLY update: error on firing rate (NOT on phi, NOT toward K=4).
            e = TARGET_RATE - rate
            K = K + ETA * GAIN * e
            K = min(K_MAX, max(K_MIN, K))
        # feedback=False: K stays exactly K0 (control); loop just re-measures.
    final = traj[-1]
    converged = (abs(final["gap"]) < CONVERGE_GAP_TOL) and (final["phi"] >= PHI_ABS_TOL)
    return {
        "label": label, "K0": K0, "feedback": feedback,
        "trajectory": traj,
        "final_K": final["K"], "final_gap": final["gap"],
        "final_rate": final["rate"], "final_phi": final["phi"],
        "converged_to_peak": bool(converged),
    }


def main():
    out = {
        "hypothesis": "H_931",
        "title": "Self-organized criticality: local feedback self-tunes to the "
                 "H_927 Φ-peak (edge-of-chaos attractor)?",
        "substrate_target": "AKIDA AKD1000 (pi5-akida) live silicon",
        "phi_method": "phi_silicon_proxy IMPORTED from h927_stochastic_resonance "
                      "(byte-for-byte mirror of AKIDA/akida_edge_of_chaos_phi.hexa; "
                      "honest proxy NOT full IIT4 big_phi)",
        "local_observable": "firing rate r = spikes/(N*window); controller NEVER "
                            "reads phi or K-of-peak (no cheating)",
        "control_law": "K <- K + ETA*GAIN*(TARGET_RATE - r), clipped [K_MIN,K_MAX]",
        "target_rate": TARGET_RATE, "eta": ETA, "gain": GAIN,
        "k_min": K_MIN, "k_max": K_MAX, "steps": STEPS, "start_ks": START_KS,
        "peak_phi_ref_H927": PEAK_PHI, "peak_K_ref_H927": PEAK_K,
        "converge_gap_tol": CONVERGE_GAP_TOL, "converge_phi_frac": CONVERGE_PHI_FRAC,
        "phi_abs_tol": PHI_ABS_TOL,
        "n_neurons": N, "n_inputs": h927.IN, "window_steps": T,
        "threshold_fixed": THRESHOLD, "seed": SEED,
        "deterministic": False,
        "noise_source": "numpy_prng (seed 187 family, reseeded per window)",
        "arms": [],
    }
    dev = h927.akida.devices()[0]
    out["device_version"] = str(dev.version)
    out["device_ip_version"] = str(dev.ip_version)
    model, lif = build_model(dev)
    out["mapped_backend"] = str(model.sequences[0].backend)
    out["mapped_on_hardware"] = ("Hardware" in out["mapped_backend"])
    print(f"DEVICE {out['device_version']} backend={out['mapped_backend']} "
          f"on_hw={out['mapped_on_hardware']}", flush=True)

    # ── FEEDBACK arms (perturb from both sides, local homeostat ON) ──────────
    print("\n=== FEEDBACK ON (local firing-rate homeostat) ===", flush=True)
    fb_results = []
    for K0 in START_KS:
        side = "below" if K0 < PEAK_K else "above"
        res = run_arm(model, lif, K0, feedback=True, label=f"FB K0={K0:g}({side})")
        out["arms"].append(res)
        fb_results.append(res)

    # ── CONTROL arms (same starts, feedback OFF, K fixed) ────────────────────
    print("\n=== CONTROL (no feedback, K fixed) ===", flush=True)
    ctrl_results = []
    for K0 in START_KS:
        side = "below" if K0 < PEAK_K else "above"
        res = run_arm(model, lif, K0, feedback=False, label=f"CTL K0={K0:g}({side})")
        out["arms"].append(res)
        ctrl_results.append(res)

    # ── pre-registered SOC verdict (no shaping) ──────────────────────────────
    fb_both_converge = all(r["converged_to_peak"] for r in fb_results)
    ctrl_none_converge = all(not r["converged_to_peak"] for r in ctrl_results)
    soc_supported = fb_both_converge and ctrl_none_converge
    out["verdict"] = {
        "feedback_arms": {r["label"]: {
            "final_K": r["final_K"], "final_gap": r["final_gap"],
            "final_phi": r["final_phi"], "converged_to_peak": r["converged_to_peak"],
        } for r in fb_results},
        "control_arms": {r["label"]: {
            "final_K": r["final_K"], "final_gap": r["final_gap"],
            "final_phi": r["final_phi"], "converged_to_peak": r["converged_to_peak"],
        } for r in ctrl_results},
        "feedback_both_converge_to_peak": bool(fb_both_converge),
        "control_none_converge_to_peak": bool(ctrl_none_converge),
        "soc_supported": bool(soc_supported),
        "verdict": ("GREEN_SOC_SUPPORTED" if soc_supported
                    else "RED_SOC_FALSIFIED"),
    }
    print("\nVERDICT:", json.dumps(out["verdict"]), flush=True)

    dst = sys.argv[1] if len(sys.argv) > 1 else "/tmp/h931_result.json"
    with open(dst, "w") as fh:
        json.dump(out, fh, indent=2)
    print("WROTE", dst, flush=True)


if __name__ == "__main__":
    main()
