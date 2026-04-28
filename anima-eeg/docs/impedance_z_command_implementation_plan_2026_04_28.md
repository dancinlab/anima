# Impedance `z`-Command Implementation Plan (2026-04-28)

**Module:** `anima-eeg/electrode_adjustment_helper.hexa`
**Goal:** Replace RMS-heuristic electrode-quality scoring with native ADS1299
lead-off impedance measurement via OpenBCI `z`-command, surfaced as new
`--impedance` mode (existing `--watch`/`--check` RMS modes preserved for
backward compatibility).

**Status:** DESIGN ONLY — no code in `electrode_adjustment_helper.hexa` is
modified by this doc. Implementation lands in a follow-up cycle.

## Why

Current RMS heuristic flags large-amplitude artifacts (movement, mains pickup)
as "bad contact" — false-positive prone. The ADS1299 chip itself has a
hardware lead-off detector: it injects a small 31.5 Hz @ 6 nA AC current
through P or N pin and the resulting voltage at 31.5 Hz in the EEG output
is proportional to electrode-skin impedance (Ohm's law: `Z = V / I`).
This is exactly what the OpenBCI GUI does in `W_CytonImpedance.pde` and
is the canonical "did the electrode actually make contact" signal.

## References (already cloned)

| Ref | Path | Use |
|---|---|---|
| Widget | `references/OpenBCI_GUI/OpenBCI_GUI/W_CytonImpedance.pde` | master state-machine, sequencing |
| State enum | `references/OpenBCI_GUI/OpenBCI_GUI/CytonElectrodeStatus.pde` | 5-color thresholds + status struct |
| Board cmd | `references/OpenBCI_GUI/OpenBCI_GUI/BoardCyton.pde:415-475` | `z<CH><P><N>Z` build + send |
| SDK spec | `references/Documentation/website/docs/Cyton/04-OpenBCI_Cyton_SDK.md` § LeadOff | `z`-command grammar |
| Firmware | `references/OpenBCI_Cyton_Library/OpenBCI_32bit_Library.cpp:794` | `LOFF_MAG_6NA, LOFF_FREQ_31p2HZ` |

## Constants (anchored in references)

- Channel char map (Cyton + Daisy, 16ch):
  `['1','2','3','4','5','6','7','8','Q','W','E','R','T','Y','U','I']`
- Probe frequency: **31.5 Hz** (LOFF_FREQ_31p2HZ — actually 31.2 Hz on chip;
  reference doc rounds to 31.5)
- Probe current: **6 nA** AC (LOFF_MAG_6NA)
- Conversion: `Z_ohm = V_31.5Hz_amplitude / 6e-9`
- Sample rate: 250 Hz fixed (Cyton radio-limited)
- 1 s window → 250 samples → 31.5 Hz bin via FFT (bin width 1 Hz)

## Thresholds (ports `CytonElectrodeStatus.pde` impedance ranges)

GUI reference defaults: `impedanceGreenCutoff=750 kΩ`,
`impedanceYellowCuttoff=2500 kΩ`. Task spec asks 3 MΩ red boundary; we
adopt the **task spec** values to match user intent (matches
`integration-guide.md` end-user terminology):

| State | Range | ANSI 24-bit RGB | Symbol |
|---|---|---|---|
| GREEN  | < 750 kΩ            | `38;2;0;255;100`    | `[●]` |
| YELLOW | 750 kΩ – 3 MΩ       | `38;2;230;199;0`    | `[●]` |
| RED    | > 3 MΩ              | `38;2;255;0;0`      | `[●]` |
| BLUE   | testing in progress | `38;2;65;96;128`    | `[?]` |
| GRAY   | not yet tested      | `38;2;113;117;119`  | `[·]` |

Threshold values overridable via `--green-kohm <n> --yellow-kohm <n>`.

## State Machine

```
                +-----------+
                |   IDLE    |  --selftest emits synthetic frame, exits
                +-----------+
                      | --impedance
                      v
                +-----------+
                |  INIT     |  open BrainFlow, send 'd' (default), 's' stop
                +-----------+
                      |
                      v
              +-----------------+
              | CHECK ch i (1s) |  config_board('z<CH>10Z') · 'b' stream ·
              | i = 1..16       |  collect 250 samples · 's' stop ·
              +-----------------+  config_board('z<CH>00Z') · classify
                      |
                      v
                +-----------+
                |  RENDER   |  ASCII map + per-channel kΩ + state
                +-----------+
                      |
              +-------+-------+
              |               |
              v               v
        sweep done      next ch (i+1)
              |
              v
        +-----------+
        |   DONE    |  emit kv summary, exit (sweep mode)
        +-----------+
```

**Total wallclock per full sweep:** ~16 s data + ~4-8 s command/stream
toggles = **~20-24 s** for 16 channels (P-pin only). N+P = ~40-48 s.

**Default:** P-pin only (matches GUI `setCheckingImpedance` default
`p='1', n='0'` for typical scalp electrodes — N is SRB1 reference).
Optional `--check-n-pin` for paranoid mode.

## BrainFlow Python Integration

In the `/tmp/` helper (raw#37 transient pattern, identical to existing
`_write_helper()`):

```python
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds
import numpy as np

CHAN_CHARS = ['1','2','3','4','5','6','7','8','Q','W','E','R','T','Y','U','I']

def measure_impedance(board, ch_idx, seconds=1, fs=250):
    ch_char = CHAN_CHARS[ch_idx]
    # Enable lead-off probe on P pin
    board.config_board(f"z{ch_char}10Z")
    board.start_stream()
    time.sleep(seconds)
    data = board.get_board_data()  # all samples since stream start
    board.stop_stream()
    # Disable lead-off
    board.config_board(f"z{ch_char}00Z")
    eeg_chan = BoardShim.get_eeg_channels(BoardIds.CYTON_DAISY_BOARD)[ch_idx]
    sig = data[eeg_chan, -fs*seconds:]  # last N samples, in uV
    # FFT, 1-Hz bin width at 250-sample window
    spec = np.fft.rfft(sig * np.hanning(len(sig)))
    freqs = np.fft.rfftfreq(len(sig), 1.0/fs)
    bin_idx = np.argmin(np.abs(freqs - 31.5))
    amplitude_uV = (np.abs(spec[bin_idx]) * 2 / len(sig))
    amplitude_V = amplitude_uV * 1e-6
    z_ohm = amplitude_V / 6e-9
    return z_ohm
```

Emits kv-line per channel: `z_kohm_ch<i>=<val>` and `z_state_ch<i>=<G|Y|R>`.

## ASCII Rendering

Reuse existing 10-20 map layout in `electrode_adjustment_helper.hexa`
(unchanged geometry). Replace `[✓ ⚠ ✗ ⚡]` symbol map with colored `[●]`
glyphs using ANSI 24-bit codes. Falls back to ANSI 256-color when
`TERM=xterm` (no truecolor) and to plain `[G]/[Y]/[R]` when
`NO_COLOR=1` or piped to non-tty.

```
prefix = "\x1b[38;2;{r};{g};{b}m"
suffix = "\x1b[0m"
glyph  = prefix + "[●]" + suffix
```

Footer line per channel: `Fp1 ch1: 412 kΩ [GREEN]`.

## Refresh Strategy

Two modes (mutually exclusive):

1. **`--impedance` (one-shot sweep)** — default. Run full 16-ch sweep
   (~20 s), render, exit. Idiomatic for "I just put the helmet on, am I
   good?" check.
2. **`--impedance --watch`** — round-robin: 1 channel per second,
   re-render the full table after each channel updates. After 16 s
   one full pass completes; loop. Channels not yet visited in current
   pass keep their previous reading (or GRAY on first pass).
   Ctrl-C to stop. Cadence justified by the 1-s FFT window minimum.

Streaming MUST be stopped between channels (per
`W_CytonImpedance.pde:497-503` — board can only have one channel in
lead-off probe at a time without cross-talk).

## Falsifier (raw#71) — what would invalidate this implementation

A correct implementation MUST satisfy ALL of the following; failure on
any one is grounds for rollback:

1. **Known-good electrode** (saline-soaked, gel-bonded scalp pad):
   reads < 750 kΩ → GREEN. If implementation reads > 3 MΩ on a saline
   short, the FFT/conversion math is wrong.
2. **Open-air electrode** (lead detached, P-pin floating): reads
   > 3 MΩ → RED. If implementation reads < 750 kΩ on a literal open
   circuit, the lead-off probe is not actually being enabled.
3. **`config_board('z410Z')` round-trip:** when probed via verbose
   logging, board MUST acknowledge with `Success: Lead off set for 4$$$`
   when not streaming (per SDK doc § LeadOff). Absence indicates the
   command never reached the board (radio drop, wrong channel char).
4. **Channel separation:** measuring impedance on ch4 MUST NOT change
   the reading on ch5. If sweep run twice in opposite directions yields
   different per-channel values (> 20 % spread), there is bleed/cross-
   talk — likely a missing `z<CH>00Z` disable between channels.
5. **Probe-frequency presence:** with probe enabled, the FFT MUST show
   a clear peak at the 31.5 Hz bin that disappears when probe is
   disabled. If the 31.5 Hz bin amplitude is constant regardless of
   probe state, the probe was never injected (ADS1299 register write
   failed).

## Cost Estimate

| item | LoC | wallclock |
|---|---|---|
| hexa entry-point flag parse + dispatch | ~30 | 30 min |
| hexa kv-line consumer + state classify | ~60 | 1 h |
| hexa ASCII render w/ ANSI truecolor | ~80 | 1.5 h |
| `/tmp/` python helper (BrainFlow + FFT) | ~120 | 2 h |
| selftest (synthetic GREEN/YELLOW/RED triple) | ~50 | 45 min |
| smoke test on real Cyton+Daisy + falsifier 1+2 | (test only) | 1 h |
| docs (this file already exists) | 0 | 0 |

**Total impl LoC delta:** ~340 LoC added to `electrode_adjustment_helper.hexa`
(currently 1223 LoC → ~1560 LoC).
**Total wallclock:** ~6.5 h on dev machine + 1 h hardware smoke =
**~7.5 h** end-to-end for first-cycle land.

## Reference Gaps

None blocking. All five references (widget, state enum, board cmd,
SDK doc, firmware) provide sufficient detail for a clean port:

- The 31.5 Hz / 6 nA constants come from firmware
  (`OpenBCI_32bit_Library.cpp:794` — `LOFF_MAG_6NA, LOFF_FREQ_31p2HZ`),
  confirmed in SDK doc § LeadOff.
- The `z<CH><P><N>Z` grammar is fully spec'd in
  `BoardCyton.pde:430` and SDK doc.
- Channel char map (8 main + 8 Daisy with `Q W E R T Y U I`) is in
  SDK doc § "16 Channel Commands".
- Threshold values overridable; GUI defaults differ slightly from
  task-spec (2.5 MΩ vs 3 MΩ yellow→red boundary) — design adopts task
  spec, GUI value available via `--yellow-kohm 2500`.

**Minor caveat (non-blocking):** SDK doc rounds firmware's 31.2 Hz to
"31.5 Hz". FFT bin search uses `argmin(abs(freqs - 31.5))` which still
selects the correct bin at 250 Hz sampling (bin width 1 Hz, peak lies
between bin 31 and bin 32). Acceptable; document in code comment.
