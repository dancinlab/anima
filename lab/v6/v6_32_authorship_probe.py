"""V6_32 -- AGENCY wedge, slice 1: does the FROZEN trunk carry an authorship (efference-copy)
signal INDEPENDENT of the driver scalars?  ($0 numpy, laptop)

Redesign context (this session): the 15 "consciousness" lanes are ~3-dim theater -- formulas over
one grounding scalar m (V6_31). R9's "interior faculties blind/absent" is the phenotype; V6_31 is
the cause: faculties were never given INDEPENDENT trained substrate variables. lab-full reconciled:

  Fable -> AGENCY as an authorship/efference-copy head.  ADOPTED.
    Independent variable = a_vec = A . yn on the trunk hidden yn=clm_forward_hidden (post-MoE,
    post-GN, pre-readout -- byte-identical to what the gates decode over). Label auth_t in {0,1} =
    was byte t self-emitted (passed the mouth) or externally supplied? An ACTION-HISTORY fact,
    NOT a function of m/m_field/emit_drive by construction -> cleanest independent substrate var.
  Sol  -> SURPRISE (latent-transition residual). DISSENT, not taken: its independence from m must
    be EARNED empirically (Sol's own pre-mortem predicts REAL fails to beat BASE because tau+x
    already carries the CE innovation); repo also shows recon_err==0 (H_9336) and cb_surprise==0.0
    (H_9398 dead-gauge) in production -- surprise's substrate input is a dead gauge. Agency wins.

This slice = Fable's Leg I (presence AUC) + Leg II (independence beyond drivers) + controls. It is
the SMALLEST honest measurement that can KILL the whole redesign thesis for $0: if the trunk holds
no authorship signal independent of the driver scalars, co-training a faculty head is moot.
Leg III (causal downstream on the V6_29 A3 gate) is the named follow-on, run only if I+II PASS.

In-vitro authorship (labels by construction): for each held-out natural sentence, split at mid.
  prefix = first half (seed).
  OTHER continuation = the true natural second half         -> auth=0 (externally supplied)
  SELF  continuation = trained57's OWN sampled continuation -> auth=1 (self-emitted)
Matched transcripts (prefix+cont) put both classes at the SAME positions => authorship _|_ position
by construction. The trunk hidden while CONSUMING self- vs externally-authored context is the read.

Pre-mortem (Fable, load-bearing): self bytes are model-sampled => high-prob => a probe can hit high
AUC by reading log-prob alone, which IS a driver scalar (recon_err/surp) -> the result collapses
back into the ~3-dim shadow. Three guards, all here: (1) per-byte CE sits INSIDE the drivers-only
baseline so Leg II nets it out; (2) self is sampled at temperature (not greedy) and we report the
self/other CE overlap coefficient -- non-overlap => INVALID; (3) the pedestal arm catches any
surface-statistics shortcut CE can't express.

Engine-native (decode.clm_forward_hidden / _fwd_logits). lab/v6 = DIRECTIONAL ceiling.
"""
import sys, os, re
import numpy as np

# ---- engine (repo-local core; anima_py package has no core symlink here) --------------------
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "core"))
import decode as clm

CORPUS   = os.path.expanduser("~/anima-weights/en_general.txt")
N_PROMPT = 200
HELDOUT  = 0.20          # same tail split family as V6_29
SEED     = 7
TEMP     = 1.0           # self-sampling temperature (>0 => CE overlaps natural; report OVL)
MAXCONT  = 80            # cap continuation bytes per prompt (position-balanced across classes)

_DATE = re.compile(r"^\s*\d{3,4}\s*[–-]"); _YEAR = re.compile(r"\b\d{3,4}\b\s*[–-]\s*[A-Z]")
def prose(txt):
    for line in txt.split("\n"):
        line = line.strip()
        if not line or _DATE.match(line): continue
        for s in re.split(r"(?<=[.!?])\s+", line):
            s = s.strip()
            if not (60 < len(s) < 260) or _YEAR.search(s): continue
            if s.count(",") > 6 or sum(c.isdigit() for c in s) > 12: continue
            if s.endswith((".", "!", "?")): yield s

def softmax_row(x, temp=1.0):
    z = (x - x.max()) / max(temp, 1e-6); e = np.exp(z); return e / (e.sum() + 1e-12)

def sample_self(W, prefix_bytes, n, rng, temp):
    """trained57's own continuation of prefix, n bytes, sampled at temperature."""
    seq = [float(x) for x in prefix_bytes]
    out = []
    for _ in range(n):
        lg = clm._fwd_logits(W, np.array(seq, dtype=np.float64), len(seq))[len(seq) - 1]
        p = softmax_row(lg, temp)
        b = int(rng.choice(len(p), p=p))
        out.append(b); seq.append(float(b))
    return out

