#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ATD-1/2 — the decisive crux: byte-LM CE on AUTHORED transferable data → transferable bilinear rep?

Mirror of the #3032 film303 crux, but on a toy byte-LM trained with pure next-token CE (NO role/filler
head — mirror E1 rung-3) on the ATD-0-VALIDATED authored corpus. Shares the validated generator
(latents/operator/target/syllable) from atd0_anchor as SSOT.

  ATD-1a REP-CRUX  : FiLM vs additive predicting the model's own h_joint(a,b) from h_a,h_b on HELD-OUT
                     disjoint concept pairs. delta = R2_FiLM - R2_additive. (film303 verbatim readout math.)
  ATD-1b NONDEGEN  : from h_joint(a,b), linearly decode ground-truth t(z_a,z_b) on held-out. R2 >= 0.5.
  controls         : order-shuffle (drop >= 0.15) · permutation-null (delta_null <= 0.02).
  ATD-2 BEHAV      : greedy-decode held-out payload; per-dim acc vs chance; swapped-target < 0.5x true.
  ladder (lambda)  : lambda in {1,.75,.5,.25,0} transferable fraction; lambda=0 MUST reproduce delta~0 (#3032).

Frozen bars (pre-registered · p7): PASS delta>=+0.10 median & >+0.05 every seed & shuffle-drop>=0.15 &
ATD-1b>=0.5 & perm-null<=0.02 & ATD-2 heldout-acc>=0.40 & swapped<0.5x. KILL delta<=+0.03 (ATD-0 valid).
toy=DIRECTIONAL (a_toy_scale_recheck); 303M core/-decode only=TERMINAL. summer torch, never mini.
"""
import os, sys, json, argparse
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from atd0_anchor import latents, operator, target, syllable, K, D, TRAIN_C, HELD_C

Q = 16                              # quantization levels per payload dim
HEX = "0123456789abcdef"
TRAIN_TPL = ["{h} : ", "obs {h} => ", "{h} ~ "]      # framing templates (payload follows)
EVAL_TPL  = "val {h} : "                              # eval-only template (held-out-template control)

def quant(vec):                     # tanh output (-1,1) or z -> 0..Q-1 hex string, D chars
    q = np.clip(((vec + 1.0) * 0.5 * Q).astype(int), 0, Q - 1)
    return "".join(HEX[i] for i in q)

def build_corpus(lam, seed, coverage=0.6, reversal=0.5, filler="", expose_held=True):
    """single-fact lines (all concepts incl held) render quant(z_c); pair lines render quant(t) with prob
    lam else a per-pair MEMORIZED random payload (collocation, non-generalizing).
    expose_held=True (Cartesian PAIR-holdout): held concepts appear paired WITH TRAIN concepts in training
    (so their compositional rep forms); only held×held pairs are held out for the test. expose_held=False
    (strict CONCEPT-holdout, Fable ATD-0): held concepts only in single-fact lines."""
    z = latents(seed); OP = operator(z)
    rs = np.random.RandomState(seed + 100)
    coll = np.random.RandomState(seed + 200)
    name = [syllable(c) for c in range(K)]
    zq = [quant(np.tanh(z[c] * 1.5)) for c in range(K)]  # single payload = concept latent (bounded)
    lines = []
    # single-fact lines: every concept, multiple templates (train templates only in corpus)
    for c in range(K):
        for tpl in TRAIN_TPL:
            for _ in range(6):
                lines.append(tpl.format(h=name[c]) + zq[c] + " .")
    # pair lines. TEST = held x held (always excluded from corpus). expose_held adds (train,held)+(held,train).
    tt = [(a, b) for a in TRAIN_C for b in TRAIN_C if a != b]
    if expose_held:
        tt += [(a, b) for a in TRAIN_C for b in HELD_C] + [(a, b) for a in HELD_C for b in TRAIN_C]
    rs.shuffle(tt); tt = tt[:int(len(tt) * coverage)]
    memo = {}
    for (a, b) in tt:
        if rs.rand() < lam:
            pay = quant(target(z, OP, a, b))
        else:
            key = (a, b)
            if key not in memo: memo[key] = "".join(HEX[coll.randint(Q)] for _ in range(D))
            pay = memo[key]
        for _ in range(4):
            lines.append(f"{name[a]} + {name[b]} = " + pay + " .")
        if rs.rand() < reversal:                          # also emit (b,a) with its distinct payload
            if rs.rand() < lam: pay2 = quant(target(z, OP, b, a))
            else:
                key = (b, a)
                if key not in memo: memo[key] = "".join(HEX[coll.randint(Q)] for _ in range(D))
                pay2 = memo[key]
            for _ in range(4):
                lines.append(f"{name[b]} + {name[a]} = " + pay2 + " .")
    rs.shuffle(lines)
    body = "\n".join(lines) + "\n"
    if filler:                                            # ATD-5 dilution: prepend natural filler bytes
        body = filler + "\n" + body
    return body, z, OP, name

def train_bytelm(corpus, seed, d_model=256, n_layer=4, n_head=8, block=64, steps=3000, lr=3e-4):
    import torch, torch.nn as nn
    torch.manual_seed(seed)
    dev = "cuda" if torch.cuda.is_available() else "cpu"
    raw = np.frombuffer(corpus.encode("utf-8"), dtype=np.uint8)
    vocab = sorted(set(raw.tolist())); stoi = {b: i for i, b in enumerate(vocab)}; Vs = len(vocab)
    ids = torch.tensor([stoi[b] for b in raw.tolist()], dtype=torch.long, device=dev)

    class Blk(nn.Module):
        def __init__(s):
            super().__init__(); s.l1 = nn.LayerNorm(d_model); s.l2 = nn.LayerNorm(d_model)
            s.at = nn.MultiheadAttention(d_model, n_head, batch_first=True)
            s.mp = nn.Sequential(nn.Linear(d_model, 4*d_model), nn.GELU(), nn.Linear(4*d_model, d_model))
        def forward(s, x):
            T = x.size(1); m = torch.triu(torch.ones(T, T, device=x.device), 1).bool()
            a, _ = s.at(s.l1(x), s.l1(x), s.l1(x), attn_mask=m, need_weights=False)
            x = x + a; return x + s.mp(s.l2(x))
    class LM(nn.Module):
        def __init__(s):
            super().__init__(); s.tk = nn.Embedding(Vs, d_model); s.ps = nn.Embedding(block, d_model)
            s.bk = nn.ModuleList([Blk() for _ in range(n_layer)]); s.lf = nn.LayerNorm(d_model)
            s.hd = nn.Linear(d_model, Vs)
        def forward(s, idx, hidden=False):
            T = idx.size(1); x = s.tk(idx) + s.ps(torch.arange(T, device=idx.device))[None]
            for b in s.bk: x = b(x)
            x = s.lf(x); return x if hidden else s.hd(x)
    m = LM().to(dev); opt = torch.optim.AdamW(m.parameters(), lr=lr); N = len(ids); bs = 64
    m.train()
    for st in range(steps):
        ix = torch.randint(0, N - block - 1, (bs,), device=dev)
        xb = torch.stack([ids[i:i+block] for i in ix]); yb = torch.stack([ids[i+1:i+1+block] for i in ix])
        loss = nn.functional.cross_entropy(m(xb).reshape(-1, Vs), yb.reshape(-1))
        opt.zero_grad(); loss.backward(); opt.step()
    m.eval()
    def last_hidden(text):
        b = list(text.encode("utf-8"))[-block:]
        idx = torch.tensor([[stoi.get(c, 0) for c in b]], device=dev)
        with torch.no_grad(): h = m(idx, hidden=True)[0, -1]
        return h.float().cpu().numpy().astype(np.float64)
    def greedy(prompt, n=D):
        g = prompt
        for _ in range(n):
            b = list(g.encode("utf-8"))[-block:]
            idx = torch.tensor([[stoi.get(c, 0) for c in b]], device=dev)
            with torch.no_grad(): nb = int(m(idx)[0, -1].argmax())
            g += chr(vocab[nb]) if vocab[nb] < 128 else "?"
        return g[len(prompt):]
    return last_hidden, greedy

# ---- readout (film303 verbatim) ----
def pca_fit(X, k):
    mu = X.mean(0); U, S, Vt = np.linalg.svd(X - mu, full_matrices=False); return mu, Vt[:k].T
def r2(p, t): return 1.0 - np.sum((p-t)**2)/np.sum((t-t.mean(0))**2)
def rfit(F, Y, lam=1.0):
    A = np.hstack([F, np.ones((len(F),1))]); return np.linalg.solve(A.T@A+lam*np.eye(A.shape[1]), A.T@Y)
def rpred(w, F): return np.hstack([F, np.ones((len(F),1))])@w

def crux(last_hidden, z, OP, name, seed, d_low=64, n_tr=2000):
    rs = np.random.RandomState(seed + 99)
    allc = TRAIN_C + HELD_C
    hp = "{h} : "                                          # single prompt for rep (train template)
    S = np.stack([last_hidden(hp.format(h=name[c])) for c in allc])
    mu, P = pca_fit(S, d_low); Sl = {c: (S[i]-mu)@P for i, c in enumerate(allc)}
    def pj(pool, k):
        out = set()
        while len(out) < k:
            a, b = int(rs.choice(pool)), int(rs.choice(pool))
            if a != b: out.add((a, b))
        return list(out)
    trp = pj(TRAIN_C, n_tr); tep = [(a, b) for a in HELD_C for b in HELD_C if a != b]
    def joint(pairs): return np.stack([(last_hidden(f"{name[a]} + {name[b]} = ")-mu)@P for a, b in pairs])
    Ytr, Yte = joint(trp), joint(tep)
    ha_tr = np.stack([Sl[a] for a,b in trp]); hb_tr = np.stack([Sl[b] for a,b in trp])
    ha_te = np.stack([Sl[a] for a,b in tep]); hb_te = np.stack([Sl[b] for a,b in tep])
    wa = rfit(np.hstack([ha_tr,hb_tr]), Ytr); add = r2(rpred(wa, np.hstack([ha_te,hb_te])), Yte)
    wf = rfit(np.hstack([ha_tr*hb_tr, ha_tr, hb_tr]), Ytr)
    film = r2(rpred(wf, np.hstack([ha_te*hb_te, ha_te, hb_te])), Yte)
    perm = rs.permutation(len(tep)); hb_sh = hb_te[perm]
    film_sh = r2(rpred(wf, np.hstack([ha_te*hb_sh, ha_te, hb_sh])), Yte)
    # permutation-null: refit FiLM with concept identities permuted among held pool
    pmap = {c: c for c in HELD_C}; hv = list(HELD_C); rs.shuffle(hv); pmap = dict(zip(HELD_C, hv))
    ha_p = np.stack([Sl[pmap[a]] for a,b in tep]); hb_p = np.stack([Sl[pmap[b]] for a,b in tep])
    wf_p = rfit(np.hstack([ha_tr*hb_tr, ha_tr, hb_tr]), Ytr)
    film_null = r2(rpred(wf_p, np.hstack([ha_p*hb_p, ha_p, hb_p])), Yte)
    # ATD-1b non-degeneracy: decode ground-truth t(a,b) from h_joint on held-out
    Gtr = np.stack([target(z, OP, a, b) for a,b in trp]); Gte = np.stack([target(z, OP, a, b) for a,b in tep])
    wg = rfit(Ytr, Gtr); nondeg = r2(rpred(wg, Yte), Gte)
    return dict(add_cross=float(add), film_cross=float(film), delta=float(film-add),
                film_shuffled=float(film_sh), perm_null_delta=float(film_null-add),
                nondegen_r2=float(nondeg), n_train=len(trp), n_test=len(tep))

def behav(greedy, z, OP, name, seed):
    rs = np.random.RandomState(seed + 3)
    hp = [(a, b) for a in HELD_C for b in HELD_C if a != b]; rs.shuffle(hp); hp = hp[:200]
    dims_ok = 0; dims_tot = 0; swap_ok = 0
    for a, b in hp:
        pred = greedy(f"{name[a]} + {name[b]} = ")[:D]
        tru = quant(target(z, OP, a, b)); swp = quant(target(z, OP, b, a))
        for i in range(min(D, len(pred))):
            dims_tot += 1
            if pred[i] == tru[i]: dims_ok += 1
            if i < len(swp) and pred[i] == swp[i]: swap_ok += 1
    return dict(heldout_dim_acc=dims_ok/max(1,dims_tot), swapped_dim_acc=swap_ok/max(1,dims_tot),
                chance=1.0/Q, n=len(hp))

def run_cell(lam, seed, filler=""):
    corpus, z, OP, name = build_corpus(lam, seed, filler=filler)
    lh, gr = train_bytelm(corpus, seed)
    cx = crux(lh, z, OP, name, seed); bh = behav(gr, z, OP, name, seed)
    return dict(lam=lam, seed=seed, corpus_bytes=len(corpus), **cx, **{"behav_"+k: v for k, v in bh.items()})

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lams", default="1.0,0.0")            # crux + mandatory #3032 negative control
    ap.add_argument("--seeds", default="0,1,2")
    ap.add_argument("--out", default="ATD1_RESULT.json")
    a = ap.parse_args()
    lams = [float(x) for x in a.lams.split(",")]; seeds = [int(x) for x in a.seeds.split(",")]
    cells = []
    for lam in lams:
        for sd in seeds:
            c = run_cell(lam, sd); cells.append(c)
            print(f"  lam={lam:.2f} seed={sd}: add={c['add_cross']:.3f} film={c['film_cross']:.3f} "
                  f"delta={c['delta']:+.3f} shuf={c['film_shuffled']:.3f} null={c['perm_null_delta']:+.3f} "
                  f"nondeg={c['nondegen_r2']:.3f} bhv={c['behav_heldout_dim_acc']:.3f}"
                  f"(ch{c['behav_chance']:.3f} swp{c['behav_swapped_dim_acc']:.3f})", flush=True)
    def agg(lam):
        s = [c for c in cells if c["lam"] == lam]
        return dict(lam=lam, med_delta=float(np.median([c["delta"] for c in s])),
                    min_delta=float(np.min([c["delta"] for c in s])),
                    med_add=float(np.median([c["add_cross"] for c in s])),
                    med_film=float(np.median([c["film_cross"] for c in s])),
                    med_shuf_drop=float(np.median([c["film_cross"]-c["film_shuffled"] for c in s])),
                    max_permnull=float(np.max([c["perm_null_delta"] for c in s])),
                    med_nondeg=float(np.median([c["nondegen_r2"] for c in s])),
                    med_behav=float(np.median([c["behav_heldout_dim_acc"] for c in s])),
                    med_swap=float(np.median([c["behav_swapped_dim_acc"] for c in s])), n=len(s))
    ladder = [agg(l) for l in lams]
    a1 = next((x for x in ladder if x["lam"] == 1.0), None)
    a0 = next((x for x in ladder if x["lam"] == 0.0), None)
    verdict = "INCONCLUSIVE"
    if a1:
        # mandatory internal control: lam=0 must reproduce #3032 collapse (delta~0)
        control_ok = (a0 is None) or (a0["med_delta"] <= 0.05)
        strong = (a1["med_delta"] >= 0.10 and a1["min_delta"] > 0.05 and a1["med_shuf_drop"] >= 0.15
                  and a1["max_permnull"] <= 0.02 and a1["med_nondeg"] >= 0.5
                  and a1["med_behav"] >= 0.40 and a1["med_swap"] < 0.5 * a1["med_behav"])
        if not control_ok:
            verdict = "HARNESS-INVALID-lam0-manufactures-bilinearity"
        elif strong:
            verdict = "PASS-AUTHORED-INDUCES-TRANSFERABLE-BILINEAR"
        elif a1["med_delta"] <= 0.03:
            verdict = "KILL-CE-COLLAPSES-TO-ADDITIVE"
    out = dict(probe="ATD-1/2 authored-transferable-data crux (mirror #3032)",
               frozen_bars=dict(pass_delta_med=0.10, pass_delta_min=0.05, shuf_drop=0.15, permnull_max=0.02,
                                nondeg_min=0.5, behav_min=0.40, kill_delta=0.03),
               ladder=ladder, alpha1=a1, alpha0_control=a0, verdict=verdict, cells=cells)
    json.dump(out, open(os.path.join(HERE, a.out), "w"), ensure_ascii=False, indent=1)
    print(f"\nVERDICT: {verdict}")
    if a1: print(f"  lam=1: med_delta={a1['med_delta']:+.3f} min={a1['min_delta']:+.3f} shuf_drop={a1['med_shuf_drop']:.3f} "
                 f"permnull={a1['max_permnull']:+.3f} nondeg={a1['med_nondeg']:.3f} behav={a1['med_behav']:.3f}")
    if a0: print(f"  lam=0 (control, must be ~0): med_delta={a0['med_delta']:+.3f}")

if __name__ == "__main__":
    main()
