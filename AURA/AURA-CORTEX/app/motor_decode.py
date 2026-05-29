"""AURA-CORTEX app — 운동 의도(손/발/혀/휴식 등 5-class)를 피질 표면 read로 분류 — 커서·의수 제어 BCI (runnable toy, numpy).
honest: toy. See verify/motor_decode.txt."""
import numpy as np
G=10; N=G*G
_grid=np.array([[i,j] for i in range(G) for j in range(G)],float)
def _sens(M,sd): return np.random.RandomState(sd).uniform(0,G-1,size=(M,2))
def _d3(M,sd,depth): return np.sqrt(((_sens(M,sd)[:,None,:]-_grid[None,:,:])**2).sum(-1)+depth**2)
def LF(M,sd,depth,mod):
    D=_d3(M,sd,depth)
    if mod=="eeg": return 1.0/D
    if mod=="meg": return 1.0/D**2
    if mod=="tfus": return np.exp(-D/1.2)*np.exp(-0.10*depth)
    return 1.0/D
def r2(x,xh):
    den=((x-x.mean())**2).sum(); return max(1-((x-xh)**2).sum()/den,-1) if den>0 else 0.0
def patt(rng,K=5): sp=rng.choice(N,K,replace=False); x=np.zeros(N); x[sp]=rng.randn(K)*2; return x
def inv(L,y,M): return L.T@np.linalg.solve(L@L.T+1e-2*np.trace(L@L.T)/M*np.eye(M),y)

mts=[patt(np.random.RandomState(900+k)) for k in range(5)]
def decode(mod,M,snr,depth=1.0):
    L=LF(M,1,depth,mod); Tb=[L@m for m in mts]; acc=0
    for i in range(200):
        k=i%5; y=L@mts[k]; p=np.sqrt((y**2).mean()); y=y+np.random.RandomState(i).randn(M)*(p/(10**(snr/20)))
        acc+=int(np.argmin([((y-tb)**2).sum() for tb in Tb])==k)
    return 100*acc/200
if __name__=="__main__":
    for lbl,mod,M,snr in [("EEG-64","eeg",64,15),("RTSC-MEG-256","meg",256,25),("tFUS-64","tfus",64,15)]:
        print("%-14s 5-class acc=%.1f%% (chance 20%%)"%(lbl,decode(mod,M,snr)))
