"""V6_35 (store-channel redesign · $0 ABORT gate) -- BEFORE spending a 303M pool fire on routing
AGENCY through the H_9775 store lane, answer the precondition that gates it, for $0:

    Does a DIFFICULTY-ORTHOGONAL authorship label exist on natural corpus at all?

Reconciled Fable+Sol (lab full 2026-07-23):
- Fable: the store gives authorship a physical value-slot the mouth lacked, BUT it only pays off if
  the SELF/OTHER tag is difficulty-orthogonal; if SELF/OTHER differ in predictability the store just
  re-encodes difficulty = V6_33 rebuilt. The real untested variable is a $0 CORPUS question (can a
  difficulty-balanced mixed-authorship natural corpus be built), with ABORT authority over the fire.
- Sol (dissent, recorded): a toy KV-store passes by construction (H_9775 proved addressed bits
  travel), so only a 303M pool fire is scientifically decisive -- BUT Sol's own pre-mortem concedes
  even a clean pass proves only "episodic source-memory," not agency, and requires a later unlabeled
  causal-credit test before saying AGENCY. And V6_32 already read authorship-beyond-difficulty at
  ΔAUC +0.041 (immaterial). So the $0 difficulty-orthogonality gate legitimately gates the spend:
  if the label is difficulty-confounded, the fire would at best show "source memory != agency".
- We drop Fable's vacuous toy-KV-store step (Sol's objection is correct); we keep Fable's decisive
  corpus difficulty-orthogonality gate and measure it cleanly.

Gate logic (all $0, natural held-out corpus, reuses the V6_32/33 SELF/OTHER construction):
  SELF span  = trained57's own temperature-sampled continuation of a natural prefix (auth=1)
  OTHER span = the true natural continuation (auth=0)
  Per span, difficulty features = [mean NLL, mean entropy, mean top1-top2 margin, length].
  A1 NLL-BALANCE (TOST): are SELF vs OTHER per-span mean-NLL equivalent within +-0.10 nat?
  A2 ORTHOGONALITY: AUC of authorship predicted from difficulty features (AUC_diff). If >> 0.5,
     authorship IS carried by difficulty (a store would re-encode difficulty). Plus the content
     ceiling AUC from the trunk hidden (AUC_content) and the residual ΔAUC = content - difficulty
     (V6_32's Leg-II reframed at span level) -- the difficulty-orthogonal authorship signal.

Decision: GATE-PASS (fire warranted) iff NLL TOST-balanced AND ΔAUC (content beyond difficulty) is
MATERIAL (>= 0.10, the V6_29/34 material floor scaled to AUC) -- i.e. a real difficulty-orthogonal
authorship signal exists for the store to carry. Else GATE-FAIL -> STOP, no spend.

Engine-native (decode.clm_forward_hidden / _fwd_logits). lab/v6 = DIRECTIONAL ceiling.
"""
import sys, os, re
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "core"))
import decode as clm

CORPUS = os.path.expanduser("~/anima-weights/en_general.txt")
N_PROMPT = 300; HELDOUT = 0.20; SEED = 7; TEMP = 1.0; MAXCONT = 80
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

def sample_self(W, prefix, n, rng, temp):
    seq = [float(x) for x in prefix]; out = []
    for _ in range(n):
        lg = clm._fwd_logits(W, np.array(seq, dtype=np.float64), len(seq))[len(seq) - 1]
        b = int(rng.choice(len(lg), p=softmax_row(lg, temp))); out.append(b); seq.append(float(b))
    return out

def span_feats(W, allbytes, lo, hi):
    """mean difficulty features over continuation + mean trunk hidden (content ceiling)."""
    T = len(allbytes); ta = np.array([float(x) for x in allbytes], dtype=np.float64)
    yn = clm.clm_forward_hidden(W, ta, T); lg = clm._fwd_logits(W, ta, T)
    nlls, ents, margs, hids = [], [], [], []
    for t in range(lo, min(hi, T - 1)):
        p = softmax_row(lg[t], 1.0); y = allbytes[t + 1]; srt = np.sort(p)[::-1]
        nlls.append(-np.log(p[y] + 1e-12)); ents.append(-np.sum(p * np.log(p + 1e-12)))
        margs.append(srt[0] - srt[1]); hids.append(yn[t])
    diff = np.array([np.mean(nlls), np.mean(ents), np.mean(margs), float(hi - lo)], np.float32)
    content = np.mean(hids, 0).astype(np.float32)
    return diff, content, float(np.mean(nlls))