def feats_for(W, allbytes, cont_lo, cont_hi):
    """Run the trunk once over the full transcript; return (yn[cont], drivers[cont]) for
    continuation positions [cont_lo, cont_hi). drivers = [CE, entropy, margin, top1_logprob]."""
    T = len(allbytes)
    ta = np.array([float(x) for x in allbytes], dtype=np.float64)
    yn = clm.clm_forward_hidden(W, ta, T)            # [T, d]
    lg = clm._fwd_logits(W, ta, T)                   # [T, V]
    YN, DR = [], []
    for t in range(cont_lo, min(cont_hi, T - 1)):
        p = softmax_row(lg[t], 1.0)
        y = allbytes[t + 1]
        ce = float(-np.log(p[y] + 1e-12))
        H = float(-np.sum(p * np.log(p + 1e-12)))
        srt = np.sort(p)[::-1]
        logp1 = float(np.log(srt[0] + 1e-12))
        YN.append(yn[t].astype(np.float32))
        DR.append(np.array([ce, H, float(srt[0] - srt[1]), logp1], np.float32))
    return YN, DR

def auc(scores, labels):
    """Mann-Whitney rank AUC (tie-averaged)."""
    s = np.asarray(scores, float); y = np.asarray(labels, int)
    _, inv, cnt = np.unique(s, return_inverse=True, return_counts=True)
    csum = np.cumsum(cnt); start = csum - cnt
    avg = (start + csum + 1) / 2.0
    ranks = avg[inv]
    n1 = y.sum(); n0 = len(y) - n1
    if n1 == 0 or n0 == 0: return 0.5
    return float((ranks[y == 1].sum() - n1 * (n1 + 1) / 2.0) / (n1 * n0))

# ---- tiny numpy MLP d->8->1 (Adam) / logistic (hidden=0), grouped 70/30 split ---------------
def train_head(X, y, groups, hidden, seed, epochs=120, lr=5e-3):
    rng = np.random.default_rng(seed)
    d = X.shape[1]
    gids = np.unique(groups); rng.shuffle(gids)
    ntr = int(len(gids) * 0.7)
    tr = np.isin(groups, gids[:ntr]); te = ~tr
    mu = X[tr].mean(0); sd = X[tr].std(0) + 1e-6
    Xtr, Xte = (X[tr] - mu) / sd, (X[te] - mu) / sd
    ytr, yte = y[tr], y[te]
    if hidden > 0:
        W1 = rng.standard_normal((d, hidden)) * (1.0 / np.sqrt(d)); b1 = np.zeros(hidden)
        W2 = rng.standard_normal((hidden, 1)) * (1.0 / np.sqrt(hidden)); b2 = np.zeros(1)
        params = [W1, b1, W2, b2]
    else:
        W1 = rng.standard_normal((d, 1)) * (1.0 / np.sqrt(d)); b1 = np.zeros(1)
        params = [W1, b1]
    m = [np.zeros_like(p) for p in params]; v = [np.zeros_like(p) for p in params]
    b1a, b2a, eps, t = 0.9, 0.999, 1e-8, 0
    n = len(ytr)
    for ep in range(epochs):
        idx = rng.permutation(n)
        for s0 in range(0, n, 256):
            bi = idx[s0:s0 + 256]; xb = Xtr[bi]; yb = ytr[bi].reshape(-1, 1)
            if hidden > 0:
                W1, b1, W2, b2 = params
                h = np.maximum(0, xb @ W1 + b1); z = h @ W2 + b2
                pr = 1 / (1 + np.exp(-z)); g = (pr - yb) / len(bi)
                gW2 = h.T @ g; gb2 = g.sum(0); gh = (g @ W2.T) * (h > 0)
                grads = [xb.T @ gh, gh.sum(0), gW2, gb2]
            else:
                W1, b1 = params
                z = xb @ W1 + b1; pr = 1 / (1 + np.exp(-z)); g = (pr - yb) / len(bi)
                grads = [xb.T @ g, g.sum(0)]
            t += 1
            for i, gr in enumerate(grads):
                m[i] = b1a * m[i] + (1 - b1a) * gr; v[i] = b2a * v[i] + (1 - b2a) * gr * gr
                mh = m[i] / (1 - b1a ** t); vh = v[i] / (1 - b2a ** t)
                params[i] -= lr * mh / (np.sqrt(vh) + eps)
    if hidden > 0:
        W1, b1, W2, b2 = params
        h = np.maximum(0, Xte @ W1 + b1); zt = (h @ W2 + b2).ravel()
    else:
        W1, b1 = params; zt = (Xte @ W1 + b1).ravel()
    return auc(zt, yte)

def overlap_coef(a, b, bins=40):
    lo = min(a.min(), b.min()); hi = max(a.max(), b.max())
    edges = np.linspace(lo, hi, bins + 1)
    ha, _ = np.histogram(a, edges, density=True); hb, _ = np.histogram(b, edges, density=True)
    return float(np.sum(np.minimum(ha, hb) * (edges[1] - edges[0])))

