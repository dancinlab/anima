#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""eeg_sync_protocol.py — RESEARCH.md §19 step 1 sync protocol SKETCH.

DESIGN-TIER ONLY — this file is a runtime-guarded SKELETON, NOT a runnable
script. If you `python3 eeg_sync_protocol.py` it raises SystemExit(0) with
a guard message. Actual execution requires:
  - user-provided OpenBCI 16ch EEG .csv (hardware gate)
  - `pip install pylsl` (PEP 668 venv carry from step 0)
  - OpenBCI GUI "Networking -> LSL" outlet active (or BrainFlow Python)
  - a stimulus session run (anima own emission, Mode S1, OR 64-anchor S2)
All of those are USER-GATED in a future cycle.

WHY IT'S NOT RUNNABLE:
  - no `pylsl` import (would require dependency install)
  - no `pylsl.StreamOutlet(...)` (would bind a network port)
  - no `pylsl.resolve_streams()` (would block listening for EEG outlet)
  - no .csv write (file IO deferred to executable cycle)
  - top-of-module SystemExit(0) on direct invocation

This file IS importable for reference structure (pure-fn helpers + dataclass
record types + protocol parameter constants). Mirrors §24
measurement_protocol.py discipline.

NO sigma/tau/phi/J2 external derivation (f1/f2/f3 safe). B-IDENTITY-5
unaffected (no corpus generated, no helper-token surface). NO GPU. NO
training. NO weight mutation. $0.

