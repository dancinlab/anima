#!/usr/bin/env python3
# anima-eeg-core/_metrics/pe_native cross-validate (path a).
# Reads native-produced int fixture, recomputes PE via numpy, emits pe_x1000.
# raw#9 OK: /tmp-style transient.
import sys, os, math
try:
    import numpy as np
except ImportError:
    sys.stderr.write('numpy not installed in invoking python\n'); sys.exit(10)
if len(sys.argv) < 3:
    sys.stderr.write('usage: helper <fixture.txt> <out.txt>\n'); sys.exit(2)
in_path, out_path = sys.argv[1], sys.argv[2]
if not os.path.isfile(in_path):
    sys.stderr.write('fixture not found: ' + in_path + '\n'); sys.exit(3)
M, TAU = 3, 1
SCALES = [1, 2, 5, 10]

def coarse_grain_floor(x, s):
    if s <= 1: return x.astype(np.int64)
    n = len(x) // s
    if n <= 0: return np.array([], dtype=np.int64)
    cg = np.floor(x[: n * s].reshape(n, s).sum(axis=1) / float(s)).astype(np.int64)
    # Match native floor(sum/s) semantics exactly: floor(sum/s) == sum//s
    cg = (x[: n * s].reshape(n, s).sum(axis=1) // s).astype(np.int64)
    return cg

# Stable rank ordinal index for m=3 — same logic as native ordinal_index_m3.
def ordinal_index_m3(a, b, c):
    ra = (1 if b < a else 0) + (1 if c < a else 0)
    rb = ((1 if a < b else 0) + (1 if a == b else 0) + (1 if c < b else 0))
    rc = ((1 if a < c else 0) + (1 if a == c else 0) + (1 if b < c else 0) + (1 if b == c else 0))
    table = {(0,1,2):0,(0,2,1):1,(1,0,2):2,(2,0,1):4,(1,2,0):3,(2,1,0):5}
    return table.get((ra,rb,rc), -1)

def pe_x1000(x):
    n = len(x)
    if n < 3: return None
    L = n - 2
    counts = [0]*6
    for i in range(L):
        idx = ordinal_index_m3(int(x[i]), int(x[i+1]), int(x[i+2]))
        if idx < 0: return None
        counts[idx] += 1
    # H_log2 in float
    H = 0.0
    for c in counts:
        if c > 0:
            p = c / float(L)
            H -= p * math.log2(p)
    Hmax = math.log2(6.0)
    return int(round((H / Hmax) * 1000.0))

with open(in_path) as f:
    blob = f.read().splitlines()
n_ch, n_samp = 0, 0
data = []
for ln in blob:
    if ln.startswith('n_ch='): n_ch = int(ln.split('=',1)[1])
    elif ln.startswith('n_samp='): n_samp = int(ln.split('=',1)[1])
    elif ln.strip() != '':
        try: data.append(int(ln))
        except: pass

flat = np.array(data, dtype=np.int64)
if flat.size != n_ch * n_samp:
    sys.stderr.write('size-mismatch: got ' + str(flat.size) + ' expect ' + str(n_ch*n_samp) + '\n'); sys.exit(4)
flat = flat.reshape(n_ch, n_samp)

per_scale_means = []
for s in SCALES:
    chvals = []
    for ci in range(n_ch):
        cg = coarse_grain_floor(flat[ci, :], s)
        v = pe_x1000(cg)
        if v is not None: chvals.append(v)
    if chvals:
        per_scale_means.append(int(round(sum(chvals) / float(len(chvals)))))
    else:
        per_scale_means.append(None)

valid = [v for v in per_scale_means if v is not None]
overall = int(round(sum(valid) / float(len(valid)))) if valid else None

with open(out_path, 'w') as f:
    f.write('pe_x1000=' + (str(overall) if overall is not None else 'NA') + '\n')
    for i, s in enumerate(SCALES):
        v = per_scale_means[i]
        f.write('pe_mean_scale' + str(s) + '_x1000=' + (str(v) if v is not None else 'NA') + '\n')
print('OK pe_x1000=' + (str(overall) if overall is not None else 'NA'))
