#!/usr/bin/env python3
# anima-eeg-core/_metrics/lz76_chunked .npy -> ASCII '0'/'1' binarized stream.
# Auto-generated, /tmp-only; raw#9 OK.
import sys, os
try:
    import numpy as np
except ImportError:
    sys.stderr.write('numpy not installed in invoking python\n'); sys.exit(10)
if len(sys.argv) < 3:
    sys.stderr.write('usage: helper <in.npy> <out.txt>\n'); sys.exit(2)
in_path, out_path = sys.argv[1], sys.argv[2]
if not os.path.isfile(in_path):
    sys.stderr.write('input not found: ' + in_path + '\n'); sys.exit(3)
arr = np.load(in_path, allow_pickle=False, mmap_mode='r')
if arr.ndim != 2:
    sys.stderr.write('expected 2-D array, got ndim=' + str(arr.ndim) + '\n'); sys.exit(4)
rows, cols = arr.shape
if rows == 16:
    n_ch, n_samp = rows, cols
    chmajor = arr
elif cols == 16:
    n_ch, n_samp = cols, rows
    chmajor = arr.T
elif rows >= 32 and cols > rows:
    n_ch, n_samp = 16, cols
    chmajor = arr[1:17, :]
elif cols >= 32 and rows > cols:
    n_ch, n_samp = 16, rows
    chmajor = arr.T[1:17, :]
else:
    sys.stderr.write('cannot infer 16ch layout from shape ' + str(arr.shape) + '\n'); sys.exit(5)
n_total = int(n_ch) * int(n_samp)
with open(out_path, 'w') as f:
    f.write('n_ch=' + str(int(n_ch)) + '\n')
    f.write('n_samp=' + str(int(n_samp)) + '\n')
    f.write('n_total=' + str(int(n_total)) + '\n')
    f.write('STREAM\n')
    for c in range(int(n_ch)):
        row = np.asarray(chmajor[c, :], dtype=np.float64)
        m = float(np.median(row))
        bits_u8 = (row > m).astype(np.uint8)
        # Map 0->'0' (0x30), 1->'1' (0x31); ASCII offset add → bytes.
        ascii_buf = (bits_u8 + np.uint8(0x30)).tobytes()
        f.write(ascii_buf.decode('ascii'))
    f.write('\n')
print('OK n_ch=' + str(int(n_ch)) + ' n_samp=' + str(int(n_samp)) + ' n_total=' + str(int(n_total)))
