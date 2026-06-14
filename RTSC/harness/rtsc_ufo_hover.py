#!/usr/bin/env python3
"""RTSC_19 — UFO as a HOVERCRAFT (SC flux-pinning levitation, NOT antigravity). Scale the
hoverboard mechanism up. Lift = (flux-pinning force) vs gravity. Honest: needs a strong
EXTERNAL field gradient (track) — Earth's field is too weak & uniform for free flight. p7 $0."""
mu0=4e-7*3.141592653589793
g=9.81
def lift_force(Jc, B, layer_m, area, gradient_frac=1.0):
    # pinning force density ~ Jc·B (needs field INHOMOGENEITY to give NET lift; gradient_frac scales it)
    return Jc*B*layer_m*area*gradient_frac
craft_mass=1000.0   # 1-ton UFO
need=craft_mass*g
print("="*82); print("RTSC_19 — UFO = 호버크래프트 (초전도 자속고정 부상, 반중력 아님)"); print("="*82)
print(f"  목표: {craft_mass:.0f}kg 크래프트 부상 (필요 양력 {need:.0f} N)")
print("-"*82)
Jc=1e10  # YBCO type-II critical current density A/m^2
for label,B,grad in [("지구 자기장(자유비행)",5e-5,0.001),
                      ("영구자석 노면 ~0.5T",0.5,1.0),
                      ("자기 트랙 1T(maglev식)",1.0,1.0),
                      ("초전도 트랙 5T",5.0,1.0)]:
    F=lift_force(Jc,B,1e-3,4.0,grad)   # 1mm SC layer, 4 m^2 underside
    ok=F>=need
    print(f"  {label:<22} B={B:>7.0e}T → 양력 {F:>10.2e} N  {'🟢 부상' if ok else '🔴 부족'}")
print("-"*82)
print("결론: 초전도 자속고정 부상은 강한 '외부 자기장 구조(트랙/노면)' 위에서만 큰 양력 →")
print(" • 자기 트랙/노면 위: 🟢 1톤 크래프트도 부상(maglev·호버보드 원리, UFO=대형 호버크래프트 가능).")
print(" • 임의 지면 자유비행: 🔴 지구 자기장(5e-5T)은 약하고 거의 균일 → 순양력 거의 0 (불가).")
print(" • 자체 자기장: 크래프트가 자석을 싣고 '반발할 상대'(지면 도체/자성체) 필요 → inductrack 식 가능.")
print("∴ UFO 호버는 반중력이 아니라 '강자기장 환경(트랙/자성노면)+상온 Type-II SC'로 성립. 임의공간 자유비행 ✗.")
print("  RTSC 연결: 무냉각 상온 Type-II(RTSC_15/16 pyrochlore/CoSn)면 냉각 없이 호버크래프트 실현.")
