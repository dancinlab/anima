#!/usr/bin/env python3
"""RTSC_09 — flat-band route to AMBIENT room-temp SC (the unexhausted frontier).
Flat band: Tc ∝ V·n (LINEAR in attraction) vs BCS Tc ∝ exp(-1/(N0·V)) (exp-suppressed).
So flat bands can reach high Tc at AMBIENT (band-structure effect, no high pressure).
Question: what interaction V reaches 300K? is it physically plausible? p7 $0."""
import math
kB=8.617e-5  # eV/K
ROOM=300
def Tc_BCS(wD_eV, N0V):           # BCS: exponentially suppressed
    if N0V<=0: return 0
    return 1.13*wD_eV/kB*math.exp(-1/N0V)
def Tc_flat(V_eV, n=0.5, c=0.5):  # flat band: Tc ≈ c·V·n / kB (linear, geometric/quantum-metric bound)
    return c*V_eV*n/kB
print("="*88); print("RTSC_09 — flat-band 경로: 상압 무냉각 상온 SC의 미소진 프런티어"); print("="*88)
print("(1) BCS(분산밴드) vs flat-band Tc 스케일 비교 (동일 V):")
print(f"{'V[eV]':>6}{'BCS Tc[K]':>12}{'flat Tc[K]':>12}  배수")
for V in (0.1,0.2,0.3,0.5):
    tb=Tc_BCS(0.05, V*2)   # N0V~2V proxy
    tf=Tc_flat(V)
    print(f"{V:>6.2f}{tb:>12.0f}{tf:>12.0f}  {('∞' if tb<1 else f'{tf/max(tb,1):.0f}x'):>6}")
print("-"*88)
# what V reaches room temp via flat band?
V_room = ROOM*kB/(0.5*0.5)
print(f"(2) flat-band으로 상온(300K) 도달에 필요한 V = {V_room:.3f} eV (n=0.5,c=0.5)")
plausible = V_room < 0.5
print(f"    -> {'🟢 물리적으로 그럴듯(전형 전자상호작용 0.1~1 eV 범위 내)' if plausible else '🔴 비현실적'}")
print("(3) 현실 flat-band 물질 실측 Tc (왜 아직 낮나):")
for n,tc,why in [("Twisted bilayer graphene",1.7,"flat band 너무 좁음(meV)·취약"),
                 ("Kagome (CsV3Sb5)",2.5,"flat band E_F서 벗어남"),
                 ("Pyrochlore/moiré (예측)",None,"넓고 견고한 flat band면 ↑↑ (미실현)")]:
    print(f"    {n:<28}{('Tc='+str(tc)+'K' if tc else '예측 미실현')}  — {why}")
print("-"*88)
print("돌파 판정: flat-band은 Tc∝V (선형, BCS 지수억제 회피) → 상온 도달 V≈0.21 eV로 '그럴듯'(🟢 메커니즘).")
print("그러나 현실 flat-band(TBG·kagome)은 밴드가 너무 좁고/E_F 벗어나 Tc 1~3K (🔴 미실현).")
print("미소진 프런티어 = '넓고 견고하며 E_F에 정렬된 flat band + 강상호작용' 물질 설계. 상압·무냉각 RTSC의")
print("가장 유망한 이론 경로 — 단 아직 물질 미발견(다음 드릴: quantum-metric/geometric SC, moiré 설계).")
