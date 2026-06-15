#!/usr/bin/env python3
"""EEG_CLM/capture_eeg.py — OpenBCI Cyton+Daisy (UltraCortex Mk IV) capture → channel-major flat recording.

Writes the format build_eeg_clm.hexa / tension_link.hexa expect:
    # n_ch n_samp
    <float>            # channel-major: s[ch*n_samp + t]
    ...

Usage:
    # real headset (find port: ls /dev/cu.usbserial-*)
    python3 EEG_CLM/capture_eeg.py --serial /dev/cu.usbserial-XXXX --seconds 8 --out EEG_CLM/eeg_recording.txt
    # no hardware (brainflow synthetic board — for pipeline test)
    python3 EEG_CLM/capture_eeg.py --synthetic --seconds 8
    # pure-numpy synthetic (no brainflow at all — always works)
    python3 EEG_CLM/capture_eeg.py --fake --seconds 8

Default channels = 4 midline-ish (indices 0..3 of the EEG channel list); override with --channels 0,1,2,3.
n_ch <= 8 keeps the CLM state alphabet (2^n_ch) usable; 4 → 16 states (matches a7 Fz/Cz/Pz/Oz).
"""
import argparse, sys, math


def write_recording(out_path, data, ch_idx, n_samp):
    """data: list-of-lists [channel][t]; ch_idx: selected channel indices."""
    n_ch = len(ch_idx)
    with open(out_path, "w") as f:
        f.write(f"# {n_ch} {n_samp}\n")
        for ci in ch_idx:                       # channel-major: all of ch0, then ch1, ...
            row = data[ci]
            for t in range(n_samp):
                f.write(f"{row[t]:.4f}\n")
    print(f"[capture] wrote {n_ch}ch x {n_samp}samp -> {out_path}")


def fake_capture(seconds, fs, n_ch):
    """pure-numpy-free deterministic synthetic EEG (alpha + noise), no deps."""
    n_samp = int(seconds * fs)
    data = []
    for ci in range(max(8, n_ch)):
        row = []
        f_alpha = 8.0 + ci * 1.5            # distinct rhythm per channel
        for t in range(n_samp):
            tt = t / fs
            v = 30.0 * math.sin(2 * math.pi * f_alpha * tt)
            v += 12.0 * math.sin(2 * math.pi * (2.0 + ci) * tt)   # slow drift
            v += 6.0 * math.sin(2 * math.pi * 40.0 * tt + ci)     # gamma-ish
            # deterministic pseudo-noise (no RNG)
            v += 4.0 * math.sin(t * (0.7 + 0.13 * ci) + ci * 2.1)
            row.append(v)
        data.append(row)
    return data, n_samp


def brainflow_capture(serial, synthetic, seconds):
    from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds
    import time
    params = BrainFlowInputParams()
    if synthetic:
        board_id = BoardIds.SYNTHETIC_BOARD.value
    else:
        board_id = BoardIds.CYTON_DAISY_BOARD.value     # Cyton+Daisy = 16ch
        params.serial_port = serial
    fs = BoardShim.get_sampling_rate(board_id)
    eeg_ch = BoardShim.get_eeg_channels(board_id)
    board = BoardShim(board_id, params)
    board.prepare_session()
    board.start_stream()
    print(f"[capture] streaming {seconds}s @ {fs}Hz board={board_id} ...")
    time.sleep(seconds)
    raw = board.get_board_data()
    board.stop_stream(); board.release_session()
    data = [list(raw[c]) for c in eeg_ch]      # [channel][t]
    n_samp = len(data[0])
    return data, n_samp, fs, list(range(len(eeg_ch)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--serial", default=None, help="serial port of the Cyton dongle")
    ap.add_argument("--synthetic", action="store_true", help="brainflow synthetic board")
    ap.add_argument("--fake", action="store_true", help="pure-python synthetic (no brainflow)")
    ap.add_argument("--seconds", type=float, default=8.0)
    ap.add_argument("--channels", default="0,1,2,3", help="comma channel indices (<=8)")
    ap.add_argument("--out", default="EEG_CLM/eeg_recording.txt")
    a = ap.parse_args()
    ch_idx = [int(x) for x in a.channels.split(",")]
    if len(ch_idx) > 8:
        print("[warn] >8 channels → 2^n state alphabet too large; truncating to 8")
        ch_idx = ch_idx[:8]

    if a.fake:
        data, n_samp = fake_capture(a.seconds, 125.0, len(ch_idx))
    else:
        try:
            data, n_samp, fs, all_idx = brainflow_capture(a.serial, a.synthetic, a.seconds)
        except Exception as e:
            print(f"[capture] brainflow unavailable ({e}); falling back to --fake", file=sys.stderr)
            data, n_samp = fake_capture(a.seconds, 125.0, len(ch_idx))

    write_recording(a.out, data, ch_idx, n_samp)


if __name__ == "__main__":
    main()
