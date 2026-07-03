import sys, decode as bg
ckpt, jobs, outp = sys.argv[1], sys.argv[2], sys.argv[3]
W = bg.bg_load(ckpt)
print("[np] loaded", W["vocab"], W["d"], W["nlay"], flush=True)
with open(outp, "w", encoding="utf-8", errors="replace") as f:
    for line in open(jobs):
        line = line.rstrip("\n")
        if line.count("\t") < 2: continue
        rng, tag, seed = line.split("\t", 2)
        r = bg._decode_argmax_W(W, seed, 40)  # greedy argmax, KV-cache
        f.write("%s\t%s\n" % (tag, r["text"].replace("\n"," ").replace("\t"," ")))
        f.flush()
        try: print("[np]", tag, r["text"][:50].encode("ascii","replace").decode(), flush=True)
        except: pass
print("NPDONE", flush=True)
