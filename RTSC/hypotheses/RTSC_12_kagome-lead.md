---
id: RTSC_12
slug: kagome-lead
title: kagome 고-quantum-metric flat band = 무냉각 상온상압 RTSC의 현실적 리드 — 상온 도달 U≈1.24eV(현실적!). quantum metric 큰 flat band일수록 상온이 현실 결합으로 가능. 실 후보 CsV3Sb5·FeSn·Co3Sn2S2.
domain: rtsc flat-band kagome quantum-geometry ambient room-temperature lead
status_grade: 🟢 (realistic-U room-temp route on a real lattice geometry) / 🟠 (material E_F-alignment+U unverified)
since: 2026-06-14
verification_method: exact Bloch quantum metric per lattice + U-needed-for-300K inversion; numpy ED; p7 $0
sister: RTSC_09, RTSC_10, RTSC_11
verdict: 🟢 kagome flat band <tr g>=1.33 → 상온(300K) 필요 U≈1.24eV = 현실적(강상관 kagome 금속 영역). Lieb 2.94eV 경계. quantum-metric 클수록 상온 현실화 → kagome형이 무냉각 상온상압 RTSC 현실적 리드. 실 후보 CsV3Sb5·FeSn·Co3Sn2S2. 🟠 flat band E_F정렬+강U는 실물질 DFT 미검증.
---
# RTSC_12 — kagome 고-quantum-metric flat band (현실적 상온 리드)
> **가설.** quantum metric이 큰 flat band(kagome)은 현실적 결합 U로 상온상압 SC에 도달할 수 있다.
## 측정 (rtsc_multilattice_closure.py · 정확 대각화)
상온(300K) 필요 U 역산: **kagome <g>=1.33 → U≈1.24 eV (🟢 현실적)** · Lieb <g>=0.56 → 2.94 eV(경계). quantum metric 클수록 U_need 급감.
## 결론
🟢 **돌파 리드** — RTSC_11(Lieb, ~100K)에서 멈춘 게 아니라, **고-quantum-metric kagome flat band은 현실 U(~1.2eV)로 상온 가능권**. quantum-geometry SC의 핵심 = ⟨g⟩ 극대화. 실재 kagome 금속(CsV3Sb5·FeSn·Co3Sn2S2)이 flat band 보유 → 무냉각 상온상압 RTSC의 가장 구체적 현실 리드. 🟠 남은 검증: 실물질서 flat band를 E_F에 정렬 + 충분한 U 확보(QE deck DFT, 동기 분명). 무냉각 RTSC는 미해결이나 **닫힌 게 아니라 kagome로 열림.**
verdict: `RTSC/verdicts/multilattice_closure.txt`
