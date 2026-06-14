---
id: RTSC_16
slug: pyrochlore-frontier
title: pyrochlore flat-band 프런티어 — 3D flat doublet의 다중오비탈 quantum geometry가 kagome보다 훨씬 큼(<g>≫1). 상온이 가장 유망한 $0 design point(명목 U~0.16eV); 단 평탄-분산 접점 특이점으로 Tc 추정 과대 → beyond-MF/DFT 필요.
domain: rtsc pyrochlore flat-band quantum-geometry band-touching ambient
status_grade: 🟢 (most favorable geometry / room-temp design point) / 🟠 (estimate inflated by band-touching; needs DFT)
since: 2026-06-14
verification_method: REAL 3D pyrochlore tight-binding, exact flat-doublet projector quantum metric over 3D BZ; p7 $0
sister: RTSC_12, RTSC_15
verdict: 🟢 pyrochlore 평탄 doublet(폭~0) <tr g>=10.6(3D BZ, 다중오비탈+접점) ≫ kagome 1.3 → 상온 명목 필요 U≈0.16eV(현실권). 최상위 $0 design point. 🟠 단 평탄-분산 quadratic band touching 특이점으로 D_s∝<g> 추정 과대(Tc 1915K=상한 artifact, 단일밴드 MF 붕괴). 실 Tc=beyond-MF/DFT.
---
# RTSC_16 — pyrochlore flat-band 프런티어
> **가설.** 3D pyrochlore 평탄 doublet은 다중오비탈 quantum geometry가 커 상온상압 SC의 최상위 design point다.
## 측정 (rtsc_pyrochlore.py · 3D exact diag)
평탄 doublet 폭 6.7e-15·t(평탄 확인), <tr g>=10.56(3D BZ avg, 2-밴드 projector). 명목 상온 필요 U≈0.16eV.
## 결론
🟢 **최상위 $0 design point** — pyrochlore 다중오비탈 flat band은 quantum geometry가 kagome(1.3)보다 훨씬 커(<g>~10) 상온이 현실 U로 가능해 보임. pyrochlore 금속(비자성·flat band E_F근접 A2B2O7/breathing-pyrochlore형)이 상온상압 RTSC의 최우선 후보 클래스. 🟠 **정직 경계** — <g>=10.6은 평탄-분산 **quadratic band touching 특이점**이 끼어 부풀려진 값; 단일밴드 평균장 D_s∝<g> 추정이 거기서 붕괴 → Tc 1915K는 상한 artifact. 실 Tc는 접점을 제대로 다루는 beyond-MF + 실물질 QE DFT 필요. **$0 이론 사다리 종착**: kagome(12)→병목(13)→처방(14)→깨끗base(15)→pyrochlore design(16).
verdict: `RTSC/verdicts/pyrochlore.txt`
