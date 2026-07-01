#!/usr/bin/env python3
# hjorth_band_gate helper. Hjorth 1970 (Activity, Mobility, Complexity).
# raw#9 transient .py; raw#37 re-written each call.
import sys, os, math
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

def hjorth(x):
    x = np.asarray(x, dtype=np.float64)
    activity = float(np.var(x))
    if activity == 0.0: return 0.0, 0.0, 0.0
    d1 = np.diff(x); var_d1 = float(np.var(d1))
    if var_d1 == 0.0: return activity, 0.0, 0.0
    mobility = math.sqrt(var_d1 / activity)
    d2 = np.diff(d1); var_d2 = float(np.var(d2))
    if var_d1 == 0.0 or mobility == 0.0: return activity, mobility, 0.0
    mobility_d1 = math.sqrt(var_d2 / var_d1)
    complexity = mobility_d1 / mobility
    return activity, mobility, complexity

if mode == 'selftest':
    kind = src
    n = 60 * 125
    rng = np.random.RandomState(11)
    eeg = np.zeros((16, n), dtype=np.float64)
    if kind == 'awake':
        # awake-like 1/f-ish broadband
        t = np.arange(n) / 125.0
        for ch in range(16):
            eeg[ch, :] = rng.normal(0, 1, n) + 0.5 * np.sin(2 * np.pi * 10.0 * t)
    elif kind == 'const':
        pass
    elif kind == 'white':
        for ch in range(16):
            eeg[ch, :] = rng.normal(0, 1, n)
    elif kind == 'sine':
        t = np.arange(n) / 125.0
        for ch in range(16):
            eeg[ch, :] = np.sin(2 * np.pi * 10.0 * t)
    elif kind == 'drift':
        t = np.arange(n) / 125.0
        for ch in range(16):
            eeg[ch, :] = np.sin(2 * np.pi * 0.05 * t)
    else:
        sys.stderr.write('unknown kind: ' + kind + '\n'); sys.exit(3)
    n_ch, n_samp = 16, n
elif mode == 'real':
    if not os.path.isfile(src):
        sys.stderr.write('not-found: ' + src + '\n'); sys.exit(4)
    eeg, n_ch, n_samp = load_eeg16(src)
else:
    sys.stderr.write('unknown mode\n'); sys.exit(2)

acts, mobs, cpxs = [], [], []
for ch in range(n_ch):
    a_, m_, c_ = hjorth(eeg[ch, :])
    acts.append(a_); mobs.append(m_); cpxs.append(c_)
act_mean = float(np.mean(acts))
mob_mean = float(np.mean(mobs))
cpx_mean = float(np.mean(cpxs))

with open(out_path, 'w') as f:
    f.write('schema=hjorth_band_gate_v1\n')
    f.write('n_ch=' + str(int(n_ch)) + '\n')
    f.write('n_samp=' + str(int(n_samp)) + '\n')
    if act_mean > 0:
        f.write('log10_activity_mean_x1000=' + str(int(round(math.log10(act_mean) * 1000))) + '\n')
    else:
        f.write('log10_activity_mean_x1000=-2147483647\n')
    f.write('mobility_mean_x1000=' + str(int(round(mob_mean * 1000))) + '\n')
    f.write('complexity_mean_x1000=' + str(int(round(cpx_mean * 1000))) + '\n')
print('OK cpx=' + ('%.4f' % cpx_mean))
