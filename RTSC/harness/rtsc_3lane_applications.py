#!/usr/bin/env python3
"""RTSC 3-LANE practical screen — each application has ITS OWN superconductor criteria.
LANE A hoverboard · LANE B fusion magnet (demiurge) · LANE C UFO/propulsion. p7 $0.
lit values (🟡) + application logic (🟢)."""
def lane(title, rows, criteria, verdict):
    print("="*92); print(title); print("  기준:",criteria); print("-"*92)
    for r in rows: print("  "+r)
    print("  → "+verdict); print()

# ---- LANE A : HOVERBOARD ----
lane("LANE A — 호버보드 (자속고정 부상)",
 ["YBCO  Tc93K  P0  Type-II pin0.9  → 🟢 가능 (LN2 77K 냉각) — 실제 Lexus 2015",
  "Hg-1223 Tc133K P0 II → 🟢 가능 (LN2)",
  "Li2MgH16 Tc355K P250GPa → 🔴 무용 (보드에 250GPa 불가)",
  "[dream] 상온상압 II Tc300K → 🟢 무냉각 (미발견)"],
 "상압 필수 + Type-II 자속고정 + 작동온도",
 "냉각 호버보드 🟢 지금 가능(YBCO+LN2); 무냉각 상온 🔴 미해결. 고압 RTSC 무용.")

# ---- LANE B : FUSION MAGNET (demiurge) ----
# tokamak needs HIGH FIELD (≥12-20T), Jc at field; temp can be 20K (cryocooler). P=ambient.
lane("LANE B — 핵융합 고자기장 자석 (demiurge: REBCO)",
 ["REBCO(YBCO tape) Tc93K  Hc2>100T  Jc@20T,20K 매우높음 → 🟢 SPARC/ITER급 20T 자석 실현(20K)",
  "Nb3Sn  Tc18K  Hc2~25T  → 🟢 ITER/CERN 현역(4K) 그러나 ~12-16T 한계",
  "Nb-Ti  Tc9K   Hc2~12T  → 🟢 MRI/저자기장(4K)",
  "Li2MgH16 Tc355K P250GPa → 🔴 자석코일에 고압 불가",
  "[dream] 상온상압 RTSC Hc2>50T → 🟢 무냉각 초고자기장 = 핵융합 비용 급감(미발견)"],
 "상압 + 고임계자기장 Hc2≥20T + Jc@field (온도는 20K cryocooler 허용)",
 "핵융합 자석 🟢 지금 가능(REBCO 20T@20K, SPARC). RTSC 필수 아님 — 다만 상온RTSC면 냉각제거로 비용·크기 급감(업그레이드). RTSC 가장 큰 수혜 = fusion.")

# ---- LANE C : UFO / 반중력·추진 ----
lane("LANE C — UFO (반중력·추진)",
 ["초전도 Meissner 반자성 부상: 실재하나 약함(자기장 필요) → 물체 자체가 떠오르는 반중력 아님",
  "Podkletnov 중력차폐(회전 SC 디스크): 재현 실패 — 🔴 (사이비, 미검증)",
  "초전도 자석 기반 MHD/플라즈마 추진: 가능성 있음(강자석) → 반중력 아닌 전자기 추진",
  "RTSC로 반중력? → 🔴 물리적 근거 없음 (SC는 중력 안 가림)"],
 "반중력 또는 추진을 초전도로 달성?",
 "반중력 UFO 🔴 — 초전도는 중력을 가리지 않음(Podkletnov 재현실패). 단 강한 SC자석은 MHD/플라즈마 전자기 추진엔 유용(반중력 아님). RTSC가 그 자석을 경량화할 뿐.")

print("="*92)
print("3-LANE 종합: 상압 Type-II SC는 (A)호버보드·(B)핵융합 자석 둘 다 '냉각형'으로 이미 실용.")
print("RTSC(상온상압)의 진짜 수혜 = 냉각 제거 → A 무냉각 호버보드 + B 핵융합 비용급감. C UFO반중력은 물리 무관.")
print("∴ RTSC 실용 1순위 타깃 = 핵융합 자석(demiurge). 미해결 핵심 = 상온+상압+Type-II+고Hc2 동시.")
