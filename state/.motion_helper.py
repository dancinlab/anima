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
    if kind == 'motion':
        # 10 motion epochs ~0.1s long, all channels co-spike
        for k in range(10):
            i0 = int((k*5 + 1)*fs); w = int(0.1*fs)
            for ch in range(16): eeg[ch, i0:i0+w] += 200.0 * np.sign(rng.randn()) * np.hanning(w)
    elif kind == 'mild_motion':
        for k in range(3):
            i0 = int((k*15 + 5)*fs); w = int(0.1*fs)
            for ch in range(16): eeg[ch, i0:i0+w] += 200.0 * np.sign(rng.randn()) * np.hanning(w)
    elif kind == 'blink':
        for sec in range(60):
            i0 = int(sec*fs); w = int(0.2*fs)
            for ch in [0, 1]: eeg[ch, i0:i0+w] += 300.0 * np.hanning(w)
    elif kind == 'alpha':
        for ch in [6, 7]: eeg[ch] += 8.0 * np.sin(2*np.pi*10.0*t)
    elif kind == 'line60':
        for ch in range(16): eeg[ch] += 8.0 * np.sin(2*np.pi*60.0*t)
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

# per-ch z-score, find spikes > 5σ
sds = np.std(eeg, axis=1, keepdims=True) + 1e-9
mus = np.mean(eeg, axis=1, keepdims=True)
z = np.abs(eeg - mus) / sds
spikes = z > 5.0  # (16, n)
# bin into 0.1s windows; count channels co-spiking
win = max(1, int(0.1 * fs))
nb = n_samp // win
co_count = np.zeros(nb, dtype=np.int32)
for b in range(nb):
    seg = spikes[:, b*win:(b+1)*win]
    co_count[b] = int(np.sum(np.any(seg, axis=1)))
motion_epochs = int(np.sum(co_count >= 8))
max_co = int(np.max(co_count)) if nb > 0 else 0

with open(out_path, 'w') as f:
    f.write('schema=motion_artifact_v1\n')
    f.write('n_ch=' + str(int(n_ch)) + '\n')
    f.write('n_samp=' + str(int(n_samp)) + '\n')
    f.write('motion_epochs=' + str(motion_epochs) + '\n')
    f.write('max_coactive_channels=' + str(max_co) + '\n')
print('OK')
