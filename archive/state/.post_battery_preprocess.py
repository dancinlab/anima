#!/usr/bin/env python3
"""
post-battery preprocessor: produces 3 versions of the 16ch EEG segment:
  1) raw      : 16ch passthrough from BoardShim layout (rows[1..16])
  2) filtered : 1Hz HP + 50Hz notch + 0.5..50Hz bandpass (zero-phase)
  3) ICA      : 16-component FastICA, drop top-2 high-kurtosis components
                (artifact rejection proxy without manual labeling)

Outputs 16xN .npy files that the existing hexa tools can read directly
(load_npy infers 16ch when rows==N_CH).

raw#9 transient: .py helper, hexa orchestrates via wrapper if needed.
raw#10 honest: 60s @ 125Hz, single-subject, ICA artifact rejection by
       kurtosis heuristic (not manual visual inspection — operator-blind).
raw#82 darwin-native: scipy + scikit-learn FastICA in .venv-eeg.
"""
import os
import sys
import json
import numpy as np
from scipy.signal import iirnotch, butter, filtfilt

FS = 125.0
N_CH = 16
INPUT = "recordings/sessions/baseline_resting_post_battery_20260428T132612Z_seg000.npy"

OUT_DIR = "recordings/sessions"
OUT_RAW = os.path.join(OUT_DIR, "post_battery_raw_16ch_2026_04_28.npy")
OUT_FLT = os.path.join(OUT_DIR, "post_battery_filtered_16ch_2026_04_28.npy")
OUT_ICA = os.path.join(OUT_DIR, "post_battery_ica_16ch_2026_04_28.npy")
OUT_META = "state/post_battery_preprocess_meta_2026_04_28.json"


def load_16ch(path: str) -> np.ndarray:
    arr = np.load(path, allow_pickle=False)
    if arr.ndim != 2:
        raise SystemExit(f"expected 2-D, got ndim={arr.ndim}")
    rows, cols = arr.shape
    if rows == N_CH:
        return np.asarray(arr, dtype=np.float64)
    if cols == N_CH:
        return np.asarray(arr.T, dtype=np.float64)
    if rows >= 32 and cols > rows:
        return np.asarray(arr[1:17, :], dtype=np.float64)  # BrainFlow Cyton+Daisy
    if cols >= 32 and rows > cols:
        return np.asarray(arr.T[1:17, :], dtype=np.float64)
    raise SystemExit(f"cannot infer 16ch layout: shape={arr.shape}")


def filter_chain(eeg: np.ndarray) -> np.ndarray:
    """1Hz HP + 50Hz notch + 0.5..50Hz BP (zero-phase filtfilt)."""
    out = np.zeros_like(eeg)
    nyq = FS / 2.0
    # Notch 50Hz Q=30
    b_n, a_n = iirnotch(50.0 / nyq, Q=30.0)
    # Bandpass 0.5..50Hz, 4th-order Butterworth
    bp_lo, bp_hi = 0.5 / nyq, 50.0 / nyq
    b_bp, a_bp = butter(4, [bp_lo, bp_hi], btype="bandpass")
    for ch in range(eeg.shape[0]):
        x = eeg[ch].astype(np.float64)
        x = x - np.mean(x)
        y = filtfilt(b_n, a_n, x)
        y = filtfilt(b_bp, a_bp, y)
        out[ch] = y
    return out


