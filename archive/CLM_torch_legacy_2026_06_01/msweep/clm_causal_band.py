"""CLM CAUSAL-POWER — LIVE AKD1000 coupling-BAND characterization (axis B follow-up).

F-CLM-CAUSAL-XFER axis B (clm_causal_hw.py) showed the GREEN CAUSAL-POWER measure
SURVIVES on real silicon at ONE coupling point (rich = balanced drive + coupling 3).
This harness CHARACTERIZES the regime: it sweeps the coupling strength K (the
SW-closed feedback gain around the chip, an ENVIRONMENT knob — NOT a measure knob)
and maps Delta(K) = causal_power(rich,K) - causal_power(collapse_floor) on the LIVE
AKD1000, to locate the edge-of-chaos BAND where the measure reads integration.

The measure itself (region_rates / bin_to_regions / poke logic / MARGIN_FRAC) is
REUSED VERBATIM from measure_sweep.py — FROZEN, never re-tuned. Only the regime
coupling K varies. The on-chip threshold-and-fire is unchanged silicon.

PRE-REGISTERED falsifier  F-CLM-CAUSAL-BAND  (the "edge-of-chaos" claim is BOUNDED):
  Sweep K over a frozen grid. Let Delta(K)=cp_rich(K)-cp_collapse, K*=interior argmax.
  PASS (genuine bounded band) iff ALL three:
    (a) band-exists   : Delta(K*) > NONTRIVIAL_EPS  AND  K* is INTERIOR (not an end).
    (b) cold rolloff  : Delta(K_min) < (1-MARGIN_FRAC)*Delta(K*)  (too-weak coupling
                        -> decoupled, a poke dies locally; integration absent).
    (c) sat rolloff   : Delta(K_max) < (1-MARGIN_FRAC)*Delta(K*)  (too-strong coupling
                        -> all-fire saturation, a poke changes nothing; THIS is the
                        falsifiable edge-of-chaos high-end claim).
  RED (FALSIFIED) iff Delta is MONOTONE in K (no high-end rolloff) -> the signal is
  just "more coupling = more integration", NOT a bounded edge-of-chaos band; the
  measure would then not certify a *regime* on the chip, only a direction.

Also reports per-K mean firing fraction (cold ~0, band partial, saturate ~1) as the
mechanistic signature of the two failure ends.

Run ON pi5 (single-chip file-lock): stop the streamer service, run this, then
RESTART the streamer identically (leave pi5 as found). Mac=0; $0.
"""
from __future__ import annotations
import argparse, json, os, sys
from typing import Dict, List, Tuple
import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
_MSWEEP = os.environ.get("CLM_MSWEEP", _HERE)
if _MSWEEP not in sys.path:
    sys.path.insert(0, _MSWEEP)
from measure_sweep import (  # frozen — DO NOT re-implement
    bin_to_regions, region_rates,
    MARGIN_FRAC, NONTRIVIAL_EPS, N_SIZES, CAUSAL_POKES, N_STEPS, NEURONS_PER_REGION,
)

import akida

IN_LINES = 16
IN_LEVEL = 8

# PRE-REGISTERED coupling grid (frozen). K=0 (with balanced drive) is the cold /
# decoupled end; the top of the grid is the saturation end. Monopoly collapse is a
# SEPARATE floor (region0-only drive, coupling 0).
K_GRID = [0.0, 1.0, 2.0, 3.0, 4.0, 6.0, 9.0, 13.0, 18.0, 24.0]


def build_chip(n_units, device):
    """InputData -> FullyConnected LIF pool, mapped to HARDWARE (spike_streamer)."""
    m = akida.Model()
    m.add(akida.InputData(input_shape=(1, 1, IN_LINES), input_bits=4, name="in"))
    m.add(akida.FullyConnected(units=n_units, weights_bits=4, activation=True,
                               act_bits=1, name="lif"))
    m.map(device)
    lif = m.get_layer("lif")
    W = lif.get_variable("weights")
    lif.set_variable("weights", np.ones_like(W))
    backend = str(m.sequences[0].backend)
    return m, lif, backend


def hw_spike_raster(m, lif, n_regions, monopoly, coupling, seed):
    """Collect a (n_neurons x N_STEPS) BINARY raster from the LIVE chip at a given
    coupling K. monopoly=True => collapse floor (region0 drive only, K forced 0).
    Otherwise rich-style balanced drive with feedback gain K."""
    rng = np.random.default_rng(seed)
    n_neurons = n_regions * NEURONS_PER_REGION
    region_of = np.repeat(np.arange(n_regions), NEURONS_PER_REGION)
    if monopoly:
        region_drive = np.full(n_regions, -5.0); region_drive[0] = 6.0
        coupling = 0.0
    else:
        region_drive = np.full(n_regions, -1.0)   # balanced, just below threshold
    POT = IN_LEVEL * IN_LINES
    inp = np.full((1, 1, 1, IN_LINES), IN_LEVEL, dtype=np.uint8)
    raster = np.zeros((n_neurons, N_STEPS), dtype=np.int8)
    region_act = np.zeros(n_regions)
    for t in range(N_STEPS):
        other = (region_act.sum() - region_act) / max(1, n_regions - 1)
        drive_u = region_drive[region_of] + coupling * other[region_of]
        drive_u = drive_u + rng.normal(0.0, 1.0, n_neurons)
        thr = np.clip(POT - drive_u, -32, 128).astype(np.int32)
        lif.set_variable("threshold", thr)
        y = m.forward(inp)
        yv = np.asarray(y).reshape(-1)
        fire = (yv[:n_neurons] > 0).astype(np.int8) if yv.size >= n_neurons \
            else np.zeros(n_neurons, dtype=np.int8)
        raster[:, t] = fire
        for r in range(n_regions):
            region_act[r] = 0.7 * region_act[r] + 0.3 * float(fire[region_of == r].mean())
    return raster


