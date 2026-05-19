#!/usr/bin/env python3
"""
SLM Phase 3 cond.C1 — Real-data TRF on ZuCo ZAB SR1
Replaces mock-EEG fixture (Pearson r=0.225 planted at lag 120ms)
with real ZuCo ZAB SR1 measurement.

Pipeline:
  1. Load EEG (gip_ZAB_SR1_EEG.mat, HDF5 v7.3) — 105ch x 122182 samples @ 500Hz
  2. Load ET fixations (ZAB_SR1_corrected_ET.mat, scipy.io v5)
  3. Align ET-time → EEG-sample via shared event 100 anchor
  4. Build word-fixation onset spike train (1 spike per fixation start)
  5. TRF: lag-sweep Pearson r between EEG-band-envelope and fixation regressor
  6. Auditory ROI (EGI 128 → T7/T8/P7/P8 ≈ E45/E108/E58/E96)
  7. F-SLM-C1 falsifier: Pearson r >= 0.15 (Brennan-Hale 2019 baseline)
"""
import json
import sys
import time
from pathlib import Path
import numpy as np
import h5py
import scipy.io as sio
from scipy.signal import butter, filtfilt, hilbert

t0 = time.time()
DATA_DIR = Path('/tmp/zuco_sample/ZAB_task1_SR_preprocessed')
EEG_FILE = DATA_DIR / 'gip_ZAB_SR1_EEG.mat'
ET_FILE = DATA_DIR / 'ZAB_SR1_corrected_ET.mat'
OUT = Path('/tmp/slm_p3_c1_zuco_real/results.json')
OUT.parent.mkdir(parents=True, exist_ok=True)

FS_HZ = 500
LAG_SWEEP_MS = list(range(60, 501, 20))  # 60..500 in 20ms steps
# Auditory ROI: T7/T8/P7/P8 region in EGI HydroCel 128 → roughly E45/E108/E58/E96.
# We also include adjacent channels for robustness (E40/E41/E45/E46 left-temp; E102/E108/E114/E115 right-temp)
AUDITORY_ROI = ['E45', 'E108', 'E58', 'E96', 'E40', 'E46', 'E102']
# Bandpass for speech-tracking (delta-theta, 1-8Hz typical for word-rate)
BAND_LOW, BAND_HIGH = 1.0, 8.0


def load_eeg():
    f = h5py.File(EEG_FILE, 'r')
    eeg = f['EEG']
    data = np.array(eeg['data'])  # (122182, 105) float32
    srate = float(np.array(eeg['srate']).flatten()[0])
    # channel labels
    chanlocs = eeg['chanlocs']
    labels_ref = chanlocs['labels']
    labels = []
    for i in range(labels_ref.shape[0]):
        ref = labels_ref[i, 0]
        obj = f[ref]
        s = ''.join(chr(c[0]) for c in np.array(obj))
        labels.append(s)
    # events
    event = eeg['event']
    type_refs = event['type']
    lat_refs = event['latency']
    types, lats = [], []
    for i in range(type_refs.shape[0]):
        s = ''.join(chr(c[0]) for c in np.array(f[type_refs[i, 0]])).strip()
        types.append(s)
        lats.append(float(np.array(f[lat_refs[i, 0]]).flatten()[0]))
    f.close()
    return data, srate, labels, types, lats


def load_et():
    d = sio.loadmat(ET_FILE)
    fix_inner = d['eyeevent']['fixations'][0, 0]
    fix_data = fix_inner['data'][0, 0]  # (N, 6) latency,endtime,duration,x,y,pupil
    events = d['event']  # (N, 2) ET-time, code
    et_data_time = d['data'][:, 0]  # (T,) ET timeline
    return fix_data, events, et_data_time


