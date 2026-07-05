import sys, os
base = sys.argv[1] if len(sys.argv) > 1 else "."
CHUNK = 1000  # elements per literal (well under clang -fbracket-depth=4096)
def read(name):
    with open(os.path.join(base, name)) as f:
        hd = f.readline().split(); n_ch, n_samp = int(hd[0]), int(hd[1])
        vals = f.read().split()
    return n_ch, n_samp, [float(v) for v in vals]
out = ['// H_6196 generated hidden-channel data (chunked to avoid bracket-depth) — hexa probe']
for fn, name in [("topvar", "samples_topvar.txt"), ("shuffle", "samples_shuffle.txt"), ("random", "samples_random.txt")]:
    n_ch, n_samp, vals = read(name)
    chunks = [vals[i:i+CHUNK] for i in range(0, len(vals), CHUNK)]
    cnames = []
    for ci, ch in enumerate(chunks):
        body = ", ".join(f"{v:.6f}" for v in ch)
        cn = f"_{fn}_c{ci}"
        out.append(f"fn {cn}() -> [float] {{ return [{body}] }}")
        cnames.append(cn)
    expr = " + ".join(f"{cn}()" for cn in cnames)
    out.append(f"pub fn d_{fn}() -> [float] {{ return {expr} }}")
    if fn == "topvar":
        out.append(f"pub fn d_nch() -> int {{ return {n_ch} }}")
        out.append(f"pub fn d_nsamp() -> int {{ return {n_samp} }}")
open(os.path.join(base, "samples_data.hexa"), "w").write("\n".join(out) + "\n")
print(f"wrote chunked samples_data.hexa (n_ch={n_ch} n_samp={n_samp}, {len(vals)} floats/arm, {len(chunks)} chunks)")
