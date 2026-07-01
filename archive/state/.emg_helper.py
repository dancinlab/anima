#!/usr/bin/env python3
import sys, os
try:
    import numpy as np
    from scipy import signal, integrate
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
    kind = src; n = 30 * int(fs); rng = np.random.RandomState(42)
    eeg = rng.normal(0, 1.0, size=(16, n))
    t = np.arange(n) / fs
    if kind == 'emg':
        # high-freq broadband on temporal+all channels
        hf = rng.normal(0, 8.0, size=(16, n))
        b, a = signal.butter(4, [20.0/(fs/2), 0.95], btype='band')
        for ch in range(16): eeg[ch] += signal.filtfilt(b, a, hf[ch])
    elif kind == 'mild_emg':
        hf = rng.normal(0, 8.0, size=(16, n))
        b, a = signal.butter(4, [20.0/(fs/2), 0.95], btype='band')
        for ch in [4, 5]: eeg[ch] += signal.filtfilt(b, a, hf[ch])
    elif kind == 'alpha':
        for ch in [6, 7]: eeg[ch] += 8.0 * np.sin(2*np.pi*10.0*t)
    elif kind == 'line60':
        for ch in range(16): eeg[ch] += 8.0 * np.sin(2*np.pi*60.0*t)
    elif kind == 'drift':
        for ch in range(16): eeg[ch] += 50.0 * np.sin(2*np.pi*0.05*t)
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
def bp(f, psd, lo, hi):
    m = (f >= lo) & (f <= hi)
    if not np.any(m): return 0.0
    return float(integrate.simpson(psd[m], x=f[m]))
n_emg = 0; ratios = []
for ci in range(int(n_ch)):
    f, psd = signal.welch(eeg[ci], fs=fs, nperseg=min(512, eeg.shape[1]))
    a_p = bp(f, psd, 8.0, 13.0)
    g_p = bp(f, psd, 20.0, 60.0)
    r = (g_p / a_p) if a_p > 1e-12 else 999.0
    ratios.append(r)
    if r > 2.0: n_emg += 1
max_r = max(ratios) if ratios else 0.0
with open(out_path, 'w') as f:
    f.write('schema=emg_muscle_v1\n')
    f.write('n_ch=' + str(int(n_ch)) + '\n')
    f.write('n_samp=' + str(int(n_samp)) + '\n')
    f.write('n_emg_channels=' + str(n_emg) + '\n')
    f.write('max_gamma_alpha_ratio_x100=' + str(int(round(min(max_r, 99.0)*100))) + '\n')
    # T7, T8 specific (idx 4, 5)
    f.write('t7_ratio_x100=' + str(int(round(min(ratios[4], 99.0)*100))) + '\n')
    f.write('t8_ratio_x100=' + str(int(round(min(ratios[5], 99.0)*100))) + '\n')
print('OK')
