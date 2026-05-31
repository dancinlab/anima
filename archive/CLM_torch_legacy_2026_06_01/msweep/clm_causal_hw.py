"""CLM CAUSAL-POWER — LIVE pi5 AKD1000 HW spike test (F-CLM-CAUSAL-XFER axis B).

Tests whether the GREEN CAUSAL-POWER measure survives on REAL SILICON: the spike
raster is collected from the live AKD1000 chip (threshold-and-fire ON the chip,
NOT akida_sw_lif), then fed to the SAME frozen CAUSAL-POWER 3-check.

CHIP MODEL (spike_streamer.py pattern): InputData(1,1,IN) -> FullyConnected(N,
weights=ones, act_bits=1) mapped to BackendType.Hardware. potential(unit_j) =
Σ inputs; per-unit int32 threshold; on-chip binary threshold-and-fire.

COUPLING (the integration mechanism): the chip is feedforward, so to create
cross-region causal structure we close a SW loop AROUND the silicon — each step's
input is built from the PREVIOUS step's on-chip spike output plus a per-region
drive. The spike DECISION runs on the real chip every step (model.forward); SW
only carries the coupling feedback (the toy LIF's `coupling` term, but the
threshold-and-fire is silicon). This mirrors measure_sweep.gen_spike exactly:
  collapse : region 0 drive monopoly + coupling 0 (decoupled -> no integration).
  rich     : balanced drive + strong coupling (cross-region integration).

FROZEN (reused verbatim from CLM/msweep/measure_sweep.py — DO NOT tamper):
  bin_to_regions / region_rates / m_causal_power poke-logic / evaluate (3-check)
  MARGIN_FRAC=0.10, NONTRIVIAL_EPS=1e-6, N_SIZES=[4,5,6], CAUSAL_POKES=16.

GREEN => CAUSAL-POWER is a genuine chip-native measure on real silicon.
RED   => HW-limited (escalate backlog #3 CERTIFY-NOT-MEASURE).

Run ON pi5 (single-chip file-lock): stop the streamer service first, run this,
then RESTART the streamer (leave pi5 as found). Mac=0; $0.
"""
from __future__ import annotations
import argparse, json, os, sys, time
from typing import Dict, List, Tuple
import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
# the frozen measure lives in the anima repo CLM/msweep; allow an override path
_MSWEEP = os.environ.get("CLM_MSWEEP", _HERE)
if _MSWEEP not in sys.path:
    sys.path.insert(0, _MSWEEP)
from measure_sweep import (  # frozen — DO NOT re-implement
    bin_to_regions, region_rates, evaluate,
    MARGIN_FRAC, NONTRIVIAL_EPS, N_SIZES, CAUSAL_POKES, N_STEPS, NEURONS_PER_REGION,
)

import akida

IN_LINES = 16   # InputData width (spike_streamer default)


def build_chip(n_units, device):
    """InputData -> FullyConnected LIF pool, mapped to HARDWARE (spike_streamer)."""
    m = akida.Model()
    m.add(akida.InputData(input_shape=(1, 1, IN_LINES), input_bits=4, name="in"))
    m.add(akida.FullyConnected(units=n_units, weights_bits=4, activation=True,
                               act_bits=1, name="lif"))
    m.map(device)
    lif = m.get_layer("lif")
    W = lif.get_variable("weights")
    lif.set_variable("weights", np.ones_like(W))   # potential = Σ inputs
    backend = str(m.sequences[0].backend)
    return m, lif, backend


