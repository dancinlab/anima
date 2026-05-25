#!/usr/bin/env python3
"""
sleep_staging_helper.py — anima T14 overnight sleep staging helper


  --record --duration-sec N --out <dir>
      Live continuous Cyton+Daisy capture into 60s .npy segments.
      Requires brainflow + Mac AC + caffeinate -i for the duration.

  --stage --recording <path> --audit <path>
      Post-hoc AASM 30s-epoch 5-state HMM (Wake/N1/N2/N3/REM) staging.
      Computes per-epoch bandpower (delta/theta/alpha/beta) + EOG +
      spindle density, fits Gaussian HMM, emits per-epoch JSONL with
      stage label and LZ76 score.

"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone


FS_HZ = 125
N_CH = 16
EPOCH_SEC = 30
SEGMENT_SEC = 60


def _ts_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _check_ac() -> bool:
    """own5 safety: must be on AC for 8h overnight."""
    try:
        import subprocess
        out = subprocess.check_output(["pmset", "-g", "batt"], text=True)
        return "AC Power" in out
    except Exception:
        return False


def cmd_record(duration_sec: int, out_dir: str) -> int:
    if not _check_ac():
        print("FATAL: not on AC power — overnight 8h aborted (own5).", file=sys.stderr)
        return 2
    os.makedirs(out_dir, exist_ok=True)
    n_seg = duration_sec // SEGMENT_SEC
    print(f"[{_ts_iso()}] sleep_staging_helper --record")
    print(f"  duration_sec={duration_sec}  n_segments={n_seg}")
    print(f"  out_dir={out_dir}")
    try:
        import numpy as np  # noqa
        from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds  # noqa
    except ImportError:
        print("WARN: brainflow / numpy not installed — dry-run stub only.")
        # write a marker so downstream --stage can still run on synth data
        marker = os.path.join(out_dir, datetime.now(timezone.utc).strftime("%Y%m%d") + "_overnight.marker")
        with open(marker, "w") as f:
            f.write(json.dumps({"mode": "dry_run_stub", "ts_iso": _ts_iso(),
                                "duration_sec": duration_sec, "n_seg": n_seg}) + "\n")
        return 0

    import numpy as np
    from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds

    params = BrainFlowInputParams()
    params.serial_port = os.environ.get("CYTON_PORT", "/dev/cu.usbserial-DM00Q4SS")
    board = BoardShim(BoardIds.CYTON_DAISY_BOARD.value, params)
    eeg_ch = BoardShim.get_eeg_channels(BoardIds.CYTON_DAISY_BOARD.value)

    board.prepare_session()
    board.start_stream()
    seg_samples = SEGMENT_SEC * FS_HZ
    date_tag = datetime.now(timezone.utc).strftime("%Y%m%d")
    out_path = os.path.join(out_dir, f"{date_tag}_overnight.npy")
    all_segments = []
    try:
        for seg_idx in range(n_seg):
            t0 = time.time()
            while time.time() - t0 < SEGMENT_SEC:
                time.sleep(0.5)
            data = board.get_current_board_data(seg_samples)  # (rows, samples)
            eeg = data[eeg_ch, :]  # (16, samples)
            all_segments.append(eeg.astype(np.float32))
            if seg_idx % 30 == 0:
                print(f"  seg {seg_idx}/{n_seg} captured  shape={eeg.shape}")
    finally:
        board.stop_stream()
        board.release_session()
    arr = np.stack(all_segments, axis=0)  # (n_seg, 16, samples)
    np.save(out_path, arr)
    print(f"  saved {out_path}  shape={arr.shape}")
    return 0


def _bandpower(x, fs, lo, hi):
    import numpy as np
    from scipy.signal import welch
    f, p = welch(x, fs=fs, nperseg=min(len(x), fs * 4))
    mask = (f >= lo) & (f <= hi)
    return float(np.trapz(p[mask], f[mask]))


def _lz76(x):
    """Kaspar-Schuster 1987 binary LZ76, normalized."""
    import numpy as np
    s = (x > np.median(x)).astype(int).tolist()
    n = len(s)
    i, c, l, k_max = 0, 1, 1, 1
    k = 1
    while True:
        if i + k > n - 1:
            c += 1
            break
        if s[i:i + k] == s[i + l:i + l + k]:
            k += 1
            if i + k > n - 1:
                c += 1
                break
        else:
            if k > k_max:
                k_max = k
            i += 1
            if i == l:
                c += 1
                l += k_max
                if l + 1 > n:
                    break
                i = 0
                k_max = 1
            k = 1
    norm = c * (max(1, n / max(1, (n / max(1, c)))))  # simple normalization
    return c / max(1, n / 8)  # rough x100 scale; replaced by anima-clm-eeg lz76 real


def cmd_stage(recording: str, audit: str) -> int:
    print(f"[{_ts_iso()}] sleep_staging_helper --stage")
    print(f"  recording={recording}")
    print(f"  audit={audit}")
    try:
        import numpy as np
        from hmmlearn.hmm import GaussianHMM
    except ImportError:
        print("WARN: numpy/hmmlearn not installed — emitting stub audit.")
        os.makedirs(os.path.dirname(audit), exist_ok=True)
        with open(audit, "w") as f:
            f.write(json.dumps({"mode": "stub", "ts_iso": _ts_iso(),
                                "recording": recording}) + "\n")
        return 0

    if not os.path.exists(recording):
        print(f"FATAL: recording not found: {recording}", file=sys.stderr)
        return 2
    arr = np.load(recording)  # (n_seg, 16, samples)
    n_seg = arr.shape[0]
    n_epochs = n_seg * (SEGMENT_SEC // EPOCH_SEC)
    print(f"  n_seg={n_seg}  n_epochs={n_epochs}")

    feats = []
    epoch_samples = EPOCH_SEC * FS_HZ
    for s in range(n_seg):
        seg = arr[s]  # (16, samples)
        for ep in range(SEGMENT_SEC // EPOCH_SEC):
            x = seg[:, ep * epoch_samples:(ep + 1) * epoch_samples]
            chan = x.mean(axis=0)
            d = _bandpower(chan, FS_HZ, 0.5, 4)
            t = _bandpower(chan, FS_HZ, 4, 8)
            a = _bandpower(chan, FS_HZ, 8, 13)
            b = _bandpower(chan, FS_HZ, 13, 30)
            sp = _bandpower(chan, FS_HZ, 12, 14)
            eog = float(np.std(x[0] - x[1]))  # Fp1-Fp2 differential
            feats.append([d, t, a, b, sp, eog])
    F = np.array(feats)
    Fz = (F - F.mean(0)) / (F.std(0) + 1e-9)

    hmm = GaussianHMM(n_components=5, covariance_type="diag", n_iter=50, random_state=42)
    hmm.fit(Fz)
    states = hmm.predict(Fz)
    # Map HMM states to AASM labels by mean delta power (highest -> N3,
    # lowest -> Wake / REM disambiguated by alpha)
    label_names = ["Wake", "N1", "N2", "N3", "REM"]
    delta_per_state = [F[states == k, 0].mean() if (states == k).any() else 0 for k in range(5)]
    order = np.argsort(delta_per_state)  # ascending delta
    state_to_label = {}
    state_to_label[order[0]] = "Wake"
    state_to_label[order[1]] = "REM"
    state_to_label[order[2]] = "N1"
    state_to_label[order[3]] = "N2"
    state_to_label[order[4]] = "N3"

    os.makedirs(os.path.dirname(audit), exist_ok=True)
    with open(audit, "w") as f:
        for ep_idx in range(len(states)):
            d, t, a, b, sp, eog = F[ep_idx]
            lz = _lz76(arr[ep_idx // (SEGMENT_SEC // EPOCH_SEC)].mean(axis=0))
            row = {
                "epoch_idx": int(ep_idx),
                "ts_iso": _ts_iso(),
                "stage": state_to_label[states[ep_idx]],
                "alpha_x1000": int(a * 1000),
                "theta_x1000": int(t * 1000),
                "delta_x1000": int(d * 1000),
                "beta_x1000": int(b * 1000),
                "spindle_x1000": int(sp * 1000),
                "eog_x1000": int(eog * 1000),
                "lz76_x1000": int(lz * 1000),
                "schema": "anima/sleep_staging/1",
            }
            f.write(json.dumps(row) + "\n")
    print(f"  audit written: {audit}  ({len(states)} epochs)")
    return 0


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--record", action="store_true")
    p.add_argument("--stage", action="store_true")
    p.add_argument("--duration-sec", type=int, default=28800)
    p.add_argument("--out", default="state/sleep_recordings")
    p.add_argument("--recording", default="")
    p.add_argument("--audit", default="")
    args = p.parse_args()

    if args.record:
        return cmd_record(args.duration_sec, args.out)
    if args.stage:
        if not args.recording or not args.audit:
            print("FATAL: --stage requires --recording and --audit", file=sys.stderr)
            return 2
        return cmd_stage(args.recording, args.audit)
    p.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
