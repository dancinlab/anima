---
id: RTSC_09
slug: flatband-route
title: flat-band 경로 — Tc∝V(선형, BCS 지수억제 회피)라 상압 무냉각 상온 SC의 가장 유망한 이론 경로(V≈0.1-0.2eV로 300K 그럴듯). 단 현실 flat-band(TBG 1.7K·kagome 2.5K)은 좁/어긋나 미실현.
domain: rtsc flat-band quantum-metric ambient room-temperature
status_grade: 🟢 (mechanism viable) / 🔴 (materials unrealized)
since: 2026-06-14
verification_method: Tc∝V flat-band vs BCS exp-suppression scaling; 🟢 numerical / 🟡 lit
sister: RTSC_08
verdict: 🟢 메커니즘 — flat band은 Tc 선형(BCS exp 억제 회피); 상온 도달 V≈0.10-0.21eV(전형 0.1~1eV 내, 그럴듯). 🔴 미실현 — 현실 flat-band(TBG 1.7K·kagome 2.5K) 밴드 좁고 E_F 어긋남. 프런티어=넓고 견고한 E_F-정렬 flat band.
---
# RTSC_09 — flat-band 경로 (무냉각 상온의 유망 프런티어)
> **가설.** flat band(고/발산 DOS)은 BCS 지수억제를 피해 Tc가 결합에 선형 → 상압서 상온 도달이 그럴듯.
## 측정 (rtsc_flatband_route.py)
flat Tc∝V vs BCS exp: V=0.1eV서 flat 290K vs BCS 4K(66x). 상온 필요 V≈0.10-0.21eV(🟢 그럴듯). 현실: TBG 1.7K·kagome 2.5K (🔴 밴드 좁/어긋남).
## 결론
🟢 **메커니즘 유망** — flat-band SC는 무냉각 상온상압의 가장 그럴듯한 이론 경로(선형 Tc). 🔴 **물질 미실현** — 견고·광폭·E_F정렬 flat band 미발견. 다음 드릴: quantum-metric/geometric SC, moiré/pyrochlore flat-band 설계 (양자+텐션 탐색).
verdict: `RTSC/verdicts/flatband_route.txt`
