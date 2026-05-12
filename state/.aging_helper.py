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
    kind = src; n = 30 * int(fs); rng = np.random.RandomState(42)
    eeg = rng.normal(0, 5.0, size=(16, n))
    t = np.arange(n) / fs
    if kind == 'aging':
        # 5 channels with elevated noise floor (electrode aging)
        for ch in [2, 5, 8, 11, 14]:
            eeg[ch] += rng.normal(0, 25.0, size=n)
    elif kind == 'mild_aging':
        for ch in [2, 5]: eeg[ch] += rng.normal(0, 25.0, size=n)
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

# per-ch broadband RMS
rms = np.sqrt(np.mean(eeg*eeg, axis=1))
med = float(np.median(rms))
mad = float(np.median(np.abs(rms - med))) + 1e-9
sigma = 1.4826 * mad
suspect = []
for ci in range(int(n_ch)):
    z = (rms[ci] - med) / sigma if sigma > 1e-9 else 0.0
    if z > 3.0: suspect.append(ci)

with open(out_path, 'w') as f:
    f.write('schema=electrode_aging_v1\n')
    f.write('n_ch=' + str(int(n_ch)) + '\n')
    f.write('n_samp=' + str(int(n_samp)) + '\n')
    f.write('n_suspect=' + str(len(suspect)) + '\n')
    f.write('median_rms_x100=' + str(int(round(med*100))) + '\n')
    f.write('mad_rms_x100=' + str(int(round(mad*100))) + '\n')
    f.write('suspect_channels=' + ','.join(str(s) for s in suspect) + '\n')
print('OK')