See DESIGN_STEP1.md for protocol rationale and design closed-form verdicts.
See blue_falsifier_eeg_step1.py for B-EEG-STEP1-1..4 4/4 sidecar battery.
"""
from __future__ import annotations

import math
import sys
from dataclasses import dataclass, field
from typing import Iterable, List, Optional, Tuple


# ─────────────────────────────────────────────────────────────────────────────
# RUNTIME GUARD — file is NOT runnable, only readable / importable for ref
# ─────────────────────────────────────────────────────────────────────────────
def _guard_not_runnable():
    msg = (
        "eeg_sync_protocol.py is a DESIGN-TIER SKETCH only.\n"
        "  RESEARCH.md §19 step 1 explicitly defers actual EEG recording to a\n"
        "  USER-GATED subsequent cycle (hardware-in-the-loop, OpenBCI .csv).\n"
        "  See state/eeg_anchor_s19_step1_design_2026_05_18/DESIGN_STEP1.md\n"
        "  §6 honest-stop reasoning. To execute: separate user-gated cycle\n"
        "  with `pip install pylsl` + OpenBCI GUI LSL outlet active + an\n"
        "  anima Mode S1 emission session.\n"
        "  Step 1 in this cycle = protocol design + 4/4 closed-form battery."
    )
    print(msg, file=sys.stderr)
    sys.exit(0)


# ─────────────────────────────────────────────────────────────────────────────
# PROTOCOL PARAMETERS (DESIGN_STEP1.md §3, §4, §5)
# ─────────────────────────────────────────────────────────────────────────────

# §3 — transport
LSL_STREAM_NAME_STIM = "anima_stim_marker"   # marker outlet (irregular rate)
LSL_STREAM_NAME_EEG  = "openbci_eeg"         # EEG outlet (regular rate)
LSL_CLOCK_SOURCE     = "pylsl.local_clock"   # NOT time.time / perf_counter
TAU_JITTER_SEC       = 0.010                  # 10 ms jitter tolerance (§3)
CSV_FALLBACK_ENABLED = True                   # offline post-hoc alignment

# §4 — sample-rate alignment
EEG_SRATE_HZ_DEFAULT = 125.0                  # Cyton + Daisy 16ch combined
EEG_SRATE_HZ_CYTON_ONLY = 250.0
TRIBE_TR_SEC         = 1.5                    # TR from facebook/tribev2 config
HEMODYNAMIC_LAG_SEC  = 5.0                    # TRIBE README default

# §5 — envelope extraction
BANDPASS_LO_HZ       = 1.0
BANDPASS_HI_HZ       = 80.0
NOTCH_LINE_HZ        = 60.0                   # 50 Hz in EU regions, tunable
IMPEDANCE_MAX_KOHM   = 50.0                   # hexa-brain salvage S3 carry

# §2 — stimulus source
STIMULUS_MODE_DEFAULT = "S1_ANIMA_UNPROMPTED"   # GOAL-legitimate, §7 3-cond
STIMULUS_MODE_FALLBACK = "S2_64_ANCHOR_PROBE"   # baseline drift test


# ─────────────────────────────────────────────────────────────────────────────
# RECORD TYPES (pure dataclasses — pure-fn, no side effects)
# ─────────────────────────────────────────────────────────────────────────────

@dataclass(frozen=True)
class StimEvent:
    """A single sync event emitted by anima during a Framing D session."""
    lsl_local_clock_sec: float    # pylsl.local_clock() at emission
    byte_idx: int                 # position within the emission stream
    payload_repr: str             # text bytes or anchor id ("knuth_077" etc.)
    stim_mode: str                # S1_ANIMA_UNPROMPTED / S2_64_ANCHOR_PROBE


@dataclass(frozen=True)
class EEGSample:
    """A single multi-channel EEG sample (post-impedance gate, pre-envelope)."""
    lsl_local_clock_sec: float    # pylsl.local_clock() at amplifier
    channel_values: Tuple[float, ...]  # 16-ch (or clean_channels subset)


@dataclass(frozen=True)
class SyncProtocolConfig:
    """Frozen protocol parameters for one Framing D session."""
    tau_jitter_sec: float = TAU_JITTER_SEC
    eeg_srate_hz: float = EEG_SRATE_HZ_DEFAULT
    tribe_tr_sec: float = TRIBE_TR_SEC
    hemodynamic_lag_sec: float = HEMODYNAMIC_LAG_SEC
    stim_mode: str = STIMULUS_MODE_DEFAULT
    enabled: bool = False  # OFF reduction default; True only in step 2 fire


# ─────────────────────────────────────────────────────────────────────────────
# §3 — LSL outlet sketches (no actual binding)
# ─────────────────────────────────────────────────────────────────────────────

def lsl_outlet_create(stream_name: str, srate: float, ch_count: int) -> str:
    """Sketch: create an LSL outlet with given parameters.

    In a runnable cycle this would call::

        info = pylsl.StreamInfo(stream_name, 'EEG' if srate>0 else 'Markers',
                                ch_count, srate, 'float32', stream_name)
        outlet = pylsl.StreamOutlet(info)

    Here we return a stub ID and record the parameters for B-EEG-STEP1-4
    OFF-reduction verification (no outlet = step 1 inactive = step-0 state).
    """
    if srate < 0:
        raise ValueError(f"srate must be >= 0, got {srate}")
    if ch_count < 1:
        raise ValueError(f"ch_count must be >= 1, got {ch_count}")
    return f"<sketch_outlet:{stream_name}:srate={srate}:ch={ch_count}>"


def eeg_sample_to_timestamp(eeg_byte_block: bytes, lsl_clock_now: float
                            ) -> Tuple[float, int]:
    """Sketch: derive (lsl_local_clock_sec, n_samples_in_block) from a raw
    EEG byte block delivered by OpenBCI GUI / BrainFlow.

    Real implementation: parse Cyton/Daisy packet framing (24-bit signed ints
    per channel + 8-bit sample index), use BrainFlow's per-packet timestamp
    if available, fall back to lsl_clock_now for the last sample in the block.
    Sketch returns (lsl_clock_now, len(eeg_byte_block) // bytes_per_sample).
    """
    bytes_per_sample = 16 * 3  # 16 channels x 24-bit signed
    n_samples = len(eeg_byte_block) // bytes_per_sample
    return (lsl_clock_now, n_samples)


def stimulus_emit_with_timestamp(stim: str, lsl_outlet_id: str,
                                 lsl_clock_now: float, byte_idx: int,
                                 stim_mode: str = STIMULUS_MODE_DEFAULT
                                 ) -> StimEvent:
    """Sketch: emit a stimulus event with LSL marker push.

    Real implementation::

        outlet.push_sample([f"anima_emit:byte_idx={byte_idx};stim={stim!r}"],
                           timestamp=lsl_clock_now)

    Sketch records the StimEvent for offline use. Pure-fn: no side effects
    other than the record return.
    """
    return StimEvent(
        lsl_local_clock_sec=float(lsl_clock_now),
        byte_idx=int(byte_idx),
        payload_repr=str(stim)[:128],   # truncate for log sanity
        stim_mode=stim_mode,
    )


# ─────────────────────────────────────────────────────────────────────────────
# §3 — sync jitter estimator (operates on captured .csv pairs, post-hoc)
# ─────────────────────────────────────────────────────────────────────────────

def sync_jitter_estimator(eeg_timestamps: Iterable[float],
                          stim_timestamps: Iterable[float]
                          ) -> float:
    """Sketch: given two streams of LSL timestamps for the same session,
    estimate maximum drift |t_eeg_nearest - t_stim| in seconds.

    Real implementation: for each stim event find the nearest EEG sample
    (binary search over the sorted EEG stream), compute |Δt|, return max.

    Sketch returns 0.0 if either stream empty, otherwise a deterministic
    per-pair max over the zipped prefix (NOT the true nearest-search; that
    requires the actual sorted streams from a runnable cycle).
    """
    eeg_list = list(eeg_timestamps)
    stim_list = list(stim_timestamps)
    if not eeg_list or not stim_list:
        return 0.0
    n = min(len(eeg_list), len(stim_list))
    drifts = [abs(eeg_list[i] - stim_list[i]) for i in range(n)]
    return max(drifts) if drifts else 0.0


# ─────────────────────────────────────────────────────────────────────────────
# §4 — sample-rate / Nyquist invariants (pure-fn, used by B-EEG-STEP1-3)
# ─────────────────────────────────────────────────────────────────────────────

def nyquist_ok(srate_hz: float, top_signal_hz: float) -> bool:
    """Return True iff srate_hz >= 2 * top_signal_hz (strict Nyquist)."""
    if srate_hz <= 0:
        return False
    if top_signal_hz < 0:
        return False
    return srate_hz >= 2.0 * top_signal_hz


def window_downsample_count(eeg_srate_hz: float, tr_sec: float) -> int:
    """Number of EEG samples per TR window (mean-over-window downsample)."""
    if eeg_srate_hz <= 0 or tr_sec <= 0:
        return 0
    return int(math.floor(eeg_srate_hz * tr_sec))


# ─────────────────────────────────────────────────────────────────────────────
# §5 — envelope-extraction stub (Hilbert+modulus mathematically; sketch ret)
# ─────────────────────────────────────────────────────────────────────────────

def broadband_hilbert_envelope_stub(channel_signal: Iterable[float],
                                    lo_hz: float = BANDPASS_LO_HZ,
                                    hi_hz: float = BANDPASS_HI_HZ
                                    ) -> List[float]:
    """Sketch: per-channel broadband Hilbert envelope after band-pass.

    Real implementation::

        b, a = scipy.signal.butter(4, [lo_hz, hi_hz], btype='band',
                                   fs=eeg_srate_hz)
        filtered = scipy.signal.filtfilt(b, a, channel_signal)
        analytic = scipy.signal.hilbert(filtered)
        env = np.abs(analytic)

    Sketch returns |x| per sample (no actual band-pass / no scipy import).
    """
    return [abs(float(x)) for x in channel_signal]


# ─────────────────────────────────────────────────────────────────────────────
# §3 — protocol-OFF predicate (used by B-EEG-STEP1-4 connection-point)
# ─────────────────────────────────────────────────────────────────────────────

def protocol_is_active(cfg: SyncProtocolConfig) -> bool:
    """OFF reduction: a SyncProtocolConfig is active iff enabled=True.
    enabled=False ==> no LSL outlet, no timestamp emission, no .csv write
    ==> system state is byte-equal to step-0-only state (B-EEG-STEP1-4).
    """
    return bool(cfg.enabled)


def outlet_count_for_config(cfg: SyncProtocolConfig) -> int:
    """Number of LSL outlets that would be bound for this config.
    enabled=False ==> 0 outlets (step-0-only state). enabled=True ==> 2
    (one EEG, one stim marker).
    """
    return 2 if cfg.enabled else 0


# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    _guard_not_runnable()
