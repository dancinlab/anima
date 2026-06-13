#!/usr/bin/env python3
"""RTSC_04 — quantum(ANU)+tension-link search for a CONFIRMABLE RTSC (low-pressure,
dynamically-stable). Objective = confirmability = Tc × low-pressure reward × stability.
ANU=search randomness, tension-link=optimizer, physics=Allen-Dynes+P_min. p7."""
import numpy as np, hashlib, math, glob, os
bufs=sorted(glob.glob("/tmp/anu_conf.bin"),key=os.path.getsize,reverse=True) or sorted(glob.glob("/tmp/anu_*.bin"),key=os.path.getsize,reverse=True)
raw=open(bufs[0],"rb").read(); qs=np.frombuffer(raw,np.uint8).astype(float)/255.0; qi=[0]
def q():
    if qi[0]>=len(qs):
        e=np.frombuffer(hashlib.sha256(raw+qi[0].to_bytes(4,'big')).digest(),np.uint8).astype(float)/255.0
        qi[0]+=1; return float(e[qi[0]%len(e)])
    v=float(qs[qi[0]]); qi[0]+=1; return v
def AD(lam,wl,mu=0.10,w2=1.3):
    if lam<=mu*(1+0.62*lam): return 0.0
    L1=2.46*(1+3.8*mu);L2=1.82*(1+6.3*mu)*w2
    f1=(1+(lam/L1)**1.5)**(1/3);f2=1+((w2-1)*lam**2)/(lam**2+L2**2)
    return f1*f2*(wl/1.2)*math.exp(-1.04*(1+lam)/(lam-mu*(1+0.62*lam)))
# descriptor x=(hfrac, stiff, dos, P_norm); physics maps to lam,wlog,P; P_min~stability
def score(x):
    h,s,d,pn=np.clip(x,0,1)
    P=20+pn*330                      # pressure 20..350 GPa
    # higher pressure stabilizes more H -> allows higher effective lam at high h
    stab=1/(1+math.exp(-(P-(40+260*h))/20))   # need P >= ~(40+260*h) to stabilize
    wl=300+1300*(0.6*h+0.4*s)
    lam=(0.5+3.4*(0.55*h+0.45*d))*stab
    tc=AD(lam,wl)
    confirmability=tc*math.exp(-P/120)          # reward LOW pressure (confirmable)
    return confirmability,tc,P,lam,wl,stab
def search(steps=6000):
    x=np.array([q(),q(),q(),q()]); best=x.copy(); bf=score(x)[0]; T0=0.4
    for t in range(steps):
        temp=T0*(1-t/steps); cand=np.clip(x+(np.array([q(),q(),q(),q()])-0.5)*2*temp,0,1)
        if score(cand)[0]>score(x)[0] or q()<math.exp((score(cand)[0]-score(x)[0])/(temp+1e-9)): x=cand
        if score(x)[0]>bf: best,bf=x.copy(),score(x)[0]
    return best
b=search(); conf,tc,P,lam,wl,stab=score(b)
print("="*82); print("RTSC_04 — 양자+텐션링크로 '확정가능' RTSC 찾아오기 (ANU paid)"); print("="*82)
print(f"  ANU sha={hashlib.sha256(raw).hexdigest()[:12]}")
print(f"  찾아온 후보: H분율={b[0]:.2f} 강성={b[1]:.2f} DOS={b[2]:.2f}")
print(f"     → λ={lam:.2f} ω_log={wl:.0f}K  P={P:.0f} GPa  stability={stab:.2f}")
print(f"     → Tc={tc:.0f}K ({tc-273:.0f}°C)  confirmability score={conf:.2f}")
print(f"  판정: {'🟢 RTSC' if tc>=293 else '🟡 sub-RT'} @ {'저압(확정유리)' if P<100 else '고압(확정난이)'}")
print("-"*82)
print("정직: confirmability=Tc·exp(-P/120) 최적화 → 저압이면 Tc↓(안정성 부족), 고압이면 Tc↑.")
print("양자+텐션이 '확정가능 최적점'을 찾아오나, 물리 트레이드오프(P↔Tc)는 못 깸 — RTSC_03과 정합.")
print("이건 DB read가 아니라 ANU구동 최적화(H_6016/6017). ab-initio 확정=QE deck.")