def build(model, sents, rng):
    W = clm.clm_load_weights(model)
    YN, DR, LAB, GRP, CE_SELF, CE_OTHER = [], [], [], [], [], []
    for gi, s in enumerate(sents):
        b = list(s.encode("utf-8"))
        if len(b) < 40: continue
        mid = len(b) // 2
        prefix = b[:mid]; other = b[mid:mid + MAXCONT]
        if len(other) < 8: continue
        selfc = sample_self(W, prefix, len(other), rng, TEMP)
        lo, hi = len(prefix), len(prefix) + len(other)
        yo, do = feats_for(W, prefix + other, lo, hi)
        ys, ds = feats_for(W, prefix + selfc, lo, hi)
        for yy, dd in zip(yo, do): YN.append(yy); DR.append(dd); LAB.append(0); GRP.append(gi); CE_OTHER.append(dd[0])
        for yy, dd in zip(ys, ds): YN.append(yy); DR.append(dd); LAB.append(1); GRP.append(gi); CE_SELF.append(dd[0])
    return (np.array(YN), np.array(DR), np.array(LAB), np.array(GRP),
            np.array(CE_SELF), np.array(CE_OTHER))

def main():
    model = sys.argv[1] if len(sys.argv) > 1 else "lab/v6/trained57.clm"
    ped = sys.argv[2] if len(sys.argv) > 2 else "lab/v6/pedestal57.clm"
    full = open(CORPUS, encoding="utf-8", errors="ignore").read()
    eval_txt = full[int(len(full) * (1 - HELDOUT)):]
    sents = []
    for s in prose(eval_txt):
        sents.append(s)
        if len(sents) >= N_PROMPT: break
    rng = np.random.default_rng(SEED)

    YN, DR, LAB, GRP, CE_S, CE_O = build(model, sents, rng)
    ovl = overlap_coef(CE_S, CE_O); frac1 = LAB.mean()
    print(f"# V6_32 authorship probe -- {model}")
    print(f"positions={len(LAB)}  self%={frac1:.3f}  prompts={len(np.unique(GRP))}")
    print(f"CE overlap(self,other) OVL={ovl:.3f}   self_meanCE={CE_S.mean():.3f} other_meanCE={CE_O.mean():.3f}")

    def trimean(X, y, g, hidden):
        a = [train_head(X, y, g, hidden, sd) for sd in (7, 11, 4302)]
        return float(np.mean(a)), float(np.std(a))

    au_yn, sd_yn = trimean(YN, LAB, GRP, 8)               # Leg I presence
    au_dr, sd_dr = trimean(DR, LAB, GRP, 0)               # drivers-only baseline
    dAUC = au_yn - au_dr                                  # Leg II independence
    ysh = LAB.copy()                                      # shuffle control
    for g in np.unique(GRP):
        idx = np.where(GRP == g)[0]; ysh[idx] = rng.permutation(ysh[idx])
    au_sh, sd_sh = trimean(YN, ysh, GRP, 8)
    marker = (LAB.reshape(-1, 1) + rng.standard_normal((len(LAB), 1)) * 0.05).astype(np.float32)
    au_pos, _ = trimean(np.hstack([YN, marker]), LAB, GRP, 8)   # positive control (instrument)

    YNp, DRp, LABp, GRPp, _, _ = build(ped, sents, rng)  # pedestal arm
    au_ynp, _ = trimean(YNp, LABp, GRPp, 8)
    au_drp, _ = trimean(DRp, LABp, GRPp, 0)
    dAUC_ped = au_ynp - au_drp
    trained_minus_pedestal = dAUC - dAUC_ped
    chance_lo, chance_hi = au_sh - 2 * sd_sh, au_sh + 2 * sd_sh

    print("\n| leg | metric | value |")
    print("|---|---|---|")
    print(f"| I  | trunk AUC (d->8->1) | {au_yn:.3f} ± {sd_yn:.3f} |")
    print(f"| I  | drivers-only AUC [CE,H,margin,logp] | {au_dr:.3f} ± {sd_dr:.3f} |")
    print(f"| II | dAUC = trunk - drivers | {dAUC:+.3f} |")
    print(f"| ctl| shuffle AUC (realized chance) | {au_sh:.3f} ± {sd_sh:.3f}  (2sd [{chance_lo:.3f},{chance_hi:.3f}]) |")
    print(f"| ctl| pedestal dAUC | {dAUC_ped:+.3f} |")
    print(f"| ctl| trained - pedestal dAUC | {trained_minus_pedestal:+.3f} |")
    print(f"| pos| marker positive control AUC | {au_pos:.3f} |")

    minclass = min(frac1, 1 - frac1)
    invalid = (au_pos < 0.95) or (minclass < 0.20) or (ovl < 0.50)
    present = (au_yn >= 0.70) and (dAUC >= 0.10) and (trained_minus_pedestal >= 0.10) and (chance_lo <= 0.55)
    absent = (au_pos >= 0.95) and ((au_yn < 0.60) or (dAUC < 0.05) or (trained_minus_pedestal < 0.03))
    if invalid:
        v = "INVALID (pos-ctl<0.95 or class<20% or CE non-overlap OVL<0.50)"
    elif present:
        v = "PRESENT-SUBSTRATE (DIRECTIONAL; independent authorship signal in trunk; Leg-III causal = follow-on)"
    elif absent:
        v = "ABSENT (no independent authorship signal beyond driver scalars)"
    else:
        v = "PARTIAL/INCONCLUSIVE (re-power or read the leg that missed)"
    print(f"\nVERDICT: {v}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
