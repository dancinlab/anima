#!/usr/bin/env python3
# anima-eeg-core/_metrics/hjorth_native fixture -> .npy emitter.
# Auto-generated, /tmp-only; raw#9 OK.
import sys, os
try:
    import numpy as np
except ImportError:
    sys.stderr.write('numpy not installed in invoking python\n'); sys.exit(10)
if len(sys.argv) < 4:
    sys.stderr.write('usage: helper <flat_txt> <out_npy> <n_ch> [n_samp]\n'); sys.exit(2)
flat_path = sys.argv[1]; out_npy = sys.argv[2]; n_ch = int(sys.argv[3])
n_samp = int(sys.argv[4]) if len(sys.argv) >= 5 else -1
vals = []
with open(flat_path, 'r') as f:
    for line in f:
        line = line.strip()
        if line == '': continue
        try:
            vals.append(int(line))
        except ValueError:
            pass
total = len(vals)
if n_samp < 0:
    if total % n_ch != 0:
        sys.stderr.write('flat length ' + str(total) + ' not divisible by n_ch ' + str(n_ch) + '\n'); sys.exit(3)
    n_samp = total // n_ch
expected = n_ch * n_samp
if total < expected:
    sys.stderr.write('flat length ' + str(total) + ' < expected ' + str(expected) + '\n'); sys.exit(4)
arr = np.asarray(vals[:expected], dtype=np.float64).reshape(n_ch, n_samp)
np.save(out_npy, arr.astype(np.float64))
print('OK n_ch=' + str(int(n_ch)) + ' n_samp=' + str(int(n_samp)) + ' path=' + out_npy)
