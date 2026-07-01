#!/usr/bin/env python3
# eye_blink_detector helper — auto-generated (raw#9/raw#37 transient)
import sys, os
try:
    import numpy as np
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
    kind = src; n = 60 * int(fs); rng = np.random.RandomState(42)
    eeg = rng.normal(0, 5.0, size=(16, n))
    t = np.arange(n) / fs
    if kind == 'blink':
        # inject 60 blinks (1 per s) on Fp1/Fp2 (ch 0,1) ~ 300 µV spike
        for sec in range(60):
            i0 = int(sec*fs); w = int(0.2*fs)
            for ch in [0, 1]:
                eeg[ch, i0:i0+w] += 300.0 * np.hanning(w)
    elif kind == 'mild_blink':
        for sec in range(0, 60, 3):  # 20 blinks
            i0 = int(sec*fs); w = int(0.2*fs)
            for ch in [0, 1]: eeg[ch, i0:i0+w] += 300.0 * np.hanning(w)
    elif kind == 'alpha':
        for ch in [6, 7]: eeg[ch] += 8.0 * np.sin(2*np.pi*10.0*t)
    elif kind == 'line60':
        for ch in range(16): eeg[ch] += 8.0 * np.sin(2*np.pi*60.0*t)
    elif kind == 'drift':
        for ch in range(16): eeg[ch] += 50.0 * np.sin(2*np.pi*0.05*t)
    elif kind == 'white':
        pass
    else:
        sys.stderr.write('unknown kind: ' + kind + '\n'); sys.exit(3)
    n_ch, n_samp = 16, n
elif mode == 'real':
    if not os.path.isfile(src): sys.stderr.write('not-found: ' + src + '\n'); sys.exit(4)
    eeg, n_ch, n_samp = load_eeg16(src)
else:
    sys.stderr.write('bad mode\n'); sys.exit(2)

def count_spikes(x, k=6.0, refractory_samples=10):
    med = np.median(x); mad = np.median(np.abs(x - med)) + 1e-9
    thr = k * 1.4826 * mad
    over = np.abs(x - med) > thr
    # refractory: collapse runs separated by < refractory
    n_events = 0; last = -10**9
    idxs = np.where(over)[0]
    for ix in idxs:
        if ix - last >= refractory_samples:
            n_events += 1; last = ix
    return n_events, float(thr), float(med + 0.0)

duration_s = float(n_samp) / fs
total_blinks = 0
ch_blink_counts = []
for ci in [0, 1]:  # Fp1, Fp2
    if ci >= n_ch: ch_blink_counts.append(0); continue
    n_ev, thr, med = count_spikes(eeg[ci, :])
    ch_blink_counts.append(n_ev)
# union estimate: max(Fp1, Fp2) since blinks are bilateral
max_blinks = max(ch_blink_counts) if ch_blink_counts else 0
rate_per_min = (max_blinks / duration_s) * 60.0 if duration_s > 0 else 0.0

with open(out_path, 'w') as f:
    f.write('schema=eye_blink_detector_v1\n')
    f.write('n_ch=' + str(int(n_ch)) + '\n')
    f.write('n_samp=' + str(int(n_samp)) + '\n')
    f.write('duration_s_x10=' + str(int(round(duration_s*10))) + '\n')
    f.write('fp1_blinks=' + str(int(ch_blink_counts[0])) + '\n')
    f.write('fp2_blinks=' + str(int(ch_blink_counts[1])) + '\n')
    f.write('max_blinks=' + str(int(max_blinks)) + '\n')
    f.write('blink_rate_per_min_x10=' + str(int(round(rate_per_min*10))) + '\n')
print('OK')
