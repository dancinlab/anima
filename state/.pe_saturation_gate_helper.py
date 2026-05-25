#!/usr/bin/env python3
# pe_saturation_gate helper. Bandt-Pompe 2002, Costa multiscale 2002.
# raw#9 transient .py; raw#37 re-written each call.
import sys, os, math
try:
    import numpy as np
except Exception as e:
    sys.stderr.write('import-failed: ' + repr(e) + '\n'); sys.exit(10)

if len(sys.argv) < 4:
    sys.stderr.write('usage: helper <mode> <input_or_kind> <out>\n'); sys.exit(2)
mode, src, out_path = sys.argv[1], sys.argv[2], sys.argv[3]
M = 3; TAU = 1; SCALES = [1, 2, 5, 10]

def load_eeg16(path):
    a = np.load(path, allow_pickle=False)
    if a.ndim != 2: raise RuntimeError('expected 2-D')
    r, c = a.shape
    if r == 16: return a, 16, c
    if c == 16: return a.T, 16, r
    if r >= 32 and c > r: return a[1:17, :], 16, c
    if c >= 32 and r > c: return a.T[1:17, :], 16, r
    raise RuntimeError('cannot infer 16-ch from ' + str(a.shape))

def coarse_grain(x, s):
    if s <= 1: return x
    n = len(x) // s
    if n <= 0: return np.array([], dtype=np.float64)
    return x[: n * s].reshape(n, s).mean(axis=1)

def permutation_entropy(x, m=3, tau=1):
    n = len(x); L = n - (m - 1) * tau
    if L <= 0: return 0.0
    counts = {}
    for i in range(L):
        w = x[i:i + m * tau:tau]
        perm = tuple(int(v) for v in np.argsort(w, kind='stable'))
        counts[perm] = counts.get(perm, 0) + 1
    total = float(L); H = 0.0
    for c in counts.values():
        p = c / total
        if p > 0.0: H -= p * math.log(p)
    Hmax = math.log(math.factorial(m))
    return H / Hmax if Hmax > 0 else 0.0

if mode == 'selftest':
    kind = src
    n = 60 * 125
    rng = np.random.RandomState(7)
    eeg = np.zeros((16, n), dtype=np.float64)
    if kind == 'const':
        pass
    elif kind == 'white':
        for ch in range(16):
            eeg[ch, :] = rng.normal(0, 1, n)
    elif kind == 'monotone':
        for ch in range(16):
            eeg[ch, :] = np.arange(n, dtype=np.float64) + ch * 0.5
    elif kind == 'awake':
        # mixed alpha-dominant + small broadband + low-freq trend. PE on
        # awake EEG is empirically 0.6-0.85; pure i.i.d. ramps to ~1.0,
        # so we need structured oscillations to dominate. Strong 10 Hz
        # alpha (amp 5) + weak noise (amp 0.3) yields PE ≈ 0.7.
        t = np.arange(n) / 125.0
        for ch in range(16):
            eeg[ch, :] = (5.0 * np.sin(2 * np.pi * 10.0 * t + ch * 0.1)
                          + 0.3 * rng.normal(0, 1, n))
    else:
        sys.stderr.write('unknown kind: ' + kind + '\n'); sys.exit(3)
    n_ch, n_samp = 16, n
elif mode == 'real':
    if not os.path.isfile(src):
        sys.stderr.write('not-found: ' + src + '\n'); sys.exit(4)
    eeg, n_ch, n_samp = load_eeg16(src)
else:
    sys.stderr.write('unknown mode\n'); sys.exit(2)

pe_per = np.zeros((n_ch, len(SCALES)), dtype=np.float64)
for ch in range(n_ch):
    x = np.asarray(eeg[ch, :], dtype=np.float64)
    for j, s in enumerate(SCALES):
        cg = coarse_grain(x, s)
        if len(cg) <= M * TAU: pe_per[ch, j] = float('nan')
        else: pe_per[ch, j] = permutation_entropy(cg, m=M, tau=TAU)

pe_mean_overall = float(np.nanmean(pe_per))
pe_s = [float(np.nanmean(pe_per[:, j])) for j in range(len(SCALES))]

with open(out_path, 'w') as f:
    f.write('schema=pe_saturation_gate_v1\n')
    f.write('n_ch=' + str(int(n_ch)) + '\n')
    f.write('n_samp=' + str(int(n_samp)) + '\n')
    f.write('embed_dim=' + str(M) + '\n')
    f.write('scales=1,2,5,10\n')
    f.write('pe_mean_overall_x1000=' + str(int(round(pe_mean_overall * 1000))) + '\n')
    f.write('pe_mean_scale1_x1000=' + str(int(round(pe_s[0] * 1000))) + '\n')
    f.write('pe_mean_scale2_x1000=' + str(int(round(pe_s[1] * 1000))) + '\n')
    f.write('pe_mean_scale5_x1000=' + str(int(round(pe_s[2] * 1000))) + '\n')
    f.write('pe_mean_scale10_x1000=' + str(int(round(pe_s[3] * 1000))) + '\n')
print('OK pe=' + ('%.4f' % pe_mean_overall))
