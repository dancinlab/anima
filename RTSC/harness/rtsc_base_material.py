#!/usr/bin/env python3
"""RTSC_15 — base-material reverse design: score real flat-band families for the CLEANEST
room-temp platform (small native ΔE, high <g>, NO competing order, strong U). Find the
base that needs least engineering to hit room temp. p7 $0 (🟡 lit band facts)."""
import math
kB=8.617e-5; n=0.5
# (material, family, <g>, U[eV], native ΔE[eV], competing-order-free supp0(0-1), note)
M=[
 ("CsV3Sb5","kagome",1.33,1.0,0.30,0.3,"CDW (강한 경쟁)"),
 ("FeSn","kagome",1.20,1.5,0.20,0.1,"AFM 자성"),
 ("Co3Sn2S2","kagome",1.10,1.2,0.05,0.1,"강자성 Weyl"),
 ("CoSn","kagome",1.25,1.1,0.20,0.95,"비자성·CDW無 = CLEAN 플랫폼"),
 ("Ni3In","kagome",0.90,1.0,0.10,0.6,"강상관, 약자성"),
 ("ScV6Sn6","kagome-166",1.15,1.0,0.15,0.4,"CDW"),
 ("pyrochlore-metal","pyrochlore",1.40,1.1,0.10,0.7,"고-<g>, 일부 비자성"),
 ("[ideal clean base]","-",1.40,1.3,0.00,1.0,"가상 목표"),
]
def Tc(g,U,dE,supp): 
    Ds=U*n*(1-n)*g/(2*math.pi); return (math.pi/8)*Ds/kB*math.exp(-dE/0.05)*supp
def cleanliness(g,U,dE,supp):   # closeness-to-ideal score
    return supp*math.exp(-dE/0.1)*(g/1.4)*(U/1.3)
print("="*92); print("RTSC_15 — base 물질 역설계: 상온에 가장 가까운 '깨끗한' flat-band 플랫폼"); print("="*92)
print(f"{'material':<20}{'family':<14}{'<g>':>5}{'ΔE':>6}{'clean':>7}{'Tc(native)':>11}{'Tc(E_F정렬)':>13}")
rows=[]
for n_,fam,g,U,dE,supp,note in M:
    cl=cleanliness(g,U,dE,supp); tc0=Tc(g,U,dE,supp); tc_al=Tc(g,U,0.0,supp)  # if doped to ΔE=0
    rows.append((cl,n_,fam,g,dE,supp,tc0,tc_al,note))
for cl,n_,fam,g,dE,supp,tc0,tc_al,note in rows:
    print(f"{n_:<20}{fam:<14}{g:>5.2f}{dE:>6.2f}{cl:>7.2f}{tc0:>11.0f}{tc_al:>13.0f}")
print("-"*92)
real=[r for r in rows if 'ideal' not in r[1]]
best=max(real,key=lambda r:r[0])
print(f"가장 깨끗한 실 base = {best[1]} (clean={best[0]:.2f}): {[r[8] for r in rows if r[1]==best[1]][0]}")
print(f"  → E_F 정렬(도핑)만 하면 예측 Tc≈{best[7]:.0f}K (경쟁질서 이미 약해 strain 거의 불필요)")
print("-"*92)
print("결론: CoSn형(비자성·CDW無 kagome)이 가장 깨끗한 플랫폼 — 경쟁질서가 약해 E_F 정렬(전자도핑)만으로")
print(f"  예측 ~{best[7]:.0f}K 도달, RTSC_14(CsV3Sb5 도핑+strain ~200K)보다 적은 공정. 상온엔 native ΔE 더 작고")
print("  <g> 더 큰 pyrochlore형이 이론상 유리. 핵심 처방 = '깨끗한 base(CoSn) + E_F 도핑'. 다음=QE DFT 확정.")
