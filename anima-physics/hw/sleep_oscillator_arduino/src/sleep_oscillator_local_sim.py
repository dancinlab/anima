#!/usr/bin/env python3
"""sleep_oscillator_local_sim.py

Mac-local numerical mirror of:

    1. anima-physics/oscillator/sleep_oscillator.hexa  (SW substrate)
    2. anima-physics/hw/sleep_oscillator_arduino/src/sleep_oscillator.ino
       + ad9833_driver.{h,cpp}                          (firmware)

We model the AD9833 28-bit phase accumulator at host-side double precision
(NOT integer-exact — sub-LSB AD9833 quantization is dominated by THD ~0.5 %
anyway; the dt-step phase accumulator captures the silicon-relevant
phase-continuous property).

No matplotlib; pure numpy + stdlib. Prints F-HW-SO-1..5 PASS/FAIL.

Run:
    python3 sleep_oscillator_local_sim.py
"""

from __future__ import annotations

import math
import sys
import time
from dataclasses import dataclass
from typing import List, Tuple

try:
    import numpy as np
except ImportError:  # pragma: no cover — Mac default has numpy
    print("FATAL: numpy not installed; `pip3 install numpy`", file=sys.stderr)
    sys.exit(2)


TWO_PI = 2.0 * math.pi

# Mirror sleep_oscillator.hexa constants exactly.
DELTA_FREQ = 2.0   # SWS
DELTA_AMP  = 1.0
THETA_FREQ = 6.0   # REM
THETA_AMP  = 0.7

MODE_SWS = 0
MODE_REM = 1

# AD9833 silicon parameters (informational; sim uses double-precision phase).
AD9833_MCLK_HZ   = 25_000_000
AD9833_PHASE_BITS = 28


@dataclass
class OscState:
    phase_rad: float
    freq_hz: float
    amp: float
    mode: int


def osc_new() -> OscState:
    """Mirror sleep_osc_new() — boot in SWS / δ mode."""
    return OscState(phase_rad=0.0, freq_hz=DELTA_FREQ, amp=DELTA_AMP, mode=MODE_SWS)


def osc_step(s: OscState, dt: float) -> OscState:
    """Mirror sleep_osc_step — phase += 2π·f·dt, wrap to [0, 2π)."""
    new_phase = s.phase_rad + TWO_PI * s.freq_hz * dt
    # wrap (use fmod for symmetry with hexa's while-loop)
    new_phase = new_phase % TWO_PI
    if new_phase < 0.0:
        new_phase += TWO_PI
    return OscState(new_phase, s.freq_hz, s.amp, s.mode)


def osc_switch(s: OscState, new_mode: int) -> OscState:
    """Mirror sleep_osc_switch — phase preserved, freq/amp updated.

    This is the phase-continuous primitive: same as AD9833 FREQ0 write
    without RESET — accumulator carries.
    """
    if new_mode == MODE_SWS:
        return OscState(s.phase_rad, DELTA_FREQ, DELTA_AMP, MODE_SWS)
    if new_mode == MODE_REM:
        return OscState(s.phase_rad, THETA_FREQ, THETA_AMP, MODE_REM)
    return s


def osc_sample(s: OscState) -> float:
    """Mirror sleep_osc_sample — amp · sin(phase)."""
    return s.amp * math.sin(s.phase_rad)


def ad9833_freq_word(f_out_hz: float, mclk_hz: int = AD9833_MCLK_HZ) -> int:
    """Mirror ad9833_freq_word() — tuning word at host side."""
    if f_out_hz <= 0.0:
        return 0
    scale = (1 << AD9833_PHASE_BITS) / float(mclk_hz)
    tw = int(round(f_out_hz * scale))
    return min(tw, (1 << AD9833_PHASE_BITS) - 1)


# ───── trace generators (used by multiple falsifiers) ─────


def run_trace(state: OscState, n: int, dt: float
              ) -> Tuple[OscState, np.ndarray, np.ndarray, int]:
    """Run n osc_step calls; return final state, phase[], sample[], wrap_count."""
    phases = np.empty(n, dtype=np.float64)
    samples = np.empty(n, dtype=np.float64)
    wrap_count = 0
    s = state
    prev_phase = s.phase_rad
    for i in range(n):
        s = osc_step(s, dt)
        # detect wrap (decreased phase = wrap occurred this step)
        if s.phase_rad < prev_phase:
            wrap_count += 1
        prev_phase = s.phase_rad
        phases[i] = s.phase_rad
        samples[i] = osc_sample(s)
    return s, phases, samples, wrap_count


def zero_cross_freq(samples: np.ndarray, dt: float) -> float:
    """Cycle-counting frequency estimate (mirror of estimate_freq.hexa)."""
    n = len(samples)
    if n < 2:
        return 0.0
    crossings = 0
    prev = samples[0]
    for i in range(1, n):
        curr = samples[i]
        if (prev > 0.0 and curr <= 0.0) or (prev <= 0.0 and curr > 0.0):
            crossings += 1
        prev = curr
    total_time = (n - 1) * dt
    if total_time <= 0.0:
        return 0.0
    return crossings / (2.0 * total_time)


# ───── falsifiers F-HW-SO-1..5 ─────


