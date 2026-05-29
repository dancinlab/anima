"""AURA-WEARABLE app — 18-wearable→0: 피질 zone 직접 read/write로 기기 흡수 — zone별 전달 충실도 (runnable toy, numpy).
honest: toy. See verify/wearable_collapse.txt."""
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

def wfid(mod,depth,M=64,snr=15):
    rng=np.random.RandomState(5); x=patt(rng); L=LF(M,3,depth,mod)
    y=L@x+rng.randn(M)*np.sqrt(((L@x)**2).mean())/(10**(snr/20)); return r2(x,inv(L,y,M))
if __name__=="__main__":
    for lbl,dep,mod in [("AR안경->V1-6 d1.2",1.2,"eeg"),("이어버드->A1 d1.5",1.5,"eeg"),("외골격->M1 d1.0",1.0,"meg"),("햅틱->S1 d1.3",1.3,"eeg")]:
        print("%-22s delivery R2=%.3f"%(lbl,wfid(mod,dep)))
