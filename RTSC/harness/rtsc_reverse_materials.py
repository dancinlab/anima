#!/usr/bin/env python3
"""RTSC_13 — REVERSE: plug REAL materials into the flat-band SC model. Why no room-temp
SC despite favorable quantum geometry? Penalize by flat-band offset ΔE from E_F and
competing-order suppression. ideal-aligned vs realized → the fixable gap. p7 $0 (🟡 lit)."""
import math
kB=8.617e-5
# (material, <tr g>, U[eV], ΔE[eV] flat-band offset from E_F, supp(0-1 competing-order), obsTc[K], why)
M=[
 ("CsV3Sb5 (kagome)",   1.33,1.0,0.30,0.3,2.5,"CDW 경쟁, flat band ~0.3eV 아래"),
 ("FeSn (kagome)",      1.20,1.5,0.20,0.1,0.0,"AFM, flat band off E_F, SC 없음"),
 ("Co3Sn2S2 (kagome)",  1.10,1.2,0.05,0.1,0.0,"강자성 Weyl, SC 없음"),
 ("TBG magic-angle",    0.25,0.05,0.00,0.4,1.7,"flat band AT E_F이나 W~5meV·상관절연 경쟁"),
 ("Ni3In (kagome)",     0.90,1.0,0.10,0.5,0.0,"flat band 근접·강상관"),
 ("[ideal kagome E_F정렬]",1.33,1.2,0.00,1.0,None,"가상: ΔE=0 + 경쟁질서 억제"),
]
def Tc(g,U,dE,supp,n=0.5):
    Ds=U*n*(1-n)*g/(2*math.pi); align=math.exp(-abs(dE)/0.05)
    return (math.pi/8)*Ds/kB*align*supp
print("="*96); print("RTSC_13 — 실물질 역대입: 왜 실재 flat-band 금속은 상온 SC가 안 되나"); print("="*96)
print(f"{'material':<24}{'<g>':>5}{'U':>5}{'ΔE':>6}{'supp':>6}{'predTc':>8}{'obsTc':>7}  why")
print("-"*96)
for n_,g,U,dE,supp,obs,why in M:
    ob="—" if obs is None else f"{obs:.1f}"
    print(f"{n_:<24}{g:>5.2f}{U:>5.1f}{dE:>6.2f}{supp:>6.1f}{Tc(g,U,dE,supp):>8.0f}{ob:>7}  {why}")
print("-"*96)
ideal=[r for r in M if 'ideal' in r[0]][0]
print("결론(역대입): 실 kagome 금속은 quantum metric(<g>~1.1-1.3)은 충분하나—")
print(" (1) flat band이 E_F서 어긋남(ΔE 0.05~0.3eV) → align=exp(-ΔE/0.05) 급감, (2) CDW/자성이 SC 잠식")
print(f" → 관측 Tc 0~2.5K. 이상(ΔE=0+경쟁억제): pred {Tc(ideal[1],ideal[2],0,1):.0f}K = 상온권.")
print("∴ 병목은 이론 아닌 '물질 정렬·경쟁질서'. 고칠 것 = flat band E_F 정렬(도핑/압력/strain)+CDW/자성 억제.")
