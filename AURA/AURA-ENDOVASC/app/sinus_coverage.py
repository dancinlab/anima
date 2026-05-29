"""AURA-ENDOVASC app — Synchron 정맥동 혈관내 도달 zone 매핑 — 표면 피질 yes, 심부 no(B3/B5) (runnable toy, numpy).
honest: toy. See verify/sinus_coverage.txt."""
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

ZONES={"M1(SSS)":1,"측두A1(가로동)":1,"후두V1(S자동)":1,"DLPFC(전두)":0,"섬엽(심부)":0,"심부핵":0}
if __name__=="__main__":
    cov=sum(ZONES.values())
    print("정맥동 도달 %d/%d zone"%(cov,len(ZONES)))
    print("도달:", ", ".join(z for z,v in ZONES.items() if v))
    print("미도달:", ", ".join(z for z,v in ZONES.items() if not v))
