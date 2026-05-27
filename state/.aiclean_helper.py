#!/usr/bin/env python3
# ai_cleaning_pipeline helper — applies suppressor chain
import sys, os
try:
    import numpy as np
    from scipy import signal
except Exception as e:
    sys.stderr.write('import-failed: ' + repr(e) + '\n'); sys.exit(10)
if len(sys.argv) < 6:
    sys.stderr.write('usage: helper <mode> <src> <fs> <chain> <out_npy>\n'); sys.exit(2)
mode, src, fs_s, chain, out_npy = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]
fs = float(fs_s)

def load_eeg16(path):
    a = np.load(path, allow_pickle=False)
    if a.ndim != 2: raise RuntimeError('expected 2-D')
    r, c = a.shape
    if r == 16: return a, 16, c
    if c == 16: return a.T, 16, r
    if r >= 32 and c > r: return a[1:17, :], 16, c
    if c >= 32 and r > c: return a.T[1:17, :], 16, r
    raise RuntimeError('cannot infer 16-ch')

if mode == 'real':
    if not os.path.isfile(src):
        sys.stderr.write('not-found\n'); sys.exit(4)
    eeg, n_ch, n_samp = load_eeg16(src)
else:
    sys.stderr.write('selftest-mode-not-supported-for-pipeline-cleaning\n'); sys.exit(5)

eeg = eeg.astype(np.float64).copy()
ops = []

# parse chain ('+' separated or '→' separated)
parts = chain.replace('→','+').split('+')
parts = [p.strip() for p in parts if p.strip() and p.strip() != 'NONE']

for op in parts:
    if op == 'EMI':
        # notch 60Hz (US) + 50Hz (intl) + harmonics 120/180
        for f0 in [50.0, 60.0, 120.0, 180.0]:
            if f0 >= fs/2 - 0.5: continue
            try:
                bn, an = signal.iirnotch(f0/(fs/2), Q=30.0)
                for ch in range(eeg.shape[0]):
                    eeg[ch] = signal.filtfilt(bn, an, eeg[ch])
            except Exception:
                pass
        ops.append('notch_50_60_120_180')
    elif op == 'BLINK':
        # MAD-clip Fp1, Fp2 (idx 0, 1)
        for ch in [0, 1]:
            x = eeg[ch]; med = np.median(x); mad = np.median(np.abs(x - med)) + 1e-9
            thr = 6.0 * 1.4826 * mad
            eeg[ch] = np.clip(x, med - thr, med + thr)
        ops.append('mad_clip_fp1_fp2')
    elif op == 'MOTION':
        # zero-fill epochs where ≥8 channels co-spike (using 5σ)
        sds = np.std(eeg, axis=1, keepdims=True) + 1e-9
        z = np.abs(eeg - np.mean(eeg, axis=1, keepdims=True)) / sds
        spikes = z > 5.0
        win = max(1, int(0.1 * fs))
        nb = eeg.shape[1] // win
        n_zero = 0
        for b in range(nb):
            s_ = b*win; e_ = (b+1)*win
            if int(np.sum(np.any(spikes[:, s_:e_], axis=1))) >= 8:
                eeg[:, s_:e_] = 0.0; n_zero += 1
        ops.append('epoch_reject_motion_n=' + str(n_zero))
    elif op == 'EMG' or op == 'ECG':
        # low-pass 30 Hz
        if 'lp30' not in ops:
            bl, al = signal.butter(4, 30.0/(fs/2), btype='low')
            for ch in range(eeg.shape[0]):
                eeg[ch] = signal.filtfilt(bl, al, eeg[ch])
            ops.append('lp30')
    elif op == 'REF_DRIFT':
        bh, ah = signal.butter(4, 0.5/(fs/2), btype='high')
        for ch in range(eeg.shape[0]):
            eeg[ch] = signal.filtfilt(bh, ah, eeg[ch])
        ops.append('hp_0.5')
    elif op == 'AGING':
        # zero-fill suspect channels (cross-ch z>3 RMS)
        rms = np.sqrt(np.mean(eeg*eeg, axis=1))
        med = np.median(rms); mad = np.median(np.abs(rms - med)) + 1e-9
        sigma = 1.4826 * mad
        n_drop = 0
        for ci in range(eeg.shape[0]):
            if sigma > 1e-9 and (rms[ci] - med) / sigma > 3.0:
                eeg[ci] = 0.0; n_drop += 1
        ops.append('drop_suspect_n=' + str(n_drop))

np.save(out_npy, eeg.astype(np.float32))
print('ops=' + ','.join(ops))
print('OK')