def causal_power(m, lif, n_regions, monopoly, coupling, seed):
    """Frozen CAUSAL-POWER poke logic (verbatim from clm_causal_hw) at coupling K."""
    base = region_rates(bin_to_regions(
        hw_spike_raster(m, lif, n_regions, monopoly, coupling, seed), n_regions))
    pokes = min(CAUSAL_POKES, n_regions)
    region_of = np.repeat(np.arange(n_regions), NEURONS_PER_REGION)
    effects = []
    for k in range(pokes):
        poke_r = k % n_regions
        raster = hw_spike_raster(m, lif, n_regions, monopoly, coupling, seed + 1000 + k)
        inj = raster.copy(); qlen = N_STEPS // 4
        inj[region_of == poke_r, :qlen] = 1
        rates = region_rates(bin_to_regions(inj, n_regions))
        others = [r for r in range(n_regions) if r != poke_r]
        if others:
            effects.append(float(np.abs(rates[others] - base[others]).mean()))
    return float(np.mean(effects)) if effects else 0.0


def fire_fraction(m, lif, n_regions, coupling, seed):
    return float(hw_spike_raster(m, lif, n_regions, False, coupling, seed).mean())


def evaluate_band(deltas, grid):
    """Pre-registered F-CLM-CAUSAL-BAND 3-check on the Delta(K) curve."""
    arr = np.asarray(deltas, dtype=float)
    kstar = int(arr.argmax())
    peak = float(arr[kstar])
    interior = 0 < kstar < len(arr) - 1
    band_exists = peak > NONTRIVIAL_EPS and interior
    cold_rolloff = bool(arr[0] < (1.0 - MARGIN_FRAC) * peak)
    sat_rolloff = bool(arr[-1] < (1.0 - MARGIN_FRAC) * peak)
    monotone = bool(np.all(np.diff(arr) >= -NONTRIVIAL_EPS))
    verdict = "PASS" if (band_exists and cold_rolloff and sat_rolloff) else "RED"
    return {"k_star": grid[kstar], "k_star_idx": kstar, "peak_delta": peak,
            "interior_peak": interior, "band_exists": band_exists,
            "cold_rolloff": cold_rolloff, "sat_rolloff": sat_rolloff,
            "monotone": monotone, "verdict": verdict}


def run(seed):
    dev = akida.devices()[0]
    meta = {"sdk": akida.__version__, "device": str(dev.version)}
    backends = set()
    floor_vals = []
    for n in N_SIZES:
        m, lif, backend = build_chip(n * NEURONS_PER_REGION, dev); backends.add(backend)
        floor_vals.append(causal_power(m, lif, n, True, 0.0, seed + n))
    cp_collapse = float(np.mean(floor_vals))
    rows = []
    for K in K_GRID:
        cps, fires = [], []
        for n in N_SIZES:
            m, lif, backend = build_chip(n * NEURONS_PER_REGION, dev); backends.add(backend)
            cps.append(causal_power(m, lif, n, False, K, seed + n))
            fires.append(fire_fraction(m, lif, n, K, seed + n))
        cp = float(np.mean(cps))
        rows.append({"K": K, "cp_rich": cp, "delta": cp - cp_collapse,
                     "fire_frac": float(np.mean(fires))})
    band = evaluate_band([r["delta"] for r in rows], K_GRID)
    return {"batch": "clm-causal-band", "axis": "B_live_hw_band", "measure": "CAUSAL-POWER",
            "seed": seed, "sizes": N_SIZES, "neurons_per_region": NEURONS_PER_REGION,
            "n_steps": N_STEPS, "k_grid": K_GRID,
            "frozen_thresholds": {"margin_frac": MARGIN_FRAC, "nontrivial_eps": NONTRIVIAL_EPS,
                                  "causal_pokes_cap": CAUSAL_POKES},
            "spike_source": "LIVE AKD1000 on-chip threshold-and-fire (BackendType.Hardware)",
            "chip_backends": sorted(backends),
            "on_hardware": any("Hardware" in b for b in backends),
            "cp_collapse_floor": cp_collapse, "sweep": rows, "band": band,
            "device_meta": meta, "verdict": band["verdict"]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=187)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    led = run(a.seed)
    if a.json:
        print(json.dumps(led, indent=2)); return
    b = led["band"]
    print("=== CLM CAUSAL-POWER LIVE HW coupling-BAND (axis B follow-up) ===")
    print("on_hardware:", led["on_hardware"], "| backends:", led["chip_backends"])
    print("device:", led["device_meta"], "| collapse floor:", round(led["cp_collapse_floor"], 4))
    print("  K      cp_rich   Delta    fire_frac")
    for r in led["sweep"]:
        print("  %5.1f  %7.4f  %7.4f   %5.3f" % (r["K"], r["cp_rich"], r["delta"], r["fire_frac"]))
    print("K* = %.1f (idx %d, interior=%s) peak Delta=%.4f" %
          (b["k_star"], b["k_star_idx"], b["interior_peak"], b["peak_delta"]))
    print("band-exists=%s cold-rolloff=%s sat-rolloff=%s monotone=%s" %
          (b["band_exists"], b["cold_rolloff"], b["sat_rolloff"], b["monotone"]))
    print("VERDICT:", led["verdict"])


if __name__ == "__main__":
    main()
