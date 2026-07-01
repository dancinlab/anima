#!/usr/bin/env python3
# emi_classifier helper — auto-generated (raw#9/raw#37 transient)
import sys, os
try:
    import numpy as np
    from scipy import signal
except Exception as e:
    sys.stderr.write('import-failed: ' + repr(e) + '\n'); sys.exit(10)

if len(sys.argv) < 5:
    sys.stderr.write('usage: helper <mode> <src> <fs> <out>\n'); sys.exit(2)
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
    raise RuntimeError('cannot infer 16-ch from ' + str(a.shape))

if mode == 'selftest':
    kind = src
    n = 30 * int(fs)
    rng = np.random.RandomState(42)
    eeg = rng.normal(0, 1.0, size=(16, n))
    t = np.arange(n) / fs
    if kind == 'line50':
        for ch in range(16): eeg[ch] += 8.0 * np.sin(2*np.pi*50.0*t)
    elif kind == 'line60':
        for ch in range(16): eeg[ch] += 8.0 * np.sin(2*np.pi*60.0*t)
    elif kind == 'harm120':
        for ch in range(16): eeg[ch] += 6.0*np.sin(2*np.pi*60.0*t) + 4.0*np.sin(2*np.pi*120.0*t)
    elif kind == 'alpha':
        for ch in [6, 7]: eeg[ch] += 5.0*np.sin(2*np.pi*10.0*t)
    elif kind == 'white':
        pass
    elif kind == 'drift':
        for ch in range(16): eeg[ch] += 50.0*np.sin(2*np.pi*0.05*t)
    else:
        sys.stderr.write('unknown kind: ' + kind + '\n'); sys.exit(3)
    n_ch, n_samp = 16, n
elif mode == 'real':
    if not os.path.isfile(src):
        sys.stderr.write('not-found: ' + src + '\n'); sys.exit(4)
    eeg, n_ch, n_samp = load_eeg16(src)
else:
    sys.stderr.write('bad mode\n'); sys.exit(2)

def emi_score_ch(x):
    f, psd = signal.welch(x, fs=fs, nperseg=min(512, len(x)))
    psd_db = 10.0 * np.log10(psd + 1e-30)
    # broadband floor: median of 1-40 Hz brain band
    bb = (f >= 1.0) & (f <= 40.0)
    floor = float(np.median(psd_db[bb])) if np.any(bb) else -120.0
    # narrowband targets
    targets = [50.0, 60.0, 100.0, 120.0, 180.0]
    peaks = {}
    max_excess = -1e9
    dominant_freq = 0.0
    for tg in targets:
        m = (f >= tg - 1.0) & (f <= tg + 1.0)
        if not np.any(m): continue
        pk = float(np.max(psd_db[m]))
        ex = pk - floor
        peaks[tg] = ex
        if ex > max_excess:
            max_excess = ex; dominant_freq = tg
    return max_excess, dominant_freq, floor, peaks

with open(out_path, 'w') as f:
    f.write('schema=emi_classifier_v1\n')
    f.write('n_ch=' + str(int(n_ch)) + '\n')
    f.write('n_samp=' + str(int(n_samp)) + '\n')
    n_dominant = 0; n_mild = 0; n_clean = 0
    max_global = -1e9; freq_global = 0.0
    for ci in range(int(n_ch)):
        ex, df, fl, pks = emi_score_ch(eeg[ci, :])
        f.write('ch' + str(ci) + '_excess_db_x10=' + str(int(round(ex*10))) + '\n')
        f.write('ch' + str(ci) + '_dominant_freq_x10=' + str(int(round(df*10))) + '\n')
        if ex >= 12.0: n_dominant += 1
        elif ex >= 6.0: n_mild += 1
        else: n_clean += 1
        if ex > max_global: max_global = ex; freq_global = df
    f.write('n_dominant=' + str(n_dominant) + '\n')
    f.write('n_mild=' + str(n_mild) + '\n')
    f.write('n_clean=' + str(n_clean) + '\n')
    f.write('max_excess_db_x10=' + str(int(round(max_global*10))) + '\n')
    f.write('global_dominant_freq_x10=' + str(int(round(freq_global*10))) + '\n')
print('OK')
