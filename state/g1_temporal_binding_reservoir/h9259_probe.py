"""H_9259 $0 CPU probe — does an UNTRAINED recurrent reservoir supply the D x R
cross-product basis that a frozen feedforward conv (any readout position) lacks?
Frozen bar per card §6. Only a ridge linear readout over target bits is fit.
rho=0 (memory, no products) vs rho>=0.6 isolates PRODUCTS from RETENTION.
XOR target => additive floor is a theorem."""
import numpy as np

SEED = 20260710
rng = np.random.default_rng(SEED)
K = 8; GAP = 24; NBITS = 3; D0 = 0
Rpos = 1 + GAP; T = Rpos + 1
FILLER_VOCAB = 5; VOCAB = K + FILLER_VOCAB; EMB = 24
E = rng.standard_normal((VOCAB, EMB)) / np.sqrt(EMB)

def make_seqs(cells, n_per, r):
    toks, tgt, Ds, Rs = [], [], [], []
    for (d, rr) in cells:
        for _ in range(n_per):
            s = np.empty(T, dtype=int)
            s[D0] = d
            s[1:Rpos] = r.integers(K, VOCAB, size=GAP)
            s[Rpos] = rr
            toks.append(s); tgt.append(d ^ rr); Ds.append(d); Rs.append(rr)
    return np.array(toks), np.array(tgt), np.array(Ds), np.array(Rs)

_FCACHE = {}
def _frozen(key):
    if key not in _FCACHE:
        shape = key[-2:]
        rr = np.random.default_rng(abs(hash(key)) % (2**32))
        _FCACHE[key] = rr.standard_normal(shape) / np.sqrt(shape[0])
    return _FCACHE[key]

DILATIONS = [1, 2, 4, 8]; CH = 48
def conv_trunk(tok):
    N = tok.shape[0]; x = E[tok]
    h = np.tanh(x @ _frozen(('proj', EMB, CH)))
    for k, dil in enumerate(DILATIONS):
        Wc = _frozen(('conv', k, 2*CH, CH))
        pad = np.zeros((N, dil, CH))
        hshift = np.concatenate([pad, h[:, :-dil, :]], axis=1) if dil < T else np.zeros_like(h)
        h = np.tanh(np.concatenate([h, hshift], axis=2) @ Wc)
    return h

def _esn_mats(F, M, rho, seed):
    r = np.random.default_rng(seed)
    Win = r.standard_normal((F, M)) / np.sqrt(F)
    W = r.standard_normal((M, M))
    sr = max(abs(np.linalg.eigvals(W)))
    if sr > 0: W = W * (rho / sr)
    return Win, W

def esn_states(tok, rho, M=300, alpha=0.9, seed=7):
    Win, W = _esn_mats(EMB, M, rho, seed)
    x = E[tok]; h = np.zeros((tok.shape[0], M))
    for t in range(T):
        h = (1-alpha)*h + alpha*np.tanh(x[:, t, :] @ Win + h @ W)
    return h

def esn_from_feats(feat, rho, M=300, alpha=0.9, seed=11):
    Win, W = _esn_mats(feat.shape[2], M, rho, seed)
    h = np.zeros((feat.shape[0], M))
    for t in range(T):
        h = (1-alpha)*h + alpha*np.tanh(feat[:, t, :] @ Win + h @ W)
    return h

def target_bits(tgt):
    return ((tgt[:, None] >> np.arange(NBITS)) & 1).astype(float)

def ridge_eval(Ztr, ytr, Zte, yte, lam=None):
    Ytr = target_bits(ytr) * 2 - 1
    def fit(Z, Y, l): return np.linalg.solve(Z.T@Z + l*np.eye(Z.shape[1]), Z.T@Y)
    if lam is None:
        n = Ztr.shape[0]; idx = rng.permutation(n); cut = int(n*0.8)
        tr, va = idx[:cut], idx[cut:]; best, lam = -1, 1.0
        for c in [1e-2,1e-1,1e0,1e1,1e2]:
            b = ((Ztr[va] @ fit(Ztr[tr], Ytr[tr], c)) > 0).astype(int)
            v = ((b << np.arange(NBITS)).sum(1) == ytr[va]).mean()
            if v > best: best, lam = v, c
    Wr = fit(Ztr, Ytr, lam)
    b = ((Zte @ Wr) > 0).astype(int)
    acc8 = ((b << np.arange(NBITS)).sum(1) == yte).mean()
    bitacc = (b == target_bits(yte)).mean()
    return acc8, bitacc

def probe_D(Ztr, Dtr, Zte, Dte):
    Y = np.eye(K)[Dtr]
    Wr = np.linalg.solve(Ztr.T@Ztr + 1.0*np.eye(Ztr.shape[1]), Ztr.T@Y)
    return ((Zte @ Wr).argmax(1) == Dte).mean()

