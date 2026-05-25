#!/usr/bin/env python3
import sys, os
try:
    import numpy as np
    from scipy import signal
except Exception as e:
    sys.stderr.write('import-failed: ' + repr(e) + '\n'); sys.exit(10)
if len(sys.argv) < 5:
    sys.stderr.write('usage\n'); sys.exit(2)
mode, src, fs_s, out_path = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
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
if mode == 'selftest':
    kind = src; n = 60 * int(fs); rng = np.random.RandomState(42)
    eeg = rng.normal(0, 5.0, size=(16, n))
    t = np.arange(n) / fs
    if kind == 'ecg':
        # 72 BPM = 1.2 Hz; QRS-like spikes
        rr = 60.0 / 72.0
        for k in range(int(60.0/rr)):
            i0 = int(k*rr*fs); w = int(0.05*fs)
            for ch in range(16):
                if i0 + w <= n: eeg[ch, i0:i0+w] += 50.0 * np.hanning(w)
    elif kind == 'mild_ecg':
        rr = 60.0 / 72.0
        for k in range(int(60.0/rr)):
            i0 = int(k*rr*fs); w = int(0.05*fs)
            for ch in [10, 11]:
                if i0 + w <= n: eeg[ch, i0:i0+w] += 50.0 * np.hanning(w)
    elif kind == 'alpha':
        for ch in [6, 7]: eeg[ch] += 8.0 * np.sin(2*np.pi*10.0*t)
    elif kind == 'line60':
        for ch in range(16): eeg[ch] += 8.0 * np.sin(2*np.pi*60.0*t)
    elif kind == 'motion':
        for k in range(10):
            i0 = int((k*5+1)*fs); w = int(0.1*fs)
            for ch in range(16): eeg[ch, i0:i0+w] += 200.0 * np.sign(rng.randn()) * np.hanning(w)
    elif kind == 'white':
        pass
    else:
        sys.stderr.write('unknown\n'); sys.exit(3)
    n_ch, n_samp = 16, n
elif mode == 'real':
    if not os.path.isfile(src): sys.stderr.write('not-found\n'); sys.exit(4)
    eeg, n_ch, n_samp = load_eeg16(src)
else:
    sys.stderr.write('bad mode\n'); sys.exit(2)

# bandpass 1–3 Hz, then autocorr; look for peak in lag 0.6–1.0 s
b, a_ = signal.butter(4, [1.0/(fs/2), 3.0/(fs/2)], btype='band')
def autocorr_peak(x):
    xf = signal.filtfilt(b, a_, x)
    xf = xf - np.mean(xf)
    if np.std(xf) < 1e-9: return 0.0, 0.0
    xf = xf / (np.std(xf) + 1e-12)
    lo = int(0.6 * fs); hi = int(1.0 * fs)
    if hi >= len(xf): return 0.0, 0.0
    ac = np.correlate(xf, xf, mode='full')
    mid = len(ac) // 2
    seg = ac[mid+lo:mid+hi] / (len(xf))
    if len(seg) == 0: return 0.0, 0.0
    pi = int(np.argmax(seg))
    pk = float(seg[pi])
    lag_s = (lo + pi) / fs
    return pk, lag_s

n_ecg = 0; max_pk = 0.0; max_lag = 0.0
for ci in range(int(n_ch)):
    pk, lag = autocorr_peak(eeg[ci])
    if pk > 0.3 and 0.6 <= lag <= 1.0:
        n_ecg += 1
        if pk > max_pk: max_pk = pk; max_lag = lag

with open(out_path, 'w') as f:
    f.write('schema=ecg_artifact_v1\n')
    f.write('n_ch=' + str(int(n_ch)) + '\n')
    f.write('n_samp=' + str(int(n_samp)) + '\n')
    f.write('n_ecg_channels=' + str(n_ecg) + '\n')
    f.write('max_autocorr_x100=' + str(int(round(max_pk*100))) + '\n')
    f.write('max_lag_ms=' + str(int(round(max_lag*1000))) + '\n')
    if max_lag > 0:
        bpm = 60.0 / max_lag
        f.write('estimated_bpm_x10=' + str(int(round(bpm*10))) + '\n')
    else:
        f.write('estimated_bpm_x10=0\n')
print('OK')
