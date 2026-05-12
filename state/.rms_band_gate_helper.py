#!/usr/bin/env python3
# rms_band_gate helper. raw#9 transient .py; raw#37 re-written each call.
import sys, os
try:
    import numpy as np
except Exception as e:
    sys.stderr.write('import-failed: ' + repr(e) + '\n'); sys.exit(10)

if len(sys.argv) < 4:
    sys.stderr.write('usage: helper <mode> <input_or_kind> <out>\n'); sys.exit(2)
mode, src, out_path = sys.argv[1], sys.argv[2], sys.argv[3]

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
    n = 60 * 125
    rng = np.random.RandomState(13)
    eeg = np.zeros((16, n), dtype=np.float64)
    if kind == 'awake':
        # ~20 µV broadband — typical awake amplitude
        for ch in range(16):
            eeg[ch, :] = 20.0 * rng.normal(0, 1, n)
    elif kind == 'flatline':
        pass  # zero -> RMS 0
    elif kind == 'broadband_huge':
        # battery dying / saturated — RMS thousands µV
        for ch in range(16):
            eeg[ch, :] = 5000.0 * rng.normal(0, 1, n)
    elif kind == 'tiny':
        for ch in range(16):
            eeg[ch, :] = 0.5 * rng.normal(0, 1, n)
    else:
        sys.stderr.write('unknown kind: ' + kind + '\n'); sys.exit(3)
    n_ch, n_samp = 16, n
elif mode == 'real':
    if not os.path.isfile(src):
        sys.stderr.write('not-found: ' + src + '\n'); sys.exit(4)
    eeg, n_ch, n_samp = load_eeg16(src)
else:
    sys.stderr.write('unknown mode\n'); sys.exit(2)

rms_per_ch = []
for ch in range(n_ch):
    x = np.asarray(eeg[ch, :], dtype=np.float64)
    rms_per_ch.append(float(np.sqrt(np.mean(x * x))))
rms_per_ch = np.array(rms_per_ch)
median_rms = float(np.median(rms_per_ch))
LO, HI = 5.0, 100.0
in_band = int(np.sum((rms_per_ch >= LO) & (rms_per_ch <= HI)))
in_band_ratio = float(in_band) / float(n_ch)

with open(out_path, 'w') as f:
    f.write('schema=rms_band_gate_v1\n')
    f.write('n_ch=' + str(int(n_ch)) + '\n')
    f.write('n_samp=' + str(int(n_samp)) + '\n')
    f.write('median_rms_x10=' + str(int(round(median_rms * 10))) + '\n')
    f.write('in_band_count=' + str(int(in_band)) + '\n')
    f.write('in_band_ratio_x100=' + str(int(round(in_band_ratio * 100))) + '\n')
    for ch in range(n_ch):
        f.write('rms_ch' + str(ch) + '_x10=' + str(int(round(rms_per_ch[ch] * 10))) + '\n')
print('OK median=' + ('%.2f' % median_rms))
