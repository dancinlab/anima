#!/usr/bin/env python3
"""FREE RTSC exploration — ignore known candidates; let ANU quantum entropy roam
the FULL periodic table (binary/ternary compositions) over a physical Allen-Dynes
Tc proxy. Report whatever the search surfaces. Heuristic proxy (NOT DFT):
  ω_log ∝ 1/sqrt(reduced mass)  (phonon freq, light elements high)
  λ ∝ light covalent-network fraction × metallic-donor presence
p7 · paid ANU driven."""
import numpy as np, hashlib, math
raw=open("/tmp/anu_free.bin","rb").read()
qs=np.frombuffer(raw,dtype=np.uint8).astype(float)/255.0; qi=[0]
def q():
    if qi[0]>=len(qs):
        e=np.frombuffer(hashlib.sha256(raw+qi[0].to_bytes(4,'big')).digest(),dtype=np.uint8).astype(float)/255.0
        qi[0]+=1; return float(e[qi[0]%len(e)])
    v=float(qs[qi[0]]); qi[0]+=1; return v
# (symbol, atomic mass, valence e-, electronegativity)
E=[("H",1.0,1,2.20),("Li",6.9,1,0.98),("Be",9.0,2,1.57),("B",10.8,3,2.04),
   ("C",12.0,4,2.55),("N",14.0,5,3.04),("O",16.0,6,3.44),("Na",23.0,1,0.93),
   ("Mg",24.3,2,1.31),("Al",27.0,3,1.61),("Si",28.1,4,1.90),("P",31.0,5,2.19),
   ("S",32.1,6,2.58),("K",39.1,1,0.82),("Ca",40.1,2,1.00),("Sc",45.0,3,1.36),
   ("Ti",47.9,4,1.54),("V",50.9,5,1.63),("Y",88.9,3,1.22),("Zr",91.2,4,1.33),
   ("Nb",92.9,5,1.6),("La",138.9,3,1.10),("Ce",140.1,3,1.12)]
def proxy_Tc(comp):
    # comp = list of (idx, count)
    tot=sum(c for _,c in comp); 
    fr=[(i,c/tot) for i,c in comp]
    # omega_log ∝ 1/sqrt(mean mass weighted) — light elements win
    meanmass=sum(f*E[i][1] for i,f in fr)
    wlog=1700.0/math.sqrt(max(meanmass,0.5))
    wlog=min(wlog,2200)
    hfrac=sum(f for i,f in fr if E[i][0] in ("H",))           # hydrogen fraction
    lightcov=sum(f for i,f in fr if E[i][0] in ("H","B","C","Li","Be"))  # light covalent formers
    has_metal=any(E[i][2] in (1,2,3) and E[i][1]>6 for i,_ in comp) # a heavier metal donor
    eneg=[E[i][3] for i,_ in fr]; spread=max(eneg)-min(eneg)
    lam=0.4 + 3.6*lightcov*(0.6+0.4*hfrac) - 0.25*spread + (0.3 if has_metal else 0.0)
    lam=max(0.2,min(lam,4.0))
    # Allen-Dynes
    mu=0.10; w2=1.3; L1=2.46*(1+3.8*mu); L2=1.82*(1+6.3*mu)*w2
    f1=(1+(lam/L1)**1.5)**(1/3); f2=1+((w2-1)*lam**2)/(lam**2+L2**2)
    tc=f1*f2*(wlog/1.2)*math.exp(-1.04*(1+lam)/(lam-mu*(1+0.62*lam)))
    return tc,lam,wlog
def random_comp():
    n=2+int(q()*2)                      # 2 or 3 elements
    idxs=[]
    while len(idxs)<n:
        j=min(int(q()*len(E)),len(E)-1)
        if j not in idxs: idxs.append(j)
    return [(j,1+int(q()*8)) for j in idxs]  # counts 1..8
def fmt(comp):
    return "".join(f"{E[i][0]}{c if c>1 else ''}" for i,c in comp)
seen={}; 
for _ in range(40000):
    c=random_comp(); tc,lam,wl=proxy_Tc(c); key=fmt(c)
    if key not in seen or tc>seen[key][0]: seen[key]=(tc,lam,wl,c)
rank=sorted(seen.values(),reverse=True)[:12]
print("="*82)
print("FREE RTSC EXPLORATION — ANU-quantum roam over full periodic table (no seeding)")
print("="*82)
print(f"{'composition':<16}{'λ':>6}{'ω_log':>8}{'Tc[K]':>8}{'Tc[°C]':>8}  flag")
print("-"*82)
for tc,lam,wl,c in rank:
    flag="🟢 RTSC" if tc>=293 else ("🟡" if tc>=250 else "")
    print(f"{fmt(c):<16}{lam:>6.2f}{wl:>8.0f}{tc:>8.0f}{tc-273:>8.0f}  {flag}")
print("-"*82)
rtsc=[fmt(c) for tc,_,_,c in rank if tc>=293]
print(f"🟢 RTSC (Tc>=293K): {', '.join(rtsc) if rtsc else 'none'}")
print("HONEST: heuristic Tc proxy (ω∝1/√M, λ∝light-covalent×metal) free-roamed by paid")
print("ANU; NOT DFT. Surfaces the physics frontier (light covalent + metal donor). Ab-initio=QE.")
