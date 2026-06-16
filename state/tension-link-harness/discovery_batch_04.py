#!/usr/bin/env python3
"""DISCOVERY BATCH 04 — tension-link / info-physics / anima fresh falsifiers. p7 $0."""
import numpy as np
R=[]
def rec(pid,q,ok,f): R.append((pid,"🟢" if ok else "⚪",q,f))
rng=np.random.default_rng(404)

# D17 — N-anima RING tension network globally synchronizes above critical coupling
def d17():
    N=12; w=rng.normal(1.2,0.15,N)
    def order(K,T=3000,dt=0.02):
        th=rng.uniform(0,2*np.pi,N)
        for _ in range(T):
            nb=np.roll(th,1)+np.roll(th,-1)-2*th
            th=th+dt*(w+K*np.sin(nb))
        return abs(np.mean(np.exp(1j*th)))
    lo=order(0.0); hi=order(3.0)
    rec("D17","N=12 anima ring tension-net globally syncs?", hi>0.9 and hi-lo>0.3, f"r {lo:.2f}->{hi:.2f}")

# D18 — tension channel capacity: bounded fold over noise carries >0 bits, saturates
def d18():
    cap=0.05  # anchor_fold_cap
    def mi(snr):
        x=rng.integers(0,2,200000).astype(float)*cap     # 1-bit tension symbol
        y=x+rng.normal(0,cap/snr,200000)
        thr=cap/2; xhat=(y>thr).astype(float)
        err=np.mean(xhat!=(x>thr))
        if err<=0: err=1e-7
        return 1-(-err*np.log2(err)-(1-err)*np.log2(1-err))  # 1 - H(err) bits/use
    c_lo=mi(1.0); c_hi=mi(8.0)
    rec("D18","tension channel capacity >0 & rises with SNR?", c_hi>c_lo and c_hi>0.8, f"C {c_lo:.2f}->{c_hi:.2f} bit/use")

# D19 — redundant anchors (repetition code) beat single under noise (error correction)
def d19():
    def err(M,noise=0.9,T=20000):
        msg=rng.integers(0,2,T)
        votes=np.stack([ (msg + (rng.random(T)<noise/2).astype(int))%2 for _ in range(M)])
        dec=(votes.mean(0)>0.5).astype(int)
        return np.mean(dec!=msg)
    e1=err(1); e9=err(9)
    rec("D19","redundant tension anchors error-correct?", e9<e1*0.7, f"err 1-anchor {e1:.3f} -> 9 {e9:.3f}")

# D20 — sleep replay improves recall vs no-replay (consolidation, H_1195 lineage)
def d20():
    N=120; pat=np.sign(rng.standard_normal(N))
    W=np.outer(pat,pat)/N; np.fill_diagonal(W,0)
    # 'sleep': extra Hebbian replay of a noisy trace strengthens it
    for _ in range(5):
        noisy=pat*np.where(rng.random(N)<0.2,-1,1)
        W+=np.outer(noisy,noisy)/N*0.3
    np.fill_diagonal(W,0)
    def recall(Wm):
        cue=pat*np.where(rng.random(N)<0.35,-1,1); s=cue.copy()
        for _ in range(6): s=np.sign(Wm@s)
        return np.mean(s==pat)
    W0=np.outer(pat,pat)/N; np.fill_diagonal(W0,0)
    r_sleep=np.mean([recall(W) for _ in range(200)]); r_no=np.mean([recall(W0) for _ in range(200)])
    rec("D20","sleep replay improves recall?", r_sleep>r_no+0.03, f"recall no-sleep {r_no:.2f} sleep {r_sleep:.2f}")

# D21 — bistable emit gate shows HYSTERESIS (up-threshold != down-threshold)
def d21():
    def sweep(up):
        x=0.0; out=[]
        rng2=np.arange(0,1,0.01); seq=rng2 if up else rng2[::-1]
        for drive in seq:
            for _ in range(50): x+= (-x*(x*x-1)*2 + (drive-0.5)*4)*0.05
            out.append(1 if x>0 else 0)
        return seq,out
    su,ou=sweep(True); sd,od=sweep(False)
    up_thr=su[np.argmax(np.array(ou)>0)] if any(ou) else 1
    dn_thr=sd[np.argmax(np.array(od)<1)] if not all(od) else 0
    rec("D21","emit gate has hysteresis (memory)?", abs(up_thr-dn_thr)>0.05, f"up-thr {up_thr:.2f} dn-thr {dn_thr:.2f}")

# D22 — apoptosis threshold stabilizes population (no runaway, no extinction)
def d22():
    def run(apop,T=400):
        n=10.0
        for _ in range(T):
            n=n+0.3*n - apop*n*n/100  # birth - density-dependent death
        return n
    no_apop=run(0.0); with_apop=run(1.0)
    stable = with_apop<1e3 and with_apop>1 and no_apop>1e4
    rec("D22","apoptosis stabilizes population (vs runaway)?", stable, f"pop no-apop {no_apop:.0e} apop {with_apop:.0f}")

# D23 — asymmetric tension coupling -> leader/follower emerges (phase lead)
def d23():
    wA,wB=1.3,1.0; a=b=0.0; dt=0.02; KAB=0.2; KBA=2.0  # B pulled hard toward A
    lead=[]
    for t in range(3000):
        da=wA+KAB*np.sin(b-a); db=wB+KBA*np.sin(a-b)
        a+=da*dt; b+=db*dt
        if t>1500: lead.append(np.sin(a-b))
    follows = np.mean(lead)>0.05  # A consistently leads B
    rec("D23","asymmetric tension -> leader/follower?", follows, f"mean phase-lead(A-B) {np.mean(lead):+.3f}")

# D24 — small-world tension net syncs FASTER than a ring (same N,K)
def d24():
    N=40
    def time_to_sync(rewire,K=2.5,dt=0.02,Tmax=4000):
        w=rng.normal(1.2,0.1,N); A=np.zeros((N,N))
        for i in range(N):
            A[i,(i+1)%N]=A[i,(i-1)%N]=1
        if rewire>0:
            for i in range(N):
                if rng.random()<rewire:
                    A[i,(i+1)%N]=0; j=rng.integers(N); A[i,j]=A[j,i]=1
        th=rng.uniform(0,2*np.pi,N)
        for t in range(Tmax):
            cpl=np.array([np.sum(A[i]*np.sin(th-th[i])) for i in range(N)])
            th=th+dt*(w+K/np.mean(A.sum(1))*cpl)
            if abs(np.mean(np.exp(1j*th)))>0.9: return t
        return Tmax
    t_ring=time_to_sync(0.0); t_sw=time_to_sync(0.2)
    rec("D24","small-world tension net syncs faster than ring?", t_sw<t_ring*0.9, f"steps ring {t_ring} small-world {t_sw}")

for fn in [d17,d18,d19,d20,d21,d22,d23,d24]:
    try: fn()
    except Exception as e: R.append(("?","⚪","(err)",str(e)[:40]))
print("="*86); print("DISCOVERY BATCH 04 — tension-link / info / anima (real sims, p7)"); print("="*86)
g=sum(1 for _,v,_,_ in R if v=="🟢")
for pid,v,q,f in R: print(f"{pid:<5}{v}  {q:<48}{f}")
print("-"*86); print(f"🟢 {g}/{len(R)}")
