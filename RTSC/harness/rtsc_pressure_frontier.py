#!/usr/bin/env python3
"""RTSC pressure-Tc frontier — toward a CONFIRMABLE material (synthesizability axis).
Allen-Dynes Tc with a pressure-dependent stabilization: hydride H-networks need
P>=P_min to be dynamically stable; below that the structure collapses (Tc->0).
Find the max achievable Tc within a PRESSURE BUDGET (the real route to confirmation).
λ,ω_log,P_min = published DFT/exp; Allen-Dynes computed. p7 $0."""
import math
def AD(lam,wl,mu=0.10,w2=1.3):
    if lam<=mu*(1+0.62*lam): return 0.0
    L1=2.46*(1+3.8*mu); L2=1.82*(1+6.3*mu)*w2
    f1=(1+(lam/L1)**1.5)**(1/3); f2=1+((w2-1)*lam**2)/(lam**2+L2**2)
    return f1*f2*(wl/1.2)*math.exp(-1.04*(1+lam)/(lam-mu*(1+0.62*lam)))
# (name, lam_highP, wlog, P_min[GPa]=dyn-stability floor, status)
M=[
 ("LaH10",        2.2,1130,150,"confirmed 250K@170"),
 ("H3S",          2.0,1320,120,"confirmed 203K@155"),
 ("YH9",          2.5,1100,150,"confirmed 243K@200"),
 ("CaH6",         2.7, 970,150,"confirmed 215K@172"),
 ("LaBH8 (pred)", 2.3, 900, 40,"LOW-P route ~126K@40"),
 ("Li2MgH16(pr)", 3.35,1330,250,"pred 473K@250 (extreme P)"),
 ("LaH10@lowP",   2.2,1130,150,"same, test below P_min"),
 ("MgB2",         0.87,630,  0,"ambient! conf 39K"),
 ("cuprate(amb)", 0.0,   0,  0,"ambient ~133K (non-BCS, not Allen-Dynes)"),
]
def Tc_at(lam,wl,Pmin,P):
    if wl==0: return None                       # non-BCS, skip formula
    if P<Pmin: return 0.0                        # below stability floor → collapses
    return AD(lam,wl)
print("="*88); print("RTSC pressure-Tc frontier — toward a CONFIRMABLE material (lower P = more confirmable)"); print("="*88)
budgets=[300,170,100,50,0]
print(f"{'material':<15}{'P_min':>6}", *[f"{b:>7}" for b in budgets], " status")
print("-"*88)
for n,lam,wl,pmin,st in M:
    row=[]
    for b in budgets:
        t=Tc_at(lam,wl,pmin,b)
        row.append("  n/a " if t is None else (f"{t:>5.0f}K" if t>0 else "   -- "))
    print(f"{n:<15}{pmin:>6}", *[f"{c:>7}" for c in row], f" {st}")
print("-"*88)
# best Tc within each pressure budget
print("달성가능 압력별 최선(BCS hydride):")
for b in budgets:
    best=max(((Tc_at(lam,wl,pm,b) or 0,n) for n,lam,wl,pm,st in M if wl>0), default=(0,"-"))
    tag="🟢 RTSC" if best[0]>=293 else ("🟡" if best[0]>=200 else "")
    print(f"  P<={b:>3} GPa: {best[1]:<14} Tc≈{best[0]:.0f}K {tag}")
print("-"*88)
print("결론: 고-Tc는 >100GPa 필요(미합성·미확정). 저압 루트=LaBH8(~40GPa). 상압(0GPa) BCS는")
print("MgB2 39K가 한계, RTSC 아님. 상압 RTSC는 미해결(cuprate 133K도 non-BCS). 확정 최고=LaH10 250K@170GPa.")
