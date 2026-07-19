"""H_9259 v2 addendum — close the ESN retention confound.
Pure ESN loses D to fading memory (Dprobe=0). Add retention-preserving readouts:
 - esn-pool  : mean over ALL reservoir states (D-carrying positions included)
 - esn-cat   : [state@R ; state@emit ; mean-pool]  (max retention available to a linear head)
 - esnfeat-pool : conv-features -> ESN, pooled (retention from conv + reservoir products)
If binding STILL floors when retention is restored, the KILL is about PRODUCTS not RETENTION."""
import numpy as np
SEED=20260710; rng=np.random.default_rng(SEED)
K=8; GAP=24; NBITS=3; D0=0; Rpos=1+GAP; T=Rpos+1
FILLER_VOCAB=5; VOCAB=K+FILLER_VOCAB; EMB=24
E=rng.standard_normal((VOCAB,EMB))/np.sqrt(EMB)
def make(cells,n,r):
    tk,tg,Ds,Rs=[],[],[],[]
    for (d,rr) in cells:
        for _ in range(n):
            s=np.empty(T,dtype=int); s[D0]=d; s[1:Rpos]=r.integers(K,VOCAB,size=GAP); s[Rpos]=rr
            tk.append(s); tg.append(d^rr); Ds.append(d); Rs.append(rr)
    return np.array(tk),np.array(tg),np.array(Ds),np.array(Rs)
_FC={}
def frz(k):
    if k not in _FC:
        sh=k[-2:]; r=np.random.default_rng(abs(hash(k))%(2**32)); _FC[k]=r.standard_normal(sh)/np.sqrt(sh[0])
    return _FC[k]
DIL=[1,2,4,8]; CH=48
def conv(tok):
    N=tok.shape[0]; x=E[tok]; h=np.tanh(x@frz(('proj',EMB,CH)))
    for k,dl in enumerate(DIL):
        Wc=frz(('conv',k,2*CH,CH)); pad=np.zeros((N,dl,CH))
        hs=np.concatenate([pad,h[:,:-dl,:]],1) if dl<T else np.zeros_like(h)
        h=np.tanh(np.concatenate([h,hs],2)@Wc)
    return h
def mats(F,M,rho,seed):
    r=np.random.default_rng(seed); Win=r.standard_normal((F,M))/np.sqrt(F); W=r.standard_normal((M,M))
    sr=max(abs(np.linalg.eigvals(W)));  W=W*(rho/sr) if sr>0 else W
    return Win,W
def esn_all(tok,rho,M=300,alpha=0.9,seed=7):
    Win,W=mats(EMB,M,rho,seed); x=E[tok]; h=np.zeros((tok.shape[0],M)); S=[]
    for t in range(T):
        h=(1-alpha)*h+alpha*np.tanh(x[:,t,:]@Win+h@W); S.append(h)
    return np.stack(S,1)  # N,T,M
def esnfeat_all(feat,rho,M=300,alpha=0.9,seed=11):
    Win,W=mats(feat.shape[2],M,rho,seed); h=np.zeros((feat.shape[0],M)); S=[]
    for t in range(T):
        h=(1-alpha)*h+alpha*np.tanh(feat[:,t,:]@Win+h@W); S.append(h)
    return np.stack(S,1)
def tb(t): return ((t[:,None]>>np.arange(NBITS))&1).astype(float)
def rev(Ztr,ytr,Zte,yte):
    Y=tb(ytr)*2-1
    def fit(Z,Yy,l): return np.linalg.solve(Z.T@Z+l*np.eye(Z.shape[1]),Z.T@Yy)
    n=Ztr.shape[0]; idx=rng.permutation(n); c=int(n*0.8); tr,va=idx[:c],idx[c:]; best,lam=-1,1.0
    for cand in [1e-2,1e-1,1e0,1e1,1e2]:
        b=((Ztr[va]@fit(Ztr[tr],Y[tr],cand))>0).astype(int)
        v=((b<<np.arange(NBITS)).sum(1)==ytr[va]).mean()
        if v>best: best,lam=v,cand
    Wr=fit(Ztr,Y,lam); b=((Zte@Wr)>0).astype(int)
    return ((b<<np.arange(NBITS)).sum(1)==yte).mean(),(b==tb(yte)).mean()
def pD(Ztr,Dtr,Zte,Dte):
    Y=np.eye(K)[Dtr]; Wr=np.linalg.solve(Ztr.T@Ztr+np.eye(Ztr.shape[1]),Ztr.T@Y)
    return ((Zte@Wr).argmax(1)==Dte).mean()
allc=[(d,r) for d in range(K) for r in range(K)]; p=rng.permutation(len(allc))
te=[allc[i] for i in sorted(p[:16])]; trn=[allc[i] for i in sorted(p[16:])]
Xtr,ytr,Dtr,Rtr=make(trn,60,rng); Xte,yte,Dte,Rte=make(te,60,rng)
print(f"# v2 retention-fixed arms | chance 8-way=0.125\n{'arm':<24}{'held8':>8}{'bitacc':>8}{'Dprobe':>8}")
Hc_tr=conv(Xtr); Hc_te=conv(Xte)
def report(nm,ztr,zte):
    a8,ba=rev(ztr,ytr,zte,yte); print(f"{nm:<24}{a8:>8.3f}{ba:>8.3f}{pD(ztr,Dtr,zte,Dte):>8.3f}")
for rho in [0.6,0.9,1.1]:
    Sa_tr=esn_all(Xtr,rho); Sa_te=esn_all(Xte,rho)
    report(f"esn-pool rho={rho}", Sa_tr.mean(1), Sa_te.mean(1))
    cat_tr=np.concatenate([Sa_tr[:,Rpos,:],Sa_tr[:,-1,:],Sa_tr.mean(1)],1)
    cat_te=np.concatenate([Sa_te[:,Rpos,:],Sa_te[:,-1,:],Sa_te.mean(1)],1)
    report(f"esn-cat rho={rho}", cat_tr, cat_te)
for rho in [0.9]:
    Fa_tr=esnfeat_all(Hc_tr,rho); Fa_te=esnfeat_all(Hc_te,rho)
    report(f"esnfeat-pool rho={rho}", Fa_tr.mean(1), Fa_te.mean(1))
    cat_tr=np.concatenate([Fa_tr[:,Rpos,:],Fa_tr.mean(1)],1); cat_te=np.concatenate([Fa_te[:,Rpos,:],Fa_te.mean(1)],1)
    report(f"esnfeat-cat rho={rho}", cat_tr, cat_te)
# retention-max control: give linear head BOTH conv-pool (retains D) AND esn products, concatenated
Sa_tr=esn_all(Xtr,0.9); Sa_te=esn_all(Xte,0.9)
best_tr=np.concatenate([Hc_tr.mean(1),Sa_tr.mean(1),Sa_tr[:,Rpos,:]],1)
best_te=np.concatenate([Hc_te.mean(1),Sa_te.mean(1),Sa_te[:,Rpos,:]],1)
report("convpool+esn (max)", best_tr, best_te)