def f_hw_so_1() -> Tuple[bool, str]:
    """Phase init = 0 at t=0."""
    s = osc_new()
    ok = math.isclose(s.phase_rad, 0.0, abs_tol=1e-12)
    return ok, f"phase_init={s.phase_rad:.6e} (expect 0.0)"


def f_hw_so_2(dt: float = 0.001, n: int = 10_000) -> Tuple[bool, str]:
    """SWS mode → zero-cross freq ≈ 2.0 Hz over 10 s."""
    s = osc_new()  # already SWS
    _, _, samples, _ = run_trace(s, n=n, dt=dt)
    f_est = zero_cross_freq(samples, dt)
    ok = abs(f_est - DELTA_FREQ) < 0.1
    return ok, f"SWS f_est={f_est:.4f} Hz (expect {DELTA_FREQ} ±0.1)"


def f_hw_so_3(dt: float = 0.001, n: int = 10_000) -> Tuple[bool, str]:
    """REM mode → zero-cross freq ≈ 6.0 Hz over 10 s."""
    s = osc_switch(osc_new(), MODE_REM)
    _, _, samples, _ = run_trace(s, n=n, dt=dt)
    f_est = zero_cross_freq(samples, dt)
    ok = abs(f_est - THETA_FREQ) < 0.2
    return ok, f"REM f_est={f_est:.4f} Hz (expect {THETA_FREQ} ±0.2)"


def f_hw_so_4(dt: float = 0.001, n: int = 327) -> Tuple[bool, str]:
    """Mode switch is phase-continuous (no jump in phase across switch).

    Run SWS for n steps, snapshot phase, switch to REM, snapshot phase
    immediately. Difference must be exactly 0 (silicon analog: AD9833
    FREQ0 write does not touch phase accumulator).
    """
    s = osc_new()
    s, _, _, _ = run_trace(s, n=n, dt=dt)
    phase_before = s.phase_rad
    s_after = osc_switch(s, MODE_REM)
    phase_after = s_after.phase_rad
    delta = abs(phase_after - phase_before)
    ok = delta < 1e-9 and s_after.freq_hz == THETA_FREQ
    return ok, (
        f"phase_before={phase_before:.9f} phase_after={phase_after:.9f} "
        f"delta={delta:.3e} freq_after={s_after.freq_hz}"
    )


def f_hw_so_5(dt: float = 0.001, n: int = 10_000) -> Tuple[bool, str]:
    """10 s of SWS (2 Hz) → ≥20 phase wraps."""
    s = osc_new()
    _, _, _, wrap_count = run_trace(s, n=n, dt=dt)
    ok = wrap_count >= 20
    return ok, f"wrap_count={wrap_count} (expect >=20 for 2Hz × 10s)"


FALSIFIERS = [
    ("F-HW-SO-1", "phase init = 0", f_hw_so_1),
    ("F-HW-SO-2", "SWS freq = 2.0 Hz", f_hw_so_2),
    ("F-HW-SO-3", "REM freq = 6.0 Hz", f_hw_so_3),
    ("F-HW-SO-4", "mode switch phase-continuous", f_hw_so_4),
    ("F-HW-SO-5", "10 s SWS produces ≥20 wraps", f_hw_so_5),
]


# ───── informational AD9833 tuning-word table ─────


def print_freq_word_table() -> None:
    print("[AD9833 tuning words @ MCLK=25 MHz]")
    for label, f in [("SWS δ", DELTA_FREQ), ("REM θ", THETA_FREQ)]:
        tw = ad9833_freq_word(f)
        lsb14 = tw & 0x3FFF
        msb14 = (tw >> 14) & 0x3FFF
        print(f"  {label}  f={f:>4.1f} Hz  word=0x{tw:07X}  "
              f"lsb14=0x{lsb14:04X}  msb14=0x{msb14:04X}")


# ───── driver ─────


def main() -> int:
    print("=" * 72)
    print("sleep_oscillator_local_sim.py — anima-physics HW #4 Phase 1a Mac sim")
    print(f"SW source: oscillator/sleep_oscillator.hexa (§188 PASS 5/5)")
    print(f"firmware:  src/sleep_oscillator.ino + ad9833_driver.{{h,cpp}}")
    print("=" * 72)
    print_freq_word_table()
    print()
    t0 = time.time()
    pass_count = 0
    results: List[Tuple[str, str, bool, str]] = []
    for fid, desc, fn in FALSIFIERS:
        try:
            ok, detail = fn()
        except Exception as exc:  # defensive
            ok, detail = False, f"EXCEPTION {type(exc).__name__}: {exc}"
        verdict = "PASS" if ok else "FAIL"
        print(f"[{fid}] {verdict}  {desc}")
        print(f"        {detail}")
        if ok:
            pass_count += 1
        results.append((fid, desc, ok, detail))
    wall_s = time.time() - t0
    print()
    print(f"summary: {pass_count}/{len(FALSIFIERS)} PASS  (wall {wall_s:.3f} s)")
    print()
    if pass_count == len(FALSIFIERS):
        print(">>> sleep_oscillator_arduino Python sim: 5/5 PASS — HW #4 Phase 1a DONE")
        return 0
    print(">>> SOME FALSIFIERS FAILED — see detail above")
    return 1


if __name__ == "__main__":
    sys.exit(main())
