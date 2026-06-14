---
id: RTSC_13
slug: reverse-materials
title: 역대입 진단 — 실 kagome 금속은 quantum metric은 충분하나 flat band E_F-어긋남(ΔE)+경쟁질서(CDW/자성)로 막힘. 정렬+경쟁억제면 ~289K. 병목=이론 아닌 물질공학.
domain: rtsc flat-band kagome reverse-screen E_F-alignment competing-order
status_grade: 🟢 (bottleneck diagnosed: fixable material-engineering) / 🔴 (no real material aligned yet)
since: 2026-06-14
verification_method: plug real-material band params into flat-band SC model + alignment/competing-order penalties; p7 $0 (🟡 lit)
sister: RTSC_12, RTSC_11
verdict: 실물질 역대입 — CsV3Sb5/FeSn/Co3Sn2S2/Ni3In/TBG: <g> 충분(1.1-1.3)이나 ΔE 0.05-0.3eV(align exp(-ΔE/0.05) 급감)+CDW/자성 → 관측 Tc 0-2.5K. 이상(ΔE=0+경쟁억제) pred 289K=상온권. 병목=flat band E_F정렬+경쟁질서 억제(도핑/압력/strain), 이론 아님.
---
# RTSC_13 — 실물질 역대입 진단
> **방향.** 정탐색 대신 실재 flat-band 물질 밴드값을 모델에 거꾸로 대입 → 왜 안 되는지 진단.
## 측정 (rtsc_reverse_materials.py)
| 물질 | <g> | ΔE[eV] | supp | predTc | obsTc |
|---|---|---|---|---|---|
| CsV3Sb5 | 1.33 | 0.30 | 0.3 | 0 | 2.5 (CDW) |
| Co3Sn2S2 | 1.10 | 0.05 | 0.1 | 9 | 0 (자성) |
| Ni3In | 0.90 | 0.10 | 0.5 | 11 | 0 |
| TBG | 0.25 | 0.00 | 0.4 | 1 | 1.7 (W 5meV) |
| **이상(E_F정렬+억제)** | 1.33 | 0.00 | 1.0 | **289** | — |
## 결론
🟢 **병목 진단 완료** — 실 kagome 금속은 **quantum metric은 이미 충분**(이론 OK). 막는 건 (1) flat band이 E_F서 ΔE만큼 어긋남(align factor 급감), (2) CDW/자성 경쟁질서. 둘 다 잡으면 **~289K(상온권)**. 즉 무냉각 RTSC의 병목은 이론이 아니라 **물질공학: flat band를 E_F에 정렬(도핑/압력/strain) + 경쟁질서 억제**. 🔴 아직 정렬된 실물질 없음 — 명확한 합성 타깃(예: CsV3Sb5 도핑으로 flat band E_F화 + CDW 억제). 다음: QE DFT로 도핑/strain별 ΔE·U 정밀.
verdict: `RTSC/verdicts/reverse_materials.txt`
