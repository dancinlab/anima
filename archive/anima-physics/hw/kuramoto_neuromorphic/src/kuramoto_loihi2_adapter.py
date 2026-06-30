#!/usr/bin/env python3
"""kuramoto_loihi2_adapter.py — Intel Loihi 2 (NxSDK) skeleton adapter.

CLOUD-ONLY on Mac: Intel NxSDK is Linux-only with gated educational access
via Intel Neuromorphic Research Cloud (NRC).  This file is a *syntactic*
skeleton intended to (a) py_compile cleanly on Mac without NxSDK installed,
(b) demonstrate the intended NxSDK API call shape for the Kuramoto
all-to-all coupling network, and (c) serve as the dispatch-target for the
Phase 1b cloud cycle.

SW source: anima-physics/social/kuramoto_coupling.hexa (§188 PASS 6/6)
Local sim: anima-physics/hw/kuramoto_neuromorphic/src/kuramoto_local_sim.py

Mapping (mirror of DESIGN.md §4):
    Oscillator i (intrinsic freq ω_i)  →  nx.Compartment(bias=ω_i)
    Phase θ_i ∈ [0, 2π)                →  compartment voltage
                                            (wrap on spike)
    Spike emit when θ_i ≥ 2π            →  threshold-crossing spike
    Coupling I_i = (K/N)·Σ sin(θ_j-θ_i)→  dendritic accumulator over
                                            all-to-all weight matrix w_ij = K/N
    Order parameter r                   →  host-side post-process from
                                            graded-spike payload (Loihi 2's
                                            8-bit graded spikes carry θ_i)

Phase 1b usage (on Intel NRC cloud VM):
    pip install nxsdk
    python3 kuramoto_loihi2_adapter.py --submit --n 8 --k 2.0 --steps 1000
"""

from __future__ import annotations

import argparse
import sys

# ─── NxSDK gated import (Mac local: ImportError expected) ───────────────
NXSDK_AVAILABLE = False
try:
    # The real cloud-side import — Mac local must NOT have this.
    import nxsdk.api.n2a as nx  # type: ignore  # noqa: F401
    from nxsdk.graph.processes.phase_enums import Phase  # type: ignore  # noqa: F401
    NXSDK_AVAILABLE = True
except ImportError:
    # Expected on Mac local.  Adapter remains importable for syntax check.
    nx = None  # type: ignore[assignment]


def build_kuramoto_network(n: int, k: float, steps: int):
    """Construct a Loihi 2 Kuramoto network — NxSDK API skeleton.

    Cloud-side behavior (when NXSDK_AVAILABLE):
        1. Create nx.NxNet()
        2. For each oscillator i: nx.Compartment with bias=ω_i and
           threshold=2π (spike when phase wraps).
        3. Create all-to-all ConnectionGroup with weight matrix w_ij = K/N
           (zero diagonal).
        4. Configure graded-spike output probes per compartment to recover
           phase θ_i(t) at each step.
        5. Return the network handle for `.run(num_steps=steps)`.

    Mac local: raises NotImplementedError immediately — by design.
    """
    if not NXSDK_AVAILABLE:
        raise NotImplementedError(
            "NxSDK not installed (Mac local).  This adapter is a syntactic "
            "skeleton; submit from Intel NRC cloud VM."
        )

    # ─── cloud-side skeleton (commented for syntactic clarity) ──────────
    # net = nx.NxNet()
    # cx_proto = nx.CompartmentPrototype(
    #     vThMant=int(2 * 3.14159 * 1000),   # threshold = 2π · scale
    #     biasMant=0,                          # set per-i below
    #     biasExp=6,
    #     functionalState=2,                   # IDLE → activate on run
    # )
    # compartments = []
    # import numpy as _np
    # rng = _np.random.default_rng(42)
    # omegas = 1.0 + 1.5 * rng.standard_normal(n)
    # for i in range(n):
    #     cx = net.createCompartment(prototype=cx_proto)
    #     cx.biasMant = int(omegas[i] * 1000)
    #     compartments.append(cx)
    #
    # # All-to-all weight matrix (zero diagonal)
    # weight = int((k / n) * 256)             # Loihi 2 weight is 8-bit
    # conn_proto = nx.ConnectionPrototype(weight=weight)
    # for i in range(n):
    #     for j in range(n):
    #         if i == j:
    #             continue
    #         net.createConnection(
    #             srcGrp=compartments[j],
    #             dstGrp=compartments[i],
    #             prototype=conn_proto,
    #         )
    #
    # # Graded-spike probes — payload carries θ_i(t)
    # phase_probes = [cx.probe(nx.ProbeParameter.SPIKE) for cx in compartments]
    # return net, phase_probes
    raise NotImplementedError("cloud-side body — see commented skeleton")


def submit_run(n: int, k: float, steps: int) -> dict:
    """Compile and submit the Kuramoto network to Loihi 2 (NRC cloud)."""
    net, probes = build_kuramoto_network(n, k, steps)
    # net.run(numSteps=steps)
    # net.disconnect()
    # spike_train = [p.data for p in probes]
    # r_hist = _reconstruct_order_parameter(spike_train, n, steps)
    # return {"r_tail": float(r_hist[-int(steps * 0.1):].mean()),
    #         "spike_count": int(sum(len(p.data) for p in probes))}
    raise NotImplementedError("cloud-side submit — Phase 1b dispatch only")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Loihi 2 NxSDK Kuramoto adapter (cloud-only)"
    )
    parser.add_argument("--n", type=int, default=8, help="oscillator count")
    parser.add_argument("--k", type=float, default=2.0, help="coupling strength")
    parser.add_argument("--steps", type=int, default=1000, help="sim steps")
    parser.add_argument("--submit", action="store_true",
                        help="submit to Loihi 2 (requires NxSDK + NRC access)")
    args = parser.parse_args()

    print(f"[kuramoto_loihi2_adapter] NXSDK_AVAILABLE={NXSDK_AVAILABLE}")
    print(f"  N={args.n}, K={args.k}, steps={args.steps}")
    if args.submit:
        if not NXSDK_AVAILABLE:
            print("  ERROR: --submit requires nxsdk; install on Intel NRC cloud VM")
            return 2
        result = submit_run(args.n, args.k, args.steps)
        print(f"  result: {result}")
    else:
        print("  (syntax-check mode — pass --submit to fire on cloud)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
