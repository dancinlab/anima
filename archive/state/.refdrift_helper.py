#!/usr/bin/env python3
import sys, os
try:
    import numpy as np
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
    if kind == 'drift':
        # large 0.05 Hz drift on all channels
        for ch in range(16): eeg[ch] += 100.0 * np.sin(2*np.pi*0.05*t)
    elif kind == 'mild_drift':
        for ch in range(16): eeg[ch] += 30.0 * np.sin(2*np.pi*0.05*t)
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

# grand mean across channels
gm = np.mean(eeg, axis=0)
t_axis = np.arange(len(gm)) / fs
# linear slope (µV/s) — simple least-squares
slope, intercept = np.polyfit(t_axis, gm, 1)
abs_slope = abs(float(slope))
# range of grand mean
gm_range = float(np.max(gm) - np.min(gm))
# cross-ch low-freq correlation: detrend long, smooth window 1s
win = max(1, int(1.0*fs))
sm = np.zeros_like(eeg)
for ch in range(int(n_ch)):
    sm[ch] = np.convolve(eeg[ch], np.ones(win)/win, mode='same')
# pairwise corr mean among first 8 channels
n_corr_ch = min(8, int(n_ch))
corrs = []
for i in range(n_corr_ch):
    for j in range(i+1, n_corr_ch):
        x1 = sm[i]; x2 = sm[j]
        s1 = np.std(x1); s2 = np.std(x2)
        if s1 < 1e-9 or s2 < 1e-9: continue
        corrs.append(float(np.mean((x1-np.mean(x1))*(x2-np.mean(x2)))/(s1*s2)))
mean_corr = float(np.mean(corrs)) if corrs else 0.0

with open(out_path, 'w') as f:
    f.write('schema=reference_drift_v1\n')
    f.write('n_ch=' + str(int(n_ch)) + '\n')
    f.write('n_samp=' + str(int(n_samp)) + '\n')
    f.write('grand_mean_slope_x100=' + str(int(round(abs_slope*100))) + '\n')
    f.write('grand_mean_range_x100=' + str(int(round(gm_range*100))) + '\n')
    f.write('mean_pairwise_corr_x1000=' + str(int(round(mean_corr*1000))) + '\n')
print('OK')
