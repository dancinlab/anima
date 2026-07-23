"""V6_26 (LANE-BUS Step-0) -- does content/context tension have >1 effective dimension? ($0)

The production tension is a scalar: cli/chat.py a0 wiring has ag_g_drive = A's own complement
(the H_9356 tautology), so s = 2*emit_drive - 1 -- ZERO independent dims (Fable's diagnosis,
confirmed in code). LANE-BUS's whole premise is that CONTENT, routed to the pre-softmax logit
row, carries MULTI-dimensional disagreement a scalar cannot host. But H_9576 showed a
deliberately-wide lane folds to one bit. So before building LANE-BUS, test the premise cheaply.

Metric: for a sample of natural held-out sentences, at each position compute
  composed[pos] = model logits given the FULL prefix        (one teacher-forced forward)
  reflex[pos]   = model logits given only the last W bytes  (short-context forward)
  tension[pos]  = composed[pos] - reflex[pos]                (V-dim vector = what broad context adds)
Stack tension vectors -> matrix M [Npos x V]. Effective rank = participation ratio
  PR = (Σσ_i)^2 / Σσ_i^2   (σ = singular values).
PR >> 1  => context tension is genuinely multi-dimensional; the scalar servo discards real
           disagreement -> LANE-BUS has headroom (build warranted).
PR ~ 1-2 => content tension ALSO collapses (H_9576 at the logit row) -> LANE-BUS is built on
           sand; the wall is deeper than the interface. Kills the build cheaply.

Engine-native (decode._fwd_logits). Reuses trained57.clm + natural held-out text.
"""
import sys, os, re, importlib.util
import numpy as np

W_LOC = 8       # reflex local window (bytes)
N_SENT = 60     # sentence sample
HELDOUT_FRAC = 0.20

_DATE = re.compile(r"^\s*\d{3,4}\s*[–-]"); _YEAR = re.compile(r"\b\d{3,4}\b\s*[–-]\s*[A-Z]")
def prose(txt):
    for line in txt.split("\n"):
        line = line.strip()
        if not line or _DATE.match(line): continue
        for s in re.split(r"(?<=[.!?])\s+", line):
            s = s.strip()
            if not (40 < len(s) < 300) or _YEAR.search(s): continue
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

def pr_eff_rank(M):
    # participation ratio of singular values (effective rank)
    M = M - M.mean(0, keepdims=True)
    s = np.linalg.svd(M, compute_uv=False)
    s2 = s * s
    return float((s.sum())**2 / (s2.sum() + 1e-12)) if s.sum() > 0 else 0.0, s

def main():
    model = sys.argv[1] if len(sys.argv) > 1 else "trained57.clm"
    corpus = os.path.expanduser("~/anima-weights/en_general.txt")
    full = open(corpus, encoding="utf-8", errors="ignore").read()
    eval_txt = full[int(len(full)*(1-HELDOUT_FRAC)):]
    sents = []
    for s in prose(eval_txt):
        sents.append(s)
        if len(sents) >= N_SENT: break

    _decode(); import decode as clm
    W = clm.clm_load_weights(model)
    V = W["V"]

    tension_rows = []       # LANE-BUS content tension (composed - reflex)
    composed_rows = []      # for reference: raw logit-row rank
    for s in sents:
        b = list(s.encode("utf-8"))
        T = len(b) - 1
        if T < W_LOC + 2: continue
        comp = clm._fwd_logits(W, np.array([float(x) for x in b[:T]], dtype=np.float64), T)  # [T,V]
        for pos in range(W_LOC, T):
            lo = pos - W_LOC
            loc = b[lo:pos+1]                       # last W_LOC+1 bytes ending at pos
            tl = len(loc) - 1
            rl = clm._fwd_logits(W, np.array([float(x) for x in loc[:tl]], dtype=np.float64), tl)
            tension_rows.append(comp[pos] - rl[tl-1])
            composed_rows.append(comp[pos])

    M = np.array(tension_rows)          # [Npos, V]
    C = np.array(composed_rows)
    pr_t, st = pr_eff_rank(M)
    pr_c, sc = pr_eff_rank(C)
    print(f"# V6_26 LANE-BUS Step-0 -- content-tension dimensionality  (model={os.path.basename(model)})")
    print(f"sample: {len(sents)} sentences, {M.shape[0]} positions, V={V}, local window={W_LOC}B")
    print(f"\nCONTEXT TENSION (composed - reflex) effective rank (participation ratio) = {pr_t:.2f}")
    print(f"  raw composed logit-row effective rank                                  = {pr_c:.2f}")
    print(f"  (production emit tension effective dims = ~0-1, scalar servo)")
    # top singular value share
    top = (st[0]**2) / ((st**2).sum() + 1e-12)
    print(f"  top-1 singular direction explains {top*100:.1f}% of tension variance")
    print()
    if pr_t >= 4:
        print(f"→ MULTI-DIM ({pr_t:.1f}): context tension is genuinely high-dimensional. The scalar")
        print( "  servo discards real disagreement — LANE-BUS has headroom; build WARRANTED.")
    elif pr_t >= 2:
        print(f"→ LOW-DIM ({pr_t:.1f}): some structure but thin. LANE-BUS headroom is marginal;")
        print( "  a wide bus may buy little over a 2-3 dim lane. Proceed cautiously.")
    else:
        print(f"→ COLLAPSED ({pr_t:.1f}): content tension folds to ~1 dim at the logit row (H_9576")
        print( "  at the bus). LANE-BUS is built on sand — the wall is deeper than the interface.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
