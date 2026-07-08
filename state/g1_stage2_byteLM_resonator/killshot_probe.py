#!/usr/bin/env python3
"""
KILL-SHOT control (Fable spec) — measure the circularity of the resonator framebreak in ONE task.
Same superposition-partner-recall task (stage-1 structure, HRR's home turf). ONLY the ATOM SOURCE varies:
  B_handed : atoms = clean random gaussian codebook (factorization handed for free — like stage-1 H_9211)
  B_blind  : atoms = hidden states of a TRAINED tiny byte-LM over the name strings (must derive geometry from data)
  C_handed : additive op, handed atoms (floor control)
Prediction (pre-registered): B_handed HIGH, B_blind ~ chance. The (B_handed - B_blind) margin = the measured
circularity. If B_blind collapses, the operator-escape requires a handed factorization → framebreak is NOT a
transfer lever (only a superposition-capacity lever when atoms are given). 🧱 FALSIFIED-as-G1-lever.
"""
import os, json, math, statistics as st
os.environ.setdefault("CUBLAS_WORKSPACE_CONFIG", ":4096:8")
import numpy as np, torch, torch.nn as nn, torch.nn.functional as Fn
torch.use_deterministic_algorithms(True)
DEV = 'cuda' if torch.cuda.is_available() else 'cpu'

D, N_VOCAB, M_BUNDLE, TRIALS, SEEDS = 512, 256, 8, 2000, 3
NAME_LEN = 6

def circconv(u, v): return torch.fft.irfft(torch.fft.rfft(u)*torch.fft.rfft(v), n=D)
def circcorr(s, u): return torch.fft.irfft(torch.fft.rfft(s)*torch.conj(torch.fft.rfft(u)), n=D)

# tiny byte-LM to produce BLIND atoms (learned geometry) -----------------
class TinyLM(nn.Module):
    def __init__(s, seed):
        super().__init__(); torch.manual_seed(seed)
        s.emb = nn.Embedding(256, 128); s.gru = nn.GRU(128, D, batch_first=True); s.head = nn.Linear(D, 256)
    def hidden(s, idx):
        h, _ = s.gru(s.emb(idx)); return h[:, -1]           # last-step hidden = atom
    def forward(s, idx):
        h, _ = s.gru(s.emb(idx)); return s.head(h)

def make_names(g, n):
    used=set(); out=[]
    while len(out)<n:
        b=bytes(g.integers(97,123,NAME_LEN).tolist())
        if b not in used: used.add(b); out.append(b)
    return out

def blind_atoms(seed, names):
    # train tiny LM to next-byte-predict the name strings, then extract last-hidden as atom
    lm = TinyLM(seed).to(DEV); opt=torch.optim.Adam(lm.parameters(), 3e-3)
    X = torch.full((len(names), NAME_LEN), ord('\n'), dtype=torch.long)
    for i,nm in enumerate(names): X[i]=torch.tensor(list(nm))
    X=X.to(DEV)
    for _ in range(400):
        logits=lm(X[:, :-1]); loss=Fn.cross_entropy(logits.reshape(-1,256), X[:,1:].reshape(-1))
        opt.zero_grad(); loss.backward(); opt.step()
    with torch.no_grad(): A=lm.hidden(X)
    return A/(A.norm(dim=1,keepdim=True)+1e-8)

def handed_atoms(seed, n):
    g=torch.Generator().manual_seed(70000+seed)
    A=torch.randn(n, D, generator=g)/math.sqrt(D)
    return (A/(A.norm(dim=1,keepdim=True)+1e-8)).to(DEV)

def recall(atoms, op):
    rng=np.random.default_rng(9)
    hit=0
    for _ in range(TRIALS):
        idx=rng.choice(len(atoms), 2*M_BUNDLE, replace=False)
        a_ids, b_ids = idx[:M_BUNDLE], idx[M_BUNDLE:]
        A=atoms[a_ids]; B=atoms[b_ids]
        if op=='conv':
            s=sum(circconv(A[i],B[i]) for i in range(M_BUNDLE)); q=rng.integers(M_BUNDLE)
            bh=circcorr(s, atoms[a_ids[q]])
        else:
            s=sum(A[i]+B[i] for i in range(M_BUNDLE)); q=rng.integers(M_BUNDLE)
            bh=s-atoms[a_ids[q]]
        sims=Fn.cosine_similarity(bh[None], atoms, dim=1).clone(); sims[a_ids]=-9
        hit += (int(torch.argmax(sims))==b_ids[q])
    return hit/TRIALS

if __name__=='__main__':
    print(f"device={DEV} killshot handed-vs-blind · D={D} M={M_BUNDLE} seeds={SEEDS} chance={1/(N_VOCAB-M_BUNDLE):.4f}", flush=True)
    res={}
    for s in range(SEEDS):
        g=np.random.default_rng(3000+s); names=make_names(g, N_VOCAB)
        Ah=handed_atoms(s, N_VOCAB); Ab=blind_atoms(s, names)
        # geometry probe: mean |cos| off-diagonal (lower=more orthogonal=HRR-friendly)
        def offdiag_abscos(A):
            C=(A@A.T).abs(); n=A.shape[0]; return float((C.sum()-C.diag().sum())/(n*(n-1)))
        r=dict(B_handed=round(recall(Ah,'conv'),4), B_blind=round(recall(Ab,'conv'),4),
               C_handed=round(recall(Ah,'add'),4),
               geom_handed=round(offdiag_abscos(Ah),4), geom_blind=round(offdiag_abscos(Ab),4))
        res[s]=r
        print(f"seed{s}: B_handed={r['B_handed']:.3f} B_blind={r['B_blind']:.3f} C_handed={r['C_handed']:.3f} "
              f"| offdiag|cos| handed={r['geom_handed']:.3f} blind={r['geom_blind']:.3f}", flush=True)
    def med(k): return round(st.median([res[s][k] for s in res]),4)
    chance=1/(N_VOCAB-M_BUNDLE)
    summ=dict(B_handed_med=med('B_handed'), B_blind_med=med('B_blind'), C_handed_med=med('C_handed'),
              circularity_margin=round(med('B_handed')-med('B_blind'),4), chance=round(chance,4),
              geom_handed_med=med('geom_handed'), geom_blind_med=med('geom_blind'))
    # frozen bars (pre-registered): B_handed high, B_blind ~ chance -> circularity confirmed -> framebreak falsified
    falsified = (summ['B_handed_med']>=0.80 and summ['B_blind_med']<=0.15 and summ['circularity_margin']>=0.50)
    verdict = ('🧱 FALSIFIED-as-G1-lever (B_handed high, B_blind~chance → escape needs handed factorization)'
               if falsified else '🟠 inspect — B_blind not at chance')
    out=dict(spec='killshot_handed_vs_blind', device=DEV, seeds=res, summary=summ, verdict=verdict)
    print("\n=== VERDICT:", verdict, "===")
    print(json.dumps(summ, indent=2))
    open('/tmp/killshot_result.json','w').write(json.dumps(out, indent=2, ensure_ascii=False))
