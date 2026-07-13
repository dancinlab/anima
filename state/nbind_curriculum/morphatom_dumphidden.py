#!/usr/bin/env python3
"""NAT-ATOM (H_9290) — codec-aware dump-hidden for the H_9289 G-PROBE (reference-match gt_step0_gprobe.py).

Encodes each frozen natural-context prompt through the MORPH-2B codec, forwards through a codec-CPT'd
303M, and saves the penultimate (pre-readout) hidden at the LAST position (= the contextualized atom
rep, __last) to an npz keyed exactly like the raw-byte dump so `gt_step0_gprobe.py probe` runs verbatim.
Only two deltas vs the raw-byte dump: (1) codec encoding, (2) real-context framing (constant padding is
OOD — convergence morphatom-gate-py-1). Question it answered: does codec atomicity make held-out predicate
polarity linearly readable where raw bytes fail (N2 held-out probe-acc 0.55 = INFO-ABSENT)? → NO (0.345).

Usage: morphatom_dumphidden.py <ckpt.clm> <gt_prompts.json> <out.npz> --codec <codec.json> [--ctx cpt_M.bytes]
"""
import json, os, sys
import numpy as np

try:
    import anima_py.core.decode as _d
    sys.path.insert(0, os.path.dirname(_d.__file__))
    from anima_py.core import decode as clm
except Exception:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import decode as clm
import morph2b as MB


def _asnp(a):
    return a.get() if hasattr(a, "get") else np.asarray(a)


CKPT = sys.argv[1]
PROMPTS = sys.argv[2]
OUT = sys.argv[3]
CODEC = sys.argv[sys.argv.index("--codec") + 1]
CTXF = sys.argv[sys.argv.index("--ctx") + 1] if "--ctx" in sys.argv else "cpt_M.bytes"
T = 96
SENT = b"\x00\x0a"


def load_enc():
    d = json.load(open(CODEC, encoding="utf-8"))
    mr = {tuple(k.split("\t")): r for r, k in enumerate(d["merges"])}
    t2i = d["tok2id"]
    return lambda t: MB.encode_to_bytes(t, mr, t2i)


def tok_from_bytes(bs, ctx):
    bs = bytes(bs); w = len(SENT)
    n = min(len(bs), T); n -= n % w
    content = bs[len(bs) - n:] if n else b""
    buf = bytes(ctx) + SENT + content
    buf = buf[-T:] if len(buf) >= T else (SENT * ((T - len(buf)) // w + 1))[-(T - len(buf)):] + buf
    return np.frombuffer(buf, dtype=np.uint8).astype(float)


def main():
    W = clm.clm_load_weights(CKPT)
    if not W.get("ok"):
        print("ERROR ckpt not decodable"); return 1
    enc = load_enc()
    ctx = open(CTXF, "rb").read(120)[:60] if os.path.exists(CTXF) else b""
    items = json.load(open(PROMPTS, encoding="utf-8"))["items"]
    out = {}
    for k, it in enumerate(items):
        tok = tok_from_bytes(enc(it["prompt"]), ctx)
        yn = _asnp(clm._fwd_trunk(W, tok, T))          # [T,d] penultimate
        out[it["id"] + "__last"] = yn[-1].astype(np.float32)
        if (k + 1) % 200 == 0:
            print("dumped %d/%d" % (k + 1, len(items)), flush=True)
    np.savez(OUT, **out)
    print("DUMP_DONE %s (%d vecs, d=%d)" % (OUT, len(out), len(next(iter(out.values())))))
    return 0


if __name__ == "__main__":
    sys.exit(main())