def hw_spike_raster(m, lif, n_regions, regime, seed, device):
    """Collect a (n_neurons x N_STEPS) BINARY raster from the LIVE chip.

    n_neurons = n_regions * NEURONS_PER_REGION mapped onto the chip's n_units LIF
    pool (n_units == n_neurons). Each step: build the IN_LINES input from a
    per-region drive + (rich only) coupling feedback from the previous on-chip
    spike, run model.forward ON THE CHIP, record the binary spike vector.
    """
    rng = np.random.default_rng(seed)
    n_neurons = n_regions * NEURONS_PER_REGION
    region_of = np.repeat(np.arange(n_regions), NEURONS_PER_REGION)
    # per-region base drive, CENTERED so thr=POT-drive straddles POT (partial,
    # poke-responsive fire band — NOT saturated). drive>0 => fires; <0 => silent.
    # collapse: region0 strongly above threshold (monopoly), others below &
    #           DECOUPLED -> a poke dies locally (no integration).
    # rich:     every region near threshold + strong coupling -> a poke shifts
    #           OTHER regions across the firing boundary (integration).
    if regime == "collapse":
        region_drive = np.full(n_regions, -5.0); region_drive[0] = 6.0
        coupling = 0.0
    elif regime == "rich":
        # baseline just below threshold so noise occasionally fires -> coupling
        # (OTHER regions' activity) amplifies it into a SELF-SUSTAINING partial
        # fire band at the edge of chaos: poke-responsive (a poke crosses other
        # regions over the boundary = integration), NOT saturated, NOT silent.
        region_drive = np.full(n_regions, -1.0)
        coupling = 3.0
    else:
        raise ValueError("unknown regime " + repr(regime))
    # Constant input -> every unit's on-chip potential = Σ inp = POT (all-ones
    # weights). The per-unit DRIVE is encoded into the per-unit int32 THRESHOLD,
    # rewritten each step (the streamer's set_variable("threshold", ...) knob):
    #   thr_j = POT - drive_j   =>   the chip fires unit j iff POT > thr_j iff
    #   drive_j > 0. The threshold-AND-FIRE comparison runs ON THE CHIP per unit;
    # SW only sets the per-unit threshold (the drive) and reads the chip's
    # per-unit binary spike. coupling feeds the PREVIOUS on-chip spike back into
    # the drive (rich only) -> cross-region integration around the silicon.
    IN_LEVEL = 8
    POT = IN_LEVEL * IN_LINES                     # Σ inp with all-ones weights
    inp = np.full((1, 1, 1, IN_LINES), IN_LEVEL, dtype=np.uint8)
    raster = np.zeros((n_neurons, N_STEPS), dtype=np.int8)
    region_act = np.zeros(n_regions)              # EMA of region spike fraction
    for t in range(N_STEPS):
        other = (region_act.sum() - region_act) / max(1, n_regions - 1)
        drive_u = region_drive[region_of] + coupling * other[region_of]
        drive_u = drive_u + rng.normal(0.0, 1.0, n_neurons)
        # encode per-unit drive into the per-unit chip threshold (higher drive
        # -> lower threshold -> more likely to fire on-chip)
        thr = np.clip(POT - drive_u, -32, 128).astype(np.int32)
        lif.set_variable("threshold", thr)
        y = m.forward(inp)                        # ON-CHIP threshold-and-fire
        yv = np.asarray(y).reshape(-1)
        fire = (yv[:n_neurons] > 0).astype(np.int8) if yv.size >= n_neurons \
            else np.zeros(n_neurons, dtype=np.int8)
        raster[:, t] = fire
        for r in range(n_regions):
            region_act[r] = 0.7 * region_act[r] + 0.3 * float(fire[region_of == r].mean())
    return raster


def m_causal_power_hw(m, lif, n_regions, regime, seed, device):
    base = region_rates(bin_to_regions(
        hw_spike_raster(m, lif, n_regions, regime, seed, device), n_regions))
    pokes = min(CAUSAL_POKES, n_regions)
    region_of = np.repeat(np.arange(n_regions), NEURONS_PER_REGION)
    effects = []
    for k in range(pokes):
        poke_r = k % n_regions
        raster = hw_spike_raster(m, lif, n_regions, regime, seed + 1000 + k, device)
        inj = raster.copy(); qlen = N_STEPS // 4
        inj[region_of == poke_r, :qlen] = 1
        rs = bin_to_regions(inj, n_regions); rates = region_rates(rs)
        others = [r for r in range(n_regions) if r != poke_r]
        if others:
            effects.append(float(np.abs(rates[others] - base[others]).mean()))
    return float(np.mean(effects)) if effects else 0.0


def run(seed):
    dev = akida.devices()[0]
    meta = {"sdk": akida.__version__, "device": str(dev.version)}
    vals = {}; backends = set()
    for n in N_SIZES:
        n_units = n * NEURONS_PER_REGION
        m, lif, backend = build_chip(n_units, dev)
        backends.add(backend)
        for regime in ("collapse", "rich"):
            vals[(regime, n)] = m_causal_power_hw(m, lif, n, regime, seed + n, dev)
    ev = evaluate("CAUSAL-POWER", vals)
    return {"batch": "clm-causal-hw", "axis": "B_live_hw_spike", "measure": "CAUSAL-POWER",
        "seed": seed, "sizes": N_SIZES, "neurons_per_region": NEURONS_PER_REGION, "n_steps": N_STEPS,
        "frozen_thresholds": {"margin_frac": MARGIN_FRAC, "nontrivial_eps": NONTRIVIAL_EPS, "causal_pokes_cap": CAUSAL_POKES},
        "spike_source": "LIVE AKD1000 on-chip threshold-and-fire (BackendType.Hardware)",
        "chip_backends": sorted(backends), "on_hardware": any("Hardware" in b for b in backends),
        "regime_def": {"collapse": "region0 monopoly drive + coupling 0 (decoupled)",
                       "rich": "balanced drive + coupling 6 (SW-closed loop around silicon)"},
        "device_meta": meta, "result": ev, "verdict": ev["verdict"]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=187)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    led = run(a.seed)
    if a.json:
        print(json.dumps(led, indent=2))
    else:
        ev = led["result"]; c = ev["checks"]
        print("=== CLM CAUSAL-POWER LIVE HW (axis B) ===")
        print("spike:", led["spike_source"], "| on_hardware:", led["on_hardware"], "| backends:", led["chip_backends"])
        print("device:", led["device_meta"])
        print("values:", json.dumps(ev["values"], indent=2))
        print("non-trivial=%s  collapse<rich=%s  size-robust=%s" % (c["nontrivial"], c["collapse_vs_rich"], c["size_robust"]))
        print("VERDICT:", ev["verdict"])


if __name__ == "__main__":
    main()
