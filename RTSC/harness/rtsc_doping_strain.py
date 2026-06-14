#!/usr/bin/env python3
"""RTSC_14 — material-engineering optimization: dope+strain a kagome metal (CsV3Sb5-like)
to align the flat band to E_F (ΔE→0) AND suppress CDW, maximizing predicted SC Tc.
Phenomenology matches real CsV3Sb5 (pressure suppresses CDW, enhances SC). ANU search. p7."""
import numpy as np, math, glob, os
kB=8.617e-5; g=1.33; U=1.2; n=0.5
bufs=sorted(glob.glob('/tmp/anu_ds.bin'),key=os.path.getsize,reverse=True) or sorted(glob.glob('/tmp/anu_*.bin'),key=os.path.getsize,reverse=True)
raw=open(bufs[0],'rb').read(); qs=np.frombuffer(raw,np.uint8).astype(float)/255.0; qi=[0]
def q():
    if qi[0]>=len(qs): qi[0]=0
    v=float(qs[qi[0]]); qi[0]+=1; return v
dE0=0.30   # CsV3Sb5 flat band ~0.3eV below E_F (electron-dope to raise E_F to it)
def model(x, eps):
    # x = electron doping (raises E_F toward flat band): ΔE = dE0 - 0.5*x
    dE = abs(dE0 - 0.5*x)
    # strain/pressure eps suppresses CDW: supp rises 0.2→1.0 with eps; but too much strain detunes flat band
    supp = 0.2 + 0.8*(1-math.exp(-eps/0.04))
    detune = 0.15*eps                       # strain also shifts flat band (penalty)
    dE = dE + detune
    align = math.exp(-dE/0.05)
    Ds = U*n*(1-n)*g/(2*math.pi)
    Tc = (math.pi/8)*Ds/kB*align*supp
    return Tc, dE, supp
def search(steps=6000):
    best=None
    bx=q(); be=q()
    bt=model(bx*0.8, be*0.15)[0]; T0=0.4
    for t in range(steps):
        temp=T0*(1-t/steps)
        cx=min(max(bx+(q()-0.5)*2*temp,0),1); ce=min(max(be+(q()-0.5)*2*temp,0),1)
        if model(cx*0.8,ce*0.15)[0]>model(bx*0.8,be*0.15)[0] or q()<math.exp((model(cx*0.8,ce*0.15)[0]-model(bx*0.8,be*0.15)[0])/(temp*300+1e-9)):
            bx,be=cx,ce
    return bx*0.8, be*0.15
print("="*82); print("RTSC_14 — kagome 도핑+strain 최적화: flat band E_F 정렬 + CDW 억제 (CsV3Sb5형)"); print("="*82)
print(f"  출발: CsV3Sb5 flat band ΔE0={dE0}eV below E_F, CDW 경쟁 (관측 Tc~2.5K)")
# grid scan to show landscape
print("  (도핑 x, strain ε) 격자 일부:")
for x in (0.0,0.3,0.6):
    for e in (0.0,0.05,0.1):
        tc,dE,supp=model(x,e); print(f"    x={x:.1f} ε={e:.2f} → ΔE={dE:.3f} supp={supp:.2f} Tc={tc:.0f}K")
xb,eb=search(); tc,dE,supp=model(xb,eb)
print("-"*82)
print(f"  ANU 탐색 최적: 전자도핑 x≈{xb:.2f} (E_F를 flat band로) + strain/압력 ε≈{eb:.3f} (CDW 억제)")
print(f"  → ΔE={dE:.3f}eV  경쟁억제 supp={supp:.2f}  예측 Tc≈{tc:.0f}K ({tc-273:.0f}°C) {'🟢 상온권' if tc>=293 else '🟡'}")
print("-"*82)
print("결론: 전자도핑으로 flat band를 E_F에 정렬(ΔE↓) + 적정 strain/압력으로 CDW 억제(supp↑) →")
print(f"  CsV3Sb5형 kagome서 예측 Tc {tc:.0f}K. 단 strain 과하면 flat band 재이탈(detune). sweet spot 존재.")
print("실제 정합: CsV3Sb5는 압력서 CDW 억제+SC 증가 관측됨 — 모델 방향 일치. 정밀화=QE DFT(도핑/strain별 밴드).")
