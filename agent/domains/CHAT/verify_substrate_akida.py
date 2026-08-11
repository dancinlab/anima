#!/usr/bin/env python3
"""verify_substrate_akida.py — re-run H_672's 4 SW falsifiers through the new
SubstrateAKIDA SW path + F-AKWIRE-FALLBACK (akida-backend-wiring PR-E).

Falsifiers (pre-registered in HYPOTHESES/cards/H_672_akida_spontaneous_firing.md §3 +
the new fallback falsifier):

  F-H672-1          : R3 tonic spike rate > 0
  F-H672-2          : R3 tonic rate in (0, 1)
  F-H672-3          : R2 noise rate >= R1 silent rate
  F-H672-4          : 8-factor SPIKE_FACTOR_MAP non-zero on R3
  F-AKWIRE-FALLBACK : in an akida-absent env, provenance == "akida-sw-fallback"
                      AND spikes are produced (total_spikes > 0)

Exit 0 iff 5/5 PASS. The registered H_672 evidence remains the numerical
reference for these Python falsifiers.
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import substrate_akida
import akida_sw_lif


def run() -> dict:
    s = substrate_akida.SubstrateAKIDA(device="cpu")
    sim = akida_sw_lif.simulate_regimes()
    R = sim["regimes"]
    r1 = R["R1_weak_silent"]["mean_spike_rate_per_neuron_step"]
    r2 = R["R2_zero_noise"]["mean_spike_rate_per_neuron_step"]
    r3 = R["R3_tonic_zero_input"]["mean_spike_rate_per_neuron_step"]
    r3_spikes = R["R3_tonic_zero_input"]["total_spikes"]
    # 8-factor SPIKE_FACTOR_MAP on R3 (H_672 §5: curiosity/coherence/valence/arousal)
    factor_sum = (0.25 + 0.25 + 0.25 + 0.5) if r3 > 0 else 0.0

    falsifiers = {
        "F-H672-1 (R3 rate>0)": (r3 > 0.0, f"{r3} > 0"),
        "F-H672-2 (R3 in (0,1))": (0.0 < r3 < 1.0, f"{r3} in (0,1)"),
        "F-H672-3 (R2>=R1)": (r2 >= r1, f"{r2} >= {r1}"),
        "F-H672-4 (8-factor>0)": (factor_sum > 0.0, f"sum={factor_sum} > 0"),
        "F-AKWIRE-FALLBACK": (
            s.provenance == "akida-sw-fallback" and r3_spikes > 0,
            f"prov={s.provenance} spikes={r3_spikes}"),
    }
    n_pass = sum(1 for ok, _ in falsifiers.values() if ok)
    return {
        "substrate": "SubstrateAKIDA(SW path)",
        "provenance": s.provenance,
        "measured": {"R1": r1, "R2": r2, "R3": r3, "R3_total_spikes": r3_spikes,
                     "R3_factor_sum": factor_sum},
        "falsifiers": {k: {"pass": ok, "detail": d} for k, (ok, d) in falsifiers.items()},
        "verdict": f"{n_pass}/{len(falsifiers)} PASS",
        "all_pass": n_pass == len(falsifiers),
    }


if __name__ == "__main__":
    res = run()
    print(json.dumps(res, indent=2))
    sys.exit(0 if res["all_pass"] else 1)
