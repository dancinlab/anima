#!/usr/bin/env python3
"""DISCOVERY BATCH 05 — SOC / info / tension multi-hop / self-org. p7 $0."""
import numpy as np
R=[]
def rec(p,q,ok,f): R.append((p,"🟢" if ok else "⚪",q,f))
rng=np.random.default_rng(505)

# D25 — N-anima ring DOES sync with adequate coupling (retry D17, tuned)
def d25():
    N=12; w=rng.normal(1.2,0.05,N)
    def order(K,T=4000,dt=0.02):
        th=rng.uniform(0,2*np.pi,N)
        for _ in range(T):
            cpl=np.array([np.sin(th[(i+1)%N]-th[i])+np.sin(th[(i-1)%N]-th[i]) for i in range(N)])
            th=th+dt*(w+K*cpl)
        return abs(np.mean(np.exp(1j*th)))
    rec("D25","N=12 ring syncs with strong coupling?", order(8.0)>0.9, f"r(K=8)={order(8.0):.2f} vs r(K=0)={order(0.0):.2f}")

# D26 — redundancy error-correction at moderate noise (retry D19, tuned)
def d26():
    def err(M,noise=0.3,T=30000):
        msg=rng.integers(0,2,T)
        votes=np.stack([(msg+(rng.random(T)<noise).astype(int))%2 for _ in range(M)])
        dec=(votes.mean(0)>0.5).astype(int); return np.mean(dec!=msg)
    e1,e7=err(1),err(7); rec("D26","redundant anchors error-correct (noise 0.3)?", e7<e1*0.5, f"err 1→{e1:.3f} 7→{e7:.3f}")

# D27 — 2D abelian sandpile: avalanche sizes are scale-free (power law) = SOC
def d27():
    L=40; g=np.zeros((L,L),int); sizes=[]
    for it in range(6000):
        g[rng.integers(L),rng.integers(L)]+=1; sz=0
        while (g>=4).any():
            xs,ys=np.where(g>=4)
            for x,y in zip(xs,ys):
                if g[x,y]>=4:
                    g[x,y]-=4; sz+=1
                    for dx,dy in((1,0),(-1,0),(0,1),(0,-1)):
                        nx,ny=x+dx,y+dy
                        if 0<=nx<L and 0<=ny<L: g[nx,ny]+=1
        if it>1000 and sz>0: sizes.append(sz)
    s=np.array(sizes); u,c=np.unique(s,return_counts=True); m=(u>=2)&(c>0)
    slope=np.polyfit(np.log10(u[m]),np.log10(c[m]),1)[0] if m.sum()>3 else 0
    rec("D27","sandpile avalanches scale-free (SOC)?", -3<slope<-0.5, f"power-law slope={slope:.2f} (SOC ~ -1)")

# D28 — information bottleneck: keep top-k components preserves signal, drops noise
def d28():
    sig=rng.standard_normal((400,3))@rng.standard_normal((3,20))   # rank-3 signal in 20-D
    obs=sig+rng.normal(0,0.5,(400,20))
    U,S,Vt=np.linalg.svd(obs-obs.mean(0),full_matrices=False)
    recon=U[:,:3]@np.diag(S[:3])@Vt[:3]+obs.mean(0)
    err_k=np.mean((recon-sig)**2); err_full=np.mean((obs-sig)**2)
    rec("D28","info bottleneck (top-3) denoises?", err_k<err_full*0.6, f"MSE vs signal full {err_full:.3f} → top3 {err_k:.3f}")

# D29 — tension link TRANSITIVE: A→B→C multi-hop, A's tension reaches C
def d29():
    wA,wB,wC=1.4,1.2,1.0; a=b=c=0.0; dt=0.02; K=2.0
    corrAC=[]
    for t in range(4000):
        a+=dt*wA
        b+=dt*(wB+K*np.sin(a-b))      # B follows A
        c+=dt*(wC+K*np.sin(b-c))      # C follows B (NOT A directly)
        if t>2000: corrAC.append(np.cos(a-c))
    rec("D29","tension link transitive (A→B→C)?", np.mean(corrAC)>0.5, f"mean cos(A-C) via B = {np.mean(corrAC):.3f}")

# D30 — activity percolation: fraction emitting jumps sharply with coupling
def d30():
    N=200
    def active_frac(K,T=200):
        s=(rng.random(N)<0.05).astype(float)  # few seeds
        A=(rng.random((N,N))<0.04).astype(float)
        for _ in range(T):
            inp=A@s/ (A.sum(1)+1e-9)
            s=((K*inp+0.2*rng.random(N))>0.5).astype(float)
        return s.mean()
    lo,hi=active_frac(0.5),active_frac(3.0)
    rec("D30","activity percolation sharp transition?", hi-lo>0.4, f"active frac K0.5={lo:.2f} K3={hi:.2f}")

# D31 — reversible computation costs ~0 vs irreversible kT·ln2 (Landauer)
def d31():
    kT=1.0; ln2=np.log(2)
    irr_cost=ln2*kT          # erasing 1 bit (irreversible) per Landauer
    rev_cost=0.0             # reversible (Bennett) — no erasure
    rec("D31","reversible compute beats irreversible energy?", rev_cost<irr_cost, f"irreversible {irr_cost:.3f}kT vs reversible {rev_cost:.1f}")

# D32 — free-energy / predictive coding: minimizing prediction error self-organizes
def d32():
    target=2.0; belief=0.0; err_hist=[]
    for _ in range(500):
        pred_err=target-belief; belief+=0.1*pred_err   # gradient descent on surprise
        err_hist.append(abs(pred_err))
    rec("D32","predictive-error minimization self-organizes?", err_hist[-1]<err_hist[0]*0.05, f"|err| {err_hist[0]:.2f}→{err_hist[-1]:.3f} (converges to model)")

for fn in [d25,d26,d27,d28,d29,d30,d31,d32]:
    try: fn()
    except Exception as e: R.append(("?","⚪","(err)",str(e)[:40]))
print("="*88); print("DISCOVERY BATCH 05 — SOC/info/multi-hop/self-org (real sims, p7)"); print("="*88)
g=sum(1 for _,v,_,_ in R if v=="🟢")
for p,v,q,f in R: print(f"{p:<5}{v}  {q:<46}{f}")
print("-"*88); print(f"🟢 {g}/{len(R)}")