def auc(scores, labels):
    s = np.asarray(scores, float); y = np.asarray(labels, int)
    _, inv, cnt = np.unique(s, return_inverse=True, return_counts=True)
    csum = np.cumsum(cnt); avg = (csum - cnt + csum + 1) / 2.0; ranks = avg[inv]
    n1 = y.sum(); n0 = len(y) - n1
    if n1 == 0 or n0 == 0: return 0.5
    return float((ranks[y == 1].sum() - n1 * (n1 + 1) / 2.0) / (n1 * n0))

def logreg_auc(X, y, seed, epochs=300, lr=0.05):
    rng = np.random.default_rng(seed)
    n = len(y); idx = rng.permutation(n); k = int(n * 0.7)
    tr, te = idx[:k], idx[k:]
    mu = X[tr].mean(0); sd = X[tr].std(0) + 1e-9
    Xtr, Xte = (X[tr] - mu) / sd, (X[te] - mu) / sd
    d = X.shape[1]; w = np.zeros(d); b = 0.0
    for _ in range(epochs):
        z = Xtr @ w + b; p = 1 / (1 + np.exp(-z)); g = p - y[tr]
        w -= lr * (Xtr.T @ g / len(tr) + 1e-3 * w); b -= lr * g.mean()
    return auc(Xte @ w + b, y[te])

def tost(a, b, eps=0.10):
    """two one-sided tests: are mean(a), mean(b) equivalent within +-eps? returns (diff, equiv)."""
    d = a.mean() - b.mean()
    se = np.sqrt(a.var(ddof=1) / len(a) + b.var(ddof=1) / len(b))
    return d, (abs(d) + 2 * se) < eps

