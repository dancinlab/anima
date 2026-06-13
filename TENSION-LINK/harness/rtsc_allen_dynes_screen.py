#!/usr/bin/env python3
"""RTSC SCREEN — Allen-Dynes (1975) Tc from electron-phonon coupling (λ, ω_log, μ*).
Published DFT/experimental EPC values for hydride superconductor candidates; compute
Tc, flag RTSC (Tc>=293K≈20°C). Formula = 🟢 numerical; λ,ω_log = 🟡 literature.
A true ab-initio discovery needs the QE deck (vc-relax+scf+ph+Eliashberg). p7 $0."""
import math
def allen_dynes(lam, wlog, mustar=0.10, w2_over_wlog=1.3):
    L1=2.46*(1+3.8*mustar); L2=1.82*(1+6.3*mustar)*w2_over_wlog
    f1=(1+(lam/L1)**1.5)**(1/3)
    f2=1+((w2_over_wlog-1)*lam**2)/(lam**2+L2**2)
    expo=math.exp(-1.04*(1+lam)/(lam-mustar*(1+0.62*lam)))
    return f1*f2*(wlog/1.2)*expo
# (name, lambda, omega_log[K], P[GPa], note) — published DFT/exp values
cands=[
 ("Li2MgH16 (pred)", 3.35, 1330, 250, "Sun 2019 — Eliashberg Tc≈473K (ternary RTSC)"),
 ("YH10 (pred)",     2.60, 1282, 250, "predicted near/at RTSC"),
 ("MgH6 (pred)",     3.00, 1100, 300, "predicted"),
 ("Li2MgH16 cons.",  3.00, 1130, 250, "conservative params (lower bound)"),
 ("CSH (retracted)", 2.10, 1400, 267, "2020 claim 288K — RETRACTED"),
 ("LaH10",           2.20, 1130, 170, "measured ≈250–260K (2019)"),
 ("YH9",             2.50, 1100, 200, "measured ≈243K"),
 ("CaH6",            2.70,  970, 150, "measured ≈215K"),
 ("H3S",             2.00, 1320, 200, "measured ≈203K (2015)"),
 ("LaBH8 (pred)",    2.30,  900,  40, "LOW-pressure (~40 GPa) candidate"),
]
print("="*92)
print("RTSC SCREEN — Allen-Dynes Tc (μ*=0.10) — hunting room-temperature superconductors")
print("="*92)
print(f"{'material':<18}{'λ':>5}{'ω_log':>8}{'P[GPa]':>8}{'Tc[K]':>8}{'Tc[°C]':>8}  flag   note")
print("-"*92)
rows=sorted(((allen_dynes(l,w),n,l,w,P,nt) for n,l,w,P,nt in cands),reverse=True)
rtsc=[]
for tc,n,l,w,P,nt in rows:
    flag="🟢 RTSC" if tc>=293 else ("🟡 near" if tc>=250 else "      ")
    if tc>=293: rtsc.append(n)
    print(f"{n:<18}{l:>5.2f}{w:>8}{P:>8}{tc:>8.0f}{tc-273:>8.0f}  {flag:<7} {nt}")
print("-"*92)
print(f"🟢 RTSC candidates (Tc>=293K=20°C): {', '.join(rtsc) if rtsc else 'none'}")
top=rows[0]; print(f"TOP: {top[1]}  Allen-Dynes Tc≈{top[0]:.0f}K ({top[0]-273:.0f}°C) @ {top[4]} GPa")
print("HONEST: predicted (not synthesized); high pressure; Allen-Dynes underestimates vs")
print("full Eliashberg (Li2MgH16 Eliashberg≈473K). Ab-initio confirm = QE deck fire.")
