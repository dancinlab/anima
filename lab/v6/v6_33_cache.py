"""V6_33 cache -- reproduce the EXACT V6_29 held-out positions (byte-identical tau/x/emit/sid) and
ADD the fields the efference-copy slice needs: the mouth's command `cmd = argmax(composed)`, the
next-byte NLL `nll` (Fable's secondary DV), and position-within-sentence `pos`. Deterministic
(same corpus/params as v6_29_cache.py), so tau/x/emit/sid reproduce identically; asserted against
v6_29_cache.npz when present. Engine-native (decode._fwd_logits). $0 laptop.
"""
import sys, os, re
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "core"))
import decode as clm

W_LOC = 8; N_SENT = 420; HELDOUT_FRAC = 0.20; SEED = 7
CORPUS = os.path.expanduser("~/anima-weights/en_general.txt")
_DATE = re.compile(r"^\s*\d{3,4}\s*[–-]"); _YEAR = re.compile(r"\b\d{3,4}\b\s*[–-]\s*[A-Z]")

def prose(txt):
    for line in txt.split("\n"):
        line = line.strip()
        if not line or _DATE.match(line): continue
        for s in re.split(r"(?<=[.!?])\s+", line):
            s = s.strip()
            if not (40 < len(s) < 260) or _YEAR.search(s): continue
            if s.count(",") > 6 or sum(c.isdigit() for c in s) > 12: continue
            if s.endswith((".", "!", "?")): yield s

def softmax(x):
    m = x.max(); e = np.exp(x - m); return e / (e.sum() + 1e-12)
def kl(p, q): return float(np.sum(p * (np.log(p + 1e-12) - np.log(q + 1e-12))))
def ent(p): return float(-np.sum(p * np.log(p + 1e-12)))

def main():
    model = sys.argv[1] if len(sys.argv) > 1 else "lab/v6/trained57.clm"
    out = sys.argv[2] if len(sys.argv) > 2 else "lab/v6/v6_33_cache.npz"
    full = open(CORPUS, encoding="utf-8", errors="ignore").read()
    eval_txt = full[int(len(full) * (1 - HELDOUT_FRAC)):]
    sents = []
    for s in prose(eval_txt):
        sents.append(s)
        if len(sents) >= N_SENT: break
    W = clm.clm_load_weights(model); V = W["V"]
    rng = np.random.default_rng(SEED)
    P = rng.standard_normal((16, V)) / np.sqrt(V)   # same frozen projection as v6_29

    TAU, X, EMIT, SID, CMD, NLL, POS = [], [], [], [], [], [], []
    for si, s in enumerate(sents):
        b = list(s.encode("utf-8")); T = len(b) - 1
        if T < W_LOC + 2: continue
        comp = clm._fwd_logits(W, np.array([float(x) for x in b[:T]], dtype=np.float64), T)
        for pos in range(W_LOC, T):
            loc = b[pos - W_LOC:pos + 1]; tl = len(loc) - 1
            rl = clm._fwd_logits(W, np.array([float(x) for x in loc[:tl]], dtype=np.float64), tl)[tl - 1]
            cp = comp[pos]; pc, pr = softmax(cp), softmax(rl); y = b[pos + 1]
            emit = int(np.argmax(cp) == y and np.argmax(rl) != y)
            srt = np.sort(cp)[::-1]
            TAU.append((P @ (cp - rl)).astype(np.float32))
            X.append(np.array([kl(pc, pr), kl(pr, pc), ent(pc), ent(pr),
                               float(np.argmax(cp) == np.argmax(rl)), float(srt[0] - srt[1])], np.float32))
            EMIT.append(emit); SID.append(si)
            CMD.append(int(np.argmax(cp)))                 # mouth command (byte it would emit)
            NLL.append(float(-np.log(pc[y] + 1e-12)))      # next-byte NLL (secondary DV)
            POS.append(pos - W_LOC)                          # position within sentence
    TAU = np.array(TAU); X = np.array(X); EMIT = np.array(EMIT, np.int8); SID = np.array(SID, np.int32)
    CMD = np.array(CMD, np.int32); NLL = np.array(NLL, np.float32); POS = np.array(POS, np.int32)

    # alignment assertion against v6_29 cache (same deterministic positions)
    ref = "lab/v6/v6_29_cache.npz"
    if os.path.exists(ref):
        d = np.load(ref)
        ok = (len(d["emit"]) == len(EMIT) and np.array_equal(d["emit"].astype(np.int8), EMIT)
              and np.array_equal(d["sid"], SID))
        print(f"# v6_29 alignment: {'OK' if ok else 'MISMATCH'} (emit/sid byte-identical)")
        if not ok:
            print("ABORT: positions diverge from v6_29 cache"); return 3
    np.savez(out, tau=TAU, x=X, emit=EMIT, sid=SID, cmd=CMD, nll=NLL, pos=POS, P=P.astype(np.float32))
    print(f"# V6_33 cache -> {out}  positions={len(EMIT)}  emit_rate={EMIT.mean():.3f}  "
          f"nll_mean={NLL.mean():.3f}  V={V}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