def main():
    model = sys.argv[1] if len(sys.argv) > 1 else "lab/v6/trained57.clm"
    full = open(CORPUS, encoding="utf-8", errors="ignore").read()
    eval_txt = full[int(len(full) * (1 - HELDOUT)):]
    sents = []
    for s in prose(eval_txt):
        sents.append(s)
        if len(sents) >= N_PROMPT: break
    W = clm.clm_load_weights(model); rng = np.random.default_rng(SEED)

    DIFF, CONT, LAB, NLL_S, NLL_O = [], [], [], [], []
    for s in sents:
        b = list(s.encode("utf-8"))
        if len(b) < 40: continue
        mid = len(b) // 2; prefix = b[:mid]; other = b[mid:mid + MAXCONT]
        if len(other) < 8: continue
        selfc = sample_self(W, prefix, len(other), rng, TEMP)
        lo, hi = len(prefix), len(prefix) + len(other)
        do, co, no = span_feats(W, prefix + other, lo, hi)
        ds, cs, ns = span_feats(W, prefix + selfc, lo, hi)
        DIFF.append(do); CONT.append(co); LAB.append(0); NLL_O.append(no)
        DIFF.append(ds); CONT.append(cs); LAB.append(1); NLL_S.append(ns)
    DIFF = np.array(DIFF); CONT = np.array(CONT); LAB = np.array(LAB, int)
    NLL_S = np.array(NLL_S); NLL_O = np.array(NLL_O)

    # A1 NLL-balance TOST
    d_nll, balanced = tost(NLL_S, NLL_O, eps=0.10)
    # A2 orthogonality: difficulty-only vs content-ceiling authorship AUC (3 seeds)
    au_diff = np.mean([logreg_auc(DIFF, LAB, sd) for sd in (7, 11, 4302)])
    au_cont = np.mean([logreg_auc(CONT, LAB, sd) for sd in (7, 11, 4302)])
    dAUC = au_cont - au_diff

    # A3 DIFFICULTY-MATCHED re-measure (Fable pre-mortem: does the orthogonal signal survive matching?)
    # bin spans by mean-NLL decile; within each bin subsample SELF/OTHER to equal counts; re-measure.
    nll_all = DIFF[:, 0]
    q = np.quantile(nll_all, np.linspace(0, 1, 9)[1:-1]); binid = np.digitize(nll_all, q)
    keep = []
    rng2 = np.random.default_rng(SEED)
    for bb in np.unique(binid):
        idx = np.where(binid == bb)[0]
        s_idx = idx[LAB[idx] == 1]; o_idx = idx[LAB[idx] == 0]
        k = min(len(s_idx), len(o_idx))
        if k == 0: continue
        keep += list(rng2.choice(s_idx, k, replace=False)) + list(rng2.choice(o_idx, k, replace=False))
    keep = np.array(keep)
    dm_nll, dm_bal = tost(NLL_S if False else nll_all[keep][LAB[keep] == 1],
                          nll_all[keep][LAB[keep] == 0], eps=0.10)
    au_diff_m = np.mean([logreg_auc(DIFF[keep], LAB[keep], sd) for sd in (7, 11, 4302)])
    au_cont_m = np.mean([logreg_auc(CONT[keep], LAB[keep], sd) for sd in (7, 11, 4302)])
    dAUC_m = au_cont_m - au_diff_m
    # shuffle control (verdict-integrity: matched-ΔAUC must collapse under label shuffle)
    rng3 = np.random.default_rng(SEED + 1); lab_sh = rng3.permutation(LAB[keep])
    au_cont_sh = np.mean([logreg_auc(CONT[keep], lab_sh, sd) for sd in (7, 11, 4302)])
    au_diff_sh = np.mean([logreg_auc(DIFF[keep], lab_sh, sd) for sd in (7, 11, 4302)])
    dAUC_sh = au_cont_sh - au_diff_sh

    print(f"# V6_35 corpus difficulty-orthogonality gate -- {model}")
    print(f"spans={len(LAB)} (self={LAB.sum()} other={len(LAB)-LAB.sum()})")
    print(f"A1 NLL-balance: self_meanNLL={NLL_S.mean():.3f} other={NLL_O.mean():.3f} "
          f"diff={d_nll:+.3f} -> {'TOST-BALANCED' if balanced else 'NOT balanced'} (eps 0.10)")
    print(f"A2 orthogonality: AUC(difficulty)={au_diff:.3f}  AUC(content-ceiling)={au_cont:.3f}  "
          f"ΔAUC={dAUC:+.3f}")
    print(f"A3 difficulty-MATCHED (n={len(keep)}, NLL diff={dm_nll:+.3f} {'BAL' if dm_bal else 'imbal'}): "
          f"AUC(diff)={au_diff_m:.3f}  AUC(content)={au_cont_m:.3f}  matched-ΔAUC={dAUC_m:+.3f}")
    print(f"   shuffle control: matched-ΔAUC(shuffled labels)={dAUC_sh:+.3f} "
          f"-> {'CLEAN (collapses)' if abs(dAUC_sh) < 0.05 else 'LEAK (does not collapse)'}")

    material = dAUC_m >= 0.10 and abs(dAUC_sh) < 0.05   # decisive: matched ΔAUC real AND shuffle-clean
    if material and dm_bal:
        v = ("GATE-PASS — a difficulty-orthogonal authorship signal SURVIVES difficulty-matching "
             f"(matched-ΔAUC={dAUC_m:+.3f}>=0.10); the 303M store fire is WARRANTED (route the label, "
             "test value-permute + NLL-probe in-vivo per Fable/Sol table).")
    elif not material:
        v = ("GATE-FAIL -> STOP (no spend): authorship-beyond-difficulty COLLAPSES under difficulty-"
             f"matching (matched-ΔAUC={dAUC_m:+.3f}<0.10). The span-level signal was difficulty-"
             "confounded (SELF spans easier); a store would route a difficulty-confounded label = "
             "DIFFICULTY-AGAIN. Content-addressed memory is not agency. Redesign stops claiming faculties.")
    else:
        v = f"GATE-AMBIGUOUS: matched-ΔAUC material but matching left residual imbalance ({dm_nll:+.3f})."
    print(f"\nVERDICT: {v}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
