---
id: RTSC_05
slug: lane-hoverboard
title: LANE A 호버보드 — 실용기준은 상압+Type-II 자속고정. 냉각형(YBCO+LN2)은 지금 가능, 무냉각 상온은 미해결. 고압 RTSC는 무용.
domain: rtsc application hoverboard levitation
status_grade: 🟢 (cooled buildable) / 🔴 (no-cooling room-temp open)
since: 2026-06-14
verification_method: application-criteria screen (ambient P + Type-II pinning + temp); 🟡 lit / 🟢 logic
sister: RTSC_06, RTSC_07
verdict: 🟢 냉각 호버보드 가능(YBCO Tc93K+LN2 77K, 상압·자속고정, 실제 Lexus 2015) · 🔴 무냉각 상온 미해결 · 고압 수소화물 RTSC 무용(보드에 250GPa 불가).
---
# RTSC_05 — LANE A 호버보드
> **기준.** 호버보드엔 상압 필수 + Type-II 자속고정 + 작동온도.
## 측정 (rtsc_3lane_applications.py::LANE A)
YBCO Tc93K@상압 II → 🟢 LN2 77K로 가능(Lexus 2015). Hg-1223 133K → 🟢. Li2MgH16 355K@250GPa → 🔴 무용. dream 상온상압 → 미발견.
## 결론
🟢 **냉각 호버보드는 오늘 실현 가능**(상압 Type-II YBCO). 🔴 무냉각(상온) 호버보드는 상압+상온+자속고정 물질 미발견. 실용 기준에선 'Tc 최고'(고압 수소화물)가 아니라 '상압 Type-II'가 왕.
verdict: `RTSC/verdicts/3lane_applications.txt`