def ica_artifact_reject(eeg: np.ndarray, n_drop: int = 2) -> tuple:
    """FastICA decomposition, drop top-`n_drop` components by absolute kurtosis.

    Returns (cleaned, dropped_indices, kurtosis_per_component).
    """
    try:
        from sklearn.decomposition import FastICA
    except ImportError as exc:
        raise SystemExit(f"missing-dep: sklearn.decomposition.FastICA: {exc!r}")
    from scipy.stats import kurtosis

    # Filter first (ICA on raw is not robust to drift), then decompose
    filt = filter_chain(eeg)
    n_ch, n_samp = filt.shape
    # FastICA expects (n_samples, n_features)
    X = filt.T
    ica = FastICA(n_components=n_ch, random_state=20260428,
                  whiten="unit-variance", max_iter=2000, tol=1e-4)
    S = ica.fit_transform(X)               # (n_samp, n_ch)  components in time
    A = ica.mixing_                        # (n_ch, n_ch)    mixing matrix
    # Kurtosis per component (Fisher = excess kurtosis). High |kurt| → eye-blink
    # / muscle / saccade artifact (super-Gaussian).
    kurts = np.array([kurtosis(S[:, i], fisher=True) for i in range(n_ch)])
    abs_k = np.abs(kurts)
    drop_idx = np.argsort(abs_k)[::-1][:n_drop].tolist()
    keep_S = S.copy()
    for di in drop_idx:
        keep_S[:, di] = 0.0
    # Reconstruct: x_hat = S A^T + mean
    cleaned = (keep_S @ A.T) + ica.mean_
    cleaned = cleaned.T                    # (n_ch, n_samp)
    return cleaned.astype(np.float64), drop_idx, kurts.tolist()


def main():
    if not os.path.isfile(INPUT):
        raise SystemExit(f"input-not-found: {INPUT}")
    eeg = load_16ch(INPUT)
    n_ch, n_samp = eeg.shape
    sys.stdout.write(f"loaded shape=({n_ch},{n_samp}) fs={FS} duration={n_samp/FS:.2f}s\n")

    # 1) raw 16ch
    np.save(OUT_RAW, eeg.astype(np.float64))
    # 2) filtered
    flt = filter_chain(eeg)
    np.save(OUT_FLT, flt.astype(np.float64))
    # 3) ICA
    ica, drop_idx, kurts = ica_artifact_reject(eeg, n_drop=2)
    np.save(OUT_ICA, ica.astype(np.float64))

    # Sanity: variance ratios
    var_raw = float(np.mean(np.var(eeg, axis=1)))
    var_flt = float(np.mean(np.var(flt, axis=1)))
    var_ica = float(np.mean(np.var(ica, axis=1)))

    meta = {
        "schema": "anima-clm-eeg/post_battery_preprocess/1",
        "input": INPUT,
        "fs_hz": FS,
        "n_ch": n_ch,
        "n_samp": n_samp,
        "duration_s": n_samp / FS,
        "outputs": {
            "raw":      OUT_RAW,
            "filtered": OUT_FLT,
            "ica":      OUT_ICA,
        },
        "filter_chain": {
            "notch_hz": 50.0,
            "notch_Q": 30.0,
            "bandpass_hz": [0.5, 50.0],
            "bp_order": 4,
            "method": "scipy.signal.filtfilt (zero-phase)",
        },
        "ica": {
            "n_components": n_ch,
            "n_drop": 2,
            "drop_indices": drop_idx,
            "kurtosis_per_component": [round(k, 3) for k in kurts],
            "selection_rule": "top-2 absolute Fisher-kurtosis (artifact proxy)",
            "raw10_honest": "kurtosis-heuristic, NOT manual visual inspection",
        },
        "variance_per_ch_mean": {
            "raw":      var_raw,
            "filtered": var_flt,
            "ica":      var_ica,
        },
    }
    with open(OUT_META, "w") as f:
        json.dump(meta, f, indent=2)
    sys.stdout.write(f"raw      → {OUT_RAW}\n")
    sys.stdout.write(f"filtered → {OUT_FLT}\n")
    sys.stdout.write(f"ica      → {OUT_ICA}\n")
    sys.stdout.write(f"meta     → {OUT_META}\n")
    sys.stdout.write(f"ica_drop_indices = {drop_idx}\n")
    sys.stdout.write(f"variance_mean raw={var_raw:.2f} flt={var_flt:.2f} ica={var_ica:.2f}\n")


if __name__ == "__main__":
    main()