def main():
    print(f'[{time.time()-t0:.1f}s] Loading EEG ...', flush=True)
    eeg_data, srate, labels, ev_types, ev_lats = load_eeg()
    print(f'  EEG shape={eeg_data.shape} srate={srate} channels={len(labels)}')
    print(f'  Events: {len(ev_types)} (first type={ev_types[0]} @ samp {ev_lats[0]})')

    print(f'[{time.time()-t0:.1f}s] Loading ET ...', flush=True)
    fix_data, et_events, et_data_time = load_et()
    print(f'  Fixations: {fix_data.shape[0]}')
    print(f'  ET events: {et_events.shape[0]} (first code={et_events[0,1]} @ {et_events[0,0]})')

    # === Time alignment via event code 100 anchor ===
    # EEG: code 100 is at sample ev_lats[0] (typically 24)
    # ET:  first event with code 100 in et_events
    eeg_anchor_sample = None
    for t_, l_ in zip(ev_types, ev_lats):
        if t_ == '100':
            eeg_anchor_sample = l_
            break
    et_anchor_time = None
    for r in et_events:
        if r[1] == 100:
            et_anchor_time = float(r[0])
            break
    assert eeg_anchor_sample is not None and et_anchor_time is not None, 'No 100 anchor'
    print(f'  Anchor: ET_time={et_anchor_time} ↔ EEG_sample={eeg_anchor_sample}')
    # ET clock is 1ms units, EEG sample at 500Hz → 1 sample = 2ms
    # eeg_sample = eeg_anchor + (et_time - et_anchor) / 2

    def et_to_eeg_sample(et_time):
        return int(round(eeg_anchor_sample + (et_time - et_anchor_time) / 2.0))

    # === Build fixation-onset spike train (impulse regressor) ===
    n_eeg = eeg_data.shape[0]
    spike = np.zeros(n_eeg, dtype=np.float64)
    fix_starts = fix_data[:, 0]  # latency col
    fix_durs = fix_data[:, 2]  # duration
    in_range = 0
    for s in fix_starts:
        idx = et_to_eeg_sample(float(s))
        if 0 <= idx < n_eeg:
            spike[idx] = 1.0
            in_range += 1
    print(f'  Fixation spikes placed in EEG range: {in_range}/{len(fix_starts)}')

    # === Bandpass filter EEG to delta-theta (1-8Hz) ===
    print(f'[{time.time()-t0:.1f}s] Bandpass filter {BAND_LOW}-{BAND_HIGH} Hz ...', flush=True)
    nyq = srate / 2.0
    b, a = butter(4, [BAND_LOW / nyq, BAND_HIGH / nyq], btype='band')
    eeg_bp = filtfilt(b, a, eeg_data.astype(np.float64), axis=0)
    # Envelope via Hilbert
    eeg_env = np.abs(hilbert(eeg_bp, axis=0))

    # Also smooth spike to a low-rate envelope for fair comparison
    # Use a Gaussian smoothing over ~50ms (25 samples at 500Hz)
    from scipy.ndimage import gaussian_filter1d
    spike_smooth = gaussian_filter1d(spike, sigma=12.5)  # ~25ms FWHM

    # === Lag sweep TRF Pearson r ===
    print(f'[{time.time()-t0:.1f}s] Computing TRF lag-sweep ...', flush=True)
    n_lags = len(LAG_SWEEP_MS)
    n_ch = eeg_env.shape[1]
    r_matrix = np.zeros((n_ch, n_lags), dtype=np.float64)
    for li, lag_ms in enumerate(LAG_SWEEP_MS):
        lag_samp = int(round(lag_ms * srate / 1000.0))
        if lag_samp >= n_eeg:
            continue
        # Shift spike forward by lag (EEG response trails the stimulus)
        x = spike_smooth[:n_eeg - lag_samp]
        for ci in range(n_ch):
            y = eeg_env[lag_samp:, ci]
            if x.std() > 0 and y.std() > 0:
                r_matrix[ci, li] = float(np.corrcoef(x, y)[0, 1])

    # === Per-channel peak r ===
    per_ch = {}
    for ci, lab in enumerate(labels):
        peak_li = int(np.argmax(np.abs(r_matrix[ci, :])))
        per_ch[lab] = {
            'peak_lag_ms': LAG_SWEEP_MS[peak_li],
            'peak_r': float(r_matrix[ci, peak_li]),
            'r_at_120ms': float(r_matrix[ci, LAG_SWEEP_MS.index(120)]),
            'is_auditory_roi': lab in AUDITORY_ROI,
        }

    # === Aggregate ROI vs non-ROI ===
    aud_idx = [ci for ci, lab in enumerate(labels) if lab in AUDITORY_ROI]
    nonaud_idx = [ci for ci, lab in enumerate(labels) if lab not in AUDITORY_ROI]
    aud_peaks = [np.max(np.abs(r_matrix[ci, :])) for ci in aud_idx]
    nonaud_peaks = [np.max(np.abs(r_matrix[ci, :])) for ci in nonaud_idx]
    aud_lags = [LAG_SWEEP_MS[int(np.argmax(np.abs(r_matrix[ci, :])))] for ci in aud_idx]

    aggregate = {
        'auditory_roi_channels_found': [labels[ci] for ci in aud_idx],
        'auditory_peak_r_mean': float(np.mean(aud_peaks)) if aud_peaks else None,
        'auditory_peak_r_std': float(np.std(aud_peaks)) if aud_peaks else None,
        'auditory_peak_r_max': float(np.max(aud_peaks)) if aud_peaks else None,
        'nonauditory_peak_r_mean': float(np.mean(nonaud_peaks)),
        'nonauditory_peak_r_std': float(np.std(nonaud_peaks)),
        'nonauditory_peak_r_max': float(np.max(nonaud_peaks)),
        'auditory_peak_lag_ms_mean': float(np.mean(aud_lags)) if aud_lags else None,
        'global_peak_r': float(np.max(np.abs(r_matrix))),
        'global_peak_channel': labels[int(np.argmax(np.max(np.abs(r_matrix), axis=1)))],
    }

    # === F-SLM-C1 verdict ===
    floor = 0.15
    aud_max = aggregate['auditory_peak_r_max'] or 0
    aud_mean = aggregate['auditory_peak_r_mean'] or 0
    global_max = aggregate['global_peak_r']
    verdict = {
        'floor_threshold': floor,
        'auditory_roi_max_r': aud_max,
        'auditory_roi_mean_r': aud_mean,
        'global_max_r': global_max,
        'PASS_auditory_max': aud_max >= floor,
        'PASS_auditory_mean': aud_mean >= floor,
        'PASS_global_max': global_max >= floor,
        'verdict_label': 'PASS' if aud_mean >= floor else 'FAIL',
    }

    out = {
        'axis': 'P3.C1',
        'name': 'TRF real-EEG ZuCo ZAB SR1 + Pearson r lag-sweep',
        'mode': 'real_data_zuco_zab_sr1',
        'corpus': 'ZuCo task1-SR (sentiment-reading)',
        'subject': 'ZAB',
        'session': 'SR1',
        'fs_hz': FS_HZ,
        'n_channels': len(labels),
        'n_samples': int(eeg_data.shape[0]),
        'duration_s': float(eeg_data.shape[0] / srate),
        'n_fixations': int(fix_data.shape[0]),
        'n_fixation_spikes_in_eeg_range': in_range,
        'lag_sweep_ms': LAG_SWEEP_MS,
        'bandpass_hz': [BAND_LOW, BAND_HIGH],
        'auditory_roi_target': AUDITORY_ROI,
        'per_channel_peak': per_ch,
        'aggregate': aggregate,
        'falsifier_F_SLM_C1': verdict,
        'mock_baseline_compare': {
            'mock_planted_r': 0.225,
            'mock_lag_ms': 120,
            'real_aud_mean_r': aud_mean,
            'real_aud_max_r': aud_max,
            'real_aud_lag_mean_ms': aggregate['auditory_peak_lag_ms_mean'],
            'real_minus_mock_r': aud_mean - 0.225,
        },
        'honest_caveats': [
            'Single subject (ZAB) only — no cross-subject generalization tested.',
            'Automagic preprocessing artifacts: 23 of 128 channels rejected; ICA cleanup may suppress true neural variance, biasing r downward.',
            'Lag selection 60-500ms swept (not just planted 120ms); peak-lag selection inflates r vs theory-fixed lag — but per-channel report includes r_at_120ms for honest comparison.',
            'Word-level TRF approximated via fixation-onset impulse train (no per-word lexical features); Brennan-Hale 2019 used surprisal/entropy regressors which yield higher r (~0.05-0.15 typ).',
            'EGI HydroCel 128 → 10-10 mapping (T7≈E45 etc) is approximate; true T7/T8/P7/P8 may differ by 1-2 channels.',
        ],
        'wall_seconds': time.time() - t0,
    }

    OUT.write_text(json.dumps(out, indent=2))
    print(f'[{time.time()-t0:.1f}s] DONE → {OUT}')
    print(json.dumps(verdict, indent=2))
    print()
    print('Aggregate:')
    print(json.dumps(aggregate, indent=2))


if __name__ == '__main__':
    main()
