"""V6_29 (LANE-BUS Step-3) Phase A -- frozen feature cache for the emit-gate ablation ($0 laptop).

Reconciled Fable+Sol design. Emit ground truth (Fable option b, non-circular): emit exactly where
real tension existed (reflex alone is WRONG) AND the content lane resolved it (composed is RIGHT):
    emit_t = 1[ argmax(composed_t) == y_{t+1}  AND  argmax(reflex_t) != y_{t+1} ]
y_{t+1} = the actual next byte (external to the gate's inputs -> not circular; p9 natural corpus).

Per position, cache:
  tau[t] in R^16 = P @ (logit_composed - logit_reflex)   (P = FROZEN Gaussian 256->16, one seed)
  x[t]   in R^6  = [KL(c||r), KL(r||c), H(comp), H(refl), 1[c==r], top1-top2 margin of composed]
  emit[t], sid[t] (sentence id, for cluster split/bootstrap)

Emitted to v6_29_cache.npz for the (summer) torch trainer. Engine-native (decode._fwd_logits).
"""
import sys, os, re, importlib.util
import numpy as np

W_LOC = 8; N_SENT = 420; HELDOUT_FRAC = 0.20; SEED = 7
_DATE = re.compile(r"^\s*\d{3,4}\s*[–-]"); _YEAR = re.compile(r"\b\d{3,4}\b\s*[–-]\s*[A-Z]")
def prose(txt):
    for line in txt.split("\n"):
        line = line.strip()
        if not line or _DATE.match(line): continue
        for s in re.split(r"(?<=[.!?])\s+", line):
            s = s.strip()
            if not (40 < len(s) < 260) or _YEAR.search(s): continue
            if s.count(",") > 6 or sum(c.isdigit() for c in s) > 12: continue
            if s.endswith((".","!","?")): yield s

def _decode():
    spec = importlib.util.find_spec("anima_py")
    if spec and spec.submodule_search_locations:
        b = list(spec.submodule_search_locations)[0]
        for c in (os.path.join(b,"core"), b):
            if os.path.isdir(c): sys.path.insert(0, c)
    for c in ("/opt/homebrew/lib/python3.14/site-packages/anima_py/core",):
        if os.path.isdir(c): sys.path.insert(0, c)

def softmax(x):
    m = x.max(); e = np.exp(x - m); return e/(e.sum()+1e-12)
def kl(p, q):
    return float(np.sum(p*(np.log(p+1e-12)-np.log(q+1e-12))))
def ent(p):
    return float(-np.sum(p*np.log(p+1e-12)))

def main():
    model = sys.argv[1] if len(sys.argv) > 1 else "trained57.clm"
    out = sys.argv[2] if len(sys.argv) > 2 else "v6_29_cache.npz"
    full = open(os.path.expanduser("~/anima-weights/en_general.txt"), encoding="utf-8", errors="ignore").read()
    eval_txt = full[int(len(full)*(1-HELDOUT_FRAC)):]
    sents = []
    for s in prose(eval_txt):
        sents.append(s)
        if len(sents) >= N_SENT: break
    _decode(); import decode as clm
    W = clm.clm_load_weights(model); V = W["V"]
    rng = np.random.default_rng(SEED)
    P = rng.standard_normal((16, V)) / np.sqrt(V)      # frozen projection, shared by all arms

    TAU, X, EMIT, SID = [], [], [], []
    for si, s in enumerate(sents):
        b = list(s.encode("utf-8")); T = len(b) - 1
        if T < W_LOC + 2: continue
        comp = clm._fwd_logits(W, np.array([float(x) for x in b[:T]], dtype=np.float64), T)  # [T,V]
        for pos in range(W_LOC, T):
            loc = b[pos-W_LOC:pos+1]; tl = len(loc)-1
            rl = clm._fwd_logits(W, np.array([float(x) for x in loc[:tl]], dtype=np.float64), tl)[tl-1]
            cp = comp[pos]
            pc, pr = softmax(cp), softmax(rl)
            y = b[pos+1]
            emit = int(np.argmax(cp) == y and np.argmax(rl) != y)
            srt = np.sort(cp)[::-1]
            TAU.append((P @ (cp - rl)).astype(np.float32))
            X.append(np.array([kl(pc,pr), kl(pr,pc), ent(pc), ent(pr),
                               float(np.argmax(cp)==np.argmax(rl)), float(srt[0]-srt[1])], np.float32))
            EMIT.append(emit); SID.append(si)
    TAU = np.array(TAU); X = np.array(X); EMIT = np.array(EMIT, np.int8); SID = np.array(SID, np.int32)
    # z-score x on the whole cache (train/test split done in the trainer by sentence)
    np.savez(out, tau=TAU, x=X, emit=EMIT, sid=SID, P=P.astype(np.float32))
    er = EMIT.mean()
    print(f"# V6_29 Phase A cache -> {out}")
    print(f"sentences={len(sents)}  positions={len(EMIT)}  V={V}  tau=16d  x=6d")
    print(f"emit rate = {er:.3f}  (pre-reg envelope [0.05, 0.60] -> {'OK' if 0.05<er<0.60 else 'OUT OF ENVELOPE — re-scope'})")
    return 0 if 0.05 < EMIT.mean() < 0.60 else 3

if __name__ == "__main__":
    sys.exit(main())
