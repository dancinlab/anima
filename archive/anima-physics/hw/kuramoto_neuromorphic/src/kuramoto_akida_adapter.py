#!/usr/bin/env python3
"""kuramoto_akida_adapter.py — BrainChip Akida (MetaTF) skeleton adapter.

CLOUD-ONLY on Mac: BrainChip's MetaTF Python package is pip-installable
but the actual Akida NSoC is reachable only via (a) USB stick attachment
or (b) AKD1500/AKD1000 cloud appliance.  Inference on the host CPU/GPU is
available but does not exercise event-driven spiking — for that, real
hardware (or BrainChip-hosted cloud) is required.

This file is a *syntactic* skeleton:
    (a) py_compile cleanly on Mac without `akida` installed,
    (b) demonstrate the intended MetaTF API call shape, and
    (c) serve as Phase 1b dispatch target.

SW source: anima-physics/social/kuramoto_coupling.hexa (§188 PASS 6/6)
Local sim: anima-physics/hw/kuramoto_neuromorphic/src/kuramoto_local_sim.py

Mapping (mirror of DESIGN.md §4):
    Oscillator i → akida.InputLayer neuron with bias=ω_i
    Phase θ_i    → spike-rate-coded (1 spike per phase wrap)
    Coupling     → akida.FullyConnected layer with weights w_ij = K/N
    Order param r→ host-side post-process from spike-rate histogram

Phase 1b usage (with akida installed):
    pip install akida
    python3 kuramoto_akida_adapter.py --submit --n 8 --k 2.0 --steps 1000
"""

from __future__ import annotations

import argparse
import sys

# ─── MetaTF gated import (Mac local: ImportError expected) ──────────────
AKIDA_AVAILABLE = False
try:
    import akida  # type: ignore  # noqa: F401
    AKIDA_AVAILABLE = True
except ImportError:
    akida = None  # type: ignore[assignment]


def build_kuramoto_model(n: int, k: float):
    """Construct an Akida MetaTF Kuramoto model — skeleton.

    Cloud-side behavior (when AKIDA_AVAILABLE):
        1. akida.Model() container.
        2. InputLayer(input_shape=(1, 1, n)) for the N oscillators.
        3. FullyConnected(units=n, weights=(K/N)·(ones-diag)) for the
           all-to-all coupling.
        4. Threshold + spike emission via Akida's built-in activation.

    Mac local: raises NotImplementedError — by design.
    """
    if not AKIDA_AVAILABLE:
        raise NotImplementedError(
            "akida not installed (Mac local).  Skeleton only; submit from "
            "BrainChip cloud or with Akida USB stick attached."
        )

    # ─── cloud-side skeleton (commented for clarity) ────────────────────
    # import numpy as _np
    # model = akida.Model()
    # model.add(akida.InputData(name="phase_in", input_shape=(1, 1, n),
    #                           input_bits=8))
    # # All-to-all coupling weight matrix (zero diagonal, value K/N)
    # weights = ((k / n) * (_np.ones((n, n)) - _np.eye(n))).astype(_np.int8)
    # fc = akida.FullyConnected(name="coupling", units=n,
    #                           weights_bits=4,
    #                           activation=True,
    #                           threshold=1.0)
    # fc.set_variable("weights", weights)
    # model.add(fc)
    # return model
    raise NotImplementedError("cloud-side body — see commented skeleton")


def submit_run(n: int, k: float, steps: int) -> dict:
    """Run the Kuramoto model on Akida hardware (cloud/USB stick)."""
    model = build_kuramoto_model(n, k)
    # # devices = akida.devices(); model.map(devices[0])
    # # spike_train_per_step = []
    # # for t in range(steps):
    # #     out = model.forward(_initial_phase_encoding(n))
    # #     spike_train_per_step.append(out)
    # # r_hist = _reconstruct_order_parameter_from_rate(spike_train_per_step, n)
    # # return {"r_tail": float(r_hist[-int(steps * 0.1):].mean())}
    raise NotImplementedError("cloud-side submit — Phase 1b dispatch only")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Akida MetaTF Kuramoto adapter (cloud-only)"
    )
    parser.add_argument("--n", type=int, default=8, help="oscillator count")
    parser.add_argument("--k", type=float, default=2.0, help="coupling strength")
    parser.add_argument("--steps", type=int, default=1000, help="sim steps")
    parser.add_argument("--submit", action="store_true",
                        help="submit to Akida (requires akida + HW/cloud)")
    args = parser.parse_args()

    print(f"[kuramoto_akida_adapter] AKIDA_AVAILABLE={AKIDA_AVAILABLE}")
    print(f"  N={args.n}, K={args.k}, steps={args.steps}")
    if args.submit:
        if not AKIDA_AVAILABLE:
            print("  ERROR: --submit requires akida; install + attach HW/cloud")
            return 2
        result = submit_run(args.n, args.k, args.steps)
        print(f"  result: {result}")
    else:
        print("  (syntax-check mode — pass --submit to fire on cloud/HW)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
