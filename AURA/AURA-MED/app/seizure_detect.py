"""AURA-MED app — 간질 발작 감지/억제 — N1 고샘플링이 RNS보다 빠른 검출(의학 응용) (runnable toy, numpy).
honest: toy. See verify/seizure_detect.txt."""
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

def detect(fs,thr=3.0):
    rng=np.random.RandomState(7); T=int(fs*2); b=rng.randn(T); on=int(fs*1.0)
    b[on:on+int(fs*0.3)]+=rng.randn(int(fs*0.3))*4.0; w=max(2,int(fs*0.02))
    for t in range(on,T-w):
        if b[t:t+w].std()>thr: return 1000*(t-on)/fs
    return None
if __name__=="__main__":
    for lbl,fs in [("N1 (20kHz)",20000),("scalp EEG (256Hz)",256),("RNS (~250Hz)",250)]:
        lat=detect(fs); print("%-18s detect latency=%.2f ms"%(lbl,lat) if lat is not None else "%s miss"%lbl)
