#!/usr/bin/env python3
"""v6 Berger EC/EO clean-channel reanalysis (rail-corrected F1/F2/F3).

Context:
    OpenBCI Cyton+Daisy 16ch capture (post-IOSSDATALAT fix, ~120 Hz PHENOMENAL).
    Original v6 measurement showed F3 (alpha-blocking) FAIL, but channel-mapping
    audit identified rail saturation in 5/16 channels. This script re-runs the
    Berger F1/F2/F3 verdicts using ONLY the 11 clean channels.

    not part of the measurement chain).
    illustrative, not population-statistical.

Channel mapping (1-indexed, matches BrainFlow eeg_indices in meta):
    row 0       = sample counter (skipped)
    rows 1-16   = EEG (Cyton+Daisy)
        row 1 = Fp1, row 2 = Fp2, ..., row 7 = O1, row 8 = O2, ...
    rows 17-31  = aux/timestamp/marker (skipped)

Rail-saturated rows (drop): {1, 5, 6, 8, 16}
Clean rows:                 [2, 3, 4, 7, 9, 10, 11, 12, 13, 14, 15]  (11/16)

Usage:
    python3 v6_clean_reanalyze.py \\
        --ec /path/to/berger_ec_60s_v6_2026_05_03.npy \\
        --eo /path/to/berger_eo_60s_v6_2026_05_03.npy \\
        --out /path/to/state/berger_v6_clean_reanalyze_2026_05_03/
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.signal import butter, sosfiltfilt, welch

# ------------------------------------------------------------------ constants

FS = 120.0  # Hz, post-IOSSDATALAT effective rate
HPF_HZ = 0.5
HPF_ORDER = 4
ALPHA_LO = 7.5
ALPHA_HI = 12.5
NPERSEG = 128
NOVERLAP = 64

# 1-indexed row IDs (matches meta.eeg_indices); numpy index == row ID since
# row 0 is the sample counter.
RAILED_ROWS = [1, 5, 6, 8, 16]
CLEAN_CHANNELS = [2, 3, 4, 7, 9, 10, 11, 12, 13, 14, 15]

# Subset of standard 10-20 names assumed for Cyton+Daisy default montage.
# (Spec only fixes O1=row7, O2=row8, Fp1=row1; rest are inferred for plot
# labelling and are not load-bearing for verdicts.)
ROW_LABELS = {
    1: "Fp1",
    2: "Fp2",
    3: "C3",
    4: "C4",
    5: "T5",
    6: "T6",
    7: "O1",
    8: "O2",
    9: "F7",
    10: "F8",
    11: "F3",
    12: "F4",
    13: "T3",
    14: "T4",
    15: "P3",
    16: "P4",
}

# Verdict-relevant rows
O1_ROW = 7
O2_ROW = 8
FP1_ROW = 1
FP2_ROW = 2



# ------------------------------------------------------------------ pipeline


def load_npy(path: Path) -> np.ndarray:
    """Load BrainFlow board_data .npy and return rows 1..16 only (EEG)."""
    arr = np.load(path)
    if arr.shape[0] < 17:
        raise ValueError(f"{path}: expected >=17 rows, got {arr.shape[0]}")
    return arr  # caller selects rows


def hpf(x: np.ndarray, fs: float = FS, fc: float = HPF_HZ, order: int = HPF_ORDER) -> np.ndarray:
    """Zero-phase Butterworth high-pass per-channel (DC + drift removal)."""
    sos = butter(order, fc / (fs / 2.0), btype="highpass", output="sos")
    return sosfiltfilt(sos, x, axis=-1)


def welch_psd(x: np.ndarray, fs: float = FS) -> tuple[np.ndarray, np.ndarray]:
    f, psd = welch(
        x,
        fs=fs,
        window="hann",
        nperseg=NPERSEG,
        noverlap=NOVERLAP,
        axis=-1,
        scaling="density",
    )
    return f, psd


def alpha_power(f: np.ndarray, psd: np.ndarray) -> np.ndarray:
    """Integrate PSD over [ALPHA_LO, ALPHA_HI] Hz (trapezoid). Last axis = freq."""
    mask = (f >= ALPHA_LO) & (f <= ALPHA_HI)
    f_alpha = f[mask]
    psd_alpha = psd[..., mask]
    # numpy>=2.0 renames trapz -> trapezoid; fall back for older numpy
    _trap = getattr(np, "trapezoid", getattr(np, "trapz", None))
    return _trap(psd_alpha, f_alpha, axis=-1)


def alpha_peak_in_band(f: np.ndarray, psd_1d: np.ndarray) -> tuple[float, float]:
    mask = (f >= ALPHA_LO) & (f <= ALPHA_HI)
    fb = f[mask]
    pb = psd_1d[mask]
    idx = int(np.argmax(pb))
    return float(fb[idx]), float(pb[idx])


# ------------------------------------------------------------------ verdicts


def verdict_f1(f: np.ndarray, psd_ec: np.ndarray, rows: list[int], log: list[str]) -> dict:
    """F1: alpha peak between 7.5-12.5 Hz at occipital (O1, O2 if not railed)."""
    occ_rows = []
    if O1_ROW in rows:
        occ_rows.append(O1_ROW)
    if O2_ROW in rows:
        occ_rows.append(O2_ROW)
    if not occ_rows:
        log.append("F1: no occipital channel available (both O1+O2 railed) -> FAIL")
        return {"status": "FAIL", "reason": "no_occipital_clean", "channels": []}

    per_ch = {}
    any_peak = False
    for r in occ_rows:
        ch_idx = rows.index(r)
        peak_f, peak_p = alpha_peak_in_band(f, psd_ec[ch_idx])
        # require true local-max (peak > median of band)
        mask = (f >= ALPHA_LO) & (f <= ALPHA_HI)
        med = float(np.median(psd_ec[ch_idx][mask]))
        is_peak = peak_p > med * 1.2  # mild prominence
        per_ch[ROW_LABELS.get(r, f"row{r}")] = {
            "peak_hz": peak_f,
            "peak_psd": peak_p,
            "band_median_psd": med,
            "is_peak": bool(is_peak),
        }
        any_peak = any_peak or is_peak
        log.append(
            f"F1: {ROW_LABELS.get(r, f'row{r}')} EC peak={peak_f:.2f}Hz "
            f"psd={peak_p:.3e} band_med={med:.3e} prominent={is_peak}"
        )

    status = "PASS" if any_peak else "FAIL"
    return {"status": status, "channels": per_ch, "occipital_rows_used": occ_rows}


def verdict_f2(
    f: np.ndarray,
    psd_ec: np.ndarray,
    ap_ec: np.ndarray,
    rows: list[int],
    log: list[str],
) -> dict:
    """F2: occipital alpha > frontal alpha (Fp2 standin since Fp1 railed)."""
    occ_rows = [r for r in (O1_ROW, O2_ROW) if r in rows]
    front_rows = [r for r in (FP1_ROW, FP2_ROW) if r in rows]
    if not occ_rows or not front_rows:
        log.append(f"F2: insufficient channels occ={occ_rows} front={front_rows} -> FAIL")
        return {"status": "FAIL", "reason": "missing_occ_or_front"}

    occ_ap = float(np.mean([ap_ec[rows.index(r)] for r in occ_rows]))
    front_ap = float(np.mean([ap_ec[rows.index(r)] for r in front_rows]))
    ratio = occ_ap / front_ap if front_ap > 0 else float("inf")
    status = "PASS" if occ_ap > front_ap else "FAIL"
    log.append(
        f"F2: occ_alpha_mean({[ROW_LABELS[r] for r in occ_rows]})={occ_ap:.4e} "
        f"front_alpha_mean({[ROW_LABELS[r] for r in front_rows]})={front_ap:.4e} "
        f"ratio={ratio:.3f} -> {status}"
    )
    return {
        "status": status,
        "occipital_rows": occ_rows,
        "frontal_rows": front_rows,
        "occipital_alpha_mean": occ_ap,
        "frontal_alpha_mean": front_ap,
        "ratio_occ_over_front": ratio,
    }


def verdict_f3(
    ap_ec: np.ndarray,
    ap_eo: np.ndarray,
    rows: list[int],
    log: list[str],
) -> dict:
    """F3: alpha-blocking — EC occipital alpha > EO occipital alpha * 2.0.

    """
    occ_rows = [r for r in (O1_ROW, O2_ROW) if r in rows]
    if not occ_rows:
        log.append("F3: no occipital clean channel -> FAIL")
        return {"status": "FAIL", "reason": "no_occipital_clean"}

    per_ch = {}
    any_pass = False
    all_pass = True
    for r in occ_rows:
        i = rows.index(r)
        ec_a = float(ap_ec[i])
        eo_a = float(ap_eo[i])
        ratio = ec_a / eo_a if eo_a > 0 else float("inf")
        ch_pass = ratio > F3_THRESHOLD
        any_pass = any_pass or ch_pass
        all_pass = all_pass and ch_pass
        per_ch[ROW_LABELS.get(r, f"row{r}")] = {
            "ec_alpha": ec_a,
            "eo_alpha": eo_a,
            "ratio_ec_over_eo": ratio,
            "passes_2x": bool(ch_pass),
        }
        log.append(
            f"F3: {ROW_LABELS.get(r, f'row{r}')} EC={ec_a:.4e} EO={eo_a:.4e} "
            f"ratio={ratio:.3f} threshold={F3_THRESHOLD} pass={ch_pass}"
        )

    if all_pass:
        status = "PASS"
    elif any_pass:
        status = "PARTIAL"
    else:
        status = "FAIL"
    return {
        "status": status,
        "threshold": F3_THRESHOLD,
        "channels": per_ch,
        "occipital_rows": occ_rows,
    }


def compute_tier(f1: dict, f2: dict, f3: dict) -> str:
    statuses = [f1["status"], f2["status"], f3["status"]]
    n_pass = sum(s == "PASS" for s in statuses)
    n_fail = sum(s == "FAIL" for s in statuses)
    if n_pass == 3:
        return "full"
    if n_pass >= 2 and n_fail <= 1:
        return "functional"
    return "analog"


# ------------------------------------------------------------------ plotting


def plot_psd_clean(
    f: np.ndarray,
    psd_ec: np.ndarray,
    psd_eo: np.ndarray,
    rows: list[int],
    out_path: Path,
) -> None:
    n = len(rows)
    ncols = 4
    nrows = (n + ncols - 1) // ncols
    fig, axes = plt.subplots(nrows, ncols, figsize=(4 * ncols, 2.5 * nrows), sharex=True)
    axes = np.atleast_2d(axes).reshape(nrows, ncols)
    for i, r in enumerate(rows):
        ax = axes[i // ncols][i % ncols]
        ax.semilogy(f, psd_ec[i], label="EC", color="C0", lw=1.0)
        ax.semilogy(f, psd_eo[i], label="EO", color="C3", lw=1.0)
        ax.axvspan(ALPHA_LO, ALPHA_HI, color="gold", alpha=0.18, label="alpha")
        ax.set_xlim(0, 40)
        ax.set_title(f"row {r} ({ROW_LABELS.get(r, '?')})", fontsize=9)
        ax.tick_params(labelsize=8)
        if i == 0:
            ax.legend(fontsize=7, loc="upper right")
    # blank unused
    for j in range(n, nrows * ncols):
        axes[j // ncols][j % ncols].axis("off")
    fig.suptitle("v6 Berger PSD - clean channels (11/16) - HPF 0.5Hz, Welch nperseg=128", fontsize=11)
    fig.supxlabel("Frequency (Hz)")
    fig.supylabel("PSD (uV^2/Hz)")
    fig.tight_layout()
    fig.savefig(out_path, dpi=130)
    plt.close(fig)


def plot_o1_only(
    f: np.ndarray,
    psd_ec_o1: np.ndarray,
    psd_eo_o1: np.ndarray,
    out_path: Path,
) -> None:
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.semilogy(f, psd_ec_o1, label="EC O1 (row 7)", color="C0", lw=1.4)
    ax.semilogy(f, psd_eo_o1, label="EO O1 (row 7)", color="C3", lw=1.4)
    ax.axvspan(ALPHA_LO, ALPHA_HI, color="gold", alpha=0.20, label="alpha 7.5-12.5 Hz")
    ax.set_xlim(0, 40)
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("PSD (uV^2/Hz)")
    ax.set_title("v6 Berger - O1 (row 7) EC vs EO - rail-corrected")
    ax.legend()
    ax.grid(True, which="both", alpha=0.3)
    fig.tight_layout()
    fig.savefig(out_path, dpi=130)
    plt.close(fig)


# ------------------------------------------------------------------ main


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--ec", required=True, type=Path)
    p.add_argument("--eo", required=True, type=Path)
    p.add_argument("--out", required=True, type=Path)
    args = p.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    log: list[str] = []
    log.append(f"v6 clean-channel reanalyze | fs={FS}Hz | HPF={HPF_HZ}Hz/order{HPF_ORDER}")
    log.append(f"clean_channels (1-indexed)={CLEAN_CHANNELS}  railed={RAILED_ROWS}")
    log.append(f"EC npy: {args.ec}")
    log.append(f"EO npy: {args.eo}")

    ec_full = load_npy(args.ec)
    eo_full = load_npy(args.eo)
    log.append(f"EC shape={ec_full.shape}  EO shape={eo_full.shape}")

    # extract clean rows; numpy index == row ID since row 0 is sample counter
    ec = ec_full[CLEAN_CHANNELS, :]
    eo = eo_full[CLEAN_CHANNELS, :]
    log.append(f"EC clean shape={ec.shape}  EO clean shape={eo.shape}")
    log.append(
        f"N samples EC={ec.shape[1]} ({ec.shape[1]/FS:.2f}s)  "
        f"EO={eo.shape[1]} ({eo.shape[1]/FS:.2f}s)"
    )

    # HPF then Welch
    ec_hp = hpf(ec)
    eo_hp = hpf(eo)
    f_ec, psd_ec = welch_psd(ec_hp)
    f_eo, psd_eo = welch_psd(eo_hp)
    assert np.allclose(f_ec, f_eo), "freq grids must match"
    f = f_ec
    log.append(f"Welch nperseg={NPERSEG} noverlap={NOVERLAP}  freq bins={f.shape[0]} "
               f"df={(f[1]-f[0]):.4f}Hz  fmax={f[-1]:.2f}Hz")

    ap_ec = alpha_power(f, psd_ec)
    ap_eo = alpha_power(f, psd_eo)
    for i, r in enumerate(CLEAN_CHANNELS):
        log.append(
            f"  alpha row{r:2d} ({ROW_LABELS.get(r,'?'):>3}): "
            f"EC={ap_ec[i]:.4e}  EO={ap_eo[i]:.4e}  ratio={ap_ec[i]/max(ap_eo[i],1e-30):.3f}"
        )

    # Verdicts
    log.append("--- F1 (alpha peak) ---")
    f1 = verdict_f1(f, psd_ec, CLEAN_CHANNELS, log)
    log.append("--- F2 (occipital > frontal) ---")
    f2 = verdict_f2(f, psd_ec, ap_ec, CLEAN_CHANNELS, log)
    log.append("--- F3 (alpha-blocking EC > EO * 2) ---")
    f3 = verdict_f3(ap_ec, ap_eo, CLEAN_CHANNELS, log)

    tier = compute_tier(f1, f2, f3)
    log.append(f"=== TIER (rail-corrected): {tier} ===")
    log.append(f"verdicts: F1={f1['status']}  F2={f2['status']}  F3={f3['status']}")

    if f3["status"] == "FAIL":
        log.append(
            "alpha-blocking discriminator unstable. "
            "Next-cycle prereq: electrode contact re-seat (esp. O1, occipital), "
            "reference electrode check."
        )

    # outputs
    np.savez(
        args.out / "welch_clean.npz",
        f=f,
        psd_ec=psd_ec,
        psd_eo=psd_eo,
        ap_ec=ap_ec,
        ap_eo=ap_eo,
        clean_channels=np.array(CLEAN_CHANNELS, dtype=int),
        railed_rows=np.array(RAILED_ROWS, dtype=int),
        labels=np.array([ROW_LABELS.get(r, f"row{r}") for r in CLEAN_CHANNELS]),
    )

    verdict = {
        "schema": "anima-eeg/berger_clean_reanalyze/1",
        "version": "v6_clean_2026_05_03",
        "fs_hz": FS,
        "hpf_hz": HPF_HZ,
        "alpha_band_hz": [ALPHA_LO, ALPHA_HI],
        "welch": {"nperseg": NPERSEG, "noverlap": NOVERLAP, "window": "hann"},
        "ec_npy": str(args.ec),
        "eo_npy": str(args.eo),
        "ec_shape": list(ec_full.shape),
        "eo_shape": list(eo_full.shape),
        "n_samples_ec": int(ec.shape[1]),
        "n_samples_eo": int(eo.shape[1]),
        "duration_ec_s": float(ec.shape[1] / FS),
        "duration_eo_s": float(eo.shape[1] / FS),
        "clean_channels_1idx": CLEAN_CHANNELS,
        "railed_rows_1idx": RAILED_ROWS,
        "n_channels_clean": len(CLEAN_CHANNELS),
        "alpha_power_ec": {ROW_LABELS.get(r, f"row{r}"): float(ap_ec[i])
                           for i, r in enumerate(CLEAN_CHANNELS)},
        "alpha_power_eo": {ROW_LABELS.get(r, f"row{r}"): float(ap_eo[i])
                           for i, r in enumerate(CLEAN_CHANNELS)},
        "f1_alpha_peak": f1,
        "f2_occ_gt_front": f2,
        "f3_alpha_blocking": f3,
        "tier": tier,
        "f3_threshold_fixed": F3_THRESHOLD,
        "raw9_concession": "analysis-only script under anima-eeg/scripts/",
        "raw10_honest_c3": "N=1 single-subject single-session; verdicts illustrative",
        "raw71_falsifier_bound": "F3 threshold fixed at 2.0; not relaxed",
    }
    with open(args.out / "verdict.json", "w") as fp:
        json.dump(verdict, fp, indent=2)

    plot_psd_clean(f, psd_ec, psd_eo, CLEAN_CHANNELS, args.out / "psd_clean_11ch.png")
    if O1_ROW in CLEAN_CHANNELS:
        i = CLEAN_CHANNELS.index(O1_ROW)
        plot_o1_only(f, psd_ec[i], psd_eo[i], args.out / "psd_o1_only.png")
    else:
        log.append("O1 (row 7) not in clean channels -- skipping psd_o1_only.png")

    with open(args.out / "analysis_log.txt", "w") as fp:
        fp.write("\n".join(log) + "\n")

    print("\n".join(log))
    print(f"\nWrote: {args.out}/welch_clean.npz")
    print(f"Wrote: {args.out}/verdict.json")
    print(f"Wrote: {args.out}/psd_clean_11ch.png")
    print(f"Wrote: {args.out}/psd_o1_only.png")
    print(f"Wrote: {args.out}/analysis_log.txt")


if __name__ == "__main__":
    main()
