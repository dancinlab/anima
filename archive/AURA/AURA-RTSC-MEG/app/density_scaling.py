"""AURA-RTSC-MEG app — 상온초전도 고밀도 자기센서 read — 채널밀도가 복원율 lever(cryo 비용장벽 제거) (runnable toy, numpy).
honest: toy. See verify/density_scaling.txt."""
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

if __name__=="__main__":
    for M in [32,64,128,256,512]:
        L=LF(M,7,1.5,"meg"); x=patt(np.random.RandomState(1)); y=L@x+np.random.RandomState(3).randn(M)*np.sqrt(((L@x)**2).mean())/30
        print("%4dch read R2=%.3f"%(M,r2(x,inv(L,y,M))))