def swap_margin(Zb, tr_cells, te_cells, r):
    Xtr, ytr, _, _ = make_seqs(tr_cells, 40, r); Ztr = Zb(Xtr)
    Ytr = target_bits(ytr)*2-1
    Wr = np.linalg.solve(Ztr.T@Ztr + 1.0*np.eye(Ztr.shape[1]), Ztr.T@Ytr)
    def sc(cell, fd):
        toks, tgt, _, _ = make_seqs([cell], 8, r); toks[:, D0] = fd
        p = 1/(1+np.exp(-(Zb(toks) @ Wr))); tb = target_bits(tgt)
        return np.prod(np.where(tb>0.5, p, 1-p), axis=1).mean()
    m = []
    for (d, rr) in te_cells:
        pc = sc((d, rr), d)
        oth = [sc((d, rr), dp) for dp in range(K) if dp != d]
        m.append(pc - np.mean(oth))
    return float(np.mean(m))

all_cells = [(d, r) for d in range(K) for r in range(K)]
perm = rng.permutation(len(all_cells))
te_cells = [all_cells[i] for i in sorted(perm[:16])]
tr_cells = [all_cells[i] for i in sorted(perm[16:])]
Xtr, ytr, Dtr, Rtr = make_seqs(tr_cells, 60, rng)
Xte, yte, Dte, Rte = make_seqs(te_cells, 60, rng)

print(f"# H_9259 probe seed={SEED} RF=31 T={T} GAP={GAP} | train {len(tr_cells)} / held-out {len(te_cells)} cells")
print(f"# chance: 8-way=0.125 bit=0.5\n")
print(f"{'arm':<22}{'held8':>8}{'bitacc':>8}{'Dprobe':>8}{'swapM':>9}")

def oh(a, n): return np.eye(n)[a]
def bb(a): return ((a[:,None]>>np.arange(NBITS))&1).astype(float)
for nm, Ztr_, Zte_ in [
    ("oracle-additive", np.concatenate([oh(Dtr,K),oh(Rtr,K)],1), np.concatenate([oh(Dte,K),oh(Rte,K)],1)),
    ("oracle-lookup", (oh(Dtr,K)[:,:,None]*oh(Rtr,K)[:,None,:]).reshape(len(Dtr),-1), (oh(Dte,K)[:,:,None]*oh(Rte,K)[:,None,:]).reshape(len(Dte),-1)),
    ("oracle-bitprod", np.concatenate([bb(Dtr),bb(Rtr),bb(Dtr)*bb(Rtr)],1), np.concatenate([bb(Dte),bb(Rte),bb(Dte)*bb(Rte)],1)),
]:
    a8, ba = ridge_eval(Ztr_, ytr, Zte_, yte)
    print(f"{nm:<22}{a8:>8.3f}{ba:>8.3f}{'-':>8}{'-':>9}")
print()

Hc_tr = conv_trunk(Xtr); Hc_te = conv_trunk(Xte)
for nm, ztr, zte, zb in [
    ("conv-emit", Hc_tr[:,-1,:], Hc_te[:,-1,:], lambda tk: conv_trunk(tk)[:,-1,:]),
    ("conv-pool", Hc_tr.mean(1), Hc_te.mean(1), lambda tk: conv_trunk(tk).mean(1)),
]:
    a8, ba = ridge_eval(ztr, ytr, zte, yte)
    print(f"{nm:<22}{a8:>8.3f}{ba:>8.3f}{probe_D(ztr,Dtr,zte,Dte):>8.3f}{swap_margin(zb,tr_cells,te_cells,rng):>9.3f}")

for rho in [0.0,0.3,0.6,0.9,1.1]:
    ztr = esn_states(Xtr, rho); zte = esn_states(Xte, rho)
    a8, ba = ridge_eval(ztr, ytr, zte, yte)
    sm = swap_margin(lambda tk, rr=rho: esn_states(tk, rr), tr_cells, te_cells, rng)
    print(f"{('esn-rho='+str(rho)):<22}{a8:>8.3f}{ba:>8.3f}{probe_D(ztr,Dtr,zte,Dte):>8.3f}{sm:>9.3f}")

for rho in [0.0, 0.9]:
    ztr = esn_from_feats(Hc_tr, rho); zte = esn_from_feats(Hc_te, rho)
    a8, ba = ridge_eval(ztr, ytr, zte, yte)
    print(f"{('conv->esn rho='+str(rho)):<22}{a8:>8.3f}{ba:>8.3f}{probe_D(ztr,Dtr,zte,Dte):>8.3f}{'-':>9}")
